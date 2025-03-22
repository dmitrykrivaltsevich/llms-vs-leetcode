import unittest
from _0480_sliding_window_median import Solution
import threading

def timeout(seconds):
    def decorator(func):
        def wrapper(*args, **kwargs):
            timeout_event = threading.Event()

            def signal_handler():
                timeout_event.set()

            timer = threading.Timer(seconds, signal_handler)
            timer.start()

            try:
                result = func(*args, **kwargs)
            finally:
                timer.cancel()
                if timeout_event.is_set():
                    raise TimeoutError(f"Test timed out after {seconds} seconds")
            return result
        return wrapper
    return decorator

class TestSlidingWindowMedian(unittest.TestCase):

    def setUp(self):
        self.solution = Solution()

    @timeout(1)
    def test_example_1(self):
        nums = [1, 3, -1, -3, 5, 3, 6, 7]
        k = 3
        expected_output = [1.0, -1.0, -1.0, 3.0, 5.0, 6.0]
        self.assertEqual(self.solution.medianSlidingWindow(nums, k), expected_output)

    @timeout(1)
    def test_example_2(self):
        nums = [1, 2, 3, 4, 2, 3, 1, 4, 2]
        k = 3
        expected_output = [2.0, 3.0, 3.0, 3.0, 2.0, 3.0, 2.0]
        self.assertEqual(self.solution.medianSlidingWindow(nums, k), expected_output)

    @timeout(1)
    def test_empty_array(self):
        nums = []
        k = 3
        expected_output = []
        self.assertEqual(self.solution.medianSlidingWindow(nums, k), expected_output)

    @timeout(1)
    def test_k_zero(self):
        nums = [1, 2, 3]
        k = 0
        expected_output = []
        self.assertEqual(self.solution.medianSlidingWindow(nums, k), expected_output)

    @timeout(1)
    def test_single_element_window(self):
        nums = [1, 2, 3, 4, 5]
        k = 1
        expected_output = [1.0, 2.0, 3.0, 4.0, 5.0]
        self.assertEqual(self.solution.medianSlidingWindow(nums, k), expected_output)

    @timeout(5)
    def test_large_array(self):
        nums = list(range(100000))
        k = 50000
        expected_output = [49999.5] * (len(nums) - k + 1)
        self.assertEqual(self.solution.medianSlidingWindow(nums, k), expected_output)

    @timeout(1)
    def test_negative_numbers(self):
        nums = [-5, -3, -2, -1, 0]
        k = 3
        expected_output = [-2.0, -2.0, -1.0]
        self.assertEqual(self.solution.medianSlidingWindow(nums, k), expected_output)

    @timeout(1)
    def test_mixed_numbers(self):
        nums = [5, -5, 3, 7, -3, 4]
        k = 3
        expected_output = [3.0, 2.0, 3.0, 4.0, 4.0]
        self.assertEqual(self.solution.medianSlidingWindow(nums, k), expected_output)

if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestSlidingWindowMedian)
    runner = unittest.TextTestRunner()
    runner.run(suite)
