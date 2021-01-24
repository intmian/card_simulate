# -*- coding: UTF-8 -*-
"""
AUTHOR:   MIAN
DATE:     2021/1/19
DESCRIBE: 驱动
"""
import datetime
import sys
import time

from file import File
from tool import Drawer
import math_tool

if __name__ == '__main__':
    f = File(sys.argv[1])
    # f = File("例子.json")
    d = Drawer(f.mode, f.cards, f.groups, f.limits, f.target)
    re = []

    time_start = datetime.datetime.now()
    # 输出预期时间
    for i in range(1000):
        re.append(d.draw())
        d.reset()
    time_end = datetime.datetime.now()
    micro = (time_end - time_start) * (f.mode.max - 1000) / 1000
    print("预期完成消耗时间：", str(micro))

    print("正在处理数据，请稍后")
    print("进度：   10   20   30   40   50   60   70   80   90  100")
    print("完成：", end="")
    sys.stdout.flush()  # 不然会不输出

    for i in range(f.mode.max - 1000):
        # todo：当小于1000次时会出问题的,回头修成百分比好了
        re.append(d.draw())
        d.reset()
        if i != 0 and (i + 1) % ((f.mode.max - 1000) // 50) == 0:
            print("▢", end="")
            sys.stdout.flush()
    print("")
    m = math_tool.Math(re)
    m.output()
