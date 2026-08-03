# ============================================
# 背包DP (Knapsack DP) 教学模板
# ============================================

# ============================================
# 一、0/1 背包
# ============================================
# 问题：N 个物品，每个只能选一次，容量为 W 的背包，求最大价值
# 状态：dp[i][j] = 前 i 个物品，容量为 j 时的最大价值
# 转移：dp[i][j] = max(dp[i-1][j], dp[i-1][j-w[i]] + v[i])

def knapsack_01(weights, values, capacity):
    """
    0/1 背包：每个物品只能选一次
    时间复杂度 O(N*W)，空间 O(W) 优化后
    """
    n = len(weights)
    dp = [0] * (capacity + 1)
    
    for i in range(n):
        # 逆序遍历，保证每个物品只用一次
        for j in range(capacity, weights[i] - 1, -1):
            dp[j] = max(dp[j], dp[j - weights[i]] + values[i])
    
    return dp[capacity]


# 经典例题：分割等和子集 (LeetCode 416)
def canPartition(nums):
    """
    能否将数组分成和相等的两部分
    转化为：能否从数组中选出和为 sum/2 的子集
    """
    total = sum(nums)
    if total % 2 != 0:
        return False
    
    target = total // 2
    dp = [False] * (target + 1)
    dp[0] = True
    
    for num in nums:
        for j in range(target, num - 1, -1):
            dp[j] = dp[j] or dp[j - num]
    
    return dp[target]


# 经典例题：零钱兑换 (LeetCode 322)
def coinChange(coins, amount):
    """
    用最少的硬币凑出 amount
    注意：这是完全背包（每个硬币可用多次）
    """
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    for coin in coins:
        for j in range(coin, amount + 1):  # 正序 = 完全背包
            dp[j] = min(dp[j], dp[j - coin] + 1)
    
    return dp[amount] if dp[amount] != float('inf') else -1


# ============================================
# 二、完全背包
# ============================================
# 区别：物品可以选无限次
# 转移：dp[i][j] = max(dp[i-1][j], dp[i][j-w[i]] + v[i])
# 实现区别：内层循环正序遍历

def knapsack_complete(weights, values, capacity):
    """
    完全背包：每个物品可用无限次
    """
    n = len(weights)
    dp = [0] * (capacity + 1)
    
    for i in range(n):
        # 正序遍历，允许重复选择
        for j in range(weights[i], capacity + 1):
            dp[j] = max(dp[j], dp[j - weights[i]] + values[i])
    
    return dp[capacity]


# ============================================
# 三、多重背包
# ============================================
# 问题：每个物品有数量限制 count[i]
# 优化：二进制拆分，将 count 拆成 1,2,4,8... 的组合

def knapsack_multiple(weights, values, counts, capacity):
    """
    多重背包：每个物品有数量限制
    使用二进制拆分优化
    """
    # 二进制拆分
    new_weights = []
    new_values = []
    
    for i in range(len(weights)):
        k = 1
        while k <= counts[i]:
            new_weights.append(weights[i] * k)
            new_values.append(values[i] * k)
            counts[i] -= k
            k *= 2
        if counts[i] > 0:
            new_weights.append(weights[i] * counts[i])
            new_values.append(values[i] * counts[i])
    
    # 转化为 0/1 背包
    return knapsack_01(new_weights, new_values, capacity)


# ============================================
# 四、分组背包
# ============================================
# 问题：物品分成若干组，每组最多选一个

def knapsack_group(groups, capacity):
    """
    groups: 列表的列表，每个子列表是一组 (weight, value) 元组
    """
    dp = [0] * (capacity + 1)
    
    for group in groups:
        for j in range(capacity, -1, -1):  # 逆序
            for w, v in group:
                if j >= w:
                    dp[j] = max(dp[j], dp[j - w] + v)
    
    return dp[capacity]


# ============================================
# 五、练习题推荐
# ============================================
# Easy:
#   - 746. 使用最小花费爬楼梯
#   - 518. 零钱兑换 II (完全背包求方案数)
#
# Medium:
#   - 416. 分割等和子集
#   - 494. 目标和
#   - 1049. 最后一块石头的重量 II
#
# Hard:
#   - 879. 盈利计划 (分组背包)
#   - 1187. 使数组严格递增 (DP + 二分)

if __name__ == "__main__":
    # 测试 0/1 背包
    weights = [2, 3, 4, 5]
    values = [3, 4, 5, 6]
    capacity = 8
    print(f"0/1 背包最大价值: {knapsack_01(weights, values, capacity)}")
    
    # 测试分割等和子集
    nums = [1, 5, 11, 5]
    print(f"能否分割等和子集: {canPartition(nums)}")
    
    # 测试零钱兑换
    coins = [1, 2, 5]
    amount = 11
    print(f"零钱兑换最少硬币: {coinChange(coins, amount)}")
