class Solution:
    def stoneGameIII(self, stoneValue):
        n = len(stoneValue)

        # dp[i] 表示从 i 开始，当前玩家领先多少分
        dp = [0] * (n + 3)

        # 从后往前计算
        for i in range(n - 1, -1, -1):

            dp[i] = float('-inf')

            total = 0

            # 最多拿三堆
            for k in range(3):
                if i + k < n:
                    total += stoneValue[i + k]

                    # 当前拿走 total，对手优势是 dp[i+k+1]
                    dp[i] = max(
                        dp[i],
                        total - dp[i+k+1]
                    )


        if dp[0] > 0:
            return "Alice"
        elif dp[0] < 0:
            return "Bob"
        else:
            return "Tie"