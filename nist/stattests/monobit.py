import numpy as np
from math import sqrt, erfc


def monobit(bitSeq: list[int]) -> float:
    # Convert the sequence to a NumPy array for vectorized operations
    bitSeq = np.array(bitSeq)
    n = len(bitSeq)
    # Calculate the test statistic
    s = abs(2 * np.sum(bitSeq) - n) / sqrt(n)
    # Compute the p-value
    p_value = erfc(s / sqrt(2))
    return p_value
