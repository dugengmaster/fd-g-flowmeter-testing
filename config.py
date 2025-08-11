import json

with open("config.json", "r", encoding="utf-8") as f:
    _config = json.load(f)

class ModbusConfig:
    HOST = _config["ModbusConfig"]["HOST"]
    PORT = _config["ModbusConfig"]["PORT"]
    UNIT_ID = _config["ModbusConfig"]["UNIT_ID"]
    TIMEOUT = _config["ModbusConfig"]["TIMEOUT"]
    AUTO_OPEN = _config["ModbusConfig"]["AUTO_OPEN"]
    AUTO_CLOSE = _config["ModbusConfig"]["AUTO_CLOSE"]

class AppConfig:
    WAIT_TIME = _config["AppConfig"]["WAIT_TIME"]

class RegisterConfig:
    REGISTER_GROUPS = _config["RegisterConfig"]["REGISTER_GROUPS"]

class MqttConfig:
    BROKER = _config["MqttConfig"]["BROKER"]
    PORT = _config["MqttConfig"]["PORT"]
    TOPIC = _config["MqttConfig"]["TOPIC"]
    CLIENT_ID = _config["MqttConfig"]["CLIENT_ID"]
    QOS = _config["MqttConfig"]["QOS"]
    RETAIN = _config["MqttConfig"]["RETAIN"]
    KEEPALIVE = _config["MqttConfig"]["KEEPALIVE"]
    MQTT_USERNAME = _config["MqttConfig"]["MQTT_USERNAME"]
    MQTT_PASSWORD = _config["MqttConfig"]["MQTT_PASSWORD"]
