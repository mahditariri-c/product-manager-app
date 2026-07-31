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
android.api = 29
android.minapi = 21
android.ndk = 23b
android.sdk = 29
android.enable_androidx = True
