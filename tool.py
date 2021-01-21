# -*- coding: UTF-8 -*-
"""
AUTHOR:   MIAN
DATE:     2021/1/19
DESCRIBE: 小工具
"""
import random
from typing import List, Dict
import math_tool

random.seed()


class Card:
    # 卡片（享元模式
    def __init__(self, p: float, name: str):
        self.p = p
        self.name = name


class Cards:
    # 对抽卡池的简单封装，如果做成函数式闭包就太麻烦了
    def __init__(self, cards: List):
        self.cards = []
        self.p = []  # 每张卡片的概率范围
        self.if_get = dict()
        self.cards_map = dict()  # 方便根据
        t = 0
        for card in cards:
            t += card.p
            self.cards.append(card)
            self.p.append(t)
            self.if_get[card.name] = False
            self.cards_map[card.name] = card
        self.p.append(1)
        self.if_get["剩下的卡"] = False
        c = Card(0, "剩下的卡")
        self.cards_map["剩下的卡"] = c
        self.cards.append(c)
        self.num = 0  # 已抽卡次数

    def normal_draw(self) -> Card:
        """
普通的抽一张卡, 当cards概率之和不为1
        :return: 享元的引用
        """
        self.num += 1
        t = random.random()
        """
        # 二分查找变形，找到落在那个区间内
        left = 0
        right = len(self.p) - 1
        while left <= right:
            mid = (left + right) // 2
            v = self.p[mid]
            if v > t:
                right = mid - 1
            elif v <= t:
                left = mid + 1
        """
        index = 0
        while not self.p[index] > t:
            index += 1  # todo: 改成二分版的
        self.if_get[self.cards[index].name] = True
        return self.cards[index]

    def reset(self):
        """
对卡池状态进行重置
        """
        for key in self.if_get:
            self.if_get[key] = False
        self.num = 0


class Group:
    # 卡类型 享元模式
    def __init__(self, cards: list):
        self.cards = cards


class Mode:
    # 抽卡模式 享元模式
    def __init__(self, num=10, max_n=1000000):
        """
        :param max_n:仿真多少抽
        :param num:  默认以多少连抽进行
        """
        self.num = num
        self.max = max_n


class Target:
    # 抽卡目标 享元模式
    def __init__(self, pattern: str, cards: Cards):
        self.cards = cards

        self.parts = []
        strings = pattern.split()
        self.card_names = []
        n = 0
        for s in strings:
            # 若为卡名则直接存入数组中
            if s not in [" ", "(", ")", "and", "or", "not"]:
                self.card_names.append(s)
                self.parts.append(n)
                n += 1
            else:
                self.parts.append(s)
        # 将 a and not c 处理成 {} and not {} ,之后每次校验时按顺序将真值代入

    def if_suc(self) -> bool:
        """
判断是否成功。此版本的效率非常低，下次应该构建二叉树，并用解释器模块，并使用胜者树思想，使时间效率为O(1)
        :return: 是否达成目标
        """
        p = ""
        for part in self.parts:
            if type(part) is str:
                p += part + " "
            else:
                p += str(self.cards.if_get[self.card_names[part]]) + " "  # 此时存的是标号

        return eval(p)


class Limit:
    # 保底
    pass  # TODO


class Drawer:
    def __init__(self, m: Mode, c: Cards, g: List[Group], l: Limit, t: Target):
        self._m = m
        self._c = c
        self._g = g
        self._l = l
        self._t = t
        self.used = False

    def draw_with_no_limit(self) -> int:
        self.used = True

        while not self._t.if_suc():
            for i in range(self._m.num):
                self._c.normal_draw()

        return self._c.num

    def reset(self):
        self.used = False
        self._c.reset()


if __name__ == '__main__':
    c = []
    c.append(Card(0.02, "可畏"))
    c.append(Card(0.02, "扎拉"))
    c.append(Card(0.02, "波拉"))
    c.append(Card(0.025, "文琴佐"))
    c.append(Card(0.025, "朱利奥"))
    c.append(Card(0.005, "利托里奥"))
    cards = Cards(c)
    t = Target("可畏 and 扎拉 and 波拉 and 文琴佐 and 朱利奥 and 利托里奥", cards)
    g = []
    m = Mode(1, 10000)
    d = Drawer(m, cards, [], Limit(), t)
    l = []
    for i in range(m.max):
        l.append(d.draw_with_no_limit())
        d.reset()

    m = math_tool.Math(l)
    m.output()
