# Deployment Guide for Streamlit Cloud

## Prerequisites
- GitHub repository with this project
- Streamlit Cloud account (free at streamlit.io/cloud)

## Files Required for Deployment

The following files are essential for Streamlit Cloud deployment:

### 1. `streamlit_app.py` (Main Entry Point)
This is the entry point that Streamlit Cloud will run. It properly sets up the Python path and imports.

### 2. `requirements.txt`
Contains all Python dependencies. Make sure this file includes:
```
pandas>=2.0.0
numpy>=1.24.0
emoji>=2.10.0
textblob>=0.17.0
vaderSentiment>=3.3.2
matplotlib>=3.7.0
seaborn>=0.13.0
plotly>=5.18.0
wordcloud>=1.9.0
streamlit>=1.29.0
python-dateutil>=2.8.2
pytz>=2.023.3
```

### 3. `packages.txt` (System Dependencies)
Contains system-level packages needed for matplotlib:
```
libgl1-mesa-glx
```

### 4. `.streamlit/config.toml` (Optional)
Streamlit configuration for theme and settings.

## Deployment Steps

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Prepare for Streamlit Cloud deployment"
git push origin main
```

### Step 2: Deploy on Streamlit Cloud

1. Go to https://streamlit.io/cloud
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository: `projects-on-python/whatsapp-chat-analyzer`
5. Set the main file path: `streamlit_app.py`
6. Click "Deploy"

### Step 3: Configure Settings (if needed)

In Streamlit Cloud dashboard:
- **Python version**: 3.9 or higher
- **Main file**: `streamlit_app.py`
- **Requirements file**: `requirements.txt` (auto-detected)

## Project Structure

```
whatsapp-chat-analyzer/
├── streamlit_app.py          # Entry point for Streamlit Cloud
├── requirements.txt           # Python dependencies
├── packages.txt              # System dependencies
├── setup.py                  # Package installation script
├── .streamlit/
│   └── config.toml          # Streamlit configuration
├── src/
│   └── whatsapp_analyzer/
│       ├── __init__.py
│       ├── parser.py
│       ├── analyzer.py
│       ├── visualizer.py
│       ├── group_analyzer.py
│       └── app.py           # Main application logic
├── tests/
├── data/
└── README.md
```

## Troubleshooting

### ModuleNotFoundError: emoji
**Solution**: Ensure `emoji>=2.10.0` is in `requirements.txt`

### Import errors
**Solution**: Use `streamlit_app.py` as the entry point, not `src/whatsapp_analyzer/app.py`

### Matplotlib errors
**Solution**: Ensure `packages.txt` contains `libgl1-mesa-glx`

### App not loading
**Solution**: Check Streamlit Cloud logs in the "Manage app" menu

## Updating the Deployed App

After making changes:
```bash
git add .
git commit -m "Update feature"
git push origin main
```

Streamlit Cloud will automatically redeploy your app within 1-2 minutes.

## Local Testing

Before deploying, test locally:
```bash
# Install dependencies
pip install -r requirements.txt

# Run with streamlit
streamlit run streamlit_app.py
```

## Environment Variables

If you need to add secrets or environment variables:
1. Go to Streamlit Cloud dashboard
2. Click on your app
3. Go to Settings → Secrets
4. Add your secrets in TOML format

## Performance Tips

For better performance on Streamlit Cloud:
- Keep uploaded file sizes under 200MB
- Use caching with `@st.cache_data` where appropriate
- Optimize DataFrame operations
- Use `st.spinner()` for long-running operations

## Support

If issues persist:
- Check Streamlit Cloud logs
- Visit Streamlit Community Forum
- Check this project's GitHub Issues
