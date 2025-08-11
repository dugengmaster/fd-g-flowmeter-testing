import time
from config import AppConfig
from flowmeter_data_controller import FlowMeterDataController
from mqtt_client import MqttClient

if __name__ == "__main__":
    print(f"🚀 Starting Air Compressor MQTT data reader (every {AppConfig.WAIT_TIME} seconds)")
    print("Press Ctrl+C to stop")

    # 初始化空壓機模型
    compressor = FlowMeterDataController("test")
    
    # 初始化 MQTT 客戶端
    mqtt_client = MqttClient()
    
    # 連接到 MQTT Broker
    mqtt_connected = mqtt_client.connect()
    if not mqtt_connected:
        print("⚠️ MQTT connection failed, but will continue reading sensor data")

    try:
        while True:
            print("\n⏰ Reading sensor data...")
            
            # 讀取感測器數據
            success = compressor.read_sensor_data()
            
            if success:
                # 顯示 JSON 數據
                json_data = compressor.get_json(indent=2)
                print("Flow Meter Data:")
                print(json_data)
                
                # 發送到 MQTT（如果連線正常）
                if mqtt_client.is_alive():
                    mqtt_success = mqtt_client.publish_data(compressor.get_data())
                    if mqtt_success:
                        print("✅ Data sent to MQTT successfully")
                    else:
                        print("❌ Failed to send data to MQTT")
                else:
                    print("⚠️ MQTT disconnected, trying to reconnect...")
                    if mqtt_client.connect():
                        print("🔄 MQTT reconnected successfully")
                        mqtt_client.publish_data(compressor.get_data())
                    else:
                        print("❌ MQTT reconnection failed")
            else:
                print("❌ Failed to read sensor data")
            
            print(f"💤 Waiting {AppConfig.WAIT_TIME} seconds...")
            time.sleep(AppConfig.WAIT_TIME)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping data reader...")
        
        # 清理資源
        mqtt_client.disconnect()
        print("📴 MQTT disconnected")
        print("✋ Program terminated by user")