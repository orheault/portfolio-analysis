from security import Security

class SecurityDAO:

    def __init__(self, database):
        self.database = database

    def insert(self, symbol, description):
        conn = self.database.conn
        cur = self.database.cur

        sql = "INSERT INTO security(symbol, description) VALUES(%s,%s) ON CONFLICT (symbol) DO UPDATE SET description=%s ;"
        
        cur.execute(sql, [symbol, description, description])
        conn.commit()

    def get_all(self):
        cur = self.database.conn.cursor()
        cur.execute("SELECT symbol, description FROM security;")
        
        fetch_securities = cur.fetchall()
        securities = []
        for fetch_security in fetch_securities:
            securities.append(Security(fetch_security[0], fetch_security[1]))
        return securities
