import { useState, useEffect, useRef, useCallback } from 'react'
import { useAuthStore } from '../store/authStore'

export function useWebSocket(matchId) {
  const [moves, setMoves] = useState([])
  const [status, setStatus] = useState('disconnected') // disconnected, connecting, connected, ended
  const [gameInfo, setGameInfo] = useState(null)
  const wsRef = useRef(null)
  const accessToken = useAuthStore((s) => s.accessToken)

  const connect = useCallback(() => {
    if (!matchId || !accessToken) return

    const API_BASE = import.meta.env.VITE_API_BASE_URL || ''
    let wsUrl = ''
    if (API_BASE) {
      const url = new URL(API_BASE)
      const wsProtocol = url.protocol === 'https:' ? 'wss:' : 'ws:'
      wsUrl = `${wsProtocol}//${url.host}/ws/analysis/${matchId}?token=${accessToken}`
    } else {
      wsUrl = `${window.location.protocol === 'https:' ? 'wss:' : 'ws:'}//${window.location.host}/ws/analysis/${matchId}?token=${accessToken}`
    }
    setStatus('connecting')
    setMoves([])

    const ws = new WebSocket(wsUrl)
    wsRef.current = ws

    ws.onopen = () => setStatus('connected')

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      switch (data.type) {
        case 'game_start':
          setGameInfo(data)
          break
        case 'move':
          setMoves((prev) => [...prev, data])
          // Send acknowledgment for next move
          ws.send('next')
          break
        case 'game_end':
          setStatus('ended')
          break
        case 'error':
          console.error('WS error:', data.message)
          setStatus('disconnected')
          break
      }
    }

    ws.onclose = () => {
      if (status !== 'ended') setStatus('disconnected')
    }

    ws.onerror = () => setStatus('disconnected')
  }, [matchId, accessToken])

  const disconnect = useCallback(() => {
    if (wsRef.current) {
      wsRef.current.close()
      wsRef.current = null
    }
    setStatus('disconnected')
  }, [])

  useEffect(() => {
    return () => disconnect()
  }, [disconnect])

  return { moves, status, gameInfo, connect, disconnect }
}
