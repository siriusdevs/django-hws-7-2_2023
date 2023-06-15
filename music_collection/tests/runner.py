from django.test.runner import DiscoverRunner
from django.db import connections
from types import MethodType


def prepare_db(self):
    self.connect()
    self.connection.cursor().execute('CREATE SCHEMA IF NOT EXISTS collection;')


class PostgresSchemaRunner(DiscoverRunner):

    def setup_databases(self, **kwargs):
        for conn_name in connections:
            conn = connections[conn_name]
            conn.prepare_database = MethodType(prepare_db, conn)
        return super().setup_databases(**kwargs)
    
    
# Этот код определяет пользовательский тестовый раннер для Django, 
# который настраивает базу данных Postgres перед запуском тестов. 
# Он добавляет метод "prepare_db" к каждому соединению базы данных 
# и вызывает его во время настройки базы данных перед запуском тестов. 
# Метод "prepare_db" создает схему "collection", если ее еще нет в базе данных.