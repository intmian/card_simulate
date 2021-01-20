# -*- coding: UTF-8 -*-
"""
AUTHOR:   MIAN
DATE:     2021/1/19
DESCRIBE: 小工具
"""
import random
from typing import List, Dict

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
        self.num = 0  # 已抽卡次数

    def normal_draw(self) -> Card:
        """
普通的抽一张卡
        :return: 享元的引用
        """
        self.num += 1
        t = random.random()

        # 二分查找变形，找到落在那个区间内
        left = 0
        right = len(self.p) - 1
        while left < right:
            mid = (left + right) // 2
            v = self.p[mid]
            if v > t:
                right = mid - 1
            elif v <= t:
                left = mid + 1
        return self.cards[left + 1]

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
    def __init__(self, num):
        """
        :param num:  默认以多少连抽进行
        """
        self.num = num


class Target:
    # 抽卡目标 享元模式
    def __init__(self, pattern: str, cards: Cards):
        self.cards = cards

        self.pattern = pattern
        strings = pattern.split()
        self.card_names = []
        for s in strings:
            if s not in [" ", "(", ")", "and", "or", "not"] and s not in self.card_names:
                self.card_names.append(s)
        # 将 a and not c 处理成 {} and not {} ,之后每次校验时按顺序将真值代入

    def if_suc(self) -> bool:
        """
判断是否成功。此版本的效率非常低，下次应该构建二叉树，并用解释器模块，并使用胜者树思想，使时间效率为O(1)
        :return: 是否达成目标
        """
        p = self.pattern
        for s in self.card_names:
            p = p.replace(s, str(self.cards.if_get[s]))
        return exec(p)


class Limit:
    # 保底
