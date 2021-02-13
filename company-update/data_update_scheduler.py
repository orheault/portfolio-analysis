from update_security import SecurityUpdater
from update_inside_trader import InsideTraderUpdater
from datetime import datetime

import schedule
import time

def daily_update():
    print(datetime.now() + ": Update securities data")
    SecurityUpdater().execute()
    print(datetime.now() + ": Update insider trade data")
    InsideTraderUpdater().execute()


def start():                                                                                                                                                                      
    schedule.every().day.at("16:30").do(daily_update)

    # Todo: implement heart beat that send alive message to message broker

    while True:
        schedule.run_pending()
        time.sleep(1)