import numpy as np
from mpmath import gammainc


def mbit(bitSeq: list[int], M_param: int):
    n = len(bitSeq)
    # Convert the bit sequence to a NumPy array
    bitSeq = np.array(bitSeq)
    nr_blocks = n // M_param

    # Reshape the array to have blocks of size M_param
    blocks = bitSeq[:nr_blocks * M_param].reshape(nr_blocks, M_param)
    # Compute the mean for each block
    block_means = np.mean(blocks, axis=1)
    # Compute the test statistic
    stats = np.sum((block_means - 0.5) ** 2)
    chi_squared = stats * 4 * nr_blocks
    # Compute the p-value
    p_value = gammainc(chi_squared / 2, nr_blocks / 2)

    return float(p_value)
