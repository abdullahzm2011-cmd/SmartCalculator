[app]

title = Smart Calculator Pro
package.name = smartcalculator
package.domain = com.smartapp

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf

version = 1.0.0

requirements = python3,kivy

orientation = portrait

fullscreen = 0

android.permissions = INTERNET
android.api = 31
android.minapi = 21
android.sdk = 33
android.ndk = 23b
android.enable_androidx = True
android.bootstrap = sdl2

[buildozer]
log_level = 2
warn_on_root = 1
