import { create } from 'zustand'
import { persist } from 'zustand/middleware'

export const useAuthStore = create(
  persist(
    (set) => ({
      accessToken: null,
      refreshToken: null,
      player: null,
      setTokens: (accessToken, refreshToken) => set({ accessToken, refreshToken }),
      setPlayer: (player) => set({ player }),
      logout: () => set({ accessToken: null, refreshToken: null, player: null }),
    }),
    { name: 'skillarena-auth' }
  )
)
