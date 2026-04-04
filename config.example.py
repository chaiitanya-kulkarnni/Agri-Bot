"""
Configuration file for Grape Plant Disease Detection System
Centralized settings for easy management

IMPORTANT: Copy this file to config.py and update with your actual values
DO NOT commit config.py with sensitive information to version control
"""

# Flask Configuration
SECRET_KEY = 'your-secret-key-here-change-this'  # Change this to a random secret key
HOST = '0.0.0.0'
PORT = 5000
DEBUG = False  # Set to True for development

# Database Configuration
DATABASE_NAME = 'mydatabase.db'

# ESP32 Configuration (IoT Device)
ESP32_IP = 'http://YOUR_ESP32_IP_HERE'  # Replace with your ESP32 IP
ESP32_CAMERA_URL = 'http://YOUR_CAMERA_IP_HERE:8080/video'  # Replace with your camera URL

# Firebase Configuration
# Add your Firebase credentials here if using Firebase
FIREBASE_URL = 'your-firebase-url-here'

# Model Configuration
KERAS_MODEL_PATH = 'keras_model.h5'
DATASET_PATH = 'enhanced_plant_disease_forecast_dataset.csv'

# Image Configuration
UPLOAD_FOLDER = 'static/img'
TEST_IMAGE_PATH = 'static/img/test.jpg'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# ML Model Parameters
DISEASE_CLASSES = [
    'Grape___Black_rot',
    'Grape___Esca_(Black_Measles)',
    'Grape___healthy',
    'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)'
]
