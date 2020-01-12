from .all_code_iter import AllCodeIterator
from .reduced_code_iter import ReducedCodeIterator
from .sampling_code_iter import SamplingCodeIterator

code_iters = {
    'all'     : AllCodeIterator,
    'reduce'  : ReducedCodeIterator,
    'sampling': SamplingCodeIterator,
}
