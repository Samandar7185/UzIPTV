#!/usr/bin/env python3
"""
UzIPTV Deployment Script
Automatic deployment to various platforms
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def print_banner():
    print("""
🚀 UzIPTV Deployment Assistant
================================
    """)

def check_requirements():
    """Check if required tools are installed"""
    required = ['git', 'python']
    missing = []
    
    for tool in required:
        try:
            subprocess.run([tool, '--version'], capture_output=True, check=True)
            print(f"✅ {tool} is installed")
        except (subprocess.CalledProcessError, FileNotFoundError):
            missing.append(tool)
            print(f"❌ {tool} is not installed")
    
    return len(missing) == 0

def setup_git_repository():
    """Initialize git repository if not exists"""
    if not Path('.git').exists():
        print("📁 Initializing Git repository...")
        subprocess.run(['git', 'init'])
        subprocess.run(['git', 'add', '.'])
        subprocess.run(['git', 'commit', '-m', 'Initial commit: UzIPTV IPTV Player'])
        print("✅ Git repository initialized")
    else:
        print("✅ Git repository already exists")

def deploy_to_render():
    """Deploy to Render.com"""
    print("\n🎯 Deploying to Render.com")
    print("1. Go to https://render.com")
    print("2. Connect your GitHub account")
    print("3. Create a new Web Service")
    print("4. Connect this repository")
    print("5. Use these settings:")
    print("   - Build Command: pip install -r requirements.txt")
    print("   - Start Command: cd src && gunicorn --bind 0.0.0.0:$PORT main:app")
    print("   - Environment: Python 3")
    print("\n📋 Environment Variables to set:")
    print("   SECRET_KEY=<generate-random-key>")
    print("   DEBUG=False")
    print("   HOST=0.0.0.0")

def deploy_to_heroku():
    """Deploy to Heroku"""
    print("\n🎯 Deploying to Heroku")
    
    # Check if Heroku CLI is installed
    try:
        subprocess.run(['heroku', '--version'], capture_output=True, check=True)
    except FileNotFoundError:
        print("❌ Heroku CLI is not installed")
        print("   Download from: https://devcenter.heroku.com/articles/heroku-cli")
        return
    
    app_name = input("Enter Heroku app name (or press Enter for auto-generated): ").strip()
    
    commands = [
        ['heroku', 'create'] + ([app_name] if app_name else []),
        ['heroku', 'addons:create', 'heroku-postgresql:hobby-dev'],
        ['git', 'push', 'heroku', 'main']
    ]
    
    for cmd in commands:
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Error: {result.stderr}")
            return
        print("✅ Command completed")

def deploy_to_railway():
    """Deploy to Railway.app"""
    print("\n🎯 Deploying to Railway.app")
    print("1. Go to https://railway.app")
    print("2. Sign up with GitHub")
    print("3. Click 'New Project'")
    print("4. Select 'Deploy from GitHub repo'")
    print("5. Choose this repository")
    print("6. Railway will automatically detect Python and deploy")

def deploy_docker():
    """Deploy using Docker"""
    print("\n🐳 Deploying with Docker")
    
    try:
        subprocess.run(['docker', '--version'], capture_output=True, check=True)
    except FileNotFoundError:
        print("❌ Docker is not installed")
        print("   Download from: https://www.docker.com/products/docker-desktop")
        return
    
    print("Building Docker image...")
    subprocess.run(['docker', 'build', '-t', 'uziptv', '.'])
    print("✅ Docker image built")
    
    print("Starting container...")
    subprocess.run(['docker', 'run', '-d', '-p', '8000:8000', '--name', 'uziptv-container', 'uziptv'])
    print("✅ Container started at http://localhost:8000")

def main():
    print_banner()
    
    if not check_requirements():
        print("❌ Please install missing requirements first")
        return
    
    setup_git_repository()
    
    print("\n🎯 Choose deployment method:")
    print("1. Render.com (Free, Recommended)")
    print("2. Heroku (Classic)")
    print("3. Railway.app (Modern)")
    print("4. Docker (Local/VPS)")
    print("5. Show all instructions")
    
    choice = input("\nEnter your choice (1-5): ").strip()
    
    if choice == '1':
        deploy_to_render()
    elif choice == '2':
        deploy_to_heroku()
    elif choice == '3':
        deploy_to_railway()
    elif choice == '4':
        deploy_docker()
    elif choice == '5':
        deploy_to_render()
        deploy_to_heroku() 
        deploy_to_railway()
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✅ Deployment cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
