from typing import List
import heapq

class Solution:
    def medianSlidingWindow(self, nums: List[int], k: int) -> List[float]:
        if not nums or k == 0:
            return []

        max_heap = []  # Max-heap to store the smaller half of numbers
        min_heap = []  # Min-heap to store the larger half of numbers

        def add_number(num):
            if len(max_heap) == 0 or num <= -max_heap[0]:
                heapq.heappush(max_heap, -num)
            else:
                heapq.heappush(min_heap, num)

            # Balance the heaps
            if len(max_heap) > len(min_heap) + 1:
                heapq.heappush(min_heap, -heapq.heappop(max_heap))
            elif len(min_heap) > len(max_heap):
                heapq.heappush(max_heap, -heapq.heappop(min_heap))

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
                num_to_remove = nums[i - (k - 1)]
                if num_to_remove <= get_median():
                    max_heap.remove(-num_to_remove)
                    heapq.heapify(max_heap)
                else:
                    min_heap.remove(num_to_remove)
                    heapq.heapify(min_heap)

        return result
