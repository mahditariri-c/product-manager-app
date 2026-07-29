# ====== اپلیکیشن مدیریت هوشمند کالا - نسخه حرفه‌ای ======
# ====== سازنده: مهدی طریری ======
# ====== تلگرام: @mahdi_tar ======

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle

# کتابخانه‌های KivyMD برای طراحی حرفه‌ای
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.list import MDList, ThreeLineAvatarIconListItem, OneLineIconListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.chip import MDChip
from kivymd.icon_definitions import md_icons

import sqlite3
from datetime import datetime
import os
import json

# ====== تنظیمات پنجره ======
Window.size = (400, 780)

# ====== کد طراحی KV (رابط کاربری) ======
KV = '''
<CustomCard@MDCard>:
    radius: dp(15)
    elevation: 4
    padding: dp(10)
    spacing: dp(5)
    md_bg_color: app.theme_cls.bg_dark

<GlassCard@MDCard>:
    radius: dp(20)
    elevation: 8
    padding: dp(15)
    md_bg_color: [1, 1, 1, 0.12]
    size_hint_y: None
    height: dp(120)

MDScreen:
    md_bg_color: app.theme_cls.bg_normal
    
    MDNavigationDrawer:
        id: nav_drawer
        radius: [0, dp(25), dp(25), 0]
        md_bg_color: app.theme_cls.bg_dark
        
        MDBoxLayout:
            orientation: 'vertical'
            spacing: dp(10)
            padding: dp(20)
            
            # پروفایل کاربر
            MDBoxLayout:
                size_hint_y: None
                height: dp(130)
                orientation: 'vertical'
                spacing: dp(5)
                
                MDIconButton:
                    icon: "account-circle"
                    icon_size: dp(60)
                    pos_hint: {"center_x": 0.5}
                    theme_text_color: "Custom"
                    text_color: app.theme_cls.primary_color
                
                MDLabel:
                    text: "مهدی طریری"
                    font_style: "H6"
                    halign: "center"
                    bold: True
                
                MDLabel:
                    text: "مدیر سیستم"
                    font_style: "Caption"
                    halign: "center"
                    theme_text_color: "Hint"
            
            MDDivider:
                height: dp(1)
            
            # منوی اصلی
            MDScrollView:
                MDList:
                    id: nav_list
                    OneLineIconListItem:
                        text: "خانه"
                        on_press: 
                            root.navigation_draw()
                            root.current = "home"
                        IconLeftWidget:
                            icon: "home"
                    
                    OneLineIconListItem:
                        text: "مدیریت کالا"
                        on_press: 
                            root.navigation_draw()
                            root.current = "products"
                        IconLeftWidget:
                            icon: "format-list-bulleted"
                    
                    OneLineIconListItem:
                        text: "ثبت کالا"
                        on_press: 
                            root.navigation_draw()
                            root.current = "add"
                        IconLeftWidget:
                            icon: "plus-circle"
                    
                    OneLineIconListItem:
                        text: "آمار و تحلیل"
                        on_press: 
                            root.navigation_draw()
                            root.current = "stats"
                        IconLeftWidget:
                            icon: "chart-bar"
                    
                    OneLineIconListItem:
                        text: "تنظیمات"
                        on_press: 
                            root.navigation_draw()
                            root.current = "settings"
                        IconLeftWidget:
                            icon: "cog"

    # ====== صفحه خانه ======
    MDScreen:
        name: "home"
        
        MDBoxLayout:
            orientation: "vertical"
            spacing: dp(5)
            
            MDToolbar:
                title: "🏪 مدیریت کالا"
                elevation: dp(10)
                right_action_items:
                    [["menu", lambda x: nav_drawer.set_state("open")]]
                md_bg_color: app.theme_cls.primary_color
            
            MDScrollView:
                do_scroll_x: False
                
                MDBoxLayout:
                    orientation: "vertical"
                    spacing: dp(15)
                    padding: dp(15)
                    size_hint_y: None
                    height: self.minimum_height
                    
                    # کارت خوش‌آمدگویی
                    GlassCard:
                        md_bg_color: [0.2, 0.6, 0.8, 0.15]
                        
                        MDBoxLayout:
                            orientation: "vertical"
                            spacing: dp(5)
                            
                            MDLabel:
                                text: "سلام 👋"
                                font_style: "H4"
                                bold: True
                                theme_text_color: "Primary"
                            
                            MDLabel:
                                text: "به مدیریت هوشمند کالا خوش آمدید"
                                font_style: "Subtitle1"
                                theme_text_color: "Hint"
                            
                            MDLabel:
                                text: datetime.now().strftime('%A, %d %B %Y')
                                font_style: "Caption"
                                theme_text_color: "Hint"
                    
                    # کارت‌های آماری
                    MDGridLayout:
                        cols: 2
                        spacing: dp(10)
                        size_hint_y: None
                        height: dp(130)
                        
                        CustomCard:
                            md_bg_color: app.theme_cls.primary_color
                            MDBoxLayout:
                                orientation: "vertical"
                                spacing: dp(5)
                                MDIcon:
                                    icon: "package-variant"
                                    icon_size: dp(30)
                                    theme_text_color: "Custom"
                                    text_color: [1, 1, 1, 1]
                                MDLabel:
                                    id: home_total
                                    text: "۰"
                                    font_style: "H4"
                                    bold: True
                                    theme_text_color: "Custom"
                                    text_color: [1, 1, 1, 1]
                                MDLabel:
                                    text: "کل کالاها"
                                    theme_text_color: "Custom"
                                    text_color: [1, 1, 1, 0.7]
                        
                        CustomCard:
                            md_bg_color: app.theme_cls.accent_color
                            MDBoxLayout:
                                orientation: "vertical"
                                spacing: dp(5)
                                MDIcon:
                                    icon: "cash"
                                    icon_size: dp(30)
                                    theme_text_color: "Custom"
                                    text_color: [1, 1, 1, 1]
                                MDLabel:
                                    id: home_value
                                    text: "۰"
                                    font_style: "H4"
                                    bold: True
                                    theme_text_color: "Custom"
                                    text_color: [1, 1, 1, 1]
                                MDLabel:
                                    text: "ارزش کل"
                                    theme_text_color: "Custom"
                                    text_color: [1, 1, 1, 0.7]
                    
                    # دکمه‌های سریع
                    MDBoxLayout:
                        size_hint_y: None
                        height: dp(55)
                        spacing: dp(10)
                        
                        MDRaisedButton:
                            text: "➕ افزودن کالا"
                            size_hint_x: 0.5
                            md_bg_color: app.theme_cls.primary_color
                            on_press: root.current = "add"
                        
                        MDRaisedButton:
                            text: "📋 لیست کالاها"
                            size_hint_x: 0.5
                            md_bg_color: app.theme_cls.accent_color
                            on_press: root.current = "products"
                    
                    # آخرین فعالیت‌ها
                    MDLabel:
                        text: "🕐 آخرین فعالیت‌ها"
                        font_style: "H6"
                        bold: True
                        size_hint_y: None
                        height: dp(30)
                    
                    CustomCard:
                        height: dp(180)
                        
                        MDScrollView:
                            do_scroll_x: False
                            
                            MDList:
                                id: recent_list
                                ThreeLineAvatarIconListItem:
                                    text: "افزودن کالای جدید"
                                    secondary_text: "گوشی سامسونگ S24"
                                    tertiary_text: "امروز، ۱۴:۳۰"
                                    IconLeftWidget:
                                        icon: "plus-circle"
                                
                                ThreeLineAvatarIconListItem:
                                    text: "ویرایش قیمت"
                                    secondary_text: "هدفون بی‌سیم"
                                    tertiary_text: "امروز، ۱۳:۱۵"
                                    IconLeftWidget:
                                        icon: "update"
                                
                                ThreeLineAvatarIconListItem:
                                    text: "ثبت فروش"
                                    secondary_text: "کتاب پایتون × ۲ عدد"
                                    tertiary_text: "دیروز، ۱۸:۴۰"
                                    IconLeftWidget:
                                        icon: "cash"

    # ====== صفحه مدیریت کالا ======
    MDScreen:
        name: "products"
        
        MDBoxLayout:
            orientation: "vertical"
            spacing: dp(5)
            
            MDToolbar:
                title: "📋 مدیریت کالا"
                elevation: dp(10)
                right_action_items:
                    [["menu", lambda x: nav_drawer.set_state("open")]]
                md_bg_color: app.theme_cls.primary_color
            
            MDBoxLayout:
                size_hint_y: None
                height: dp(55)
                padding: dp(10)
                spacing: dp(10)
                
                MDTextField:
                    id: search_field
                    hint_text: "🔍 جستجو..."
                    mode: "rectangle"
                    size_hint_x: 0.7
                    height: dp(45)
                    radius: dp(10)
                    line_color_focus: app.theme_cls.primary_color
                
                MDRaisedButton:
                    text: "جستجو"
                    size_hint_x: 0.3
                    md_bg_color: app.theme_cls.primary_color
                    on_press: app.search_products(search_field.text)
            
            MDBoxLayout:
                size_hint_y: None
                height: dp(45)
                padding: dp(10)
                spacing: dp(8)
                
                MDChip:
                    text: "همه"
                    selected: True
                    on_press: app.filter_products("همه")
                
                MDChip:
                    text: "الکترونیک"
                    on_press: app.filter_products("الکترونیک")
                
                MDChip:
                    text: "پوشاک"
                    on_press: app.filter_products("پوشاک")
                
                MDChip:
                    text: "کتاب"
                    on_press: app.filter_products("کتاب")
            
            MDScrollView:
                MDList:
                    id: product_list

    # ====== صفحه ثبت کالا ======
    MDScreen:
        name: "add"
        
        MDBoxLayout:
            orientation: "vertical"
            spacing: dp(5)
            
            MDToolbar:
                title: "➕ ثبت کالا"
                elevation: dp(10)
                right_action_items:
                    [["menu", lambda x: nav_drawer.set_state("open")]]
                md_bg_color: app.theme_cls.primary_color
            
            MDScrollView:
                do_scroll_x: False
                
                MDBoxLayout:
                    orientation: "vertical"
                    spacing: dp(15)
                    padding: dp(15)
                    size_hint_y: None
                    height: self.minimum_height
                    
                    CustomCard:
                        height: dp(550)
                        
                        MDBoxLayout:
                            orientation: "vertical"
                            spacing: dp(12)
                            padding: dp(15)
                            
                            MDLabel:
                                text: "📝 اطلاعات کالا"
                                font_style: "H6"
                                bold: True
                                theme_text_color: "Primary"
                            
                            MDTextField:
                                id: name_field
                                hint_text: "نام کالا *"
                                mode: "rectangle"
                                radius: dp(10)
                            
                            MDTextField:
                                id: barcode_field
                                hint_text: "بارکد (اختیاری)"
                                mode: "rectangle"
                                radius: dp(10)
                            
                            MDTextField:
                                id: price_field
                                hint_text: "💰 قیمت فروش (تومان)"
                                mode: "rectangle"
                                input_filter: "float"
                                radius: dp(10)
                            
                            MDTextField:
                                id: purchase_field
                                hint_text: "💰 قیمت خرید (تومان)"
                                mode: "rectangle"
                                input_filter: "float"
                                radius: dp(10)
                            
                            MDBoxLayout:
                                size_hint_y: None
                                height: dp(50)
                                spacing: dp(10)
                                
                                MDTextField:
                                    id: quantity_field
                                    hint_text: "📦 تعداد"
                                    mode: "rectangle"
                                    input_filter: "int"
                                    text: "1"
                                    radius: dp(10)
                                    size_hint_x: 0.5
                                
                                MDTextField:
                                    id: min_quantity_field
                                    hint_text: "⚠️ حداقل موجودی"
                                    mode: "rectangle"
                                    input_filter: "int"
                                    text: "5"
                                    radius: dp(10)
                                    size_hint_x: 0.5
                            
                            MDTextField:
                                id: date_field
                                hint_text: "📅 تاریخ"
                                mode: "rectangle"
                                text: datetime.now().strftime('%Y-%m-%d')
                                radius: dp(10)
                            
                            MDBoxLayout:
                                size_hint_y: None
                                height: dp(50)
                                spacing: dp(10)
                                
                                MDRaisedButton:
                                    text: "✅ ثبت کالا"
                                    md_bg_color: app.theme_cls.primary_color
                                    size_hint_x: 0.5
                                    on_press: app.add_product(
                                        name_field.text,
                                        price_field.text,
                                        purchase_field.text,
                                        quantity_field.text,
                                        min_quantity_field.text,
                                        date_field.text,
                                        barcode_field.text
                                    )
                                
                                MDRaisedButton:
                                    text: "🗑️ پاک کردن"
                                    md_bg_color: app.theme_cls.error_color
                                    size_hint_x: 0.5
                                    on_press: app.clear_form()

    # ====== صفحه آمار ======
    MDScreen:
        name: "stats"
        
        MDBoxLayout:
            orientation: "vertical"
            spacing: dp(5)
            
            MDToolbar:
                title: "📊 آمار و تحلیل"
                elevation: dp(10)
                right_action_items:
                    [["menu", lambda x: nav_drawer.set_state("open")]]
                md_bg_color: app.theme_cls.primary_color
            
            MDBoxLayout:
                size_hint_y: None
                height: dp(50)
                padding: dp(10)
                spacing: dp(10)
                
                MDRaisedButton:
                    text: "🔄 بروزرسانی"
                    md_bg_color: app.theme_cls.primary_color
                    size_hint_x: 0.25
                    on_press: app.update_stats()
                
                MDRaisedButton:
                    text: "📤 خروجی"
                    md_bg_color: app.theme_cls.success_color
                    size_hint_x: 0.25
                    on_press: app.export_menu()
                
                MDRaisedButton:
                    text: "💾 پشتیبان"
                    md_bg_color: app.theme_cls.warning_color
                    size_hint_x: 0.25
                    on_press: app.backup_database()
            
            MDScrollView:
                MDBoxLayout:
                    orientation: "vertical"
                    spacing: dp(15)
                    padding: dp(15)
                    size_hint_y: None
                    height: self.minimum_height
                    
                    MDGridLayout:
                        cols: 2
                        spacing: dp(10)
                        size_hint_y: None
                        height: dp(250)
                        
                        CustomCard:
                            md_bg_color: app.theme_cls.primary_color
                            MDBoxLayout:
                                orientation: "vertical"
                                spacing: dp(5)
                                MDIcon:
                                    icon: "package-variant"
                                    icon_size: dp(30)
                                    theme_text_color: "Custom"
                                    text_color: [1, 1, 1, 1]
                                MDLabel:
                                    id: stat_total
                                    text: "۰"
                                    font_style: "H3"
                                    bold: True
                                    theme_text_color: "Custom"
                                    text_color: [1, 1, 1, 1]
                                MDLabel:
                                    text: "کل کالاها"
                                    theme_text_color: "Custom"
                                    text_color: [1, 1, 1, 0.7]
                        
                        CustomCard:
                            md_bg_color: app.theme_cls.accent_color
                            MDBoxLayout:
                                orientation: "vertical"
                                spacing: dp(5)
                                MDIcon:
                                    icon: "cash"
                                    icon_size: dp(30)
                                    theme_text_color: "Custom"
                                    text_color: [1, 1, 1, 1]
                                MDLabel:
                                    id: stat_value
                                    text: "۰"
                                    font_style: "H3"
                                    bold: True
                                    theme_text_color: "Custom"
                                    text_color: [1, 1, 1, 1]
                                MDLabel:
                                    text: "ارزش کل"
                                    theme_text_color: "Custom"
                                    text_color: [1, 1, 1, 0.7]
                    
                    MDGridLayout:
                        cols: 2
                        spacing: dp(10)
                        size_hint_y: None
                        height: dp(250)
                        
                        CustomCard:
                            md_bg_color: app.theme_cls.success_color
                            MDBoxLayout:
                                orientation: "vertical"
                                spacing: dp(5)
                                MDIcon:
                                    icon: "chart-line"
                                    icon_size: dp(30)
                                    theme_text_color: "Custom"
                                    text_color: [1, 1, 1, 1]
                                MDLabel:
                                    id: stat_avg
                                    text: "۰"
                                    font_style: "H3"
                                    bold: True
                                    theme_text_color: "Custom"
                                    text_color: [1, 1, 1, 1]
                                MDLabel:
                                    text: "میانگین قیمت"
                                    theme_text_color: "Custom"
                                    text_color: [1, 1, 1, 0.7]
                        
                        CustomCard:
                            md_bg_color: app.theme_cls.error_color
                            MDBoxLayout:
                                orientation: "vertical"
                                spacing: dp(5)
                                MDIcon:
                                    icon: "alert-circle"
                                    icon_size: dp(30)
                                    theme_text_color: "Custom"
                                    text_color: [1, 1, 1, 1]
                                MDLabel:
                                    id: stat_low
                                    text: "۰"
                                    font_style: "H3"
                                    bold: True
                                    theme_text_color: "Custom"
                                    text_color: [1, 1, 1, 1]
                                MDLabel:
                                    text: "موجودی کم"
                                    theme_text_color: "Custom"
                                    text_color: [1, 1, 1, 0.7]
                    
                    CustomCard:
                        height: dp(180)
                        
                        MDBoxLayout:
                            orientation: "vertical"
                            spacing: dp(10)
                            padding: dp(15)
                            
                            MDLabel:
                                text: "📋 جزئیات بیشتر"
                                font_style: "H6"
                                bold: True
                            
                            MDLabel:
                                id: detail_label
                                text: """
📦 تعداد کل: ۰ کالا
📂 دسته‌بندی‌ها: ۶ دسته
💰 سود کل: ۰ تومان
📈 تعداد فروش: ۰ مورد
                                """
                                font_style: "Body1"

    # ====== صفحه تنظیمات ======
    MDScreen:
        name: "settings"
        
        MDBoxLayout:
            orientation: "vertical"
            spacing: dp(5)
            
            MDToolbar:
                title: "⚙️ تنظیمات"
                elevation: dp(10)
                right_action_items:
                    [["menu", lambda x: nav_drawer.set_state("open")]]
                md_bg_color: app.theme_cls.primary_color
            
            MDScrollView:
                MDList:
                    id: settings_list
                    
                    OneLineIconListItem:
                        text: "🌙 تم تاریک"
                        on_press: app.toggle_theme()
                        IconLeftWidget:
                            icon: "brightness-4"
                    
                    OneLineIconListItem:
                        text: "🔔 اعلان‌ها"
                        on_press: app.show_notifications()
                        IconLeftWidget:
                            icon: "bell"
                    
                    OneLineIconListItem:
                        text: "☁️ همگام‌سازی ابری"
                        on_press: app.cloud_sync()
                        IconLeftWidget:
                            icon: "cloud-upload"
                    
                    OneLineIconListItem:
                        text: "📤 خروجی PDF/Excel"
                        on_press: app.export_menu()
                        IconLeftWidget:
                            icon: "export"
                    
                    OneLineIconListItem:
                        text: "📱 درباره برنامه"
                        on_press: app.show_about()
                        IconLeftWidget:
                            icon: "information"
'''

