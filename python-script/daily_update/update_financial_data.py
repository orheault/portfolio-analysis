'''
Retrieve income statements, balance sheet and cash flow.
Data is Json format 
'''
from edgar.stock import Stock

stock = Stock('AAPL')

period = 'quarterly' # or 'annual', which is the default
year = 2020 # can use default of 0 to get the latest
quarter = 1 # 1, 2, 3, 4, or default value of 0 to get the latest
# using defaults to get the latest annual, can simplify to stock.get_filing()
filing = stock.get_filing(period, year, quarter)

# financial reports (contain data for multiple years)
income_statements = filing.get_income_statements()
balance_sheets = filing.get_balance_sheets()
cash_flows = filing.get_cash_flows()
print('hello')



'''
Download form 4 xml data
'''

from sec_edgar_downloader import Downloader
dl = Downloader()
#Get one form 4 for Visa (ticker: V)
dl.get("4", "V", amount=1)
