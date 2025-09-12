import random

MAIN_INGREDIENTS: list[str] = ["курица", "говядина", "рыба", "тофу", "креветки"]
SIDES: list[str] = ["рис", "картофель", "паста", "киноа", "овощи"]
SAUCES: list[str] = ["томатный соус", "сливочный соус", "соевый соус", "барбекю"]
SPICES: list[str] = ["черный перец", "паприка", "базилик", "куркума", "чеснок"]
ADJECTIVES: list[str] = ["огненный", "нежный", "ароматный", "пикантный", "сочный"]
NOUNS: list[str] = ["шторм", "восторг", "сюрприз", "закат", "триумф"]

def generate_dish_name() -> str:
    adjective: str = random.choice(ADJECTIVES).capitalize()
    noun: str = random.choice(NOUNS)
    return f"{adjective}{noun}"

def generate_recipe():
    main_ingredient: str = random.choice(MAIN_INGREDIENTS)
    side: str = random.choice(SIDES)
    sauce: str = random.choice(SAUCES)
    spice: str = random.choice(SPICES)
    return main_ingredient, side, sauce, spice

def generate_full_recipe() -> str:
    dish_name: str = generate_dish_name()
    main_ingredient, side, sauce, spice = generate_recipe()

    ingredients: str = (
        f"-Ингредиенты:\n"
        f"-Основной Ингредиент: {main_ingredient}\n"
        f"-Гарнир: {side}\n"
        f"-Соус: {sauce}\n"
        f"-Специя: {spice}\n"
    )

    steps: list[str] = [
        f"1. Подготовьте {main_ingredient}: нарежьте на кусочки или оставьте целым по желанию",
        f"2. Приготовьте {side} согласно инструкции на упаковке.",
        f"3. Обжарьте {main_ingredient} на среднем огне до золотистой корочки.",
        f"4. Добавьте {spice} для аромата и перемешайте.",
        f"5. Полейте блюдо {sauce} и тушите 5-10 минут.",
        f"6. Подавайте {main_ingredient} с {side}, украсив свежей зеленью."
    ]

    selected_steps: list[str] = random.sample(steps, k=random.randint(4, 5))

    steps_text: str = "Шаги приготовления:\n" + "\n".join(selected_steps)

    recipe: str = (
        f"Название блюда: {dish_name}\n\n"
        f"{ingredients}\n"
        f"{steps_text}"
        f"\n\nПриятного аппетита!"
    )

    return recipe

if __name__ == "__main__":
    print(generate_full_recipe())


