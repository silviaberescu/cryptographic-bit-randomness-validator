import math


def validate_bit_sequence(bitSeq: list[int]) -> bool:
    if not all(ch in [0, 1] for ch in bitSeq):
        return False
    return True


def validate_alpha(alpha: float) -> bool:
    if alpha >= 1 or alpha <= 0:
        return False
    return True


def validate_M_param_serial(M_param: int, n: int) -> bool:
    if M_param < 3 or M_param > math.log2(n) - 2:
        return False
    return True


def validate_M_param_Mbit(M_param: int, n: int) -> bool:
    if M_param < 0.1 * n or M_param > n:
        return False
    return True


def validate_d(d: int, n: int) -> bool:
    if d > n // 2 or d <= 0:
        return False
    return True
