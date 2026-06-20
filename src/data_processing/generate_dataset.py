import pandas as pd
import numpy as np
import os

def generate_synthetic_data(num_samples=1000, output_dir="data/raw"):
    """
    Generates a synthetic dataset for Sugarcane Yield Prediction.
    The yield is calculated using a logical mathematical formula based on 
    the input features, allowing Machine Learning models to find actual patterns.
    """
    np.random.seed(42) # For reproducibility
    
    # 1. Define categorical options
    states = ['Maharashtra', 'Uttar Pradesh', 'Karnataka', 'Tamil Nadu', 'Bihar']
    soil_types = ['Alluvial', 'Black', 'Red', 'Laterite']
    irrigation_types = ['Drip', 'Flood', 'Sprinkler']
    
    # 2. Generate random feature values
    data = {
        'State': np.random.choice(states, num_samples),
        'Area_Acres': np.round(np.random.uniform(1.0, 50.0, num_samples), 2),
        'Rainfall_mm': np.round(np.random.uniform(800, 2500, num_samples), 1),
        'Temperature_C': np.round(np.random.uniform(20.0, 38.0, num_samples), 1),
        'Soil_Type': np.random.choice(soil_types, num_samples),
        'Irrigation_Type': np.random.choice(irrigation_types, num_samples),
        'Crop_Age_Months': np.random.randint(10, 19, num_samples),
    }
    
    df = pd.DataFrame(data)
    
    # 3. Calculate fertilizer used (kg) per acre
    # Let's say farmers use between 100kg to 300kg per acre
    df['Fertilizer_Used_kg'] = np.round(df['Area_Acres'] * np.random.uniform(100, 300, num_samples), 2)
    
    # 4. Generate the Target Variable: Yield (tons per acre)
    # We create a base yield and modify it based on the features so the ML model can learn it.
    base_yield = 30.0
    
    # Feature effects on yield
    rainfall_effect = (df['Rainfall_mm'] - 800) / 100 * 0.6  # More rain, more yield
    temp_effect = -np.abs(df['Temperature_C'] - 28) * 0.8    # Ideal temp is 28C
    fertilizer_effect = ((df['Fertilizer_Used_kg'] / df['Area_Acres']) - 100) / 50 * 1.5 
    
    # Categorical effects
    irrigation_effect = df['Irrigation_Type'].map({'Drip': 5.0, 'Sprinkler': 2.0, 'Flood': 0.0})
    soil_effect = df['Soil_Type'].map({'Black': 4.0, 'Alluvial': 3.0, 'Red': 0.0, 'Laterite': -2.0})
    
    # Calculate final yield with some random noise
    noise = np.random.normal(0, 3, num_samples)
    
    df['Yield_tons_per_acre'] = (base_yield + rainfall_effect + temp_effect + 
                                 fertilizer_effect + irrigation_effect + soil_effect + noise)
    
    # Ensure no unrealistic negative yields
    df['Yield_tons_per_acre'] = np.clip(df['Yield_tons_per_acre'], 10.0, 80.0)
    df['Yield_tons_per_acre'] = np.round(df['Yield_tons_per_acre'], 2)
    
    # 5. Save the dataset
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, 'sugarcane_yield.csv')
    df.to_csv(file_path, index=False)
    
    print(f"Successfully generated {num_samples} records and saved to {file_path}")
    return df

if __name__ == "__main__":
    generate_synthetic_data()
