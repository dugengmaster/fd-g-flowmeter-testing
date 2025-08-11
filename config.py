from dotenv import load_dotenv
import os

load_dotenv()


class ModbusConfig:
    """Modbus 連線設定"""

    HOST = "192.168.2.114"
    PORT = 502
    UNIT_ID = 1
    TIMEOUT = 5.0
    AUTO_OPEN = True
    AUTO_CLOSE = True


class AppConfig:
    """應用程式設定"""

    WAIT_TIME = 60  # seconds


class RegisterConfig:
    """暫存器組設定"""

    REGISTER_GROUPS = [
        {
            "start": 0,
            "end": 26,
            "float_indices": [4, 6, 8, 10, 12],
            "skip_indices": [5, 7, 9, 11, 13],
        },
        {"start": 30, "end": 95, "float_addresses": [32], "skip_addresses": [33]},
        {
            "start": 100,
            "end": 173,
            "float_relative_indices": [
                101,
                121,
                123,
                125,
                129,
                131,
                133,
                138,
                140,
                161,
                165,
                168,
                171,
            ],
            "skip_relative_indices": [
                102,
                122,
                124,
                126,
                130,
                132,
                134,
                139,
                141,
                162,
                166,
                169,
                172,
            ],
        },
        {"start": 175, "end": 205},
    ]


class MqttConfig:
    BROKER = os.getenv("BROKER")
    PORT = int(os.getenv("PORT", 1883))
    TOPIC = os.getenv("TOPIC")
    CLIENT_ID = os.getenv("CLIENT_ID")
    QOS = int(os.getenv("QOS", 0))
    RETAIN = os.getenv("RETAIN", "False").lower() == "true"
    KEEPALIVE = int(os.getenv("KEEPALIVE", 60))
    MQTT_USERNAME = os.getenv("MQTT_USERNAME")
    MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
