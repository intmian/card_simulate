# -*- coding: UTF-8 -*-
"""
AUTHOR:   MIAN
DATE:     2021/1/19
DESCRIBE: 小工具
"""
import random

random.seed()


class Card:
    # 卡片（单例
    def __init__(self, p: float, name: str):
        self.p = p
        self.name = name


class Cards:
    # 卡组
    def __init__(self, cards: list):
        self.cards = []
        self.p = []  # 每张卡片的概率范围
        t = 0
        for card in cards:
            t += card.p
            self.cards.append(card)
            self.p.append(t)

    def normal_draw(self) -> Card:
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

