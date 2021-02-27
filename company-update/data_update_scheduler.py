from update_us_security import UsSecurityUpdater
from update_cad_security import CadSecurityUpdater
from create_company_investing import InvestingCompanyCreater
from datetime import datetime

import schedule
import time

def daily_update():
    print(str(datetime.now()) + ": Update us securities")
    UsSecurityUpdater().execute()

    print(str(datetime.now()) + ": Update canadian securities")
    CadSecurityUpdater().execute()

    print(str(datetime.now()) + ": Create new companies based on securities")
    InvestingCompanyCreater().execute()

    # TODO: print(datetime.now() + ": Create new companies based on securities")
    # TODO: SecSikCreator().execute()

    # TODO: implement secsiccreator before updating the insider trade
    # print(datetime.now() + ": Update insider trade data")
    # InsideTraderUpdater().execute()

def start():                                                                                                                                                                      
    schedule.every().day.at("16:30").do(daily_update)

    while True:
        schedule.run_pending()
        time.sleep(1)


daily_update()