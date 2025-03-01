import numpy as np
from scipy.special import gammainc


def serial(seq: list[int], m: int) -> tuple[float, float]:
    n = len(seq)

    # Extend sequence for overlapping blocks
    seq_extended = np.array(seq + seq[:m - 1])

    def compute_psi(m_val: int) -> float:
        # Generate all possible binary patterns of length m_val
        patterns = np.arange(2**m_val)
        # Convert to binary strings
        patterns_bin = np.array([np.binary_repr(p, width=m_val)
                                 for p in patterns])

        # Create a sliding window of m_val bits in the extended sequence
        windows = np.array([
            ''.join(map(str, seq_extended[i:i + m_val])) for i in range(n)
        ])

        # Count occurrences of each pattern
        counts = np.array([np.sum(windows == pattern) for pattern
                           in patterns_bin])

        # Compute psi
        psi = np.sum(counts**2) / n - n
        return psi

    # Calculate psi values
    psi_0 = compute_psi(m)
    psi_1 = compute_psi(m - 1)
    psi_2 = compute_psi(m - 2)

    # Compute test statistics
    stat_0 = psi_0 - psi_1
    stat_1 = psi_0 - 2 * psi_1 + psi_2

    # Compute p-values
    p_value1 = gammainc(2**(m - 2), stat_0 / 2)
    p_value2 = gammainc(2**(m - 3), stat_1 / 2)

    return p_value1, p_value2
