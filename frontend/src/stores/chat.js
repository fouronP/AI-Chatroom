import { defineStore } from 'pinia'

export const useChatStore = defineStore('chat', {
  state: () => ({
    currentRoom: null,
    messages: [],
    onlineUsers: []
  }),
  
  actions: {
    setCurrentRoom(room) {
      this.currentRoom = room
    },
    
    addMessage(message) {
      this.messages.push(message)
    },
    
    setMessages(messages) {
      this.messages = messages
    },
    
    setOnlineUsers(users) {
      this.onlineUsers = users
    },
    
    addUser(user) {
      if (!this.onlineUsers.find(u => u.id === user.id)) {
        this.onlineUsers.push(user)
      }
    },
    
    removeUser(userId) {
      this.onlineUsers = this.onlineUsers.filter(u => u.id !== userId)
    }
  }
})