from argparse import ArgumentParser
from collections import Counter
from numpy import mean
from time import time

from utils import time_counter, input_hitblow, Config, Log
from policy import policies
from code_iter import code_iters


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
        choices=list(code_iters),
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
    code_iter = code_iters[args.iter]()
    config = Config(
        args.C, args.P, args.policy,
        code_iter, args.mode, not args.no_duplicate
    )
    print('[ setting ]')
    print(config)

    # generate log
    log = Log()  # for the statistical information

    # main function
    master_mind(log, config)

