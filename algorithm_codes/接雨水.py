# -*- coding: utf-8 -*-
# @Time    : 2025/9/18 07:48
# @Author  : kaede
# @File    : 接雨水.py
def drop_rain(arry):
    sum = height_left = height_right = 0
    for i in range(len(arry)):
        height_left = max(arry[i], height_left)
        height_right = max(arry[-i-1], height_right)
        sum += height_left + height_right - arry[i]
    return sum - len(arry) * height_left

arr = [4,2,0,3,2,5]
print(drop_rain(arr))