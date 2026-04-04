import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix

from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier

# ---------------- LOAD DATA ----------------
dataset_path = "enhanced_plant_disease_forecast_dataset.csv"
data = pd.read_csv(dataset_path)

# ---------------- PREPARE DATA ----------------
X = data[["Temperature", "Humidity", "Moisture"]]
y = data["Disease"]

label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# ---------------- SPLIT DATA ----------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42
)

# ================= MODELS =================

models = {
    "Decision Tree": DecisionTreeClassifier(random_state=42),
    "SVM": SVC(kernel='rbf', probability=True),
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
    "ANN (MLP)": MLPClassifier(hidden_layer_sizes=(32,16), max_iter=500, random_state=42)
}

results = []

print("\n================ MODEL PERFORMANCE =================\n")

for name, model in models.items():
    # Train
    model.fit(X_train, y_train)

    # Predict
    y_pred = model.predict(X_test)

    # Metrics
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    rec = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')

    results.append([name, acc, prec, rec, f1])

    print(f"\n{name} Results:")
    print("Accuracy:", acc)
    print("Precision:", prec)
    print("Recall:", rec)
    print("F1 Score:", f1)

    print("\nClassification Report:\n",
          classification_report(y_test, y_pred, target_names=label_encoder.classes_))

    print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))

# ---------------- COMPARISON TABLE ----------------
results_df = pd.DataFrame(results, columns=["Model", "Accuracy", "Precision", "Recall", "F1 Score"])

print("\n================ COMPARISON TABLE =================\n")
print(results_df)

# ---------------- BEST MODEL ----------------
best_model_name = results_df.sort_values(by="Accuracy", ascending=False).iloc[0]["Model"]
print(f"\nBest Model based on Accuracy: {best_model_name}")

# ---------------- USE DTC FOR PREDICTION ----------------
dtc = models["Decision Tree"]

# Generate label mapping dynamically from LabelEncoder
# This ensures correct mapping: LabelEncoder encodes alphabetically
label_mapping = {i: label for i, label in enumerate(label_encoder.classes_)}

print(f"\n✅ Correct Label Mapping: {label_mapping}\n")

def predict_disease_with_dtc(temperature, humidity, moisture):
    input_features = np.array([[temperature, humidity, moisture]])
    predicted_label = label_mapping[dtc.predict(input_features)[0]]
    return predicted_label