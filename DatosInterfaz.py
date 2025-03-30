from Datos import Datos
import json
import os
from SerialReader import SerialReader
from Entidad import Entidad
import pusher
from time import sleep

class DatosInterfaz():
    def __init__(self, datos=None):
        self.datos = datos if datos else Datos()
        self.datos_pendientes = Datos()
        
        if os.path.exists("Datos.json"):
            self.datos = self.cargar_datos("Datos.json")
        if os.path.exists("DatosPendientes.json"):
            self.datos_pendientes = self.cargar_datos("DatosPendientes.json")

    def cargar_datos(self, archivo):
        datos = Datos()
        with open(archivo, 'r') as f:
            json_data = json.load(f)
            datos.json_a_objeto(json_data)
        return datos

    def insertar(self):
        sr = SerialReader()
        nueva_lectura = sr.request_data()
        
        if nueva_lectura and nueva_lectura.sensores:
            self.datos.agregar_lectura(nueva_lectura)
            self.datos_pendientes.agregar_lectura(nueva_lectura)
            self.guardar()

    def guardar(self):
        with open("Datos.json", 'w') as f:
            json.dump(self.datos.diccionario(), f, indent=2)
            
        if self._hay_conexion():
            self._enviar_pendientes()
        else:
            with open("DatosPendientes.json", 'w') as f:
                json.dump(self.datos_pendientes.diccionario(), f, indent=2)

    def _hay_conexion(self):
        try:
            return Entidad.internet()
        except:
            return False

    def _enviar_pendientes(self):
        entidad = Entidad()
        entidad.conectar_mongo(uri="mongodb://44.245.166.66:27017/", database_name="neocare")
        
        pendientes_dict = self.datos_pendientes.diccionario()
        resultado = entidad.enviar_mongo(pendientes_dict)
        
        if resultado == "Data sent to MongoDB successfully":
            self.datos_pendientes = Datos()
            
            pusher_client = pusher.Pusher(
                app_id='1966859',
                key='6943e97f10680d2f0922',
                secret='2c24a7922e00cfaa7104',
                cluster='us2',
                ssl=True
            )

            pusher_client.trigger('my-channel', 'my-event', {'message': 'datos'})
            
            if os.path.exists("DatosPendientes.json"):
                os.remove("DatosPendientes.json")

if __name__ == "__main__":
    di = DatosInterfaz() 
    while True:
        di.insertar()
        sleep(10)