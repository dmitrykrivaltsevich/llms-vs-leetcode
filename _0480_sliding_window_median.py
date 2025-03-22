from typing import List

class Solution:
    def medianSlidingWindow(self, nums: List[int], k: int) -> List[float]:
        if not nums or k == 0:
            return []

        # Two sorted lists to maintain the lower and upper halves of the window elements
        lower = []
        upper = []

        def insert(num):
            if not lower or num <= lower[-1]:
                lower.append(num)
            else:
                upper.append(num)

            # Balance the lists
            if len(lower) > len(upper) + 1:
                upper.append(lower.pop())
            elif len(upper) > len(lower):
                lower.append(upper.pop())

        def remove(num):
            if num <= lower[-1]:
                lower.remove(num)
            else:
                upper.remove(num)

            # Balance the lists
            if len(lower) > len(upper) + 1:
                upper.append(lower.pop())
            elif len(upper) > len(lower):
                lower.append(upper.pop())

        def get_median():
            if k % 2 == 1:
                return float(lower[-1])
            else:
                return (lower[-1] + upper[0]) / 2

        result = []
        for i in range(len(nums)):
            insert(nums[i])
            if i >= k - 1:
                result.append(get_median())
                remove(nums[i - (k - 1)])

        return result
