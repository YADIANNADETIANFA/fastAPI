from flask import Blueprint, request, jsonify
from app_5.models.schemas import User
from datetime import datetime
import time
import threading


api_bp = Blueprint('api', __name__)


@api_bp.route('/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Hello, Flask!"})


@api_bp.route('/user', methods=['POST'])
def create_user():
    try:
        data = request.json
        user = User(**data)
        return jsonify({"username": user.username, "email": user.email})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@api_bp.route('/sync-time-sleep', methods=['GET'])
def sync_time_sleep():
    """
    同步阻塞
    client端10个并发请求
    整体等待时间：10s
    有多少个HTTP请求，server就起了多少个线程，多线程并行处理
    """

    print(threading.current_thread())

    print(f"******************start: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}**************")
    time.sleep(10)
    print(f"===============request end: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}============")
    return jsonify({"message": "syncTimeSleep return"})