import random

def draw_board(board, size):
    print("-" * (size * 4 + 1))
    for i in range(size):
        print("|", end=" ")
        for j in range(size):
            print(board[i * size + j], end=" | ")
        print()
        print("-" * (size * 4 + 1))

def take_input(player_token, board, size):
    valid = False
    while not valid:
        player_answer = input(f"Куда поставим {player_token}? ")
        try:
            player_answer = int(player_answer)
        except:
            print("Некорректный ввод. Вы уверены, что ввели число?")
            continue
        if 1 <= player_answer <= size * size:
            if str(board[player_answer - 1]) not in "XO":
                board[player_answer - 1] = player_token
                valid = True
            else:
                print("Эта клетка уже занята!")
        else:
            print("Некорректный ввод. Введите число от 1 до", size * size)

def check_win(board, size):
    win_coord = []
    # Проверка горизонтальных и вертикальных линий
    for i in range(size):
        win_coord.append([i + j * size for j in range(size)])
        win_coord.append([i * size + j for j in range(size)])
    
    # Диагонали
    win_coord.append([i * (size + 1) for i in range(size)])
    win_coord.append([i * (size - 1) for i in range(1, size + 1)])

    for each in win_coord:
        if board[each[0]] == board[each[1]] == board[each[2]]:
            return board[each[0]]
    return False

def main():
    size = 5  # Размер поля 5x5 для двух игроков
    board = list(range(1, size * size + 1))
    counter = 0
    win = False

    while not win:
        draw_board(board, size)
        if counter % 2 == 0:
            take_input("X", board, size)
        else:
            take_input("O", board, size)
        counter += 1
        if counter > 4:
            tmp = check_win(board, size)
            if tmp:
                print(tmp, "выиграл!")
                win = True
                break
        if counter == size * size:
            print("Ничья!")
            break
    draw_board(board, size)
    input("Нажмите Enter для выхода!")

def game_with_computer_3x3():
    size = 3  # Поле 3x3 для игры с компьютером
    board = list(range(1, size * size + 1))
    counter = 0
    win = False

    while not win:
        draw_board(board, size)
        if counter % 2 == 0:
            take_input("X", board, size)  # Игрок X
        else:
            computer_move(board, size)  # Ход компьютера
        counter += 1
        if counter > 4:
            tmp = check_win(board, size)
            if tmp:
                print(tmp, "выиграл!")
                win = True
                break
        if counter == size * size:
            print("Ничья!")
            break
    draw_board(board, size)
    input("Нажмите Enter для выхода!")

def game_with_computer_5x5():
    size = 5  # Поле 5x5 для игры с компьютером
    board = list(range(1, size * size + 1))
    counter = 0
    win = False

    while not win:
        draw_board(board, size)
        if counter % 2 == 0:
            take_input("X", board, size)  # Игрок X
        else:
            computer_move(board, size)  # Ход компьютера
        counter += 1
        if counter > 4:
            tmp = check_win(board, size)
            if tmp:
                print(tmp, "выиграл!")
                win = True
                break
        if counter == size * size:
            print("Ничья!")
            break
    draw_board(board, size)
    input("Нажмите Enter для выхода!")

def computer_move(board, size):
    empty_cells = [i for i, x in enumerate(board) if str(x) not in "XO"]
    move = random.choice(empty_cells) + 1
    print(f"Компьютер ставит O в клетку {move}")
    board[move - 1] = "O"

def display_menu():
    print("Выберите режим игры:")
    print("1. Игра 5x5 для двух игроков")
    print("2. Игра 3x3 против компьютера")
    print("3. Игра 5x5 против компьютера")
    print("4. Выйти")

def main_menu():
    while True:
        display_menu()
        choice = input("Введите номер выбора: ")

        if choice == "1":
            print("\nВы выбрали игру 5x5 для двух игроков.\n")
            main()
        elif choice == "2":
            print("\nВы выбрали игру 3x3 против компьютера.\n")
            game_with_computer_3x3()
        elif choice == "3":
            print("\nВы выбрали игру 5x5 против компьютера.\n")
            game_with_computer_5x5()
        elif choice == "4":
            print("Выход из игры. До свидания!")
            break
        else:
            print("Некорректный ввод. Пожалуйста, выберите правильный номер.")

if __name__ == "__main__":
    main_menu()