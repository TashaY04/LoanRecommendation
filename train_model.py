import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, classification_report
import xgboost as xgb
import joblib
import json
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

print("="*80)
print("LOAN ELIGIBILITY PREDICTION MODEL TRAINING")
print("="*80)

# ============================================================================
# STEP 1: GENERATE HIGH-QUALITY SYNTHETIC DATASET
# ============================================================================
print("\n[STEP 1] Generating synthetic dataset...")

np.random.seed(42)
n_samples = 8000

# Generate base features with realistic distributions
data = {
    'Age': np.random.randint(21, 65, n_samples),
    'Annual_Income': np.random.choice(
        np.concatenate([
            np.random.normal(300000, 100000, int(n_samples * 0.3)),  # Lower income
            np.random.normal(600000, 150000, int(n_samples * 0.4)),  # Middle income
            np.random.normal(1200000, 300000, int(n_samples * 0.3))  # Higher income
        ])
    ).astype(int),
    'CIBIL_Score': np.random.choice(
        np.concatenate([
            np.random.randint(300, 600, int(n_samples * 0.2)),   # Poor credit
            np.random.randint(600, 750, int(n_samples * 0.5)),   # Fair credit
            np.random.randint(750, 900, int(n_samples * 0.3))    # Good credit
        ])
    ),
    'Employment_Type': np.random.choice(['Salaried', 'Self-Employed', 'Business'], n_samples, p=[0.6, 0.25, 0.15]),
    'Work_Experience_Years': np.random.randint(0, 40, n_samples),
    'Loan_Amount_Requested': np.random.choice(
        np.concatenate([
            np.random.randint(100000, 500000, int(n_samples * 0.4)),
            np.random.randint(500000, 2000000, int(n_samples * 0.4)),
            np.random.randint(2000000, 5000000, int(n_samples * 0.2))
        ])
    ),
    'Loan_Purpose': np.random.choice(['Home', 'Personal', 'Education', 'Business', 'Vehicle'], n_samples, p=[0.35, 0.25, 0.15, 0.15, 0.1]),
    'Existing_Loans': np.random.choice([0, 1, 2, 3], n_samples, p=[0.4, 0.35, 0.2, 0.05]),
    'Credit_History_Years': np.random.randint(0, 25, n_samples),
    'Monthly_Debt': np.random.randint(0, 100000, n_samples),
    'Dependents': np.random.choice([0, 1, 2, 3, 4], n_samples, p=[0.25, 0.3, 0.25, 0.15, 0.05]),
    'Education_Level': np.random.choice(['High School', 'Bachelor', 'Master', 'PhD'], n_samples, p=[0.2, 0.5, 0.25, 0.05]),
    'Property_Ownership': np.random.choice(['Owned', 'Rented', 'Mortgaged'], n_samples, p=[0.35, 0.45, 0.2]),
    'City_Tier': np.random.choice([1, 2, 3], n_samples, p=[0.3, 0.4, 0.3])
}

df = pd.DataFrame(data)

# Ensure Annual_Income is positive
df['Annual_Income'] = df['Annual_Income'].clip(lower=100000)

# Create derived features
df['Monthly_Income'] = df['Annual_Income'] / 12
df['Debt_to_Income_Ratio'] = (df['Monthly_Debt'] / df['Monthly_Income']).clip(upper=1.0)
df['Loan_to_Income_Ratio'] = df['Loan_Amount_Requested'] / df['Annual_Income']
df['Age_Income_Product'] = df['Age'] * df['Annual_Income'] / 1000000
df['Experience_to_Age_Ratio'] = df['Work_Experience_Years'] / df['Age']

# ============================================================================
# STEP 2: CREATE TARGET VARIABLE WITH REALISTIC BUSINESS LOGIC
# ============================================================================
print("[STEP 2] Creating target variable with business rules...")

