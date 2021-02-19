from update_security import SecurityUpdater
from update_inside_trader import InsideTraderUpdater
from create_company import CompanyCreater
from datetime import datetime

import schedule
import time

def daily_update():
    print(datetime.now() + ": Update securities data")
    SecurityUpdater().execute()
    print(datetime.now() + ": Create new companies based on securities")
    CompanyCreater().execute()
    print(datetime.now() + ": Update insider trade data")
    InsideTraderUpdater().execute()

    # TODO:
    # Retrieve securities without association with a company. Those securities can be IPO. They don't have any general filings ( 10k-8k, etc) but they can have insider trade filings
    # Download missing filings for those securities


def start():                                                                                                                                                                      
    schedule.every().day.at("16:30").do(daily_update)

    while True:
        schedule.run_pending()
        time.sleep(1)