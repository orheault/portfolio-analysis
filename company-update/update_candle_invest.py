from model.security import Security
from model.security_type import SecurityType
from model.base import Session
from model.exchange import Exchange
from model.period import Period
from model.candle import Candle
import investpy
from tqdm import tqdm

import datetime
import time


#
# Download latest candles for all stock
#
class InvestCandleUpdater:

    def __init__(self):
        self.session = Session()

    def _get_latest_candle(self, security):
        return self.session.query(Candle).filter(Candle.security_id == security.id).order_by(
            Candle.date_.desc()).first()

    def _download_candle(self, security, from_, to):
        candles = []

        if security.exchange_id == Exchange.EXCHANGE_TSX_ID:
            country = ['Canada']
        elif security.exchange_id == Exchange.EXCHANGE_NASDAQ_ID:
            country = ['United States']

        try:
            search_result = investpy.search_quotes(text=security.symbol, products=['stocks'], countries=country,
                                                   n_results=1)
            candles = search_result.retrieve_historical_data(from_date=from_, to_date=to)
            print(" " + len(candles) + " candles from " + from_ + " to " + to)
        except:
            pass

        return candles

    def _insert_candles(self, invest_candles, security_id, period_id):
        if len(invest_candles) > 0:
            for index, invest_candle in invest_candles.iterrows():
                high = invest_candle['High']
                low = invest_candle['Low']
                open = invest_candle['Open']
                close = invest_candle['Close']
                date_ = index
                volume = invest_candle['Volume']

                candle = Candle(high, low, open, close, volume, date_, period_id, security_id)
                self.session.add(candle)
                self.session.commit()

    def execute(self):

        securities = self.session.query(Security).filter(Security.company_id is not None).filter(
            Security.security_type_id == SecurityType.SECURITY_TYPE_COMMON_STOCK).filter(
            Security.is_active == True).all()
        for security in tqdm(securities):
            print("Download candle for " + security.symbol)

            lastest_candle = self._get_latest_candle(security)

            if lastest_candle is None:
                from_ = '1990-01-01'
            else:
                from_ = lastest_candle.date_ + datetime.timedelta(days=1)
                from_ = from_.strftime('%d/%m/%Y')

            to = datetime.datetime.now().strftime('%d/%m/%Y')

            candles = self._download_candle(security, from_, to)

            self._insert_candles(candles, security.id, Period.DAILY)

            time.sleep(4)


InvestCandleUpdater().execute()
