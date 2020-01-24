from collections import Counter
from numpy import mean

class Log:
    def __init__(self):
        self.running_time = None
        self.turns = list()

    def stat(self):
        """display the statistical infomation"""
        stat  = ['[ result ]']
        stat += ['Max Turn: {}'.format(max(self.turns))]
        stat += ['Mean Turn: {0:.4f}'.format(mean(self.turns))]
        stat += ['Turn Num']
        for turn, num in sorted(Counter(self.turns).items()):
            stat += ['{:<4d} {}'.format(turn, num)]
        stat += ['All iteration: {}'.format(self.all_iteration)]
        stat += ['Ruuning time: {:.4f}'.format(self.running_time)]
        print('\n'.join(stat))

