import random
import os
import time

# Счет
score_player = 0
score_bot = 0

# Уровень сложности (0 - бот глупый, 1 - бот играет идеально)
difficulty = float(input("Введите уровень сложности бота (от 0 до 1): "))

# Начальное сообщение
all_cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

print("Поиграем в 21? \nЕсли хотите играть, нажмите Enter, если хотите выйти, то нажмите Ctrl+C")
input()

while True:
    if score_player == 21:
        print("Больше карт не надо, у вас 21")
        print("Вы автоматически победили бота, так как у вас 21.")
        input("Нажмите Enter, чтобы закрыть окно."); break
    if score_player > 21:
        print("Вы проиграли, так как набрали больше 21")
        print("Попытайте свою удачу в другой раз.")
        input("Нажмите Enter, чтобы закрыть окно."); break

    yes_or_no = input("Будете ли вы брать карту? (y/n): ").strip().lower()
    os.system('cls' if os.name == 'nt' else 'clear')

    if yes_or_no == 'y':
        card = random.choice(all_cards)
        print(f"Вы взяли карту: {card}")
        score_player += card
        print(f"Сейчас у вас {score_player} очков")
    elif yes_or_no == 'n':
        print(f"У вас {score_player} очков.")
        print("Ход бота...")
        time.sleep(2)
        os.system('cls' if os.name == 'nt' else 'clear')

        while True:
            if score_bot < 15:
                print("Бот берет карту")
                card = random.choice(all_cards)
                print(f"Боту выпало {card} очков.")
                score_bot += card
                print(f"У бота {score_bot} очков.")
                time.sleep(2)
                os.system('cls' if os.name == 'nt' else 'clear')
            else:
                if random.random() > difficulty:
                    card = random.choice(all_cards)
                    print(f"Бот берет случайную карту: {card}")
                else:
                    card = min(21 - score_bot, max(all_cards)) if 21 - score_bot > 0 else 0
                    if card > 0:
                        print(f"Бот стратегически взял карту: {card}")
                score_bot += card
                print(f"У бота {score_bot} очков.")
                time.sleep(2)
                os.system('cls' if os.name == 'nt' else 'clear')
                
            if score_bot > 21:
                print(f"Бот проиграл. У него {score_bot} очков, а у вас {score_player}")
                input("Нажмите Enter, чтобы закрыть."); exit(0)
            elif score_bot > score_player:
                print(f"Бот победил. У него {score_bot} очков, у вас {score_player}")
                input("Нажмите Enter, чтобы закрыть."); exit(0)
            elif score_bot == score_player:
                print("Вы набрали равное количество очков. Ничья!")
                input("Нажмите Enter, чтобы закрыть."); exit(0)
