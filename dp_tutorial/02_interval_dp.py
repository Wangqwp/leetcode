# ============================================
# 区间DP (Interval DP) 教学模板
# ============================================

# ============================================
# 一、区间DP核心思想
# ============================================
# 问题：在一段连续区间 [i, j] 上求最优解
# 状态：dp[i][j] 表示区间 [i, j] 的最优解
# 转移：枚举分割点 k，dp[i][j] = min/max(dp[i][k] + dp[k+1][j] + cost)
# 遍历顺序：区间长度从小到大

# 模板：
def interval_dp_template(arr):
    n = len(arr)
    dp = [[0] * n for _ in range(n)]
    
    # 长度从 2 开始（长度为 1 的区间不需要合并）
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float('inf')  # 求最小值
            for k in range(i, j):
                dp[i][j] = min(dp[i][j], dp[i][k] + dp[k+1][j] + cost(i, j, k))
    
    return dp[0][n-1]


# ============================================
# 二、经典例题：矩阵链乘法
# ============================================
# 问题：矩阵 A1(A2(A3*A4)) 乘法顺序不同，计算量不同
# 矩阵 Ai 的维度为 p[i-1] x p[i]
# 求最少乘法次数

def matrixChainOrder(p):
    """
    矩阵链乘法
    p: 维度数组，n 个矩阵有 n+1 个维度
    dp[i][j] = 从第 i 个矩阵到第 j 个矩阵的最少乘法次数
    """
    n = len(p) - 1  # 矩阵个数
    dp = [[0] * n for _ in range(n)]
    
    # length 是链的长度（矩阵个数）
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float('inf')
            for k in range(i, j):
                # dp[i][k]: 左半部分最优
                # dp[k+1][j]: 右半部分最优
                # p[i]*p[k+1]*p[j+1]: 合并两个结果的代价
                cost = dp[i][k] + dp[k+1][j] + p[i] * p[k+1] * p[j+1]
                dp[i][j] = min(dp[i][j], cost)
    
    return dp[0][n-1]


# ============================================
# 三、经典例题：石子合并
# ============================================
# 问题：n 堆石子排成一行，每次合并相邻两堆，代价为两堆之和
# 求合并成一堆的最小总代价

def stoneGame(stones):
    """
    石子合并（最小代价）
    dp[i][j] = 合并 [i, j] 区间石子的最小代价
    """
    n = len(stones)
    # 前缀和加速区间求和
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + stones[i]
    
    dp = [[0] * n for _ in range(n)]
    
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float('inf')
            total = prefix[j + 1] - prefix[i]  # 区间和
            for k in range(i, j):
                dp[i][j] = min(dp[i][j], dp[i][k] + dp[k+1][j] + total)
    
    return dp[0][n-1]


# ============================================
# 四、经典例题：戳气球 (LeetCode 312)
# ============================================
# 问题：戳破气球获得 nums[left]*nums[i]*nums[right] 的金币
# 求最大金币数
# 技巧：反向思维，从"戳破"变为"最后添加"

def maxCoins(nums):
    """
    戳气球
    dp[i][j] = 打破 (i, j) 开区间内所有气球的最大金币
    """
    n = len(nums)
    # 添加边界 1
    nums = [1] + nums + [1]
    
    dp = [[0] * (n + 2) for _ in range(n + 2)]
    
    # 从下往上，从左往右填表
    for i in range(n, -1, -1):
        for j in range(i + 2, n + 2):
            for k in range(i + 1, j):
                dp[i][j] = max(dp[i][j],
                               dp[i][k] + dp[k][j] + nums[i] * nums[k] * nums[j])
    
    return dp[0][n + 1]


# ============================================
# 五、经典例题：回文子串相关
# ============================================
# 问题：最长回文子串 / 回文分割

def longestPalindrome(s):
    """
    最长回文子串 (LeetCode 5)
    dp[i][j] = s[i:j+1] 是否是回文
    """
    n = len(s)
    dp = [[False] * n for _ in range(n)]
    start = 0
    max_len = 1
    
    # 单个字符是回文
    for i in range(n):
        dp[i][i] = True
    
    # 从长度 2 开始
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j]:
                if length == 2 or dp[i+1][j-1]:
                    dp[i][j] = True
                    if length > max_len:
                        max_len = length
                        start = i
    
    return s[start:start + max_len]


def minCut(s):
    """
    回文切割 (LeetCode 132)
    dp[i] = s[0:i+1] 的最少切割次数
    """
    n = len(s)
    # 先预处理回文
    is_pal = [[False] * n for _ in range(n)]
    for i in range(n):
        is_pal[i][i] = True
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j]:
                is_pal[i][j] = length == 2 or is_pal[i+1][j-1]
    
    # dp[i] = s[0..i] 的最少切割
    dp = [0] * n
    for i in range(n):
        if is_pal[0][i]:
            dp[i] = 0
        else:
            dp[i] = i  # 最坏情况：每个字符切一刀
            for j in range(1, i + 1):
                if is_pal[j][i]:
                    dp[i] = min(dp[i], dp[j-1] + 1)
    
    return dp[n-1]


# ============================================
# 六、练习题推荐
# ============================================
# Easy:
#   - 647. 回文子串数量
#
# Medium:
#   - 312. 戳气球
#   - 516. 最长回文子序列
#   - 1039. 多边形三角剖分的最低得分
#
# Hard:
#   - 546. 移除盒子
#   - 1000. 合并石头的最低成本

if __name__ == "__main__":
    # 测试矩阵链乘法
    p = [30, 35, 15, 5, 10, 20, 25]
    print(f"矩阵链最少乘法次数: {matrixChainOrder(p)}")
    
    # 测试石子合并
    stones = [3, 4, 6, 5]
    print(f"石子合并最小代价: {stoneGame(stones)}")
    
    # 测试戳气球
    nums = [3, 1, 5, 8]
    print(f"戳气球最大金币: {maxCoins(nums)}")
    
    # 测试最长回文子串
    s = "babad"
    print(f"最长回文子串: {longestPalindrome(s)}")
    
    # 测试回文切割
    s = "aab"
    print(f"回文最少切割: {minCut(s)}")
