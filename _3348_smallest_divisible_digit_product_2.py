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
# from functools import cache # Using dictionary memoization instead
from collections import Counter

class Solution:

    def get_prime_factorization(self, n):
        """Computes the prime factorization of n."""
        factors = Counter()
        d = 2
        temp_n = n
        # Optimization: only check factors up to sqrt(n)
        while d * d <= temp_n:
            while temp_n % d == 0:
                factors[d] += 1
                temp_n //= d
            # Optimization: check 2 then only odd numbers
            d = d + 1 if d == 2 else d + 2
        if temp_n > 1:
            factors[temp_n] += 1
        return factors

    def smallestNumber(self, num: str, t: int) -> str:
        _gcd = math.gcd # Local alias for performance

        # --- Handle t = 1 separately ---
        if t == 1:
            n = len(num)
            digits = [int(d) for d in num]
            has_zero = False
            first_zero_idx = -1
            for i in range(n):
                if digits[i] == 0:
                    has_zero = True
                    if first_zero_idx == -1:
                       first_zero_idx = i
            if not has_zero: return num # num is already zero-free

            # Find the rightmost digit < 9 strictly before the leftmost zero
            j = -1
            for i in range(first_zero_idx - 1, -1, -1):
                 if digits[i] < 9:
                     j = i
                     break

            if j == -1: # All digits before the first zero were 9 (or no digits before zero)
                return '1' * (n + 1)
            else:
                # Increment the digit at index j
                digits[j] += 1
                # Set all subsequent digits (from j+1 to end) to '1'
                for i in range(j + 1, n): digits[i] = 1
                return "".join(map(str, digits))

        # --- Handle t > 1 ---

        # Check if t has prime factors other than {2, 3, 5, 7}
        t_factors = self.get_prime_factorization(t)
        allowed_primes = {2, 3, 5, 7}
        for p in t_factors:
            if p not in allowed_primes:
                 return "-1" # t has disallowed prime factors

        # Precompute factorizations for digits 1-9
        digit_factors = {d: self.get_prime_factorization(d) for d in range(1, 10)}

        # Check if the original number `num` is a valid solution
        if '0' not in num:
            current_g = 1
            for digit in num:
                current_g = _gcd(current_g * int(digit), t)
            if current_g == t:
                 return num

        n = len(num)
        # Use a tuple of sorted items for canonical representation of target factors
        target_factors_tuple = tuple(sorted(t_factors.items()))

        # Memoization dictionaries
        memo = {}
        memo_longer = {}

        # --- Helper: Pruning Check ---
        def check_pruning(remaining_len, current_factors_cnt):
            """Checks if it's possible to achieve target factors with remaining digits."""
            if remaining_len < 0: return True # Should not happen

            # Calculate needed factors
            needed_factors = Counter()
            possible = True
            for p, target_count in t_factors.items():
                 needed = target_count - current_factors_cnt[p]
                 if needed <= 0: continue

                 # Max power of p achievable with remaining_len digits
                 max_power = 0
                 if p == 2: max_power = 3 * remaining_len # From digit 8
                 elif p == 3: max_power = 2 * remaining_len # From digit 9
                 elif p == 5: max_power = 1 * remaining_len # From digit 5
                 elif p == 7: max_power = 1 * remaining_len # From digit 7
                 # No other primes possible in t_factors at this point

                 if needed > max_power:
                     possible = False
                     break
            return not possible # Return True if pruning should occur

        # --- Helper: Canonical Factor Tuple ---
        def factors_to_tuple(factors_cnt):
             """Creates a canonical tuple representation for memoization key."""
             # Only include primes relevant to t
             items = []
             for p, target_count in t_factors.items():
                 # Store the current count for prime p, capped at target_count
                 current_count = min(factors_cnt[p], target_count)
                 if current_count > 0: # Only store non-zero counts
                     items.append((p, current_count))
             return tuple(sorted(items))

        # --- DFS for length n ---
        def dfs(index, current_factors_tuple, is_tight):
            state = (index, current_factors_tuple, is_tight)
            if state in memo:
                return memo[state]

            current_factors_cnt = Counter(dict(current_factors_tuple))

            # Base case: Check if target factors are met (using tuple comparison)
            if current_factors_tuple == target_factors_tuple:
                return '1' * (n - index) # Fill rest with 1s

            # Base case: Reached end without meeting target
            if index == n:
                return None

            # Pruning check
            if check_pruning(n - index, current_factors_cnt):
                 memo[state] = None
                 return None

            res = None
            lower_bound = int(num[index]) if is_tight else 1

            for d in range(lower_bound, 10):
                if d == 0: continue # Skip zero

                # Calculate next factors state
                next_factors_cnt = current_factors_cnt.copy()
                for p, count in digit_factors[d].items():
                    if p in t_factors: # Only consider primes relevant to t
                         # Accumulate count, but cap at the target count for that prime
                         next_factors_cnt[p] = min(t_factors[p], current_factors_cnt[p] + count)

                next_factors_tuple = factors_to_tuple(next_factors_cnt)
                next_tight = is_tight and (d == lower_bound)

                suffix = dfs(index + 1, next_factors_tuple, next_tight)

                if suffix is not None:
                    res = str(d) + suffix
                    break # Found smallest for this branch

            memo[state] = res # Store result in memo
            return res

        # --- DFS for length n+1 ---
        m = n + 1
        def dfs_longer(index, current_factors_tuple):
            state = (index, current_factors_tuple)
            if state in memo_longer:
                return memo_longer[state]

            current_factors_cnt = Counter(dict(current_factors_tuple))

            if current_factors_tuple == target_factors_tuple:
                return '1' * (m - index)

            if index == m:
                return None

            if check_pruning(m - index, current_factors_cnt):
                 memo_longer[state] = None
                 return None

            res = None
            for d in range(1, 10): # Digits 1-9
                next_factors_cnt = current_factors_cnt.copy()
                for p, count in digit_factors[d].items():
                     if p in t_factors:
                          next_factors_cnt[p] = min(t_factors[p], current_factors_cnt[p] + count)

                next_factors_tuple = factors_to_tuple(next_factors_cnt)
                suffix = dfs_longer(index + 1, next_factors_tuple)

                if suffix is not None:
                    res = str(d) + suffix
                    break
            memo_longer[state] = res # Store result
            return res

        # --- Main Logic Execution for t > 1 ---
        initial_factors_tuple = tuple() # Represents gcd=1 state (empty factors)
        memo.clear() # Clear memoization table
        solution_n = dfs(0, initial_factors_tuple, True)

        if solution_n is not None:
            return solution_n

        memo_longer.clear() # Clear memoization table
        solution_n_plus_1 = dfs_longer(0, initial_factors_tuple)

        return solution_n_plus_1 if solution_n_plus_1 is not None else "-1"
