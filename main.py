import sys
import time
import smbus
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

i2c = smbus.SMBus(1)
sensor_address = 0x5c
cred = credentials.Certificate('./credentials/air-controller2-firebase-adminsdk-d3sed-4a407aafd0.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://air-controller2.firebaseio.com'
})
database = db.reference('')

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
        while True:
            # センサーは無操作により自動スリープするので起動させる処理を挟む
            wake_up_sensor(sensor_address)
            time.sleep(0.003)

            block = read_temperature_humidity(sensor_address)
            # 人間が理解しやすいよう数値変換
            humidity = float(block[2] << 8 | block[3]) / 10
            temperature = float(block[4] << 8 | block[5]) / 10

            print(f'humidity: {humidity}%  temperature: {temperature}%')
            # RealtimeDatabaseに保存
            database.update({
                'humidity': humidity,
                'temperature': temperature
            })

            time.sleep(60)
    except KeyboardInterrupt:
        sys.exit(0)
