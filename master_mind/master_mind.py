from argparse import ArgumentParser
from collections import Counter
from numpy import mean
from time import time

from utils.common import time_counter, input_hitblow
from policy import (
    get_random_code,
    get_minmax_code,
    get_max_entropy_code,
)
from code_iter import (
    AllCodeIterator,
    ReducedCodeIterator,
    SamplingCodeIterator,
)

policies = {
    'random'     : get_random_code,
    'minmax'     : get_minmax_code,
    'max_entropy': get_max_entropy_code,
}

iters = {
    'all'     : AllCodeIterator,
    'reduce'  : ReducedCodeIterator,
    'sampling': SamplingCodeIterator,
}


class Config:
    def __init__(self, nc, np, policy_name,
                 code_iter, mode, duplicate):
        # setting number of color and pins
        self.NUM_COLOR = nc
        self.NUM_PIN = np
        self.COLORS = set(i for i in range(1, nc+1))
        self.PINS = set(i for i in range(np))
        # setting policy
        self.policy_name = policy_name
        self.policy = policies[policy_name]
        # setting other parameter
        self.mode = mode
        self.duplicate = duplicate
        # settin code-iter
        self.code_iter = code_iter.set_code_iter(self)

    def __hash__(self):
        return 1  # for lru_chache

    def __str__(self):
        s  = 'NUM_COLOR : {}\n'.format(self.NUM_COLOR)
        s += 'NUM_PIN   : {}\n'.format(self.NUM_PIN)
        s += 'POLICY    : {}\n'.format(self.policy_name)
        s += 'CODE_ITER : {}\n'.format(self.code_iter.iter_name)
        s += 'MODE      : {}\n'.format(self.mode)
        s += 'DUPLICATE : {}\n'.format(['not ', ''][self.duplicate]+'allowed')
        return s


class Log:
    def __init__(self):
        self.running_time = None
        self.turns = list()


@time_counter
def master_mind(log, config):
    if config.mode == 'mktree':
        print('\n[ search tree ]')
    elif config.mode == 'guess':
        print('\n[ guess mode ]')

    log.running_time = - time()

    # main
    all_codes = list(config.code_iter('all'))
    step(all_codes, [], log, config)

    log.running_time += time()
    disp_stat(log, config)


def step(codes, guess_hist, log, config):
    """
    Params
    ------
    codes    : the set of codes
    guess_hit: history of guess code
    log      : the log of search
    config   : setting of probelm (e.g. the number of color and pins)
    """
    # number of trials
    depth = len(guess_hist) + 1

    # guess
    code_iter = config.code_iter(codes, guess_hist=guess_hist)
    guess, dist = config.policy(codes, code_iter, config)
    guess_hist.append(guess)
    print('Trial{}: {}'.format(depth, guess))

    # display the search information and do next step
    if config.mode == 'mktree':
        for hit, blow in sorted(dist, key=lambda k: len(dist[k])):
            print('{}-> {} {} '.format(
                '\t'*depth, (hit, blow), len(dist[hit, blow])), end=''
            )
            if len(dist[hit, blow]) == 1: # find the secret code
                turn = depth if hit == config.NUM_PIN else depth+1
                print('secret is {} {} Turns'.format(dist[hit, blow][0], turn))
                log.turns.append(turn)
                continue
            step(dist[hit, blow], guess_hist, log, config)
        guess_hist.pop()

    elif config.mode == 'guess':
        print('Candidates:', len(codes))
        hit, blow = input_hitblow(config)
        if len(dist[hit, blow]) == 1:  # find the secret code
            print('secret is {}'.format(dist[hit, blow][0]))
            exit()
        step(dist[hit, blow], guess_hist, log, config)


def disp_stat(log, config):
    """display the statistical infomation"""
    stat  = ['[ result ]']
    stat += ['Max Turn: {}'.format(max(log.turns))]
    stat += ['Mean Turn: {0:.4f}'.format(mean(log.turns))]
    stat += ['Turn Num']
    for turn, num in sorted(Counter(log.turns).items()):
        stat += ['{:<4d} {}'.format(turn, num)]
    stat += ['All iteration: {}'.format(config.code_iter.n_iteration)]
    stat += ['Ruuning time: {:.4f}'.format(log.running_time)]
    print('\n'.join(stat))


def argparser():
    parser = ArgumentParser()
    parser.add_argument(
        'C', type=int, help='Number of colors'
    )
    parser.add_argument(
        'P', type=int, help='Number of pins'
    )
    parser.add_argument(
        '--policy',
        choices=list(policies),
        default='minmax',
        help='Guess code policy (Default is minmax)'
    )
    parser.add_argument(
        '--iter',
        choices=list(iters),
        default='reduce',
        help='Code iter type'
    )
    parser.add_argument(
        '--mode',
        choices=['mktree', 'guess'],
        default='mktree',
        help='If mode is guess, run interactive mode'
    )
    parser.add_argument(
        '--no_duplicate',
        action='store_true',
        help='Not allowed color dupulicate'
    )
    return parser


def assert_args(args):
    assert args.C > 0, "C should be greater than 0"
    assert args.P > 0, "P should be greater than 0"
    assert not args.no_duplicate or args.C >= args.P, \
        "if you use --no_duplicate option, C must be greater than or eaual P"


if __name__ == '__main__':
    parser = argparser()
    args = parser.parse_args()

    # check arguments
    assert_args(args)

    # generate config
    code_iter = iters[args.iter]()
    config = Config(
        args.C, args.P, args.policy,
        code_iter, args.mode, not args.no_duplicate
    )
    print('[ setting ]')
    print(config)

    log = Log()  # for the statistical information
    master_mind(log, config)

