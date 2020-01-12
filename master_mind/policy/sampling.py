from random import sample
from utils.common import calc_dist
from .minmax import get_minmax_code

N = 1000  # number of sampling

def get_sampling_code(feasible_codes, guess_iter, config):
    n_sample = min(len(feasible_codes), N)
    # print('n_sample: {} <- {}'.format(n_sample, len(feasible_codes)))
    sub_feasible_codes = sample(feasible_codes, n_sample)
    sub_minmax_code, _ = get_minmax_code(
        sub_feasible_codes,
        guess_iter,
        config
    )
    return sub_minmax_code, calc_dist(sub_minmax_code, feasible_codes, config)
