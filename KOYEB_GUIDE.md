# 🐳 Deploying SkillArena on Koyeb (Free)

Koyeb is a great free alternative that supports Docker natively.

## 1. Setup GitHub Connection
- In the Koyeb dashboard, click **"Create Service"**.
- Select **"GitHub"** and authorize Koyeb to access your repositories.
- Select your **`SkillArena`** repository.

## 2. Deploy Backend
Create your first service for the backend:
- **Service Name**: `skillarena-backend`
- **Builder**: Keep it as **"Docker"** (Koyeb will find the Dockerfile).
- **Docker Search Path**: `skillarena-backend`
- **Exposed Port**: `8000`
- **Environment Variables**:
  - `DATABASE_URL`: (Paste your Koyeb Postgres URL here later)
  - `REDIS_URL`: (You can add a free Redis from [Upstash](https://upstash.com/) or similar if needed, or skip for now)
  - `SECRET_KEY`: `your-random-secret-key`
  - `FRONTEND_URL`: `https://your-frontend-app.koyeb.app`

## 3. Deploy Frontend
Create a second service for the frontend:
- **Service Name**: `skillarena-frontend`
- **Builder**: **"Docker"**
- **Docker Search Path**: `skillarena-frontend`
- **Exposed Port**: `80`
- **Environment Variables**:
  - `VITE_API_BASE_URL`: `https://your-backend-app.koyeb.app`

## 4. Free Database
- Go to the **"Databases"** tab in Koyeb.
- Click **"Create Database"** and select the free PostgreSQL tier.
- Once created, copy the **"Public URL"** and paste it into your Backend's `DATABASE_URL` variable.
