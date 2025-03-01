from stattests.autocorrelation import autocorrelation
from stattests.mbit import mbit
from stattests.monobit import monobit
from stattests.runs import runs
from stattests.serial import serial


def test_autocorrelation(bitSeq: list[int], m: int) -> tuple[float, float]:
    pvalue = autocorrelation(bitSeq, m)
    print(f"Autocorrelation test p-value: {pvalue}")
    assert 0 <= pvalue <= 1
    return pvalue


def test_mbit(bitSeq: list[int], M_param: int) -> float:
    pvalue = mbit(bitSeq, M_param)
    print(f"M-bit test p-value: {pvalue}")
    assert 0 <= pvalue <= 1
    return pvalue


def test_monobit(bitSeq: list[int]) -> float:
    pvalue = monobit(bitSeq)
    print(f"Monobit test p-value: {pvalue}")
    assert 0 <= pvalue <= 1
    return pvalue


def test_runs(bitSeq: list[int]) -> float:
    pvalue = runs(bitSeq)
    print(f"Runs test p-value: {pvalue}")
    assert 0 <= pvalue <= 1
    return pvalue


def test_serial(bitSeq: list[int], m: int) -> tuple[float, float]:
    pvalue1, pvalue2 = serial(bitSeq, m)
    print(f"Serial test p-values: {pvalue1}, {pvalue2}")
    assert 0 <= pvalue1 <= 1 and 0 <= pvalue2 <= 1
    return pvalue1, pvalue2


def test_all_stat_tests():
    bitSeq = "1010101010101010101010101010101010101010101010101010101010101010"
    bitSeq = [int(bit) for bit in bitSeq]
    m = 10
    M_param = 10
    print("Running statistical tests...")
    test_autocorrelation(bitSeq, m)
    test_mbit(bitSeq, M_param)
    test_monobit(bitSeq)
    test_runs(bitSeq)
    test_serial(bitSeq, m)
    print("All unit tests for the simplified batch \
of statistical tests passed")
    return True


if __name__ == "__main__":
    test_all_stat_tests()
