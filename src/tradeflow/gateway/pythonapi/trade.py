# -*- coding: utf-8 -*-
from vnpy.trader.object import OrderRequest, CancelRequest

class PythonApiTrade:
    """交易通道占位"""

    def __init__(self, gateway):
        self.gateway = gateway

    def connect(self, setting: dict):
        """初始化并连接交易 API"""
        pass

    def send_order(self, req: OrderRequest):
        """发单"""
        pass

    def cancel_order(self, req: CancelRequest):
        """撤单"""
        pass

    def close(self):
        """关闭交易连接"""
        pass
