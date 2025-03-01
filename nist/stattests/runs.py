import numpy as np
from scipy.special import erfc


def runs(seq: list[int]) -> float:
    # Convert the sequence to a NumPy array
    seq = np.array(seq)
    n = len(seq)

    # Count the number of "1"s
    n_1 = np.sum(seq)
    # Proportion of "1"s in the binary sequence
    ratio = n_1 / n
    # Count the number of runs (gaps and blocks)
    stat = np.sum(seq[:-1] != seq[1:]) + 1

    # Compute p-value
    a = stat - 2 * n * ratio * (1 - ratio)
    b = 2 * np.sqrt(2 * n) * ratio * (1 - ratio)
    p_value = erfc(a / b)

    return p_value
