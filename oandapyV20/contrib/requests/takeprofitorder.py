# -*- encoding: utf-8 -*-

from .baserequest import BaseRequest
from oandapyV20.types import TradeID, PriceValue
import oandapyV20.definitions.orders as OD


class TakeProfitOrderRequest(BaseRequest):
    """create a TakeProfit OrderRequest.

    TakeProfitOrderRequest is used to build the body for a TakeProfitOrder.
    The body can be used to pass to the OrderCreate endpoint.
    """

    def __init__(self,
                 tradeID,
                 price,
                 clientTradeID=None,
                 timeInForce=OD.TimeInForce.GTC,
                 gtdTime=None,
                 clientExtensions=None):
        """
        Instantiate a TakeProfitOrderRequest.

        Parameters
        ----------

        tradeID : string (required)
            the tradeID of an existing trade

        price: float (required)
            the price indicating the target price to close the order.

        Example
        -------

            >>> import json
            >>> from oandapyV20 import API
            >>> import oandapyV20.endpoints.orders as orders
            >>> from oandapyV20.contrib.requests import TakeProfitOrderRequest
            >>>
            >>> accountID = "..."
            >>> client = API(access_token=...)
            >>> ordr = TakeProfitOrderRequest(tradeID="1234",
            >>>                               price=1.22)
            >>> print(json.dumps(ordr.data, indent=4))
            >>> r = orders.OrderCreate(accountID, data=ordr.data)
            >>> rv = client.request(r)
            >>> ...
        """
        super(TakeProfitOrderRequest, self).__init__()

        # by default for a TAKE_PROFIT order
        self._data.update({"type": OD.OrderType.TAKE_PROFIT})
        self._data.update({"timeInForce": timeInForce})

        # required
        self._data.update({"tradeID": TradeID(tradeID).value})
        self._data.update({"price": PriceValue(price).value})

        # optional, but required if
        self._data.update({"gtdTime": gtdTime})
        if timeInForce == OD.TimeInForce.GTD and not gtdTime:
            raise ValueError("gtdTime missing")

        # optional
        self._data.update({"clientExtensions": clientExtensions})

    @property
    def data(self):
        """data property.

        return the JSON order body
        """
        return dict({"order": super(TakeProfitOrderRequest, self).data})