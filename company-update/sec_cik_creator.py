from sec_edgar_downloader import Downloader
from model.company_security import CompanySecurity
from model.company import Company
from model.base import Session
from pathlib import Path
from sec_edgar_downloader import Downloader
from xml.dom import minidom
from requests import get
from tqdm import tqdm

import shutil
import os
import time
import re


class SecCikCreator:
    def __init__(self):
        self.session = Session()
        self.dl = Downloader()
    
    def retrieve_cik_with_http(self, symbol):
        URL = 'http://www.sec.gov/cgi-bin/browse-edgar?CIK={}&Find=Search&owner=exclude&action=getcompany'
        CIK_RE = re.compile(r'.*CIK=(\d{10}).*')    
        cik = 0

        f = get(URL.format(symbol), stream = True)
        results = CIK_RE.findall(f.text)
        if len(results):
            results[0] = int(re.sub('\.[0]*', '.', results[0]))
            cik = results[0]
        time.sleep(1)
        
        return cik

    def retrieve_cik_with_effect_filing(self, symbol):  
        cik = 0
        # Remove sec-edgar-filings directory
        edgar_path = os.path.abspath('sec-edgar-filings')
        shutil.rmtree(edgar_path, ignore_errors=True)

        # Retreive CIK number for that symbol from EDGAR
        self.dl.get("EFFECT", symbol, amount=1)

        base_path = os.path.abspath('sec-edgar-filings/'+symbol+'/EFFECT/')
        path = Path(base_path)
        for filepath in path.rglob("*.xml"):

            form = minidom.parse(str(filepath))
            node_effectiveData = form.getElementsByTagName("effectiveData")[0]
            node_filters = node_effectiveData.getElementsByTagName("filer")[0]
            node_cik = node_filters.getElementsByTagName("cik")
            cik = node_cik[0].firstChild.data

        shutil.rmtree(edgar_path, ignore_errors=True)
        time.sleep(1)

    ''' 
       Downlaod cik from edgar database using EFFECT filing. 
    '''
    def __download_cik(self, symbol):
        cik = self.retrieve_cik_with_effect_filing(symbol)

        if cik == None or cik == 0:
            cik = self.retrieve_cik_with_http(symbol)

        return cik

    def __cik_is_register(self, cik):
        company = self.session.query(Company).filter(Company.cik == cik).first()
        if company is not None and company.cik is not None:
            return True
        else:
            return False

    def __deactivate_company(self, symbol):
        result = self.session.query(Company).filter(Company.company_securities.any(CompanySecurity.symbol==symbol)).first()
    
        # Company does not exist, only the security exist in the database without any association with a compnay
        if result is None:
            print("SEC does not have any cik for " + symbol + ", deactivate the security.") # Symbol could be an ETF, blank check company
            self.session.query(CompanySecurity).filter(CompanySecurity.symbol == symbol).update({CompanySecurity.is_active:False})
            self.session.commit()
        else:
            # TODO: implement ...
            print(result)
            

        
    def __create_company(self, cik):
        print("Create company for: " + str(cik))
        company = Company(cik)

        # TODO: 
        import yfinance as yf
        msft = yf.Ticker("SU")

        # get stock info
        msft.info
        print( msft.info)
        
        self.session.add(company)
        self.session.commit()

    def __associate_symbol(self, cik, symbol):
        company = self.session.query(Company).filter(Company.cik==cik).first()
        self.session.query(CompanySecurity).filter(CompanySecurity.symbol==symbol).update({CompanySecurity.company_id:company.id})
        self.session.commit()

    ''' 
        
    '''
    def execute(self):
        securities = self.session.query(CompanySecurity).filter(CompanySecurity.company_id==None).filter(CompanySecurity.is_active==None).all()
        for security in tqdm(securities):
            symbol = ''
            if "$" in security.symbol:
                symbol = security.symbol.split("$",1)[0]
            else:
                symbol = security.symbol

            cik = self.__download_cik(symbol)

            # TODO: MAJOR REFACTOR. INCLUDE CANADIAN COMPANY/ETF/
            if cik == 0:
                # TODO: check if it is an ETF, if so create etf row
                # TODO: check if it is a FUND, if so create fund row
                # TODO: else deactivate company
                self.__deactivate_company(symbol)
            else:
                company = None
                if self.__cik_is_register(cik) is False:
                    self.__create_company(cik)

                self.__associate_symbol(cik, security.symbol)
            
        self.session.close()



#CompanyCreater().execute()

# session = Session()
# for security in session.query(Security).all():
#     if security.company_cik is not None:
#         session.query(Security).filter(Security.symbol == security.symbol).update({Security.is_active:True})
#         session.commit()
    
