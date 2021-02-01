#!/usr/bin/python

class SecurityDAO:

    def __init__(self, database):
        self.database = database

    def insert(self, symbol, description):
        conn = self.database.conn
        cur = self.database.cur

        sql = "INSERT INTO security(symbol, description) VALUES(%s,%s) ON CONFLICT (symbol) DO UPDATE SET description=%s ;"
        
        cur.execute(sql, [symbol, description, description])
        conn.commit()
