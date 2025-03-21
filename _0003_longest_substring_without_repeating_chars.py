class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        char_index_map = {}
        char_set = set()
        left = 0
        max_length = 0

        for right in range(len(s)):
            while s[right] in char_set:
                char_set.remove(s[left])
                left += 1
            char_set.add(s[right])
            char_index_map[s[right]] = right
            max_length = max(max_length, right - left + 1)

        return max_length
