import json
from pymongo import MongoClient

class Entidad:
    def __init__(self):
        self.entidades = []
        self.client = None
        self.db = None

    def ver(self):
        return self.entidades

    def agregar(self, entidad):
        self.entidades.append(entidad)

    def transformar_json(self, ruta):
        with open(ruta, 'w') as file:
            json.dump(self.diccionario(), file, indent=2)

    def obtener_json(self, ruta):
        with open(ruta, 'r') as file:
            return json.load(file)

    def conectar_mongo(self, uri="mongodb://44.245.166.66:27017/", database_name="neocare"):
        self.client = MongoClient(uri)
        self.db = self.client[database_name]
        return "MongoDB"

    def enviar_mongo(self, jsonData):
        if self.db is not None:
            if jsonData:
                collection = self.db['prueba']
                for data_key, data_group in jsonData.items():
                    incubator_id = int(data_group.get("incubator", "0"))
                    values = {}
                    for sensor_code, sensor_data in data_group.items():
                        if sensor_code == "incubator" or sensor_code == "date":
                            continue
                        if isinstance(sensor_data, dict):
                            values[sensor_code] = {
                                "value": sensor_data["value"],
                                "date": sensor_data["date"]
                            }
                    collection.update_one(
                        {"incubator_id": incubator_id},
                        {"$push": {"values": values}},
                        upsert=True
                    )
                return f"Data sent to MongoDB successfully"
            return "No data to send"
        return "No database connection"

    @staticmethod
    def internet():
        try:
            client = MongoClient("mongodb://44.245.166.66:27017/")
            client.server_info()
            return True
        except:
            return False