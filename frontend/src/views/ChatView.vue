<template>
  <div class="chat-container">
    <!-- 聊天头部 -->
    <div class="chat-header">
      <h2>{{ currentRoom ? currentRoom.name : '聊天室' }}</h2>
      <div class="room-info">
        <span>在线人数: {{ onlineUsers.length }}</span>
      </div>
    </div>
    
    <div class="chat-main">
      <!-- 左侧用户列表 -->
      <div class="user-list">
        <h3>在线用户</h3>
        <ul>
          <li v-for="user in onlineUsers" :key="user.id" class="user-item">
            <img :src="user.avatar || 'default-avatar.png'" :alt="user.username" class="avatar" />
            <span>{{ user.username }}</span>
          </li>
        </ul>
      </div>
      
      <!-- 右侧聊天区域 -->
      <div class="chat-area">
        <!-- 消息显示区域 -->
        <div class="messages-container" ref="messagesContainer">
          <div 
            v-for="message in messages" 
            :key="message.id" 
            :class="['message', message.type]"
          >
            <div v-if="message.type === 'system'" class="system-message">
              {{ message.content }}
            </div>
            <div v-else-if="message.type === 'news'" class="system-message" v-html="renderNewsMessage(message.content)"></div>
            <div v-else-if="message.type === 'music'" class="system-message" v-html="renderMusicMessage(message.content)"></div>
            <div v-else-if="message.type === 'weather'" class="system-message" v-html="renderWeatherMessage(message.content)"></div>
            <div v-else-if="message.type === 'video'" class="system-message">
              <iframe :srcdoc="message.content" width="100%" height="300"></iframe>
            </div>
            <div v-else-if="message.type === 'ai'" class="system-message ai-message">
              <div class="ai-header">AI助手</div>
              <div class="ai-content">{{ message.content }}</div>
            </div>
            <div v-else class="user-message">
              <div class="message-header">
                <span class="username">{{ message.username }}</span>
                <span class="timestamp">{{ message.timestamp }}</span>
              </div>
              <div class="message-content">{{ message.content }}</div>
            </div>
          </div>
        </div>
        
        <!-- 输入区域 -->
        <div class="input-area">
          <div class="input-container">
            <input 
              type="text" 
              v-model="messageInput" 
              @keyup.enter="sendMessage" 
              placeholder="输入消息，或使用指令 @新闻 @听歌 @天气 城市 @视频 url @AI 内容"
            />
            <button @click="sendMessage">发送</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from '../stores/user'
import socket from '../utils/socket'
import apiClient from '../utils/api'

// 组件引用
const messagesContainer = ref(null)

// 状态管理
const route = useRoute()
const userStore = useUserStore()
const chatStore = useChatStore()

// 数据状态
const messageInput = ref('')
const messages = ref([])
const onlineUsers = ref([])
const currentRoom = ref(null)

// 渲染系统消息
const renderSystemMessage = (message) => {
  // 这里可以根据消息类型渲染不同的组件
  return 'div'
}

// 渲染新闻消息
const renderNewsMessage = (newsData) => {
  return `
    <div class="news-card">
      <h4>最新新闻</h4>
      <ul>
        ${newsData.map(item => `
          <li>
            <h5><a href="${item.url}" target="_blank">${item.title}</a></h5>
            <p>${item.desc}</p>
            <div class="news-meta">
              <span>热度: ${item.hot}</span>
            </div>
          </li>
        `).join('')}
      </ul>
    </div>
  `
}

// 渲染音乐消息
const renderMusicMessage = (musicData) => {
  return `
    <div class="music-card">
      <h4>推荐音乐</h4>
      <div class="music-info">
        <h5>${musicData.song}</h5>
        <p>歌手: ${musicData.singer}</p>
        <audio controls>
          <source src="${musicData.Music}" type="audio/mpeg">
          您的浏览器不支持音频播放。
        </audio>
      </div>
    </div>
  `
}

