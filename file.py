# -*- coding: UTF-8 -*-
"""
AUTHOR:   MIAN
DATE:     2021/1/19
DESCRIBE: 文件处理
"""

"""
文件格式：x.json
{
    "cards":{
        "a": 概率（小数形式）,  // a不得包含and or not ( )
        "b": p,
        ...
    },
    "must_get":"a and ( b or not c )", // 任何两个部分之间必须要有空格, 使用半角括号
    "once_draw": n, 一次抽几张
    "group": {
        "group1": ["a",...],
        ...
    }
    "limit":[
        [保底抽数,保底group,保底类型(随机 1 |未获取(默认采用最优策略选择概率最小的) 2),若提前取得是否会重置(当抽出保底卡后，是否重置保底 1 抽出后立刻重置count（幻书启示录） 2 抽出后不重置count，但不再触发（pcr 二星保底） 3 无（pcr 井）),保底方式（替换 1|附加 2）],
        # 保底类型为2时，系统默认玩家以抽齐为策略。例如克总（0.35%）、春田（0.7%）双保底时，若一井内都没出，则优先选择克总（次数期望最优）
        # 一个保底被触发且给出保底方式为1时，将不触发剩下的保底给出方式为1的保底，防止浪费保底，所以请把优先度高的放在上面
        ...
    ]
}
"""
