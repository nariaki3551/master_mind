# setting
SCR_DIR = './../master_mind'
DATA_DIR = './storage'
PROCESS = 4  # number of thread

import sys
sys.path.append(SCR_DIR)
import os
from contextlib import redirect_stdout
from itertools import product
import pickle
import multiprocessing

from policy import *
from code_iter import *
from master_mind import master_mind, Config, Log

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


def main():
    make_data1()
    make_data2()
    make_data3()


def make_data1():
    Cs = [6]
    Ps = list(range(1, 3))
    iter_names = ['all', 'reduce', 'sampling']
    policy_names = ['minmax']
    duplicate = True
    pickle_path = DATA_DIR + '/data1'
    make_data(Cs, Ps, iter_names, policy_names, duplicate, pickle_path)


def make_data2():
    Cs = list(range(1, 3))
    Ps = [4]
    iter_names = ['all', 'reduce', 'sampling']
    policy_names = ['minmax']
    duplicate = True
    pickle_path = DATA_DIR + '/data2'
    make_data(Cs, Ps, iter_names, policy_names, duplicate, pickle_path)


def make_data3():
    Cs = [6]
    Ps = [4]
    iter_names = ['reduce']
    policy_names = ['minmax', 'max_entropy']
    duplicate = True
    pickle_path = DATA_DIR + '/data3'
    make_data(Cs, Ps, iter_names, policy_names, duplicate, pickle_path)


def make_data(Cs, Ps, iter_names, policy_names, duplicate, pickle_path):
    # make dirctory
    if not os.path.exists(pickle_path):
        os.mkdir(pickle_path)

    # generate setarch tree
    config_iter = product(Cs, Ps, iter_names, policy_names,
                          [duplicate], [pickle_path])
    with multiprocessing.Pool(processes=PROCESS) as pool:
        pool.starmap(make_search_tree, config_iter, chunksize=1)

    # save config
    data_config = {
        'Cs': Cs, 'Ps': Ps, 'iter_names': iter_names,
        'policy_names': policy_names, 'duplicate': duplicate
    }
    with open(pickle_path + '/config.pickle', 'wb') as pf:
        pickle.dump(data_config, pf)


def make_search_tree(C, P, iter_name, policy_name, duplicate, pickle_path):
    process = multiprocessing.current_process()
    print('ID =', process.pid, 'C =', C, ' P =', P,
          'iter_name =', iter_name,' policy_name =', policy_name)
    code_iter = iters[iter_name]()
    config = Config(
        nc=C, np=P, policy_name=policy_name,
        code_iter=code_iter, mode='mktree',
        duplicate=duplicate
    )
    log = Log()

    # excute
    with redirect_stdout(open(os.devnull, 'w')):
        master_mind(log, config)

    # save
    pickle_file = pickle_path + '/{}_{}_{}_{}.pickle'.format(
        C, P, iter_name, policy_name
    )
    with open(pickle_file, 'wb') as pf:
        pickle.dump((log, config), pf)
    print('save', pickle_file)


if __name__ == '__main__':
    main()
