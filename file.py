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
        "a": 概率（小数形式）,
        "b": p,
        ...
    },
    "must_get":"a & (b | c)", 此条一定要有,
    "once_draw": n, 一次抽几张
    "group": {
        "group1": ["a",...],
        ...
    }
    "limit":[
        [保底抽数,保底方式(随机|未获取),保底group],
        ...
    ]
}
"""