// 渲染天气消息
const renderWeatherMessage = (weatherData) => {
  return `
    <div class="weather-card">
      <h4>${weatherData.city}天气预报</h4>
      <div class="weather-list">
        ${weatherData.data.map(day => `
          <div class="weather-item">
            <h5>${day.date}</h5>
            <p>天气: ${day.weather}</p>
            <p>温度: ${day.temperature}</p>
            <p>风力: ${day.wind}</p>
            <p>空气质量: ${day.air_quality}</p>
          </div>
        `).join('')}
      </div>
    </div>
  `
}

// 发送消息
const sendMessage = () => {
  if (!messageInput.value.trim()) return
  
  const content = messageInput.value.trim()
  messageInput.value = ''
  
  // 处理特殊指令
  if (content.startsWith('@新闻')) {
    handleNewsCommand()
  } else if (content.startsWith('@听歌')) {
    handleMusicCommand()
  } else if (content.startsWith('@天气')) {
    const city = content.substring(4).trim()
    handleWeatherCommand(city)
  } else if (content.startsWith('@视频')) {
    const url = content.substring(4).trim()
    handleVideoCommand(url)
  } else if (content.startsWith('@AI')) {
    const prompt = content.substring(4).trim()
    handleAICommand(prompt)
  } else {
    // 普通消息
    socket.emit('send_message', {
      username: userStore.userInfo.username,
      user_id: userStore.userInfo.id,
      room_id: route.params.roomId,
      content: content
    })
  }
}

// 处理新闻指令
const handleNewsCommand = async () => {
  try {
    // 添加系统消息占位符
    const systemMessage = {
      id: Date.now(),
      type: 'system',
      content: '正在获取新闻...',
      timestamp: new Date().toLocaleTimeString()
    }
    messages.value.push(systemMessage)
    scrollToBottom()
    
    // 调用新闻API
    const response = await fetch('https://v2.xxapi.cn/api/baiduhot')
    const data = await response.json()
    
    if (data.code === 200) {
      // 更新系统消息
      const newsMessage = {
        id: Date.now(),
        type: 'news',
        content: data.data.slice(0, 5), // 只取前5条
        timestamp: new Date().toLocaleTimeString()
      }
      messages.value[messages.value.length - 1] = newsMessage
    } else {
      messages.value[messages.value.length - 1].content = '获取新闻失败'
    }
    scrollToBottom()
  } catch (error) {
    console.error('获取新闻失败:', error)
    messages.value[messages.value.length - 1].content = '获取新闻失败'
    scrollToBottom()
  }
}

// 处理音乐指令
const handleMusicCommand = async () => {
  try {
    // 添加系统消息占位符
    const systemMessage = {
      id: Date.now(),
      type: 'system',
      content: '正在获取音乐...',
      timestamp: new Date().toLocaleTimeString()
    }
    messages.value.push(systemMessage)
    scrollToBottom()
    
    // 调用音乐API
    const response = await fetch('https://api.52vmy.cn/api/music/wy/rand')
    const data = await response.json()
    
    if (data.code === 200) {
      // 更新系统消息
      const musicMessage = {
        id: Date.now(),
        type: 'music',
        content: data.data,
        timestamp: new Date().toLocaleTimeString()
      }
      messages.value[messages.value.length - 1] = musicMessage
    } else {
      messages.value[messages.value.length - 1].content = '获取音乐失败'
    }
    scrollToBottom()
  } catch (error) {
    console.error('获取音乐失败:', error)
    messages.value[messages.value.length - 1].content = '获取音乐失败'
    scrollToBottom()
  }
}

