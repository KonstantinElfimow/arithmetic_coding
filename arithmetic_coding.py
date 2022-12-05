from numpy import log2
from math import ceil

accurateness: int = 8  # Округдение до знака


def _insert_row_with_format(table: list, l: list = None, length: int = 0) -> None:
    if l:
        table.append(tuple(l))
    if length:
        table.append(tuple(['-' * length]))


def _create_encode_table(p_ensemble: dict, q_ensemble: dict, seq: list) -> (tuple, float, float):
    F_ik = 0
    G_ik = 1

    encode_table: list = list()
    _insert_row_with_format(encode_table, ['step k', 's_i', 'p(s_i)', 'q(s_i)', 'F(s_ik)', 'G(s_ik)'], 65)

    _insert_row_with_format(encode_table, [0, '-', '-', '-', F_ik, G_ik], 65)

    for i, alpha in enumerate(seq):
        if i == 0:
            F_ik = q_ensemble[alpha]
            G_ik = p_ensemble[alpha]
        else:
            F_ik = round(F_ik + round(G_ik * q_ensemble[alpha], accurateness), accurateness)
            G_ik = round(G_ik * p_ensemble[alpha], accurateness)

        _insert_row_with_format(encode_table, [i + 1, alpha, p_ensemble[alpha], q_ensemble[alpha], F_ik, G_ik], 65)

    return tuple(encode_table), F_ik, G_ik


def _bin_to_float(b: str) -> float:
    return round(sum([int(x) * 2 ** -(i + 1) for i, x in enumerate(b)]), accurateness)


def _create_decode_table(p_ensemble: dict, q_ensemble: dict, seq: list, code_word: str) -> tuple:
    F_k = 0
    G_k = 1

    decode_table: list = list()
    _insert_row_with_format(decode_table, ['step k', 'F_k', 'G_k', 'Guess s_i', 'q(s_i)', 'Comparison', 'Solution'], 90)

    x: float = _bin_to_float(code_word)
    _insert_row_with_format(decode_table, [0, 'X = 0.{} -> x = {}'.format(code_word, x)], 90)

    for i, alpha in enumerate(seq):
        for s, q in q_ensemble.items():
            _insert_row_with_format(decode_table, [i + 1, F_k, G_k, s, q, f'{round(F_k + q * G_k, accurateness)} < {x}',
                                                   round(F_k + q * G_k, accurateness) < x])
        _insert_row_with_format(decode_table, length=90)
        if i == 0:
            F_k = q_ensemble[alpha]
            G_k = p_ensemble[alpha]
        else:
            F_k = round(F_k + round(G_k * q_ensemble[alpha], accurateness), accurateness)
            G_k = round(G_k * p_ensemble[alpha], accurateness)
    return tuple(decode_table)


def _make_q_ensemble(p_ensemble: dict) -> dict:
    q_ensemble: dict = dict()
    q: float = 0.0
    for i, (alpha, p) in enumerate(p_ensemble.items()):
        q_ensemble[alpha] = q
        q = (round(q + p, accurateness))
    return q_ensemble


def _length_of_code_word(G: float) -> int:
    return ceil(- log2(G)) + 1


def _code_word_digital(F: float, G: float) -> float:
    return round(F + round(G / 2, accurateness), accurateness)


def _float_to_bin(f: float, length: int = 15) -> str:
    length = max(15, length)
    result: str = ''
    inter: float = f
    for _ in range(length):
        inter = round(inter * 2, accurateness)
        if inter - 1 >= 0:
            inter -= 1
            result += '1'
        else:
            result += '0'
    return result


def _arithmetic_encode_algorythm(p_ensemble: dict, seq: list) -> (tuple, tuple, int, float, str):
    q_ensemble: dict = _make_q_ensemble(p_ensemble)

    encode_table, F, G = _create_encode_table(p_ensemble, q_ensemble, seq)

    L: int = _length_of_code_word(G)
    X: float = _code_word_digital(F, G)
    code_word: str = _float_to_bin(X, length=L)

    decode_table = _create_decode_table(p_ensemble, q_ensemble, seq, code_word[0: L])

    return encode_table, decode_table, L, X, code_word[0: 15]


def arithmetic_coding(*, input_ensemble: dict, sequence: list) -> (tuple, tuple, int, float, str):
    print(input_ensemble)
    print(*sequence)
    print()
    encode_table, decode_table, L, X, code_word = _arithmetic_encode_algorythm(input_ensemble, sequence)
    return encode_table, decode_table, L, X, code_word
