#!/usr/bin/env python3
"""
Database Reset Script
Ma'lumotlar bazasini qayta yaratish skripti
"""

import os
import sys
from pathlib import Path

def reset_database():
    """Ma'lumotlar bazasini qayta yaratish"""
    
    # Change to src directory for proper imports
    os.chdir("src")
    sys.path.insert(0, os.getcwd())
    
    try:
        from main import app
        from database import db, init_database
        
        print("🗑️ Eski ma'lumotlar bazasini o'chirish...")
        
        # Delete existing database file
        db_files = [
            "../uziptv.db",
            "uziptv.db", 
            "../uziptv.sqlite",
            "uziptv.sqlite"
        ]
        
        for db_file in db_files:
            if os.path.exists(db_file):
                os.remove(db_file)
                print(f"   ✅ {db_file} o'chirildi")
        
        print("📦 Yangi ma'lumotlar bazasini yaratish...")
        
        with app.app_context():
            # Drop all tables
            db.drop_all()
            
            # Create all tables
            db.create_all()
            
            # Initialize default data
            init_database(app)
            
        print("✅ Ma'lumotlar bazasi muvaffaqiyatli yaratildi!")
        print("🚀 Endi UzIPTV.bat yoki python run.py ishga tushiring")
        
    except Exception as e:
        print(f"❌ Xatolik: {e}")
        print("📋 To'liq xatolik ma'lumoti:")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Return to original directory
        os.chdir("..")
    
    return True

if __name__ == "__main__":
    print("🔄 UzIPTV Database Reset")
    print("=" * 30)
    
    if reset_database():
        print("\n✅ Tayyor! Dasturni ishga tushiring:")
        print("   Windows: UzIPTV.bat")
        print("   Python:  python run.py")
    else:
        print("\n❌ Ma'lumotlar bazasini qayta yaratishda xatolik!")
    
    input("\nEnter tugmasini bosing...")
