[app]
title = Cooler Control
package.name = coolercontrol
package.domain = org.coolercontrol

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,json

version = 0.1

# ⚠️ نسخه‌های پایدار و تست‌شده
requirements = python3==3.11.5,kivy==2.3.0,kivymd==1.1.1,pyjnius==1.6.1

orientation = portrait
fullscreen = 0

# آیکون (اختیاری - اگر ندارید این خط را حذف کنید)
# icon.filename = %(source.dir)s/icon.png

# مجوزهای بلوتوث
android.permissions = android.permission.BLUETOOTH,android.permission.BLUETOOTH_ADMIN,android.permission.BLUETOOTH_CONNECT,android.permission.BLUETOOTH_SCAN,android.permission.ACCESS_FINE_LOCATION,android.permission.ACCESS_COARSE_LOCATION,android.permission.INTERNET

android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.archs = arm64-v8a
android.allow_backup = True
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
