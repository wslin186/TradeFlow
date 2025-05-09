# src/tradeflow/strategy/ma_cross.py
from collections import deque

from vnpy.trader.constant import Interval, Direction, Offset
from vnpy.trader.object import OrderRequest
from tradeflow.gateway.pythonapi.gateway import PythonApiGateway

class MaCrossStrategy:
    """
    简单均线交叉示例策略：
    - 短期均线上穿长期均线时买入
    - 短期均线下穿长期均线时平仓
    """

    def __init__(self, gateway: PythonApiGateway, short_window=5, long_window=20):
        self.gateway = gateway
        self.short_w = short_window
        self.long_w  = long_window
        self.prices = deque(maxlen=long_window)
        self.in_pos = False
        self.last_cross = None  # "golden" or "dead"

    def on_tick(self, tick):
        # 1. 收集价格
        self.prices.append(tick.last_price)
        if len(self.prices) < self.long_w:
            return

        # 2. 计算均线
        short_ma = sum(list(self.prices)[-self.short_w:]) / self.short_w
        long_ma  = sum(self.prices) / self.long_w

        # 3. 判断交叉
        if short_ma > long_ma and self.last_cross != "golden":
            self.last_cross = "golden"
            if not self.in_pos:
                # 下多单
                req = OrderRequest(
                    symbol=tick.symbol,
                    exchange=tick.exchange,
                    direction=Direction.LONG,
                    offset=Offset.OPEN,
                    price=tick.last_price,
                    volume=100
                )
                cl = self.gateway.send_order(req)
                print(f"[策略] 金叉买入 → clSeqNo={cl}")
                self.in_pos = True

        elif short_ma < long_ma and self.last_cross != "dead":
            self.last_cross = "dead"
            if self.in_pos:
                # 平仓
                req = OrderRequest(
                    symbol=tick.symbol,
                    exchange=tick.exchange,
                    direction=Direction.SHORT,
                    offset=Offset.CLOSE,
                    price=tick.last_price,
                    volume=100
                )
                cl = self.gateway.send_order(req)
                print(f"[策略] 死叉卖出 → clSeqNo={cl}")
                self.in_pos = False