// 处理天气指令
const handleWeatherCommand = async (city) => {
  if (!city) {
    const errorMessage = {
      id: Date.now(),
      type: 'system',
      content: '请指定城市，例如：@天气 北京',
      timestamp: new Date().toLocaleTimeString()
    }
    messages.value.push(errorMessage)
    scrollToBottom()
    return
  }
  
  try {
    // 添加系统消息占位符
    const systemMessage = {
      id: Date.now(),
      type: 'system',
      content: `正在获取${city}天气...`,
      timestamp: new Date().toLocaleTimeString()
    }
    messages.value.push(systemMessage)
    scrollToBottom()
    
    // 调用天气API
    const response = await fetch(`https://v2.xxapi.cn/api/weather?city=${encodeURIComponent(city)}&key=2d5c904b712686d2`)
    const data = await response.json()
    
    if (data.code === 200) {
      // 更新系统消息
      const weatherMessage = {
        id: Date.now(),
        type: 'weather',
        content: data.data,
        timestamp: new Date().toLocaleTimeString()
      }
      messages.value[messages.value.length - 1] = weatherMessage
    } else {
      messages.value[messages.value.length - 1].content = `获取${city}天气失败`
    }
    scrollToBottom()
  } catch (error) {
    console.error('获取天气失败:', error)
    messages.value[messages.value.length - 1].content = `获取${city}天气失败`
    scrollToBottom()
  }
}

// 处理视频指令
const handleVideoCommand = async (url) => {
  if (!url) {
    const errorMessage = {
      id: Date.now(),
      type: 'system',
      content: '请指定视频URL，例如：@视频 https://example.com/video',
      timestamp: new Date().toLocaleTimeString()
    }
    messages.value.push(errorMessage)
    scrollToBottom()
    return
  }
  
  try {
    // 添加系统消息占位符
    const systemMessage = {
      id: Date.now(),
      type: 'system',
      content: '正在解析视频...',
      timestamp: new Date().toLocaleTimeString()
    }
    messages.value.push(systemMessage)
    scrollToBottom()
    
    // 调用视频解析API
    const response = await fetch(`https://jx.playerjy.com?url=${encodeURIComponent(url)}`)
    const html = await response.text()
    
    // 更新系统消息
    const videoMessage = {
      id: Date.now(),
      type: 'video',
      content: html,
      timestamp: new Date().toLocaleTimeString()
    }
    messages.value[messages.value.length - 1] = videoMessage
    scrollToBottom()
  } catch (error) {
    console.error('解析视频失败:', error)
    messages.value[messages.value.length - 1].content = '解析视频失败'
    scrollToBottom()
  }
}

// 处理AI指令
const handleAICommand = async (prompt) => {
  if (!prompt) {
    const errorMessage = {
      id: Date.now(),
      type: 'system',
      content: '请提供AI对话内容，例如：@AI 你好，介绍一下你自己',
      timestamp: new Date().toLocaleTimeString()
    }
    messages.value.push(errorMessage)
    scrollToBottom()
    return
  }
  
  try {
    // 添加系统消息占位符
    const systemMessage = {
      id: Date.now(),
      type: 'system',
      content: '正在与AI对话...',
      timestamp: new Date().toLocaleTimeString()
    }
    messages.value.push(systemMessage)
    scrollToBottom()
    
    // 调用AI聊天API
    const response = await fetch('https://api.siliconflow.cn/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': 'Bearer sk-ixpbuncvthcjoriysusiruafibbiaodapmbkmkuwipglkmbo',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        model: 'THUDM/GLM-4-9B-0414',
        messages: [
          {
            role: 'user',
            content: prompt
          }
        ]
      })
    })
    
    const data = await response.json()
    
    if (data.choices && data.choices.length > 0) {
      // 更新系统消息
      const aiMessage = {
        id: Date.now(),
        type: 'ai',
        content: data.choices[0].message.content,
        timestamp: new Date().toLocaleTimeString()
      }
      messages.value[messages.value.length - 1] = aiMessage
    } else {
      messages.value[messages.value.length - 1].content = 'AI对话失败'
    }
    scrollToBottom()
  } catch (error) {
    console.error('AI对话失败:', error)
    messages.value[messages.value.length - 1].content = 'AI对话失败'
    scrollToBottom()
  }
}

// 滚动到底部
const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

// WebSocket事件监听
onMounted(() => {
  // 加入房间
  socket.emit('join_room', {
    username: userStore.userInfo.username,
    room_id: route.params.roomId
  })
  
  // 监听接收消息
  socket.on('receive_message', (data) => {
    messages.value.push({
      id: Date.now(),
      username: data.username,
      content: data.content,
      timestamp: data.timestamp,
      type: 'user'
    })
    scrollToBottom()
  })
  
  // 监听用户加入
  socket.on('user_joined', (data) => {
    // 这里可以更新在线用户列表
    console.log(`${data.username} 加入了房间`)
  })
  
  // 监听用户离开
  socket.on('user_left', (data) => {
    // 这里可以更新在线用户列表
    console.log(`${data.username} 离开了房间`)
  })
  
  // 获取房间信息
  fetchRoomInfo()
})

