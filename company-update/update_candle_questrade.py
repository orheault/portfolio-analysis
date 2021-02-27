from model.security import Security
from model.security_type import SecurityType
from model.base import Session
from model.exchange import Exchange
from model.period import Period
from model.candle import Candle
from qtrade import Questrade
from tqdm import tqdm

import datetime
import time

class QuestradeCandleUpdater:

    def __init__(self):
        self.session = Session()
        self.qtrade = Questrade(token_yaml='access_token.yml')
        self.qtrade.refresh_access_token(from_yaml=True)

    def _get_latest_candle(self, security):
        return self.session.query(Candle).filter(Candle.security_id==security.id).order_by(Candle.date_.desc()).first()        

    def _get_extension(self, exchange_id):
        extension = ''
        if exchange_id == Exchange.EXCHANGE_TSX_ID:
            extension = ".TO"

        return extension

    def _download_candle(self, security, from_, to):
        candles = []
        symbol = security.symbol + self._get_extension(security.exchange_id)

        try:
            candles = self.qtrade.get_historical_data(symbol, from_, to, 'OneDay')
        except:
            pass

        return candles

    def _insert_candles(self, qt_candles, security_id, period_id):
        for questrade_candle in qt_candles:
            high = questrade_candle['high']
            low = questrade_candle['low']
            open = questrade_candle['open']
            close = questrade_candle['close']
            date_ = questrade_candle['start']
            volume = questrade_candle['volume']

            candle = Candle(high, low, open, close, volume, date_, period_id, security_id)
            self.session.add(candle)
            self.session.commit()            


    def execute(self):        
        
        securities = self.session.query(Security).filter(Security.company_id is not None).filter(Security.security_type_id==SecurityType.SECURITY_TYPE_COMMON_STOCK).filter(Security.is_active==True).all()
        for security in tqdm(securities):
            print("Download candle for " + security.symbol)

            lastest_candle = self._get_latest_candle(security)

            if lastest_candle is None:
                from_ = '1990-01-01'
            else:
                from_ = lastest_candle.date_ + datetime.timedelta(days=1)
                from_ = from_.strftime('%Y-%m-%d')

            to = datetime.datetime.now().strftime('%Y-%m-%d')

            candles = self._download_candle(security, from_, to)
            
            self._insert_candles(candles, security.id, Period.DAILY)

            time.sleep(4)


            

    
def init_questrade_token():
    Questrade(access_code='dR_ldO6YwZT_mQdlR9wBuUYdobumF33O0')

#QuestradeCandleUpdater().execute()
