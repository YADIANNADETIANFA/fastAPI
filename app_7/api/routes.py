from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app_7.models.schemas import User, Info, RequestUser, ResponseTemplate
from datetime import datetime
import time
import asyncio
import httpx
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type


router = APIRouter()


# 异步处理外部接口请求 (注意响应超时时间的控制)
# tenacity库原生支持异步函数重试机制
@retry(stop=stop_after_attempt(3),
       wait=wait_fixed(2),
       retry=retry_if_exception_type(Exception),    # 注意避免异常捕获遗漏
       reraise=True)
async def async_external_request(url: str, payload: dict) -> dict:
    async with httpx.AsyncClient(timeout=120) as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        return response.json()  # 将响应结果转为dict


@router.post("/get-user")
async def get_user(req_user: RequestUser):
    try:
        print(f"服务开始， {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        name = req_user.name
        url = "http://127.0.0.1:8000/api/get-user-info"

        payload = {
            "name": req_user.name
        }
        result = await async_external_request(url=url, payload=payload)
        info = Info.model_validate(result['data']['info'])  # 从dict反序列化为模型对象

        user = User(
            name=name,
            info=info.model_dump()  # 将模型对象转为dict
        )
        response = ResponseTemplate(
            code=0,
            msg="success",
            data={
                "user": user.model_dump()   # 将模型对象转为dict
            }
        )
        print(f"服务结束, {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        return JSONResponse(
            # 自定义HTTP请求状态码
            status_code=200,
            content=response.model_dump()   # 将模型对象转为dict
        )
    except Exception as e:
        print(e)
        response = ResponseTemplate(
            code=1,
            msg="failed",
            data={
                "error": e
            }
        )
        return JSONResponse(
            # 自定义HTTP请求状态码
            status_code=500,
            content=response.model_dump()   # 将模型对象转为dict
        )


@router.post("/get-user-info")
async def get_user_info(req_user: RequestUser):
    try:
        print(f"开始执行用户阻塞任务, {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        name = req_user.name

        # 不能使用阻塞任务，否则阻塞会串行堆积在这里
        # time.sleep(5)

        await asyncio.sleep(5)

        # raise Exception("手动抛出异常，测试@retry重试是否生效")

        info = Info(
            phone="2333",
            email="2333@gmail.com"
        )
        response = ResponseTemplate(
            code=0,
            msg="success",
            data={
                "info": info.model_dump()
            }
        )

        print(f"用户阻塞任务结束, {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        return JSONResponse(
            # 自定义HTTP请求状态码
            status_code=200,
            content=response.model_dump()
        )
    except Exception as e:
        print(e)
        response = ResponseTemplate(
            code=1,
            msg="failed",
            data={
                "error": e
            }
        )
        return JSONResponse(
            # 自定义HTTP请求状态码
            status_code=500,
            content=response.model_dump()
        )
