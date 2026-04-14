import os
import warnings
warnings.filterwarnings("ignore")   # suppress warnings

from joblib import dump
from utils.preprocessing import load_data
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier
from sklearn.svm import SVC
from lightgbm import LGBMClassifier
import matplotlib.pyplot as plt


# Load Data
X_train, X_test, y_train, y_test, encoder = load_data(
    "dataset/training_data.csv",
    "dataset/test_data.csv"
)

# Split data
X_train_split, X_val, y_train_split, y_val = train_test_split(
    X_train, y_train, test_size=0.33, random_state=101
)

# Models (fixed)
models = {
    "XGBoost": XGBClassifier(use_label_encoder=False, eval_metric='mlogloss'),
    "SVM": SVC(probability=True),
    "LightGBM": LGBMClassifier(verbose=-1)   # no warnings
}

results = {}
trained_models = {}

print("\n🔍 Training & Comparing Models...\n")

# Train models
for name, model in models.items():
    model.fit(X_train_split, y_train_split)
    preds = model.predict(X_val)
    acc = accuracy_score(y_val, preds)

    results[name] = acc
    trained_models[name] = model

    print(f"{name} Accuracy: {acc:.4f}")

# Select best model
best_model_name = max(results, key=results.get)
best_model = trained_models[best_model_name]

print(f"\n🏆 Best Model: {best_model_name} ({results[best_model_name]:.4f})")

# Save model to ML_models
os.makedirs("ML_models", exist_ok=True)
dump((best_model, encoder), "ML_models/best_model.joblib")

print("\n Model saved in ML_models/best_model.joblib")

# Plot model comparison
plt.figure(figsize=(8, 5))
plt.bar(results.keys(), results.values())
plt.title("Model Comparison")
plt.ylabel("Accuracy")
plt.tight_layout()

os.makedirs("assets", exist_ok=True)
plt.savefig("assets/model_comparison.png")
plt.close()

print(" Model comparison graph saved in assets/")