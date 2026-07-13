import { io } from 'socket.io-client'

// 创建WebSocket连接
const socket = io('http://localhost:5000', {
  transports: ['websocket']
})

export default socket