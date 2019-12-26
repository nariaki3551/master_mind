# Policy

Policy select the guess code from the `guss_iter`.



## format

```python
def policy_name(feasible_codes, guess_iter, config):
  return the guess code from the guess_iter
```



## minmax

Returns a code that minimizes the size of the max candidate code set

<br>

## max_entroypy

Returns a code that maximizes the entropy of candidate code sets
