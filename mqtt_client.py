import paho.mqtt.client as mqtt
import json
import time
from config import MqttConfig
from typing import Optional, Dict, Any


class MqttClient:
    def __init__(self):
        self.client = None
        self.is_connected = False
        self._setup_client()

    def _setup_client(self):
        self.client = mqtt.Client(client_id=MqttConfig.CLIENT_ID)

        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_publish = self._on_publish
        self.client.on_log = self._on_log

        if MqttConfig.MQTT_USERNAME and MqttConfig.MQTT_PASSWORD:
            self.client.username_pw_set(MqttConfig.MQTT_USERNAME, MqttConfig.MQTT_PASSWORD)

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.is_connected = True
            print(f"✅ Connected to MQTT Broker: {MqttConfig.BROKER}:{MqttConfig.PORT}")
        else:
            self.is_connected = False
            print(f"❌ Failed to connect to MQTT Broker, return code: {rc}")

    def _on_disconnect(self, client, userdata, rc):
        self.is_connected = False
        if rc != 0:
            print(f"⚠️ Unexpected disconnection from MQTT Broker")
        else:
            print("📴 Disconnected from MQTT Broker")

    def _on_publish(self, client, userdata, mid):
        print(f"📤 Message {mid} published successfully")

    def _on_log(self, client, userdata, level, buf):
        pass

    def connect(self) -> bool:
        """連接到 MQTT Broker"""
        try:
            print(
                f"🔗 Connecting to MQTT Broker: {MqttConfig.BROKER}:{MqttConfig.PORT}"
            )
            self.client.connect(
                MqttConfig.BROKER, MqttConfig.PORT, MqttConfig.KEEPALIVE
            )
            self.client.loop_start()

            # 等待連線完成
            timeout = 10  # 10 秒超時
            start_time = time.time()
            while not self.is_connected and (time.time() - start_time) < timeout:
                time.sleep(0.1)

            return self.is_connected

        except Exception as e:
            print(f"❌ MQTT connection error: {e}")
            return False

    def disconnect(self):
        """斷開 MQTT 連線"""
        if self.client:
            self.client.loop_stop()
            self.client.disconnect()

    def publish_data(self, data: Dict[Any, Any], topic: Optional[str] = None) -> bool:
        """發送數據到 MQTT"""
        if not self.is_connected:
            print("⚠️ MQTT not connected, attempting to reconnect...")
            if not self.connect():
                print("❌ Failed to reconnect to MQTT")
                return False

        try:
            # 使用預設 topic 或自訂 topic
            publish_topic = topic or MqttConfig.TOPIC

            # 轉換為 JSON
            json_data = json.dumps(data) if isinstance(data, dict) else data

            # 發送訊息
            result = self.client.publish(
                publish_topic, json_data, qos=MqttConfig.QOS, retain=MqttConfig.RETAIN
            )

            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                print(f"📡 Data sent to topic: {publish_topic}")
                return True
            else:
                print(f"❌ Failed to publish data, error code: {result.rc}")
                return False

        except Exception as e:
            print(f"❌ MQTT publish error: {e}")
            return False

    def publish_json(self, json_string: str, topic: Optional[str] = None) -> bool:
        """發送 JSON 字串到 MQTT"""
        if not self.is_connected:
            print("⚠️ MQTT not connected, attempting to reconnect...")
            if not self.connect():
                print("❌ Failed to reconnect to MQTT")
                return False

        try:
            publish_topic = topic or MqttConfig.TOPIC

            result = self.client.publish(
                publish_topic, json_string, qos=MqttConfig.QOS, retain=MqttConfig.RETAIN
            )

            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                print(f"📡 JSON data sent to topic: {publish_topic}")
                return True
            else:
                print(f"❌ Failed to publish JSON, error code: {result.rc}")
                return False

        except Exception as e:
            print(f"❌ MQTT publish error: {e}")
            return False

    def is_alive(self) -> bool:
        """檢查連線狀態"""
        return self.is_connected
