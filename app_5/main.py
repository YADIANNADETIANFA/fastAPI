from flask import Flask
from app_5.api.routes import api_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(api_bp, url_prefix='/api')
    return app

app_5 = create_app()


if __name__ == '__main__':
    # 默认，多线程处理
    app_5.run(host="127.0.0.1", port=8000, debug=False, threaded=True)