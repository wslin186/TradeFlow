# src/tradeflow/spi/oes_spi.py
# -*- coding: utf-8 -*-
from typing import Any
from vendor.trade_api.oes_spi import OesClientSpi
from vnpy.trader.object import OrderData, TradeData, AccountData, PositionData

class OesSpiImpl(OesClientSpi):
    """OES SPI 实现：交易&查询回报"""

    def __init__(self, gateway):
        super().__init__()
        self.gateway = gateway

    def on_rpt_connect(self, channel: Any, user_info: Any) -> int:
        # 回报通道连上
        return 0

    def on_rpt_disconnect(self, channel: Any, user_info: Any) -> int:
        # 回报通道断开
        return 0

    def on_order_report(self,
            channel: Any,
            msg_head: Any,
            rpt_msg_head: Any,
            rpt_msg_body: Any,
            user_info: Any) -> int:
        order: OrderData = self.gateway.create_order_data_from_oes(rpt_msg_body)
        self.gateway.on_order(order)
        return 0

    def on_trade_report(self,
            channel: Any,
            msg_head: Any,
            rpt_msg_head: Any,
            rpt_msg_body: Any,
            user_info: Any) -> int:
        trade: TradeData = self.gateway.create_trade_data_from_oes(rpt_msg_body)
        self.gateway.on_trade(trade)
        return 0

    def on_query_cash_asset(self,
            channel: Any,
            msg_head: Any,
            msg_body: Any,
            cursor: Any,
            user_info: Any) -> int:
        account: AccountData = self.gateway.create_account_data_from_oes(msg_body)
        self.gateway.on_account(account)
        return 0

    def on_query_stk_holding(self,
            channel: Any,
            msg_head: Any,
            msg_body: Any,
            cursor: Any,
            user_info: Any) -> int:
        position: PositionData = self.gateway.create_position_data_from_oes(msg_body)
        self.gateway.on_position(position)
        return 0
