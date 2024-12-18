import serial

def start(port=r'COM7', baudrate='9600'):
    ser = serial.Serial(port, baudrate, timeout=1)
    ser.write(bytes.fromhex("02 80 30 30 30 31 31 03 42 33"))

    response = ser.readline()
    print(response)

def read_pressure(port=r'COM7', baudrate='9600'):
    ser = serial.Serial(port, baudrate, timeout=1)
    ser.write(bytes.fromhex("02 80 32 32 34 30 03 38 37"))

    response = ser.readline()
    pressure_str = response[6:13].decode('UTF-8')

    ser.close()

    return float(pressure_str)

def calculate_xor_checksum(data):
    """Calculates the XOR checksum for a given bytearray."""
    checksum = 0
    for byte in data:
        checksum ^= byte
    return checksum

def main():
    # start()
    pressure = read_pressure()
    print(f'Current pressure: {pressure} mbar')

    # data = bytearray([0x80, 0x30, 0x30, 0x30, 0x31, 0x31, 0x03])
    # checksum = calculate_xor_checksum(data)
    # print(f"Checksum: 0x{checksum:02X}")

if __name__=="__main__":
    main()

