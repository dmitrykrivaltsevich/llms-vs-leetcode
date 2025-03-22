class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        m, n = len(s), len(p)
        dp = [[False] * (n + 1) for _ in range(2)]

        # Base case: empty pattern matches empty string
        dp[0][0] = True

        # Handle patterns like a*, a*b*, a*b*c*
        for j in range(2, n + 1):
            if p[j - 1] == '*':
                dp[0][j] = dp[0][j - 2]

        # Fill the dp table
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if p[j - 1] == s[i - 1] or p[j - 1] == '.':
                    dp[i % 2][j] = dp[(i - 1) % 2][j - 1]
                elif p[j - 1] == '*':
                    # Two cases:
                    # 1. '*' matches zero occurrence of the preceding element
                    # 2. '*' matches one or more occurrences of the preceding element
                    dp[i % 2][j] = dp[i % 2][j - 2] or (dp[(i - 1) % 2][j] and (p[j - 2] == s[i - 1] or p[j - 2] == '.'))

        return dp[m % 2][n]
