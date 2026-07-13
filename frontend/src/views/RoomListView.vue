<template>
  <div class="room-list-container">
    <div class="header">
      <h2>房间列表</h2>
      <button class="create-room-btn" @click="showCreateRoomModal = true">创建房间</button>
    </div>
    
    <div class="room-list">
      <div 
        class="room-item" 
        v-for="room in rooms" 
        :key="room.id"
        @click="joinRoom(room)"
      >
        <div class="room-info">
          <h3>{{ room.name }}</h3>
          <p>创建者: {{ room.creator }}</p>
          <p>在线人数: {{ room.online_count }}</p>
        </div>
        <button class="join-btn">加入房间</button>
      </div>
    </div>
    
    <!-- 创建房间模态框 -->
    <div v-if="showCreateRoomModal" class="modal">
      <div class="modal-content">
        <h3>创建房间</h3>
        <form @submit.prevent="createRoom">
          <div class="form-group">
            <label for="roomName">房间名称:</label>
            <input 
              type="text" 
              id="roomName" 
              v-model="newRoomName" 
              required 
              placeholder="请输入房间名称"
            />
          </div>
          <div class="modal-actions">
            <button type="button" @click="showCreateRoomModal = false">取消</button>
            <button type="submit">创建</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import apiClient from '../utils/api'

const rooms = ref([])
const showCreateRoomModal = ref(false)
const newRoomName = ref('')
const router = useRouter()
const userStore = useUserStore()

// 获取房间列表
const fetchRooms = async () => {
  try {
    const response = await apiClient.get('/rooms')
    if (response.success) {
      rooms.value = response.rooms
    }
  } catch (error) {
    console.error('获取房间列表失败:', error)
  }
}

// 加入房间
const joinRoom = (room) => {
  router.push(`/chat/${room.id}`)
}

// 创建房间
const createRoom = async () => {
  try {
    const response = await apiClient.post('/rooms', {
      name: newRoomName.value,
      creator_id: userStore.userInfo.id
    })
    
    if (response.success) {
      showCreateRoomModal.value = false
      newRoomName.value = ''
      fetchRooms() // 重新获取房间列表
      router.push(`/chat/${response.room.id}`)
    } else {
      alert(response.message)
    }
  } catch (error) {
    console.error('创建房间失败:', error)
    alert('创建房间失败，请检查网络连接')
  }
}

onMounted(() => {
  fetchRooms()
})
</script>

<style scoped>
.room-list-container {
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.header h2 {
  margin: 0;
}

.create-room-btn {
  padding: 0.5rem 1rem;
  background-color: #1890ff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.create-room-btn:hover {
  background-color: #40a9ff;
}

.room-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.room-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
}

.room-item:hover {
  background-color: #f5f5f5;
}

.room-info h3 {
  margin: 0 0 0.5rem 0;
  color: #333;
}

.room-info p {
  margin: 0.25rem 0;
  color: #666;
  font-size: 0.9rem;
}

.join-btn {
  padding: 0.5rem 1rem;
  background-color: #52c41a;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.join-btn:hover {
  background-color: #73d13d;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  width: 100%;
  max-width: 400px;
}

.modal-content h3 {
  margin-top: 0;
}

.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  color: #555;
}

input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1rem;
}

.modal-actions button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.modal-actions button:first-child {
  background-color: #f0f0f0;
  color: #333;
}

.modal-actions button:last-child {
  background-color: #1890ff;
  color: white;
}
</style>