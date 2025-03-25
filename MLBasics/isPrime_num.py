def isPrime(x):
    if x == 2:
        return True
    if x < 2 or x % 2 == 0:
        return False
    for i in range(3, int(x**0.5) + 1, 2):
        if x % i == 0:
            return False
    return True

def genPrime(currentPrime):
    newPrime = currentPrime + 1
    while not isPrime(newPrime):
        newPrime += 1
    return newPrime

while True:
    # Запрашиваем число у пользователя
    try:
        user_number = int(input("Введите число: "))
    except ValueError:
        print("Ошибка! Введите целое число.")
        continue

    # Проверяем, является ли оно простым
    if isPrime(user_number):
        print(f"Число {user_number} простое.")
    else:
        print(f"Число {user_number} не является простым.")
        nearest_prime = genPrime(user_number)
        print(f"Ближайшее простое число после {user_number}: {nearest_prime}")

    # Запрос на вывод следующего простого числа
    currentPrime = nearest_prime
    while True:
        answer = input('Показать следующее простое число? (Y/N) ').strip().lower()
        if answer.startswith('y'):
            currentPrime = genPrime(currentPrime)
            print(f"Следующее простое число: {currentPrime}")
        elif answer.startswith('n'):
            break
        else:
            print("Введите 'Y' для продолжения или 'N' для выхода.")
    
    # Запрос на повторный ввод числа
    repeat = input("Хотите проверить новое число? (Y/N) ").strip().lower()
    if repeat.startswith('n'):
        print("Программа завершена.")
        break
