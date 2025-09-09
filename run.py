#!/usr/bin/env python3
"""
UzIPTV - Single File Runner
Bitta fayl bosish bilan ishga tushuvchi skript
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def check_python_version():
    """Python versiyasini tekshirish"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 yoki yuqori versiya kerak!")
        print(f"Hozirgi versiya: {sys.version}")
        sys.exit(1)
    print(f"✅ Python versiyasi: {sys.version.split()[0]}")

def check_and_create_venv():
    """Virtual environment yaratish yoki tekshirish"""
    venv_path = Path("venv")
    
    if not venv_path.exists():
        print("📦 Virtual environment yaratilmoqda...")
        result = subprocess.run([sys.executable, "-m", "venv", "venv"], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Virtual environment yaratishda xatolik: {result.stderr}")
            sys.exit(1)
        print("✅ Virtual environment yaratildi")
    else:
        print("✅ Virtual environment mavjud")

def get_venv_python():
    """Virtual environment ichidagi python path"""
    if os.name == 'nt':  # Windows
        return Path("venv/Scripts/python.exe")
    else:  # Linux/Mac
        return Path("venv/bin/python")

def install_requirements():
    """Requirements.txt dan paketlarni o'rnatish"""
    venv_python = get_venv_python()
    
    print("📚 Paketlar o'rnatilmoqda...")
    
    # pip ni yangilash
    subprocess.run([str(venv_python), "-m", "pip", "install", "--upgrade", "pip"], 
                  capture_output=True)
    
    # Requirements o'rnatish
    result = subprocess.run([str(venv_python), "-m", "pip", "install", "-r", "requirements.txt"], 
                           capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ Paketlar o'rnatishda xatolik: {result.stderr}")
        print("⚠️ Ba'zi paketlar o'rnatilmagan bo'lishi mumkin, lekin davom etamiz...")
    else:
        print("✅ Barcha paketlar o'rnatildi")

def create_env_file():
    """Agar .env fayl bo'lmasa, .env.example dan yaratish"""
    env_path = Path(".env")
    env_example_path = Path(".env.example")
    
    if not env_path.exists() and env_example_path.exists():
        print("🔧 .env fayl yaratilmoqda...")
        with open(env_example_path, 'r', encoding='utf-8') as src:
            content = src.read()
        with open(env_path, 'w', encoding='utf-8') as dst:
            dst.write(content)
        print("✅ .env fayl yaratildi")
    elif env_path.exists():
        print("✅ .env fayl mavjud")

def check_database():
    """Ma'lumotlar bazasini tekshirish va yaratish"""
    try:
        # Virtual environment ichidagi python bilan database yaratish
        venv_python = get_venv_python()
        
        init_script = '''
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), "src"))

try:
    from main import app
    from database import db, init_database
    
    with app.app_context():
        # Try to create tables
        db.create_all()
        init_database(app)
    print("✅ Database initialized successfully")
except Exception as e:
    error_msg = str(e)
    if "mapper" in error_msg.lower() or "foreign" in error_msg.lower():
        print(f"❌ Database schema error: {e}")
        print("🔧 Database ni qayta yaratish kerak - Reset_Database.bat ishga tushiring")
    else:
        print(f"⚠️ Database initialization warning: {e}")
        print("Application will try to create tables on startup")
'''
        
        result = subprocess.run([str(venv_python), "-c", init_script], 
                               capture_output=True, text=True, cwd=os.getcwd())
        
        if "✅ Database initialized successfully" in result.stdout:
            print("✅ Ma'lumotlar bazasi tayyor")
        elif "❌ Database schema error" in result.stdout:
            print("❌ Ma'lumotlar bazasi sxemasida xatolik!")
            print("🔧 Hal qilish: Reset_Database.bat ni ishga tushiring")
            print("   yoki: python reset_db.py")
            return False
        else:
            print("⚠️ Ma'lumotlar bazasi keyinroq yaratiladi")
            
    except Exception as e:
        print(f"⚠️ Ma'lumotlar bazasi tekshirishda xatolik: {e}")
    
    return True

def start_application():
    """Ilovani ishga tushirish"""
    venv_python = get_venv_python()
    
    print("\n🚀 UzIPTV ishga tushirilmoqda...")
    print("=" * 50)
    print("🌐 Server manzillari:")
    print("   Local:   http://127.0.0.1:5000")
    print("   Network: http://192.168.x.x:5000")
    print("=" * 50)
    print("⏹️ To'xtatish uchun Ctrl+C bosing")
    print("=" * 50)
    
    # Src papkasiga o'tib main.py ni ishga tushirish
    try:
        os.chdir("src")
        result = subprocess.run([str(Path("../") / venv_python), "main.py"])
        return result.returncode
    except KeyboardInterrupt:
        print("\n\n✅ UzIPTV to'xtatildi")
        return 0
    except Exception as e:
        print(f"❌ Ilovani ishga tushirishda xatolik: {e}")
        return 1

def main():
    """Asosiy funksiya"""
    print("🎬 UzIPTV - IPTV Playlist Search & Player")
    print("=" * 50)
    
    # Barcha tekshiruvlar va sozlamalar
    check_python_version()
    check_and_create_venv()
    install_requirements()
    create_env_file()
    
    # Database tekshirish
    if not check_database():
        print("\n❌ Ma'lumotlar bazasi xatoligi tufayli dastur to'xtatildi")
        print("🔧 Avval database ni qayta yarating:")
        print("   Windows: Reset_Database.bat")
        print("   Python:  python reset_db.py")
        input("\nEnter tugmasini bosing...")
        return 1
    
    # Ilovani ishga tushirish
    return start_application()

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n✅ Dastur to'xtatildi")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Kutilmagan xatolik: {e}")
        sys.exit(1)
