import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
import os

# --- SENIOR DEV SAFE PATHS ---
base_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_dir, 'data', 'indian_food_dataset.csv')
models_dir = os.path.join(base_dir, 'models')
model_save_path = os.path.join(models_dir, 'calorie_model.pkl')

# Check if data exists
if not os.path.exists(data_path):
    print(f"❌ Error: Data file not found at {data_path}")
    print("Please run create_data.py first.")
    exit()

# 1. Load Data
df = pd.read_csv(data_path)

# 2. Train Model
X = df[['Protein_g', 'Fat_g', 'Carbs_g']]
y = df['Calories']
model = LinearRegression()
model.fit(X, y)

# 3. Save Model
if not os.path.exists(models_dir):
    os.makedirs(models_dir)

joblib.dump(model, model_save_path)
print(f"✅ Step 2 Complete: Model saved at: {model_save_path}")