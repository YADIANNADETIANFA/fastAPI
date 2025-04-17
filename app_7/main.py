from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import httpx
import uvicorn
from datetime import datetime
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type


app_7 = FastAPI(title="My FastAPI App_7", version="1.0.0")


# 请求结构体
class RequestData(BaseModel):
    name: str
    email: str


# 请求响应体模版
class ResponseTemplate(BaseModel):
    # 非HTTP状态码，而是业务规定的状态码 (这里规定: 0-请求成功; 1-请求失败)
    code: str = Field(..., description="请求响应业务状态码")
    msg: str = Field(..., description="请求响应信息")
    data: Optional[Dict[str, Any]] = Field(None, description="请求响应数据")





# 异步封装POST请求
# tenacity库原生支持异步函数的重试机制
@retry(stop=stop_after_attempt(3),
       wait=wait_fixed(2),
       # retry=retry_if_exception_type(httpx.RequestError),
       retry=retry_if_exception_type(Exception),        # 如果使用httpx.RequestError，则捕获不到Exception异常
       reraise=True)
async def async_post_request(url: str, payload: dict) -> dict:
    async with httpx.AsyncClient(timeout=100.0) as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        return response.json()

@app_7.post("/api-test")
async def call_api(data: RequestData):
    print(f"服务开始, {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    url = "http://127.0.0.1:8001/self-post"
    try:
        payload = {
            "name": data.name,
            "email": data.email
        }
        result = await async_post_request(url=url, payload=payload)
        print(f"服务结束, {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        return {"success": True, "data": result}
    except Exception as e:
        print(e)
        return {"success": False, "error": str(e)}


if __name__ == '__main__':
    uvicorn.run("app_7.main:app_7", host="127.0.0.1", port=8000, workers=1)