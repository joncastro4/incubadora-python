import serial
import json
from datetime import datetime
import time
from Valores import Valores

class SerialReader:
    def __init__(self, puerto="COM3", baudrate=115200):
        self.valores = None
        self.sensores_requeridos = set()  # Almacenará las claves de Sensores.json
        
        # Cargar las claves de los sensores desde el JSON
        try:
            with open('Sensores.json', 'r') as f:
                sensores = json.load(f)
                for sensor in sensores:
                    clave = sensor.get('clave')
                    if clave:
                        self.sensores_requeridos.add(clave)
        except FileNotFoundError:
            print("Error: No se encontró el archivo Sensores.json")
        except json.JSONDecodeError:
            print("Error: Sensores.json tiene un formato inválido")
        
        # Inicializar conexión serial
        try:
            self.serial = serial.Serial(puerto, baudrate, timeout=1)
            time.sleep(2)
        except serial.SerialException:
            self.serial = None

    def leer_linea(self):
        if self.serial is None:
            return None
            
        linea = self.serial.readline().decode("utf-8", errors="ignore").strip()
        if linea and ":" in linea:
            protocolo, valor = linea.split(":", 1)
            return protocolo, valor
        return None

    def obtener_lectura_completa(self):
        lectura = Valores()
        sensores_leidos = set()
        timeout = time.time() + 5

        while time.time() < timeout and sensores_leidos != self.sensores_requeridos:
            dato = self.leer_linea()
            if dato:
                protocolo, valor = dato
                codigo = protocolo[:3]
                incubadora = protocolo[3:].lstrip('0') or "1"
                fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                if codigo in self.sensores_requeridos:
                    lectura.incubator = incubadora
                    lectura.date = fecha
                    lectura.agregar_sensor(codigo, valor, fecha)
                    sensores_leidos.add(codigo)

        return lectura if sensores_leidos else None

    def request_data(self):
        if self.serial:
            self.serial.write(b"GET_DATA\n")
            return self.obtener_lectura_completa()