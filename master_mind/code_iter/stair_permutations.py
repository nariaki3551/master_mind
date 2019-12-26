def stair_permutations(elms, num):
    """
    returns perm sorted in steps
    note: avoid duplication due to floor space
    Example
    -------
    elms = (1, 2), num = 3
      ->  [(1, 1, 1), (1, 1, 2)]
    elms = (1, 2, 3), num = 4
      ->  [(1, 1, 1, 1), (1, 1, 1, 2), (1, 1, 2, 2), (1, 1, 2, 3)]
    """
    if len(elms) == 0:
        yield (-1, )  # dummy
    else:
        num_partitions = partitions(num, len(elms))
        for p in num_partitions:
            perm = [None]*num
            elm_ix = 0
            perm_ix = 0
            for n in p:
                for _ in range(n):
                    perm[perm_ix] = elms[elm_ix]
                    perm_ix += 1
                elm_ix += 1
            yield tuple(perm)


def partitions(n, m=None):
    """ Divide integer n by m or less """
    m = m or n
    for p in _partitions(n):
        if len(p) <= m:
            yield p[::-1]


def _partitions(n):
    """ Divide integer n """
    # base case of recursion: zero is the sum of the empty list
    if n == 0:
        yield []
        return

    # modify partitions of n-1 to form partitions of n
    for p in _partitions(n-1):
        yield [1] + p
        if p and (len(p) < 2 or p[1] > p[0]):
            yield [p[0] + 1] + p[1:]
