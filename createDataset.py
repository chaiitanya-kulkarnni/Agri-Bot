import pandas as pd
import random

import random
import pandas as pd

# Define ranges for dataset generation
def determine_disease(temp, humidity, moisture):
    if temp > 35 and humidity < 40 and moisture < 20:
        return "Blight"
    elif 25 <= temp <= 35 and 60 <= humidity <= 80 and moisture > 40:
        return "Powdery Mildew"
    elif 20 <= temp < 30 and 40 <= humidity < 60 and 20 <= moisture <= 40:
        return "Rust"
    elif temp < 20 and humidity > 70 and 30 < moisture <= 50:
        return "Wilt"
    elif 30 <= temp <= 35 and 50 <= humidity < 70 and 20 <= moisture <= 30:
        return "Leaf Spot"
    else:
        return "No Disease"

# Predefined ranges for each disease
ranges = {
    "Blight": {"temp": (36, 40), "humidity": (20, 39), "moisture": (10, 19)},
    "Powdery Mildew": {"temp": (25, 35), "humidity": (60, 80), "moisture": (41, 60)},
    "Rust": {"temp": (20, 29), "humidity": (40, 59), "moisture": (20, 40)},
    "Wilt": {"temp": (15, 19), "humidity": (71, 90), "moisture": (31, 50)},
    "Leaf Spot": {"temp": (30, 35), "humidity": (50, 69), "moisture": (20, 30)},
    "No Disease": {"temp": (20, 25), "humidity": (40, 50), "moisture": (10, 20)},
}

# Generate dataset with 60 samples per class
data = []
for disease, conditions in ranges.items():
    for _ in range(60):
        temperature = round(random.uniform(*conditions["temp"]), 1)
        humidity = round(random.uniform(*conditions["humidity"]), 1)
        moisture = round(random.uniform(*conditions["moisture"]), 1)
        data.append([temperature, humidity, moisture, disease])

# Shuffle the dataset to mix samples
random.shuffle(data)

# Convert to DataFrame and save as CSV
df = pd.DataFrame(data, columns=["Temperature", "Humidity", "Moisture", "Disease"])
#df.to_csv("plant_disease_dataset.csv", index=False)

#print("Dataset generated and saved as 'plant_disease_dataset.csv'")


# Save to CSV
file_path = "enhanced_plant_disease_forecast_dataset.csv"
df.to_csv(file_path, index=False)
print(f"Enhanced dataset saved to {file_path}")
