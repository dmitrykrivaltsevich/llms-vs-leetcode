# Problem:
# You are given a string num which represents a positive integer, and an integer t.
# A number is called zero-free if none of its digits are 0.
# Return a string representing the smallest zero-free number greater than or equal to num such that the product of its digits is divisible by t. If no such number exists, return "-1".
# Example 1:
# Input: num = "1234", t = 256
# Output: "1488"
# Explanation:
# The smallest zero-free number that is greater than 1234 and has the product of its digits divisible by 256 is 1488, with the product of its digits equal to 256.
# Example 2:
# Input: num = "12355", t = 50
# Output: "12355"
# Explanation:
# 12355 is already zero-free and has the product of its digits divisible by 50, with the product of its digits equal to 150.
# Example 3:
# Input: num = "11111", t = 26
# Output: "-1"
# Explanation:
# No number greater than 11111 has the product of its digits divisible by 26.
# Constraints:
# 2 <= num.length <= 2 * 105
# num consists only of digits in the range ['0', '9'].
# num does not contain leading zeros.
# 1 <= t <= 10^14
# Hint:
# To optimize the solution using the factors of t, we can:                                                                   
#  1 Generate all prime factors of t.                                                                                        
#  2 Use these prime factors to construct the smallest number greater than or equal to num that is divisible by t. 
# Make edits below this line only. Good code contains docstrings, comments, and correct indentation.

from math import gcd
from functools import reduce

class Solution:
    def smallestNumber(self, num: str, t: int) -> str:

        def prime_factors(n):
            """Return the prime factors of n."""
            i = 2
            factors = []
            while i * i <= n:
                if n % i:
                    i += 1
                else:
                    n //= i
                    factors.append(i)
            if n > 1:
                factors.append(n)
            return factors

        def product_of_digits(s):
            """Return the product of digits in string s."""
            return reduce(lambda x, y: x * int(y), s, 1)

        def is_zero_free(s):
            """Check if the string s contains any zeroes."""
            return '0' not in s

        def next_number(s):
            """Generate the next number greater than the given number s."""
            num = int(s)
            while True:
                num += 1
                yield str(num)

        # Generate prime factors of t
        factors = prime_factors(t)

        # Convert num to integer for easier manipulation
        current_num = int(num)

        # Iterate over possible numbers greater than or equal to num
        for candidate in next_number(num):
            if is_zero_free(candidate) and all(factor in prime_factors(product_of_digits(candidate)) for factor in factors):
                return candidate

        return "-1"
