"""
مدیریت بلوتوث - کار با Android Bluetooth API
"""

import time


class BluetoothManager:
    def __init__(self):
        self.connected = False
        self.device = None
        self.socket = None
        self.is_android = self._check_android()
    
    def _check_android(self):
        try:
            from jnius import autoclass
            return True
        except ImportError:
            return False
    
    def scan(self):
        if not self.is_android:
            time.sleep(1)
            return [
                {'name': 'Cooler-01', 'address': '00:11:22:33:44:55'},
                {'name': 'Cooler-02', 'address': 'AA:BB:CC:DD:EE:FF'},
                {'name': 'Cooler-03', 'address': '11:22:33:44:55:66'},
            ]
        
        try:
            from jnius import autoclass
            BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
            adapter = BluetoothAdapter.getDefaultAdapter()
            if adapter is None:
                return []
            if not adapter.isEnabled():
                adapter.enable()
                time.sleep(2)
            adapter.startDiscovery()
            time.sleep(5)
            adapter.cancelDiscovery()
            bonded = adapter.getBondedDevices()
            devices = []
            for device in bonded:
                devices.append({
                    'name': device.getName() or "Unknown",
                    'address': device.getAddress(),
                })
            return devices
        except Exception as e:
            print(f"Scan error: {e}")
            return []
    
    def connect(self, address=None):
        if not self.is_android:
            time.sleep(1)
            self.connected = True
            return True
        try:
            from jnius import autoclass
            BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
            adapter = BluetoothAdapter.getDefaultAdapter()
            if address is None:
                bonded = adapter.getBondedDevices()
                for device in bonded:
                    address = device.getAddress()
                    break
            if address is None:
                return False
            device = adapter.getRemoteDevice(address)
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
            print(f"Connect error: {e}")
            return False
    
    def send(self, data):
        if not self.connected or self.socket is None:
            return False
        try:
            if isinstance(data, str):
                data = data.encode('utf-8')
            self.socket.getOutputStream().write(data)
            return True
        except Exception as e:
            print(f"Send error: {e}")
            return False
    
    def disconnect(self):
        try:
            if self.socket:
                self.socket.close()
        except:
            pass
        self.connected = False
        self.socket = None
        self.device = None
