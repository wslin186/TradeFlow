# -*- coding: utf-8 -*-
from vnpy.gateway import BaseGateway
from .trade import PythonApiTrade
from .quote import PythonApiQuote

class PythonApiGateway(BaseGateway):
    """TradeFlow 基于服务商 python_api 的 Gateway"""

    default_name = "PYTHONAPI"

    def __init__(self, event_engine, gateway_name: str = None):
        super().__init__(event_engine, gateway_name or self.default_name)
        self.trade_api = PythonApiTrade(self)
        self.quote_api = PythonApiQuote(self)

    def connect(self, setting: dict):
        """连接行情与交易"""
        self.quote_api.connect(setting)
        self.trade_api.connect(setting)

    def subscribe(self, req):
        """行情订阅"""
        self.quote_api.subscribe(req)

    def send_order(self, req):
        """发单"""
        return self.trade_api.send_order(req)

    def cancel_order(self, req):
        """撤单"""
        return self.trade_api.cancel_order(req)

    def close(self):
        """断开所有连接"""
        self.quote_api.close()
        self.trade_api.close()
