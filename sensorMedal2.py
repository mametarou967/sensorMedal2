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

interval = 3 # 動作間隔

from bluepy import btle
from sys import argv
import getpass
from time import sleep
import json
from collections import OrderedDict
import pprint
import SensorMedal2

# 設定の読み込み
with open("config.json","r") as f:
	config = json.load(f)
	sensorMedal2Address = config['SensorMedal2']['Address']
# bluetoothのscan
scanner = btle.Scanner()
while True:
    # BLE受信処理
    try:
        devices = scanner.scan(interval)
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
    
    sensorMedal2 = SensorMedal2.SensorMedal2(sensorMedal2Device)
    print("Device %s (%s), RSSI=%d dB" % (sensorMedal2Device.addr, sensorMedal2Device.addrType, sensorMedal2Device.rssi))




