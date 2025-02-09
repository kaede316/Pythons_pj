from flask import Flask, render_template, request
from collections import Counter

app = Flask(__name__)

# 预加载词典并计算字母频率
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


# 主页面
@app.route('/')
def index():
    return render_template('index.html')


# 高效单词查找器功能页面
@app.route('/word-finder', methods=['GET', 'POST'])
def word_finder():
    found_words = []
    if request.method == 'POST':
        # 处理输入
        letters = request.form['letters'].lower().strip()
        filtered = [c for c in letters if c.isalpha()]
        if not filtered:
            return render_template('word_finder.html', error="请输入正确的有效字母")

        input_counter = Counter(filtered)

        # 快速过滤词典
        for entry in word_data:
            word_counter = entry["counter"]
            # 检查每个字母是否不超过输入数量
            valid = all(
                word_counter[char] <= input_counter.get(char, 0)
                for char in word_counter
            )
            if valid:
                found_words.append(entry["text"])

        # 按长度和字母排序
        found_words.sort(key=lambda x: (len(x), x))

    return render_template('word_finder.html', words=found_words)

# 添加大小写转换功能
@app.route('/case-converter', methods=['GET', 'POST'])
def case_converter():
    result = ""
    if request.method == 'POST':
        input_text = request.form.get('letters', '').strip()
        if input_text:
            # 检测输入内容并进行大小写转换
            if input_text.islower():
                result = input_text.upper()
            elif input_text.isupper():
                result = input_text.lower()
            else:
                result = "输入内容必须是纯大写或纯小写！"
    return render_template('case_converter.html', result=result)

# 判断是否为闰年的逻辑
@app.route('/leap-year-checker', methods=['GET', 'POST'])
def leap_year_checker():
    result = None
    error = None
    year = None

    if request.method == 'POST':
        try:
            year = int(request.form['year'])
            if year <= 0:
                raise ValueError
            # 闰年判断逻辑
            if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                result = True
            else:
                result = False
        except ValueError:
            error = "请输入有效的正整数年份"

    return render_template('leap_year_checker.html', result=result, year=year, error=error)

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8080, debug=True)
    app.run(host='127.0.0.1', port=8080, debug=True)