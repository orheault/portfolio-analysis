# Update securities from sec
# ftp://ftp.nasdaqtrader.com/symboldirectory/nasdaqlisted.txt
# ftp://ftp.nasdaqtrader.com/symboldirectory/otherlisted.txt

from ftplib import FTP
from model.base import Session
from model.security import Security
from model.exchange import Exchange
from security_formatter import SecurityFormatter
from sqlalchemy.dialects.postgresql import insert
from tqdm import tqdm

class UsSecurityUpdater:
    def __init__(self):
        self._securityFormatter = SecurityFormatter()
        self._session = Session()

    def __download_file_content(self, url):
        ftp = FTP('ftp.nasdaqtrader.com') 
        ftp.login()
        ftp.retrlines('RETR ' + url, self._securityFormatter) #__split_row

    def execute(self):
        print("Download symbol from nasdaq listed")
        self.__download_file_content('/symboldirectory/nasdaqlisted.txt')
        print("Insert securities")
        self.__insert_nasdaq_securities()
        self._securityFormatter.rows.clear()

        print("Download symbol from nasdaq other listed")
        self.__download_file_content('/symboldirectory/otherlisted.txt')
        print("Insert securities")
        self.__insert_other_securities()

    '''
    DATABASE:
    1,New York Stock Exchange
    2,NYSE MKT
    3,NYSE ARCA
    4,BATS Global Markets
    5,"Investors' Exchange, LLC (IEXG)"

    FTP DATA:
    A = NYSE MKT
    N = New York Stock Exchange (NYSE)
    P = NYSE ARCA
    Z = BATS Global Markets (BATS)
    V = Investors' Exchange, LLC (IEXG)

    '''
    def get_exchange(self, exchange_code):
        # 1 = N
        exchange_id = 1

        if exchange_code == "A":
            exchange_id = 2
        elif exchange_code == "P":
            exchange_id = 3
        elif exchange_code == "Z":
            exchange_id = 4
        elif exchange_code == "V":
            exchange_id = 5

        return exchange_id

    def __get_security_type_id(self, is_etf):
        security_type_id = 1
        if is_etf == 'Y':
            security_type_id = 2
            
        return security_type_id


    def __insert_other_securities(self):
        # Remove first and last row since they are not symbol
        del self._securityFormatter.rows[0]
        del self._securityFormatter.rows[len(self._securityFormatter.rows)-1]

        for row in tqdm(self._securityFormatter.rows):
            symbol = row[0]
            description = row[1]
            exchange = self.get_exchange(row[2])
            security_type_id = self.__get_security_type_id(row[4])
            
            self.__insert(symbol, description, exchange, security_type_id)
    
    def __insert_nasdaq_securities(self):
         # Remove first and last row since they are not symbol
        del self._securityFormatter.rows[0]
        del self._securityFormatter.rows[len(self._securityFormatter.rows)-1]

        for row in tqdm(self._securityFormatter.rows):
            symbol = row[0]
            description = row[1]
            security_type_id = self.__get_security_type_id(row[6])
            
            existing_security = self._session.query(Security).filter(Security.symbol==symbol).filter(Security.exchange_id == Exchange.EXCHANGE_NASDAQ_ID).first()
            if existing_security is None:
                self.__insert(symbol,description, Exchange.EXCHANGE_NASDAQ_ID, security_type_id)
        
    def __insert(self, symbol, description, exchange_id, security_type_id):
        insert_statement = insert(Security).values({Security.symbol:symbol, Security.description: description, Security.exchange_id:exchange_id, Security.security_type_id:security_type_id})
        self._session.execute(insert_statement.on_conflict_do_nothing())
        self._session.commit()

#UsSecurityUpdater().execute()