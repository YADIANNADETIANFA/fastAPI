from fastapi import APIRouter
import time
from datetime import datetime
import asyncio

router = APIRouter()

# (不推荐的方式) 同步阻塞
@router.get("/sync-time-sleep")
async def syncTimeSleep():
    print(f"******************start: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}**************")
    time.sleep(10)
    print(f"===============request end: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}============")
    return "syncTimeSleep return"


# 异步阻塞
@router.get("/async-time-sleep")
async def asyncTimeSleep():
    print(f"******************start: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}**************")
    await asyncio.sleep(10)
    print(f"===============request end: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}============")
    return "asyncTimeSleep return"