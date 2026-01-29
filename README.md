# 🥗 AI-Powered Smart Diet Tracker

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/iotabhi/smart-diet-tracker)
![Python](https://img.shields.io/badge/Python-3.9-blue)
![MongoDB](https://img.shields.io/badge/Database-MongoDB%20Atlas-green)
![Status](https://img.shields.io/badge/Status-Deployed-success)

A full-stack health and nutrition application tailored for **Indian Diets**, featuring AI-based calorie estimation and real-time cloud data synchronization.

🔗 **Live Demo:** [Click here to view App](https://share.streamlit.io/iotabhi/smart-diet-tracker)

## 🚀 Key Features

* **🧠 AI Calorie Estimator:** Uses a **Linear Regression** model (Scikit-Learn) to predict calories for custom home-cooked Indian meals based on approximate macro inputs.
* **☁️ Cloud Integration:** Fully integrated with **MongoDB Atlas** (NoSQL) to persist user logs, history, and health metrics securely across sessions.
* **📊 Smart Health Dashboard:** Real-time visualization of BMI, BMR, TDEE, and daily calorie targets.
* **🇮🇳 Indian Food Database:** Built-in standard menu options specifically curated for Indian cuisine (Roti, Dal, Paneer, etc.).
* **🔒 Secure Deployment:** Implemented industry-standard security using Streamlit Secrets management and SSL bypass protocols for reliable cloud connectivity.

## 🛠️ Tech Stack

* **Frontend:** Streamlit (Python)
* **Backend Logic:** Python (Pandas, NumPy)
* **Machine Learning:** Scikit-Learn (Linear Regression)
* **Database:** MongoDB Atlas (Cloud)
* **Deployment:** Streamlit Cloud

## 📂 Project Structure

smart-diet-tracker/
├── app.py                # Main application source code
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
├── data/
│   └── indian_food_dataset.csv  # Dataset for standard menu items
├── models/
│   └── calorie_model.pkl        # Pre-trained ML model for prediction
└── .gitignore            # Files excluded from Git

## ⚙️ How to Run Locally

If you want to run this app on your own machine:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/iotabhi/smart-diet-tracker.git](https://github.com/iotabhi/smart-diet-tracker.git)
    cd smart-diet-tracker
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up Secrets:**
    * Create a folder named `.streamlit` in the root directory.
    * Create a file `.streamlit/secrets.toml`.
    * Add your MongoDB connection string:
    ```toml
    [mongo]
    uri = "your_mongodb_connection_string_here"
    ```

4.  **Run the App:**
    ```bash
    streamlit run app.py
    ```

## 👨‍💻 Author

**Abhilasha**
* **Role:** Full Stack Developer & ML Enthusiast
* **Education:** B.Tech CSE (2nd Year)
* **Focus:** Building real-world applications with Python and AI.

---
*Built with ❤️ and Python.*
