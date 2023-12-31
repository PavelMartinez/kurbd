from typing import Optional

from pymysql import connect
from pymysql.cursors import Cursor
from pymysql.connections import Connection
from pymysql.err import OperationalError


class UseDatabase:

    def __init__(self, config: dict):
        self.config = config
        self.conn: Optional[Connection] = None
        self.cursor: Optional[Cursor] = None

    def __enter__(self) -> Optional[Cursor]:
        try:
            self.conn = connect(**self.config)
            self.cursor = self.conn.cursor()
            self.conn.begin()
            return self.cursor
        except OperationalError as err:
            if err.args[0] == 1045:
                print('Проверьте логин / пароль')
            elif err.args[0] == 1049:
                print('Проверьте имя базы данных')
            else:
                print(err)
            return None

    def __exit__(self, exc_type, exc_val, exc_tr) -> bool:
        if exc_type:
            print(f"Error type: {exc_type.__name__}")
            print(f"DB error: {' '.join(exc_val.args)}")

        if self.conn and self.cursor:
            if exc_type:
                self.conn.rollback()
            else:
                self.conn.commit()
            self.conn.close()
            self.cursor.close()
        return True




































"""
        Тут у нас хранится все нужное для подключения и работы с бд
        Конструктор, инициализатор, деструктор
        в конструкторе (__init__) чисто задаем начальные настройки
        в __enter__ уже инициализируем все необходимое для работы с бд (курсор и соединение с бд)
        в деструкторе (__exit__) чисто выходим из бд и разрываем с ней все соединения
"""