# 💬 AI聊天室 (AI Chatroom)

> 一个支持AI智能体交互和局域网通信的实时聊天应用。

这是一个基于 **Vue3 + Flask + WebSocket** 技术栈的**全栈个人项目**。它不仅能实现局域网内的即时通信，还集成了新闻、音乐、天气、视频解析等实用工具，并**特别设计了AI角色扮演对话功能**。

**项目亮点**：
- 🤖 **AI 智能体交互**：通过提示词工程，让AI扮演不同角色进行对话。
- ⚡ **局域网实时通信**：基于WebSocket实现多房间、多用户的即时消息推送。
- 🛠️ **功能聚合工具**：内置新闻、音乐、天气、视频解析等小工具，丰富应用场景。

---

## 📸 演示截图
<img width="1830" height="941" alt="image" src="https://github.com/user-attachments/assets/0a556ec0-cee3-4378-a1fb-c58bb3c6855f" /><img width="1841" height="1985" alt="image" src="https://github.com/user-attachments/assets/98af8637-713a-4b08-b38e-cd83da1f1b6e" /><img width="1833" height="924" alt="image" src="https://github.com/user-attachments/assets/30858a3b-4866-466c-9b45-3ee25caa4e55" />



*(支持智能体对话，查询天气，随机音乐，摸鱼日历，新闻，AI对话等功能)*

## 🎯 项目功能

### 1. 用户系统
- 用户注册/登录、头像选择、用户信息管理
- 基于Session的用户状态保持

### 2. 核心聊天系统
- **房间管理**：用户可创建或加入聊天室
- **实时通信**：基于WebSocket实现消息的实时收发与广播
- **在线状态**：实时显示房间内在线用户列表

### 3. 特色功能（部分需外部API）
- **📰 新闻**：一键获取实时热点新闻
- **🎵 听歌**：随机推荐音乐
- **🌤️ 天气**：查询指定城市天气
- **🎬 视频**：解析视频链接并播放
- **🤖 AI 对话**：与AI智能体进行自然语言交互（支持角色设定）

---

## 🏗️ 技术架构与实现

| 层级 | 技术选型 | 职责 |
| :--- | :--- | :--- |
| **前端** | Vue3 + Vue Router + Pinia + Axios | 构建用户界面，管理状态，发起HTTP/WebSocket请求 |
| **后端** | Flask + Flask-SocketIO + SQLAlchemy | 处理RESTful API，管理WebSocket连接与事件 |
| **数据库** | SQLite | 存储用户信息、聊天记录（如需） |
| **实时通信** | WebSocket (Socket.IO) | 实现双向、低延迟的消息推送 |

**技术难点与思考**：
- **WebSocket 连接管理**：为了解决多房间隔离问题，使用 `Socket.IO` 的房间机制（`room`），将不同聊天室的消息进行逻辑隔离。
- **跨域与代理**：前端通过Vite的代理解决开发环境跨域问题，生产环境则使用Flask-CORS进行统一配置。
- **AI 提示词管理**：将AI角色设定和对话上下文存储在服务端，实现了多轮对话的上下文理解。

---

## 📂 项目结构

```bash
ai_chatroom/
├── backend/                    # Flask 后端
│   ├── app.py                  # 应用入口
│   ├── requirements.txt        # Python依赖
│   ├── models/                 # 数据模型 (SQLAlchemy)
│   ├── routes/                 # 路由与WebSocket事件处理
│   └── prompt_templates/       # AI提示词模板库
├── frontend/                   # Vue3 前端
│   └── ai-chatroom/
│       ├── src/                # 源代码
│       ├── public/             # 静态资源
│       └── package.json        # npm依赖
├── start.bat                   # Windows 一键启动
└── start.sh                    # Linux/Mac 一键启动
```   
---
## 🚀 快速开始

### 环境要求
- Python 3.6+
- Node.js 14+
- npm 6+

### 1. 启动后端
```bash
cd backend
pip install -r requirements.txt
python app.py   # 默认运行在 http://localhost:5000
```
### 2. 启动前端
bash
cd frontend/ai-chatroom
npm install
npm run dev     # 默认运行在 http://localhost:8080
访问 http://localhost:8080 即可使用。

### 🖥️ 使用说明

1.访问 http://localhost:8080 进入登录页面

2.新用户请先注册账号

3.登录后，创建或加入聊天室即可开始聊天

在聊天框中可使用以下指令唤起工具：
```bash
text
@新闻         - 获取热点新闻
@听歌         - 推荐一首音乐
@天气 城市名  - 查询指定城市天气
@视频 视频链接 - 解析并播放视频
@AI 你的问题  - 与AI智能体对话
```
### 📡 API 接口列表
**用户相关**

- POST /api/register - 用户注册

- POST /api/login - 用户登录

**房间相关**

- GET /api/rooms - 获取房间列表

- POST /api/rooms - 创建房间

**功能接口**

- GET /api/news - 获取新闻

- GET /api/music - 获取随机音乐

- GET /api/weather?city=城市名 - 查询天气

- GET /api/video?url=链接 - 解析视频

- POST /api/ai - AI对话

### 📦 生产环境部署
1.构建前端：cd frontend/ai-chatroom && npm run build

2.将构建产物（dist 目录）部署到 Web 服务器

3.配置生产环境的 Flask 应用（如使用 gunicorn）

4.建议使用 Nginx 反向代理，统一处理 80/443 端口请求

## ✅ 当前状态与未来计划
**已完成 (v0.1)**

✅ 基础用户系统与房间管理

✅ WebSocket 实时通信

✅ 工具插件（新闻/音乐/天气/视频）

✅ AI 对话基础交互

**未来计划 (TODO)**

- 优化前端 UI，提升交互体验

- 增加聊天记录持久化存储

- 支持更多的 AI 角色预设

- 添加消息已读/未读状态



## ⚠️ 注意事项
- 请确保防火墙允许 5000 (后端) 和 8080 (前端开发) 端口通信

- 部分 API 功能（如新闻、天气）需要网络访问权限

- **AI 对话功能需要配置有效的 API 密钥**，请在 backend/config.py 中设置

## 📄 License
MIT

🙋 关于作者

本人是信息与计算科学专业大三在校大学生。项目过程中有任何问题或建议，欢迎联系：

GitHub: (https://github.com/fouronP)

📄 详细需求文档请查看：[docs/需求文档.md](./docs/需求文档.md)
