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

class TimeoutTestLoader(unittest.TestLoader):
    def loadTestsFromNames(self, names, module=None):
        suite = super().loadTestsFromNames(names, module)
        for test in suite:
            if isinstance(test, unittest.FunctionTestCase):
                timeout = getattr(test._testMethodDoc, 'timeout', 1)
                setattr(test, '_timeout', timeout)
        return suite

class TimeoutTestSuite(unittest.TestSuite):
    def run(self, result, debug=False):
        for test in self:
            if isinstance(test, unittest.FunctionTestCase):
                timeout = getattr(test, '_timeout', 1)
                runner = TimeoutTestRunner(timeout=timeout)
                result = runner.run(test)
        return result

if __name__ == '__main__':
    loader = TimeoutTestLoader()
    suite = loader.loadTestsFromNames(['test_0480_sliding_window_median.py'])
    runner = unittest.TextTestRunner()
    runner.run(TimeoutTestSuite(suite))
