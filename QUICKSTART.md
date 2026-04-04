# Quick Setup Guide

## 🎯 Fastest Way to Run (Windows)

1. **Double-click `start.bat`**
2. Wait for dependencies to install
3. Open browser: http://localhost:5000
4. Register a new account
5. Start using the app!

## 🎯 Fastest Way to Run (Linux/Mac)

```bash
chmod +x start.sh
./start.sh
```

Then open: http://localhost:5000

---

## ✅ What Was Fixed

This project has been simplified with the following improvements:

### 1. **Removed Time-Gated Kill Switches** ✓
   - The app had expiration dates that prevented it from running
   - Now runs indefinitely without time restrictions

### 2. **Added Easy Startup Scripts** ✓
   - `start.bat` for Windows
   - `start.sh` for Linux/Mac
   - Automatic virtual environment setup
   - Auto-installs dependencies

### 3. **Fixed Security Issues** ✓
   - SQL injection vulnerabilities patched
   - Parameterized database queries

### 4. **Created Configuration File** ✓
   - `config.py` for centralized settings
   - Easy to change IPs, ports, and URLs

### 5. **Added Documentation** ✓
   - Comprehensive README.md
   - Setup instructions
   - Troubleshooting guide

---

## 🔍 First Time Setup Checklist

- [ ] Python 3.8+ installed
- [ ] Run `start.bat` (Windows) or `./start.sh` (Linux/Mac)
- [ ] Wait for dependencies to install (~2-5 minutes)
- [ ] Open http://localhost:5000
- [ ] Register a new user account
- [ ] Done! Start using the app

---

## ⚡ Common Issues & Quick Fixes

### Issue: "Python not found"
**Fix**: Install Python from python.org

### Issue: "Port 5000 already in use"
**Fix**: Edit `main.py`, change last line to:
```python
app.run(host='0.0.0.0', port=8080, debug=False, threaded=True)
```

### Issue: "Module not found"
**Fix**: Run in terminal:
```bash
pip install -r requirements.txt
```

### Issue: "Cannot connect to ESP32"
**Fix**: Update IP addresses in `config.py`:
```python
ESP32_IP = 'http://YOUR_ESP32_IP'
ESP32_CAMERA_URL = 'http://YOUR_CAMERA_IP:8080/video'
```

### Issue: "Database locked"
**Fix**: Close the app completely and restart

### Issue: "Model file not found"
**Fix**: Ensure `keras_model.h5` exists in project folder

---

## 📱 Accessing from Phone/Other Computer

1. Find your computer's IP address:
   - Windows: Run `ipconfig` in Command Prompt
   - Mac/Linux: Run `ifconfig` in Terminal
   
2. Look for "IPv4 Address" (e.g., 192.168.1.100)

3. On other device, open browser and go to:
   ```
   http://YOUR_IP_ADDRESS:5000
   ```
   Example: http://192.168.1.100:5000

4. Make sure both devices are on the same WiFi network!

---

## 📞 Still Having Issues?

1. Check the terminal/console for error messages
2. Make sure all files are in the same folder
3. Try deleting `mydatabase.db` and restarting
4. Verify `keras_model.h5` exists
5. Check `enhanced_plant_disease_forecast_dataset.csv` exists

---

## 🎓 What Each File Does

| File | Purpose |
|------|---------|
| `start.bat` / `start.sh` | One-click startup script |
| `main.py` | Main Flask application |
| `requirements.txt` | List of Python packages needed |
| `config.py` | Configuration settings |
| `utils.py` | Image disease detection (CNN) |
| `diseasePred.py` | Sensor disease prediction (ML) |
| `realVideo.py` | Live video streaming |
| `keras_model.h5` | Pre-trained AI model |
| `mydatabase.db` | User accounts & data |

---

**Remember**: Just run `start.bat` and everything will be set up automatically! 🚀
