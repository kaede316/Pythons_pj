# -*- coding: utf-8 -*-
# @Time    : 2025/9/17 21:32
# @Author  : kaede
# @File    : inser_sort.py
def inser_sort(arr):
    n = len(arr)
    for i in range(1,n):
        current = arr[i]
        j = i -1
        while j > 0 and arr[j] > current:
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = current
    return arr

print(inser_sort([1,4,3,2,5]))