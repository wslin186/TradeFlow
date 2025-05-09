# -*- coding: utf-8 -*-
from typing import Any, cast
from vnpy.trader.constant import Exchange
from vnpy.trader.object import SubscribeRequest
from vendor.quote_api.mds_api import MdsClientApi
from tradeflow.spi.mds_spi import MdsSpiImpl

class PythonApiQuote:
    """行情通道：封装 MDS 行情订阅"""

    api: MdsClientApi
    spi: MdsSpiImpl

    def __init__(self, gateway: Any):
        self.gateway = gateway
        # connect() 时赋值
        self.api = cast(MdsClientApi, None)
        self.spi = cast(MdsSpiImpl, None)

    def connect(self, setting: dict):
        cfg = setting["mds_conf_file"]
        # 初始化并启动行情 API
        self.api = MdsClientApi()
        self.spi = MdsSpiImpl(self.gateway)
        self.api.register_spi(self.spi)
        self.api.create_context(cfg)
        self.api.start()

    def subscribe(self, req: SubscribeRequest):
        """订阅 Level-2 行情"""
        assert self.api, "API 未初始化"
        symbol = req.symbol
        exch   = req.exchange
        mkt_id = 1 if exch == Exchange.SSE else 2
        self.api.subscribe(symbol, mkt_id)

    def close(self):
        """关闭行情通道"""
        if self.api:
            self.api.close()
