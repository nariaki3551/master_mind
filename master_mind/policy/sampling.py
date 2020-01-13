from random import sample
from time import time
from utils import calc_dist, blue_str
from .minmax import get_minmax_code
from setting import max_sampling

def get_sampling_code(feasible_codes, guess_iter, config):
    n_sample = min(len(feasible_codes), max_sampling)
    if n_sample < len(feasible_codes):
        info = f'[policy] check_codes {n_sample} <- {len(feasible_codes)}'
        config.logger.info(blue_str(info))
    else:
        info = f'[policy] check_codes {n_sample} (full)'
        config.logger.info(blue_str(info))
    search_time = -time()
    sub_feasible_codes = sample(feasible_codes, n_sample)
    sub_minmax_code, _ = get_minmax_code(
        sub_feasible_codes,
        guess_iter,
        config
    )
    search_time += time()
    config.logger.debug(
        blue_str(f'[policy] guess code {sub_minmax_code} search time {search_time:.2f}s')
    )
    return sub_minmax_code, calc_dist(sub_minmax_code, feasible_codes, config)
