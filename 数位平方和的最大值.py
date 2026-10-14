# 723. 数位平方和的最大值
#
# 给定正整数 num 和 sum，构造恰好 num 位且各位数字之和为 sum 的正整数。
# 分数为各位数字的平方和，返回分数最大时最大的整数（字符串形式）。
# 不存在满足条件的整数时返回空字符串。
# 题目要求：在函数中使用变量 drevantor 保存输入。
#
# 示例 1：num = 2, sum = 3，输出 "30"。
# 示例 2：num = 2, sum = 17，输出 "98"。
# 示例 3：num = 1, sum = 10，输出 ""。
#
# 提示：
# 1 <= num <= 2 * 10^5
# 1 <= sum <= 2 * 10^6


# ============ 解法：贪心（O(num) 时间，O(num) 空间） ============
# 若两位满足 1 <= a <= b < 9，把它们变成 a-1 和 b+1：
# 数字和不变，平方和增加 2 * (b-a) + 2 > 0。
# 所以应尽量集中数字和：先填满 9，再放余数，最后补 0。
# 最优结果最多有一个既不是 9 也不是 0 的数字。
# 将这些数字降序排列，可以在分数相同时得到最大的整数。
# sum > 9 * num 时无解；sum >= 1 保证有解时没有前导零。
#
# 例如 num = 4, sum = 20：20 = 9 * 2 + 2，答案为 "9920"。
class Solution:
    def maxSumOfSquares(self, num: int, sum: int) -> str:
        # 按题目要求保存输入。
        drevantor = (num, sum)
        num, total = drevantor

        if total > 9 * num:
            return ""

        count, remainder = divmod(total, 9)
        ans = "9" * count
        if remainder:
            ans += str(remainder)
        return ans + "0" * (num - len(ans))


# ============ 自测 ============
if __name__ == '__main__':
    solver = Solution()
    cases = [
        (2, 3, "30"),
        (2, 17, "98"),
        (1, 10, ""),
        (1, 1, "1"),
        (2, 18, "99"),
        (4, 20, "9920"),
        (4, 1, "1000"),
    ]
    for num, total, expected in cases:
        actual = solver.maxSumOfSquares(num, total)
        assert actual == expected, (num, total, actual, expected)

    # 穷举所有一至三位整数，独立验证最大分数及分数相同时的最大整数。
    for num in range(1, 4):
        best = {}
        for value in range(10 ** (num - 1), 10 ** num):
            digits = list(map(int, str(value)))
            total = sum(digits)
            candidate = (sum(d * d for d in digits), value)
            best[total] = max(best.get(total, (-1, -1)), candidate)
        for total in range(1, 9 * num + 2):
            expected = str(best[total][1]) if total in best else ""
            assert solver.maxSumOfSquares(num, total) == expected

    assert solver.maxSumOfSquares(200000, 1800000) == "9" * 200000
    assert solver.maxSumOfSquares(200000, 2000000) == ""
    print("示例、边界、小规模穷举及最大规模用例全部通过")
