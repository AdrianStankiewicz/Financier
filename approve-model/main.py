import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import pickle

# Load the dataset
data = pd.read_csv("model-data.csv")

# Data preprocessing
# Drop rows with missing values in the target variable (Loan_Status)
data = data.dropna(subset=["Loan_Status"])

# Data preprocessing
# Handle missing values in other columns
data["Dependents"].fillna("0", inplace=True)  # Fill missing values with "0"
data["Dependents"] = data["Dependents"].str.replace("3+", "4", regex=True)  # Replace '3+' with '4'
data["Dependents"] = data["Dependents"].str.extract('(\d+)').astype(int)  # Extract numeric part and convert to int
data["LoanAmount"].fillna(data["LoanAmount"].mean(), inplace=True)
data["Loan_Amount_Term"].fillna(data["Loan_Amount_Term"].mode()[0], inplace=True)
data["Credit_History"].fillna(1, inplace=True)
data["Self_Employed"].fillna("No", inplace=True)

# Encode categorical features
label_encoder = LabelEncoder()
categorical_cols = ["Gender", "Married", "Education", "Self_Employed", "Property_Area"]
for col in categorical_cols:
    data[col] = label_encoder.fit_transform(data[col])

# Define the feature columns and target variable
X = data[["Gender", "Married", "Dependents", "Education", "Self_Employed", "ApplicantIncome", "CoapplicantIncome", "LoanAmount", "Loan_Amount_Term", "Credit_History", "Property_Area"]]
y = data["Loan_Status"]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Build and train the logistic regression model
model = LogisticRegression()
model.fit(X_train, y_train)

# Save the trained model using Pickle
with open('/model/package/Financier-approver.pkl', 'wb') as model_file:
    pickle.dump(model, model_file)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

print("Accuracy:", accuracy)
print("Classification Report:\n", report)
