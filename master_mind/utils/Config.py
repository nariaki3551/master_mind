from policy import policies

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


