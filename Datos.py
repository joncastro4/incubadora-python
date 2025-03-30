from Entidad import Entidad
from Valores import Valores

class Datos(Entidad):
    def __init__(self):
        super().__init__()
        self.lecturas = []

    def agregar_lectura(self, valores):
        if isinstance(valores, Valores) and valores.sensores:
            self.lecturas.append(valores)

    def diccionario(self):
        return {
            f"data{idx}": lectura.diccionario()
            for idx, lectura in enumerate(self.lecturas, 1)
        }

    def json_a_objeto(self, json_data):
        for key in json_data:
            if key.startswith("data"):
                lectura_data = json_data[key]
                lectura = Valores.from_json(lectura_data)
                self.agregar_lectura(lectura)
        return self