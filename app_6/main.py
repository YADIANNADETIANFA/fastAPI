from fastapi import FastAPI
from starlette.concurrency import run_in_threadpool
import time
import uvicorn
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import asyncio


# 自定义一个用于处理同步阻塞任务的线程池
# 用于"/run-task-self-pool-1/"和"/run-task-self-pool-2/"
threadpool = ThreadPoolExecutor(max_workers=10)


app_6 = FastAPI(title="My FastAPI App_6", version="1.0.0")


@app_6.get("/run-task/")
async def run_task(name: str = "请求内的同步阻塞任务", sleep_time: float = 10):
    """
    使用Starlette内置的`run_in_threadpool`
    (简洁，稳定可靠，推荐使用)
    """

    def blocking_task(name: str, sleep_time: float):
        print(f"[{name}] 开始执行阻塞任务, {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        time.sleep(sleep_time)
        print(f"[{name}] 阻塞任务结束, {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        return f"{name} 执行完成"

    # `run_in_threadpool()`返回的是一个awaitable协程，表示"等待该任务完成后，返回结果"
    # 因此，这行代码，会在`blocking_task(name, sleep_time)`执行完成后，立即返回
    # 而不是等待线程池内所有任务全部完成后，才返回
    result = await run_in_threadpool(blocking_task, name, sleep_time)

    return {"message": result}


@app_6.get("/run-task-self-pool-1/")
async def run_task_self_pool_1(name: str = "请求内的同步阻塞任务", sleep_time: float = 10):
    """
    使用自定义的线程池
    (与Starlette内置的`run_in_threadpool`功能一致，但更底层，仅推荐学习使用)
    """

    # 获取asyncio event_loop
    loop = asyncio.get_event_loop()

    # 准备任务对象
    task = {
        "input": "hehe",

        # `asyncio.Event()`是asyncio中的异步时事件对象，用来在多个协程之间进行"通知/同步"
        # 它的初始状态是"未设置(unset)"
        "event": asyncio.Event(),

        "result": ""
    }

    # 具体任务内容
    def handle_task(result):
        print(f"[{name}] 开始执行阻塞任务, {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        time.sleep(sleep_time)
        task["result"] = result
        print(f"[{name}] 阻塞任务结束, {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        def async_callback():
            # 设置事件为"已触发(set)"状态
            task["event"].set()

        # 这里是关键
        # 作用："从子线程中，安全地通知主线程事件循环，去做点事情"
        # 因为，不可以在子线程中调用`event.set()`，因为它不是线程安全的异步对象。所以需要让主线程去执行调用`event.set()`
        loop.call_soon_threadsafe(async_callback)

    threadpool.submit(handle_task, "haha")

    # 如果事件当前是"未设置(unset)"状态，则当前协程会被挂起，直到另一个协程调用`event.set()`
    # 如果事件是"已触发(set)"状态，则立即返回，不阻塞
    await task["event"].wait()

    return task["result"]


@app_6.get("/run-task-self-pool-2/")
async def run_task_self_pool_2(name: str = "请求内的同步阻塞任务", sleep_time: float = 10):
    """
    使用自定义的线程池
    (比"/run-task/"更底层；但比"/run-task-self-pool-1/"更简单)
    (Starlette内置的`run_in_threadpool`，底层实际就是`loop.run_in_executor(None, ...)`)
    (同样，仅推荐学习使用)
    """

    # 获取asyncio event_loop
    loop = asyncio.get_event_loop()

    # 准备任务对象
    task = {
        "input": "hehe",
        "result": ""
    }

    # 具体任务内容
    def handle_task():
        print(f"[{name}] 开始执行阻塞任务, {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        task["result"] = "haha"
        time.sleep(sleep_time)
        print(f"[{name}] 阻塞任务结束, {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        return f"{name} 执行完成"

    # 提交并等待结果
    result = await loop.run_in_executor(threadpool, handle_task)

    return {"message": result}


if __name__ == "__main__":
    # 默认，单进程处理
    uvicorn.run("app_6.main:app_6", host="127.0.0.1", port=8000, workers=1)