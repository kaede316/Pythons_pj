#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time : 2025/2/7 23:46 
# @Author : Kaede
import os

def show_directory_structure(path, prefix=""):
    """
    显示指定路径下的目录结构
    :param path: 要展示的目录路径
    :param prefix: 用于缩进的前缀字符串
    """
    # 获取目录内容
    try:
        items = os.listdir(path)   # 返回一个列表
        # print(f"items is {items}")      # 当前层级的文件或者目录名字
        # 对目录内容进行排序，目录在前，文件在后
        items.sort(key=lambda x: (not os.path.isdir(os.path.join(path, x)), x))

        # 遍历所有项目
        for index, item in enumerate(items):
            item_path = os.path.join(path, item)   # 把父级目录和当前文件拼接到一起
            is_last = index == len(items) - 1

            # 确定显示的连接符
            connector = "└── " if is_last else "├── "

            # 打印当前项目
            print(f"{prefix}{connector}{item}")

            # 如果是目录，递归显示其内容
            if os.path.isdir(item_path):
                # 确定下一级的前缀
                next_prefix = prefix + ("    " if is_last else "│   ")
                show_directory_structure(item_path, next_prefix)
    except Exception as e:
        print(f"错误: {e}")

def print_directory_tree(path):
    """
    打印目录树的主函数
    :param path: 要展示的目录路径
    """
    if not os.path.exists(path):
        print(f"路径不存在: {path}")
        return

    print(f"\n目录结构: {path}")
    print(".")
    show_directory_structure(path)


# 使用示例
if __name__ == "__main__":
    print(f"当前文件为：{os.path.abspath(__file__)}")     #当前文件
    # 获取当前文件所在目录的路径
    # 用于获取文件路径中的目录部分。
    directory_path = os.path.dirname(os.path.abspath(__file__))
    print(f"当前文件路径: {directory_path}")

    # 获取上一级目录的路径
    parent_dir_path = os.path.dirname(directory_path)
    print(f"当前文件路径: {parent_dir_path}")
    print_directory_tree(directory_path)