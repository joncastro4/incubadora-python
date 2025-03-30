from Entidad import Entidad

class Valores(Entidad):
    def __init__(self, incubator=None, date=None):
        super().__init__()
        self.incubator = incubator
        self.date = date
        self.sensores = {}

    def agregar_sensor(self, codigo, valor, fecha):
        self.sensores[codigo] = {
            "value": valor,
            "date": fecha
        }

    def diccionario(self):
        return {
            "incubator": self.incubator,
            "date": self.date,
            **{codigo: datos for codigo, datos in self.sensores.items()}
        }

    @staticmethod
    def from_json(data):
        valores = Valores(
            incubator=data.get("incubator"),
            date=data.get("date")
        )
        for codigo, datos in data.items():
            if codigo not in ["incubator", "date"]:
                valores.agregar_sensor(codigo, datos["value"], datos["date"])
        return valores