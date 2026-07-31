[app]
title = مدیریت هوشمند کالا
package.name = productmanager
package.domain = org.mahditar

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

requirements = python3,kivy,kivymd,openpyxl,reportlab

version = 4.0.0
orientation = portrait

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 34
android.minapi = 21
android.ndk = 28c
android.sdk = 34
android.enable_androidx = True

# مشخص کردن نسخه build-tools
android.build_tools = 34.0.0
