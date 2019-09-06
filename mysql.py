import pymysql
from pymysql.cursors import DictCursor
from contextlib import closing
import os

class MySQL:
    
    def __init__(self):
        self.db = pymysql.connect(
            host=os.environ['DB_HOST'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD'],
            db=os.environ['DB_NAME'],
            charset='utf8mb4',
            cursorclass=DictCursor
        )
        
    def get_rows(self, query):
        ''' Run query and return cursor '''
        with self.db.cursor() as cursor:
            cursor.execute(query)
            return cursor
            
    def query(self, query):
        ''' Alias of get_rows() '''
        return self.get_rows(query)
    