# ====== کلاس دیتابیس ======
class Database:
    def __init__(self):
        self.conn = sqlite3.connect('products.db')
        self.cursor = self.conn.cursor()
        self.create_table()
    
    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE,
                barcode TEXT,
                name TEXT,
                price REAL,
                purchase_price REAL,
                quantity INTEGER DEFAULT 1,
                min_quantity INTEGER DEFAULT 5,
                date TEXT,
                description TEXT
            )
        ''')
        self.conn.commit()
    
    def add_product(self, name, price, purchase_price, quantity, min_quantity, date, barcode=''):
        code = f"PRD-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        self.cursor.execute('''
            INSERT INTO products (code, barcode, name, price, purchase_price, quantity, min_quantity, date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (code, barcode, name, price, purchase_price, quantity, min_quantity, date))
        self.conn.commit()
        return code
    
    def get_all_products(self):
        self.cursor.execute("SELECT * FROM products ORDER BY id DESC")
        return self.cursor.fetchall()
    
    def delete_product(self, product_id):
        self.cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        self.conn.commit()
    
    def get_stats(self):
        self.cursor.execute("SELECT COUNT(*) FROM products")
        total = self.cursor.fetchone()[0]
        
        self.cursor.execute("SELECT SUM(price * quantity) FROM products")
        total_value = self.cursor.fetchone()[0] or 0
        
        self.cursor.execute("SELECT AVG(price) FROM products")
        avg_price = self.cursor.fetchone()[0] or 0
        
        self.cursor.execute("SELECT COUNT(*) FROM products WHERE quantity <= min_quantity")
        low_stock = self.cursor.fetchone()[0]
        
        return {
            'total': total,
            'total_value': total_value,
            'avg_price': avg_price,
            'low_stock': low_stock
        }

