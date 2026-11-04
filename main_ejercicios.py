"""
Soluciones de referencia (para el profesor).
Ejercicio 1: boletos de cine. Ejercicio 2: estacionamiento.
"""


# ---------------------------------------------------------------
# Ejercicio 1: boletos de cine
# ---------------------------------------------------------------
class Boleto:
    def __init__(self, cliente, funcion, precio_base=90):
        self.cliente = cliente
        self.funcion = funcion
        self.precio_base = precio_base

    def calcular_precio(self):
        return self.precio_base

    def ticket(self):
        return f"{self.cliente} - {self.funcion}: ${self.calcular_precio():,.2f}"


class BoletoEstudiante(Boleto):
    def __init__(self, cliente, funcion, descuento=0.3):
        super().__init__(cliente, funcion)
        self.descuento = descuento

    def calcular_precio(self):
        precio_normal = super().calcular_precio()
        return precio_normal - precio_normal * self.descuento


class BoletoCortesia(Boleto):
    def calcular_precio(self):
        return 0


# Reto: hereda de BoletoEstudiante y solo cambia el descuento
class BoletoTerceraEdad(BoletoEstudiante):
    def __init__(self, cliente, funcion):
        super().__init__(cliente, funcion, descuento=0.5)


# ---------------------------------------------------------------
# Ejercicio 2: estacionamiento
# ---------------------------------------------------------------
class Estancia:
    def __init__(self, placa, horas):
        # Reto: la validación vive en el padre y la heredan todas las hijas
        if horas <= 0:
            raise ValueError("Las horas deben ser mayores que cero")
        self.placa = placa
        self.horas = horas

    def cobrar(self):
        return self.horas * 20

    def ticket(self):
        return f"{self.placa} ({self.horas} h): ${self.cobrar():,.2f}"


class EstanciaPension(Estancia):
    def __init__(self, placa):
        super().__init__(placa, horas=24)

    def cobrar(self):
        return 250


class EstanciaNocturna(Estancia):
    def __init__(self, placa, horas, cargo_nocturno=50):
        super().__init__(placa, horas)
        self.cargo_nocturno = cargo_nocturno

    def cobrar(self):
        return super().cobrar() + self.cargo_nocturno


if __name__ == "__main__":
    print("Ejercicio 1")
    boletos = [
        Boleto("Andrea", "Sala 2, 18:00"),
        BoletoEstudiante("Bruno", "Sala 2, 18:00"),
        BoletoCortesia("Carla", "Sala 5, 20:30"),
    ]
    for boleto in boletos:
        print(boleto.ticket())
    print("Reto:", BoletoTerceraEdad("Diana", "Sala 1, 16:00").ticket())

    print("\nEjercicio 2")
    estancias = [
        Estancia("ABC-123", 3),
        EstanciaPension("XYZ-789"),
        EstanciaNocturna("JKL-456", 5),
    ]
    for estancia in estancias:
        print(estancia.ticket())
    try:
        Estancia("MNO-111", 0)
    except ValueError as error:
        print("Reto:", error)