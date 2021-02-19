from sec_edgar_downloader import Downloader
from datetime import datetime
from xml.dom import minidom
from model.inside_trader import InsideTrader
from model.security import Security
from model.security_type import SecurityType
from model.non_derivative_transaction import NonDerivativeTransaction
from model.base import Session, engine, Base
from datetime import date
from pathlib import Path
from sqlalchemy.orm import Query

import shutil
import os
import time

class InsideTraderUpdater:
    def __init__(self):
        self.session = Session()


    def convert_non_derivative_xml(self,form):
        non_derivative_transactions = []

        non_derivative_table = form.getElementsByTagName('nonDerivativeTable')

        if non_derivative_table is not None and len(non_derivative_table) > 0:
            non_derivative_transactions_node = non_derivative_table[0].getElementsByTagName('nonDerivativeTransaction')

            for non_derivative_transaction in non_derivative_transactions_node:
                transaction_code = non_derivative_transaction.getElementsByTagName('transactionCoding')[0].getElementsByTagName('transactionCode')[0].firstChild.data

                if transaction_code == 'P' or transaction_code == 'S':
                    amount_share = non_derivative_transaction.getElementsByTagName('transactionAmounts')[0].getElementsByTagName('transactionShares')[0].getElementsByTagName('value')[0].firstChild.data
                    price_per_share = non_derivative_transaction.getElementsByTagName('transactionAmounts')[0].getElementsByTagName('transactionPricePerShare')[0].getElementsByTagName('value')[0].firstChild.data
                    
                    security_title = self.get_first_child_data(form, 'securityTitle')
                    query_security_type = Query(SecurityType, self.session)
                    query_security_type.filter(SecurityType.title == security_title)
                    security_type = query_security_type.first()

                    if security_type is None:
                        security_type = SecurityType(security_title)
                        self.session.add(security_type)
                        self.session.commit()

                    non_derivative_transactions.append(NonDerivativeTransaction(int(float(amount_share)),price_per_share,transaction_code,security_type))

        return non_derivative_transactions

    def convert_inside_trader_xml(self, form, symbol):
        node_reporting_owner = form.getElementsByTagName("reportingOwner")[0]
        reporting_owner_name = node_reporting_owner.getElementsByTagName('reportingOwnerId')[0].getElementsByTagName('rptOwnerName')[0].firstChild.data
        reporting_owner_relationship = node_reporting_owner.getElementsByTagName('reportingOwnerRelationship')[0]

        is_director = self.convert_bool(self.get_first_child_data(reporting_owner_relationship, 'isDirector'))
        is_officer = self.convert_bool(self.get_first_child_data(reporting_owner_relationship, 'isOfficer'))
        is_other = self.convert_bool(self.get_first_child_data(reporting_owner_relationship, 'isOther'))
        is_ten_percent = self.convert_bool(self.get_first_child_data(reporting_owner_relationship,'isTenPercentOwner'))
        title = self.get_first_child_data(reporting_owner_relationship, 'officerTitle')
        other_text = self.get_first_child_data(reporting_owner_relationship, 'otherText')
        description = title + other_text
        transaction_date = self.get_first_child_data(form, 'periodOfReport')

        return InsideTrader(symbol, reporting_owner_name, transaction_date, is_director, is_officer, is_ten_percent, is_other, description)

    def convert_bool(self, data):
        if data == '0':
            return False
        else:
            return True

    def get_first_child_data(self, data, tag_name):
        ret_value = ""
        data = data.getElementsByTagName(tag_name)
        if data is not None and len(data) > 0:
            if data[0] is not None and data[0].firstChild is not None:
                if data[0].firstChild.data is not None:
                    ret_value = data[0].firstChild.data
        return ret_value

    
    def execute(self):

        # Remove sec-edgar-filings directory
        edgar_path = os.path.abspath('sec-edgar-filings')
        shutil.rmtree(edgar_path, ignore_errors=True)

        # Retrieve inside trader form.
        securities = self.session.query(Security).all()
        for security in securities:
            # Download form 4 in sec-edgar-filings folder
            dl = Downloader()
            # todo: Get latest downloaded form 4 date from the database and pass the date as paramenter to the dl.get function ...
            ret = dl.get("4", security.symbol, after=str(datetime.now().date())

            base_path = os.path.abspath('sec-edgar-filings/'+security.symbol+'/4/')
            path = Path(base_path)
            for filepath in path.rglob("*.xml"):

                #file_name = base_path + '/' + directory_name + '/' + 'filing-details.xml'
                form = minidom.parse(str(filepath))

                inside_trader = self.convert_inside_trader_xml(form, security.symbol)
                non_derivative_transactions = self.convert_non_derivative_xml(form)

                self.session.add(inside_trader)
                for non_derivative_transaction in non_derivative_transactions:
                    non_derivative_transaction.add_inside_trader(inside_trader)
                    self.session.add(non_derivative_transaction)
                self.session.commit()

            shutil.rmtree(edgar_path, ignore_errors=True)
            time.sleep(1)
                    
        self.session.close()


# stock = Stock('AAPL')

# period = 'quarterly' # or 'annual', which is the default
# year = 2021 # can use default of 0 to get the latest
# quarter = 1 # 1, 2, 3, 4, or default value of 0 to get the latest
# # using defaults to get the latest annual, can simplify to stock.get_filing()
# filing = stock.get_filing(period, year, quarter)

# # financial reports (contain data for multiple years)
# income_statements = filing.get_income_statements()
# balance_sheets = filing.get_balance_sheets()
# cash_flows = filing.get_cash_flows()
# print('hello')

InsideTraderUpdater().execute()