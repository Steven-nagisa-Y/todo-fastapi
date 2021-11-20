# coding=utf-8
import json


def read_config(file):
    try:
        with open(file, 'r', encoding='utf-8') as f:
            config = json.load(f)
            return config
    except PermissionError as e:
        print("Write Config Permission Error: " + str(e))
        exit(-1)
    except ValueError as e:
        print("Config Value Error: " + str(e))


class Config:
    def __init__(self):
        try:
            self.conf = read_config('Config/conf.json')
            self.__dict__ = self.conf
        except PermissionError as err:
            print("[ERROR] :: Permission Error", err)
        except ValueError as err:
            print("[ERROR] :: Value Error", err)


if __name__ == '__main__':
    conf = Config()
    print(conf.db_user)
