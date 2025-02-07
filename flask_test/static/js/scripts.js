function clearInput() {
    // 获取输入框元素
    const input = document.querySelector('input[name="letters"]');
    if (input) {
        input.value = ''; // 清空输入框
    }
}