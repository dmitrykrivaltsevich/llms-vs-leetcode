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

    def add_factors(self, factors1: dict, factors2: dict):
        """Adds the counts of factors from two dictionaries."""
        result = factors1.copy()
        for p, count in factors2.items():
            result[p] = result.get(p, 0) + count
        return result

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
        best_digit_list_sorted = None # Optimization: Store the sorted version of best_digit_list

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

                # Compare this solution (current_list) with the best found so far
                # Prioritize minimum length, then lexicographically smallest *sorted* list

                if best_digit_list is None:
                    # First valid solution found
                    best_digit_list = current_list
                    best_digit_list_sorted = sorted(best_digit_list) # Store sorted version
                else:
                    # Compare lengths first
                    if len(current_list) < len(best_digit_list):
                        # Shorter solution is always better
                        best_digit_list = current_list
                        best_digit_list_sorted = sorted(best_digit_list) # Store sorted version
                    elif len(current_list) == len(best_digit_list):
                        # If lengths are equal, compare lexicographically using sorted lists
                        current_list_sorted = sorted(current_list) # Sort current list once
                        # Compare against the stored sorted version of the best list
                        if current_list_sorted < best_digit_list_sorted:
                            best_digit_list = current_list # Update best solution
                            best_digit_list_sorted = current_list_sorted # Update stored sorted version

        # Memoize and return the best list found (represents the combination of digits, not necessarily sorted)
        memo[factors_tuple] = best_digit_list
        return best_digit_list

    def get_min_suffix_parts(self, needed_factors: dict, length: int, memo_minimal_digits: dict):
        """
        Finds the minimal factor digits and padding '1's count for a suffix.
        Returns (min_digits_list, num_ones) or None if impossible or length constraint violated.
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

        # Return the parts needed to construct the smallest suffix later
        return (min_digits_list, num_ones)


    def smallestNumber(self, num: str, t: int) -> str:
        """
        Finds the smallest zero-free number >= num with digit product divisible by t.
        """
        n = len(num)

        # --- Handle t=1: Smallest zero-free number >= num ---
        if t == 1:
            if '0' not in num:
                return num # num is already zero-free

            # num contains '0', find the smallest zero-free number > num
            num_list = list(num)
            n = len(num_list)

            # Find the index of the leftmost '0'
            first_zero_idx = -1
            for k in range(n):
                if num_list[k] == '0':
                    first_zero_idx = k
                    break
            # first_zero_idx will be found because we checked '0' in num

            # Find the rightmost index j < first_zero_idx such that num[j] != '9'
            j = first_zero_idx - 1
            while j >= 0 and num_list[j] == '9':
                j -= 1

            # If all digits before the first '0' are '9' (or first_zero_idx is 0)
            if j < 0:
                return '1' * (n + 1)
            else:
                # Increment the digit at index j
                num_list[j] = str(int(num_list[j]) + 1)
                # Set all digits after j to '1'
                for k in range(j + 1, n):
                    num_list[k] = '1'
                return "".join(num_list)

        # --- Handle t > 1 ---
        target_factors = self.get_prime_factors(t)
        # If t requires prime factors > 7, no solution exists
        if target_factors is None:
            return "-1"

        memo_minimal_digits = {} # Memoization cache for get_minimal_factor_digits

        # --- Candidate 1: Check if num itself is valid ---
        candidate_num = None
        if '0' not in num:
            num_factors = self.get_factors_from_digits(num)
            if not self.subtract_factors(target_factors, num_factors): # True if needed is empty
                candidate_num = num

        # --- Candidate 2: Find the smallest number > num of length n ---
        candidate_n_greater = None
        current_prefix_factors = {2: 0, 3: 0, 5: 0, 7: 0} # Factors accumulated by num[:i]
        for i in range(n):
            original_digit = int(num[i])
            prefix_so_far = num[:i]

            # Try digits `d` greater than the original digit at position `i`
            for d in range(max(1, original_digit + 1), 10):
                factors_after_prefix_plus_d = self.add_factors(current_prefix_factors, self.DIGIT_FACTORS[d])
                needed_suffix_factors = self.subtract_factors(target_factors, factors_after_prefix_plus_d)
                remaining_len = n - 1 - i
                suffix_parts = self.get_min_suffix_parts(needed_suffix_factors, remaining_len, memo_minimal_digits)

                if suffix_parts is not None:
                    min_digits_list, num_ones = suffix_parts
                    suffix_str = '1' * num_ones + "".join(map(str, sorted(min_digits_list)))
                    # This is the smallest possible number > num of length n
                    candidate_n_greater = prefix_so_far + str(d) + suffix_str
                    goto end_n_loop # Break both loops

            # If we continue, we must use the original digit num[i] for this prefix
            if original_digit == 0:
                # Cannot use '0' and continue matching num's prefix.
                # Any valid solution must have been found above by changing a digit.
                break # Stop checking prefixes matching num

            # Add factors for the original digit and continue to next position i
            current_prefix_factors = self.add_factors(current_prefix_factors, self.DIGIT_FACTORS[original_digit])

        end_n_loop: # Label to break out of nested loops

        # --- Candidate 3: Find the smallest number of length n+1 or longer ---
        candidate_longer = None
        # Clear memo cache for a clean calculation based only on target_factors
        memo_minimal_digits.clear()
        min_factor_digits_list = self.get_minimal_factor_digits(target_factors, memo_minimal_digits)

        if min_factor_digits_list is not None:
            # Sort the minimal digits to form the smallest number base
            min_factor_digits_sorted_str = "".join(map(str, sorted(min_factor_digits_list)))
            # Determine the required length (at least n+1, at least len of digits)
            required_len = max(n + 1, len(min_factor_digits_sorted_str))
            # Calculate padding '1's
            num_ones = required_len - len(min_factor_digits_sorted_str)
            # Construct the smallest number of this required length
            candidate_longer = '1' * num_ones + min_factor_digits_sorted_str

        # --- Compare Candidates ---
        valid_candidates = []
        if candidate_num is not None:
            valid_candidates.append(candidate_num)
        if candidate_n_greater is not None:
            valid_candidates.append(candidate_n_greater)
        if candidate_longer is not None:
            valid_candidates.append(candidate_longer)

        if not valid_candidates:
            return "-1"
        else:
            # Return the lexicographically smallest among the valid candidates
            # Note: Python's min() on strings works lexicographically
            return min(valid_candidates)

# Helper to jump out of nested loops (requires Python 3.10+ or alternative)
# Since we can't use goto easily, restructure the loop slightly:
# Replace `goto end_n_loop` with `break` and add a flag

    def smallestNumber(self, num: str, t: int) -> str:
        """
        Finds the smallest zero-free number >= num with digit product divisible by t.
        """
        n = len(num)

        # --- Handle t=1: Smallest zero-free number >= num ---
        if t == 1:
            if '0' not in num:
                return num # num is already zero-free

            # num contains '0', find the smallest zero-free number > num
            num_list = list(num)
            n = len(num_list) # Re-get n if needed

            # Find the index of the leftmost '0'
            first_zero_idx = -1
            for k in range(n):
                if num_list[k] == '0':
                    first_zero_idx = k
                    break
            # first_zero_idx will be found because we checked '0' in num

            # Find the rightmost index j < first_zero_idx such that num[j] != '9'
            j = first_zero_idx - 1
            while j >= 0 and num_list[j] == '9':
                j -= 1

            # If all digits before the first '0' are '9' (or first_zero_idx is 0)
            if j < 0:
                return '1' * (n + 1)
            else:
                # Increment the digit at index j
                num_list[j] = str(int(num_list[j]) + 1)
                # Set all digits after j to '1'
                for k in range(j + 1, n):
                    num_list[k] = '1'
                return "".join(num_list)

        # --- Handle t > 1 ---
        target_factors = self.get_prime_factors(t)
        if target_factors is None:
            return "-1"

        memo_minimal_digits = {} # Memoization cache

        # --- Candidate 1: Check if num itself is valid ---
        candidate_num = None
        if '0' not in num:
            num_factors = self.get_factors_from_digits(num)
            if not self.subtract_factors(target_factors, num_factors):
                candidate_num = num

        # --- Candidate 2: Find the smallest number > num of length n ---
        candidate_n_greater = None
        current_prefix_factors = {2: 0, 3: 0, 5: 0, 7: 0}
        found_n_greater = False # Flag to break outer loop
        for i in range(n):
            original_digit = int(num[i])
            prefix_so_far = num[:i]

            for d in range(max(1, original_digit + 1), 10):
                factors_after_prefix_plus_d = self.add_factors(current_prefix_factors, self.DIGIT_FACTORS[d])
                needed_suffix_factors = self.subtract_factors(target_factors, factors_after_prefix_plus_d)
                remaining_len = n - 1 - i
                suffix_parts = self.get_min_suffix_parts(needed_suffix_factors, remaining_len, memo_minimal_digits)

                if suffix_parts is not None:
                    min_digits_list, num_ones = suffix_parts
                    suffix_str = '1' * num_ones + "".join(map(str, sorted(min_digits_list)))
                    candidate_n_greater = prefix_so_far + str(d) + suffix_str
                    found_n_greater = True # Set flag
                    break # Break inner d loop

            if found_n_greater:
                break # Break outer i loop

            # If we continue, process the original digit
            if original_digit == 0:
                break # Cannot use '0' and continue matching num's prefix

            current_prefix_factors = self.add_factors(current_prefix_factors, self.DIGIT_FACTORS[original_digit])

        # --- Candidate 3: Find the smallest number of length n+1 or longer ---
        candidate_longer = None
        memo_minimal_digits.clear() # Use a fresh cache
        min_factor_digits_list = self.get_minimal_factor_digits(target_factors, memo_minimal_digits)

        if min_factor_digits_list is not None:
            min_factor_digits_sorted_str = "".join(map(str, sorted(min_factor_digits_list)))
            required_len = max(n + 1, len(min_factor_digits_sorted_str))
            num_ones = required_len - len(min_factor_digits_sorted_str)
            candidate_longer = '1' * num_ones + min_factor_digits_sorted_str

        # --- Compare Candidates ---
        valid_candidates = []
        if candidate_num is not None:
            valid_candidates.append(candidate_num)
        if candidate_n_greater is not None:
            valid_candidates.append(candidate_n_greater)
        if candidate_longer is not None:
            valid_candidates.append(candidate_longer)

        if not valid_candidates:
            return "-1"
        else:
            # Return the lexicographically smallest among the valid candidates
            return min(valid_candidates)
