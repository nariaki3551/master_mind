from utils.common import calc_dist
from math import log2

def calc_entropy(code, feasible_codes, config):
    entropy = 0
    dist = calc_dist(code, feasible_codes, config)
    for key in dist:
        p = len(dist[key]) / len(feasible_codes)
        entropy -= p*log2(p)
    score = (entropy, code in feasible_codes)
    return score


def get_max_entropy_code(feasible_codes, guess_iter, config):
    """
    現在あり得る組み合わせの分割方法で,
    最大クラスのエントロピーがとなるような, 検査codeを見つけて, 出力する
    """
    max_entropy_code = max(
        guess_iter,
        key=lambda code: calc_entropy(code, feasible_codes, config)
    )
    return max_entropy_code, calc_dist(max_entropy_code, feasible_codes, config)
