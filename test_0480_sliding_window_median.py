import unittest
from _0480_sliding_window_median import Solution

class TestSlidingWindowMedian(unittest.TestCase):

    def setUp(self):
        self.solution = Solution()

    def test_example_1(self):
        nums = [1, 3, -1, -3, 5, 3, 6, 7]
        k = 3
        expected_output = [1.0, -1.0, -1.0, 3.0, 5.0, 6.0]
        self.assertEqual(self.solution.medianSlidingWindow(nums, k), expected_output)

    def test_example_2(self):
        nums = [1, 2, 3, 4, 2, 3, 1, 4, 2]
        k = 3
        expected_output = [2.0, 3.0, 3.0, 3.0, 2.0, 3.0, 2.0]
        self.assertEqual(self.solution.medianSlidingWindow(nums, k), expected_output)

    def test_empty_array(self):
        nums = []
        k = 3
        expected_output = []
        self.assertEqual(self.solution.medianSlidingWindow(nums, k), expected_output)

    def test_k_zero(self):
        nums = [1, 2, 3]
        k = 0
        expected_output = []
        self.assertEqual(self.solution.medianSlidingWindow(nums, k), expected_output)

    def test_single_element_window(self):
        nums = [1, 2, 3, 4, 5]
        k = 1
        expected_output = [1.0, 2.0, 3.0, 4.0, 5.0]
        self.assertEqual(self.solution.medianSlidingWindow(nums, k), expected_output)

    @unittest.timeout(3)
    def test_large_array(self):
        nums = list(range(100000))
        k = 50000
        expected_output = [49999.5] * (len(nums) - k + 1)
        self.assertEqual(self.solution.medianSlidingWindow(nums, k), expected_output)

    def test_negative_numbers(self):
        nums = [-5, -3, -2, -1, 0]
        k = 3
        expected_output = [-2.0, -2.0, -1.0]
        self.assertEqual(self.solution.medianSlidingWindow(nums, k), expected_output)

    def test_mixed_numbers(self):
        nums = [5, -5, 3, 7, -3, 4]
        k = 3
        expected_output = [3.0, 2.0, 3.0, 4.0, 4.0]
        self.assertEqual(self.solution.medianSlidingWindow(nums, k), expected_output)

if __name__ == '__main__':
    unittest.main()
