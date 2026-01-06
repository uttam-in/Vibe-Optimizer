# SmartX AI Dashboard Deployment Guide

## Local Development

The dashboard is currently running at:
- **Local URL**: http://localhost:8502
- **Network URL**: http://192.168.1.84:8502

### Run Locally
```bash
.conda\python.exe -m streamlit run dashboard_app.py --server.port 8502
```

## Deployment Options

### Option 1: Streamlit Cloud (Recommended)

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Select `dashboard_app.py` as the main file
5. Add environment variables if needed
6. Deploy!

**Requirements file**: `dashboard_requirements.txt`

### Option 2: Vercel with Custom Server

Since Streamlit requires a persistent WebSocket connection, standard Vercel deployment won't work. However, you can:

1. Use Vercel for the static landing page (index.html)
2. Deploy the Streamlit dashboard separately on:
   - Streamlit Cloud (free)
   - Heroku
   - AWS EC2
   - Google Cloud Run
   - Azure App Service

### Option 3: Docker Deployment

Create a `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY dashboard_requirements.txt .
RUN pip install -r dashboard_requirements.txt

COPY dashboard_app.py .
COPY .streamlit .streamlit

EXPOSE 8502

CMD ["streamlit", "run", "dashboard_app.py", "--server.port=8502", "--server.address=0.0.0.0"]
```

Deploy to any container platform:
- Google Cloud Run
- AWS ECS
- Azure Container Instances
- DigitalOcean App Platform

## Environment Variables

If using Exa API in production, set:
```
EXA_API_KEY=your_api_key_here
```

## Features

- 🏠 **Home Dashboard**: Overview metrics and activity feed
- 🔍 **AI Search**: Web search and code context using Exa
- 📊 **Analytics**: Search volume, query types, response times
- 💡 **Insights**: Trending topics and key insights
- ⚙️ **Settings**: API configuration and preferences

## Current Status

✅ Dashboard created and running locally
✅ UI designed with SmartX branding
✅ Exa integration structure in place
⏳ Ready for cloud deployment
