import random
import sys
import msvcrt
import datetime

# Функции для работы с консолью
def get_key():
    """Считывает нажатую клавишу без нажатия Enter"""
    return msvcrt.getch().decode("utf-8").lower()

def clear_console():
    """Очищает консоль"""
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()

# Словарь эмодзи для отображения игровых объектов
EMOJI_MAP = {
    "#": "🟦",  # стена
    ".": "⚪",  # точка (еда)
    "P": "😋",  # пакман
    " ": "⬛",  # пустое пространство
    "G": "👻"   # призрак
}

# Шаблон игровой карты
RAW_MAP = [
    "############################",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#.####.#####.##.#####.####.#",
    "#..........................#",
    "#.####.##.########.##.####.#",
    "#......##....##....##......#",
    "######.#####.##.#####.######",
    "#..........................#",
    "#..........######..........#",
    "#.######...####....######..#",
    "#..........................#",
    "#.####.##.########.##.####.#",
    "#.####.##....##....##.####.#",
    "#......######.##.######....#",
    "#..........................#",
    "#.####.#####.##.#####.####.#",
    "#............##............#",
    "#............##............#",
    "############################",
]

# Инициализация игрового поля
field = [list(row) for row in RAW_MAP]
pacman_x, pacman_y = 1, 1  # Начальная позиция Pac-Man
field[pacman_x][pacman_y] = "P"

# Размещение призраков
ghosts = [(5, 5), (10, 10), (15, 15)]  # Начальные позиции призраков
for x, y in ghosts:
    field[x][y] = "G"

# Игровые переменные
score = 0  # Счет игрока
game_over = False  # Флаг окончания игры
total_points = sum(row.count(".") for row in field)  # Общее количество точек на карте

def print_field():
    """Отображает игровое поле и текущий счет"""
    clear_console()
    for row in field:
        print("".join(EMOJI_MAP[cell] for cell in row))
    print(f"Счет: {score} | Осталось точек: {total_points}")

def move_pacman(dx, dy):
    """Обрабатывает движение Pac-Man"""
    global pacman_x, pacman_y, score, game_over, total_points
    new_x, new_y = pacman_x + dx, pacman_y + dy
    
    # Проверка границ поля и препятствий
    if 0 <= new_x < len(field) and 0 <= new_y < len(field[0]):
        if field[new_x][new_y] == "#":  # Стена
            return
        if field[new_x][new_y] == ".":  # Точка
            score += 10
            total_points -= 1
        if field[new_x][new_y] == "G":  # Призрак
            game_over = True
            return
        
        # Обновление позиции Pac-Man
        field[pacman_x][pacman_y] = " "
        pacman_x, pacman_y = new_x, new_y
        field[pacman_x][pacman_y] = "P"

def move_ghosts():
    """Обрабатывает движение призраков"""
    global ghosts, game_over
    new_ghosts = []
    for x, y in ghosts:
        # Возможные направления движения
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        random.shuffle(directions)  # Случайный порядок направлений
        
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            # Проверка возможности хода
            if (0 <= new_x < len(field) and 
                0 <= new_y < len(field[0]) and 
                field[new_x][new_y] != "#" and
                field[new_x][new_y] != "G"):
                if field[new_x][new_y] == "P":  # Столкновение с Pac-Man
                    game_over = True
                    return
                field[x][y] = " "  # Очистка старой позиции
                field[new_x][new_y] = "G"  # Новая позиция призрака
                new_ghosts.append((new_x, new_y))
                break
        else:
            new_ghosts.append((x, y))  # Призрак остается на месте, если нет доступных ходов
    ghosts = new_ghosts

def save_result(player_name, score, result):
    """Сохраняет результаты игры в файл"""
    with open("results.txt", "a", encoding="utf-8") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        f.write(f"[{timestamp}] Игрок: {player_name} | Очки: {score} | Результат: {result}\n")

def main():
    """Основной игровой цикл"""
    global game_over
    print("Добро пожаловать в Pacman!")
    print("Управление: W (вверх), A (влево), S (вниз), D (вправо), Q (выход)")
    player_name = input("Введите ваше имя: ")
    
    while not game_over:
        print_field()
        key = get_key()
        
        # Обработка нажатий клавиш
        if key == "q":
            save_result(player_name, score, "Выход")
            break
        elif key == "w":
            move_pacman(-1, 0)
        elif key == "s":
            move_pacman(1, 0)
        elif key == "a":
            move_pacman(0, -1)
        elif key == "d":
            move_pacman(0, 1)
            
        move_ghosts()
        
        # Проверка условий окончания игры
        if total_points == 0:
            game_over = True
            save_result(player_name, score, "Победа")
            print_field()
            print("Поздравляем! Вы победили!")
        elif game_over:
            save_result(player_name, score, "Поражение")
            print_field()
            print("Игра окончена! Вы столкнулись с призраком!")

if __name__ == "__main__":
    main()