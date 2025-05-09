# src/tradeflow/main.py
# -*- coding: utf-8 -*-
import os
import sys
import time

# 1. 计算项目根目录（TradeFlow）
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
# 2. 将 src 加入到 sys.path
SRC_PATH = os.path.join(BASE_DIR, "src")
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

from vnpy.event import EventEngine
from vnpy.trader.constant import Exchange, Direction, Offset
from vnpy.trader.object import SubscribeRequest, OrderRequest
from tradeflow.gateway.pythonapi.gateway import PythonApiGateway


def main():
    # 3. 实例化事件引擎和 Gateway
    ee = EventEngine()
    gw = PythonApiGateway(ee)

    # 4. 加载配置文件（位于项目根的 config 目录）
    cfg_dir = os.path.join(BASE_DIR, "config")
    gw.connect({
        "oes_conf_file": os.path.join(cfg_dir, "oes_client_stk.conf"),
        "mds_conf_file": os.path.join(cfg_dir, "mds_client_sample.conf"),
    })

    # 5. 注册回调打印
    ee.register("tick", lambda event: print("[TICK]", event.data))
    ee.register("order", lambda event: print("[ORDER]", event.data))
    ee.register("trade", lambda event: print("[TRADE]", event.data))
    ee.register("account", lambda event: print("[ACCOUNT]", event.data))
    ee.register("position", lambda event: print("[POSITION]", event.data))

    # 6. 订阅行情
    print("▶️ 订阅行情 600000.SSE")
    gw.subscribe(SubscribeRequest(symbol="600000", exchange=Exchange.SSE))

    # 7. 发一笔测试限价单
    print("▶️ 发送测试委托")
    cl_seq = gw.send_order(OrderRequest(
        symbol="600000",
        exchange=Exchange.SSE,
        direction=Direction.LONG,
        offset=Offset.OPEN,
        price=10.00,
        volume=1
    ))
    print("  → clSeqNo =", cl_seq)

    # 8. 启动事件引擎循环（或等待回调）
    print("▶️ 启动事件引擎循环，按 Ctrl+C 停止")
    try:
        ee.start()
    except AttributeError:
        # 如果没有 start() 方法，则用 sleep 循环
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass

    # 9. 关闭
    print("▶️ 关闭 Gateway")
    gw.close()


if __name__ == "__main__":
    main()