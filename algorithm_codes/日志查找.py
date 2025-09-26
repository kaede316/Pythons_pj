# -*- coding: utf-8 -*-
# @Time    : 2025/9/26 07:57
# @Author  : kaede
# @File    : 日志查找.py

logs = """71000, 146320, 1, 0
72000, 71836, 1, 0
88000, 3492, 1, 0
89000, 153764, 1, 0
95000, 154676, 1, 0"""
list_logs = logs.splitlines()
a_list = []
# 预处理成列表
for line in list_logs:
    parts = [int(part.strip()) for part in line.split(",")]
    a_list.append(parts)
time_cost = 0
time_cost_list = []
flag = False
for i in range(1, len(a_list)):
    if int(a_list[i][0]) - int(a_list[i-1][0]) > 1000:
        time_cost_list.append((int(a_list[i-1][0]), int(a_list[i][0])))



print(time_cost_list)