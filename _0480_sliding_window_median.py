from typing import List
import heapq

class Solution:
    def medianSlidingWindow(self, nums: List[int], k: int) -> List[float]:
        if not nums or k == 0:
            return []

        max_heap = []  # Max-heap to store the smaller half of numbers
        min_heap = []  # Min-heap to store the larger half of numbers
        count_max = {}
        count_min = {}

        def add_number(num):
            if len(max_heap) == 0 or num <= -max_heap[0]:
                heapq.heappush(max_heap, -num)
                count_max[num] = count_max.get(num, 0) + 1
            else:
                heapq.heappush(min_heap, num)
                count_min[num] = count_min.get(num, 0) + 1

            # Balance the heaps
            if len(max_heap) > len(min_heap) + 1:
                val = -heapq.heappop(max_heap)
                heapq.heappush(min_heap, val)
                if count_max[val] == 1:
                    del count_max[val]
                else:
                    count_max[val] -= 1
            elif len(min_heap) > len(max_heap):
                val = heapq.heappop(min_heap)
                heapq.heappush(max_heap, -val)
                if count_min[val] == 1:
                    del count_min[val]
                else:
                    count_min[val] -= 1

        def remove_number(num):
            if num <= get_median():
                if count_max[num] == 1:
                    del count_max[num]
                else:
                    count_max[num] -= 1
            else:
                if count_min[num] == 1:
                    del count_min[num]
                else:
                    count_min[num] -= 1

        def get_median():
            if len(max_heap) == len(min_heap):
                return (-max_heap[0] + min_heap[0]) / 2
            else:
                return float(-max_heap[0])

        result = []
        for i in range(len(nums)):
            add_number(nums[i])
            if i >= k - 1:  # Window size is k
                result.append(get_median())
                # Remove the element that is sliding out of the window
                remove_number(nums[i - (k - 1)])

        return result
