import sqlite3
import typing as tp
from datetime import datetime

from pypika import Query, Table, Order


class DataBaseHandler:

    def __init__(self, sql_db_name: str) -> None:
        """
        Initialize all the context for working with database here
        :param sql_db_name: path to the sqlite3 database file
        """
        self.db_name = sql_db_name

    def add_to_history(self, user_id: int, query: str, status: str, movie: str) -> tp.Any:
        history = Table("history")
        query = Query.into(history).columns("user_id", "date", "query", "status", history.movie)\
            .insert(user_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), query, status, movie)
        return self._execute(query, commit=True)

    def get_history_10(self, user_id: int) -> tuple:
        history = Table("history")
        query = Query.from_(history) \
            .select(history.date, history.movie) \
            .where(history.user_id == user_id)\
            .limit(10)
        return self._execute(query, fetchall=True)

    def get_last_record(self, user_id: int):
        history = Table("history")
        query = Query.from_(history) \
            .select(history.movie) \
            .where(history.user_id == user_id)\
            .orderby("date", order=Order.desc)
        return self._execute(query, fetchone=True)[0]

    def _execute(self, query: Query, fetchone=False, fetchall=False, commit=False) -> tp.Any:
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
