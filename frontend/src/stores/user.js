import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    userInfo: null,
    isLoggedIn: false
  }),
  
  actions: {
    setUser(userInfo) {
      this.userInfo = userInfo
      this.isLoggedIn = true
    },
    
    logout() {
      this.userInfo = null
      this.isLoggedIn = false
    }
  },
  
  persist: true
})