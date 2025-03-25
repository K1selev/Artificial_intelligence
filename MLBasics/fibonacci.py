def fib_sequence(n):
    """Генерация последовательности чисел Фибоначчи итеративным методом."""
    assert n > 0, "Число должно быть больше нуля"
    
    series = [1]
    while len(series) < n:
        if len(series) == 1:
            series.append(1)
        else:
            series.append(series[-1] + series[-2])
    
    return ', '.join(map(str, series))

def fib_recurse(n):
    """Рекурсивный алгоритм вычисления n-го числа Фибоначчи."""
    assert n > 0, "Число должно быть больше нуля"
    
    if n == 1 or n == 2:
        return 1
    return fib_recurse(n - 1) + fib_recurse(n - 2)

if __name__ == "__main__":
    while True:
        try:
            num = int(input("Сколько чисел Фибоначчи вывести? "))
            if num <= 0:
                raise ValueError("Число должно быть больше нуля.")
            break
        except ValueError as e:
            print(f"Ошибка: {e}. Попробуйте снова.")
    
    print("Итеративный метод:", fib_sequence(num))
    
    print("Рекурсивный метод (вывод отдельных значений):")
    for i in range(1, num + 1):
        print(f"F({i}) = {fib_recurse(i)}")
