from fastapi import FastAPI
from starlette.concurrency import run_in_threadpool
import time
import uvicorn
from datetime import datetime

app_6 = FastAPI(title="My FastAPI App_6", version="1.0.0")

def blocking_task(name: str, sleep_time: float):
    print(f"[{name}] 开始执行阻塞任务, {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    time.sleep(sleep_time)
    print(f"[{name}] 阻塞任务结束, {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    return f"{name} 执行完成"


@app_6.get("/run-task/")
async def run_task(name: str = "请求内的同步阻塞任务", sleep_time: float = 10):

    # `run_in_threadpool()`返回的是一个awaitable协程，表示"等待该任务完成后，返回结果"
    # 因此，这行代码，会在`blocking_task(name, sleep_time)`执行完成后，立即返回
    # 而不是等待线程池内所有任务全部完成后，才返回
    result = await run_in_threadpool(blocking_task, name, sleep_time)

    return {"message": result}


if __name__ == "__main__":
    # 默认，单进程处理
    uvicorn.run("app_6.main:app_6", host="127.0.0.1", port=8000, workers=1)