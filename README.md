# 🍇 Grape Plant Disease Detection System

AI-powered web application for detecting grape leaf diseases using image classification and IoT sensor data.

## ⚡ Quick Start (Recommended)

### Windows
Simply double-click `start.bat` or run in terminal:
```batch
start.bat
```

### Linux/Mac
```bash
chmod +x start.sh
./start.sh
```

The script will automatically:
- Create a virtual environment
- Install all dependencies
- Start the Flask server at http://localhost:5000

## 📋 Manual Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone or Download the Project
```bash
cd "Python (1)"
```

### Step 2: Create Virtual Environment (Optional but Recommended)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Step 5: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 6: Run the Application
```bash
python main.py
```


The application will be accessible at: **http://localhost:5000**

## 🎯 Features

### 1. **Image-Based Disease Detection**
- Upload grape leaf images
- CNN model classifies 4 disease types:
  - Black Rot
  - Esca (Black Measles)
  - Leaf Blight (Isariopsis Leaf Spot)
  - Healthy
- Provides pesticide recommendations

### 2. **Sensor-Based Prediction**
- IoT sensor integration (ESP32/Firebase)
- Predicts diseases using:
  - Temperature
  - Humidity
  - Soil Moisture
- Multiple ML models: Decision Tree, SVM, Random Forest, ANN

### 3. **Live Video Monitoring**
- Real-time camera feed from ESP32
- Video stream processing

### 4. **User Management**
- Registration and login system
- Session management
- User feedback collection

## 📁 Project Structure

```
Python (1)/
├── main.py                 # Flask app with all routes
├── utils.py                # Image classification (CNN model)
├── diseasePred.py          # Sensor-based ML predictions
├── realVideo.py            # Video streaming
├── firebaseTest.py         # Firebase integration
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── start.bat              # Windows startup script
├── start.sh               # Linux/Mac startup script
├── keras_model.h5         # Pre-trained CNN model
├── mydatabase.db          # SQLite database (auto-created)
├── mydata/                # Training/test image datasets
├── pesticides/            # Disease treatment recommendations
├── static/                # CSS, JS, images
└── templates/             # HTML templates
```

## ⚙️ Configuration

### First-Time Setup

1. **Create Configuration File**
   ```bash
   # Copy the example config file
   cp config.example.py config.py
   ```

2. **Download Model File** (not included in repository)
   - The `keras_model.h5` file is not included due to its size (2.3 MB)
   - Download it from [your model source] or train your own model
   - Place it in the project root directory

3. **Edit `config.py`** to customize:
   ```python
   # Flask settings
   SECRET_KEY = 'your-random-secret-key'  # IMPORTANT: Change this!
   HOST = '0.0.0.0'          # Change to '127.0.0.1' for local only
   PORT = 5000

# ESP32 device IP addresses
ESP32_IP = 'http://10.1.239.192'
ESP32_CAMERA_URL = 'http://10.1.239.122:8080/video'

   # Firebase URL
   FIREBASE_URL = 'your-firebase-url-here'
   ```

**⚠️ Important**: Never commit `config.py` with sensitive information to version control!

## 🔐 Default Login

After starting the app, you'll need to register a new account at:
- http://localhost:5000/register

Then login at:
- http://localhost:5000/login

## 🚀 Usage Guide

### Image Detection
1. Navigate to **Image Prediction** page
2. Upload a grape leaf image
3. Click **Predict**
4. View disease classification and treatment recommendations

### Sensor Data
1. Go to **Sensor Data** page
2. View real-time temperature, humidity, and moisture readings
3. System automatically predicts potential diseases

### Live Video
1. Click on **Video Feed** 
2. View live camera stream from IoT device

## 🔧 Troubleshooting

### Port Already in Use
```bash
# Change port in config.py or use different port:
python main.py --port 8000
```

### Database Errors
- Delete `mydatabase.db` and restart the app to recreate it

### Model Not Found
- Ensure `keras_model.h5` exists in the project root
- Download the model file separately (not included in Git repository)
- Or train your own model using the dataset in `mydata/`
- Check `enhanced_plant_disease_forecast_dataset.csv` is present

### ESP32 Connection Issues
- Update IP addresses in `config.py`
- Ensure ESP32 is on the same network
- Test ESP32 connectivity: `ping 10.1.239.192`

### Missing Dependencies
```bash
pip install --upgrade -r requirements.txt
```

## 📊 ML Models

### Image Classification
- **Model**: Keras CNN
- **Input**: 224×224 RGB images
- **Output**: Disease class + confidence score

### Sensor-Based Prediction
- **Decision Tree**: Fast, interpretable
- **SVM**: High accuracy for non-linear data
- **Random Forest**: Ensemble robustness
- **ANN (MLP)**: Deep learning approach

## 🛡️ Security Notes

- Change `SECRET_KEY` in `config.py` for production
- Use environment variables for sensitive data
- Implement HTTPS for production deployment
- Current SQL queries are parameterized to prevent injection

## 📱 Access from Other Devices

The app runs on `0.0.0.0:5000` by default, making it accessible from other devices on your network.

Find your IP address:
```bash
# Windows
ipconfig

# Linux/Mac
ifconfig
```

Then access from other devices: `http://YOUR_IP:5000`

## 🐛 Known Limitations

- Hardcoded ESP32 IP addresses need manual configuration
- Database uses SQLite (not suitable for high concurrency)
- Video streaming requires active camera connection
- Model trained on specific grape varieties

## 📝 License

Educational/Research project

## 👥 Support

For issues or questions, check:
1. This README
2. Application logs in console
3. Error messages in web interface

---

**Quick Start**: Just run `start.bat` (Windows) or `./start.sh` (Linux/Mac) and open http://localhost:5000
