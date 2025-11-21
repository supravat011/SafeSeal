# Vercel Deployment Guide for SafeSeal

## Quick Deploy to Vercel

### Step 1: Push to GitHub
```bash
cd "d:\Projects\Academic Cerdentials"
git init
git add .
git commit -m "SafeSeal platform ready for deployment"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/safeseal.git
git push -u origin main
```

### Step 2: Deploy Frontend to Vercel
1. Go to https://vercel.com
2. Click "Add New Project"
3. Import your GitHub repository
4. **Framework Preset**: Next.js (auto-detected)
5. **Root Directory**: `client`
6. Click "Deploy"

### Step 3: Deploy Backend (Choose One)

#### Option A: Vercel Serverless Functions (Recommended for Demo)
**Note**: Has 10s timeout limit

1. Create `api/` folder in root
2. Move Python backend to serverless format
3. Deploy with frontend

#### Option B: Render (Separate Backend - No Timeout)
1. Go to https://render.com
2. New Web Service
3. Connect GitHub repo
4. Root directory: `ai_backend`
5. Build: `pip install -r requirements.txt`
6. Start: `gunicorn app:app`
7. Copy backend URL

### Step 4: Connect Backend to Frontend

Add environment variable in Vercel:
```
NEXT_PUBLIC_AI_BACKEND_URL=https://your-backend.onrender.com
```

Or if using Vercel serverless:
```
NEXT_PUBLIC_AI_BACKEND_URL=/api
```

## Environment Variables

In Vercel Dashboard → Settings → Environment Variables:

```
NEXT_PUBLIC_AI_BACKEND_URL=https://your-backend-url.com
```

## Testing

1. Visit your Vercel URL: `https://your-project.vercel.app`
2. Test AI verification at `/ai-verify`
3. Upload a certificate and verify it works!

## Important Notes

### Smart Contracts
Your Hardhat node runs locally. For production:
- Deploy to testnet (Sepolia/Goerli)
- Update contract addresses in frontend
- Or use mock data for demo

### Backend Hosting
Since Python AI backend needs long processing time:
- **Recommended**: Deploy backend to Render (free, no timeout)
- **Alternative**: Use Vercel serverless (10s limit)

## Quick Commands

```bash
# Build locally to test
cd client
npm run build

# Start production server locally
npm start
```

## Deployment Checklist

- [ ] Push code to GitHub
- [ ] Deploy frontend to Vercel
- [ ] Deploy backend to Render
- [ ] Add backend URL to Vercel env vars
- [ ] Test live site
- [ ] (Optional) Deploy contracts to testnet

## Cost

- **Vercel**: FREE (Hobby plan)
- **Render**: FREE (750 hours/month)
- **Total**: $0/month! 🎉

---

**Your site will be live at**: `https://safeseal.vercel.app` (or your custom domain)
