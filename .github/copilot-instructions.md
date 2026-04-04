# Grape Plant Disease Detection System

Flask-based IoT + AI web application for grape vineyard monitoring with image and sensor-based disease prediction.

## Architecture

**Data Flow**: IoT Sensor → Firebase/ESP32 → `diseasePred.py` → Flask Route → Jinja2 Template

**Core Files**:
- `main.py` — Flask app, all routes, SQLite DB operations
- `utils.py` — Keras CNN for grape leaf image classification (4 classes)
- `diseasePred.py` — Sensor-based ML models (Decision Tree, SVM, Random Forest, ANN)
- `firebaseTest.py` — Firebase Realtime DB reader
- `realVideo.py` — OpenCV MJPEG video streaming

## Code Conventions

### Flask Routes
- Use tabs for indentation (not spaces)
- Global `name` variable tracks logged-in user — pass to all templates: `render_template('page.html', name=name)`
- All imports at top: Flask internals first, then local modules (`from utils import *`, etc.)

### Database (SQLite)
- **CRITICAL**: Use parameterized queries `execute("SELECT ... WHERE col=?", (value,))`
- **NEVER** use f-strings in SQL: ~~`f"SELECT ... WHERE col='{value}'"`~~ ← SQL injection risk
- Tables: `Users`, `botUsers`, `Feedback` (see schema in `main.py`)

### ML Predictions
- Image: `predict()` from `utils.py` → returns `[disease_name, pesticide_text]`
  - Reads `static/img/test.jpg`, expects 224×224 RGB normalized to [-1, 1]
- Sensor: `predict_disease_with_dtc(temp, humidity, moisture)` from `diseasePred.py` → returns disease string
  - Always cast inputs to `float()`

### Templates
- All extend `layout.html`: `{% extends 'layout.html' %}{% block content %}...{% endblock %}`
- Bootstrap 4 + SB Admin 2 theme
- Pass data as Jinja2 context variables from route

### External APIs
- Firebase: `readFirebase()` → `(temp, humidity, moisture)` as strings
- ESP32: `readESP32()` from `http://10.1.239.192/data` → JSON with temp/humidity/soil_moisture
- ESP32 robot: GET to `http://10.1.239.192/move?dir=<direction>`

## Known Issues

1. **Time-gated kill switch**: `run` flag in `diseasePred.py` and `realVideo.py` based on timestamp — app stops working after April 2026
2. **Deprecated API**: `Image.ANTIALIAS` in `utils.py` (use `Image.Resampling.LANCZOS` in Pillow 10+)
3. **Hardcoded IPs**: ESP32 and Firebase URLs in source
4. **SQL injection**: Some queries in `main.py` use f-strings (needs fixing)

## Build and Test

**Install**:
```bash
pip install flask tensorflow pillow firebase requests opencv-python pandas scikit-learn
```

**Run**:
```bash
python main.py
```
App runs on `http://0.0.0.0:5000` (accessible from LAN)

**Test Flow**:
1. Register/login at `/register` → `/login`
2. Upload grape leaf image at `/image` → see prediction at `/image_test`
3. View sensor readings at `/sensor` (Firebase) or `/botdata` (ESP32)
4. Live camera at `/video`

## Security Rules

- Always parameterize SQL queries
- Validate file uploads (MIME type, extension) before saving to `static/img/`
- Never log passwords or sensitive data

## Custom Agents

Two specialized agents for this project:
- `@Task Planner` — analyze codebase, create implementation plans (read-only)
- `@Task Implementor` — execute plans, write code following conventions
