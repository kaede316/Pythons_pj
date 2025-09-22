# -*- coding: utf-8 -*-
# @Time    : 2025/9/22 23:50
# @Author  : kaede
# @File    : 解括号.py
def flatten_parentheses(s):
    # 记录括号的嵌套深度
    depth = 0
    result = []

    for char in s:
        if char == '(':
            depth += 1
            # 只保留最外层的左括号
            if depth == 1:
                result.append(char)
        elif char == ')':
            depth -= 1
            # 只保留最外层的右括号
            if depth == 0:
                result.append(char)
        else:
            # 其他字符（数字和逗号）都保留
            result.append(char)

    return ''.join(result)


# 测试输入
input_str = "(1,2,3(4,5)),6,(7,(8,9))"
output_str = flatten_parentheses(input_str)

print("输入:", input_str)
print("输出:", output_str)