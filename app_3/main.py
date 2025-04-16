from flask import Flask
from app_3.api.routes import api_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(api_bp, url_prefix='/api')
    return app

app_3 = create_app()


if __name__ == '__main__':
    # 单线程处理
    app_3.run(host="127.0.0.1", port=8000, debug=False, threaded=False)