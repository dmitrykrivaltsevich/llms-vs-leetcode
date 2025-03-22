import unittest
import threading

class TimeoutTestRunner(unittest.TextTestRunner):
    def __init__(self, timeout=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timeout = timeout

    def run(self, test):
        result = self._makeResult()
        start_time = threading.Event()

        def runner():
            start_time.set()
            test(result)

        thread = threading.Thread(target=runner)
        thread.start()
        thread.join(self.timeout)

        if thread.is_alive():
            print(f"Test timed out after {self.timeout} seconds")
            result.addError(test, TimeoutError("Test timed out"))
            thread.join()

        return result

if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromNames(['test_0480_sliding_window_median.py'])
    runner = TimeoutTestRunner(timeout=1)
    runner.run(suite)
