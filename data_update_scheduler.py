from update_security import SecurityUpdater
from datetime import datetime
import schedule
import time

def update():
    print(datetime.now() + ": Update securities data")
    SecurityUpdater().execute()

schedule.every().day.at("17:00").do(update)

# Todo: implement heart beat that send alive message to message broker

while True:
    schedule.run_pending()
    time.sleep(1)