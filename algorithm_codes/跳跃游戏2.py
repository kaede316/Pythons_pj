# -*- coding: utf-8 -*-
# @Time    : 2025/9/26 08:44
# @Author  : kaede
# @File    : 跳跃游戏2.py
def jump(nums):
    steps = 0
    cur_right = 0  # 已建造的桥的右端点
    next_right = 0  # 下一座桥的右端点的最大值
    for i in range(len(nums) - 1):
        next_right = max(next_right, i + nums[i])  # 这里已经会考虑到最长距离
        if i == cur_right:  # 到达已建造的桥的右端点
            cur_right = next_right  # 造一座桥
            steps += 1
    return steps

print(jump([2,3,1,1,4]))