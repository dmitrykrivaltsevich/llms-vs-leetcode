# Problem:
# The median is the middle value in an ordered integer list. If the size of the list is even, there is no middle value. So the median is the mean of the two middle values.
#
# For examples, if arr = [2,3,4], the median is 3.
# For examples, if arr = [1,2,3,4], the median is (2 + 3) / 2 = 2.5.
# You are given an integer array nums and an integer k. There is a sliding window of size k which is moving from the very left of the array to the very right. You can only see the k numbers in the window. Each time the sliding window moves right by one position.
#
# Return the median array for each window in the original array. Answers within 10-5 of the actual value will be accepted.
#
#
#
# Example 1:
#
# Input: nums = [1,3,-1,-3,5,3,6,7], k = 3
# Output: [1.00000,-1.00000,-1.00000,3.00000,5.00000,6.00000]
# Explanation:
# Window position                Median
# ---------------                -----
# [1  3  -1] -3  5  3  6  7        1
#  1 [3  -1  -3] 5  3  6  7       -1
#  1  3 [-1  -3  5] 3  6  7       -1
#  1  3  -1 [-3  5  3] 6  7        3
#  1  3  -1  -3 [5  3  6] 7        5
#  1  3  -1  -3  5 [3  6  7]       6
# Example 2:
#
# Input: nums = [1,2,3,4,2,3,1,4,2], k = 3
# Output: [2.00000,3.00000,3.00000,3.00000,2.00000,3.00000,2.00000]
#
#
# Constraints:
#
# 1 <= k <= nums.length <= 10^5
# -2^31 <= nums[i] <= 2^31 - 1
#
# Make sure the implementation can handle nums size of 100000 and k=50000. The "heapq" solution is not performant enough for this case.
#
# Make edits below this line only
#

from typing import List
import bisect

class Solution:
    def medianSlidingWindow(self, nums: List[int], k: int) -> List[float]:
        if not nums or k == 0:
            return []

        lower = []
        upper = []

        def insert(num):
            if not lower or num <= -lower[-1]:
                bisect.insort(lower, -num)
            else:
                bisect.insort(upper, num)

            # Balance the lists
            if len(lower) > len(upper) + 1:
                val = -bisect.pop(lower)
                bisect.insort(upper, val)
            elif len(upper) > len(lower):
                val = bisect.pop(upper)
                bisect.insort(lower, -val)

        def remove(num):
            if num <= get_median():
                index = bisect.bisect_left(lower, -num)
                if index < len(lower) and lower[index] == -num:
                    del lower[index]
            else:
                index = bisect.bisect_left(upper, num)
                if index < len(upper) and upper[index] == num:
                    del upper[index]

        def get_median():
            if k % 2 == 1:
                return -lower[-1]
            else:
                return (-lower[-1] + upper[0]) / 2

        result = []
        for i in range(len(nums)):
            insert(nums[i])
            if i >= k - 1:
                result.append(get_median())
                # Remove the element that is sliding out of the window
                remove(nums[i - (k - 1)])

        return result
