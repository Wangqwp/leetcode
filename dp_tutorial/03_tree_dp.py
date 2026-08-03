# ============================================
# 树形DP (Tree DP) 教学模板
# ============================================

# ============================================
# 一、树形DP核心思想
# ============================================
# 问题：在树结构上求最优解
# 思路：后序遍历（DFS），子节点计算完后更新父节点
# 关键：区分"选/不选"或"选/不选根节点"的状态

# ============================================
# 二、基础：二叉树的最大路径和 (LeetCode 124)
# ============================================
# 问题：找树中任意路径的最大和（路径不必经过根）

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def maxPathSum(root):
    """
    树形DP经典题
    返回：整棵树的最大路径和
    """
    max_sum = float('-inf')
    
    def dfs(node):
        nonlocal max_sum
        if not node:
            return 0
        
        # 左子树最大贡献（负数则舍弃）
        left = max(dfs(node.left), 0)
        # 右子树最大贡献
        right = max(dfs(node.right), 0)
        
        # 经过当前节点的最大路径和（可能成为最终答案）
        path_sum = node.val + left + right
        max_sum = max(max_sum, path_sum)
        
        # 返回给父节点的最大贡献（只能选一边）
        return node.val + max(left, right)
    
    dfs(root)
    return max_sum


# ============================================
# 三、打家劫舍 III (LeetCode 337)
# ============================================
# 问题：树上不能选相邻节点，求最大价值
# 状态：dp[node][0] = 不选node的最大值
#       dp[node][1] = 选node的最大值

def robTree(root):
    """
    树形DP：选/不选问题
    返回 (不选当前节点的最大值, 选当前节点的最大值)
    """
    def dfs(node):
        if not node:
            return (0, 0)
        
        left = dfs(node.left)
        right = dfs(node.right)
        
        # 不选当前节点：子节点可选可不选
        not_rob = max(left) + max(right)
        # 选当前节点：子节点不能选
        rob = node.val + left[0] + right[0]
        
        return (not_rob, rob)
    
    return max(dfs(root))


# ============================================
# 四、二叉树的直径 (LeetCode 543)
# ============================================
# 问题：求树中任意两节点间最长路径的边数

def diameterOfBinaryTree(root):
    """
    树形DP：求最长路径
    """
    max_dia = 0
    
    def depth(node):
        nonlocal max_dia
        if not node:
            return 0
        
        left = depth(node.left)
        right = depth(node.right)
        
        # 更新直径（经过当前节点的最长路径）
        max_dia = max(max_dia, left + right)
        
        # 返回最大深度
        return max(left, right) + 1
    
    depth(root)
    return max_dia


# ============================================
# 五、二叉树的最长同值路径 (LeetCode 687)
# ============================================

def longestUnivaluePath(root):
    """
    树形DP：求最长同值路径
    """
    max_len = 0
    
    def dfs(node):
        nonlocal max_len
        if not node:
            return 0
        
        left = dfs(node.left)
        right = dfs(node.right)
        
        left_arrow = left + 1 if node.left and node.left.val == node.val else 0
        right_arrow = right + 1 if node.right and node.right.val == node.val else 0
        
        max_len = max(max_len, left_arrow + right_arrow)
        
        return max(left_arrow, right_arrow)
    
    dfs(root)
    return max_len


# ============================================
# 六、N 叉树的最大深度 (LeetCode 559)
# ============================================

class NAryNode:
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children if children else []

def maxDepthNAry(root):
    """
    N叉树的DFS
    """
    if not root:
        return 0
    
    max_d = 0
    for child in root.children:
        max_d = max(max_d, maxDepthNAry(child))
    
    return max_d + 1


# ============================================
# 七、树的最长路径 (通用模板)
# ============================================

def treeLongestPath(root):
    """
    求树中最远两节点的距离（无向树）
    返回 (直径, 从根出发的最长单链)
    """
    def dfs(node, parent):
        longest = 0       # 经过 node 的最长路径（直径候选）
        single = 0        # 从 node 向下走的最长单链
        
        for child in node.children:
            if child != parent:
                child_longest, child_single = dfs(child, node)
                longest = max(longest, child_longest)
                single = max(single, child_single + 1)
        
        # 但这里没考虑两个最长子链拼接的情况，需要用排序优化
        return longest, single
    
    # 完整实现需要记录 top-2 最长子链
    ans = 0
    
    def dfs_v2(node, parent):
        nonlocal ans
        top2 = [0, 0]  # 存最长的两条子链
        
        for child in node.children:
            if child != parent:
                chain = dfs_v2(child, node) + 1
                if chain > top2[0]:
                    top2[1] = top2[0]
                    top2[0] = chain
                elif chain > top2[1]:
                    top2[1] = chain
        
        ans = max(ans, top2[0] + top2[1])
        return top2[0]
    
    dfs_v2(root, -1)
    return ans


# ============================================
# 八、练习题推荐
# ============================================
# Easy:
#   - 543. 二叉树的直径
#   - 559. N叉树的最大深度
#   - 687. 最长同值路径
#
# Medium:
#   - 337. 打家劫舍 III
#   - 124. 二叉树中的最大路径和
#   - 834. 树中距离之和
#
# Hard:
#   - 968. 监控二叉树
#   - 1530. 好叶子节点对的数量

if __name__ == "__main__":
    # 构建测试树
    #       1
    #      / \
    #     2   3
    #    / \   \
    #   4   5   6
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    root.right.right = TreeNode(6)
    
    print(f"最大路径和: {maxPathSum(root)}")
    print(f"打家劫舍III: {robTree(root)}")
    print(f"二叉树直径: {diameterOfBinaryTree(root)}")
