# 🚄 Deploying SkillArena on Railway

Railway is a great choice for this project because it handles Docker, PostgreSQL, and Redis effortlessly.

## 1. Prepare your GitHub Repo
Ensure you have pushed the latest changes (including the Dockerfile update I just made):
```bash
git add .
git commit -m "Prepare for Railway deployment"
git push
```

## 2. Deploy on Railway

1.  **Go to [Railway.app](https://railway.app/)** and log in with GitHub.
2.  **Click "New Project"** -> "Deploy from GitHub repo".
3.  **Select your `SkillArena` repository**.
4.  **Important**: Railway will detect multiple Dockerfiles. You should set up three services in the same project:

### Service A: Backend
- **Root Directory**: `skillarena-backend`
- **Environment Variables**:
  - `DATABASE_URL`: (Will be provided by the Postgres service)
  - `REDIS_URL`: (Will be provided by the Redis service)
  - `SECRET_KEY`: `your-random-secret-key`
  - `FRONTEND_URL`: `https://your-frontend-url.up.railway.app` (Update this once frontend is deployed)

### Service B: Frontend
- **Root Directory**: `skillarena-frontend`
- **Environment Variables**:
  - `VITE_API_BASE_URL`: `https://your-backend-url.up.railway.app`

### Service C & D: Database & Redis
- Click **"New"** -> **"Database"** -> **"Add PostgreSQL"**.
- Click **"New"** -> **"Database"** -> **"Add Redis"**.

## 3. Connecting Services
Once the Postgres and Redis services are created:
1.  Go to your **Backend** service settings.
2.  Go to the **Variables** tab.
3.  Click **"New Variable"** -> **"Reference"** and select the Postgres and Redis URLs. Railway makes this very easy!

## 4. Final Polish
Once both are live, ensure the `FRONTEND_URL` in the backend and `VITE_API_BASE_URL` in the frontend are pointing to each other's Railway URLs.
