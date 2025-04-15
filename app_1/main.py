from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app_1.api.routes import router
import uvicorn

app_1 = FastAPI(title="My FastAPI App_1", version="1.0.0")

# CORS 中间件配置（前端跨域时必须配置）
app_1.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产建议指定域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app_1.include_router(router, prefix="/api")

if __name__ == "__main__":
    # "app_1.main"为py模块路径，即`app_1/main.py`。具体根据当前工作目录所在位置
    # "app_1"表示这个模块中名为`app_1`的FastAPI实例
    uvicorn.run("app_1.main:app_1", host="127.0.0.1", port=8000)

"""  
访问`http://127.0.0.1:8000/docs`，可获取 Swagger/OpenAPI 文档  

可以在py脚本中启动服务

也可以不定义`if __name__ == "__main__":`，直接在启动脚本`start.sh`中启动服务
`uvicorn app_1.main:app_1 --host 127.0.0.1 --port 8000`
(Docker部署更推荐后者，更专业) (两者功能等价)
"""