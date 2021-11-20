# coding=utf-8

from pydantic import BaseModel
from typing import Optional, Union
from enum import Enum


class Status(Enum):
    todo = 1
    finished = 0


class Type(Enum):
    todo = 'todo'
    timer = 'timer'


class PostItem(BaseModel):
    """
    type: 'to-do' or 'timer'
    end_time: 10位时间戳
    status: 1 -> to do 2 -> finished
    """
    type: Type
    content: str
    end_time: int
    status: Optional[Status] = Status.todo


class ModifyItem(BaseModel):
    """
    type: 'to-do' or 'timer'
    id: Todo项目的ID
    """
    type: Type
    id: str
    content: Optional[str] = None
    end_time: Optional[int] = None
    status: Optional[Status] = None
