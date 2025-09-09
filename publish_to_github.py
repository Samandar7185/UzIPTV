#!/usr/bin/env python3
"""
GitHub Publishing Script for UzIPTV
"""

import os
import subprocess
import sys
from pathlib import Path

def print_banner():
    print("""
📦 UzIPTV GitHub Publisher
==========================
    """)

def check_git_status():
    """Check git repository status"""
    try:
        # Check if we're in a git repository
        subprocess.run(['git', 'status'], capture_output=True, check=True)
        print("✅ Git repository detected")
        return True
    except subprocess.CalledProcessError:
        print("❌ Not a git repository")
        return False

def setup_git_repo():
    """Initialize git repository if needed"""
    if not Path('.git').exists():
        print("📁 Initializing git repository...")
        subprocess.run(['git', 'init'], check=True)
        subprocess.run(['git', 'branch', '-M', 'main'], check=True)
    
    # Add files
    print("📄 Adding files to git...")
    subprocess.run(['git', 'add', '.'], check=True)
    
    # Check if there are changes to commit
    result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
    if result.stdout.strip():
        # Commit changes
        commit_message = input("Enter commit message (default: 'Initial UzIPTV commit'): ").strip()
        if not commit_message:
            commit_message = "Initial UzIPTV commit"
        
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        print(f"✅ Committed with message: {commit_message}")
    else:
        print("✅ No changes to commit")

def publish_to_github():
    """Publish repository to GitHub"""
    print("\n🚀 Publishing to GitHub...")
    
    repo_name = input("Enter GitHub repository name (default: uziptv): ").strip()
    if not repo_name:
        repo_name = "uziptv"
    
    print("\n📋 Next steps:")
    print("1. Go to https://github.com/new")
    print(f"2. Create a new repository named: {repo_name}")
    print("3. Don't initialize with README (we already have files)")
    print("4. Copy the repository URL")
    
    repo_url = input("\nPaste GitHub repository URL (https://github.com/username/repo.git): ").strip()
    
    if repo_url:
        try:
            # Add remote origin
            subprocess.run(['git', 'remote', 'add', 'origin', repo_url], check=True)
            print("✅ Remote origin added")
        except subprocess.CalledProcessError:
            # Remote might already exist
            try:
                subprocess.run(['git', 'remote', 'set-url', 'origin', repo_url], check=True)
                print("✅ Remote origin updated")
            except subprocess.CalledProcessError:
                print("⚠️ Could not add remote origin")
        
        # Push to GitHub
        try:
            subprocess.run(['git', 'push', '-u', 'origin', 'main'], check=True)
            print("✅ Successfully pushed to GitHub!")
            print(f"🌐 Repository URL: {repo_url.replace('.git', '')}")
        except subprocess.CalledProcessError:
            print("❌ Failed to push to GitHub")
            print("   Make sure you have push access to the repository")

def create_readme():
    """Create or update README.md"""
    readme_content = f"""# 🎬 UzIPTV - IPTV Playlist Search & Player

Internetdan IPTV pleylistlarini qidiruvchi va ishga tushiruvchi platforma.

## ✨ Xususiyatlar

- 🔍 **Smart Search** - GitHub va IPTV-ORG dan playlist qidirish
- 📺 **Inline Player** - HLS.js bilan video o'ynash  
- 💾 **Playlist Manager** - Pleylistlarni saqlash va boshqarish
- 📊 **Analytics** - Statistika va analytics
- 📱 **Responsive** - Mobile va desktop uchun
- 🎮 **Advanced Controls** - To'liq player boshqaruvi

## 🚀 O'rnatish

### Lokal ishga tushirish:
```bash
# Repository ni clone qiling
git clone https://github.com/yourusername/uziptv.git
cd uziptv

# Bitta buyruq bilan ishga tushiring
python run.py
```

### Onlayn deploy qilish:
```bash
# Deployment assistant
python deploy.py
```

## 🌐 Live Demo

- **Demo**: [https://uziptv.onrender.com](https://uziptv.onrender.com)
- **Backup**: [https://uziptv.herokuapp.com](https://uziptv.herokuapp.com)

## 📋 Deployment Options

- ✅ **Render.com** (Bepul, tavsiya etiladi)
- ✅ **Heroku** (Classic cloud platform) 
- ✅ **Railway.app** (Modern deployment)
- ✅ **Docker** (Containerized deployment)

## 🛠 Texnologiyalar

- **Backend**: Python, Flask, SQLAlchemy
- **Frontend**: HTML5, Bootstrap 5, JavaScript
- **Player**: HLS.js, HTML5 Video
- **Database**: SQLite/PostgreSQL
- **Deployment**: Gunicorn, Docker

## 📖 API Endpoints

- `GET /` - Bosh sahifa
- `POST /api/search` - Playlist qidirish
- `POST /api/parse` - Playlist parsing
- `GET /api/channels` - Kanallar ro'yxati
- `GET /player/:id` - Video player

## 🤝 Hissa qo'shish

1. Repository ni fork qiling
2. Feature branch yarating
3. O'zgarishlar qiling
4. Pull request yuboring

## 📄 Litsenziya

MIT License - `LICENSE` faylini ko'ring.

## 🙏 Minnatdorchilik

- [IPTV-ORG](https://github.com/iptv-org/iptv) - Bepul IPTV kanallar
- [HLS.js](https://github.com/video-dev/hls.js/) - Video player
- [Bootstrap](https://getbootstrap.com/) - UI framework

---

⭐ Agar loyiha yoqsa, yulduzcha bosib qoldiring!
"""
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("✅ README.md created/updated")

def main():
    print_banner()
    
    if not check_git_status():
        setup_git_repo()
    
    create_readme()
    setup_git_repo()
    publish_to_github()
    
    print("\n🎉 Publishing completed!")
    print("\n📋 Next steps for deployment:")
    print("1. Go to https://render.com")
    print("2. Connect your GitHub account") 
    print("3. Create Web Service from your repository")
    print("4. Your app will be live in minutes!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✅ Publishing cancelled")
    except Exception as e:
        print(f"\n❌ Error: {e}")
