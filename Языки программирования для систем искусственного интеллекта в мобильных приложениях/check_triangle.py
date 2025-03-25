import math

def check_triangle(a, b, c):
    """Проверяет существование треугольника"""
    return a + b > c and a + c > b and b + c > a

def triangle_type(a, b, c):
    """Определяет тип треугольника"""
    # Проверка существования треугольника
    if not check_triangle(a, b, c):
        return "Такого треугольника не существует!"

    # Сортировка сторон (c - гипотенуза для проверки углов)
    sides = sorted([a, b, c])
    a, b, c = sides

    # Проверка по длинам сторон
    if a == b == c:
        return "Равносторонний и остроугольный треугольник"
    elif a == b or b == c:
        side_type = "Равнобедренный"
    else:
        side_type = "Разносторонний"

    # Проверка по углам (теорема Пифагора)
    if math.isclose(c**2, a**2 + b**2):  # Прямоугольный
        angle_type = "Прямоугольный"
    elif c**2 > a**2 + b**2:  # Тупоугольный
        angle_type = "Тупоугольный"
    else:  # Остроугольный
        angle_type = "Остроугольный"

    return f"{side_type} и {angle_type} треугольник"

# Ввод данных
a = float(input("Введите длину стороны a: "))
b = float(input("Введите длину стороны b: "))
c = float(input("Введите длину стороны c: "))

# Вывод результата
print(triangle_type(a, b, c))
