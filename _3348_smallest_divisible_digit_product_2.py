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
#  2 If any prime factor of t is greather than 9, return "-1"                                                                                      
#  3 Otherwise use these prime factors and "1" as digits to construct the smallest number greater than or equal to num that is divisible by t. 
import math
from collections import Counter
# Make edits below this line only. Good code contains docstrings, comments, and correct indentation.

class Solution:
    # Precompute prime factors for digits 1-9
    DIGIT_FACTORS = {
        1: {}, 2: {2: 1}, 3: {3: 1}, 4: {2: 2}, 5: {5: 1},
        6: {2: 1, 3: 1}, 7: {7: 1}, 8: {2: 3}, 9: {3: 2}
    }

    def get_prime_factors(self, t: int):
        """
        Calculates the prime factors (2, 3, 5, 7) and their counts for t.
        Returns None if t has any prime factor > 7.
        """
        if t == 1: return {}
        factors = {2: 0, 3: 0, 5: 0, 7: 0}
        d = 2
        temp_t = t
        # Trial division for primes up to sqrt(t)
        while d * d <= temp_t:
            while temp_t % d == 0:
                # Only track factors 2, 3, 5, 7
                if d > 7: return None # Found prime factor > 7
                if d in factors: factors[d] += 1
                temp_t //= d
            d += 1
        # Handle the remaining factor if it's > 1
        if temp_t > 1:
            if temp_t > 7: return None # Remaining prime factor > 7
            if temp_t in factors: factors[temp_t] += 1
        # Return only factors with count > 0
        return {p: c for p, c in factors.items() if c > 0}

    def get_factors_from_digits(self, digits_str: str):
        """Calculates the combined prime factors (2,3,5,7) from a string of digits."""
        total_factors = {2: 0, 3: 0, 5: 0, 7: 0}
        for digit_char in digits_str:
            digit = int(digit_char)
            # Assumes digits are 1-9 for factor calculation
            if digit >= 1:
                 digit_f = self.DIGIT_FACTORS[digit]
                 for p, c in digit_f.items():
                     total_factors[p] += c
        return total_factors

    def subtract_factors(self, target: dict, current: dict):
        """Calculates the remaining factors needed from target after accounting for current."""
        needed = {}
        for p, target_count in target.items():
            current_count = current.get(p, 0)
            if current_count < target_count:
                needed[p] = target_count - current_count
        return needed # Returns empty dict if all target factors are met or exceeded.

    def get_minimal_factor_digits(self, needed_factors: dict, memo: dict):
        """
        Recursively finds the minimum list of digits (2-9) whose product covers
        the needed_factors. Uses memoization. Minimizes count, then lexicographical value.
        Returns a list of integers, or None if impossible.
        """
        # Convert dict to sorted tuple for memoization key
        factors_tuple = tuple(sorted(needed_factors.items()))
        if not factors_tuple: return [] # Base case: no factors needed
        if factors_tuple in memo: return memo[factors_tuple]

        best_digit_list = None # Stores the best list found so far [d] + recursive_result

        # Try adding digit d (9 down to 2) to the solution
        for d in range(9, 1, -1):
            digit_f = self.DIGIT_FACTORS[d]
            temp_needed = dict(factors_tuple) # Current factors needed

            # Check if digit 'd' contributes towards satisfying any needed factor
            contributes = False
            for p, c_needed in temp_needed.items():
                if digit_f.get(p, 0) > 0:
                    contributes = True
                    break
            if not contributes: continue # Skip digit d if it doesn't help satisfy remaining factors

            # Calculate the factors remaining *after* using digit 'd'
            next_factors_dict = temp_needed.copy()
            for p, c_digit in digit_f.items():
                 if p in next_factors_dict:
                     # Reduce the needed count for prime p by the amount provided by digit d
                     next_factors_dict[p] = max(0, next_factors_dict[p] - c_digit)

            # Remove factors that are now fully satisfied (count is 0)
            next_factors_dict = {p: c for p, c in next_factors_dict.items() if c > 0}

            # Recursively find the minimal digits for the remaining factors
            res = self.get_minimal_factor_digits(next_factors_dict, memo)

            # If the recursive call found a solution for the remainder...
            if res is not None:
                current_list = [d] + res # Prepend the current digit 'd'

                # Compare this solution (current_list) with the best found so far (best_digit_list)
                # Prioritize minimum length, then lexicographically smallest *sorted* list
                current_list_sorted_str = "".join(map(str, sorted(current_list)))
                best_digit_list_sorted_str = ""
                if best_digit_list is not None:
                    best_digit_list_sorted_str = "".join(map(str, sorted(best_digit_list)))

                if best_digit_list is None or \
                   len(current_list) < len(best_digit_list) or \
                   (len(current_list) == len(best_digit_list) and current_list_sorted_str < best_digit_list_sorted_str):
                     best_digit_list = current_list # Update best solution

        # Memoize the result for this factor state and return it
        memo[factors_tuple] = best_digit_list
        return best_digit_list

    def get_min_suffix(self, needed_factors: dict, length: int, memo_minimal_digits: dict):
        """
        Constructs the smallest suffix string of a given length that satisfies
        needed_factors, using '1's and the minimal factor digits.
        """
        # Find the minimal set of digits (2-9) required for the factors
        min_digits_list = self.get_minimal_factor_digits(needed_factors, memo_minimal_digits)

        # If factors cannot be satisfied (shouldn't happen with valid t)
        if min_digits_list is None: return None

        # If the minimal required digits exceed the available suffix length
        if len(min_digits_list) > length:
            return None

        # Calculate how many '1's are needed for padding
        num_ones = length - len(min_digits_list)

        # Construct the suffix: '1's followed by the sorted minimal digits
        # Sorting ensures the smallest numerical value for the suffix
        suffix_list = [1] * num_ones + sorted(min_digits_list)
        return "".join(map(str, suffix_list))


    def smallestNumber(self, num: str, t: int) -> str:
        """
        Finds the smallest zero-free number >= num with digit product divisible by t.
        """
        n = len(num)

        # --- Handle t=1: Smallest zero-free number >= num ---
        if t == 1:
            if '0' not in num:
                return num # num is already zero-free and >= num

            num_list = list(num)
            # Find the first '0' from the left
            first_zero_idx = -1
            for k in range(n):
                if num_list[k] == '0':
                    first_zero_idx = k
                    break
            # This should always find a '0' based on the initial check

            # Find the rightmost non-'9' digit *before* the first '0'
            j = first_zero_idx - 1
            while j >= 0 and num_list[j] == '9':
                j -= 1

            if j < 0: # All '9's before the zero, or zero at index 0
                # The smallest zero-free number is '1' repeated n+1 times
                return '1' * (n + 1)
            else:
                # Increment the digit at index j
                num_list[j] = str(int(num_list[j]) + 1)
                # Set all digits *after* j to '1' (smallest non-zero digit)
                for k in range(j + 1, n):
                    num_list[k] = '1'
                return "".join(num_list)

        # --- Handle t > 1 ---
        target_factors = self.get_prime_factors(t)
        # If t requires prime factors > 7, no solution exists
        if target_factors is None:
            return "-1"

        min_found_num = None # Stores the best candidate found so far
        memo_minimal_digits = {} # Memoization cache for get_minimal_factor_digits

        # --- Try to find a solution of length n ---

        # Iterate through positions `i` from right-to-left (n-1 down to 0)
        # Try changing the digit at `num[i]` to something larger
        for i in range(n - 1, -1, -1):
            prefix = num[:i]
            original_digit = int(num[i])

            # Try digits `d` greater than the original digit at position `i`
            for d in range(original_digit + 1, 10): # d is 1-9
                current_prefix_digits = prefix + str(d)
                # This prefix is guaranteed zero-free up to this point if num was

                # Calculate factors provided by this new prefix
                prefix_factors = self.get_factors_from_digits(current_prefix_digits)
                # Calculate factors still needed for the suffix
                needed_factors = self.subtract_factors(target_factors, prefix_factors)
                # Calculate the length of the suffix needed
                remaining_len = n - len(current_prefix_digits)

                # Find the smallest possible suffix satisfying needs
                suffix = self.get_min_suffix(needed_factors, remaining_len, memo_minimal_digits)

                # If a valid suffix was found...
                if suffix is not None:
                    candidate = current_prefix_digits + suffix
                    # This candidate has length n, is > num, and satisfies factors.
                    # Since we iterate `i` downwards and `d` upwards, the first
                    # candidate found this way is the smallest possible number
                    # of length n that is strictly greater than num.
                    min_found_num = candidate
                    break # Break inner loop (d)
            if min_found_num is not None:
                 break # Break outer loop (i) - we found the smallest length-n number > num

        # --- Check if `num` itself is a valid solution ---
        num_satisfies = False
        if '0' not in num:
            num_factors = self.get_factors_from_digits(num)
            # Check if `num`'s factors cover the target factors
            if not self.subtract_factors(target_factors, num_factors): # True if needed is empty
                num_satisfies = True

        # Determine the result based on whether `num` satisfies and if a larger candidate was found
        if num_satisfies:
            # If num works and either no larger candidate was found, OR num is smaller than the larger candidate found
            if min_found_num is None or num < min_found_num:
                 return num # num is the smallest valid solution
            else:
                 return min_found_num # The larger candidate found was actually the smallest
        elif min_found_num is not None: # num doesn't satisfy, but a larger candidate of length n was found
             return min_found_num

        # --- If no solution of length n works, try length n+1 (or longer) ---
        memo_minimal_digits.clear() # Clear cache for the next independent call
        # Find the absolute minimal set of digits (2-9) for target_factors
        min_factor_digits_list = self.get_minimal_factor_digits(target_factors, memo_minimal_digits)

        # If factors can be satisfied (should always be true if target_factors was not None)
        if min_factor_digits_list is not None:
            min_factor_digits_str = "".join(map(str, sorted(min_factor_digits_list)))

            # Determine the length of the smallest number satisfying factors
            # It must be at least n+1 and at least the length of the minimal factor digits
            required_len = max(n + 1, len(min_factor_digits_str))

            # Calculate padding with '1's
            num_ones = required_len - len(min_factor_digits_str)

            # Construct the smallest number of required_len
            result_longer = '1' * num_ones + min_factor_digits_str
            return result_longer

        # If no solution is found at all
        return "-1"
