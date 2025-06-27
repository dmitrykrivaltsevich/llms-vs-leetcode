import math
import sys
from collections import Counter, deque
from functools import lru_cache

class Solution:
    def get_prime_factorization(self, n):
        factors = Counter()
        d = 2
        temp_n = n
        while d * d <= temp_n:
            if temp_n % d == 0:
                while temp_n % d == 0:
                    factors[d] += 1
                    temp_n //= d
            d += 1
        if temp_n > 1:
            factors[temp_n] += 1
        return factors

    def smallestNumber(self, num: str, t: int) -> str:
        if t == 1:
            if '0' in num:
                return '1' * (len(num) + 1)
            return num

        t_factors = self.get_prime_factorization(t)
        if any(p not in {2, 3, 5, 7} for p in t_factors):
            return "-1"

        p_factors_map = {
            d: self.get_prime_factorization(d) for d in range(1, 10)
        }

        p2, p3, p5, p7 = t_factors.get(2, 0), t_factors.get(3, 0), t_factors.get(5, 0), t_factors.get(7, 0)
        
        max_len = 60
        min_len_dp = {}
        queue = deque([(0, 0, 0, 0, 0)])
        min_len_dp[(0, 0, 0, 0)] = 0

        while queue:
            length, c2, c3, c5, c7 = queue.popleft()
            if length + 1 > max_len:
                continue
            for d in range(2, 10):
                d_factors = p_factors_map[d]
                n2, n3, n5, n7 = (min(p2, c2 + d_factors[2]),
                                  min(p3, c3 + d_factors[3]),
                                  min(p5, c5 + d_factors[5]),
                                  min(p7, c7 + d_factors[7]))
                if (n2, n3, n5, n7) not in min_len_dp:
                    min_len_dp[(n2, n3, n5, n7)] = length + 1
                    queue.append((length + 1, n2, n3, n5, n7))

        @lru_cache(None)
        def get_smallest_suffix(length, f2, f3, f5, f7):
            if f2 <= 0 and f3 <= 0 and f5 <= 0 and f7 <= 0:
                return '1' * length
            if length == 0:
                return None

            for d in range(1, 10):
                d_factors = p_factors_map[d]
                nf2, nf3, nf5, nf7 = max(0, f2 - d_factors[2]), max(0, f3 - d_factors[3]), max(0, f5 - d_factors[5]), max(0, f7 - d_factors[7])
                
                needed_len = min_len_dp.get((nf2, nf3, nf5, nf7), float('inf'))

                if needed_len <= length - 1:
                    suffix = get_smallest_suffix(length - 1, nf2, nf3, nf5, nf7)
                    if suffix is not None:
                        return str(d) + suffix
            return None

        n = len(num)
        if '0' not in num:
            num_factors = Counter()
            for digit_char in num:
                num_factors.update(p_factors_map[int(digit_char)])
            if all(num_factors[p] >= count for p, count in t_factors.items()):
                return num

        for i in range(n, -1, -1):
            prefix = num[:i]
            
            start_digit = 1
            if i < n:
                start_digit = int(num[i]) + 1

            for d_val in range(start_digit, 10):
                d = str(d_val)
                new_prefix = prefix + d
                
                prefix_factors = Counter()
                for digit_char in new_prefix:
                    digit = int(digit_char)
                    if digit > 0:
                        prefix_factors.update(p_factors_map[digit])

                rem_f2 = max(0, p2 - prefix_factors.get(2, 0))
                rem_f3 = max(0, p3 - prefix_factors.get(3, 0))
                rem_f5 = max(0, p5 - prefix_factors.get(5, 0))
                rem_f7 = max(0, p7 - prefix_factors.get(7, 0))

                rem_len = n - len(new_prefix)
                needed_len = min_len_dp.get((rem_f2, rem_f3, rem_f5, rem_f7), float('inf'))
                
                if needed_len <= rem_len:
                    suffix = get_smallest_suffix(rem_len, rem_f2, rem_f3, rem_f5, rem_f7)
                    if suffix is not None:
                        return new_prefix + suffix
        
        for length in range(n + 1, max_len + 2):
            res = get_smallest_suffix(length, p2, p3, p5, p7)
            if res is not None:
                return res
                
        return "-1"
