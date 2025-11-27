import sqlite3
import os
import getpass

DB_NAME = "resistance.db"


# ============================================
# 1. ИНИЦИАЛИЗАЦИЯ БАЗЫ
# ============================================

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS agents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codename TEXT UNIQUE,
        rank INTEGER CHECK(rank >= 1),
        skill TEXT,
        alive INTEGER DEFAULT 1
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS missions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        difficulty INTEGER CHECK(difficulty BETWEEN 1 AND 10),
        status TEXT CHECK(status IN ('planned','in progress','failed','success')),
        assigned_agent INTEGER,
        FOREIGN KEY(assigned_agent) REFERENCES agents(id) ON DELETE CASCADE
    );
    """)

    conn.commit()
    conn.close()


# ============================================
# 2. CRUD: AGENTS
# ============================================

def add_agent():
    codename = input("Позывной агента: ")
    rank = int(input("Ранг: "))
    skill = input("Навык: ")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO agents (codename, rank, skill) VALUES (?,?,?)",
                       (codename, rank, skill))
        conn.commit()
        print("Агент добавлен!")
    except sqlite3.IntegrityError:
        print("Ошибка: позывной не уникален!")
    conn.close()


def show_agents_sorted():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM agents ORDER BY rank DESC")
    for row in cursor.fetchall():
        print(row)
    conn.close()


def show_alive_above_rank():
    n = int(input("Введите N: "))
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM agents WHERE alive = 1 AND rank > ? ORDER BY rank DESC", (n,))
    for row in cursor.fetchall():
        print(row)
    conn.close()


def update_agent_rank():
    agent_id = int(input("ID агента для повышения ранга: "))
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE agents SET rank = rank + 1 WHERE id = ?", (agent_id,))
    conn.commit()
    print("Ранг повышен!")
    conn.close()


def kill_agent():
    agent_id = int(input("ID погибшего агента: "))
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE agents SET alive = 0 WHERE id = ?", (agent_id,))
    conn.commit()
    print("Агент помечен как погибший.")
    conn.close()


# ============================================
# 3. CRUD: MISSIONS
# ============================================

def agent_active_missions(agent_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM missions WHERE assigned_agent=? AND status='in progress'",
                   (agent_id,))
    result = cursor.fetchone()[0]
    conn.close()
    return result


def add_mission():
    title = input("Название миссии: ")
    difficulty = int(input("Сложность (1-10): "))
    agent_id = int(input("ID агента: "))

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT alive FROM agents WHERE id=?", (agent_id,))
    agent = cursor.fetchone()

    if not agent:
        print("Агент не найден.")
        return

    if agent[0] == 0:
        print("Нельзя назначать миссии погибшему агенту!")
        return

    if agent_active_missions(agent_id) >= 3:
        print("У агента уже 3 активные миссии!")
        return

    cursor.execute(
        "INSERT INTO missions (title, difficulty, status, assigned_agent) VALUES (?,?, 'planned',?)",
        (title, difficulty, agent_id)
    )
    conn.commit()
    print("Миссия добавлена!")
    conn.close()


def show_missions_with_agents():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT missions.id, missions.title, missions.status, agents.codename
    FROM missions
    JOIN agents ON missions.assigned_agent = agents.id
    """)
    for row in cursor.fetchall():
        print(row)
    conn.close()


def update_mission_status():
    mission_id = int(input("ID миссии: "))
    print("1 → in progress")
    print("2 → success")
    print("3 → failed")
    choice = input("> ")

    mapping = {"1": "in progress", "2": "success", "3": "failed"}

    if choice not in mapping:
        print("Ошибка выбора.")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE missions SET status=? WHERE id=?", (mapping[choice], mission_id))
    conn.commit()
    conn.close()
    print("Статус обновлён!")


def delete_failed_missions():
    lvl = int(input("Удалить проваленные миссии сложнее: "))
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM missions WHERE status='failed' AND difficulty > ?", (lvl,))
    conn.commit()
    print("Удалено.")
    conn.close()


# ============================================
# 4. АНАЛИТИКА
# ============================================

