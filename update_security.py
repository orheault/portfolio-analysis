
# Update securities from sec
# ftp://ftp.nasdaqtrader.com/symboldirectory/nasdaqlisted.txt
# ftp://ftp.nasdaqtrader.com/symboldirectory/otherlisted.txt

from ftplib import FTP
from security_dao import SecurityDAO
from database import Database
from security_formatter import SecurityFormatter

class SecurityUpdater:
    def __init__(self):
        database = Database()
        self.securityDAO = SecurityDAO(database)
        self.securityFormatter = SecurityFormatter()

    def __download_file_content(self, url):
        ftp = FTP('ftp.nasdaqtrader.com') 
        ftp.login()
        ftp.retrlines('RETR ' + url, self.securityFormatter) #__split_row

    def execute(self):
        self.__download_file_content('/symboldirectory/nasdaqlisted.txt')
        self.__insert_securities(self.securityFormatter.rows)
        self.securityFormatter.rows.clear()

        self.__download_file_content('/symboldirectory/otherlisted.txt')
        self.__insert_securities(self.securityFormatter.rows)

    def __insert_securities(self, rows):
        # Remove first and last row since they are not symbol
        del rows[0]
        del rows[len(rows)-1]

        for row in rows:
            symbol = row[0]
            description = row[1]
            self.securityDAO.insert(symbol, description)