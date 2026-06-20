import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def perform_eda(df, output_dir="eda_reports"):
    """Generates and saves basic EDA plots."""
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Yield Distribution
    plt.figure(figsize=(8, 5))
    sns.histplot(df['Yield_tons_per_acre'], kde=True, color='green')
    plt.title('Distribution of Sugarcane Yield')
    plt.xlabel('Yield (tons/acre)')
    plt.savefig(os.path.join(output_dir, 'yield_distribution.png'))
    plt.close()
    
    # 2. Correlation Heatmap (Numerical features only)
    plt.figure(figsize=(10, 8))
    numeric_df = df.select_dtypes(include=[np.number])
    sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Feature Correlation Heatmap')
    plt.savefig(os.path.join(output_dir, 'correlation_heatmap.png'))
    plt.close()
    
    print(f"EDA plots saved to {output_dir}/")

def build_model_pipeline(model):
    """Creates a Scikit-Learn pipeline with preprocessing and the given model."""
    # Define categorical and numerical columns
    categorical_cols = ['State', 'Soil_Type', 'Irrigation_Type']
    numerical_cols = ['Area_Acres', 'Rainfall_mm', 'Temperature_C', 'Crop_Age_Months', 'Fertilizer_Used_kg']
    
    # Create transformers
    categorical_transformer = OneHotEncoder(handle_unknown='ignore')
    numerical_transformer = StandardScaler()
    
    # Bundle transformers into a preprocessor
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numerical_transformer, numerical_cols),
            ('cat', categorical_transformer, categorical_cols)
        ]
    )
    
    # Create and return the full pipeline
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('model', model)
    ])
    
    return pipeline

def train_and_evaluate():
    # 1. Load Data
    data_path = 'data/raw/sugarcane_yield.csv'
    if not os.path.exists(data_path):
        print(f"Error: Dataset not found at {data_path}. Run generate_dataset.py first.")
        return
        
    df = pd.read_csv(data_path)
    
    # 2. Perform EDA
    perform_eda(df)
    
    # 3. Data Preprocessing Setup
    X = df.drop(columns=['Yield_tons_per_acre'])
    y = df['Yield_tons_per_acre']
    
    # Split data into training and testing sets (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 4. Define Models to test
    models = {
        "Linear Regression": LinearRegression(),
        "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42),
        "XGBoost": XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
    }
    
    # 5. Train and Evaluate
    results = {}
    best_model = None
    best_r2 = -float('inf')
    best_model_name = ""
    
    print("\n--- Model Training & Evaluation ---")
    for name, model in models.items():
        # Build pipeline
        pipeline = build_model_pipeline(model)
        
        # Train
        pipeline.fit(X_train, y_train)
        
        # Predict
        y_pred = pipeline.predict(X_test)
        
        # Evaluate metrics
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)
        
        results[name] = {'MAE': mae, 'RMSE': rmse, 'R2': r2}
        print(f"{name}:\n  MAE: {mae:.2f} | RMSE: {rmse:.2f} | R²: {r2:.4f}")
        
        # Keep track of the best model based on R2 Score
        if r2 > best_r2:
            best_r2 = r2
            best_model = pipeline
            best_model_name = name

    print(f"\nBest Model: {best_model_name} with R2: {best_r2:.4f}")
    
    # 6. Save the best model
    os.makedirs('models', exist_ok=True)
    model_path = 'models/yield_model.pkl'
    joblib.dump(best_model, model_path)
    print(f"Best model saved successfully to {model_path}")

if __name__ == "__main__":
    train_and_evaluate()
