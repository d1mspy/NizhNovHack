from infrastructure.db.connect import pg_connection
from sqlalchemy import insert, select, update, delete

class UserRepository:
    def __init__(self):
        self._sessionmaker = pg_connection()