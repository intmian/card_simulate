# -*- coding: UTF-8 -*-
"""
AUTHOR:   MIAN
DATE:     2021/1/19
DESCRIBE: 驱动
"""

import sys

from file import File
from tool import Drawer
import math_tool

if __name__ == '__main__':
    f = File(sys.argv[1])
    #f = File("例子.json")
    d = Drawer(f.mode, f.cards, f.groups, f.limits, f.target)
    re = []
    for i in range(f.mode.max):
        re.append(d.draw())
        d.reset()
    m = math_tool.Math(re)
    m.output()
