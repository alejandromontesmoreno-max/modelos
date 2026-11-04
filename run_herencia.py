class Envio:
    def __init__(self, destinatario, peso_kg):
        self.destinatario = destinatario
        self.peso_kg = peso_kg

    def calcular_costo(self):
        return 100 + self.peso_kg * 20

    def resumen(self):
        return f"{self.destinatario} ({self.peso_kg} kg): ${self.calcular_costo():,.2f}"


class EnvioSobre(Envio):
    def __init__(self, destinatario):
        super().__init__(destinatario, peso_kg=0.5)

    def calcular_costo(self):
        return 80


class EnvioExpress(Envio):
    def __init__(self, destinatario, peso_kg, recargo=0.6):
        super().__init__(destinatario, peso_kg)
        self.recargo = recargo

    def calcular_costo(self):
        costo_normal = super().calcular_costo()
        return costo_normal + costo_normal * self.recargo


envios = [
    Envio("Carlos", 3),
    EnvioSobre("Lucía"),
    EnvioExpress("Pedro", 2),
]
for envio in envios:
    print(envio.resumen())