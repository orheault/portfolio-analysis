
def get_company_description_invest():
    ### COMPANY DESCRIPTION ###
    import investpy
    #profile = investpy.get_stock_company_profile(stock='AACQ', country='United States', language='english')
    #print(profile)
    #ret = investpy.search_stocks('isin', 'KY04316G1057')
    ret = investpy.search_quotes(text='aacq', products=['stocks'], countries=['United States'], n_results=1)
    print (ret)


def get_questrade_history():
    from qtrade import Questrade
    #qtrade = Questrade(access_code='JYO2nVzvnCSYAZNz7F39ER8GwaDFv4EF0')
    qtrade = Questrade(token_yaml='access_token.yml')
    qtrade.refresh_access_token(from_yaml=True)
    aapl_history = qtrade.get_historical_data('ATD.B.TO', '2021-02-18', '2021-02-19','OneDay')
    print(aapl_history)

def get_tsx_symbol():
    # https://www.tsx.com/json/company-directory/search/tsx/^*
    import urllib.request, json 
    with urllib.request.urlopen("https://www.tsx.com/json/company-directory/search/tsx/^*") as url:
        data = json.loads(url.read().decode())
        print(data)

def get_company_description_yahoo():
    import yfinance as yf
    msft = yf.Ticker("SU")

    # get stock info
    msft.info
    print( msft.info)

get_company_description_invest()
#get_company_description_yahoo()
#get_questrade_history()
#get_tsx_symbol()