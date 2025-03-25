import random

def get_computer_choice():
    options = ["Камень", "Бумага", "Ножницы", "Колодец"]
    return random.choice(options)

def determine_winner(player, computer):
    if player == computer:
        return "Ничья!"
    
    winning_cases = {
        "Камень": ["Ножницы"],
        "Бумага": ["Камень", "Колодец"],
        "Ножницы": ["Бумага"],
        "Колодец": ["Камень", "Ножницы"]
    }
    
    if computer in winning_cases[player]:
        return f"Ты выиграл! {player} побеждает {computer}."
    else:
        return f"Ты проиграл! {computer} побеждает {player}."

def main():
    print("Добро пожаловать в игру 'Камень, Ножницы, Бумага, Колодец'!")
    
    while True:
        player = input("Выберите Камень, Ножницы, Бумагу или Колодец (или 'q' для выхода): ").capitalize()
        if player == 'Q':
            print("Спасибо за игру!")
            break
        
        if player not in ["Камень", "Ножницы", "Бумага", "Колодец"]:
            print("Некорректный выбор. Попробуйте снова.")
            continue
        
        computer = get_computer_choice()
        print(f"Компьютер выбрал: {computer}")
        print(determine_winner(player, computer))
        print("---")

if __name__ == "__main__":
    main()
