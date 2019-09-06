import pymysql
from pymysql.cursors import DictCursor
from contextlib import closing

class MySQL:
    
    def __init__(self):
        self.db = pymysql.connect(
            host='localhost',
            user='root',
            password='root',
            db='parking',
            charset='utf8mb4',
            cursorclass=DictCursor
        )
        
    def get_rows(self, query):
        with self.db.cursor() as cursor:
            cursor.execute(query)
            return cursor