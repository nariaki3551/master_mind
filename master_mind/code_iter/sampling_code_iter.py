from code_iter.reduced_code_iter import ReducedCodeIterator
from random import sample
from math import floor

class SamplingCodeIterator(ReducedCodeIterator):
    def __init__(self):
        self.iter_name = 'sampling'
        self.n_iteration = 0

    def set_code_iter(self, config):
        self.config = config
        super().set_code_iter(config)
        self.set_n_par_iteration()
        return self

    def set_n_par_iteration(self):
        all_code_iter = super().__call__('all')
        code_iter = super().__call__(set(), guess_hist=[])
        self.n_par_iteration = round(len(all_code_iter) * len(code_iter)*4)

    def __call__(self, codes, *args, **kwargs):
        code_iter = super().__call__(codes, *args, **kwargs)
        self.n_iteration -= len(code_iter)
        n_sample = floor(self.n_par_iteration/len(codes))
        if codes == 'all' \
        or len(code_iter) < n_sample:
            print('samplineg:', len(code_iter), '(full)')
            self.n_iteration += len(code_iter)
            return code_iter
        else:
            print('samplineg:', n_sample)
            self.n_iteration += n_sample
            return sample(code_iter, n_sample)
