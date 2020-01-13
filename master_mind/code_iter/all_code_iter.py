import os
import pickle
from time import time
from itertools import combinations_with_replacement, combinations, permutations
from sympy.utilities.iterables import multiset_permutations  # 要素の重複を含む順列を求める用
from utils import magenta_str

class AllCodeIterator:
    """
    Class AllCodeIterator
    return all codes following config
    """
    def __init__(self):
        self.iter_name = 'all'
        self.n_iteration = 0

    def set_code_iter(self, config):
        if os.path.exists(config.all_code_path):
            config.logger.debug(
                magenta_str(f'[code_iter] all_code is load from {config.all_code_path}')
            )
            enum_time = -time()
            with open(config.all_code_path, 'rb') as pf:
                all_code = pickle.load(pf)
            enum_time += time()
        else:
            config.logger.debug(magenta_str(f'[code_iter] enumerate all_codes'))
            enum_time = -time()
            all_code = sorted(list(get_code_generator_all(config)))
            enum_time += time()
            config.logger.debug(
                magenta_str(f'[code_iter] all_code is saved in {config.all_code_path}')
            )
            # save all_code
            os.makedirs(config.storage_dir, exist_ok=True)
            with open(config.all_code_path, 'wb') as pf:
                pickle.dump(all_code, file=pf)
        config.logger.info(
            magenta_str(f'[code_iter] the number of all_code is {len(all_code)} ({enum_time:.2f}s)')
        )
        self.all_code_iter = all_code
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
