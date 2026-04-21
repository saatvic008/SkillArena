import { create } from 'zustand'

export const useGameStore = create((set) => ({
  matches: [],
  currentMatch: null,
  currentMoves: [],
  currentMoveIndex: -1,
  setMatches: (matches) => set({ matches }),
  setCurrentMatch: (match) => set({ currentMatch: match }),
  setCurrentMoves: (moves) => set({ currentMoves: moves }),
  setCurrentMoveIndex: (index) => set({ currentMoveIndex: index }),
  nextMove: () => set((s) => ({
    currentMoveIndex: Math.min(s.currentMoveIndex + 1, s.currentMoves.length - 1)
  })),
  prevMove: () => set((s) => ({
    currentMoveIndex: Math.max(s.currentMoveIndex - 1, -1)
  })),
  resetGame: () => set({ currentMatch: null, currentMoves: [], currentMoveIndex: -1 }),
}))