def determine_loan_eligibility(row):
    """
    Comprehensive loan eligibility determination based on multiple factors
    """
    score = 0
    
    # CIBIL Score (Most Important - 40 points)
    if row['CIBIL_Score'] >= 750:
        score += 40
    elif row['CIBIL_Score'] >= 700:
        score += 30
    elif row['CIBIL_Score'] >= 650:
        score += 20
    elif row['CIBIL_Score'] >= 600:
        score += 10
    else:
        score += 0
    
    # Income Assessment (25 points)
    if row['Annual_Income'] >= 1000000:
        score += 25
    elif row['Annual_Income'] >= 600000:
        score += 18
    elif row['Annual_Income'] >= 400000:
        score += 12
    else:
        score += 5
    
    # Debt-to-Income Ratio (20 points)
    if row['Debt_to_Income_Ratio'] <= 0.3:
        score += 20
    elif row['Debt_to_Income_Ratio'] <= 0.4:
        score += 15
    elif row['Debt_to_Income_Ratio'] <= 0.5:
        score += 10
    elif row['Debt_to_Income_Ratio'] <= 0.6:
        score += 5
    else:
        score += 0
    
    # Work Experience (8 points)
    if row['Work_Experience_Years'] >= 5:
        score += 8
    elif row['Work_Experience_Years'] >= 3:
        score += 5
    elif row['Work_Experience_Years'] >= 1:
        score += 2
    
    # Credit History (7 points)
    if row['Credit_History_Years'] >= 5:
        score += 7
    elif row['Credit_History_Years'] >= 3:
        score += 4
    elif row['Credit_History_Years'] >= 1:
        score += 2
    
    # Existing Loans penalty
    if row['Existing_Loans'] == 0:
        score += 5
    elif row['Existing_Loans'] == 1:
        score += 2
    elif row['Existing_Loans'] >= 2:
        score -= 8
    
    # Loan Amount vs Income (critical)
    if row['Loan_to_Income_Ratio'] > 6:
        score -= 20
    elif row['Loan_to_Income_Ratio'] > 4:
        score -= 12
    elif row['Loan_to_Income_Ratio'] > 3:
        score -= 5
    
    # Property Ownership bonus
    if row['Property_Ownership'] == 'Owned':
        score += 5
    elif row['Property_Ownership'] == 'Mortgaged':
        score += 2
    
    # Education Level bonus
    if row['Education_Level'] in ['Master', 'PhD']:
        score += 3
    elif row['Education_Level'] == 'Bachelor':
        score += 1
    
    # Age factor
    if 25 <= row['Age'] <= 45:
        score += 3  # Prime working age
    elif row['Age'] > 55:
        score -= 5  # Closer to retirement
    
    # Add some randomness for realistic variation (±10 points)
    score += np.random.randint(-10, 11)
    
    # Decision threshold: 75+ points = Approved (more stringent)
    return 1 if score >= 75 else 0

df['Loan_Approved'] = df.apply(determine_loan_eligibility, axis=1)

print(f"Dataset created with {len(df)} samples")
print(f"Loan Approval Rate: {df['Loan_Approved'].mean()*100:.2f}%")
print(f"Features: {len(df.columns)-1}")

# Save dataset
df.to_csv('loan_dataset.csv', index=False)
print("✓ Dataset saved as 'loan_dataset.csv'")

# ============================================================================
# STEP 3: FEATURE ENGINEERING AND PREPROCESSING
# ============================================================================
print("\n[STEP 3] Feature engineering and preprocessing...")

# Separate features and target
X = df.drop('Loan_Approved', axis=1)
y = df['Loan_Approved']

# Encode categorical variables
label_encoders = {}
categorical_cols = ['Employment_Type', 'Loan_Purpose', 'Education_Level', 'Property_Ownership']

for col in categorical_cols:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col])
    label_encoders[col] = le

# Save label encoders
joblib.dump(label_encoders, 'label_encoders.pkl')
print("✓ Label encoders saved")

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
print(f"✓ Train set: {len(X_train)} samples")
print(f"✓ Test set: {len(X_test)} samples")

# Feature scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Save scaler
joblib.dump(scaler, 'scaler.pkl')
print("✓ Scaler saved")

# ============================================================================
# STEP 4: MODEL TRAINING WITH HYPERPARAMETER TUNING
# ============================================================================
print("\n[STEP 4] Training XGBoost model with hyperparameter tuning...")

# Define parameter grid for tuning (simplified for faster training)
param_grid = {
    'n_estimators': [200],
    'max_depth': [6, 8],
    'learning_rate': [0.1],
    'subsample': [0.9],
    'colsample_bytree': [0.9],
    'min_child_weight': [3]
}

print("Performing Grid Search (this may take a few minutes)...")

# Base model
base_model = xgb.XGBClassifier(
    objective='binary:logistic',
    random_state=42,
    eval_metric='logloss',
    use_label_encoder=False
)

