#!/usr/bin/env python3
# coding: utf-8

################################################################################
# BLE Logger for Rohm SensorMedal-EVK-002
# Raspberry Piを使って、センサメダルのセンサ情報をAWS IoT Coreに通知します
#
#                                               Copyright (c) 2019 mametarou963
################################################################################

#【インストール方法】
#   bluepy (Bluetooth LE interface for Python)をインストールしてください
#       sudo pip3 install bluepy
#
#   pip3 がインストールされていない場合は、先に下記を実行
#       sudo apt-get update
#       sudo apt-get install python-pip libglib2.0-dev
#
#	確認方法
#		sudo pip3 show bluepy

#【参考文献】
#   本プログラムを作成するにあたり下記を参考にしました
#   BLE Logger for Rohm SensorMedal-EVK-002

SCAN_INTERVAL_SEC = 3 # 動作間隔
# SEND_INTERVAL_SEC = 300 # AWS送信間隔

CLIENT_ID = "test_client_id"
PORT = 8883

ROOT_CA = "./cert/root_ca.pem"
PRIVATE_KEY = "./cert/private.pem.key"
CERTIFICATE = "./cert/certificate.pem.crt"

from bluepy import btle
from sys import argv
import getpass
from time import sleep
import json
from collections import OrderedDict
import pprint
import SensorMedal2

# for AWS
import time
import json
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import datetime
from decimal import Decimal , ROUND_HALF_UP, ROUND_HALF_EVEN


def decimalRound(floatNumber):
    return Decimal(floatNumber).quantize(Decimal('0.01'),rounding=ROUND_HALF_EVEN)

# 設定の読み込み
with open("config.json","r") as f:
    config = json.load(f)
    sensorMedal2Address = config['SensorMedal2']['Address']
    ENDPOINT = config['AWS']['Endpoint']
    TOPIC = config['AWS']['Topic']
    SEND_INTERVAL_SEC = config['AWS']['SendIntervalSec'] # AWS送信間隔
# bluetoothのscan
scanner = btle.Scanner()
# AWSの接続
client = AWSIoTMQTTClient(CLIENT_ID)
client.configureEndpoint(ENDPOINT, PORT)
client.configureCredentials(ROOT_CA, PRIVATE_KEY, CERTIFICATE)

client.configureAutoReconnectBackoffTime(1, 32, 20)
client.configureOfflinePublishQueueing(-1)
client.configureDrainingFrequency(2)
client.configureConnectDisconnectTimeout(10)
client.configureMQTTOperationTimeout(5)

client.connect()
while True:
    # BLE受信処理
    try:
        devices = scanner.scan(SCAN_INTERVAL_SEC)
    except Exception as e:
        print("ERROR",e)
        if getpass.getuser() != 'root':
            print('使用方法: sudo', argv[0])
            exit()
        sleep(interval)
        continue
        
    # 受信データからセンサメダル2のデバイスを取得
    sensorMedal2Device = None
    for dev in devices:
        if sensorMedal2Address == dev.addr :
            sensorMedal2Device = dev;
    
    # センサメダル2のデバイスが取得できない場合はスキャンに戻る
    if sensorMedal2Device is None: continue
    
    # センサメダル2からデータを取得する
    sensorMedal2 = SensorMedal2.SensorMedal2(sensorMedal2Device)
    sensors = sensorMedal2.getInfo()
    
    # センサー情報が取得できない場合はスキャンに戻る
    if sensors is None: continue
    
    print('    ID            =',sensors['ID'])
    print('    SEQ           =',sensors['SEQ'])
    print('    Temperature   =',round(sensors['Temperature'],2),'℃')
    print('    Humidity      =',round(sensors['Humidity'],2),'%')
    print('    Pressure      =',round(sensors['Pressure'],3),'hPa')
    print('    Illuminance   =',round(sensors['Illuminance'],1),'lx')
    print('    Accelerometer =',round(sensors['Accelerometer'],3),'g (',\
                                round(sensors['Accelerometer X'],3),\
                                round(sensors['Accelerometer Y'],3),\
                                round(sensors['Accelerometer Z'],3),'g)')
    print('    Geomagnetic   =',round(sensors['Geomagnetic'],1),'uT (',\
                                round(sensors['Geomagnetic X'],1),\
                                round(sensors['Geomagnetic Y'],1),\
                                round(sensors['Geomagnetic Z'],1),'uT)')
    print('    Magnetic      =',sensors['Magnetic'])
    print('    Steps         =',sensors['Steps'],'歩')
    print('    Battery Level =',sensors['Battery Level'],'%')
    print('    RSSI          =',sensors['RSSI'],'dB')
    print('===================')
    
    dict = {"date":str(datetime.datetime.now()),
            "temperature": round(sensors['Temperature'],2),
            "humidity": round(sensors['Humidity'],2),
            "Pressure" : round(sensors['Pressure'],3),
            "Illuminance" : round(sensors['Illuminance'],1),
            "Accelerometer" : round(sensors['Accelerometer'],3),
            #"AccelerometerX" : round(sensors['Accelerometer X'],3),
            #"AccelerometerY" : round(sensors['Accelerometer Y'],3),
            #"AccelerometerZ" : round(sensors['Accelerometer Z'],3),
            "Geomagnetic" : round(sensors['Geomagnetic'],1),
            #"GeomagneticX" : round(sensors['Geomagnetic X'],1),
            #"GeomagneticY" : round(sensors['Geomagnetic Y'],1),
            #"GeomagneticZ" : round(sensors['Geomagnetic Z'],1),
            "Magnetic" : sensors['Magnetic'],
            "Steps" : sensors['Steps'],
            "BatteryLevel" : sensors['Battery Level'],
            "RSSI" : sensors['RSSI']
            }
    client.publish(TOPIC,json.dumps(dict),1)
    print('AWS IoT Coreに送信しました')
    time.sleep(SEND_INTERVAL_SEC)
    
    
    




