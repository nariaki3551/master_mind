from multiprocessing import Pool
from utils import calc_dist


def max_feasibles(code, feasible_codes, config):
    score = (
        max(map(len, calc_dist(code, feasible_codes, config).values())),
        code not in feasible_codes
    )
    return score


def get_minmax_code(feasible_codes, guess_iter, config):
    """
    現在あり得る組み合わせの分割方法で,
    最大クラスの大きさが最小となるような, 検査codeを見つけて, 出力する
    """
    if len(guess_iter) == 1:
        code = guess_iter[0]
        return code, calc_dist(code, feasible_codes, config)

    minmax_code = min(
        guess_iter,
        key=lambda code: max_feasibles(code, feasible_codes, config)
    )
    return minmax_code, calc_dist(minmax_code, feasible_codes, config)
