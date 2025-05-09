# -*- coding: utf-8 -*-
from typing import Any, Dict, cast
from vnpy.trader.constant import Direction
from vnpy.trader.object import OrderRequest, CancelRequest
from vendor.trade_api.oes_api import (
    OesClientApi,
    OesOrdReqT,
    OesOrdCancelReqT
)
from tradeflow.spi.oes_spi import OesSpiImpl

class PythonApiTrade:
    """交易通道：封装 OES 下单、撤单与账户/持仓查询"""

    api: OesClientApi
    spi: OesSpiImpl
    order_map: Dict[int, str]

    def __init__(self, gateway: Any):
        self.gateway = gateway
        # 下面两个属性在 connect() 时初始化
        self.api = cast(OesClientApi, None)
        self.spi = cast(OesSpiImpl, None)
        self.order_map = {}

    def connect(self, setting: Dict[str, Any]):
        cfg = setting["oes_conf_file"]
        # 初始化并连接 API
        self.api = OesClientApi(cfg)
        self.spi = OesSpiImpl(self.gateway)
        self.api.register_spi(self.spi)
        self.api.connect()
        # 初次查询资金与持仓
        self.query_account()
        self.query_position()

    def send_order(self, req: OrderRequest) -> int:
        """发限价单，返回 clSeqNo"""
        assert self.api, "API 未初始化"
        ori = OesOrdReqT()
        ori.clSeqNo    = self.api.get_next_cl_seq_no()
        ori.securityId = req.symbol
        ori.quantity   = req.volume
        ori.price      = req.price
        ori.bsType     = 0 if req.direction == Direction.LONG else 1
        ori.marketId   = 1
        ori.orderType  = 2
        self.api.send_order(ori)
        # 记录以便撤单
        self.order_map[ori.clSeqNo] = getattr(ori, "orderId", "")
        return ori.clSeqNo

    def cancel_order(self, req: CancelRequest):
        """撤单"""
        assert self.api, "API 未初始化"
        ori = OesOrdCancelReqT()
        ori.clSeqNo  = req.orderid
        ori.orderId  = self.order_map.get(req.orderid, "")
        ori.marketId = 1
        self.api.cancel_order(ori)

    def query_account(self):
        """请求资金账户"""
        assert self.api, "API 未初始化"
        self.api.req_query_cash_asset()

    def query_position(self):
        """请求持仓"""
        assert self.api, "API 未初始化"
        self.api.req_query_stk_holding()

    def close(self):
        """关闭交易通道"""
        if self.api:
            self.api.close()
