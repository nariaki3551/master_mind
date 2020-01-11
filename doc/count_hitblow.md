# count_hitblow function

  calculate hit and blow between code and other_code

  hit ... number of match color and position

  blow ... number of match color - hit

  e.g. (1, 2, 3, 4) and (1, 2, 4, 5) -> (hit, blow) = (2, 1)

​     (1, 2, 3, 4) and (1, 3, 3, 3) -> (hit, blow) = (2, 0)



**old version** 

```python
def _count_hitblow(code, other_code, config):
    a = Conter(code)
    b = Conter(other_code)
    hit = sum(c == oc for c, oc in zip(code, other_code)
    blow = sum(min(a[color], b[color]) for color in config.COLORS) - hit
    return hit, blow
```



**updated version**

```python
def _count_hitblow(code, other_code, config):
    a = [0]*len(config.COLORS)
    b = [0]*len(config.COLORS)
    hit = 0
    for c, oc in zip(code, other_code):
        if c == oc:
            hit += 1
        else:
            a[c-1]  += 1
            b[oc-1] += 1
    blow = sum(min(a[color-1], b[color-1]) for color in config.COLORS)
    return hit, blow
```



**compair**

compair the time of making a search tree

code-iteration: reduce

policy: minmax

| (COLOR, PIN) | update | old    |
| ------------ | ------ | ------ |
| (6, 3)       | 0.19s  | 0.32s  |
| (5, 4)       | 1.48s  | 2.32s  |
| (6, 4)       | 7.30s  | 11.66s |
| (7, 4)       | 31.39s | 46.59s |