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
            return num

        t_factors = self.get_prime_factorization(t)
        if any(p not in {2, 3, 5, 7} for p in t_factors):
            return "-1"

        p_factors_map = {
            d: self.get_prime_factorization(d) for d in range(1, 10)
        }
        p_factors_map[0] = Counter()

        n = len(num)
        p2, p3, p5, p7 = t_factors.get(2, 0), t_factors.get(3, 0), t_factors.get(5, 0), t_factors.get(7, 0)

        min_len_dp = {}
        queue = deque([(0, (0, 0, 0, 0))])
        min_len_dp[(0, 0, 0, 0)] = 0

        q_for_min_len = deque([(0, 0, 0, 0, 0)])
        min_len_dp_no_zero = {(0,0,0,0): 0}

        while q_for_min_len:
            length, c2, c3, c5, c7 = q_for_min_len.popleft()
            if length + 1 > n + 25:
                continue
            for d in range(2, 10):
                d_factors = p_factors_map[d]
                n2 = min(p2, c2 + d_factors.get(2, 0))
                n3 = min(p3, c3 + d_factors.get(3, 0))
                n5 = min(p5, c5 + d_factors.get(5, 0))
                n7 = min(p7, c7 + d_factors.get(7, 0))
                state = (n2, n3, n5, n7)
                if state not in min_len_dp_no_zero:
                    min_len_dp_no_zero[state] = length + 1
                    q_for_min_len.append((length + 1, n2, n3, n5, n7))

        @lru_cache(None)
        def get_smallest_suffix(f2, f3, f5, f7):
            state = (f2, f3, f5, f7)
            if state not in min_len_dp_no_zero:
                return None
            length = min_len_dp_no_zero[state]
            res = []
            curr_f = state
            current_len = length
            while len(res) < length:
                found = False
                for d in range(1, 10):
                    d_factors = p_factors_map[d]
                    prev_f2 = max(0, curr_f[0] - d_factors.get(2, 0))
                    prev_f3 = max(0, curr_f[1] - d_factors.get(3, 0))
                    prev_f5 = max(0, curr_f[2] - d_factors.get(5, 0))
                    prev_f7 = max(0, curr_f[3] - d_factors.get(7, 0))
                    prev_state = (prev_f2, prev_f3, prev_f5, prev_f7)
                    if min_len_dp_no_zero.get(prev_state, float('inf')) == current_len - 1:
                        res.append(str(d))
                        curr_f = prev_state
                        current_len -= 1
                        found = True
                        break
                if not found:
                    return None
            return "".join(sorted(res))

        @lru_cache(None)
        def solve(index, f2, f3, f5, f7, is_tight, is_started):
            state = (index, f2, f3, f5, f7, is_tight, is_started)
            if index >= n:
                if f2 >= p2 and f3 >= p3 and f5 >= p5 and f7 >= p7:
                    return ""
                return None

            res = None
            limit = int(num[index]) if is_tight else 9

            start_digit = 0 if is_started else 1
            if is_tight:
                start_digit = limit

            for d in range(start_digit, 10):
                if d == 0:
                    continue

                new_tight = is_tight and (d == limit)

                d_factors = p_factors_map.get(d, Counter())
                nf2 = min(p2, f2 + d_factors.get(2, 0))
                nf3 = min(p3, f3 + d_factors.get(3, 0))
                nf5 = min(p5, f5 + d_factors.get(5, 0))
                nf7 = min(p7, f7 + d_factors.get(7, 0))

                rem_len = n - (index + 1)
                needed_len = min_len_dp_no_zero.get((max(0, p2 - nf2), max(0, p3 - nf3), max(0, p5 - nf5), max(0, p7 - nf7)), float('inf'))

                if needed_len > rem_len:
                    continue

                suffix = solve(index + 1, nf2, nf3, nf5, nf7, new_tight, is_started or d > 0)
                if suffix is not None:
                    current_res = str(d) + suffix
                    if res is None or current_res < res:
                        res = current_res
            
            return res

        result = solve(0, 0, 0, 0, 0, True, False)
        if result is not None:
            return result

        for length in range(n + 1, n + 25):
            rem_len = length - 1
            for first_digit in range(1, 10):
                d_factors = p_factors_map[first_digit]
                rem_f2 = max(0, p2 - d_factors.get(2, 0))
                rem_f3 = max(0, p3 - d_factors.get(3, 0))
                rem_f5 = max(0, p5 - d_factors.get(5, 0))
                rem_f7 = max(0, p7 - d_factors.get(7, 0))

                needed_len = min_len_dp_no_zero.get((rem_f2, rem_f3, rem_f5, rem_f7), float('inf'))
                if needed_len <= rem_len:
                    suffix = get_smallest_suffix(rem_f2, rem_f3, rem_f5, rem_f7)
                    if suffix is not None:
                        padding = "1" * (rem_len - len(suffix))
                        return str(first_digit) + padding + suffix
        return "-1"