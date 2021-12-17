# coding-utf=8
import utils
from conf import Config
from tinydb import TinyDB, Query
from Model.model import Status


class User(object):
    def __init__(self):
        config = Config()
        self.db = TinyDB(config.db_user, indent=2, ensure_ascii=False)
        self.all = self.db.all()
        self.q = Query()

    def close(self):
        self.db.close()

    def tables(self):
        return self.db.tables()

    def get_all(self, tb_name):
        return self.db.table(tb_name).all()

    def clear(self, tb_name=None):
        if tb_name:
            tb = self.db.table(tb_name)
            tb.truncate()
        else:
            self.db.truncate()

    def store_user(self, name: str):
        """
        :param name: str
        :return: index in Database
        """
        if utils.check_name(name):
            # 表名为 user
            tb_user = self.db.table('user')
            r = tb_user.search(self.q['name'] == name)
            if r:
                idx = tb_user.update({
                    'last_login': utils.get_time()
                }, self.q['name'] == name)
                return idx
            else:
                idx = tb_user.insert({
                    'name': name,
                    'create_time': utils.get_time(),
                    'last_login': utils.get_time()
                })
                return idx


class Todo:
    def __init__(self):
        config = Config()
        self.db = TinyDB(config.db_todo, indent=2, ensure_ascii=False)
        self.all = self.db.all()
        self.q = Query()

    def close(self):
        self.db.close()

    def tables(self):
        return self.db.tables()

    def get_all(self, tb_name):
        return self.db.table(tb_name).all()

    def get_user(self, name: str, table: str):
        todo = self.db.table(table)
        r = todo.search(self.q['name'] == name)
        return r

    def clear(self, tb_name=None):
        """

        :param tb_name: 可选，不提供时情况所有数据库
        :return: 无
        """
        if tb_name:
            tb = self.db.table(tb_name)
            tb.truncate()
        else:
            self.db.truncate()

    def remove_todo(self, table: str, todo_id: str):
        """
        根据ID删除To-do
        :param table: 表名，对应'to-do' or 'timer'
        :param todo_id: to-do的ID
        :return: 删除值的位置
        """
        tb_todo = self.db.table(table)
        r = tb_todo.search(self.q['id'] == todo_id)
        if r:
            idx = tb_todo.remove(self.q['id'] == todo_id)
            return idx
        else:
            return 0

    def get_todo(self, table: str, todo_id: str):
        """
        根据ID查询To-do
        :param table: 表名，对应'to-do' or 'timer'
        :param todo_id: to-do的ID
        :return:
        """
        tb_todo = self.db.table(table)
        return tb_todo.search(self.q['id'] == todo_id)

    def store(self,
              table: str,
              name: str,
              content: str,
              end_time: int,
              status: int,
              todo_id: str = None,
              ) -> [int]:
        """
        :param table: 表名，对应'to-do' or 'timer'
        :param todo_id: to-do的ID
        :param name: 用户名
        :param content: To-do 内容
        :param end_time: 截止时间，默认10位时间戳
        :param status: 状态：1 未完成 0 已完成
        :return: list(int)
        """
        tb_todo = self.db.table(table)
        r = tb_todo.search(self.q['id'] == todo_id)
        if r:
            idx = tb_todo.update({
                'content': content,
                'end_time': end_time,
                'status': status
            }, self.q['id'] == todo_id)
            return idx
        else:
            idx = tb_todo.insert({
                'id': todo_id,
                'name': name,
                'content': content,
                'create_time': utils.get_time(),
                'end_time': end_time,
                'status': status
            })
            return idx
