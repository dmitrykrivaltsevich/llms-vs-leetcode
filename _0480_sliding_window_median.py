from typing import List
import heapq

class Solution:
    def medianSlidingWindow(self, nums: List[int], k: int) -> List[float]:
        if not nums or k == 0:
            return []

        # Min-heap for the larger half of the numbers
        max_heap = []
        # Max-heap for the smaller half of the numbers (inverted to use min-heap)
        min_heap = []

        def add_num(num):
            if not max_heap or num <= -max_heap[0]:
                heapq.heappush(max_heap, -num)
            else:
                heapq.heappush(min_heap, num)

            # Balance the heaps
            if len(max_heap) > len(min_heap) + 1:
                heapq.heappush(min_heap, -heapq.heappop(max_heap))
            elif len(min_heap) > len(max_heap):
                heapq.heappush(max_heap, -heapq.heappop(min_heap))

        def remove_num(num):
            if num <= -max_heap[0]:
                max_heap.remove(-num)
                heapq.heapify(max_heap)
            else:
                min_heap.remove(num)
                heapq.heapify(min_heap)

            # Balance the heaps
            if len(max_heap) > len(min_heap) + 1:
                heapq.heappush(min_heap, -heapq.heappop(max_heap))
            elif len(min_heap) > len(max_heap):
                heapq.heappush(max_heap, -heapq.heappop(min_heap))

        def get_median():
            if k % 2 == 1:
                return float(-max_heap[0])
            else:
                return (-max_heap[0] + min_heap[0]) / 2

        result = []
        for i in range(len(nums)):
            add_num(nums[i])
            if i >= k - 1:
                result.append(get_median())
                remove_num(nums[i - (k - 1)])

        return result
