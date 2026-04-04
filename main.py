# import the necessary packages
from flask import Flask, render_template, redirect, url_for, request,session,Response,json
from werkzeug.utils import secure_filename
import sqlite3
import pandas as pd
from datetime import datetime
import os
from utils import *
from firebaseTest import *
from diseasePred import *
from realVideo import *
#from weather import *
#from autocorrect import Speller
#from chatgptTest import *

name = ''

#pell = Speller(lang='en')
app = Flask(__name__)

app.secret_key = '1234'
app.config["CACHE_TYPE"] = "null"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# ============ VALIDATION HELPER FUNCTIONS ============
import re

def validate_email(email):
	"""Validate email format"""
	pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
	return re.match(pattern, email) is not None

def validate_password(password):
	"""Validate password strength (min 6 chars)"""
	return len(password) >= 6

def validate_phone(phone):
	"""Validate phone number format"""
	cleaned = phone.replace('+','').replace('-','').replace(' ','').replace('(','').replace(')','')
	return cleaned.isdigit() and 10 <= len(cleaned) <= 15

def is_safe_string(text, max_length=100):
	"""Check if string is safe (no SQL injection attempts)"""
	if not text or len(text) > max_length:
		return False
	dangerous_patterns = ['--', ';', '/*', '*/', 'xp_', 'sp_', 'DROP', 'DELETE', 'INSERT', 'UPDATE', 'EXEC']
	return not any(pattern.lower() in text.lower() for pattern in dangerous_patterns)

# =====================================================

@app.route('/', methods=['GET', 'POST'])
def landing():
	return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	global name
	if request.method == 'POST':
		email = request.form.get('email', '').strip()
		password = request.form.get('password', '').strip()
		
		# Validation: Check empty fields
		if not email or not password:
			error = "Email and password are required!"
			return render_template('login.html',error=error)
		
		# Validation: Email format using helper
		if not validate_email(email):
			error = "Please enter a valid email address!"
			return render_template('login.html',error=error)
		
		con = sqlite3.connect('mydatabase.db')
		cursorObj = con.cursor()
		cursorObj.execute("SELECT Name from Users WHERE Email=? AND password=?", (email, password))
		try:
			name = cursorObj.fetchone()[0]
			session['username'] = name
			return redirect(url_for('home'))
		except:
			error = "Invalid Credentials Please try again..!!!"
			return render_template('login.html',error=error)
		finally:
			con.close()
	return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
	error = None
	if request.method == 'POST':
		if request.form['sub']=='Submit':
			name = request.form.get('name', '').strip()
			email = request.form.get('email', '').strip()
			password = request.form.get('password', '').strip()
			rpassword = request.form.get('rpassword', '').strip()
			pet = request.form.get('pet', '').strip()
			
			# Validation: Check empty fields
			if not name or not email or not password or not rpassword or not pet:
				error='All fields are required!'
				return render_template('register.html',error=error)
			
			# Validation: Email format using helper
			if not validate_email(email):
				error='Please enter a valid email address!'
				return render_template('register.html',error=error)
			
			# Validation: Name safety check
			if not is_safe_string(name, 50):
				error='Invalid name format!'
				return render_template('register.html',error=error)
			
			# Validation: Password strength using helper
			if not validate_password(password):
				error='Password must be at least 6 characters long!'
				return render_template('register.html',error=error)
			
			if(password != rpassword):
				error='Password does not match..!!!'
				return render_template('register.html',error=error)
			try:
				con = sqlite3.connect('mydatabase.db')
				cursorObj = con.cursor()
				cursorObj.execute("SELECT Name from Users WHERE Email=? AND password=?", (email, password))
			
				if(cursorObj.fetchone()):
					error = "User already Registered...!!!"
					return render_template('register.html',error=error)
			except:
				pass
			now = datetime.now()
			dt_string = now.strftime("%d/%m/%Y %H:%M:%S")			
			con = sqlite3.connect('mydatabase.db')
			cursorObj = con.cursor()
			cursorObj.execute("CREATE TABLE IF NOT EXISTS Users (Date text,Name text,Email text,password text,pet text)")
			cursorObj.execute("INSERT INTO Users VALUES(?,?,?,?,?)",(dt_string,name,email,password,pet))
			con.commit()

			return redirect(url_for('login'))

	return render_template('register.html')

