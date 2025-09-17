# -*- coding: utf-8 -*-
# @Time    : 2025/9/17 21:37
# @Author  : kaede
# @File    : binary_search.py
def binary_serch(arr, target):
    start, end = 0, len(arr) - 1
    while True:
        if end <= start:
            if target == arr[start]:
                return start
            elif target == arr[end]:
                return end
            else:
                return None
        mid = (start + end) // 2
        if arr[mid] > target:
            end = mid
        elif arr[mid] < target:
            start = mid
        else:
            return mid
arr = [1,2,3,4,5,6,7,9]
print(binary_serch(arr,5))