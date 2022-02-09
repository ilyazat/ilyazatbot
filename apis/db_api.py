import sqlite3
import typing as tp
from datetime import datetime

import aiohttp
from pypika import Query, Table, Order, PostgreSQLQuery
from aiogram import types
import psycopg2
from .imdb_api import IMDbMovieInfo


class DataBaseHandler:

    def __init__(self, sql_db_name: str) -> None:
        """
        Initialize all the context for working with database here
        :param sql_db_name: path to the sqlite3 database file
        """
        self.db_name = sql_db_name

    def add_to_history(self, user_id: int, query: str, status: str, movie: str):
        history = Table("history")
        query = Query.into(history).columns("user_id", "date", "query", "status", history.movie) \
            .insert(user_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), query, status, movie)
        return self._execute(query, commit=True)

    def get_ok_queries(self, user_query: str):
        history = Table("history")
        query = Query.from_(history).select(history.query) \
            .where(history.query == user_query) \
            .where(history.status == "OK")
        return self._execute(query, fetchall=True)

    def get_movie_from_query(self, user_query: str) -> tuple:
        history = Table("history")
        query = Query.from_(history).select(history.movie) \
            .where(history.query == user_query) \
            .where(history.status == "OK")
        return self._execute(query, fetchall=True)

    def get_history_10(self, user_id: int):
        history = Table("history")
        query = Query.from_(history) \
            .select(history.date, history.movie) \
            .where(history.user_id == user_id) \
            .limit(10)
        return self._execute(query, fetchall=True)

    def get_last_record(self, user_id: int):
        history = Table("history")
        query = Query.from_(history) \
            .select(history.movie) \
            .where(history.user_id == user_id) \
            .orderby("date", order=Order.desc)
        return self._execute(query, fetchone=True)[0]

    def _execute(self, query: Query, fetchone=False, fetchall=False, commit=False):
        connection = sqlite3.connect(self.db_name)
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

    # def cash_movie(self, info: IMDbMovieInfo):
    #     add_movie = PostgreSQLQuery.into(self.movie) \
    #         .insert(info.id,
    #                 info.fullTitle,
    #                 info.type,
    #                 info.plot,
    #                 info.image,
    #                 info.imDbRating)
    #     self._execute(add_movie, commit=True)
    #
    # def get_cash(self, req: str):
    #     query = PostgreSQLQuery.from_(self.requests) \
    #         .where(req == self.requests.query_text) \
    #         .where(self.requests.status == True)\
    #         .select(self.requests.movie_id)\
    #         .inner_join(self.movie).on(self.requests.movie_id == self.movie.id)


    # def get_queries_list(self):
    #     query = PostgreSQLQuery.from_(self.requests).select(self.requests.query_text)
    #     return [q[0] for q in self._execute(query, fetchall=True)]

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
