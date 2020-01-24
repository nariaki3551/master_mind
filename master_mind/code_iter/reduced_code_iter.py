import os
import pickle
from time import time
from itertools import combinations_with_replacement, combinations, permutations
from sympy.utilities.iterables import multiset_permutations  # 要素の重複を含む順列を求める用
from .all_code_iter import get_code_generator_all
from .stair_permutations import stair_permutations
from .all_code_iter import get_code_generator_all
from setting import storage
from utils import green_str, magenta_str

class ReducedCodeIterator:
    def __init__(self):
        self.iter_name = 'reduce'
        self.n_iteration = 0

    def set_code_iter(self, config):
        self.config = config
        self.code_iters = dict()
        all_colors = tuple(sorted(list(config.COLORS)))
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
            all_code = list(get_code_generator_all(config))
            enum_time += time()
            config.logger.debug(
                magenta_str(f'[code_iter] save all_code in {config.all_code_path}')
            )
            os.makedirs(config.storage_dir, exist_ok=True)
            with open(config.all_code_path, 'wb') as pf:
                pickle.dump(all_code, file=pf)
        config.logger.info(
            magenta_str(f'[code_iter] the number of all_code is {len(all_code)} ({enum_time:.2f}s)')
        )
        self.code_iters[all_colors] = all_code
        return self

    def __call__(self, codes, *args, **kwargs):
        # guessの履歴から, すでに使用されている色を抽出する
        if codes == 'all':
            guessed_colors = self.config.COLORS
        else:
            guess_hist = kwargs['guess_hist']
            guessed_colors = set(color for guess in guess_hist for color in guess)

        tuple_guessed_colors = tuple(sorted(list(guessed_colors)))
        if not tuple_guessed_colors in self.code_iters:
            self.code_iters[tuple_guessed_colors] \
                = sorted(list(get_code_generator(guessed_colors, self.config)))

        self.n_iteration += len(self.code_iters[tuple_guessed_colors])
        return self.code_iters[tuple_guessed_colors]


def get_code_generator(guessed_colors, config):
    """ return a generator of all code """
    A = guessed_colors
    B = sorted(list(config.COLORS - guessed_colors))

    if len(B) < 2:
        code_iter = get_code_generator_all(config)
    else:
        if config.duplicate:
            code_iter = _code_generator(guessed_colors, config)
        else:
            code_iter = _code_generator_noduplicate(guessed_colors, config)

    return code_iter


def _code_generator(guessed_colors, config):
    A = guessed_colors
    B = sorted(list(config.COLORS - guessed_colors))

    max_usable_num_A = config.NUM_PIN if A else 0
    for i in range(0, max_usable_num_A+1):
        # i : number of using color from guessed_colors
        # j : number of using color from unguessed_colors
        # B_j: using colors from unguessed_colors
        j = config.NUM_PIN - i
        for B_j in stair_permutations(B[:j], j):
            for A_ii in combinations_with_replacement(A, i):
                for A_i in multiset_permutations(A_ii, i):
                    if i == config.PINS:
                        yield tuple(A_i)
                    for A_ixs in combinations(config.PINS, i):
                        # A_i: using colors from guessed_colors
                        # A_ixs: ixs using A_i
                        code = [None]*config.NUM_PIN
                        ix_A, ix_B = 0, 0
                        for ix in range(config.NUM_PIN):
                            if ix in A_ixs:
                                code[ix] = A_i[ix_A]
                                ix_A += 1
                            else:
                                code[ix] = B_j[ix_B]
                                ix_B += 1
                        yield tuple(code)


def _code_generator_noduplicate(guessed_colors, config):
    A = guessed_colors
    B = sorted(list(config.COLORS - guessed_colors))

    for i in range(
            max(0, config.NUM_PIN-len(B)),
            min(config.NUM_PIN, len(A))+1
        ):
        # i : number of using color from guessed_colors
        # j : number of using color from unguessed_colors
        # B_j: using colors from unguessed_colors
        j = config.NUM_PIN - i
        B_j = B[:j]
        for A_i in permutations(A, i):
            if i == config.PINS:
                yield tuple(A_i)
            for A_ixs in combinations(config.PINS, i):
                # A_i: using colors from guessed_colors
                # A_ixs: ixs using A_i
                code = [None]*config.NUM_PIN
                ix_A, ix_B = 0, 0
                for ix in range(config.NUM_PIN):
                    if ix in A_ixs:
                        code[ix] = A_i[ix_A]
                        ix_A += 1
                    else:
                        code[ix] = B_j[ix_B]
                        ix_B += 1
                yield tuple(code)

