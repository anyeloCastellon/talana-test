import re
from django.db import models
from datetime import date
import math

# Create your models here.


class VehicleType(models.Model):
    name = models.CharField(max_length=32)
    max_capacity = models.PositiveIntegerField()

    def __str__(self) -> str:
        return self.name


class Vehicle(models.Model):
    name = models.CharField(max_length=32)
    passengers = models.PositiveIntegerField()
    vehicle_type = models.ForeignKey(VehicleType, null=True, on_delete=models.SET_NULL)
    number_plate = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.name

    def can_start(self) -> bool:
        return self.vehicle_type.max_capacity >= self.passengers

    def get_distribution(self) -> list:
        residuo, cociente = math.modf(self.passengers/2)

        # distribución_de_asientos = []

        # for i in range(int(cociente)):
        #     distribución_de_asientos.append([True, True])
        
        distribución_de_asientos = [[True, True] for i in range(int(cociente))]

        if residuo > 0 and residuo < 1: distribución_de_asientos.append([True,False])

        return distribución_de_asientos


    def validate_number_plate(self, numero_patente):
        regex_validacion_patente = "[A-Z]{2}-[0-9]{2}-[0-9]{2}"
        compilacion_patente = re.compile(regex_validacion_patente)
        if not numero_patente: return False
        elif(re.search(compilacion_patente, numero_patente) and len(numero_patente) == 8): return True
        else: False


class Journey(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    start = models.DateField()
    end = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.vehicle.name} ({self.start} - {self.end})"

    def is_finished(self):
        return (self.end != None and self.end <= date.today())
