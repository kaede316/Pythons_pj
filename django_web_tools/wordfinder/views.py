#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time : 2025/2/12 0:55 
# @Author : Kaede
from django.shortcuts import render
from collections import Counter

word_data = []
with open('words.txt', 'r') as f:
    for word in f.read().splitlines():
        word = word.strip().lower()
        if len(word) < 2:  # 忽略单字母单词
            continue
        word_data.append({
            "text": word,
            "counter": Counter(word)
        })

def word_finder(request):
    found_words = []
    if request.method == 'POST':
        # 处理输入
        letters = request.POST.get('letters', '').lower().strip()
        filtered = [c for c in letters if c.isalpha()]
        if not filtered:
            return render(request, 'word_finder.html', {'error': "请输入正确的有效字母"})

        input_counter = Counter(filtered)

        # 快速过滤词典
        for entry in word_data:
            word_counter = entry["counter"]
            # 检查每个字母是否不超过输入数量
            valid = all(word_counter[char] <= input_counter.get(char, 0) for char in word_counter)
            if valid:
                found_words.append(entry["text"])

        # 按长度和字母排序
        found_words.sort(key=lambda x: (len(x), x))

    return render(request, 'word_finder.html', {'words': found_words})