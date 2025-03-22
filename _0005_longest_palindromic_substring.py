class Solution:
    def longestPalindrome(self, s: str) -> str:
        if not s or len(s) == 1:
            return s

        # Transform the string to handle even-length palindromes
        transformed = '#'.join(f'^{s}$')
        n = len(transformed)
        P = [0] * n
        C = R = 0

        for i in range(1, n - 1):
            mirror = 2 * C - i

            if i < R:
                P[i] = min(R - i, P[mirror])

            # Attempt to expand palindrome centered at i
            while transformed[i + 1 + P[i]] == transformed[i - 1 - P[i]]:
                P[i] += 1

            # If palindrome centered at i expands past R,
            # adjust center based on expanded palindrome.
            if i + P[i] > R:
                C, R = i, i + P[i]

        # Find the maximum element in P.
        max_len, center_index = max((n, i) for i, n in enumerate(P))
        start = (center_index - max_len) // 2

        return s[start:start + max_len]
