[app]

title = Cooler Control
package.name = coolercontrol
package.domain = org.coolercontrol

source.dir = .
source.include_exts = py,kv,png,jpg,jpeg,atlas,ttf,json
source.exclude_dirs = .git,.github,.buildozer,venv,.venv,__pycache__

version = 0.1.0

requirements = python3,kivy==2.3.0,kivymd==1.1.1,pyjnius

orientation = portrait
fullscreen = 0

android.api = 33
android.minapi = 23
android.ndk = 25b
android.ndk_api = 23

android.archs = arm64-v8a
android.accept_sdk_license = True
android.allow_backup = True

android.permissions = BLUETOOTH,BLUETOOTH_ADMIN,BLUETOOTH_CONNECT,BLUETOOTH_SCAN,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION

p4a.branch = master

[buildozer]

log_level = 2
warn_on_root = 1
