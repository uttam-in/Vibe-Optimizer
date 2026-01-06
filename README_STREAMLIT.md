# SmartX AI Dashboard - Streamlit Deployment

## 🚀 Quick Deploy to Streamlit Cloud

### Prerequisites
- GitHub account
- Streamlit Cloud account (free at [share.streamlit.io](https://share.streamlit.io))

### Deployment Steps

1. **Push to GitHub**
   ```bash
   git add dashboard_app.py requirements-streamlit.txt .streamlit/
   git commit -m "Add Streamlit dashboard"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your repository: `uttam-in/Vibe-Optimizer`
   - Set main file path: `dashboard_app.py`
   - Set Python version: `3.10`
   - Click "Deploy"

3. **Configure Secrets (Optional)**
   - In Streamlit Cloud dashboard, go to your app settings
   - Click "Secrets"
   - Add your Exa API key:
     ```toml
     [exa]
     api_key = "your_actual_api_key"
     ```

### App URL
After deployment, your app will be available at:
`https://[your-app-name].streamlit.app`

### Features
- 🏠 Home Dashboard with metrics
- 🔍 AI Search powered by Exa
- 📊 Analytics and visualizations
- 💡 Insights and trends
- ⚙️ Settings configuration

### Local Development
```bash
streamlit run dashboard_app.py --server.port 8502
```

### Troubleshooting

**Issue**: Module not found
- **Solution**: Ensure `requirements-streamlit.txt` is in the root directory

**Issue**: App won't start
- **Solution**: Check Streamlit Cloud logs for errors

**Issue**: Secrets not working
- **Solution**: Verify secrets are added in Streamlit Cloud settings

### Support
For issues, contact SmartX Technologies support or check the [Streamlit documentation](https://docs.streamlit.io).
