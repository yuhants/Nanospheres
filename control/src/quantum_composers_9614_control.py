import serial
import time

def write_and_receive(ser, command):
    ser.write(bytes(command, encoding='UTF-8'))
    response = ser.readline()

    return(response.decode('UTF-8'))

def set_pulse(port=r'COM9', baudrate='38400', channel=1, amp=5, width='0.0000002', period='0.3'):
    ser = serial.Serial(r'COM9', baudrate='38400', timeout=1)

    pulse_channel = f'PULSE{str(channel)}'
    _ = write_and_receive(ser, f':{pulse_channel}:STATE ON \r\n')
    _ = write_and_receive(ser, f':{pulse_channel}:OUTP:AMPL {amp} \r\n')
    _ = write_and_receive(ser, f':PULSE1:WIDT {width} \r\n')
    _ = write_and_receive(ser, f':PULSE0:PER {period} \r\n')

    _ = write_and_receive(ser, f':{pulse_channel}:POL NORM \r\n')
    _ = write_and_receive(ser, f':{pulse_channel}:DELAY 0 \r\n')

    _ = write_and_receive(ser, ':PULSE0:MODE NORM \r\n')
    _ = write_and_receive(ser, ':PULSE0:EXT:MODE DIS \r\n')

    ser.close()

def turn_on(port=r'COM9', baudrate='38400'):
    ser = serial.Serial(r'COM9', baudrate='38400', timeout=1)
    ser.write(b':PULSE0:STATE ON \r\n')
    ser.close()

def turn_off(port=r'COM9', baudrate='38400'):
    ser = serial.Serial(r'COM9', baudrate='38400', timeout=1)
    ser.write(b':PULSE0:STATE OFF \r\n')
    ser.close()

def main():
    set_pulse(channel=1, amp=10, width='0.0000002', period='0.3')
    turn_on()

    i = 0
    while i < 1000:
        try:
            time.sleep(1)
            i+=1
        except KeyboardInterrupt:
            break

    turn_off()

if __name__ == '__main__':
    main()