from fastapi import FastAPI
from app_4.api.routes import router
import uvicorn

app_4 = FastAPI(title="My FastAPI App_4", version="1.0.0")

app_4.include_router(router)


if __name__ == "__main__":
    # 多进程处理
    uvicorn.run("app_4.main:app_4", host="127.0.0.1", port=8000, workers=5)