# 🚀 UzIPTV Online Deployment Guide

UzIPTV dasturini onlayn qo'yish uchun bir necha variant mavjud:

## 1️⃣ Render.com (Tavsiya etiladi - Bepul)

### Avzalliklari:
- ✅ Bepul hosting
- ✅ Avtomatik deployment
- ✅ SSL sertifikat
- ✅ GitHub integratsiyasi

### Qadamlar:
1. GitHub'ga repository yarating
2. Render.com'da account oching
3. Web Service yarating
4. Repository ulang
5. Deploy qiling

## 2️⃣ Railway.app (Oson deployment)

### Avzalliklari:
- ✅ Oson setup
- ✅ Avtomatik scaling
- ✅ Database bilan
- ✅ $5/month dan boshlanadi

## 3️⃣ Heroku (Classic choice)

### Avzalliklari:
- ✅ Kuchli platform
- ✅ Add-onlar ko'p
- ✅ PostgreSQL database
- ✅ $7/month

## 4️⃣ PythonAnywhere (Python-specific)

### Avzalliklari:
- ✅ Python-ga mo'ljallangan
- ✅ SSH access
- ✅ Cron jobs
- ✅ $5/month

## 5️⃣ Vercel (Frontend-focused)

### Avzalliklari:
- ✅ CDN bilan
- ✅ Serverless functions
- ✅ GitHub integratsiyasi
- ✅ Bepul plan

---

# 🛠 Quick Deployment

## Method 1: Automatic Script
```bash
python deploy.py
```
Bu script barcha kerakli sozlamalarni qiladi va deployment variantlarini ko'rsatadi.

## Method 2: Manual Deployment

### Render.com (BEPUL - Tavsiya etiladi)

1. **Repository yarating:**
   - GitHub'da yangi repository yarating
   - Kodlarni upload qiling

2. **Render.com'da:**
   - https://render.com ga kiring
   - "New Web Service" tugmasini bosing
   - GitHub repository'ni ulang
   - Quyidagi sozlamalarni kiriting:
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `cd src && gunicorn --bind 0.0.0.0:$PORT main:app`
     - **Environment:** Python 3

3. **Environment Variables:**
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=False
   HOST=0.0.0.0
   PORT=10000
   ```

4. **Deploy tugmasini bosing!**

### Heroku (Classic)

1. **Heroku CLI o'rnating:**
   ```bash
   # Windows
   winget install heroku-cli
   
   # Mac
   brew tap heroku/brew && brew install heroku
   ```

2. **Deploy qiling:**
   ```bash
   heroku create your-app-name
   heroku addons:create heroku-postgresql:hobby-dev
   git push heroku main
   heroku open
   ```

### Railway.app (Zamonaviy)

1. https://railway.app ga kiring
2. GitHub bilan sign up qiling
3. "New Project" → "Deploy from GitHub repo"
4. Repository'ni tanlang
5. Avtomatik deploy bo'ladi!

### Docker (VPS/Cloud)

```bash
# Image yaratish
docker build -t uziptv .

# Ishga tushirish
docker run -d -p 8000:8000 --name uziptv-app uziptv
```

---

# 🎯 Production Optimizations
