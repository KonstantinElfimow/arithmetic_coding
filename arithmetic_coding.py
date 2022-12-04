from numpy import log2
from math import ceil

accurateness: int = 8  # Округдение до знака


def float_to_bin(f: float) -> str:
    result: str = ''
    summary: float = 0.0
    for i in range(1, 16):
        if round(summary + 2 ** -i, accurateness) > f:
            result += '0'
        else:
            summary += 2 ** -i
            result += '1'
    return result


def _arithmetic_encode_algorythm(p_ensemble: dict, seq: list) -> (tuple, ):
    q_ensemble: dict = dict()
    q: float = 0.0
    for i, (alpha, p) in enumerate(p_ensemble.items()):
        q_ensemble[alpha] = q
        q = (round(q + p, accurateness))

    q_seq_i: float = 0.0
    p_seq_i: float = 0.0

    result_table: list = list()
    result_table.append(tuple(['step k', 's_i', 'p(s_i)', 'q(s_i)', 'F(s_ik)', 'G(s_ik)']))
    result_table.append(tuple([0, '-', '-', '-', 0, 1]))
    for i, alpha in enumerate(seq):
        if i == 0:
            q_seq_i = q_ensemble[alpha]
            p_seq_i = p_ensemble[alpha]
        else:
            q_seq_i = round(q_seq_i + round(p_seq_i * q_ensemble[alpha], accurateness), accurateness)
            p_seq_i = round(p_seq_i * p_ensemble[alpha], accurateness)
        result_table.append(tuple([i + 1, alpha, p_ensemble[alpha], q_ensemble[alpha], q_seq_i, p_seq_i]))

    L: int = ceil(- log2(p_seq_i)) + 1
    X: float = round(q_seq_i + round(p_seq_i / 2, accurateness), accurateness)
    code_word = float_to_bin(X)

    return tuple(result_table), L, X, code_word


def arithmetic_encode(*, input_ensemble: dict, sequence: list) -> (tuple, int, float, str):
    print(input_ensemble)
    print(*sequence)
    result_table, L, X, code_word = _arithmetic_encode_algorythm(input_ensemble, sequence)
    print()
    return result_table, L, X, code_word


def arithmetic_decode(*, input_ensemble: dict, code_word: float) -> tuple:
    ...
