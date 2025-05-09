# -*- coding: utf-8 -*-
from vnpy.event import EventEngine
from vnpy.trader.gateway import BaseGateway
from .trade import PythonApiTrade
from .quote import PythonApiQuote

class PythonApiGateway(BaseGateway):
    """TradeFlow 基于服务商 API 的统一 Gateway 层"""

    default_name = "PYTHONAPI"

    def __init__(self, event_engine: EventEngine, gateway_name: str = None):
        super().__init__(event_engine, gateway_name or self.default_name)
        # 行情与交易通道
        self.quote_api = PythonApiQuote(self)
        self.trade_api = PythonApiTrade(self)

    def connect(self, setting: dict):
        """
        连接行情与交易通道
        setting: {
          "oes_conf_file": "<path/to>/oes_client_stk.conf",
          "mds_conf_file": "<path/to>/mds_client_sample.conf"
        }
        """
        self.quote_api.connect(setting)
        self.trade_api.connect(setting)

    def subscribe(self, req):
        """行情订阅"""
        self.quote_api.subscribe(req)

    def send_order(self, req):
        """发单（返回 clSeqNo）"""
        return self.trade_api.send_order(req)

    def cancel_order(self, req):
        """撤单"""
        self.trade_api.cancel_order(req)

    def query_account(self):
        """查询资金账户"""
        self.trade_api.query_account()

    def query_position(self):
        """查询持仓"""
        self.trade_api.query_position()

    def close(self):
        """关闭所有通道"""
        self
