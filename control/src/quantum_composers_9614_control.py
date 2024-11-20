import serial

def set_pulse(port=r'COM9', baudrate='38400', channel=1, amp=5, width_ns=200, period_ms=300):
    ser = serial.Serial(r'COM9', baudrate='38400', timeout=1)

    ## TODO: for channels other than channel 1
    ## set `PULSE1` below to `PULSE{n}`
    ser.write(b':PULSE1:STATE ON \r\n')

    ser.write(b':PULSE1:AMP 20 \r\n')
    ser.write(b':PULSE1:WIDTH 0.0000002 \r\n')
    ser.write(b':PULSE0:PER 0.3 \r\n')

    ser.write(b':PULSE1:POL NORM \r\n')
    ser.write(b':PULSE1:DELAY 0 \r\n')

    ser.write(b':PULSE0:MODE NORM \r\n')
    ser.write(b':PULSE0:EXT:MODE DIS \r\n')

    ser.close()

def turn_on(port=r'COM9', baudrate='38400'):
    ser = serial.Serial(r'COM9', baudrate='38400', timeout=1)
    ser.write(b':PULSE0:STATE ON \r\n')
    ser.close()

def turn_off(port=r'COM9', baudrate='38400'):
    ser = serial.Serial(r'COM9', baudrate='38400', timeout=1)
    ser.write(b':PULSE0:STATE OFF \r\n')
    ser.close()

# set_pulse()
# turn_on()
turn_off()

# response = ser.readline().decode('utf-8')
# print(response)

# ser.close()