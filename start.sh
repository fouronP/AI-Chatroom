#!/bin/bash
# 启动AI聊天室应用

echo "正在启动AI聊天室应用..."

# 创建并激活Python虚拟环境
echo "创建Python虚拟环境..."
python -m venv venv

echo "激活虚拟环境..."
source venv/bin/activate

# 安装Python依赖
echo "安装Python依赖..."
pip install -r requirements.txt

# 启动Flask后端
echo "启动Flask后端服务..."
python app.py &

# 等待后端启动
sleep 3

# 启动Vue前端
echo "启动Vue前端开发服务器..."
cd ../frontend/ai-chatroom
npm install
npm run dev

echo "应用启动完成！"