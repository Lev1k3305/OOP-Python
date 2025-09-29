# 1. Введение в ООП и классы
class Car:
    """Класс автомобиля"""
    wheels = 4  # Атрибут класса
    total_cars = 0
    
    def __init__(self, brand, model, year):
        self.brand = brand
        self.model = model
        self.year = year
        self.is_running = False
        Car.total_cars += 1

# Создание объектов
car1 = Car("Toyota", "Camry", 2020)
car2 = Car("BMW", "X5", 2019)

# 2. Конструкторы и self
class Person:
    def __init__(self, name, age, city="Неизвестно"):
        self.name = name
        self.age = age
        self.city = city
    
    @classmethod
    def from_age(cls, name, age):
        from datetime import datetime
        birth_year = datetime.now().year - age
        return cls(name, birth_year, "Неизвестно")

# 3. Методы и поля
class BankAccount:
    total_accounts = 0
    bank_name = "Мой Банк"
    
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance
        BankAccount.total_accounts += 1
    
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return True
        return False
    
    @classmethod
    def get_total_accounts(cls):
        return cls.total_accounts
    
    @staticmethod
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True

# 4. Инкапсуляция
class BankAccountEncapsulated:
    def __init__(self, owner, initial_balance=0):
        self.owner = owner
        self.__balance = initial_balance
    
    @property
    def balance(self):
        return self.__balance
    
    def deposit(self, amount, pin):
        if pin == "1234":  # Упрощенная проверка PIN
            self.__balance += amount
            return f"Пополнено: {amount}"
        raise ValueError("Неверный PIN")

# 5. Наследование
class Animal:
    def __init__(self, name, species):
        self.name = name
        self.species = species
    
    def make_sound(self):
        return f"{self.name} издает звук"

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name, "Собака")
        self.breed = breed
    
    def make_sound(self):
        return f"{self.name} гавкает: Гав-гав!"

# 6. Полиморфизм
class Shape:
    def area(self):
        pass

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        import math
        return math.pi * self.radius ** 2

# 7. Абстракция
from abc import ABC, abstractmethod
class AnimalABC(ABC):
    @abstractmethod
    def make_sound(self):
        pass

class Cat(AnimalABC):
    def __init__(self, name):
        self.name = name
    
    def make_sound(self):
        return f"{self.name} мяукает: Мяу!"

# 8. Специальные методы
class Book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages
    
    def __str__(self):
        return f'"{self.title}" by {self.author}'
    
    def __len__(self):
        return self.pages

# 9. Декораторы в классах
def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton
class Database:
    def __init__(self, connection_string="sqlite://memory"):
        self.connection_string = connection_string

# Демонстрация
if __name__ == "__main__":
    # Классы и объекты
    print(f"Car 1: {car1.brand} {car1.model}")  # Toyota Camry
    print(f"Total cars: {Car.total_cars}")  # 2
    
    # Конструкторы
    person = Person.from_age("Боб", 25)
    print(f"Person: {person.name}, Age: {person.age}")
    
    # Методы
    account = BankAccount("Алиса", 1000)
    account.deposit(500)
    print(f"Balance: {account.balance}")  # 1500
    print(f"Total accounts: {BankAccount.get_total_accounts()}")  # 1
    
    # Инкапсуляция
    enc_account = BankAccountEncapsulated("Боб", 1000)
    print(enc_account.deposit(500, "1234"))  # Пополнено: 500
    
    # Наследование
    dog = Dog("Рекс", "Лабрадор")
    print(dog.make_sound())  # Рекс гавкает: Гав-гав!
    
    # Полиморфизм
    circle = Circle(5)
    print(f"Circle area: {circle.area():.2f}")  # 78.54
    
    # Абстракция
    cat = Cat("Мурзик")
    print(cat.make_sound())  # Мурзик мяукает: Мяу!
    
    # Специальные методы
    book = Book("1984", "George Orwell", 328)
    print(str(book))  # "1984" by George Orwell
    print(f"Pages: {len(book)}")  # 328
    
    # Декораторы
    db1 = Database()
    db2 = Database()
    print(f"Same database instance: {db1 is db2}")  # True