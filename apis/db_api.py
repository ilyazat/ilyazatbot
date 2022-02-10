import sqlite3
import typing as tp
from datetime import datetime

import aiohttp
from pypika import Query, Table, Order, PostgreSQLQuery
from aiogram import types
import psycopg2
from .imdb_api import IMDbMovieInfo


class Postgres:

    def __init__(self, sql_db_name: str, password: str, user: str = "postgres", host: str = "localhost") -> None:
        """
        Initialize all the context for working with database here
        :param sql_db_name: path to the sqlite3 database file
        """
        self.db_name = sql_db_name
        self.host = host
        self.user = user
        self.password = password
        self.requests = Table("requests")
        self.users = Table("users")
        self.movie = Table("movie")

        self._execute(
        "CREATE TABLE IF NOT EXISTS requests(id serial primary key, user_id integer not null, date varchar(50), query_text varchar(50), status boolean, movie_id varchar(20));")
        self._execute("CREATE TABLE IF NOT EXISTS users(user_id integer primary key, name varchar(50));")

    def add_to_history(self, message: types.Message, status: bool, movie_id: str) -> None:
        add_to_test1 = PostgreSQLQuery.into(self.requests). \
            columns("user_id", "date", "query_text", "status", "movie_id"). \
            insert(message.from_user.id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message.text, status, movie_id)
        self._execute(add_to_test1, commit=True)
        add_to_users = PostgreSQLQuery.into(self.users) \
            .insert(message.from_user.id, message.from_user.full_name) \
            .on_conflict(self.users.user_id) \
            .do_update(self.users.name, message.from_user.first_name)
        self._execute(add_to_users, commit=True)

    def get_users(self):
        users = Table("users")
        return self._execute(PostgreSQLQuery.from_(users).select(users.user_id))

    def get_history_10(self, user_id: int):
        query = PostgreSQLQuery.from_(self.requests) \
            .select(self.requests.date, self.requests.query_text) \
            .where(self.requests.user_id == user_id) \
            .limit(10)
        return self._execute(query, fetchall=True)

    def _execute(self, query: PostgreSQLQuery, fetchone=False, fetchall=False, commit=False):
        connection = psycopg2.connect(host=self.host,
                                      user=self.user,
                                      password=self.password,
                                      database=self.db_name)
        cursor = connection.cursor()
        cursor.execute(str(query))
        data = None
        if commit:
            connection.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        connection.close()
        return data
