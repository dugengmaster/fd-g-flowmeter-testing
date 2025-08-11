def parse_modbus_float(high_reg, low_reg, big_endian=True):
    first, second = (high_reg, low_reg) if big_endian else (low_reg, high_reg)
    return (second << 16) | first
