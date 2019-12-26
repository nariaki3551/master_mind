from itertools import combinations_with_replacement, combinations, permutations
from sympy.utilities.iterables import multiset_permutations  # 要素の重複を含む順列を求める用

class AllCodeIterator:
    """
    Class AllCodeIterator
    return all codes following config
    """
    def __init__(self):
        self.iter_name = 'all'
        self.n_iteration = 0

    def set_code_iter(self, config):
        self.all_code_iter = sorted(list(get_code_generator_all(config)))
        return self

    def __call__(self, *args, **kwargs):
        self.n_iteration += len(self.all_code_iter)
        return self.all_code_iter


def get_code_generator_all(config):
    """ return a generator of all code """
    if config.duplicate:
        return code_generator_all(config)
    else:
        return code_generator_noduplicate(config)


def code_generator_all(config):
    """ a generator of all code with color duplicate """
    for elms in combinations_with_replacement(config.COLORS, config.NUM_PIN):
        for perm in multiset_permutations(elms, config.NUM_PIN):
            yield tuple(perm)

def code_generator_noduplicate(config):
    """ a generator of all code without color duplicate """
    return permutations(config.COLORS, config.NUM_PIN)
