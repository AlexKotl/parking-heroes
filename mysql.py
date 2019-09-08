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
        
    def get_rows(self, query, data=()):
        ''' Run query and return cursor '''
        with self.db.cursor() as cursor:
            cursor.execute(query, data)
            if int(cursor.rowcount) == 0:
                return False
            return cursor
            
    def get_row(self, query, data=()):
        ''' Get one row and return as dict '''
        res = self.get_rows(query, data)
        if res == False:
            return False
        return res.fetchone()
            
    def query(self, query):
        ''' Alias of get_rows() '''
        return self.get_rows(query)
    
    def insert(self, table, data):
        ''' insert row into table ''' 
        sql = "INSERT INTO {} ({}) VALUES ({})".format(table, ', '.join(data.keys()), ', '.join(('%s' for _ in data)))
        with self.db.cursor() as cursor:
            cursor.execute(sql, list(data.values()))
            self.db.commit()