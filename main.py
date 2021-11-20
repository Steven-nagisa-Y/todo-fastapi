# coding=utf-8
from fastapi import FastAPI, Response
from fastapi import status as http_status

import utils
from Model.model import PostItem, Status, Type, ModifyItem
from Database import db

app = FastAPI()


@app.get("/")
async def root():
    return {"status": "ok"}


@app.get("/{user_name}")
async def read_user(user_name: str):
    User = db.User()
    Todo = db.Todo()
    idx = User.store_user(user_name)
    if isinstance(idx, list):
        idx = idx[0]
    all_todo = Todo.get_user(user_name, 'todo')
    all_timer = Todo.get_user(user_name, 'timer')
    count = len(all_todo) + len(all_timer)
    return {
        "status": "ok",
        "userid": idx,
        "data": {
            "count": count,
            "todo": all_todo,
            "timer": all_timer
        }
    }


@app.post("/{user_name}/add")
async def add_todo(user_name: str, item: PostItem):
    User = db.User()
    Todo = db.Todo()
    user_idx = User.store_user(user_name)
    if isinstance(user_idx, list):
        user_idx = user_idx[0]
    uuid = utils.gen_uuid()
    res = Todo.store(item.type.value,
                     user_name,
                     item.content,
                     item.end_time,
                     item.status.value,
                     uuid,
                     )
    if res:
        return {
            "status": "ok",
            "userid": user_idx,
            "data": {
                "id": uuid
            }
        }
    else:
        return {"status": "err", "errMsg": "写入错误"}


@app.post("/{user_name}/modify")
async def modify_todo(user_name: str, item: ModifyItem, response: Response, remove: int = 0):
    User = db.User()
    Todo = db.Todo()
    user_idx = User.store_user(user_name)
    if isinstance(user_idx, list):
        user_idx = user_idx[0]
    if user_idx < 1:
        return {
            "status": "err",
            "errMsg": "该用户为新用户"
        }
    old_todo = Todo.get_todo(item.type.value, item.id)
    if not old_todo:
        return {
            "status": "err",
            "errMsg": "未查到此数据。ID: " + item.id
        }
    if old_todo[0]['name'] != user_name:
        response.status_code = http_status.HTTP_403_FORBIDDEN
        return {
            "status": "err",
            "errMsg": "访问用户错误"
        }
    if remove == 1:
        res = Todo.remove_todo(item.type.value, item.id)
        if res != 0:
            return {
                "status": "ok",
                "data": {
                    "id": item.id
                }
            }
        else:
            return {
                "status": "err",
                "errMsg": "Todo ID错误：" + item.id
            }
    content = item.content or old_todo[0]['content']
    end_time = item.end_time or old_todo[0]['end_time']
    status = item.status.value or old_todo[0]['status']
    res = Todo.store(item.type.value,
                     user_name,
                     content,
                     end_time,
                     status,
                     item.id
                     )
    if res:
        return {
            "status": "ok",
            "userid": user_idx,
            "data": {
                "id": item.id
            }
        }
    else:
        return {"status": "err", "errMsg": "写入错误"}


@app.get("/{user_name}/get")
async def get_todo(user_name: str, type: str, id: str, response: Response):
    User = db.User()
    Todo = db.Todo()
    user_idx = User.store_user(user_name)
    if isinstance(user_idx, list):
        user_idx = user_idx[0]
    if user_idx < 1:
        return {
            "status": "err",
            "errMsg": "该用户为新用户"
        }
    old_todo = Todo.get_todo(type, id)
    if not old_todo:
        return {
            "status": "err",
            "errMsg": "此条Todo不存在，ID: " + id
        }
    if old_todo[0]['name'] != user_name:
        response.status_code = http_status.HTTP_403_FORBIDDEN
        return {
            "status": "err",
            "errMsg": "访问用户错误"
        }
    return {
        "status": "ok",
        "userid": user_idx,
        "data": old_todo[0]
    }
