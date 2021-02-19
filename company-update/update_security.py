# Update securities from sec
# ftp://ftp.nasdaqtrader.com/symboldirectory/nasdaqlisted.txt
# ftp://ftp.nasdaqtrader.com/symboldirectory/otherlisted.txt

from ftplib import FTP
from model.base import Session
from model.company_security import CompanySecurity
from security_formatter import SecurityFormatter
from sqlalchemy.dialects.postgresql import insert
from tqdm import tqdm

class SecurityUpdater:
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
        self.__insert_securities(self._securityFormatter.rows)
        self._securityFormatter.rows.clear()

        print("Download symbol from nasdaq other listed")
        self.__download_file_content('/symboldirectory/otherlisted.txt')
        print("Insert securities")
        self.__insert_securities(self._securityFormatter.rows)

        self._session.close()

    def __insert_securities(self, rows):
        # Remove first and last row since they are not symbol
        del rows[0]
        del rows[len(rows)-1]

        for row in tqdm(rows):
            symbol = row[0]
            description = row[1]
            
            security = CompanySecurity(symbol, description)
            insert_statement = insert(CompanySecurity).values({CompanySecurity.symbol:symbol, CompanySecurity.description: description})
            self._session.execute(insert_statement.on_conflict_do_nothing())
        
        self._session.commit()


SecurityUpdater().execute()