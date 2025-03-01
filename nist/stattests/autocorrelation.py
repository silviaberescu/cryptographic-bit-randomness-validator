import numpy as np
from math import sqrt, erfc


def autocorrelation(bitstr: list[int], d: int) -> float:
    n = len(bitstr)
    # Convert the bit sequence to a NumPy array
    bitstr = np.array(bitstr)
    # Compute the XOR of the bit sequence
    e = bitstr[:len(bitstr) - d] ^ bitstr[d:]
    # Compute the test statistic
    sum_e = np.sum(e)
    s_obs = abs(2 * sum_e - n + d) / sqrt(n - d)
    # Compute the p-value
    p_val = erfc(s_obs / sqrt(2))
    return np.round(p_val, 3)
