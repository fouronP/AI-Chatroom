import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import RoomListView from '../views/RoomListView.vue'
import ChatView from '../views/ChatView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'login',
      component: LoginView
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView
    },
    {
      path: '/rooms',
      name: 'rooms',
      component: RoomListView
    },
    {
      path: '/chat/:roomId',
      name: 'chat',
      component: ChatView,
      props: true
    }
  ]
})

export default router