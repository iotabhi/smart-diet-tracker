import pandas as pd
import os

# --- SENIOR DEV SAFE PATHS ---
# Get the folder where this script is running
base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, 'data')

# Create 'data' folder if it doesn't exist
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Define the Data
data = {
    'Food_Item': ['Roti', 'Plain Rice', 'Dal Fry', 'Paneer Butter Masala', 'Chole', 'Aloo Paratha', 'Dosa', 'Idli', 'Samosa', 'Tea (Chai)', 'Curd (Dahi)', 'Chicken Curry', 'Egg Bhurji', 'Poha', 'Upma', 'Gulab Jamun', 'Biscuits', 'Apple', 'Banana', 'Mixed Sabzi'],
    'Calories': [100, 130, 150, 350, 250, 280, 160, 60, 260, 80, 100, 300, 150, 180, 200, 150, 40, 52, 89, 120],
    'Protein_g': [3, 2.7, 8, 12, 10, 6, 4, 2, 4, 1, 4, 25, 12, 4, 5, 2, 0.5, 0.3, 1.1, 3],
    'Fat_g': [0.5, 0.3, 5, 25, 12, 12, 6, 0.2, 18, 2, 4, 18, 10, 5, 6, 8, 2, 0.2, 0.3, 8],
    'Carbs_g': [20, 28, 18, 15, 30, 35, 25, 12, 28, 12, 6, 5, 1, 30, 30, 20, 6, 14, 23, 12],
    'Serving_Unit': ['1 piece', '1 katori', '1 katori', '1 plate', '1 plate', '1 piece', '1 piece', '1 piece', '1 piece', '1 cup', '1 katori', '1 plate', '2 eggs', '1 plate', '1 plate', '1 piece', '1 piece', '1 medium', '1 medium', '1 katori']
}

df = pd.DataFrame(data)
df.index = range(1, len(df) + 1)

# Save safely
save_path = os.path.join(data_dir, 'indian_food_dataset.csv')
df.to_csv(save_path, index_label='ID')

print(f"✅ Step 1 Complete: Data saved at: {save_path}")