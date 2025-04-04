class Car:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year


    def honk(self, honks):
        self.honks = honks
        print(honks)

class Plane(Car):
    def __init__(self, make, model, year):
        super().__init__(make, model, year)



BMW = Car("BMW", "BIMMER", 1998)
print(BMW.make, BMW.year, BMW.model)
BMW.honk("BEEP BEEP")

fighterjet = Plane("AMerica", "FIGHTER", 2024)
print(fighterjet.make, fighterjet.model, fighterjet.year)