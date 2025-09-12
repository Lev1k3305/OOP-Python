import random
import time

def get_difficulty():
    print(" Дело детектива Питона")
    print("Выберите уровень сложности:")
    print("1. Новичок (1-50, 8 попыток)")
    print("2. Детектив (1-100, 7 попыток)")
    print("3. Мастер-сыщик (1-200, 6 попыток)")
    while True:
        try:
            choice = int(input("Выберите сложность (1-3): "))
            if choice in [1, 2, 3]:
                return choice
            print("Введите число от 1 до 3!")
        except ValueError:
            print("Введите корректное число!")

def get_game_settings(difficulty):
    if difficulty == 1:
        return 50, 8, "Новичок"
    elif difficulty == 2:
        return 100, 7, "Детектив"
    else:
        return 200, 6, "Мастер-сыщик"

def get_hint(number, guess, max_range):
    hints = [
        lambda x, g: f"🔍 'Код {'больше' if x > g else 'меньше'}!' — {'утверждает свидетель' if x > g else 'шепчет информатор'}",
        lambda x, g: f"🔍 Чутьё детектива: 'Число {'чётное' if x % 2 == 0 else 'нечётное'}!'",
        lambda x, g: f"🔍 Свидетель сообщает: 'Число {'делится' if x % 3 == 0 else 'не делится'} на 3!'",
        lambda x, g: f"🔍 Информатор шепчет: 'Число {'кратное 5' if x % 5 == 0 else 'не кратное 5'}!'",
        lambda x, g: f"🕵 Найдена улика: 'Число {max_range} или меньше!'"
    ]
    return random.choice(hints)(number, guess)

def play_game(max_range, max_attempts, difficulty_name):
    number = random.randint(1, max_range)
    attempts = 0
    start_time = time.time()
    
    print(f"\n🕵 ДЕТЕКТИВ ДЖАВА ВЫХОДИТ НА СЛЕД 🕵")
    print("Злодей украл код от сейфа!")
    print(f"Это число от 1 до {max_range}.")
    print(f"У вас {max_attempts} попыток, чтобы раскрыть тайну...")
    
    while attempts < max_attempts:
        attempts += 1
        print(f"\nПопытка {attempts}/{max_attempts}")
        
        while True:
            try:
                guess = input("Введите вашу догадку: ")
                guess = int(guess)
                if 1 <= guess <= max_range:
                    break
                print(f"Число должно быть от 1 до {max_range}!")
            except ValueError:
                print("Введите корректное число!")
        
        if guess == number:
            end_time = time.time()
            print(f"🎉 Дело раскрыто! Детектив Джава взломал код за {attempts} попыток!")
            print(f"Время: {end_time - start_time:.2f} секунд")
            return True, attempts, end_time - start_time
        
        print(get_hint(number, guess, max_range))
        if attempts == max_attempts - 1:
            print("🕵 Подсказок больше нет! Последняя попытка!")
    
    print("💀 Злодей сбежал! Сейф остался заперт...")
    return False, attempts, time.time() - start_time

def main():
    games_played = 0
    games_won = 0
    total_attempts = 0
    total_time = 0
    
    while True:
        difficulty = get_difficulty()
        max_range, max_attempts, difficulty_name = get_game_settings(difficulty)
        won, attempts, game_time = play_game(max_range, max_attempts, difficulty_name)
        
        games_played += 1
        total_attempts += attempts
        total_time += game_time
        if won:
            games_won += 1
        
        print("\n📊 Статистика дела:")
        print(f"Игр сыграно: {games_played}")
        print(f"Процент успеха: {(games_won / games_played * 100):.1f}%")
        print(f"Среднее число попыток: {(total_attempts / games_played):.1f}")
        print(f"Среднее время: {(total_time / games_played):.2f} секунд")
        
        play_again = input("\nХотите взяться за новое дело? (y/n): ").lower()
        if play_again != 'y':
            print("🕵 Детектив Питон завершает расследование. Отличная работа, напарник!")
            break

if __name__ == "__main__":
    main()