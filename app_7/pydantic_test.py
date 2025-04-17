from typing import Optional, Union, List
from pydantic import BaseModel, Field


class User(BaseModel):
    # `id`为必填字段，类型为int
    id: int = Field(..., description="用户id")

    # `name`为必填字段，类型为str，最大长度为20
    name: str = Field(..., max_length=20, description="用户姓名")

    # `age`为非必填字段，默认为None，类型可以为int或None，0≤age≤150
    # "Optional[int]" 等价于 "Union[int, None]"
    age: Optional[int] = Field(None, ge=0, le=150, description="用户年龄")

    # `tag`为非必填字段，默认为None，类型可以为str或List[str]或None
    tags: Optional[Union[str, List[str]]] = Field(None, description="用户标签")