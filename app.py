import streamlit as st
import pandas as pd
import joblib
import os
from datetime import date
from sklearn.linear_model import LinearRegression
from urllib.parse import quote_plus
import pymongo
import certifi
# -------------------- ARCHITECTURE & PATHS --------------------
base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, 'models', 'calorie_model.pkl')
data_path = os.path.join(base_dir, 'data', 'indian_food_dataset.csv')

# -------------------- APP CONFIGURATION --------------------
st.set_page_config(
    page_title="Diet and Calorie Tracker",
    page_icon="🥗",
    layout="centered",
    initial_sidebar_state="expanded"
)

# -------------------- DATABASE CONNECTION --------------------
@st.cache_resource
# -------------------- DATABASE CONNECTION (UNIVERSAL) --------------------
@st.cache_resource
# -------------------- DATABASE CONNECTION (SSL FIX) --------------------
@st.cache_resource
# -------------------- DATABASE CONNECTION (CERTIFI FIX) --------------------
@st.cache_resource
def init_connection():
    try:
        # 1. DEFINE CREDENTIALS
        username = quote_plus("admin")
        password = quote_plus("Abhi@1994") 
        
        # 2. CREATE URI
        uri = f"mongodb+srv://{username}:{password}@cluster0.ojk15i9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        
        # 3. CONNECT (WITH CERTIFI)
        # This tells Python exactly where to find the secure certificates
        return pymongo.MongoClient(uri, tlsCAFile=certifi.where())
             
    except Exception as e:
        st.error(f"❌ Connection Error: {e}")
        return None
def save_to_mongo(data):
    """Saves a single daily log entry to MongoDB"""
    client = init_connection()
    if client:
        try:
            db = client.diet_tracker
            collection = db.daily_logs
            collection.insert_one(data)
            return True
        except Exception as e:
            st.error(f"❌ Save Failed: {e}")
            return False
    return False

def load_history_from_mongo():
    """Fetches all history from MongoDB for Page 3"""
    client = init_connection()
    if client:
        try:
            db = client.diet_tracker
            # Fetch all logs, exclude the system ID (_id)
            items = list(db.daily_logs.find({}, {"_id": 0}))
            return pd.DataFrame(items)
        except Exception as e:
            st.error(f"❌ Fetch Error: {e}")
            return pd.DataFrame()
    return pd.DataFrame()

# -------------------- LOAD INTELLIGENCE --------------------
@st.cache_resource
def load_resources():
    if not os.path.exists(data_path): return None, None
    df = pd.read_csv(data_path)
    if os.path.exists(model_path):
        model = joblib.load(model_path)
    else:
        model = LinearRegression()
    return model, df

model, food_df = load_resources()

if food_df is None:
    st.error("⚠️ System Error: Data files missing. Please initialize the project.")
    st.stop()

food_names = sorted(food_df['Food_Item'].unique())

# -------------------- SMART HEALTH LOGIC --------------------
def get_health_status(bmi):
    if bmi < 18.5: return "Focus on Nourishment", "Muscle Gain"
    elif 18.5 <= bmi < 24.9: return "Optimal Zone", "Maintenance"
    elif 25 <= bmi < 29.9: return "Finding Balance", "Weight Loss"
    else: return "Health Prioritization", "Weight Loss"

def get_bmi_feedback_text(bmi):
    if bmi < 18.5: return "You are slightly underweight. Focusing on nutrient-dense foods will help build strength."
    elif 18.5 <= bmi < 24.9: return "Great work! You are in a healthy weight range. Keep maintaining this balance."
    elif 25 <= bmi < 29.9: return "You are slightly above the ideal range. Small adjustments to your diet can help."
    else: return "Your health matters. A structured plan for weight management is recommended."

