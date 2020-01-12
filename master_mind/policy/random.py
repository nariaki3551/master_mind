from random import choice
from utils import calc_dist


def get_random_code(feasible_codes, guess_iter, config):
    random_code = choice(guess_iter)
    return random_code, calc_dist(random_code, feasible_codes, config)
