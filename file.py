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
        [保底抽数,保底group,保底类型(随机|未获取),若提前取得是否会重置,保底方式（给出|替换）],
        ...
    ]
}
"""