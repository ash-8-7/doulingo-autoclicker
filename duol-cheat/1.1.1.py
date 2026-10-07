import pyautogui
import time
import json
import os

# فعال‌سازی ویژگی ایمنی: اگر موس را سریع به گوشه‌ی بالا-چپ صفحه ببرید، برنامه متوقف می‌شود.
pyautogui.FAILSAFE = True

CONFIG_FILE = "bot_config.json"

# تنظیمات پیش‌فرض
default_config = {
    "start_button_x": 0,
    "start_button_y": 0,
    "loop_delay": 10,          # زمان انتظار (ثانیه) برای اتمام مرحله و شروع مجدد
    "action_delay": 2,         # زمان انتظار بعد از کلیک روی استارت برای لود شدن مرحله
    "page_load_delay": 5,      # زمان انتظار برای لود شدن صفحه بعد از رفرش (فعال کردن F5)
    "key_delay": 0.3           # تاخیر بین هر کلید زدن
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    else:
        return default_config

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)
    print(f"تنظیمات در فایل {CONFIG_FILE} ذخیره شد.")

def setup_coordinates(config):
    print("\n--- تنظیم مختصات ---")
    print("لطفاً صفحه مرورگر خود را باز کنید و صفحه دولینگو را بیاورید.")
    print("شما ۵ ثانیه وقت دارید تا موس خود را روی دکمه 'START +10 XP' ببرید و آن را حرکت ندهید...")
    
    for i in range(5, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    x, y = pyautogui.position()
    config["start_button_x"] = x
    config["start_button_y"] = y
    print(f"مختصات ثبت شد: X={x}, Y={y}")
    save_config(config)

def run_bot():
    config = load_config()
    
    if config["start_button_x"] == 0 and config["start_button_y"] == 0:
        print("مختصات دکمه استارت تنظیم نشده است. لطفاً برنامه را مجدداً اجرا کرده و گزینه y را انتخاب کنید.")
        return

    print("\nربات در حال آماده‌سازی است...")
    print("لطفاً پنجره مرورگر خود را باز کنید و روی آن کلیک کنید تا فوکوس روی مرورگر باشد.")
    print("شروع عملیات در ۵ ثانیه دیگر...")
    time.sleep(5)

    cycle_count = 1
    while True:
        print(f"\n--- شروع سیکل شماره {cycle_count} ---")
        
        # 1. رفرش کردن صفحه برای برگشتن به بالای صفحه
        print("در حال رفرش کردن صفحه (F5) برای برگشت به بالا...")
        pyautogui.hotkey('f5')
        
        # صبر برای لود شدن کامل صفحه بعد از رفرش
        print(f"انتظار برای لود شدن صفحه ({config['page_load_delay']} ثانیه)...")
        time.sleep(config['page_load_delay'])
        
        # 2. کلیک روی دکمه استارت
        print("کلیک روی دکمه استارت...")
        pyautogui.click(config["start_button_x"], config["start_button_y"])
        
        # صبر برای لود شدن مرحله جدید
        time.sleep(config["action_delay"])
        
        # 3. فاز اول: ۲۰ بار زدن عدد ۱ و اینتر
        print("فاز ۱: ۲۰ بار عدد ۱ + اینتر...")
        for _ in range(20):
            pyautogui.press('1')
            time.sleep(config["key_delay"])
            pyautogui.press('enter')
            time.sleep(config["key_delay"])
            
        time.sleep(1)
        
        # 4. فاز دوم: الگوی اعداد ۱ تا ۴ با ۵ تا ۸
        print("فاز ۲: الگوی مچ کردن اعداد (1->5, 1->6, ...)...")
        for i in range(1, 5):       # اعداد 1, 2, 3, 4
            for j in range(5, 9):   # اعداد 5, 6, 7, 8
                pyautogui.press(str(i))
                time.sleep(config["key_delay"])
                pyautogui.press(str(j))
                time.sleep(config["key_delay"])
                
        time.sleep(1)
        
        # 5. فاز سوم: ۷ بار تکرار الگوی (اینتر -> 2 -> اینتر)
        print("فاز ۳: ۷ بار تکرار الگوی (اینتر -> 2 -> اینتر)...")
        for _ in range(7):
            pyautogui.press('enter')
            time.sleep(config["key_delay"])
            pyautogui.press('2')
            time.sleep(config["key_delay"])
            pyautogui.press('enter')
            time.sleep(config["key_delay"])

        time.sleep(1)
        
        # 6. فاز چهارم: زدن اینتر ۶ بار
        print("فاز ۴: زدن اینتر ۶ بار...")
        for _ in range(6):
            pyautogui.press('enter')
            time.sleep(config["key_delay"])
            
        # 7. انتظار برای اتمام مرحله و شروع مجدد
        print(f"مرحله تمام شد. انتظار برای {config['loop_delay']} ثانیه...")
        time.sleep(config["loop_delay"])
        cycle_count += 1

if __name__ == "__main__":
    print("به بات اتوکلیکر دولینگو خوش آمدید!")
    current_config = load_config()
    
    choice = input("آیا می‌خواهید مختصات دکمه استارت را دوباره تنظیم کنید؟ (y/n): ").lower()
    if choice == 'y':
        setup_coordinates(current_config)
    
    print("\nتنظیمات فعلی:")
    print(json.dumps(load_config(), indent=4))
    print("نکته: برای تغییر زمان‌ها، فایل bot_config.json را ویرایش کنید.")
    
    input("برای شروع بات، کلید Enter را فشار دهید...")
    
    run_bot()