@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
	error = None
	global name
	if request.method == 'POST':
		email = request.form.get('email', '').strip()
		pet = request.form.get('pet', '').strip()
		
		# Validation: Check empty fields
		if not email or not pet:
			error = "Email and pet name are required!"
			return render_template('forgot-password.html',error=error)
		
		# Validation: Email format using helper
		if not validate_email(email):
			error = "Please enter a valid email address!"
			return render_template('forgot-password.html',error=error)
		
		con = sqlite3.connect('mydatabase.db')
		cursorObj = con.cursor()
		cursorObj.execute("SELECT password from Users WHERE Email=? AND pet=?", (email, pet))
		
		try:
			password = cursorObj.fetchone()
			#print(password)
			error = "Your password : "+password[0]
		except:
			error = "Invalid information Please try again..!!!"
		finally:
			con.close()
		return render_template('forgot-password.html',error=error)
	return render_template('forgot-password.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
	global name
	return render_template('home.html',name=name)

@app.route('/dashboard')
def dashboard():

    # Sensor-based model comparison results
    model_results = [
        ["Decision Tree", "100%", "100%", "100%", "100%"],
        ["SVM", "98.61%", "98.76%", "98.61%", "98.61%"],
        ["Random Forest", "100%", "100%", "100%", "100%"],
        ["ANN (MLP)", "93.05%", "93.08%", "93.05%", "93.00%"]
    ]

    return render_template(
        'dashboard.html',
        model_results=model_results
    )

@app.route('/validate', methods=['GET', 'POST'])
def validate_model():
	"""Model Validation Page - Compare predictions with actual dataset"""
	global name
	
	# Read the dataset
	dataset_path = "enhanced_plant_disease_forecast_dataset.csv"
	df = pd.read_csv(dataset_path)
	
	# Configuration for validation
	num_samples = len(df)  # Use all samples by default (360)
	
	if request.method == 'POST':
		# Get number of samples from form
		num_samples = int(request.form.get('num_samples', len(df)))
	
	# Take samples from dataset
	if num_samples >= len(df):
		sample_df = df.copy()  # Use all data
	else:
		sample_df = df.sample(n=num_samples, random_state=None)  # Use random samples each time
	
	print("\n" + "="*80)
	print("🔍 MODEL VALIDATION STARTED")
	print("="*80)
	print(f"Dataset: {dataset_path}")
	print(f"Total Records in Dataset: {len(df)}")
	print(f"Validating with {num_samples} samples...")
	print("-"*80)
	
	# Perform validation
	validation_results = []
	correct_predictions = 0
	total_predictions = 0
	
	print(f"\n{'#':<5} {'Temp':<8} {'Humidity':<10} {'Moisture':<10} {'Actual':<18} {'Predicted':<18} {'Status':<10}")
	print("-"*80)
	
	for idx, row in sample_df.iterrows():
		temp = row['Temperature']
		humidity = row['Humidity']
		moisture = row['Moisture']
		actual_disease = row['Disease']
		
		# Predict using model
		predicted_disease = predict_disease_with_dtc(float(temp), float(humidity), float(moisture))
		
		# Check if prediction matches actual
		is_correct = (predicted_disease == actual_disease)
		if is_correct:
			correct_predictions += 1
		total_predictions += 1
		
		# Console output for each prediction
		status_symbol = "✓" if is_correct else "✗"
		status_text = "CORRECT" if is_correct else "WRONG"
		print(f"{total_predictions:<5} {temp:<8.2f} {humidity:<10.2f} {moisture:<10.2f} {actual_disease:<18} {predicted_disease:<18} {status_symbol} {status_text}")
		
		# Store result
		validation_results.append({
			'temperature': round(temp, 2),
			'humidity': round(humidity, 2),
			'moisture': round(moisture, 2),
			'actual': actual_disease,
			'predicted': predicted_disease,
			'match': 'Yes' if is_correct else 'No',
			'status': 'Correct' if is_correct else 'Wrong'
		})
	
	# Calculate accuracy
	accuracy = (correct_predictions / total_predictions * 100) if total_predictions > 0 else 0
	
	print("-"*80)
	print(f"\n📊 VALIDATION RESULTS:")
	print(f"   Total Samples Tested: {total_predictions}")
	print(f"   Correct Predictions: {correct_predictions}")
	print(f"   Wrong Predictions: {total_predictions - correct_predictions}")
	print(f"   Accuracy Calculation: ({correct_predictions} / {total_predictions}) * 100 = {accuracy:.2f}%")
	print(f"   Accuracy: {accuracy:.2f}%")
	print("="*80)
	print(f"✅ Validation {'PASSED' if accuracy >= 90 else 'NEEDS IMPROVEMENT'}")
	print("="*80 + "\n")
	
	return render_template(
		'validate.html',
		name=name,
		validation_results=validation_results,
		accuracy=round(accuracy, 2),
		correct=correct_predictions,
		total=total_predictions,
		num_samples=num_samples,
		dataset_size=len(df)
	)

@app.route('/sensor', methods=['GET', 'POST'])
def sensor():
	try:
		# ============ MODEL VALIDATION OUTPUT IN TERMINAL ============
		print("\n" + "="*80)
		print("🔍 MODEL VALIDATION - Running on /sensor page visit")
		print("="*80)
		
		# Read dataset and run quick validation
		dataset_path = "enhanced_plant_disease_forecast_dataset.csv"
		df = pd.read_csv(dataset_path)
		num_samples = 10  # Quick validation with 10 samples
		sample_df = df.sample(n=num_samples, random_state=None)  # Random samples each time
		
		print(f"Dataset: {dataset_path}")
		print(f"Total Records: {len(df)} | Testing {num_samples} random samples")
		print("-"*80)
		print(f"{'#':<5} {'Temp':<8} {'Humid':<8} {'Moist':<8} {'Actual':<15} {'Predicted':<15} {'Status':<10}")
		print("-"*80)
		
		correct = 0
		for idx, (i, row) in enumerate(sample_df.iterrows(), 1):
			t = row['Temperature']
			h = row['Humidity']
			m = row['Moisture']
			actual = row['Disease']
			predicted = predict_disease_with_dtc(float(t), float(h), float(m))
			is_correct = (predicted == actual)
			if is_correct:
				correct += 1
			status = "✓" if is_correct else "✗"
			print(f"{idx:<5} {t:<8.1f} {h:<8.1f} {m:<8.1f} {actual:<15} {predicted:<15} {status}")
		
		accuracy = (correct / num_samples) * 100
		print("-"*80)
		print(f"📊 Quick Validation: {correct}/{num_samples} correct | Accuracy: {accuracy:.1f}%")
		print("="*80 + "\n")
		# ============================================================
		
		temp,humidity,moisture = readFirebase()
		
		# Validation: Check if values are valid
		if temp is None or humidity is None or moisture is None:
			return render_template('sensor1.html',name=name,temp='N/A',humidity='N/A',moisture='N/A',disease='Sensor data unavailable')
		
		# Validation: Convert to float safely
		try:
			temp_float = float(temp)
			humidity_float = float(humidity)
			moisture_float = float(moisture)
		except (ValueError, TypeError):
			return render_template('sensor1.html',name=name,temp=temp,humidity=humidity,moisture=moisture,disease='Invalid sensor data')
		
		# Validation: Check reasonable ranges
		if not (-50 <= temp_float <= 100):
			return render_template('sensor1.html',name=name,temp=temp,humidity=humidity,moisture=moisture,disease='Temperature out of range')
		if not (0 <= humidity_float <= 100):
			return render_template('sensor1.html',name=name,temp=temp,humidity=humidity,moisture=moisture,disease='Humidity out of range')
		if not (0 <= moisture_float <= 100):
			return render_template('sensor1.html',name=name,temp=temp,humidity=humidity,moisture=moisture,disease='Moisture out of range')
		
		predicted_disease = predict_disease_with_dtc(temp_float, humidity_float, moisture_float)
		
		# Print current sensor prediction
		print(f"🌡️  CURRENT SENSOR READING:")
		print(f"   Temperature: {temp_float}°C | Humidity: {humidity_float}% | Moisture: {moisture_float}%")
		print(f"   ➜ Predicted Disease: {predicted_disease}\n")
		
		return render_template('sensor1.html',name=name,temp=temp,humidity=humidity,moisture=moisture,disease=predicted_disease)
	except Exception as e:
		print(f"❌ Error in sensor route: {e}\n")
		return render_template('sensor1.html',name=name,temp='Error',humidity='Error',moisture='Error',disease='System error')

# @app.route('/apidata', methods=['GET', 'POST'])
# def apidata():
#     temp, humidity, moisture = readWeatherAPI()

#     predicted_disease = predict_disease_with_dtc(
#         float(temp),
#         float(humidity),
#         float(moisture)
#     )

#     return render_template(
#         'sensor.html',
#         name=name,
#         temp=temp,
#         humidity=humidity,
#         moisture=moisture,
#         disease=predicted_disease
#     )
@app.route('/video', methods=['GET', 'POST'])
def video():
	global name
	global cap
	if request.method == 'POST':
		ret,img = cap.read()
		cv2.imwrite('static/img/test.jpg',img)
		return redirect(url_for('image_test'))
	return render_template('video.html',name=name)

# Flask Routes
@app.route('/video_stream')
def video_stream():
	cam  = 'http://10.1.235.164:8080/stream'
	#cam = 0
	return Response(video_feed(cam),
					mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/image', methods=['GET', 'POST'])
def image():
	if request.method=='POST':
		# Validation: Check if file was uploaded
		if 'doc' not in request.files:
			return render_template('image.html',name=name,error='No file uploaded!')
		
		f = request.files['doc']
		
		# Validation: Check if file is selected
		if f.filename == '':
			return render_template('image.html',name=name,error='No file selected!')
		
		# Validation: Check file extension
		allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
		file_ext = f.filename.rsplit('.', 1)[1].lower() if '.' in f.filename else ''
		if file_ext not in allowed_extensions:
			return render_template('image.html',name=name,error='Invalid file type! Only PNG, JPG, JPEG, GIF, BMP allowed.')
		
		# Validation: Check file size (max 10MB)
		f.seek(0, os.SEEK_END)
		file_size = f.tell()
		f.seek(0)
		if file_size > 10 * 1024 * 1024:
			return render_template('image.html',name=name,error='File too large! Maximum 10MB allowed.')
		
		savepath = r'static/img/'
		if not os.path.exists(savepath):
			os.makedirs(savepath)
		
		f.save(os.path.join(savepath,(secure_filename('test.jpg'))))
		return redirect(url_for('image_test'))
	return render_template('image.html',name=name)

@app.route('/image_test', methods=['GET', 'POST'])
def image_test():
	result,pesticide = predict()
	return render_template('image_test.html',name=name,result=result,suggestion=pesticide)

@app.route('/bot', methods=['GET', 'POST'])
def bot():
	state = 0
	global name
	global num
	
	if request.method == 'POST':
		if request.form['sub']=='Submit':
			state = 1
			name = request.form.get('name', '').strip()
			num = request.form.get('num', '').strip()
			
			# Validation: Check empty fields
			if not name or not num:
				return render_template('bot.html',state=json.dumps(0),error='Name and contact number are required!')
			
			# Validation: Check contact number format using helper
			if not validate_phone(num):
				return render_template('bot.html',state=json.dumps(0),error='Please enter a valid contact number!')
			
			# Validation: Name safety
			if not is_safe_string(name, 50):
				return render_template('bot.html',state=json.dumps(0),error='Invalid name format!')
			now = datetime.now()
			dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

			con = sqlite3.connect('mydatabase.db')
			cursorObj = con.cursor()
			cursorObj.execute("CREATE TABLE IF NOT EXISTS botUsers (Date text,Name text,Contact text)")
			cursorObj.execute("INSERT INTO botUsers VALUES(?,?,?)",(dt_string,name,num))
			con.commit()

		if request.form['sub']=='Rate':
			rating = request.form.get('rate', '').strip()
			suggestion = request.form.get('suggestions', '').strip()
			
			# Validation: Check rating is provided and valid
			if not rating:
				return render_template('bot.html',state=json.dumps(1),error='Please provide a rating!')
			
			# Validation: Rating should be a number between 1-5
			try:
				rating_int = int(rating)
				if not (1 <= rating_int <= 5):
					return render_template('bot.html',state=json.dumps(1),error='Rating must be between 1 and 5!')
			except ValueError:
				return render_template('bot.html',state=json.dumps(1),error='Invalid rating format!')
			
			# Validation: Check suggestion length
			if suggestion and len(suggestion) > 500:
				return render_template('bot.html',state=json.dumps(1),error='Feedback too long! Maximum 500 characters.')
			
			now = datetime.now()
			dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

			con = sqlite3.connect('mydatabase.db')
			cursorObj = con.cursor()
			cursorObj.execute("CREATE TABLE IF NOT EXISTS Feedback (Date text,Name text,Contact text,Ratings text,Feedback text)")
			cursorObj.execute("INSERT INTO Feedback VALUES(?,?,?,?,?)",(dt_string,name,num,rating,suggestion))
			con.commit()
			con.close()
			return redirect(url_for('home'))


	#print(state)
	return render_template('bot.html',state = json.dumps(state))


@app.route("/get")
def get_bot_response():
	user_response = spell(request.args.get('msg'))
	user_response=user_response.lower()
	botResponse = ''
	print(user_response)
	if('bye' not in user_response):
		if(('thank you' or 'thanks' or 'thanx' or 'ty') in user_response):
			flag=False
			#print("CollegeBot: You are welcome..")
			botResponse = "You are welcome.."
		else:
			if(greeting(user_response)!=None):
				#print("CollgeBot: "+greeting(user_response))
				botResponse = greeting(user_response)
			else:
				#print("CollgeBot: ",end="")
				#print(response(user_response))
				botResponse = response(user_response)
				sent_tokens.remove(user_response)
				
	else:
		flag=False
		#print("CollgeBot: Bye! take care..")
		botResponse = "Bye! take care.."

	#return str(english_bot.get_response(user_response))
	return botResponse



import requests

ESP32_IP = "http://10.1.230.211"   # change to your ESP32 IP

def readESP32(): 
    response = requests.get(f"{ESP32_IP}/data", timeout=2)
    data = response.json()

    temp = data["temperature"]
    humidity = data["humidity"]
    moisture = data["soil_moisture"]

    return temp, humidity, moisture

@app.route('/botdata')
def botdata():
    try:
        temp, humidity, moisture = readESP32()

        predicted_disease = predict_disease_with_dtc(
            float(temp), float(humidity), float(moisture)
        )

        return render_template(
            'sensor.html',
            temp=temp,
            humidity=humidity,
            moisture=moisture,
            disease=predicted_disease,
            name=name
        )
    except Exception as e:
        print(f"Error reading ESP32 data: {e}")
        return render_template(
            'sensor.html',
            temp="N/A",
            humidity="N/A",
            moisture="N/A",
            disease="Unable to connect to ESP32 device. Please check if the device is online.",
            name=name,
            error=str(e)
        )

@app.route('/api/sensor')
def api_sensor():
    try:
        temp, humidity, moisture = readESP32()

        predicted_disease = predict_disease_with_dtc(
            float(temp), float(humidity), float(moisture)
        )

        return {
            "temperature": temp,
            "humidity": humidity,
            "moisture": moisture,
            "disease": predicted_disease
        }
    except:
        return {
            "temperature": 0,
            "humidity": 0,
            "moisture": 0,
            "disease": "Error"
        }


@app.route('/move/<direction>', methods=['POST'])
def move_robot(direction):
    try:
        requests.get(
            f"{ESP32_IP}/move",
            params={"dir": direction},
            timeout=1
        )
        return {"status": "ok"}
    except:
        return {"status": "error"}, 500





# No caching at all for API endpoints.
@app.after_request
def add_header(response):
	# response.cache_control.no_store = True
	response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
	response.headers['Pragma'] = 'no-cache'
	response.headers['Expires'] = '-1'
	return response


if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=False, threaded=True)
