from random import sample
from time import time
from math import floor
from .reduced_code_iter import ReducedCodeIterator
from utils import green_str


class SamplingCodeIterator(ReducedCodeIterator):
    def __init__(self):
        self.iter_name = 'sampling'
        self.n_iteration = 0

    def set_code_iter(self, config):
        self.config = config
        super().set_code_iter(config)
        self.set_n_par_iteration(config)
        return self

    def set_n_par_iteration(self, config):
        all_code_iter = super().__call__('all', config=config)
        code_iter = super().__call__(set(), guess_hist=[])
        # self.n_par_iteration = round(len(all_code_iter) * len(code_iter)*4)
        self.n_par_iteration = round(len(all_code_iter) * len(code_iter))

    def __call__(self, codes, *args, **kwargs):
        config = kwargs['config']
        code_iter = super().__call__(codes, *args, **kwargs)
        self.n_iteration -= len(code_iter)
        n_sample = floor(self.n_par_iteration/len(codes))
        if codes == 'all' \
        or len(code_iter) < n_sample:
            info = f'[code_iter] sampling_iter {len(code_iter)} (full)'
            config.logger.info(green_str(info))
            self.n_iteration += len(code_iter)
            return code_iter
        else:
            info = f'[code_iter] sampling {n_sample} <- {len(code_iter)}'
            config.logger.info(green_str(info))
            self.n_iteration += n_sample
            return sample(code_iter, n_sample)
