import unittest
from multiprocessing import Process, Queue
import time
from _3348_smallest_divisible_digit_product_2 import Solution

# This function runs in a separate process
def run_solution_in_process(q, num, t):
    try:
        s = Solution()
        result = s.smallestNumber(num, t)
        q.put(result)
    except Exception as e:
        # Put the exception in the queue to be analyzed by the main process
        q.put(e)

class TestSmallestNumber(unittest.TestCase):
    def test_case_1(self):
        s = Solution()
        self.assertEqual(s.smallestNumber("1234", 256), "1488")

    def test_case_2(self):
        s = Solution()
        self.assertEqual(s.smallestNumber("12355", 50), "12355")

    def test_case_3(self):
        s = Solution()
        self.assertEqual(s.smallestNumber("11111", 26), "-1")

    def test_failing_case(self):
        s = Solution()
        self.assertEqual(s.smallestNumber("12", 1968750), "255555579")

    def test_another_failing_case(self):
        s = Solution()
        self.assertEqual(s.smallestNumber("19", 2), "21")

    def test_zero_in_num(self):
        s = Solution()
        self.assertEqual(s.smallestNumber("302", 48), "328")

    def test_another_failing_case_2(self):
        s = Solution()
        self.assertEqual(s.smallestNumber("26", 9), "29")

    def test_new_case(self):
        s = Solution()
        self.assertEqual(s.smallestNumber("129709", 18), "129711")

    def test_performance_with_large_input(self):
        # This test is designed to FAIL with the current implementation.
        # The goal is to optimize the smallestNumber function so that this test PASSES.
        # It checks that the function can handle a very large input within a
        # reasonable time (10 seconds) without crashing.
        q = Queue()
        num = "1" * 50001 + "35782"
        t = 99883155456000

        p = Process(target=run_solution_in_process, args=(q, num, t))
        p.start()

        # Wait for 10 seconds for the process to complete
        p.join(10)

        if p.is_alive():
            p.terminate()
            p.join()
            self.fail("The function took too long to execute and was terminated.")

        # Check the result from the queue
        result = q.get()

        if isinstance(result, Exception):
            self.fail(f"The function raised an unhandled exception: {result}")

        # If the function completes successfully, this assertion should pass.
        # For now, we just check if it's a string, as we don't know the exact output.
        self.assertIsInstance(result, str, "The function should return a string.")
        self.assertNotEqual(result, "-1", "The function should find a valid result.")

    def test_user_case(self):
        s = Solution()
        self.assertEqual(s.smallestNumber("20091", 128), "21188")


if __name__ == '__main__':
    unittest.main()
