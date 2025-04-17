from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import time
from datetime import datetime
import asyncio


app_self_tmp = FastAPI(title="my FastAPI app_self_tmp", version="1.0.0")


# 请求输出参数的结构体
class PostRequestData(BaseModel):
    name: str
    email: str



# VPN的问题？  在这里！！！！   不要开启vpn！！！

# 不能使用阻塞任务，否则阻塞会串行堆积在这里

@app_self_tmp.post("/self-post")
async def self_post(request_input: PostRequestData):
    name = request_input.name
    email = request_input.email
    print(f"开始执行阻塞任务, {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    # time.sleep(5)
    await asyncio.sleep(5)
    # raise Exception("手动抛出异常，为了测试@retry重试是否生效")
    print(f"结束阻塞任务, {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    return {"output_name": name, "output_email": email}


if __name__ == '__main__':
    uvicorn.run("app_7.self_tmp_api:app_self_tmp", host="127.0.0.1", port=8001, workers=1)