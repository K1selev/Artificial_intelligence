import random

def choose_word():
    words = ['яблоко', 'победа', 'программирование', 'терминал', 'ноутбук', 'компьютер', 'разработка', 'питон', 'искусство', 'алгоритм']
    return random.choice(words)

def display_progress(word, discovered):
    return ' '.join([ch if ch in discovered else '_' for ch in word])

def play_game():
    word = choose_word()
    unique_letters = set(word)
    discovered_letters = set()
    user_health = 5
    computer_health = 5
    is_user_turn = True
    
    print("Добро пожаловать в игру! Угадайте слово, отгадывая буквы по очереди с компьютером.")
    print(display_progress(word, discovered_letters))
    
    while discovered_letters != unique_letters and user_health > 0 and computer_health > 0:
        if is_user_turn:
            guess = input('Введите букву: ').lower()
            if len(guess) != 1 or not guess.isalpha():
                print("Введите ОДНУ букву!")
                continue
        else:
            guess = random.choice([ch for ch in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя' if ch not in discovered_letters])
            print(f'Компьютер выбрал букву: {guess}')
        
        if guess in discovered_letters:
            print(f'Буква {guess} уже открыта, попробуйте другую.')
        elif guess in unique_letters:
            discovered_letters.add(guess)
            print(f'Буква {guess} есть в слове!')
        else:
            if is_user_turn:
                user_health -= 1
                print(f'Буквы {guess} нет в слове. Осталось жизней у игрока: {user_health}')
            else:
                computer_health -= 1
                print(f'Буквы {guess} нет в слове. Осталось жизней у компьютера: {computer_health}')
        
        print(display_progress(word, discovered_letters))
        is_user_turn = not is_user_turn
    
    if user_health == 0:
        print(f'Игрок проиграл! Компьютер победил. Загаданное слово было: {word}')
    elif computer_health == 0:
        print(f'Компьютер проиграл! Игрок победил. Загаданное слово было: {word}')
    else:
        winner = 'Игрок' if not is_user_turn else 'Компьютер'
        print(f'Поздравляем! {winner} угадал слово: {word}')

play_game()
