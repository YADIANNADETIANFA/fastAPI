from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class Info(BaseModel):
    phone: str = Field(..., description="用户电话")
    email: str = Field(..., description="用户邮箱")


class User(BaseModel):
    name: str = Field(..., description="用户姓名")
    # 支持嵌套
    info: Optional[Info] = Field(..., description="用户信息")


class RequestUser(BaseModel):
    name: str = Field(..., description="用户姓名")


# 统一的请求响应体模版
class ResponseTemplate(BaseModel):
    # 非HTTP状态码，而是业务规定的状态码 (这里规定: 0-请求成功; 1-请求失败)
    code: int = Field(..., description="请求响应业务状态码")
    msg: str = Field(..., description="请求响应信息")
    data: Optional[Dict[str, Any]] = Field(None, description="请求响应数据")