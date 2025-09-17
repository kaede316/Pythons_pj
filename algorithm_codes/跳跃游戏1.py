# -*- coding: utf-8 -*-
# @Time    : 2025/9/17 23:08
# @Author  : kaede
# @File    : 跳跃游戏1.py
def canjump(arr):
    max_i = 0
    for i, jump_lenth in enumerate(arr):
        if max_i >= i and i + jump_lenth> max_i:
            max_i = i + jump_lenth
        return max_i > i