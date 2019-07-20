from sys import argv
import getpass
from time import sleep

class SensorMedal2 :
    # 初期処理
    def __init__(self,device) :
        self.device = device
        self.val = None
        for (adtype, desc, val) in device.getScanData():
            if desc == 'Manufacturer' :
                self.val = val
                break
    
    def getInfo(self) :
        if self.val is None :
            return
        sensors = dict()
        sensors['ID'] = hex(self.payval(2,2))
        sensors['Temperature'] = -45 + 175 * self.payval(4,2) / 65536
        sensors['Humidity'] = 100 * self.payval(6,2) / 65536
        sensors['SEQ'] = self.payval(8)
        sensors['Condition Flags'] = bin(int(self.val[16:18],16))
        sensors['Accelerometer X'] = self.payval(10,2,True) / 4096
        sensors['Accelerometer Y'] = self.payval(12,2,True) / 4096
        sensors['Accelerometer Z'] = self.payval(14,2,True) / 4096
        sensors['Accelerometer'] = (sensors['Accelerometer X'] ** 2\
                                  + sensors['Accelerometer Y'] ** 2\
                                  + sensors['Accelerometer Z'] ** 2) ** 0.5
        sensors['Geomagnetic X'] = self.payval(16,2,True) / 10
        sensors['Geomagnetic Y'] = self.payval(18,2,True) / 10
        sensors['Geomagnetic Z'] = self.payval(20,2,True) / 10
        sensors['Geomagnetic']  = (sensors['Geomagnetic X'] ** 2\
                                 + sensors['Geomagnetic Y'] ** 2\
                                 + sensors['Geomagnetic Z'] ** 2) ** 0.5
        sensors['Pressure'] = self.payval(22,3) / 2048
        sensors['Illuminance'] = self.payval(25,2) / 1.2
        sensors['Magnetic'] = self.payval(27)
        sensors['Steps'] = self.payval(28,2)
        sensors['Battery Level'] = self.payval(30)
        sensors['RSSI'] = self.device.rssi
        return sensors
        
    def payval(self,num, bytes=1, sign=False):
        a = 0
        for i in range(0, bytes):
            a += (256 ** i) * int(self.val[(num - 2 + i) * 2 : (num - 1 + i) * 2],16)
        if sign:
            if a >= 2 ** (bytes * 8 - 1):
                a -= 2 ** (bytes * 8)
        return a
                
