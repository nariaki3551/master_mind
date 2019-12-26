# code iter

code iter is a class to reduce the search time from the set of feasible codes `codes`  and the history of guess code `guess_hist`.
The policy function selects the guess code from the set of codes returned by `__call__` function of the code iter class. Therefore, the fewer codes the code iter returns, the faster the policy function can select the guess code.

<br>



## format

```python
class ClassName:
  def init(self):
    self.iter_name = iter_name
    self.n_iteration = 0  # recode the number of iteration

  def set_code_iter(self, config):
    # the first setting for the __call__
    return self

  def __call__(self, codes, *args, **kwargs):
    # codes is  'all' or the set(list) of feasible codes
    # if codes == 'all':
    #     return the all code
    # else:
    #     return the set of codes to input the policy function
```

<br>

ex) AllCodeIterator

```python
class AllCodeIterator:
    def __init__(self):
        self.iter_name = 'all'
        self.n_iteraion = 0

    def set_code_iter(self, config):
        self.all_code_iter = sorted(list(get_code_generator_all(config)))
        return self

    def __call__(self, *args, **kwargs):
        self.n_iteraion += len(self.all_code_iter)
        return self.all_code_iter
```

<br>



## AllCodeIterator

iterator of all code.

**algorithm**

1. Extract colors by the number of pins with overlap
2. Rearrange patterns while removing duplicate patterns

<br>

## ReducedCodeIterator

Iterator of code reduced by guess history.

**idea**

A ... the set of colors are included in the guess history

B ... the set of colors are **not** included in the guess history

+ The color of B can be considered indistinguishable in that turn
  + For example, at the first turn, player cannot distinguish all colors
    in the case of 3 colors and 3 pins, it is only necessary to search for (1, 1, 1), (1, 1, 2), (1, 2, 3)
  + In this way, combinations of B colors that cannot be distinguished can be reduced

