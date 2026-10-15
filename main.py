"""
Cooler Control - کنترل کولر با بلوتوث
KV در فایل جداگانه cooler.kv است
"""

import os
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.app import MDApp

# بلوتوث
try:
    from bluetooth_manager import BluetoothManager
    BLUETOOTH_AVAILABLE = True
except ImportError:
    BLUETOOTH_AVAILABLE = False
    BluetoothManager = None


class CoolerControlApp(MDApp):
    is_connected = False
    devices = []
    
    def build(self):
        """ساخت اپلیکیشن"""
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        self.title = "Cooler Control"
        Window.clearcolor = (0.95, 0.95, 0.95, 1)
        
        # راه‌اندازی بلوتوث
        if BLUETOOTH_AVAILABLE:
            self.bt = BluetoothManager()
        else:
            self.bt = None
        
        # ⚠️ بارگذاری فایل KV جداگانه
        kv_path = os.path.join(os.path.dirname(__file__), 'cooler.kv')
        return Builder.load_file(kv_path)
    
    # ═══════════════════════════════════════════════
    # 📡 متدهای بلوتوث
    # ═══════════════════════════════════════════════
    
    def scan_devices(self):
        """اسکن دستگاه‌های بلوتوث"""
        self.update_status("در حال اسکن...", "scanning")
        self.root.ids.device_info.text = "لطفاً صبر کنید..."
        
        if self.bt:
            try:
                devices = self.bt.scan()
                self.devices = devices
                self.root.ids.device_list.clear_widgets()
                
                if devices:
                    self.root.ids.device_info.text = f"یافت شد: {len(devices)} دستگاه"
                    from kivymd.uix.list import OneLineListItem
                    for d in devices:
                        item = OneLineListItem(
                            text=f"{d['name']}  |  {d['address']}"
                        )
                        self.root.ids.device_list.add_widget(item)
                else:
                    self.root.ids.device_info.text = "دستگاهی یافت نشد"
            except Exception as e:
                self.root.ids.device_info.text = f"خطا: {str(e)[:50]}"
        else:
            # حالت دمو
            self.root.ids.device_info.text = "حالت دمو (بدون بلوتوث)"
            from kivymd.uix.list import OneLineListItem
            self.root.ids.device_list.clear_widgets()
            demo = [
                {'name': 'Cooler-01', 'address': '00:11:22:33:44:55'},
                {'name': 'Cooler-02', 'address': 'AA:BB:CC:DD:EE:FF'},
            ]
            for d in demo:
                self.root.ids.device_list.add_widget(
                    OneLineListItem(text=f"{d['name']}  |  {d['address']}")
                )
        
        self.update_status("قطع", "disconnected")
    
    def toggle_connection(self):
        """اتصال/قطع"""
        if self.is_connected:
            self.disconnect()
        else:
            self.connect()
    
    def connect(self):
        """اتصال"""
        self.update_status("در حال اتصال...", "connecting")
        
        if self.bt:
            try:
                success = self.bt.connect()
                if success:
                    self.is_connected = True
                    self.update_status("متصل", "connected")
                    self.root.ids.device_info.text = "دستگاه متصل است"
                    self.root.ids.connect_btn.text = "قطع اتصال"
                else:
                    self.update_status("قطع", "disconnected")
                    self.root.ids.device_info.text = "اتصال ناموفق"
            except Exception as e:
                self.root.ids.device_info.text = f"خطا: {str(e)[:50]}"
                self.update_status("قطع", "disconnected")
        else:
            # حالت دمو
            self.is_connected = True
            self.update_status("متصل (دمو)", "connected")
            self.root.ids.device_info.text = "حالت تست"
            self.root.ids.connect_btn.text = "قطع اتصال"
    
    def disconnect(self):
        """قطع اتصال"""
        if self.bt:
            try:
                self.bt.disconnect()
            except:
                pass
        self.is_connected = False
        self.update_status("قطع", "disconnected")
        self.root.ids.device_info.text = "دستگاهی متصل نیست"
        self.root.ids.connect_btn.text = "اتصال"
    
    def update_status(self, text, state):
        """به‌روزرسانی وضعیت"""
        if not hasattr(self.root.ids, 'status_label'):
            return
        self.root.ids.status_label.text = text
        colors = {
            "connected": (0.2, 0.7, 0.3, 1),
            "disconnected": (0.8, 0.2, 0.2, 1),
            "scanning": (0.9, 0.6, 0.1, 1),
            "connecting": (0.9, 0.6, 0.1, 1),
        }
        self.root.ids.status_label.text_color = colors.get(state, (0.5, 0.5, 0.5, 1))
    
    # ═══════════════════════════════════════════════
    # 🎛️ کنترل کولر
    # ═══════════════════════════════════════════════
    
    def set_speed(self, speed):
        """تنظیم سرعت"""
        if not self.is_connected:
            self.root.ids.device_info.text = "ابتدا متصل شوید"
            return
        commands = {
            "low": "SPEED_LOW\n",
            "medium": "SPEED_MED\n",
            "high": "SPEED_HIGH\n",
            "off": "SPEED_OFF\n",
        }
        command = commands.get(speed, "")
        if command:
            self.send_command(command)
            self.root.ids.device_info.text = f"سرعت: {speed}"
    
    def power_off(self):
        """خاموش کردن کامل"""
        if not self.is_connected:
            self.root.ids.device_info.text = "ابتدا متصل شوید"
            return
        self.send_command("POWER_OFF\n")
        self.root.ids.device_info.text = "دستور خاموش ارسال شد"
    
    def send_command(self, command):
        """ارسال دستور"""
        if self.bt:
            try:
                self.bt.send(command)
            except Exception as e:
                self.root.ids.device_info.text = f"خطا: {str(e)[:50]}"
        else:
            print(f"[دمو] ارسال: {command}")
    
    def show_settings(self):
        """تنظیمات"""
        self.root.ids.device_info.text = "تنظیمات (به‌زودی)"


if __name__ == '__main__':
    CoolerControlApp().run()
