# -*- coding: utf-8 -*-
from typing import Any
from vendor.quote_api.mds_spi import MdsClientSpi
from vnpy.trader.object import TickData
from vnpy.trader.constant import Exchange

class MdsSpiImpl(MdsClientSpi):
    """
    MDS SPI 实现：Level2 快照 → vn.py Gateway

    只保留股票市场常用的回调：
      - on_connect        通道连接
      - on_disconnect     通道断开
      - on_l2_market_data_snapshot  L2 快照
    """

    def __init__(self, gateway: Any):
        super().__init__()
        self.gateway = gateway

    def on_connect(self,
                   channel: Any,
                   user_info: Any) -> int:
        """行情通道连接成功"""
        # 如需日志： print("MDS connected", user_info)
        return 0

    def on_disconnect(self,
                      channel: Any,
                      user_info: Any) -> int:
        """行情通道断开"""
        # 如需重连：在这里调用 self.gateway.quote_api.connect(...) 等
        return 0

    def on_l2_market_data_snapshot(self,
                                   channel: Any,
                                   msg_head: Any,
                                   msg_body: Any,
                                   user_info: Any) -> int:
        """
        Level-2 行情快照回调

        参数 msg_body 的典型属性包括：
          securityId, mktId, updateTime,
          lastPrice,
          bidPrice (列表), bidVolume (列表),
          askPrice (列表), askVolume (列表)
        """
        tick = TickData(
            symbol=msg_body.securityId,
            exchange=Exchange.SSE if msg_body.mktId == 1 else Exchange.SZSE,
            datetime=msg_body.updateTime,
            last_price=msg_body.lastPrice,
            bid_price_1=msg_body.bidPrice[0],
            bid_volume_1=msg_body.bidVolume[0],
            ask_price_1=msg_body.askPrice[0],
            ask_volume_1=msg_body.askVolume[0],
        )
        # 派发到 Gateway，再由 EventEngine 分发给策略
        self.gateway.on_tick(tick)
        return 0
