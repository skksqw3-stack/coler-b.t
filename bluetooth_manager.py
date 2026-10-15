"""
مدیریت بلوتوث برای اندروید
"""

import threading
import time
import os


class BluetoothManager:
    def __init__(self):
        self.connected = False
        self.device = None
        self.socket = None
        self.is_android = self._check_android()
    
    def _check_android(self):
        """بررسی اینکه روی اندروید اجرا می‌شویم یا نه"""
        try:
            from jnius import autoclass
            return True
        except ImportError:
            return False
    
    def scan(self):
        """اسکن دستگاه‌های بلوتوث اطراف"""
        if not self.is_android:
            # حالت دمو
            time.sleep(2)
            return [
                {'name': 'Cooler-01', 'address': '00:11:22:33:44:55'},
                {'name': 'Cooler-02', 'address': 'AA:BB:CC:DD:EE:FF'},
            ]
        
        try:
            from jnius import autoclass, cast
            
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            activity = PythonActivity.mActivity
            BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
            Intent = autoclass('android.content.Intent')
            IntentFilter = autoclass('android.content.IntentFilter')
            BroadcastReceiver = autoclass('android.content.BroadcastReceiver')
            
            adapter = BluetoothAdapter.getDefaultAdapter()
            if adapter is None:
                return []
            
            if not adapter.isEnabled():
                adapter.enable()
            
            # شروع اسکن
            adapter.startDiscovery()
            time.sleep(5)
            adapter.cancelDiscovery()
            
            # دریافت دستگاه‌های جفت‌شده
            bonded = adapter.getBondedDevices()
            devices = []
            for device in bonded:
                devices.append({
                    'name': device.getName(),
                    'address': device.getAddress(),
                })
            
            return devices
        except Exception as e:
            print(f"Bluetooth scan error: {e}")
            return []
    
    def connect(self, address=None):
        """اتصال به دستگاه"""
        if not self.is_android:
            # حالت دمو
            time.sleep(2)
            self.connected = True
            return True
        
        try:
            from jnius import autoclass
            
            BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
            adapter = BluetoothAdapter.getDefaultAdapter()
            
            if address is None:
                # اولین دستگاه جفت‌شده را انتخاب کن
                bonded = adapter.getBondedDevices()
                for device in bonded:
                    address = device.getAddress()
                    break
            
            if address is None:
                return False
            
            device = adapter.getRemoteDevice(address)
            
            # UUID استاندارد SPP
            UUID = autoclass('java.util.UUID')
            spp_uuid = UUID.fromString('00001101-0000-1000-8000-00805F9B34FB')
            
            socket = device.createRfcommSocketToServiceRecord(spp_uuid)
            adapter.cancelDiscovery()
            socket.connect()
            
            self.device = device
            self.socket = socket
            self.connected = True
            return True
        except Exception as e:
            print(f"Bluetooth connect error: {e}")
            return False
    
    def send(self, data):
        """ارسال داده به دستگاه"""
        if not self.connected or self.socket is None:
            return False
        
        try:
            if isinstance(data, str):
                data = data.encode('utf-8')
            self.socket.getOutputStream().write(data)
            return True
        except Exception as e:
            print(f"Bluetooth send error: {e}")
            return False
    
    def disconnect(self):
        """قطع اتصال"""
        try:
            if self.socket:
                self.socket.close()
        except:
            pass
        self.connected = False
        self.socket = None
        self.device = None
