@echo off
REM 启动AI聊天室应用

echo 正在启动AI聊天室应用...

REM 创建并激活Python虚拟环境
echo 创建Python虚拟环境...
python -m venv venv

echo 激活虚拟环境...
call venv\Scripts\activate

REM 安装Python依赖
echo 安装Python依赖...
pip install -r requirements.txt

REM 启动Flask后端
echo 启动Flask后端服务...
start python app.py

REM 等待后端启动
timeout /t 3 /nobreak >nul

REM 启动Vue前端
echo 启动Vue前端开发服务器...
cd ../frontend/ai-chatroom
npm install
npm run dev

echo 应用启动完成！