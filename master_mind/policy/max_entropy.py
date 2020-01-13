from math import log2
from multiprocessing import Pool
from utils import calc_dist


def calc_entropy(code, feasible_codes, config):
    entropy = 0
    dist = calc_dist(code, feasible_codes, config)
    for key in dist:
        p = len(dist[key]) / len(feasible_codes)
        entropy -= p*log2(p)
    return entropy, code


def get_max_entropy_code(feasible_codes, guess_iter, config):
    """
    現在あり得る組み合わせの分割方法で,
    最大クラスのエントロピーがとなるような, 検査codeを見つけて, 出力する
    """
    if len(guess_iter) == 1:
        code = guess_iter[0]
        return code, calc_dist(code, feasible_codes, config)

    max_entropy_code = max(
        guess_iter,
        key=lambda code: calc_entropy(code)[0]
    )
    return max_entropy_code, calc_dist(max_entropy_code, feasible_codes, config)