def missions_count_each_agent():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT agents.codename, COUNT(missions.id)
    FROM agents
    LEFT JOIN missions ON agents.id = missions.assigned_agent
    GROUP BY agents.id
    """)
    for row in cursor.fetchall():
        print(row)
    conn.close()


def agents_with_3_missions():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT codename
    FROM agents
    JOIN missions ON agents.id = missions.assigned_agent
    GROUP BY agents.id
    HAVING COUNT(missions.id) >= 3
    """)
    print(cursor.fetchall())
    conn.close()


def agent_best_success_rate():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT agents.codename,
           SUM(CASE WHEN missions.status='success' THEN 1 ELSE 0 END) * 1.0 /
           COUNT(missions.id) AS success_rate
    FROM agents
    JOIN missions ON agents.id = missions.assigned_agent
    GROUP BY agents.id
    ORDER BY success_rate DESC
    LIMIT 1
    """)
    print(cursor.fetchone())
    conn.close()


def analytics_report():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT 
        agents.codename,
        COUNT(missions.id) AS total,
        SUM(CASE WHEN missions.status='success' THEN 1 ELSE 0 END) AS success,
        SUM(CASE WHEN missions.status='failed' THEN 1 ELSE 0 END) AS failed,
        (SUM(CASE WHEN missions.status='success' THEN 1 ELSE 0 END) * 1.0 /
        COUNT(missions.id)) AS rate
    FROM agents
    LEFT JOIN missions ON agents.id = missions.assigned_agent
    GROUP BY agents.id
    """)
    for row in cursor.fetchall():
        print(row)
    conn.close()


def agents_more_failed_than_success():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT codename
    FROM agents
    JOIN missions ON agents.id = missions.assigned_agent
    GROUP BY agents.id
    HAVING 
        SUM(CASE WHEN missions.status='failed' THEN 1 ELSE 0 END) >
        SUM(CASE WHEN missions.status='success' THEN 1 ELSE 0 END)
    """)
    print(cursor.fetchall())
    conn.close()


def agents_without_missions():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT codename 
    FROM agents 
    LEFT JOIN missions ON agents.id = missions.assigned_agent
    WHERE missions.id IS NULL
    """)
    print(cursor.fetchall())
    conn.close()


# ============================================
# 5. РОЛИ И МЕНЮ
# ============================================

def operator_menu():
    while True:
        print("\n=== ОПЕРАТОР ===")
        print("1. Добавить миссию")
        print("2. Изменить статус миссии")
        print("3. Показать агентов")
        print("4. Показать миссии с агентами")
        print("0. Выход")

        choice = input("> ")

        if choice == "1":
            add_mission()
        elif choice == "2":
            update_mission_status()
        elif choice == "3":
            show_agents_sorted()
        elif choice == "4":
            show_missions_with_agents()
        elif choice == "0":
            break


def admin_menu():
    while True:
        print("\n=== АДМИН ===")
        print("1. Добавить агента")
        print("2. Удалить (пометить погибшим)")
        print("3. Повысить ранг")
        print("4. Аналитика")
        print("0. Выход")

        choice = input("> ")

        if choice == "1":
            add_agent()
        elif choice == "2":
            kill_agent()
        elif choice == "3":
            update_agent_rank()
        elif choice == "4":
            analytics_menu()
        elif choice == "0":
            break


def analytics_menu():
    while True:
        print("\n=== АНАЛИТИКА ===")
        print("1. Количество миссий у каждого агента")
        print("2. Агенты с ≥ 3 миссий")
        print("3. Агент с макс. процентом успеха")
        print("4. Отчёт")
        print("5. У кого провалов больше чем успехов")
        print("6. Агенты без миссий")
        print("0. Назад")

        choice = input("> ")

        if choice == "1":
            missions_count_each_agent()
        elif choice == "2":
            agents_with_3_missions()
        elif choice == "3":
            agent_best_success_rate()
        elif choice == "4":
            analytics_report()
        elif choice == "5":
            agents_more_failed_than_success()
        elif choice == "6":
            agents_without_missions()
        elif choice == "0":
            break


# ============================================
# 6. ВХОД В СИСТЕМУ
# ============================================

def main():
    init_db()

    print("Введите роль (admin/operator):")
    role = input("> ").strip().lower()

    if role == "admin":
        admin_menu()
    elif role == "operator":
        operator_menu()
    else:
        print("Неизвестная роль.")


if __name__ == "__main__":
    main()
