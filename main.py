from functools import reduce
from arithmetic_coding import arithmetic_coding


accurateness: int = 6  # Округдение до знака


def test_valid(*, input_ensemble: dict) -> bool:
    summary: float = reduce(lambda x, y: round(x + y, accurateness), input_ensemble.values())
    return abs(1.0 - summary) < 1e-10


def main():
    suffix: int = 1
    # Читаем файл
    file_input = open(f'./input/input_{suffix}.txt', 'r')
    # Создаём массив непустных строк из файла
    lines = file_input.read().splitlines()
    # Закрываем файл
    file_input.close()

    # Создаём пустой словарь
    ensemble: dict = dict()
    # Сжимаемая последовательность
    sequence = []
    # Добавляем ключ, значение в словарь
    for i, line in enumerate(lines):
        if i < len(lines) - 1:
            line = line.split(':')
            for word in line:
                word.replace(' ', '')
            key, value = line
            ensemble[key] = float(value)
        else:
            sequence = tuple(line.split())

    # Сумма вероятностей должна быть равна 1.0
    if test_valid(input_ensemble=ensemble):
        encode_table, decode_table, L, X, code_word = arithmetic_coding(input_ensemble=ensemble, sequence=sequence)
        # Записываем результат
        file_output = open(f'./output/output_{suffix}.txt', 'w')
        file_output.write('\n'.join([' '.join([str(x).ljust(10) for x in row]) for row in encode_table]))
        file_output.write('\n\n')
        file_output.write(f'L = {L}\n')
        file_output.write(f'X = {X}\n')
        file_output.write(f'C = {code_word}\n\n')
        file_output.write('\n'.join([' '.join([str(x).ljust(12) for x in row]) for row in decode_table]))
        file_output.close()
    else:
        raise ValueError('Неверный вход!')


if __name__ == '__main__':
    main()