def generate_smart_feedback(calories, protein, carbs, remaining_daily_cals):
    tips = []
    if protein < 5: tips.append("🥩 **Protein Boost:** This meal is low in protein. Consider adding Dal, Paneer, or Curd.")
    elif protein > 25: tips.append("💪 **Muscle Fuel:** Excellent protein content for recovery and strength.")
    
    if calories > 800: tips.append("🍽️ **Hearty Meal:** This is a heavy meal. Keep your next meal light.")
    elif calories < 150: tips.append("🍏 **Light Snack:** Good energy boost without heaviness.")
        
    if remaining_daily_cals < 0: tips.append("📉 **Over Target:** You've exceeded your goal. Maybe take a short walk?")
    elif remaining_daily_cals < 200: tips.append("🎯 **On Target:** Very close to your goal. Great consistency!")
    else: tips.append("✅ **On Track:** You have room left in your budget.")
    return tips

# -------------------- CALCULATORS --------------------
def calculate_bmr(weight, height, age, gender):
    return (10 * weight + 6.25 * height - 5 * age + 5) if gender == "Male" else (10 * weight + 6.25 * height - 5 * age - 161)

def calculate_tdee(bmr, activity):
    return bmr * {"Sedentary": 1.2, "Light": 1.375, "Moderate": 1.55, "Active": 1.725}.get(activity, 1.2)

def calculate_bmi(weight, height):
    return weight / ((height/100) ** 2)

# -------------------- STATE MANAGEMENT --------------------
for key in ["page", "name", "age", "gender", "weight", "height", "activity", "goal", "bmr", "tdee", "bmi", "bmi_status", "final_calories", "daily_log", "temp_analysis"]:
    if key not in st.session_state:
        st.session_state[key] = 1 if key == "page" else ([] if key == "daily_log" else None)

# -------------------- SIDEBAR --------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2921/2921822.png", width=50)
    st.header("Diet and Calorie Tracker")
    st.write("Your personal AI-powered nutrition companion.")
    st.divider()
    st.caption("Developed by:")
    st.markdown("**Abhilasha**") 
    st.caption("B.Tech CSE")

# ======================================================
# PAGE 1 — PROFILE SETUP
# ======================================================
if st.session_state.page == 1:
    st.title("👋 Welcome to Diet and Calorie Tracker")
    st.write("Let's personalize your health journey.")
    
    st.session_state.name = st.text_input("First, what should we call you?", st.session_state.name or "")
    
    col1, col2 = st.columns(2)
    st.session_state.age = col1.number_input("Age (years)", 10, 100, st.session_state.age or 20)
    st.session_state.gender = col2.selectbox("Gender", ["Male", "Female"], index=0 if st.session_state.gender == "Male" else 1)
    
    col3, col4 = st.columns(2)
    st.session_state.weight = col3.number_input("Weight (kg)", 30.0, 200.0, st.session_state.weight or 60.0)
    st.session_state.height = col4.number_input("Height (cm)", 120.0, 250.0, st.session_state.height or 170.0)
    
    st.session_state.activity = st.selectbox("Activity Level", ["Sedentary", "Light", "Moderate", "Active"])
    st.session_state.goal = st.selectbox("Your Health Goal", ["Weight Loss", "Maintenance", "Muscle Gain"])
    
    st.divider()
    
    if st.button("Create My Plan ➡️", use_container_width=True):
        bmi = calculate_bmi(st.session_state.weight, st.session_state.height)
        status, suggestion = get_health_status(bmi)
        bmr = calculate_bmr(st.session_state.weight, st.session_state.height, st.session_state.age, st.session_state.gender)
        tdee = calculate_tdee(bmr, st.session_state.activity)
        target = tdee - 500 if st.session_state.goal == "Weight Loss" else (tdee + 300 if st.session_state.goal == "Muscle Gain" else tdee)
        
        st.session_state.bmi = bmi
        st.session_state.bmi_status = status
        st.session_state.bmr = bmr
        st.session_state.tdee = tdee
        st.session_state.final_calories = target
        st.session_state.page = 2
        st.rerun()

