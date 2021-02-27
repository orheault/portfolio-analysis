from model.base import Session
from model.security import Security
from model.company import Company
from model.exchange import Exchange
from tqdm import tqdm
from sqlalchemy.dialects.postgresql import insert

import urllib.request, json 

class CadSecurityUpdater():
    def __init__(self):
        self._session = Session()

    def __download_tsx_json(self):
        data = []
        # https://www.tsx.com/json/company-directory/search/tsx/^*
        with urllib.request.urlopen("https://www.tsx.com/json/company-directory/search/tsx/^*") as url:
            data = json.loads(url.read().decode())
        
        return data

    def __get_company_name(self, symbol):
        return symbol['name']

    def __get_securities(self, symbol):
        securities = []
        for instrument in symbol['instruments']:
            symbol = instrument['symbol']
            name = instrument['name']
            securities.append(Security(symbol, description=name))
        
        return securities

    def __update_security(self, securities, exchange_id, security_type_id):

        for security in securities:
            existing_security = self._session.query(Security.symbol == security.symbol).filter(Security.exchange_id == exchange_id).first()
            if existing_security is not None and len(existing_security) > 0:
                insert_statement = insert(Security).values({Security.symbol:security.symbol, Security.description: security.description, Security.exchange_id: exchange_id, Security.security_type_id: security_type_id})
                self._session.execute(insert_statement.on_conflict_do_nothing())
        
        self._session.commit()

    def execute(self):
        symbol_array = self.__download_tsx_json()
        for symbol in tqdm(symbol_array['results']):
            company_name = self.__get_company_name(symbol)

            security_type_id = 1
            if " etf" in company_name or " ETF" in company_name:
                security_type_id = 2

            securities = self.__get_securities(symbol)

            self.__update_security(securities, Exchange.EXCHANGE_TSX_ID, security_type_id)
            
CadSecurityUpdater().execute()