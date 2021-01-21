# -*- coding: UTF-8 -*-
"""
AUTHOR:   MIAN
DATE:     2021/1/21
DESCRIBE: 数学运算
"""
import numpy
import typing


def binary_search_in(arr, l, r, v):
    m = (l + r) // 2
    if l == r:
        return l
    if arr[m] > v:
        return binary_search_in(arr, l, m - 1, v)
    if arr[m] < v:
        return binary_search_in(arr, m, r - 1, v)


def binary_search(arr, v, lr=True):
    """
二分查找
    :param arr: 数组
    :param v: 值
    :param lr: 当不正好落在v上时，返回偏左的还是偏右的。True 左，False 右
    :return: (index,value)
    """
    re_index = binary_search_in(arr, 0, len(arr) - 1, v)
    if arr[re_index] == v:
        return re_index, v
    elif lr:
        return re_index - 1, arr[re_index - 1]
    else:
        return re_index + 1, arr[re_index + 1]


class Math:
    def __init__(self, nums: list):
        self._nums = sorted(nums)
        self._mean = numpy.mean(nums)
        self._std = numpy.std(nums)
        self._len = len(nums)

    def mean(self) -> float:
        return self._mean

    def std(self) -> float:
        return self._std

    def n_std_value(self, n) -> (float, float, float):
        """
返回（若干个个标准差内）的上下限及所占人数
        :return: 人数/总人数,左界，右界
        """
        left = self._mean - self._std * n
        right = self._mean + self._std * n
        if left < self._nums[0]:
            li = 0
            lv = self._nums[0]
        else:
            li, lv = binary_search(self._nums, left, True)
        if right > self._nums[self._len - 1]:
            ri = self._len - 1
            rv = self._nums[self._len - 1]
        else:
            ri, rv = binary_search(self._nums, right, False)
        return (ri - li + 1) / self._len, li, lv, ri, rv

    def normal(self):
        return self.n_std_value(1)

    def rare(self):
        return self.n_std_value(2)

    def super_rare(self):
        return self.n_std_value(3)

    def ultra_rare(self):
        return self.n_std_value(4)

    def output(self):
        print("数据总量：", self._len)
        print("均值：", self._mean)
        print("标准差：", self._std)
        print("依次向下找到自己的运气区间即可")

        import matplotlib.pyplot as plt
        plt.xlabel("次数")
        plt.title("人数")

        plt.hist(self._nums,bins=100)
        plt.show()
        a = self.normal()
        b = self.rare()
        c = self.super_rare()
        d = self.ultra_rare()
        l = self._len
        print("运气极好({:.4%}):{}次~{}次".format((d[1] - 1) / l, self._nums[0], self._nums[d[1] - 1]))
        print("运气很好 ({:.4%}):{}次~{}次".format((c[1] - d[1]) / l, d[2], self._nums[c[1] - 1]))
        print("运气 好 ({:.4%}):{}次~{}次".format((b[1] - c[1]) / l, c[2], self._nums[b[1] - 1]))
        print("运气较好 ({:.4%}):{}次~{}次".format((a[1] - b[1]) / l, b[2], self._nums[a[1] - 1]))
        print("运气常见({:.4%}):{}次~{}次".format(a[0], a[2], a[4]))
        print("运气较差({:.4%}):{}次~{}次".format((b[3] - a[3]) / l, self._nums[a[3] + 1], b[4]))
        print("运气 差({:.4%}):{}次~{}次".format((c[3] - b[3]) / l, self._nums[b[3] + 1], c[4]))
        print("运气很差({:.4%}):{}次~{}次".format((d[3] - c[3]) / l, self._nums[c[3] + 1], d[4]))
        print("运气极差({:.4%}):{}次~{}次".format((self._len - d[3]) / l, self._nums[d[3] + 1], self._nums[self._len - 1]))


if __name__ == '__main__':
    l = numpy.random.normal(200, 20, 10000000)
    m = Math(l)
    m.output()