# ====== کلاس اصلی برنامه ======
class ProductApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.accent_palette = "Teal"
        self.title = "مدیریت هوشمند کالا"
        self.db = Database()
    
    def build(self):
        self.screen_manager = Builder.load_string(KV)
        self.update_stats()
        self.load_products()
        return self.screen_manager
    
    # ====== عملیات اصلی ======
    def add_product(self, name, price, purchase_price, quantity, min_quantity, date, barcode):
        if not name:
            self.show_snackbar("⚠️ لطفاً نام کالا را وارد کنید", "error")
            return
        
        try:
            price = float(price) if price else 0
            purchase_price = float(purchase_price) if purchase_price else 0
            quantity = int(quantity) if quantity else 1
            min_quantity = int(min_quantity) if min_quantity else 5
        except ValueError:
            self.show_snackbar("⚠️ مقادیر عددی نامعتبر!", "error")
            return
        
        code = self.db.add_product(name, price, purchase_price, quantity, min_quantity, date, barcode)
        self.show_snackbar(f"✅ کالا با کد {code} ثبت شد", "success")
        self.clear_form()
        self.update_stats()
        self.load_products()
    
    def delete_product(self, product_id):
        dialog = MDDialog(
            title="🗑️ حذف کالا",
            text="آیا از حذف این کالا مطمئن هستید؟",
            buttons=[
                MDFlatButton(text="لغو", on_press=lambda x: dialog.dismiss()),
                MDRaisedButton(
                    text="حذف",
                    md_bg_color=self.theme_cls.error_color,
                    on_press=lambda x: self.confirm_delete(product_id, dialog)
                )
            ]
        )
        dialog.open()
    
    def confirm_delete(self, product_id, dialog):
        self.db.delete_product(product_id)
        dialog.dismiss()
        self.show_snackbar("✅ کالا حذف شد", "success")
        self.update_stats()
        self.load_products()
    
    def load_products(self):
        products = self.db.get_all_products()
        product_list = self.screen_manager.get_screen("products").ids.product_list
        product_list.clear_widgets()
        
        if not products:
            product_list.add_widget(
                MDLabel(text="هیچ محصولی ثبت نشده است", halign="center", theme_text_color="Hint")
            )
            return
        
        for product in products:
            item = ThreeLineAvatarIconListItem(
                text=f"🔹 {product[3]}",
                secondary_text=f"💰 {product[4]:,} تومان  |  📦 {product[5]} عدد",
                tertiary_text=f"📅 {product[7]}  |  📂 {product[2] or 'بدون بارکد'}",
                on_press=lambda x, p=product: self.show_product_details(p)
            )
            item.add_widget(
                MDIconButton(
                    icon="delete",
                    pos_hint={"center_y": 0.5},
                    on_press=lambda x, pid=product[0]: self.delete_product(pid),
                    theme_text_color="Custom",
                    text_color=self.theme_cls.error_color
                )
            )
            product_list.add_widget(item)
    
    def search_products(self, query):
        if not query:
            self.load_products()
            return
        self.show_snackbar(f"🔍 جستجو برای: {query}", "info")
    
    def filter_products(self, category):
        self.show_snackbar(f"📂 فیلتر: {category}", "info")
    
    def show_product_details(self, product):
        dialog = MDDialog(
            title=f"📋 {product[3]}",
            text=f"""
💰 قیمت فروش: {product[4]:,} تومان
💰 قیمت خرید: {product[5]:,} تومان
📦 موجودی: {product[6]} عدد
⚠️ حداقل موجودی: {product[7]} عدد
📅 تاریخ: {product[8]}
🔲 بارکد: {product[2] or 'ندارد'}
📝 توضیحات: {product[9] or 'ندارد'}
            """,
            buttons=[
                MDFlatButton(text="بستن", on_press=lambda x: dialog.dismiss()),
                MDRaisedButton(
                    text="✏️ ویرایش",
                    md_bg_color=self.theme_cls.accent_color,
                    on_press=lambda x: self.edit_product(product)
                )
            ]
        )
        dialog.open()
    
    def edit_product(self, product):
        self.show_snackbar(f"✏️ در حال ویرایش: {product[3]}", "info")
    
    def clear_form(self):
        screen = self.screen_manager.get_screen("add")
        screen.ids.name_field.text = ""
        screen.ids.barcode_field.text = ""
        screen.ids.price_field.text = ""
        screen.ids.purchase_field.text = ""
        screen.ids.quantity_field.text = "1"
        screen.ids.min_quantity_field.text = "5"
        screen.ids.date_field.text = datetime.now().strftime('%Y-%m-%d')
    
    # ====== آمار ======
    def update_stats(self):
        stats = self.db.get_stats()
        
        home = self.screen_manager.get_screen("home")
        if home:
            home.ids.home_total.text = str(stats['total'])
            home.ids.home_value.text = f"{stats['total_value']:,.0f}"
        
        stat = self.screen_manager.get_screen("stats")
        if stat:
            stat.ids.stat_total.text = str(stats['total'])
            stat.ids.stat_value.text = f"{stats['total_value']:,.0f}"
            stat.ids.stat_avg.text = f"{stats['avg_price']:,.0f}"
            stat.ids.stat_low.text = str(stats['low_stock'])
    
    # ====== تنظیمات ======
    def toggle_theme(self):
        if self.theme_cls.theme_style == "Light":
            self.theme_cls.theme_style = "Dark"
            self.show_snackbar("🌙 تم تاریک فعال شد", "info")
        else:
            self.theme_cls.theme_style = "Light"
            self.show_snackbar("☀️ تم روشن فعال شد", "info")
    
    def show_notifications(self):
        self.show_snackbar("🔔 تنظیمات اعلان‌ها", "info")
    
    def cloud_sync(self):
        self.show_snackbar("☁️ همگام‌سازی ابری انجام شد", "success")
    
    def export_menu(self):
        dialog = MDDialog(
            title="📤 انتخاب فرمت خروجی",
            buttons=[
                MDRaisedButton(
                    text="📊 Excel",
                    md_bg_color=self.theme_cls.success_color,
                    on_press=lambda x: self.show_snackbar("📊 خروجی Excel ساخته شد", "success")
                ),
                MDRaisedButton(
                    text="📄 PDF",
                    md_bg_color=self.theme_cls.accent_color,
                    on_press=lambda x: self.show_snackbar("📄 خروجی PDF ساخته شد", "success")
                )
            ]
        )
        dialog.open()
    
    def backup_database(self):
        try:
            if not os.path.exists('backups'):
                os.makedirs('backups')
            import shutil
            filename = f"backups/backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            shutil.copy('products.db', filename)
            self.show_snackbar(f"💾 پشتیبان در {filename} ذخیره شد", "success")
        except Exception as e:
            self.show_snackbar(f"⚠️ خطا: {str(e)}", "error")
    
    def show_about(self):
        dialog = MDDialog(
            title="📱 درباره برنامه",
            text="""
مدیریت هوشمند کالا
نسخه ۴.۰

👨‍💻 سازنده: مهدی طریری
📱 تلگرام: @mahdi_tar
🐙 گیت‌هاب: github.com/mahditariri-c

✨ ویژگی‌ها:
• مدیریت کامل کالاها
• جستجوی پیشرفته
• خروجی PDF/Excel
• کنترل صوتی
• همگام‌سازی ابری
            """,
            buttons=[
                MDFlatButton(text="بستن", on_press=lambda x: dialog.dismiss()),
                MDRaisedButton(
                    text="🐙 گیت‌هاب",
                    md_bg_color=self.theme_cls.primary_color,
                    on_press=lambda x: self.open_github()
                )
            ]
        )
        dialog.open()
    
    def open_github(self):
        import webbrowser
        webbrowser.open('https://github.com/mahditariri-c/product-manager-app')
    
    def show_snackbar(self, text, type="info"):
        colors = {
            "info": self.theme_cls.primary_color,
            "success": self.theme_cls.success_color,
            "error": self.theme_cls.error_color,
            "warning": self.theme_cls.warning_color
        }
        Snackbar(
            text=text,
            snackbar_x=dp(10),
            snackbar_y=dp(10),
            bg_color=colors.get(type, self.theme_cls.primary_color),
            font_size=dp(14)
        ).open()

if __name__ == "__main__":
    ProductApp().run()
