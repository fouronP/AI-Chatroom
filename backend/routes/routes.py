from flask import Blueprint, request, jsonify
from backend.app import db, socketio
from backend.models.models import User, Room, Message
import hashlib
import requests
from datetime import datetime

api_bp = Blueprint('api', __name__)

# 用户注册
@api_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    avatar = data.get('avatar', '')
    
    # 检查用户名是否已存在
    if User.query.filter_by(username=username).first():
        return jsonify({'success': False, 'message': '用户名已存在'}), 400
    
    # 创建新用户
    hashed_password = hashlib.md5(password.encode()).hexdigest()
    new_user = User(username=username, password=hashed_password, avatar=avatar)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'success': True, 'message': '注册成功'}), 201

# 用户登录
@api_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # 验证用户
    hashed_password = hashlib.md5(password.encode()).hexdigest()
    user = User.query.filter_by(username=username, password=hashed_password).first()
    
    if user:
        return jsonify({'success': True, 'message': '登录成功', 'user': {
            'id': user.id,
            'username': user.username,
            'avatar': user.avatar
        }}), 200
    else:
        return jsonify({'success': False, 'message': '用户名或密码错误'}), 401

# 获取所有房间
@api_bp.route('/rooms', methods=['GET'])
def get_rooms():
    rooms = Room.query.all()
    room_list = []
    for room in rooms:
        # 获取房间创建者信息
        creator = User.query.get(room.creator_id)
        # 获取房间在线人数（简化处理，实际应该通过WebSocket连接统计）
        online_count = 1  # 默认至少有创建者
        
        room_list.append({
            'id': room.id,
            'name': room.name,
            'creator': creator.username if creator else 'Unknown',
            'online_count': online_count,
            'created_at': room.created_at.isoformat()
        })
    
    return jsonify({'success': True, 'rooms': room_list}), 200

# 创建房间
@api_bp.route('/rooms', methods=['POST'])
def create_room():
    data = request.get_json()
    name = data.get('name')
    creator_id = data.get('creator_id')
    
    # 检查房间名是否已存在
    if Room.query.filter_by(name=name).first():
        return jsonify({'success': False, 'message': '房间名已存在'}), 400
    
    # 创建新房间
    new_room = Room(name=name, creator_id=creator_id)
    db.session.add(new_room)
    db.session.commit()
    
    # 返回创建的房间信息
    creator = User.query.get(creator_id)
    room_info = {
        'id': new_room.id,
        'name': new_room.name,
        'creator': creator.username if creator else 'Unknown',
        'online_count': 1,
        'created_at': new_room.created_at.isoformat()
    }
    
    return jsonify({'success': True, 'message': '房间创建成功', 'room': room_info}), 201

# 获取新闻
@api_bp.route('/news', methods=['GET'])
def get_news():
    try:
        response = requests.get('https://v2.xxapi.cn/api/baiduhot', timeout=10)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# 获取音乐
@api_bp.route('/music', methods=['GET'])
def get_music():
    try:
        response = requests.get('https://api.52vmy.cn/api/music/wy/rand', timeout=10)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# 获取天气
@api_bp.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    key = '2d5c904b712686d2'
    
    if not city:
        return jsonify({'success': False, 'message': '缺少城市参数'}), 400
    
    try:
        response = requests.get(f'https://v2.xxapi.cn/api/weather?city={city}&key={key}', timeout=10)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# 解析视频
@api_bp.route('/video', methods=['GET'])
def parse_video():
    url = request.args.get('url')
    
    if not url:
        return jsonify({'success': False, 'message': '缺少URL参数'}), 400
    
    try:
        response = requests.get(f'https://jx.playerjy.com?url={url}', timeout=10)
        return jsonify({'success': True, 'html': response.text}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# AI聊天
@api_bp.route('/ai', methods=['POST'])
def ai_chat():
    data = request.get_json()
    content = data.get('content')
    
    if not content:
        return jsonify({'success': False, 'message': '缺少内容参数'}), 400
    
    try:
        headers = {
            'Authorization': 'Bearer sk-ixpbuncvthcjoriysusiruafibbiaodapmbkmkuwipglkmbo',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'model': 'THUDM/GLM-4-9B-0414',
            'messages': [
                {
                    'role': 'user',
                    'content': content
                }
            ]
        }
        
        response = requests.post(
            'https://api.siliconflow.cn/v1/chat/completions',
            headers=headers,
            json=payload,
            timeout=30
        )
        
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500