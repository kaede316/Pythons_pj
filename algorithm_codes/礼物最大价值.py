# -*- coding: utf-8 -*-
# @Time    : 2025/9/17 22:28
# @Author  : kaede
# @File    : 礼物最大价值.py
def max_value(gift):
    m = len(gift)
    n = len(gift[0])
    res = [ [0 for _ in range(n)] for _ in range(m)]
    res[0][0] = gift[0][0]
    for i in range(n):
        res[0][i] = res[0][i-1] + gift[0][i]
    for j in range(m):
        res[j][0] = res[j-1][0] + gift[j][0]
    for i in range(1,m):
        for j in range(1,n):
            res[i][j] = max(res[i-1][j], res[i][j-1]) + gift[i][j]
    return res[-1][-1]

gift = [
    [1, 3, 1],
    [1, 5, 1],
    [4, 2, 1]
]
print(max_value(gift))