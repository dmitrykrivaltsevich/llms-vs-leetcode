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

from math import prod

# 2 <= num.length <= 2 * 105
# num consists only of digits in the range ['0', '9'].
# num does not contain leading zeros.
# 1 <= t <= 10^14
# Make edits below this line only. First write docstring, then implementation.

class Solution:
    def smallestNumber(self, num: str, t: int) -> str:
        """
        Find the smallest zero-free number greater than or equal to a given number such that
        the product of its digits is divisible by `t`.

        Args:
            num (str): The input number as a string.
            t (int): The target divisor.

        Returns:
            str: The smallest zero-free number with the required properties, or "-1" if no such number exists.
        """
        # Helper function to calculate the product of digits in a number
        def digit_product(n):
            return prod(int(digit) for digit in n if digit != '0')

        # Helper function to generate the next possible number with zero-free digits
        def next_zero_free_number(num):
            num_list = list(map(int, num))
            n = len(num_list)

            for i in range(n - 1, -1, -1):
                if num_list[i] != 9:
                    num_list[i] += 1
                    break
                else:
                    num_list[i] = 1

            return ''.join(map(str, num_list))

        # Helper function to calculate the product of digits in a number
        def digit_product(n):
            return prod(int(digit) for digit in n if digit != '0')

        from itertools import permutations

        def has_large_factor(t):
            """Check if t has any factor greater than 9."""
            for i in range(2, int(t**0.5) + 1):
                if t % i == 0:
                    if i > 9 or t // i > 9:
                        return True
            return False

        def generate_factors(t):
            """Generate all factors of t that are less than or equal to 9."""
            factors = set()
            for i in range(1, int(t**0.5) + 1):
                if t % i == 0:
                    if i <= 9:
                        factors.add(i)
                    if t // i <= 9 and t // i != i:
                        factors.add(t // i)
            return sorted(factors)

        def smallest_number_with_factors(num, factors):
            """Find the smallest number greater than or equal to num that contains all factors."""
            num = int(num)
            for perm in permutations(factors):
                candidate = ''.join(map(str, perm))
                if int(candidate) >= num:
                    return candidate
            return "-1"

        # Check if t has any factor greater than 9
            if has_large_factor(t):
                return "-1"

        # Generate all factors of t that are less than or equal to 9
        factors = generate_factors(t)
        # Find the smallest number greater than or equal to num that contains all factors
        return smallest_number_with_factors(num, factors)
        # Remove unused helper functions
