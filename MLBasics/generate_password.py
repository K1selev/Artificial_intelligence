import random
import string

def generate_password(length=12):
    """Функция генерации случайного пароля."""
    if length < 6:
        length = 6  # Минимальная длина пароля
    
    all_chars = (
        random.choices(string.ascii_uppercase, k=2) +  # Верхний регистр
        random.choices(string.ascii_lowercase, k=2) +  # Нижний регистр
        random.choices(string.digits, k=2) +  # Цифры
        random.choices(string.punctuation, k=2)  # Специальные символы
    )
    
    remaining_chars = length - len(all_chars)
    if remaining_chars > 0:
        all_chars += random.choices(string.ascii_letters + string.digits + string.punctuation, k=remaining_chars)
    
    random.shuffle(all_chars)
    return ''.join(all_chars)

def save_credentials(site, login, password, filename="passwords.txt"):
    """Функция сохранения учетных данных в файл."""
    with open(filename, "a", encoding="utf-8") as file:
        file.write(f"{site} | {login} | {password}\n")

def main():
    print("Добро пожаловать в менеджер паролей. Введите 'q' для выхода.")
    while True:
        site = input("Введите сайт (или 'q' для выхода): ")
        if site.lower() == 'q':
            break
        
        login = input("Введите логин: ")
        password = generate_password()
        print(f"Сгенерированный пароль: {password}")
        
        save_credentials(site, login, password)
        print("Данные сохранены!\n")

if __name__ == "__main__":
    main()