// 离开房间
onUnmounted(() => {
  socket.emit('leave_room', {
    username: userStore.userInfo.username,
    room_id: route.params.roomId
  })
  
  // 移除事件监听
  socket.off('receive_message')
  socket.off('user_joined')
  socket.off('user_left')
})

// 获取房间信息
const fetchRoomInfo = async () => {
  try {
    const response = await apiClient.get('/rooms')
    if (response.success) {
      const room = response.rooms.find(r => r.id == route.params.roomId)
      if (room) {
        currentRoom.value = room
      }
    }
  } catch (error) {
    console.error('获取房间信息失败:', error)
  }
}
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background-color: #1890ff;
  color: white;
}

.room-info span {
  font-size: 0.9rem;
}

.chat-main {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.user-list {
  width: 200px;
  border-right: 1px solid #ddd;
  padding: 1rem;
  overflow-y: auto;
}

.user-list h3 {
  margin-top: 0;
}

.user-item {
  display: flex;
  align-items: center;
  margin-bottom: 0.5rem;
}

.avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  margin-right: 0.5rem;
}

.chat-area {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.messages-container {
  flex: 1;
  padding: 1rem;
  overflow-y: auto;
  background-color: #f5f5f5;
}

.message {
  margin-bottom: 1rem;
}

.user-message {
  background: white;
  padding: 0.5rem;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.message-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.25rem;
}

.username {
  font-weight: bold;
  color: #1890ff;
}

.timestamp {
  font-size: 0.8rem;
  color: #999;
}

.system-message {
  background: #e6f7ff;
  padding: 0.5rem;
  border-radius: 4px;
  border-left: 4px solid #1890ff;
}

.news-card {
  background: white;
  border-radius: 4px;
  padding: 1rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.news-card h4 {
  margin-top: 0;
  color: #333;
}

.news-card ul {
  list-style: none;
  padding: 0;
}

.news-card li {
  border-bottom: 1px solid #eee;
  padding: 0.5rem 0;
}

.news-card li:last-child {
  border-bottom: none;
}

.news-card h5 {
  margin: 0 0 0.25rem 0;
}

.news-card h5 a {
  color: #1890ff;
  text-decoration: none;
}

.news-card p {
  margin: 0.25rem 0;
  color: #666;
  font-size: 0.9rem;
}

.news-meta {
  font-size: 0.8rem;
  color: #999;
}

.music-card {
  background: white;
  border-radius: 4px;
  padding: 1rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.music-card h4 {
  margin-top: 0;
  color: #333;
}

.music-info h5 {
  margin: 0 0 0.5rem 0;
  color: #333;
}

.music-info p {
  margin: 0.25rem 0;
  color: #666;
}

.weather-card {
  background: white;
  border-radius: 4px;
  padding: 1rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.weather-card h4 {
  margin-top: 0;
  color: #333;
}

.weather-list {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.weather-item {
  flex: 1;
  min-width: 120px;
  background: #f5f5f5;
  border-radius: 4px;
  padding: 0.5rem;
}

.weather-item h5 {
  margin: 0 0 0.5rem 0;
  color: #333;
}

.weather-item p {
  margin: 0.25rem 0;
  font-size: 0.9rem;
  color: #666;
}

.ai-message {
  background: #f9f0ff;
  border-left: 4px solid #722ed1;
}

.ai-header {
  font-weight: bold;
  color: #722ed1;
  margin-bottom: 0.5rem;
}

.input-area {
  padding: 1rem;
  border-top: 1px solid #ddd;
  background: white;
}

.input-container {
  display: flex;
  gap: 0.5rem;
}

.input-container input {
  flex: 1;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.input-container button {
  padding: 0.5rem 1rem;
  background-color: #1890ff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>