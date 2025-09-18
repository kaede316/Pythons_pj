# -*- coding: utf-8 -*-
# @Time    : 2025/9/19 07:10
# @Author  : kaede
# @File    : 括号匹配.py
def kuohao(a_str):
    dic = {"}":"{","]":"[",")":"("}
    a_list = []

    for s in a_str:
        if s in dic.values():       # 左括号
            a_list.append(s)
        elif s in dic:  # 右括号
            if not a_list or a_list.pop() != dic[s]:
                return False
        else:
            return False

    return not a_list

# 测试
print(kuohao("()"))       # True
print(kuohao("([{}])"))   # True
print(kuohao("([)]"))     # False
print(kuohao("((())"))    # False