import math

def calc(a, b, op):
    """Функция выполняет арифметические операции над двумя числами."""
    if op not in ['+', '-', '*', '/', '**', '%', 'sqrt']:
        return 'Пожалуйста, выберите корректный тип операции: +, -, *, /, **, %, sqrt'
    
    if op == '+':
        return f'{a} + {b} = {a + b}'
    elif op == '-':
        return f'{a} - {b} = {a - b}'
    elif op == '*':
        return f'{a} * {b} = {a * b}'
    elif op == '/':
        return f'{a} / {b} = {a / b}' if b != 0 else 'Ошибка: Деление на ноль'
    elif op == '**':
        return f'{a} ** {b} = {a ** b}'
    elif op == '%':
        return f'{b}% от {a} = {a * (b / 100)}'
    elif op == 'sqrt':
        return f'√{a} = {math.sqrt(a)}, √{b} = {math.sqrt(b)}'

def get_number(prompt):
    """Функция для безопасного ввода чисел."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Ошибка: Введите корректное число!")

def main():
    """Главная функция для ввода данных и выполнения операций."""
    a = get_number('Введите первое число: ')
    b = get_number('Введите второе число: ')
    
    while True:
        op = input('Выберите операцию (+, -, *, /, **, %, sqrt): ')
        if op in ['+', '-', '*', '/', '**', '%', 'sqrt']:
            break
        print("Ошибка: Некорректная операция, попробуйте снова!")
    
    print(calc(a, b, op))

if __name__ == '__main__':
    main()
