# -*- coding: utf-8 -*-
# @Time    : 2025/9/17 21:37
# @Author  : kaede
# @File    : binary_search.py
def binary_search(arr, target):
    start, end = 0, len(arr)-1
    while start <= end:
        mid = (start + end) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] > target:
            end = mid - 1
        elif arr[mid] < target:
            start = mid + 1
    return None
arr = [1,2,3,4,5,6,7,9]
print(binary_search(arr,5))