from collections import defaultdict
from functools import lru_cache
from time import time


def calc_dist(guess, feasible_codes, config):
    """
    caluculate distribution of feasible codes by guess

    Return
    ------
    distribution: dist
        key is (hit, blow), value is a list of feasible codes of (hit, blow)
    """
    distribution = defaultdict(list)
    for code in feasible_codes:
        hit, blow = count_hitblow(guess, code, config)
        distribution[hit, blow].append(code)
    return distribution


def count_hitblow(code, other_code, config):
    """
    calculate hit and blow between code and other_code
    hit ... number of match color and position
    blow ... number of match color - hit
    e.g. (1, 2, 3, 4) and (1, 2, 4, 5) -> (hit, blow) = (2, 1)
         (1, 2, 3, 4) and (1, 3, 3, 3) -> (hit, blow) = (2, 0)
    """
    return _count_hitblow(*sorted([code, other_code]), config)


@lru_cache(maxsize=None)
def _count_hitblow(code, other_code, config):
    a = [0]*len(config.COLORS)
    b = [0]*len(config.COLORS)
    hit = 0
    for c, oc in zip(code, other_code):
        if c == oc:
            hit += 1
        else:
            a[c-1]  += 1
            b[oc-1] += 1
    blow = sum(min(a[color-1], b[color-1]) for color in config.COLORS)
    return hit, blow


def input_hitblow(config):
    while True:
        user_input = input('input: hit blow\n')
        if len(user_input.split()) != 2:
            continue
        hit, blow = user_input.split()
        if not hit.isdigit() or not blow.isdigit():
            continue
        hit, blow = map(int, [hit, blow])
        if hit > config.NUM_PIN or blow > config.NUM_PIN:
            continue
        return hit, blow


def time_counter(func):
    def wrapper(*args, **kwargs):
        running_time = -time()
        func(*args, **kwargs)
        running_time += time()
        print('\nRunning Time {:.2f}s'.format(running_time))
    return wrapper
