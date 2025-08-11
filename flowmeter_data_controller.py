from datetime import datetime, timezone
from pyModbusTCP.client import ModbusClient
from utils import parse_modbus_float
from config import ModbusConfig, RegisterConfig
import json

class FlowMeterDataController:
    def __init__(self, model_name: str = "test"):
        self.model_name = model_name
        self.container = self._create_container()
        self._client = None
    
    def _create_container(self) -> dict:
        return {
            "model": self.model_name,
            "timestamp": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            "data": {}
        }
    
    def refresh_timestamp(self):
        self.container["timestamp"] = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
    
    def clear_data(self):
        self.container["data"] = {}
    
    def _read_register_group(self, group_config: dict, key: int) -> tuple[bool, int]:
        start_addr = group_config["start"]
        end_addr = group_config["end"]
        
        result = self._client.read_holding_registers(start_addr, end_addr - start_addr + 1)
        
        if result is None:
            print(f"Failed to read registers {start_addr}-{end_addr}")
            return False, key
        
        for i in range(len(result)):
            addr = start_addr + i
            
            # 處理 float 數據
            if self._should_process_as_float(group_config, i, addr):
                self.container["data"][f"{key}"] = parse_modbus_float(result[i], result[i + 1])
                key += 2
                continue
            
            # 跳過指定的地址
            if self._should_skip(group_config, i, addr):
                continue
                
            # 處理一般數據
            self.container["data"][f"{key}"] = result[i]
            key += 1
            
        return True, key
    
    def _should_process_as_float(self, config: dict, i: int, addr: int) -> bool:
        if "float_indices" in config and i in config["float_indices"]:
            return True
        if "float_addresses" in config and addr in config["float_addresses"]:
            return True
        if "float_relative_indices" in config and i in config["float_relative_indices"]:
            return True
        return False
    
    def _should_skip(self, config: dict, i: int, addr: int) -> bool:
        if "skip_indices" in config and i in config["skip_indices"]:
            return True
        if "skip_addresses" in config and addr in config["skip_addresses"]:
            return True
        if "skip_relative_indices" in config and i in config["skip_relative_indices"]:
            return True
        return False

    def read_sensor_data(self) -> bool:
        self._client = ModbusClient(
            host=ModbusConfig.HOST,
            port=ModbusConfig.PORT,
            unit_id=ModbusConfig.UNIT_ID,
            auto_open=ModbusConfig.AUTO_OPEN,
            auto_close=ModbusConfig.AUTO_CLOSE,
            timeout=ModbusConfig.TIMEOUT,
        )

        try:
            # 清空舊數據並更新時間戳記
            self.clear_data()
            self.refresh_timestamp()
            
            key = 0
            # 循環讀取所有暫存器組
            for group in RegisterConfig.REGISTER_GROUPS:
                success, key = self._read_register_group(group, key)
                if not success:
                    return False
                # 更新 key 為下一組的起始值
                key = group["end"] + 1 if group["start"] != 0 else key

            return True

        except Exception as e:
            error_message = f"Error reading Modbus registers: {e}"
            self.container["data"]["error"] = error_message
            return False
        finally:
            if self._client:
                self._client.close()
    
    def get_data(self) -> dict:
        return self.container
    
    def get_json(self, indent: int = None) -> str:
        return json.dumps(self.container, indent=indent)