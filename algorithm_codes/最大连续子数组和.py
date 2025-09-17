# -*- coding: utf-8 -*-
# @Time    : 2025/9/17 21:56
# @Author  : kaede
# @File    : 最大连续子数组和.py
def max_sub_arr(arr):
    n =len(arr)
    max_curret = max_all = arr[0]
    for i in range(1,n):
        max_curret = max(arr[i], max_curret + arr[i])
        max_all = max(max_curret, max_all)
    return max_all
arr = [1,5,-10,2,5,-3,2,6,-3,1]
print(max_sub_arr(arr))
