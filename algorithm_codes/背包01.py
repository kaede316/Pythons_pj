from mpmath.calculus.differentiation import dpoly
from numpy.linalg.lapack_lite import dorgqr


def pacage01(weight, value, capacity):
    n = len(weight)
    dp =  [[0 for _ in range(capacity + 1)] for _ in range(n + 1) ]

    for i in range(1, n+1):
        for j in range(1, capacity+1):
            if weight[i-1] <= j:
                dp[i][j] = max(dp[i-1][j], value[i-1] + dp[i-1][j-weight[i-1]])
            else:
                dp[i][j] = dp[i - 1][j]

    return dp[n][capacity]

# 示例
values = [60, 100, 120]
weights = [10, 20, 30]
capacity = 50
print("01背包最大价值:", pacage01(weights, values, capacity))  # 输出: 220

########### 改进下空间
def pacage01_less(weight, value, capacity):
    n = len(weight)
    dp = [0 for _ in range(capacity+1)]

    for i in range(n):
        for j in range(capacity, weight[i]-1, -1):
            dp[j] = max(dp[j], value[i] + dp[j-weight[i]])
    return dp[-1]


values = [60, 100, 120]
weights = [10, 20, 30]
capacity = 50
print("01背包最大价值:", pacage01_less(weights, values, capacity))  # 输出: 220