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
#
# Example:
# Input num = "4093", t = 180
# Wrong answer: "4095"
# Expected output: "4159"
#
# Constraints:
# 2 <= num.length <= 2 * 10^5 (important! many test cases use lenghty numbers, make sure solution is fast)
# num consists only of digits in the range ['0', '9'].
# num does not contain leading zeros.
# 1 <= t <= 10^14
#
import math
from functools import cache

class Solution:

    def smallestNumber(self, num: str, t: int) -> str:

        _gcd = math.gcd

        # --- Handle t = 1 separately ---
        # Find the smallest zero-free number >= num
        if t == 1:
            n = len(num)
            digits = [int(d) for d in num]
            
            has_zero = False
            first_zero_idx = -1
            for i in range(n):
                if digits[i] == 0:
                    has_zero = True
                    # Find the leftmost zero index
                    if first_zero_idx == -1:
                       first_zero_idx = i
                    # Optimization: if we find a zero, we know num itself is not the answer
                    # unless we modify it. We only need the leftmost zero for the logic below.
                    # break # Removed break to correctly find the leftmost zero

            if not has_zero:
                # If num has no zeros, it's the smallest zero-free number >= itself.
                return num

            # Find the rightmost digit < 9 strictly before the leftmost zero
            j = -1
            # Iterate backwards from the position *before* the leftmost zero
            for i in range(first_zero_idx - 1, -1, -1): 
                 if digits[i] < 9:
                     j = i
                     break
            
            if j == -1: # All digits before the first zero were 9 (or no digits before zero)
                # The smallest zero-free number will have length n+1 and be all '1's
                return '1' * (n + 1)
            else:
                # Increment the digit at index j
                digits[j] += 1
                # Set all subsequent digits (from j+1 to end) to '1'
                for i in range(j + 1, n):
                    digits[i] = 1
                return "".join(map(str, digits))

        # --- Handle t > 1 ---

        # Helper: Check if t's prime factors are only within {2, 3, 5, 7}
        def check_prime_factors(target: int) -> bool:
            temp_t = target
            # Only need to check divisibility by primes up to 7
            for p in [2, 3, 5, 7]:
                # Repeatedly divide by p until it's no longer a factor
                while temp_t > 0 and temp_t % p == 0: 
                    temp_t //= p
            # If temp_t is 1, all prime factors were successfully removed
            return temp_t == 1

        if not check_prime_factors(t):
            # If t has prime factors other than 2, 3, 5, 7, no product of digits 1-9 can divide it.
            return "-1"

        # Helper: Check if the product of digits of a zero-free string s divides target
        def check_product(s: str, target: int) -> bool:
            # Assumes s is zero-free (checked before calling)
            current_g = 1
            for digit in s:
                d = int(digit)
                # Incrementally compute gcd(product_so_far, target)
                current_g = _gcd(current_g * d, target)
                # Optimization: if gcd reaches target early, product is divisible
                if current_g == target:
                    return True
            # Final check after all digits
            return current_g == target

        # Check if the original number `num` is a valid solution
        # It must be zero-free and its digit product must divide t
        if '0' not in num and check_product(num, t):
             return num

        n = len(num)

        # --- DFS to find the smallest number >= num of length n ---
        # State: (index, current_gcd_with_t, is_tight_constraint_from_num)
        # Returns: smallest valid suffix string starting from index, or None
        @cache
        def dfs(index, current_g, is_tight):
            # Base case: Product requirement met
            if current_g == t:
                # Fill the rest with '1's to minimize the number
                return '1' * (n - index)
            
            # Base case: Reached the end of the number length without meeting criteria
            if index == n:
                return None

            res = None
            # Determine the starting digit for the current position
            # If 'is_tight' is true, we must pick a digit >= num[index]
            # Otherwise, we can start from 1 (since we already exceeded num's prefix)
            lower_bound = int(num[index]) if is_tight else 1

            # Iterate through possible digits (1-9)
            for d in range(lower_bound, 10):
                # Skip 0 as we need zero-free numbers
                if d == 0: continue 

                # Calculate the gcd of the new product-so-far with t
                next_g = _gcd(current_g * d, t)
                
                # Determine if the next recursive call is still tightly bound
                # It's tight if we were tight AND we chose the lower_bound digit
                next_tight = is_tight and (d == lower_bound)
                
                # Recursively find the suffix
                suffix = dfs(index + 1, next_g, next_tight)

                # If a valid suffix was found
                if suffix is not None:
                    # Construct the result for this path
                    res = str(d) + suffix
                    # Since we iterate digits d in increasing order, 
                    # the first valid result found is the smallest.
                    break 
            return res

        # --- DFS to find the smallest number of length n+1 ---
        # State: (index, current_gcd_with_t)
        # Returns: smallest valid suffix string starting from index, or None
        m = n + 1 # Target length
        @cache
        def dfs_longer(index, current_g):
            # Base case: Product requirement met
            if current_g == t:
                # Fill the rest with '1's to minimize
                return '1' * (m - index)
            
            # Base case: Reached the end of the target length
            if index == m:
                return None

            res = None
            # Iterate through digits 1-9
            for d in range(1, 10): 
                # Calculate the next gcd
                next_g = _gcd(current_g * d, t)
                
                # Recursively find the suffix
                suffix = dfs_longer(index + 1, next_g)
                
                # If a valid suffix was found
                if suffix is not None:
                    # Construct the result and break (first found is smallest)
                    res = str(d) + suffix
                    break 
            return res

        # --- Main Logic Execution for t > 1 ---
        
        # Clear caches before starting searches (good practice)
        dfs.cache_clear()
        dfs_longer.cache_clear()

        # 1. Try finding the smallest valid number >= num with length n
        solution_n = dfs(0, 1, True) # Start DFS for length n
        if solution_n is not None:
            return solution_n # Found the smallest solution

        # 2. If no solution of length n exists, find the smallest of length n+1
        solution_n_plus_1 = dfs_longer(0, 1) # Start DFS for length n+1
        
        # Return the length n+1 solution if found, otherwise return "-1"
        return solution_n_plus_1 if solution_n_plus_1 is not None else "-1"
