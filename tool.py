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
        self.last_c_status = None  # 当保底模式为替换时，需要将最后一次的抽卡现场还原

    def normal_draw(self) -> Card:
        """
普通的抽一张卡, 当cards概率之和不为1,会抽出一张被成为剩余卡的卡
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
        self.last_c_status = self.if_get[self.cards[index].name]
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
    def __init__(self, cards: List):
        self.cards = Cards(cards)  # 新建一个小型卡池，方便在group里面抽保底


class Mode:
    def __init__(self, num=10, max_n=1000000):
        """
抽卡模式 享元模式
        :param max_n:仿真多少抽
        :param num:  默认以多少连抽进行
        """
        self.num = num
        self.max = max_n


class Target:

    def __init__(self, pattern: str, cards: Cards):
        """
抽卡目标 享元模式
        :param pattern: 条件
        :param cards: 卡池
        """
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
    def __init__(self, g: Group, n: int, way: int, if_reset: int, how: int, c: Cards):
        """
保底
        :param g: 保底类目
        :param n: 保底抽数
        :param way: 随机还是给出尚未抽到的 1 随机 2 未抽到的
        :param if_reset: 当抽出保底卡后，是否重置保底 1 抽出后立刻重置count（幻书启示录） 2 抽出后不重置count，但不再触发（pcr 二星保底） 3 无（pcr 井）
        :param how: 如何给出保底，1代表替换 2代表附加
        :param c: 卡池
        """
        self._g = g
        self._n = n
        self._count = 0
        self._way = way
        self._if_r = if_reset
        self.how = how
        self._c = c
        self._active = True  # 是否激活, 之所以不重置是为了迎合某些游戏的十连必出xxx的机制

    def reset(self):
        self._active = True
        self._count = 0

    def will_trigger(self) -> bool:
        """
是否下一步就触发了
        :return: 是/否
        """
        return self._count == self._n - 1

    def check(self, c: Card) -> (bool,) or (bool, Card, int):
        """
校验是否触发保底
        :param c:卡
        :returns (是否触发保底, 保底结果, 给出方式)
        """
        self._count += 1
        if c in self._g.cards.cards and self._count != self._n:
            # 当恰好在保底的那一发触发重置时，重置不生效
            r = self._if_r
            if r == 1:
                self.reset()
                return False,
            elif r == 2:
                self._active = False
                return False,
            elif r == 3:
                return False,
        elif self._count == self._n:
            if not self._active:
                self.reset()
                return False,

            re = None
            if self._way == 1:
                re = self._g.cards.normal_draw()
            elif self._way == 2:
                low_c = None
                low_p = 2
                for card in self._g.cards.cards:
                    if not self._c.if_get[card.name] and card.p < low_p:
                        low_c = card
                        low_p = card.p
                if low_p == 2:
                    # 全抽满却触发保底的情况
                    re = self._g.cards.normal_draw()
                else:
                    re = low_c
            self.reset()
            return True, re, self.how
        else:
            return False,


class Drawer:
    def __init__(self, m: Mode, c: Cards, g: List[Group], l: List[Limit], t: Target):
        self._m = m
        self._c = c
        self._g = g
        self._l = l
        self._t = t
        self.used = False

    @Warning
    def draw_with_no_limit(self) -> int:
        # 此方法已被废除
        self.used = True

        while not self._t.if_suc():
            for i in range(self._m.num):
                self._c.normal_draw()

        return self._c.num

    def draw(self) -> int:
        self.used = True

        while not self._t.if_suc():
            for i in range(self._m.num):
                c = self._c.normal_draw()
                for limit in self._l:
                    # 先处理所有附加型的保底
                    if limit.how == 2:
                        re = limit.check(c)
                        if re[0]:
                            self._c.if_get[re[1].name] = True
                triggered = False  # 是否已触发保底
                for limit in self._l:
                    # 处理所有替代型的保底
                    if limit.how == 1:
                        if limit.will_trigger():
                            if not triggered:
                                re = limit.check(c)
                                if re[0]:
                                    self._c.if_get[re[1].name] = True
                                    self._c.if_get[c.name] = self._c.last_c_status  # 回复现场（因为上一次的抽卡结果被顶掉了）
                                    triggered = True
                            else:
                                pass  # 不触发处理第一个以外的附加型保底
                        else:
                            re = limit.check(c)

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
    t = Target("波拉", cards)
    g = []
    m = Mode(1, 10000)
    d = Drawer(m, cards, [], [], t)
    l = []
    for i in range(m.max):
        l.append(d.draw_with_no_limit())
        d.reset()

    m = math_tool.Math(l)
    m.output()