# ======================================================
# PAGE 2 — DASHBOARD & TRACKER
# ======================================================
elif st.session_state.page == 2:
    st.subheader(f"☀️ Good day, {st.session_state.name}")
    
    # --- TOP METRICS ---
    with st.container():
        # Green Target Box
        st.success(f"🎯 **Daily Target: {st.session_state.final_calories:.0f} kcal**")
        
        # 3-Column Metrics (BMI, BMR, TDEE)
        c1, c2, c3 = st.columns(3)
        c1.metric("BMI Score", f"{st.session_state.bmi:.1f}", st.session_state.bmi_status)
        c2.metric("BMR", f"{st.session_state.bmr:.0f} kcal")
        c3.metric("TDEE", f"{st.session_state.tdee:.0f} kcal")
        
        # BMI Feedback
        st.caption(f"💡 {get_bmi_feedback_text(st.session_state.bmi)}")
    
    st.divider()
    
    # --- TRACKING TABS ---
    tab1, tab2 = st.tabs(["📖 Standard Menu", "🧠 Smart Estimator (AI)"])
    
    with tab1:
        dish = st.selectbox("Choose a Meal", food_names)
        item = food_df[food_df['Food_Item'] == dish].iloc[0]
        unit = item['Serving_Unit']
        st.info(f"ℹ️ Serving: **{unit}** ≈ **{item['Calories']} kcal**")
        qty = st.number_input("Count", 0.5, 10.0, 1.0, 0.5)
        
        if st.button("🔍 Analyze"):
            total_cal = item['Calories'] * qty
            total_pro = item['Protein_g'] * qty
            total_carb = item['Carbs_g'] * qty
            remaining = st.session_state.final_calories - sum(d['Calories'] for d in st.session_state.daily_log) - total_cal
            
            st.session_state.temp_analysis = {
                "name": dish,
                "qty_display": f"{qty} {unit.replace('1 ', '')}",
                "cal": total_cal, "pro": total_pro, "carb": total_carb, "fat": item['Fat_g'] * qty,
                "feedback": generate_smart_feedback(total_cal, total_pro, total_carb, remaining)
            }
    
    with tab2:
        st.markdown("**Eating custom? Let AI guess.**")
        custom_name = st.text_input("Meal Name", placeholder="e.g. Mom's Curry")
        rc1, rc2, rc3 = st.columns(3)
        main_type = rc1.selectbox("Base", ["Rice/Grains", "Dal/Lentils", "Paneer", "Chicken/Meat", "Egg", "Vegetables", "Fast Food/Snack"])
        style = rc2.selectbox("Style", ["Boiled / Steamed", "Home-Cooked Curry", "Restaurant / Rich Gravy", "Deep Fried"])
        vol = rc3.selectbox("Size", ["Small Bowl / 1 pc", "Medium Bowl / 2 pcs", "Large Bowl / 3 pcs"])
        
        if st.button("✨ Predict"):
            if not custom_name: st.warning("Name your meal first.")
            else:
                base_values = {"Rice/Grains": [2,0.5,25], "Dal/Lentils": [6,2,15], "Paneer": [10,12,4], "Chicken/Meat": [20,5,0], "Egg": [6,5,0], "Vegetables": [2,0.2,8], "Fast Food/Snack": [4,10,30]}
                p, f, c = base_values[main_type]
                if style == "Home-Cooked Curry": f+=5; c+=5
                elif style == "Restaurant / Rich Gravy": f+=15; c+=10
                elif style == "Deep Fried": f+=20; c+=10
                mult = 0.75 if "Small" in vol else (1.5 if "Large" in vol else 1.0)
                est_p, est_f, est_c = p*mult, f*mult, c*mult
                pred_cal = model.predict([[est_p, est_f, est_c]])[0]
                remaining = st.session_state.final_calories - sum(d['Calories'] for d in st.session_state.daily_log) - pred_cal
                st.session_state.temp_analysis = {
                    "name": f"{custom_name} (AI)", "qty_display": vol,
                    "cal": pred_cal, "pro": est_p, "carb": est_c, "fat": est_f,
                    "feedback": generate_smart_feedback(pred_cal, est_p, est_c, remaining)
                }

    # --- FEEDBACK POPUP ---
    if st.session_state.temp_analysis:
        st.divider()
        st.subheader("🧐 Nutrition Check")
        data = st.session_state.temp_analysis
        k1, k2, k3 = st.columns(3)
        k1.metric("Calories", f"{data['cal']:.0f}")
        k2.metric("Protein", f"{data['pro']:.1f}g")
        k3.metric("Carbs", f"{data['carb']:.1f}g")
        for msg in data['feedback']: st.info(msg)
        
        col_ok, col_cancel = st.columns([1, 4])
        if col_ok.button("✅ Eat it!"):
            st.session_state.daily_log.append({"Dish Name": data['name'], "Quantity": data['qty_display'], "Calories": data['cal']})
            st.session_state.temp_analysis = None
            st.rerun()
        if col_cancel.button("❌ Cancel"):
            st.session_state.temp_analysis = None
            st.rerun()

    # --- SUMMARY & NAV ---
    if st.session_state.daily_log:
        st.divider()
        st.subheader("📋 Today's Intake")
        df = pd.DataFrame(st.session_state.daily_log)
        df.index = range(1, len(df)+1)
        st.dataframe(df, use_container_width=True)
        total = df['Calories'].sum()
        rem = st.session_state.final_calories - total
        st.progress(min(total / st.session_state.final_calories, 1.0))
        c1, c2 = st.columns(2)
        c1.metric("Consumed", f"{total:.0f} kcal")
        c2.metric("Remaining", f"{rem:.0f} kcal", delta_color="normal" if rem>0 else "inverse")
        
        # --- ACTIONS (UPDATED FOR MONGODB) ---
        st.write("")
        col1, col2 = st.columns(2)
        
        # >>> NEW MONGODB SAVE BUTTON <<<
        if col1.button("☁️ Save to Cloud", use_container_width=True):
            today_str = date.today().strftime("%Y-%m-%d")
            status = "On Track" if total <= st.session_state.final_calories else "Over Limit"
            
            # The Data Bundle to Save
            log_entry = {
                "User": st.session_state.name,
                "Date": today_str,
                "Total_Calories": total,
                "Goal_Status": status,
                "Meals": st.session_state.daily_log
            }
            
            if save_to_mongo(log_entry):
                st.balloons()
                st.toast("✅ Saved to MongoDB Atlas!", icon="☁️")
            else:
                st.toast("⚠️ Save Failed. Check Connection.", icon="❌")
        
        if col2.button("🗑️ Reset Log", use_container_width=True):
            st.session_state.daily_log = []
            st.rerun()

    # --- NAVIGATION FOOTER ---
    st.markdown("---")
    nav_left, nav_mid, nav_right = st.columns([1, 1, 1])
    with nav_left:
        if st.button("⬅️ Edit Profile"): st.session_state.page = 1; st.rerun()
    with nav_right:
        if st.button("View History ➡️"): st.session_state.page = 3; st.rerun()

# ======================================================
# PAGE 3 — HISTORY (CONNECTED TO MONGODB)
# ======================================================
elif st.session_state.page == 3:
    st.title("📅 Your Progress")
    st.caption(f"History for {st.session_state.name}")
    
    # Fetch Data from MongoDB
    with st.spinner("Fetching data from cloud..."):
        hist_df = load_history_from_mongo()
    
    if not hist_df.empty:
        # --- FIX: Clean up the 'Meals' column ---
        # This converts the complex list of objects into a simple string like "Roti, Dal"
        if "Meals" in hist_df.columns:
            hist_df["Meals"] = hist_df["Meals"].apply(
                lambda meals: ", ".join([m.get('Dish Name', m.get('Dish', 'Meal')) for m in meals]) 
                if isinstance(meals, list) else str(meals)
            )

        # Display the DataFrame
        st.subheader("Cloud Logs")
        st.dataframe(hist_df, use_container_width=True)
    else:
        st.info("No cloud history found. Try saving a day first!")
        
    st.divider()
    if st.button("⬅️ Back to Tracker"):
        st.session_state.page = 2
        st.rerun()