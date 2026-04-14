# SymptoSphere 
Intelligent Disease Prediction System using Machine Learning

Go to [https://streamlit.io/cloud ](https://symptosphere-404avinotfound.streamlit.app/)
---

## Overview

SymptoSphere is a machine learning-based web application that predicts diseases based on user-selected symptoms. It uses multiple advanced models and automatically selects the best-performing model to provide accurate predictions.

The system returns the top three probable diseases along with confidence scores through an interactive user interface built with Streamlit.

---

## Features

- Symptom-based disease prediction  
- Multi-model system (XGBoost, SVM, LightGBM)  
- Automatic best model selection  
- Model comparison visualization  
- Data preprocessing and label encoding  
- Interactive Streamlit UI with checkbox input  
- Top-3 predictions with probability scores  
- Modular and scalable project structure  

---

## Project Structure
project/
│
# Streamlit UI
├── app.py 
# Model training and comparison
├── main.py 
# Saved model
├── ML_models/ 
│ └── best_model.joblib
# Training and test data
├── dataset/ 
├── utils/
  # Data cleaning and encoding
│ ├── preprocessing.py 
  # Prediction logic
│ └── prediction.py 
# Graphs and images
├── assets/ 
│ ├── feature_importance.png
│ └── model_comparison.png
# Dependencies
├── requirements.txt 
└── README.md

---

## Installation

### 1. Clone the repository
git clone https://github.com/404avinotfound/SymptoSphere.git

cd SymptoSphere
---

### 2. Install dependencies
pip install -r requirements.txt


---

## Train the Model

Run the following command:


python train.py


This will:
- Train multiple models  
- Select the best model  
- Save it in `ML_models/best_model.joblib`  
- Generate a model comparison graph  

---

## Run the Application


python -m streamlit run app.py

---

## How It Works

1. User selects symptoms through the interface  
2. Input is converted into a feature vector  
3. The trained model predicts probabilities  
4. Top three diseases are displayed with confidence scores  

---

## Models Used

- XGBoost  
- Support Vector Machine (SVM)  
- LightGBM  

The best model is selected automatically based on validation accuracy.

---

## Example Output


Top Predictions:
Dengue : 92.34%
Malaria : 85.12%
Typhoid : 78.45%


---

## Deployment

To deploy using Streamlit Cloud:

1. Push your code to GitHub  
2. Go to [https://streamlit.io/cloud ](https://symptosphere-404avinotfound.streamlit.app/) 
3. Select your repository  
4. Set the main file as:


app.py


---

## Technologies Used

- Python  
- Pandas  
- NumPy  
- Scikit-learn  
- XGBoost  
- LightGBM  
- Streamlit  
- Matplotlib  
- Joblib  

---

## Objective

To develop a practical machine learning application that demonstrates disease prediction using symptom data and provides an intuitive user interface for interaction.

---

## Disclaimer

This project is intended for educational purposes only and should not be used as a substitute for professional medical advice.

---

## Author

404avinotfound  
B.Tech CSE Student  

---

## Future Improvements

- Symptom severity input (scaled values)  
- Doctor recommendation system  
- Natural language symptom input  
- Improved UI design and responsiveness  

---

## License

This project is open-source and available for educational use.
