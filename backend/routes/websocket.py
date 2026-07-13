from flask import Blueprint
from backend.app import db, socketio
from backend.models.models import User, Room, Message
from datetime import datetime
import json

# 存储房间在线用户 {room_id: [user_ids]}
room_users = {}

# 注册蓝图
from backend.routes.routes import api_bp
from backend.app import app
app.register_blueprint(api_bp, url_prefix='/api')

# WebSocket事件处理
@socketio.on('connect')
def handle_connect():
    print('客户端已连接')

@socketio.on('disconnect')
def handle_disconnect():
    print('客户端已断开连接')

@socketio.on('join_room')
def handle_join_room(data):
    username = data['username']
    room_id = str(data['room_id'])  # 转换为字符串确保一致性
    user_id = data['user_id']
    
    # 加入房间
    socketio.join_room(room_id)
    
    # 更新房间用户列表
    if room_id not in room_users:
        room_users[room_id] = []
    
    # 如果用户不在房间用户列表中，则添加
    if user_id not in room_users[room_id]:
        room_users[room_id].append(user_id)
    
    # 广播用户加入消息
    socketio.emit('user_joined', {
        'username': username, 
        'room_id': room_id,
        'user_id': user_id,
        'online_count': len(room_users[room_id])
    }, room=room_id)
    
    # 发送当前在线用户列表
    socketio.emit('online_users', {
        'users': room_users[room_id],
        'room_id': room_id
    }, room=room_id)

@socketio.on('leave_room')
def handle_leave_room(data):
    username = data['username']
    room_id = str(data['room_id'])
    user_id = data['user_id']
    
    # 离开房间
    socketio.leave_room(room_id)
    
    # 更新房间用户列表
    if room_id in room_users and user_id in room_users[room_id]:
        room_users[room_id].remove(user_id)
    
    # 广播用户离开消息
    socketio.emit('user_left', {
        'username': username, 
        'room_id': room_id,
        'user_id': user_id,
        'online_count': len(room_users.get(room_id, []))
    }, room=room_id)

@socketio.on('send_message')
def handle_send_message(data):
    username = data['username']
    room_id = str(data['room_id'])
    content = data['content']
    user_id = data['user_id']
    
    # 保存消息到数据库
    message = Message(content=content, user_id=user_id, room_id=int(room_id))
    db.session.add(message)
    db.session.commit()
    
    # 发送消息给房间内的所有用户
    message_data = {
        'id': message.id,
        'username': username,
        'content': content,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'type': 'user'
    }
    socketio.emit('receive_message', message_data, room=room_id)