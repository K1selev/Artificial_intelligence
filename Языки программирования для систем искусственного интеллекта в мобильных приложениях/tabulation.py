import numpy as np

def f(x):
    """Функция f(x) = x^2 - 2x + 1"""
    return x**2 - 2*x + 1

# Ввод параметров
A = float(input("Введите начало интервала A: "))
B = float(input("Введите конец интервала B: "))
H = float(input("Введите шаг H: "))

# Проверка корректности ввода
if H <= 0:
    print("Ошибка: Шаг H должен быть положительным числом.")
elif A > B:
    print("Ошибка: Начало интервала A должно быть меньше конца интервала B.")
else:
    # Заголовок таблицы
    print("\nТаблица значений функции f(x) = x^2 - 2x + 1:")
    print("+-----------+------------+")
    print("|     x     |    f(x)    |")
    print("+-----------+------------+")

    # Вычисление и вывод значений
    x = A
    while x <= B:
        print(f"| {x:^9.3f} | {f(x):^10.3f} |")
        x += H
    
    print("+-----------+------------+")
