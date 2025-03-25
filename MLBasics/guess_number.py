import random

def guess_number():
    random_number = random.randint(1, 100)
    print('Компьютер и человек по очереди пытаются угадать число от 1 до 100.')
    
    user_guess = None
    computer_guess = None
    is_user_turn = True
    attempts = 0
    
    while True:
        attempts += 1
        
        if is_user_turn:
            try:
                user_guess = int(input('Ваш ход: '))
            except ValueError:
                print("Пожалуйста, введите число!")
                continue
            
            if user_guess < random_number:
                print(f'Больше, чем {user_guess}!')
            elif user_guess > random_number:
                print(f'Меньше, чем {user_guess}!')
            else:
                print(f'Поздравляем! Вы угадали число {random_number} за {attempts} попыток.')
                break
        else:
            computer_guess = random.randint(1, 100)
            print(f'Компьютер думает... {computer_guess}')
            
            if computer_guess < random_number:
                print(f'Больше, чем {computer_guess}!')
            elif computer_guess > random_number:
                print(f'Меньше, чем {computer_guess}!')
            else:
                print(f'Компьютер угадал число {random_number} за {attempts} попыток!')
                break
        
        is_user_turn = not is_user_turn

guess_number()
