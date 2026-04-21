"""Initial schema

Revision ID: 001_initial
Revises: 
Create Date: 2025-01-01
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "players",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), primary_key=True),
        sa.Column("username", sa.String(50), unique=True, nullable=False),
        sa.Column("email", sa.String(255), unique=True, nullable=False),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("elo_rating", sa.Integer(), server_default="1200", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("NOW()"), nullable=False),
    )
    op.create_index("idx_players_username", "players", ["username"])
    op.create_index("idx_players_email", "players", ["email"])

    op.execute("""
        CREATE TABLE matches (
            id UUID NOT NULL DEFAULT gen_random_uuid(),
            player_id UUID NOT NULL REFERENCES players(id) ON DELETE CASCADE,
            source VARCHAR(20) NOT NULL CHECK (source IN ('lichess','chesscom','upload')),
            opponent_username VARCHAR(100),
            result VARCHAR(10) NOT NULL CHECK (result IN ('win','loss','draw')),
            opening_name VARCHAR(200), opening_eco VARCHAR(10),
            time_control VARCHAR(30), played_at TIMESTAMPTZ NOT NULL,
            pgn_raw TEXT, metadata JSONB DEFAULT '{}',
            PRIMARY KEY (id, played_at)
        ) PARTITION BY RANGE (played_at)
    """)
    op.execute("CREATE INDEX idx_matches_player_id ON matches (player_id)")
    op.execute("CREATE INDEX idx_matches_played_at ON matches (played_at)")
    op.execute("CREATE INDEX idx_matches_opening_eco ON matches (opening_eco)")

    op.execute("""
        DO $$ DECLARE s DATE:='2024-01-01'; e DATE; n TEXT;
        BEGIN FOR i IN 0..35 LOOP e:=s+INTERVAL '1 month';
        n:='matches_'||TO_CHAR(s,'YYYY_MM');
        EXECUTE FORMAT('CREATE TABLE IF NOT EXISTS %I PARTITION OF matches FOR VALUES FROM (%L) TO (%L)',n,s,e);
        s:=e; END LOOP; END $$
    """)

    op.execute("""
        CREATE TABLE moves (
            id UUID NOT NULL DEFAULT gen_random_uuid(),
            match_id UUID NOT NULL, move_number INT NOT NULL,
            color CHAR(1) NOT NULL CHECK (color IN ('w','b')),
            san VARCHAR(10) NOT NULL, uci VARCHAR(10) NOT NULL,
            fen_before TEXT NOT NULL, fen_after TEXT NOT NULL,
            eval_score FLOAT, move_time_ms INT,
            is_blunder BOOLEAN NOT NULL DEFAULT FALSE,
            is_mistake BOOLEAN NOT NULL DEFAULT FALSE,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            PRIMARY KEY (id, created_at)
        ) PARTITION BY RANGE (created_at)
    """)
    op.execute("CREATE INDEX idx_moves_match_id ON moves (match_id)")
    op.execute("CREATE INDEX idx_moves_is_blunder ON moves (is_blunder) WHERE is_blunder = TRUE")
    op.execute("CREATE INDEX idx_moves_eval_score ON moves (eval_score)")

    op.execute("""
        DO $$ DECLARE s DATE:='2024-01-01'; e DATE; n TEXT;
        BEGIN FOR i IN 0..35 LOOP e:=s+INTERVAL '1 month';
        n:='moves_'||TO_CHAR(s,'YYYY_MM');
        EXECUTE FORMAT('CREATE TABLE IF NOT EXISTS %I PARTITION OF moves FOR VALUES FROM (%L) TO (%L)',n,s,e);
        s:=e; END LOOP; END $$
    """)

    op.create_table("move_annotations",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), primary_key=True),
        sa.Column("move_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("annotation_type", sa.String(20), nullable=False),
        sa.Column("engine_best_move", sa.String(10)),
        sa.Column("eval_delta", sa.Float()),
        sa.Column("annotation_text", sa.Text()),
        sa.CheckConstraint("annotation_type IN ('blunder','inaccuracy','best_move','brilliant')"),
    )
    op.create_index("idx_move_annotations_move_id", "move_annotations", ["move_id"])

    op.create_table("weakness_reports",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), primary_key=True),
        sa.Column("player_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("players.id", ondelete="CASCADE"), nullable=False),
        sa.Column("report_date", sa.Date(), server_default=sa.text("CURRENT_DATE"), nullable=False),
        sa.Column("blunder_rate", sa.Float()), sa.Column("avg_accuracy", sa.Float()),
        sa.Column("weak_openings", postgresql.JSONB(), server_default="'[]'"),
        sa.Column("weak_endgames", postgresql.JSONB(), server_default="'[]'"),
        sa.Column("tactical_patterns", postgresql.JSONB(), server_default="'[]'"),
        sa.Column("generated_at", sa.DateTime(timezone=True)),
    )
    op.create_index("idx_weakness_reports_player_id", "weakness_reports", ["player_id"])

    op.create_table("drills",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), primary_key=True),
        sa.Column("title", sa.String(200), nullable=False), sa.Column("description", sa.Text()),
        sa.Column("difficulty", sa.Integer(), nullable=False),
        sa.Column("category", sa.String(20), nullable=False),
        sa.Column("fen_position", sa.Text(), nullable=False),
        sa.Column("correct_move", sa.String(10), nullable=False),
        sa.Column("explanation", sa.Text()),
        sa.CheckConstraint("difficulty BETWEEN 1 AND 5"),
        sa.CheckConstraint("category IN ('tactic','endgame','opening')"),
    )

    op.create_table("drill_attempts",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), primary_key=True),
        sa.Column("player_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("players.id", ondelete="CASCADE"), nullable=False),
        sa.Column("drill_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("drills.id", ondelete="CASCADE"), nullable=False),
        sa.Column("player_move", sa.String(10), nullable=False),
        sa.Column("is_correct", sa.Boolean(), nullable=False),
        sa.Column("time_taken_ms", sa.Integer()),
        sa.Column("attempted_at", sa.DateTime(timezone=True), server_default=sa.text("NOW()"), nullable=False),
    )
    op.create_index("idx_drill_attempts_player_id", "drill_attempts", ["player_id"])
    op.create_index("idx_drill_attempts_drill_id", "drill_attempts", ["drill_id"])

    op.create_table("recommendations",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), primary_key=True),
        sa.Column("player_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("players.id", ondelete="CASCADE"), nullable=False),
        sa.Column("report_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("weakness_reports.id", ondelete="CASCADE"), nullable=False),
        sa.Column("drill_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("drills.id", ondelete="CASCADE"), nullable=False),
        sa.Column("priority", sa.Integer(), server_default="0", nullable=False),
        sa.Column("reason", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("NOW()"), nullable=False),
    )
    op.create_index("idx_recommendations_player_id", "recommendations", ["player_id"])

    op.execute("""
        CREATE MATERIALIZED VIEW player_stats_mv AS
        SELECT p.id AS player_id, p.username, p.elo_rating,
            COUNT(m.id) AS games_played,
            ROUND(AVG(CASE WHEN wr.avg_accuracy IS NOT NULL THEN wr.avg_accuracy END)::NUMERIC,2) AS avg_accuracy,
            ROUND(COUNT(CASE WHEN m.result='win' THEN 1 END)::NUMERIC/NULLIF(COUNT(m.id),0)*100,2) AS win_rate,
            COUNT(CASE WHEN m.result='win' THEN 1 END) AS wins,
            COUNT(CASE WHEN m.result='loss' THEN 1 END) AS losses,
            COUNT(CASE WHEN m.result='draw' THEN 1 END) AS draws
        FROM players p LEFT JOIN matches m ON m.player_id=p.id
        LEFT JOIN weakness_reports wr ON wr.player_id=p.id
        GROUP BY p.id, p.username, p.elo_rating
    """)
    op.execute("CREATE UNIQUE INDEX idx_player_stats_mv_player_id ON player_stats_mv (player_id)")

    op.execute("""
        CREATE OR REPLACE FUNCTION fn_create_pending_report() RETURNS TRIGGER AS $$
        BEGIN INSERT INTO weakness_reports (player_id, report_date)
        VALUES (NEW.player_id, CURRENT_DATE) ON CONFLICT DO NOTHING; RETURN NEW;
        END; $$ LANGUAGE plpgsql
    """)
    op.execute("""
        CREATE TRIGGER trg_match_insert_report AFTER INSERT ON matches
        FOR EACH ROW EXECUTE FUNCTION fn_create_pending_report()
    """)


def downgrade() -> None:
    op.execute("DROP TRIGGER IF EXISTS trg_match_insert_report ON matches")
    op.execute("DROP FUNCTION IF EXISTS fn_create_pending_report()")
    op.execute("DROP MATERIALIZED VIEW IF EXISTS player_stats_mv")
    op.drop_table("recommendations")
    op.drop_table("drill_attempts")
    op.drop_table("drills")
    op.drop_table("weakness_reports")
    op.drop_table("move_annotations")
    op.execute("DROP TABLE IF EXISTS moves CASCADE")
    op.execute("DROP TABLE IF EXISTS matches CASCADE")
    op.drop_table("players")
