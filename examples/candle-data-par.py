# -*- coding: utf-8 -*-
"""Retrieve candle data.

For complete specs of the endpoint, please check:

    http://developer.oanda.com/rest-live-v20/instrument-ep/

Specs of InstrumentsCandles()

    http://oanda-api-v20.readthedocs.io/en/latest/oandapyV20.endpoints.html

"""
import argparse
import json
from oandapyV20 import API
from concurrent.futures import ThreadPoolExecutor  # optional to ctrl #workers
from requests_futures.sessions import FuturesSession   # by default 2 workers

from oandapyV20.exceptions import V20Error
import oandapyV20.endpoints.instruments as instruments
from oandapyV20.definitions.instruments import CandlestickGranularity
from exampleauth import exampleAuth

price = ['M', 'B', 'A', 'BA', 'MBA']
granularities = CandlestickGranularity().definitions.keys()
# create the top-level parser
parser = argparse.ArgumentParser(prog='candle-data')
parser.add_argument('--nice', action='store_true', help='json indented')
parser.add_argument('--count', default=0, type=int,
                    help='num recs, if not specified 500')
parser.add_argument('--granularity', choices=granularities, required=True)
parser.add_argument('--price', choices=price, default='M', help='Mid/Bid/Ask')
parser.add_argument('--start', type=str, help="date-time YYYY-MM-DDTHH:MM:SS")
parser.add_argument('--end', type=str, help="date-time YYYY-MM-DDTHH:MM:SS")
parser.add_argument('--instruments', type=str, nargs='?',
                    action='append', help='instruments')


class Main(object):
    def __init__(self, api, accountID, clargs):
        self._accountID = accountID
        self.clargs = clargs
        self.api = api

    def main(self):

        if self.clargs.instruments:
            params = {}
            if self.clargs.granularity:
                params.update({"granularity": self.clargs.granularity})
            if self.clargs.count:
                params.update({"count": self.clargs.count})
            if self.clargs.start:
                params.update({"from": self.clargs.start})
            if self.clargs.end:
                params.update({"to": self.clargs.end})
            if self.clargs.price:
                params.update({"price": self.clargs.price})

            fut = []   # list for futures
            for i in self.clargs.instruments:
                r = instruments.InstrumentsCandles(instrument=i, params=params)
                fut.append(self.api.request(r))

            kw = {}
            if self.clargs.nice:
                kw = {"indent": self.clargs.nice}

            for F in fut:
                resp = F.result()
                print("{} {}".format(resp.status_code,
                                     json.dumps(json.loads(resp.content), **kw)))


if __name__ == "__main__":
    clargs = parser.parse_args()

    accountID, token = exampleAuth()
    # session = FuturesSession(executor=ThreadPoolExecutor(max_workers=5))
    session = FuturesSession()
    api = API(access_token=token, session=session)
    try:
        m = Main(api=api, accountID=accountID, clargs=clargs)
        m.main()
    except V20Error as v20e:
        print("ERROR {} {}".format(v20e.code, v20e.msg))
    except Exception as e:
        print("Unkown error: {}".format(e))
