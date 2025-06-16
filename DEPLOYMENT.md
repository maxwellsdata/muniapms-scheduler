
# Deployment Guide for MuniAPMs Task Scheduler

## Streamlit Cloud Deployment (Recommended)

### Prerequisites
- GitHub account
- Streamlit Cloud account (free at share.streamlit.io)

### Step-by-Step Deployment

1. **Upload to GitHub**
   - Create a new repository on GitHub
   - Upload all files from this directory to the repository
   - Ensure the repository is public or accessible to Streamlit Cloud

2. **Deploy on Streamlit Cloud**
   - Go to https://share.streamlit.io
   - Sign in with your GitHub account
   - Click "New app"
   - Select your repository
   - Set the main file path to: `app.py`
   - Click "Deploy"

3. **Configuration**
   - The app will automatically use the settings in `.streamlit/config.toml`
   - No additional configuration needed for basic deployment

### Local Development

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Locally**
   ```bash
   streamlit run app.py
   ```

3. **Access the App**
   - Open your browser to http://localhost:8501

### Environment Requirements

- Python 3.8 or higher
- All dependencies listed in requirements.txt
- No database required (uses Streamlit session state)
- No external API keys needed

### Troubleshooting

**Common Issues:**

1. **App won't start**
   - Check that all files are uploaded correctly
   - Verify requirements.txt is present
   - Ensure Python version compatibility

2. **Styling issues**
   - Verify .streamlit/config.toml is uploaded
   - Check that custom CSS is loading properly

3. **Schedule generation errors**
   - Ensure all team members have availability set
   - Check for valid day selections
   - Verify constraint logic is working

### Performance Optimization

- App is optimized for small teams (<10 people)
- Uses minimal memory with session state
- No persistent storage required
- Fast schedule generation (<1 second)

### Security Considerations

- No sensitive data stored
- All processing happens client-side in browser
- No external API calls
- Safe for internal company use

### Support

For deployment issues:
1. Check Streamlit Cloud logs
2. Verify all files are present in repository
3. Test locally first before deploying
4. Contact MuniAPMs IT team for assistance

### Updates and Maintenance

To update the deployed app:
1. Make changes to your local files
2. Push changes to GitHub repository
3. Streamlit Cloud will automatically redeploy
4. Changes typically take 1-2 minutes to appear

### Backup and Recovery

- All code is stored in GitHub repository
- No data persistence means no backup needed
- Easy to redeploy from scratch if needed
- Export functionality allows users to save schedules locally
