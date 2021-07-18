from model.security import Security
from model.security_type import SecurityType
from model.company import Company
from model.exchange import Exchange
from model.base import Session
from tqdm import tqdm

import yfinance as yf
import investpy
import time


class InvestingCompanyCreater:
    def __init__(self):
        self.session = Session()

    def disable_security(self, security):
        security.is_active = False
        self.session.commit()

    def get_security_countries(self, exchange_id):
        countries = []
        if Exchange.EXCHANGE_TSX_ID == exchange_id:
            countries.append("Canada")
        else:
            countries.append("United States")

        return countries

    def execute(self):
        securities = self.session.query(Security).filter(Security.company_id == None).filter(
            Security.security_type_id == SecurityType.SECURITY_TYPE_COMMON_STOCK).filter(
            Security.is_active == True).all()

        for security in tqdm(securities):

            if "$" in security.symbol:
                self.disable_security(security)

            symbol = security.symbol
            # formatted symbol for invest downloader. 
            symbol = symbol.replace('.', '')

            countries = self.get_security_countries(security.exchange_id)

            invest_data = None
            try:
                time.sleep(2)
                if security.security_type.id == SecurityType.SECURITY_TYPE_COMMON_STOCK:
                    product = ['stocks']
                elif security.security_type.id == SecurityType.SECURITY_TYPE_EXCHANGE_TRADED_FUND:
                    product = ['etfs']
                else:
                    print('Security de type' + security.security_type)

                invest_data = investpy.search_quotes(text=symbol, products=product, countries=countries, n_results=1)
            except:
                pass

            if invest_data is None:
                self.disable_security(security)
                continue

            name = invest_data.name
            sanitize_name = name.replace('\xa0', ' ')

            company_name = self.session.query(Company).filter(Company.name == sanitize_name).first()
            if company_name is not None:
                security.company_id = company_name.id
                self.session.commit()
                continue

            print("Create company name: " + sanitize_name)

            company = Company(name=sanitize_name, is_active=True)
            self.session.add(company)
            self.session.commit()

            security.company_id = company.id
            self.session.commit()


InvestingCompanyCreater().execute()
