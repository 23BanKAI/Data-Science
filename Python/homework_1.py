class Animal:
    def __init__(self, name, sound):
        self.name = name
        self.sound = sound

    def makesound(self):
        print(f"{self.name} говорит {self.sound}")


class Cat(Animal):
    def __init__(self, name, sound, color):
        super().__init__(name, sound)
        self.color = color

    def makesound(self):
        print(f"Кот {self.name} говорит: {self.sound}")



class Dog(Animal):
    def __init__(self, name, sound, color):
        super().__init__(name, sound)
        self.color = color

    def makesound(self):
        print(f"Собака {self.name} говорит: {self.sound}")


cat = Cat(name="Маркиз", sound="мяу", color="серый")
dog = Dog(name="Рей", sound="гав", color="коричневый")

cat.makesound()
dog.makesound()
