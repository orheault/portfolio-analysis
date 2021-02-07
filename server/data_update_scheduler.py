from update_security import SecurityUpdater
from security_dao import SecurityDAO
from update_inside_trader import InsideTraderUpdater
from datetime import datetime
from database import Database

import schedule
import time

def update():
    print(datetime.now() + ": Update securities data")
    SecurityUpdater(security_dao).execute()
    InsideTraderUpdater(security_dao).execute()


database = Database()
security_dao = SecurityDAO(database)

schedule.every().day.at("17:00").do(update)

# Todo: implement heart beat that send alive message to message broker

while True:
    schedule.run_pending()
    time.sleep(1)