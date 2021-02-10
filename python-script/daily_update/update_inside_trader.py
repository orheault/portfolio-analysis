from sec_edgar_downloader import Downloader
from datetime import datetime
from xml.dom import minidom
from pojo.inside_trader import InsideTrader
from pojo.non_derivative_transaction import NonDerivativeTransaction
from datetime import date
from dao.base import Session, engine, Base
from database import Database
from security_dao import SecurityDAO

import shutil
import os

class InsideTraderUpdater:
    def __init__(self, security_dao):
        self.security_dao = security_dao

    def execute(self):

        # Remove sec-edgar-filings directory
        edgar_path = os.path.abspath('sec-edgar-filings')
        shutil.rmtree(edgar_path, ignore_errors=True)

        session = Session()
        # Retrieve inside trader form.
        for security in self.security_dao.get_all():
            # Download form 4 in sec-edgar-filings folder
            dl = Downloader()
            dl.get("4", security.symbol, after=str(datetime.now().date()))

            path = os.path.abspath('sec-edgar-filings/'+security.symbol+'/4/')

            for directory_name in os.listdir(path):
                file_name = path + '/' + directory_name + '/' + 'filing-details.xml'
                form = minidom.parse(file_name)

                inside_trader = convert_inside_trader_xml(form)
                non_derivative_transactions = convert_non_derivative_xml(form)

                session.add(inside_trader)
                for non_derivative_transaction in non_derivative_transactions:
                    non_derivative_transaction.add_inside_trader(inside_trader)
                    session.add(non_derivative_transaction)

                session.commit()

            shutil.rmtree(edgar_path, ignore_errors=True)
                    
        session.close()



def convert_non_derivative_xml(form):
    non_derivative_transactions = []

    non_derivative_transactions_node = form.getElementsByTagName('nonDerivativeTable')[0].getElementsByTagName('nonDerivativeTransaction')
    for non_derivative_transaction in non_derivative_transactions_node:
        transaction_code = non_derivative_transaction.getElementsByTagName('transactionCoding')[0].getElementsByTagName('transactionCode')[0].firstChild.data

        amount_share = non_derivative_transaction.getElementsByTagName('transactionAmounts')[0].getElementsByTagName('transactionShares')[0].getElementsByTagName('value')[0].firstChild.data
        
        price_per_share = 0
        if transaction_code != 'M':
            price_per_share = non_derivative_transaction.getElementsByTagName('transactionAmounts')[0].getElementsByTagName('transactionPricePerShare')[0].getElementsByTagName('value')[0].firstChild.data

        security_type_id = 1
        non_derivative_transactions.append(NonDerivativeTransaction(amount_share,price_per_share,transaction_code,security_type_id))

    return non_derivative_transactions

def convert_inside_trader_xml(form):
    node_reporting_owner = form.getElementsByTagName("reportingOwner")[0]
    reporting_owner_name = node_reporting_owner.getElementsByTagName('reportingOwnerId')[0].getElementsByTagName('rptOwnerName')[0].firstChild.data
    
    reporting_owner_relationship = node_reporting_owner.getElementsByTagName('reportingOwnerRelationship')[0]
    reporting_owner_relationship_is_director = convert_bool(reporting_owner_relationship.getElementsByTagName('isDirector')[0].firstChild.data)
    reporting_owner_relationship_is_officer = convert_bool(reporting_owner_relationship.getElementsByTagName('isOfficer')[0].firstChild.data)
    reporting_owner_relationship_is_other = convert_bool(reporting_owner_relationship.getElementsByTagName('isOther')[0].firstChild.data)
    reporting_owner_relationship_is_ten_percent = convert_bool(reporting_owner_relationship.getElementsByTagName('isTenPercentOwner')[0].firstChild.data)

    reporting_owner_relationship_officer_title = reporting_owner_relationship.getElementsByTagName('officerTitle')[0].firstChild
    reporting_owner_relationship_description = ''
    if reporting_owner_relationship_officer_title is not None:
        reporting_owner_relationship_description = reporting_owner_relationship_officer_title.data

    reporting_owner_relationship_other = reporting_owner_relationship.getElementsByTagName('otherText')[0].firstChild
    if reporting_owner_relationship_other is not None:
        reporting_owner_relationship_description += '    ' + reporting_owner_relationship_other.data 
    
    transaction_date = form.getElementsByTagName('periodOfReport')[0].firstChild.data

    

    return InsideTrader(security_name, reporting_owner_name, transaction_date, reporting_owner_relationship_is_director,
    reporting_owner_relationship_is_officer, reporting_owner_relationship_is_ten_percent, reporting_owner_relationship_is_other, reporting_owner_relationship_description)

def convert_bool(data):
    if data == '0':
        return False
    else:
        return True



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


database = Database()
security_dao = SecurityDAO(database)
InsideTraderUpdater(security_dao).execute()