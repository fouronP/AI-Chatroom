<template>
  <div class="register-container">
    <div class="register-form">
      <h2>用户注册</h2>
      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label for="username">用户名:</label>
          <input 
            type="text" 
            id="username" 
            v-model="username" 
            required 
            placeholder="请输入用户名"
          />
        </div>
        <div class="form-group">
          <label for="password">密码:</label>
          <input 
            type="password" 
            id="password" 
            v-model="password" 
            required 
            placeholder="请输入密码"
          />
        </div>
        <div class="form-group">
          <label for="avatar">头像:</label>
          <select id="avatar" v-model="avatar">
            <option value="">选择头像</option>
            <option value="avatar1.png">头像1</option>
            <option value="avatar2.png">头像2</option>
            <option value="avatar3.png">头像3</option>
          </select>
        </div>
        <button type="submit" class="register-btn">注册</button>
        <p class="login-link">
          已有账号？<router-link to="/">立即登录</router-link>
        </p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '../utils/api'

const username = ref('')
const password = ref('')
const avatar = ref('')
const router = useRouter()

const handleRegister = async () => {
  try {
    const response = await apiClient.post('/register', {
      username: username.value,
      password: password.value,
      avatar: avatar.value
    })
    
    if (response.success) {
      alert('注册成功，请登录')
      router.push('/')
    } else {
      alert(response.message)
    }
  } catch (error) {
    console.error('注册失败:', error)
    alert('注册失败，请检查网络连接')
  }
}
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f0f2f5;
}

.register-form {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

h2 {
  text-align: center;
  margin-bottom: 1.5rem;
  color: #333;
}

.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  color: #555;
}

input, select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.register-btn {
  width: 100%;
  padding: 0.75rem;
  background-color: #52c41a;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  margin-top: 1rem;
}

.register-btn:hover {
  background-color: #73d13d;
}

.login-link {
  text-align: center;
  margin-top: 1rem;
}

a {
  color: #1890ff;
  text-decoration: none;
}
</style>