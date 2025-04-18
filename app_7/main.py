from fastapi import FastAPI
from app_7.api.routes import router
import uvicorn


app_7 = FastAPI(title="My FastAPI App_7", version="1.0.0")

# 注册路由
app_7.include_router(router, prefix="/api")


if __name__ == '__main__':
    # "app_7.main"为py模块路径，即`app_7/main.py`。具体根据当前工作目录所在位置
    # "app_7"表示这个模块中名为`app_7`的FastAPI实例
    # uvicorn.run("app_7.main:app_7", host="127.0.0.1", port=8000, workers=1)

    # 对于py脚本内启动服务，推荐直接使用对象 app_7
    uvicorn.run(app_7, host="127.0.0.1", port=8000, workers=1)


"""  
访问`http://127.0.0.1:8000/docs`，可获取 Swagger/OpenAPI 文档  

可以在py脚本中启动服务

也可以不定义`if __name__ == "__main__":`，直接在启动脚本`start.sh`中启动服务
`uvicorn app_7.main:app_7 --host 127.0.0.1 --port 8000`
(Docker部署更推荐后者，更专业) (两者功能等价)
"""