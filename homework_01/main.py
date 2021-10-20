"""
Домашнее задание №1
Функции и структуры данных
"""


def power_numbers():
    square_list = []
    for i in Numbers:
        square_list.append(i ** 2)
    print("Square of numbers: ", square_list)


# filter types
ODD = "odd"
EVEN = "even"
PRIME = "prime"


def filter_numbers(Numbers, filter_types):
    
    list = []

    if filter_types == ODD:
        for i in Numbers:
            if i % 2 != 0:
                list.append(i)
        print("Odd numbers: ", list)

    elif filter_types == EVEN:
        for i in Numbers:
            if i % 2 == 0:
                list.append(i)

        print("Even numbers: ", list)

    elif filter_types == PRIME:
        for i in Numbers:
            k = 0
            for j in range(2, i + 1):
                if i % j == 0:
                    k += 1
            if k <= 1:
                list.append(i)
        print("Prime numbers: ", list)

    """
    функция, которая на вход принимает список из целых чисел,
    и возвращает только чётные/нечётные/простые числа
    (выбор производится передачей дополнительного аргумента)

    >>> filter_numbers([1, 2, 3], ODD)
    <<< [1, 3]
    >>> filter_numbers([2, 3, 4, 5], EVEN)
    <<< [2, 4]
    """
    
if __name__ == '__main__':
    numbers = (1, 2, 5, 7,)
    power_numbers(numbers)

    numbs1 = [1, 2, 3]
    filter_types = ODD
    filter_numbers(numbs1, filter_types)
    numbs2 = [2, 1, 3, 5, 4]
    filter_types = EVEN
    filter_numbers(numbs2, filter_types)
    filter_types = PRIME
    numbs3 = [3, 5, 6, 8, 13, 25]
    filter_numbers(numbs3, filter_types)
