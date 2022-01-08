import sys
import time
import smbus

i2c = smbus.SMBus(1)
sensor_address = 0x5c

def wake_up_sensor(address):
    try:
        i2c.write_i2c_block_data(address, 0x00, [])
    except:
        pass

def read_temperature_humidity(address):
    i2c.write_i2c_block_data(address, 0x03, [0x00, 0x04])
    time.sleep(0.015)
    return i2c.read_i2c_block_data(address, 0, 6)

if __name__ == '__main__':
    try:
        while 1:
            wake_up_sensor(sensor_address)
            time.sleep(0.003)

            block = read_temperature_humidity(sensor_address)
            print(block)
            humidity = float(block[2] << 8 | block[3]) / 10
            temperature = float(block[4] << 8 | block[5]) / 10

            print(f'humidity: {humidity}%  temperature: {temperature}%')
            time.sleep(1)
    except KeyboardInterrupt:
        sys.exit(0)
