from abc import ABC
from homework_02.exceptions import LowFuelError, NotEnoughFuel


class Vehicle(ABC):
    type_name = None

    def __init__(self, weight, fuel, fuel_consumption):
        self.weight = weight
        self.started = False
        self.fuel = fuel
        self.fuel_consumption = fuel_consumption

    def start(self):
        if self.started is True:
            print('Vehicle is started')
        else:
            if self.fuel > 0:
                self.started = True
                return
            raise LowFuelError('В баке нет топлива!')

    # def move(self, distance):
    #     needed_fuel = distance * self.fuel_consumption  # если расход на 1 км, то для определения количества топлива нужно
    #     # дистанцию умножить на расход
    #     if self.fuel - needed_fuel >= 0:
    #         raise NotEnoughFuel('Топлива не достаточно для преодоления переданной дистанции!')
    #     self.fuel -= needed_fuel

    def move(self, distance):
        max_distance = self.fuel / self.fuel_consumption
        if distance <= max_distance:
            self.fuel = self.fuel - distance * self.fuel_consumption
            return
        raise NotEnoughFuel('Топлива не достаточно для преодоления переданной дистанции!')