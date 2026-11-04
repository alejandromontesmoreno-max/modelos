class Empleado:
    def __init__(self, nombre, salario_base):
        self.nombre = nombre
        self.salario_base = salario_base

    def calcular_pago(self):
        return self.salario_base

    def descripcion(self):
        return f"{self.nombre}: ${self.calcular_pago():,.2f}"


class EmpleadoPorHoras(Empleado):
    def __init__(self, nombre, horas, tarifa):
        super().__init__(nombre, salario_base=0)
        self.horas = horas
        self.tarifa = tarifa

    def calcular_pago(self):
        return self.horas * self.tarifa


class Vendedor(Empleado):
    def __init__(self, nombre, salario_base, ventas, comision=0.05):
        super().__init__(nombre, salario_base)
        self.ventas = ventas
        self.comision = comision

    def calcular_pago(self):
        return super().calcular_pago() + self.ventas * self.comision


empleados = [
    Empleado("Ana", 15000),
    EmpleadoPorHoras("Luis", 80, 120),
    Vendedor("Marta", 10000, 50000),
]
for empleado in empleados:
    print(empleado.descripcion())