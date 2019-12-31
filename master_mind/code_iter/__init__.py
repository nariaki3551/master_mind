from code_iter.all_code_iter import AllCodeIterator
from code_iter.reduced_code_iter import ReducedCodeIterator
from code_iter.sampling_code_iter import SamplingCodeIterator

iters = {
    'all'     : AllCodeIterator,
    'reduce'  : ReducedCodeIterator,
    'sampling': SamplingCodeIterator,
}
