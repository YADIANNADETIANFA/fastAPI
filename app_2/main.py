from fastapi import FastAPI
from app_2.api.routes import router
import uvicorn

app_2 = FastAPI(title="My FastAPI App_2", version="1.0.0")

app_2.include_router(router)


if __name__ == "__main__":
    # 默认，单进程处理
    uvicorn.run("app_2.main:app_2", host="127.0.0.1", port=8000, workers=1)