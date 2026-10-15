"""
Cooler Control - کنترل کولر با بلوتوث
"""

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, BooleanProperty
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.screen import MDScreen

# بلوتوث (در صورت پشتیبانی)
try:
    from bluetooth_manager import BluetoothManager
    BLUETOOTH_AVAILABLE = True
except ImportError:
    BLUETOOTH_AVAILABLE = False
    BluetoothManager = None


KV = '''
MDScreen:
    MDBoxLayout:
        orientation: 'vertical'
        
        MDTopAppBar:
            title: "Cooler Control"
            elevation: 4
            pos_hint: {"top": 1}
        
        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(20)
            spacing: dp(20)
            
            MDLabel:
                text: "وضعیت اتصال"
                halign: "center"
                font_style: "H5"
            
            MDLabel:
                id: status_label
                text: "قطع"
                halign: "center"
                theme_text_color: "Custom"
                text_color: 0.8, 0.2, 0.2, 1
                font_style: "H4"
            
            MDRaisedButton:
                text: "اسکن دستگاه‌ها"
                pos_hint: {"center_x": 0.5}
                size_hint_x: 0.7
                on_release: app.scan_devices()
            
            MDRaisedButton:
                text: "اتصال"
                pos_hint: {"center_x": 0.5}
                size_hint_x: 0.7
                on_release: app.connect_device()
            
            MDLabel:
                id: device_label
                text: "دستگاهی متصل نیست"
                halign: "center"
                font_style: "Body1"
'''

Builder.load_string(KV)


class CoolerControlApp(MDApp):
    connected = BooleanProperty(False)
    device_name = StringProperty("")
    
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        
        if BLUETOOTH_AVAILABLE:
            self.bt_manager = BluetoothManager()
        else:
            self.bt_manager = None
        
        return Builder.load_string(KV)
    
    def scan_devices(self):
        """اسکن دستگاه‌های بلوتوث"""
        self.root.ids.status_label.text = "در حال اسکن..."
        self.root.ids.status_label.text_color = (0.9, 0.7, 0.1, 1)
        self.root.ids.device_label.text = "در حال جستجو..."
        
        if self.bt_manager:
            try:
                devices = self.bt_manager.scan()
                if devices:
                    self.root.ids.device_label.text = f"یافت شد: {len(devices)} دستگاه"
                else:
                    self.root.ids.device_label.text = "دستگاهی یافت نشد"
            except Exception as e:
                self.root.ids.device_label.text = f"خطا: {e}"
        else:
            self.root.ids.device_label.text = "بلوتوث پشتیبانی نمی‌شود"
        
        self.root.ids.status_label.text = "قطع"
        self.root.ids.status_label.text_color = (0.8, 0.2, 0.2, 1)
    
    def connect_device(self):
        """اتصال به دستگاه"""
        if self.connected:
            # قطع اتصال
            self.connected = False
            self.root.ids.status_label.text = "قطع"
            self.root.ids.status_label.text_color = (0.8, 0.2, 0.2, 1)
            self.root.ids.device_label.text = "دستگاهی متصل نیست"
        else:
            # اتصال
            self.root.ids.status_label.text = "در حال اتصال..."
            self.root.ids.status_label.text_color = (0.9, 0.7, 0.1, 1)
            
            if self.bt_manager:
                try:
                    success = self.bt_manager.connect()
                    if success:
                        self.connected = True
                        self.root.ids.status_label.text = "متصل ✓"
                        self.root.ids.status_label.text_color = (0.2, 0.8, 0.2, 1)
                        self.root.ids.device_label.text = "دستگاه متصل است"
                    else:
                        self.root.ids.status_label.text = "قطع"
                        self.root.ids.status_label.text_color = (0.8, 0.2, 0.2, 1)
                        self.root.ids.device_label.text = "اتصال ناموفق"
                except Exception as e:
                    self.root.ids.device_label.text = f"خطا: {e}"
            else:
                # حالت دمو بدون بلوتوث
                self.connected = True
                self.root.ids.status_label.text = "متصل ✓ (دمو)"
                self.root.ids.status_label.text_color = (0.2, 0.8, 0.2, 1)
                self.root.ids.device_label.text = "حالت تست"


if __name__ == '__main__':
    CoolerControlApp().run()
