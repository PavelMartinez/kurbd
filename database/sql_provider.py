import os

from string import Template


class SQLProvider:

    def __init__(self, file_path: str):
        self._scripts = {}
        print("file_path " + file_path)  #
        for file in os.listdir(file_path):
            print("filik ---- " + file)  #
            self._scripts[file] = Template(open(f'{file_path}/{file}').read())  #

    def get(self, name: str, **kwargs) -> str:
        if name not in self._scripts:
            raise ValueError(f'No such file {name}')
        return self._scripts[name].substitute(**kwargs)




























"""
                Тут у нас содержится класс sql_provider
                Небходимая штукенция, чтобы корректно достучаться до запросов наших
                при инициализации в объект класса даем путь до папки sql нужного нам блупринта, где хранятся все наши запросы
                Потом этот провайдер впитывает в себя словарём , как !!!!!!!!!ключ - название файла с запросом!!!!!
                                                                     !!!!!!!!! значение - сам sql запрос , но не подставляя пока что переменные!!!
                                                                     
                Когда юзаем get() тогда уже и подставляются все переменные и получается тупо запрос SQL 
"""