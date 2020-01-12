from .random import get_random_code
from .minmax import get_minmax_code
from .max_entropy import get_max_entropy_code
from .sampling import get_sampling_code

policies = {
    'random'     : get_random_code,
    'minmax'     : get_minmax_code,
    'max_entropy': get_max_entropy_code,
    'sampling'   : get_sampling_code,
}
