from numpy import log2
from math import ceil

accurateness: int = 8  # Округдение до знака


def _float_to_bin(f: float) -> str:
    result: str = ''
    inter: float = f
    for _ in range(15):
        inter = round(inter * 2, accurateness)
        if inter - 1 >= 0:
            inter -= 1
            result += '1'
        else:
            result += '0'
    return result


def _create_encode_table(p_ensemble: dict, q_ensemble: dict, seq: list) -> (tuple, float, float):
    F_ik: float = 0.0
    G_ik: float = 0.0

    encode_table: list = list()
    encode_table.append(tuple(['step k', 's_i', 'p(s_i)', 'q(s_i)', 'F(s_ik)', 'G(s_ik)']))
    encode_table.append(tuple(['-' * 65]))
    encode_table.append(tuple([0, '-', '-', '-', 0, 1]))
    encode_table.append(tuple(['-' * 65]))

    for i, alpha in enumerate(seq):
        if i == 0:
            F_ik = q_ensemble[alpha]
            G_ik = p_ensemble[alpha]
        else:
            F_ik = round(F_ik + round(G_ik * q_ensemble[alpha], accurateness), accurateness)
            G_ik = round(G_ik * p_ensemble[alpha], accurateness)
        encode_table.append(tuple([i + 1, alpha, p_ensemble[alpha], q_ensemble[alpha], F_ik, G_ik]))
        encode_table.append(tuple(['-' * 65]))
    return tuple(encode_table), F_ik, G_ik


def create_decode_table(p_ensemble: dict, q_ensemble: dict, seq: list, code_word: str) -> tuple:
    decode_table: list = list()
    decode_table.append(tuple(['step k', 'F_k', 'G_k', 'Guess s_i', 'q(s_i)', 'Comparison', 'Solution']))
    decode_table.append(tuple(['-' * 90]))
    x: float = round(sum([int(x) * 2 ** -(i + 1) for i, x in enumerate(code_word)]), accurateness)
    decode_table.append(tuple([0, 'X = 0.{} -> x = {}'.format(code_word, x)]))
    decode_table.append(tuple(['-' * 90]))

    F_k: float = 0.0
    G_k: float = 1.0
    for i, alpha in enumerate(seq):
        for s, q in q_ensemble.items():
            decode_table.append(tuple([i + 1, F_k, G_k, s, q, f'{round(F_k + q * G_k, accurateness)} < {x}', round(F_k + q * G_k, accurateness) < x]))
        decode_table.append(tuple(['-' * 90]))
        if i == 0:
            F_k = q_ensemble[alpha]
            G_k = p_ensemble[alpha]
        else:
            F_k = round(F_k + round(G_k * q_ensemble[alpha], accurateness), accurateness)
            G_k = round(G_k * p_ensemble[alpha], accurateness)
    return tuple(decode_table)


def _arithmetic_encode_algorythm(p_ensemble: dict, seq: list) -> (tuple, tuple, int, float, str):
    q_ensemble: dict = dict()
    q: float = 0.0
    for i, (alpha, p) in enumerate(p_ensemble.items()):
        q_ensemble[alpha] = q
        q = (round(q + p, accurateness))

    encode_table, q_seq_i, p_seq_i = _create_encode_table(p_ensemble, q_ensemble, seq)
    L: int = ceil(- log2(p_seq_i)) + 1
    X: float = round(q_seq_i + round(p_seq_i / 2, accurateness), accurateness)
    code_word = _float_to_bin(X)

    decode_table = create_decode_table(p_ensemble, q_ensemble, seq, code_word[0: L])

    return encode_table, decode_table, L, X, code_word


def arithmetic_coding(*, input_ensemble: dict, sequence: list) -> (tuple, tuple, int, float, str):
    print(input_ensemble)
    print(*sequence)
    print()
    encode_table, decode_table, L, X, code_word = _arithmetic_encode_algorythm(input_ensemble, sequence)
    return encode_table, decode_table, L, X, code_word
