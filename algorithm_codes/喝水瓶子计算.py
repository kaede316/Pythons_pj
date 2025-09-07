# def min_purchased_bottles(total_drank):
#     """
#     计算至少需要购买多少瓶矿泉水才能喝到指定数量的水
#     :param total_drank: 总共喝到的瓶数
#     :return: 至少需要购买的瓶数
#     """
#     purchased = 0
#     while True:
#         # 计算当前购买量能喝到的总瓶数
#         total_from_purchase = purchased
#         temp = purchased
#         while temp >= 5:
#             exchanged = temp // 5  # 本次能换到的瓶数
#             total_from_purchase += exchanged
#             temp = temp % 5 + exchanged  # 剩余空瓶 + 新换瓶喝完后的空瓶
#
#         if total_from_purchase >= total_drank:
#             return purchased
#
#         purchased += 1


# # 测试
# total_drank = 189
# result = min_purchased_bottles(total_drank)
# print(f"总共喝了 {total_drank} 瓶矿泉水，至少需要购买 {result} 瓶")
#
# ###############
def min_purchased_bottles_efficient(total_drank):
    """
    使用数学公式计算最小购买量（更高效）
    """
    # 从近似值开始搜索
    approx = int(total_drank * 0.8)  # 因为 1.25x ≈ total_drank

    for x in range(approx, total_drank + 1):
        total_possible = x
        temp = x

        # 计算能换到的总瓶数
        while temp >= 5:
            exchanged = temp // 5
            total_possible += exchanged
            temp = temp % 5 + exchanged

        if total_possible >= total_drank:
            return x

    return total_drank  # 如果没找到（理论上不会发生）
total_drank = 189
result = min_purchased_bottles_efficient(total_drank)
print(f"总共喝了 {total_drank} 瓶矿泉水，至少需要购买 {result} 瓶")


################
"""
总的=买的 + 换的 = k * 换的 + 剩下的
换的 = （总的-剩下的）% k
买的 = 总 - 换的
"""
# def min_buttle(total_drank, k):
#     for i in range(1,k):
#         if (total_drank - i)%k == 0:
#             ans = total_drank - (total_drank - i)//k
#             print(ans)
# min_buttle(189,5)