from update_us_security import UsSecurityUpdater
from update_cad_security import CadSecurityUpdater
from create_company_investing import InvestingCompanyCreater
from datetime import datetime

import schedule
import time


def daily_update():
    _print(": Update us securities")
    UsSecurityUpdater().execute()

    _print(": Update canadian securities")
    CadSecurityUpdater().execute()

    _print(": Create new companies based on securities")
    InvestingCompanyCreater().execute()

    # TODO: print(datetime.now() + ": Create new companies based on securities")
    # TODO: SecSikCreator().execute()

    # TODO: implement secsiccreator before updating the insider trade
    # print(datetime.now() + ": Update insider trade data")
    # InsideTraderUpdater().execute()

    _print(": Update candles stock's security with investpy")


def _print(self, text):
    print(str(datetime.now()) + text)


def start():
    schedule.every().day.at("16:30").do(daily_update)

    while True:
        schedule.run_pending()
        time.sleep(1)


daily_update()
