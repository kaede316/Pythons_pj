# -*- coding: utf-8 -*-
# @Time    : 2025/9/17 21:36
# @Author  : kaede
# @File    : quick_dort.py
def quick_sort(arr):
    n = len(arr)
    if n <= 1:
        return arr
    pivot = arr[n // 2]
    left_sub_arr = [x for x in arr if x < pivot]
    mid = [x for x in arr if x == pivot]
    right_sub_arr = [x for x in arr if x > pivot]

    return quick_sort(left_sub_arr) + mid + quick_sort(right_sub_arr)
print(quick_sort([1,5,6,3,2]))