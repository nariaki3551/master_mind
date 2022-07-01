# Master Mind

[Mastermind](https://en.wikipedia.org/wiki/Mastermind_(board_game)) is a kind of classical board games.<br>
This python project searches the optimal strategy for the Mastermind.

<br>


## Development environment

python: 3.7.5, numpy: 1.17.4, sympy: 1.5, matplotlib: 3.1.2

<br>

## Setup

```
pip install -r requairements.txt
```

<br>

## Get Start

```
python master_mind.py C P [--policy policy_name]
                          [--iter code_iter_name]
                          [--mode mode]
                          [--no_duplicate]
                          [--benchmark]
                          [--log_level]
```

C and P are the number of colors and pins, respectively.

<br>

**options**

+ `--policy` (Default is minmax)
  + the details of policies are described in `policy/policy.md`
+ `--iter` (Default is all)
  + the details of code iterators are described in `code_iter/code_iter.md`
+ `--no_duplicate`
  + the secret and guess code has no color duplication if you use this option.
+ `--mode` (Default is mktree)
  + select `--mode guess` when you want to know the actual guess code by policies.
+ `--log_level` (Default is critical)
  + the level of standard output
+ `--benchmark`
  + execute program for benchmarking policies, codings and so on


<br>

<br>

## Modes

### mktree mode (Default)

Making the search tree according to the policy

`--mode mktree`

**save search tree**

`python master_mind.py C P [--policy policy_name] [--iter code_iter_name] > savename`

<br>

### guess mode

Interactively search the guess code according to the policy

`--mode guess`

<br>

If you want to use this program for [this online game](https://www.webgamesonline.com/mastermind/) with default setting, you run `python master_mind.py 8 4 --no_duplicate --mode guess`.

<br>

## Scripts

**code_iter**

Code-iterators which is used to search a guess code

<br>

**policy**

Algorithms to search a guess code from feasible codes and the guess history, and so on

<br>

**utils**

Stock common functions
