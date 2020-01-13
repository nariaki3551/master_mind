# Master Mind

[Mastermind](https://en.wikipedia.org/wiki/Mastermind_(board_game)) is a kind of classical board games.<br>
This python project searches the optimal strategy for the Mastermind.

<br>

version: 0.4 (2020-1-13)

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
                          [--log_level]
```

C and P are the number of colors and pins, respectively.

<br>

**options**

+ `--policy` (Default is minmax)
  + you can see all available policies by  `python master_mind.py C P --policy`
  + document about each policy is in `policy/policy.md`
+ `--iter` (Default is all)
  + you can see all aveilable code iterators by  `python master_mind.py C P --iter`
  + document about each code iterator is in `code_iter/code_iter.md`
+ `--no_duplicate`

  + if you use this option, the secret and guess code has no color duplicate.
+ `--mode` (Default is mktree)

  + If you what to know a guess code the algorithm searches, select `--mode guess`
+ `--log_level` (Default is critical)
  + you can adjust the logs displayed



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

If you play [this online game](https://www.webgamesonline.com/mastermind/) with default setting, you run `python master_mind.py 8 4 --no_duplicate --mode guess`.

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
