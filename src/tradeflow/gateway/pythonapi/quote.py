# -*- coding: utf-8 -*-
from vnpy.trader.object import SubscribeRequest, TickData

class PythonApiQuote:
    """行情通道占位"""

    def __init__(self, gateway):
        self.gateway = gateway

    def connect(self, setting: dict):
        """初始化并连接行情 API"""
        pass

    def subscribe(self, req: SubscribeRequest):
        """行情订阅"""
        pass

    def close(self):
        """关闭行情连接"""
        pass