# Grid search with cross-validation
grid_search = GridSearchCV(
    estimator=base_model,
    param_grid=param_grid,
    cv=5,
    scoring='roc_auc',
    n_jobs=-1,
    verbose=1
)

grid_search.fit(X_train_scaled, y_train)

print(f"\n✓ Best parameters found: {grid_search.best_params_}")
print(f"✓ Best CV ROC-AUC score: {grid_search.best_score_:.4f}")

# Best model
best_model = grid_search.best_estimator_

# ============================================================================
# STEP 5: MODEL EVALUATION
# ============================================================================
print("\n[STEP 5] Evaluating model performance...")

# Predictions
y_train_pred = best_model.predict(X_train_scaled)
y_test_pred = best_model.predict(X_test_scaled)
y_test_proba = best_model.predict_proba(X_test_scaled)[:, 1]

# Calculate metrics
train_accuracy = accuracy_score(y_train, y_train_pred)
test_accuracy = accuracy_score(y_test, y_test_pred)
test_precision = precision_score(y_test, y_test_pred)
test_recall = recall_score(y_test, y_test_pred)
test_f1 = f1_score(y_test, y_test_pred)
test_roc_auc = roc_auc_score(y_test, y_test_proba)

print("\n" + "="*60)
print("MODEL PERFORMANCE METRICS")
print("="*60)
print(f"Train Accuracy:     {train_accuracy:.4f} ({train_accuracy*100:.2f}%)")
print(f"Test Accuracy:      {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")
print(f"Test Precision:     {test_precision:.4f}")
print(f"Test Recall:        {test_recall:.4f}")
print(f"Test F1-Score:      {test_f1:.4f}")
print(f"Test ROC-AUC:       {test_roc_auc:.4f}")
print("="*60)

print("\nConfusion Matrix:")
cm = confusion_matrix(y_test, y_test_pred)
print(cm)

print("\nClassification Report:")
try:
    print(classification_report(y_test, y_test_pred, target_names=['Rejected', 'Approved']))
except ValueError:
    # Handle case where only one class is present in predictions
    print("Note: Classification report requires both classes in test set")
    unique_classes = np.unique(y_test_pred)
    print(f"Classes present in predictions: {unique_classes}")

# Cross-validation scores
print("\n5-Fold Cross-Validation Scores:")
cv_scores = cross_val_score(best_model, X_train_scaled, y_train, cv=5, scoring='accuracy')
print(f"CV Accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")

# Feature importance
feature_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': best_model.feature_importances_
}).sort_values('importance', ascending=False)

print("\nTop 10 Most Important Features:")
for idx, row in feature_importance.head(10).iterrows():
    print(f"  {row['feature']:.<35} {row['importance']:.4f}")

# Save feature importance
feature_importance.to_csv('feature_importance.csv', index=False)

# ============================================================================
# STEP 6: SAVE MODEL AND METADATA
# ============================================================================
print("\n[STEP 6] Saving model and metadata...")

# Save the trained model
joblib.dump(best_model, 'loan_eligibility_model.pkl')
print("✓ Model saved as 'loan_eligibility_model.pkl'")

# Save model metadata
metadata = {
    'model_type': 'XGBoost Classifier',
    'training_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'n_samples': len(df),
    'n_features': len(X.columns),
    'test_accuracy': float(test_accuracy),
    'test_precision': float(test_precision),
    'test_recall': float(test_recall),
    'test_f1': float(test_f1),
    'test_roc_auc': float(test_roc_auc),
    'best_params': grid_search.best_params_,
    'feature_names': list(X.columns),
    'categorical_features': categorical_cols
}

with open('model_metadata.json', 'w') as f:
    json.dump(metadata, f, indent=4)
print("✓ Metadata saved as 'model_metadata.json'")

print("\n" + "="*80)
print("MODEL TRAINING COMPLETED SUCCESSFULLY!")
print("="*80)
print("\nGenerated Files:")
print("  • loan_dataset.csv - Training dataset")
print("  • loan_eligibility_model.pkl - Trained model")
print("  • scaler.pkl - Feature scaler")
print("  • label_encoders.pkl - Categorical encoders")
print("  • feature_importance.csv - Feature importance scores")
print("  • model_metadata.json - Model information")
print("\nYou can now run the Streamlit app: streamlit run app.py")
print("="*80)
