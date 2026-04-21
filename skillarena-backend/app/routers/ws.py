import uuid
import asyncio
import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSessionLocal
from app.models.move import Move
from app.utils.auth_utils import decode_token

router = APIRouter()


@router.websocket("/ws/analysis/{match_id}")
async def websocket_analysis(
    websocket: WebSocket,
    match_id: uuid.UUID,
    token: str = Query(...),
):
    # Validate JWT from query param
    try:
        payload = decode_token(token)
        if payload.get("type") != "access":
            await websocket.close(code=4001, reason="Invalid token type")
            return
    except Exception:
        await websocket.close(code=4001, reason="Authentication failed")
        return

    await websocket.accept()

    try:
        async with AsyncSessionLocal() as db:
            result = await db.execute(
                select(Move)
                .where(Move.match_id == match_id)
                .order_by(Move.move_number, Move.color)
            )
            moves = result.scalars().all()

            if not moves:
                await websocket.send_json({"type": "error", "message": "No moves found"})
                await websocket.close()
                return

            # Send game metadata
            await websocket.send_json({
                "type": "game_start",
                "total_moves": len(moves),
                "match_id": str(match_id),
            })

            # Stream moves one-by-one with delay for replay effect
            for i, move in enumerate(moves):
                move_data = {
                    "type": "move",
                    "move_number": move.move_number,
                    "color": move.color,
                    "san": move.san,
                    "uci": move.uci,
                    "fen_before": move.fen_before,
                    "fen_after": move.fen_after,
                    "eval_score": move.eval_score,
                    "is_blunder": move.is_blunder,
                    "is_mistake": move.is_mistake,
                    "index": i,
                }
                await websocket.send_json(move_data)

                # Wait for client acknowledgment or auto-advance after 1.5s
                try:
                    await asyncio.wait_for(websocket.receive_text(), timeout=1.5)
                except asyncio.TimeoutError:
                    pass

            await websocket.send_json({"type": "game_end"})

    except WebSocketDisconnect:
        pass
    except Exception as e:
        try:
            await websocket.send_json({"type": "error", "message": str(e)})
        except Exception:
            pass
    finally:
        try:
            await websocket.close()
        except Exception:
            pass
