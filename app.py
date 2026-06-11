import os
import streamlit as st
import pandas as pd
from datetime import date

# Page config
st.set_page_config(page_title="Rider Profit Tracker", page_icon="💰", layout="wide")

# Custom styling
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: white;
    }
    .stNumberInput label {
        color: #00ffcc !important;
        font-weight: bold;
    }
    .stButton>button {
        background-color: #00ffcc;
        color: black;
        border-radius: 10px;
        height: 3em;
        width: 100%;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.title("💰 Daily Earnings Tracker")

# ✅ Safe load
if os.path.exists("data.csv"):
    data = pd.read_csv("data.csv")
else:
    data = pd.DataFrame(columns=["Date","Earnings","Petrol","Food","Other","Profit"])

# Ensure Date is string
data["Date"] = data["Date"].astype(str)

# ================= DATE SELECTION =================
st.header("📅 Select Date")

selected_date = st.date_input("Choose Date", value=date.today())

# Check existing entry
existing_entry = data[data["Date"] == str(selected_date)]

if not existing_entry.empty:
    st.info("✏️ Editing existing entry")

    default_earnings = int(existing_entry["Earnings"].values[0])
    default_petrol = int(existing_entry["Petrol"].values[0])
    default_food = int(existing_entry["Food"].values[0])
    default_other = int(existing_entry["Other"].values[0])
else:
    default_earnings = 0
    default_petrol = 0
    default_food = 0
    default_other = 0

# ================= INPUT SECTION =================
st.header("📥 Enter / Edit Data")

col1, col2 = st.columns(2)

with col1:
    earnings = st.number_input("Earnings (₹)", min_value=0, value=default_earnings)
    petrol = st.number_input("Petrol (₹)", min_value=0, value=default_petrol)

with col2:
    food = st.number_input("Food (₹)", min_value=0, value=default_food)
    other = st.number_input("Other Expenses (₹)", min_value=0, value=default_other)

# Calculate profit
profit = earnings - (petrol + food + other)

st.subheader(f"Today's Profit: ₹{profit}")

# ================= SAVE / UPDATE =================
if st.button("Save / Update Entry"):
    new_data = pd.DataFrame({
        "Date": [str(selected_date)],
        "Earnings": [earnings],
        "Petrol": [petrol],
        "Food": [food],
        "Other": [other],
        "Profit": [profit]
    })

    # Remove old entry
    data = data[data["Date"] != str(selected_date)]

    # Add updated entry
    data = pd.concat([data, new_data], ignore_index=True)

    data.to_csv("data.csv", index=False)

    st.success("✅ Saved / Updated!")

# ================= DATA DISPLAY =================
st.header("📊 Weekly Data")

if not data.empty:
    data["Date"] = pd.to_datetime(data["Date"])
    st.line_chart(data.set_index("Date")["Profit"])
else:
    st.info("No data yet.")

# ================= SUMMARY =================
st.header("📈 Summary")

total_earnings = data["Earnings"].sum()
total_expenses = data["Petrol"].sum() + data["Food"].sum() + data["Other"].sum()
total_profit = data["Profit"].sum()

st.write(f"💰 Total Earnings: ₹{total_earnings}")
st.write(f"💸 Total Expenses: ₹{total_expenses}")
st.write(f"🔥 Total Profit: ₹{total_profit}")

# ================= EXPENSE BREAKDOWN =================
st.header("📊 Expense Breakdown")

expenses = {
    "Petrol": data["Petrol"].sum(),
    "Food": data["Food"].sum(),
    "Other": data["Other"].sum()
}

st.bar_chart(expenses)

# ================= INSIGHTS =================
st.header("🧠 Insights")

if total_earnings > 0 and total_expenses > total_earnings * 0.6:
    st.warning("⚠️ You are spending more than 60% of your earnings!")

if not data.empty and data["Profit"].mean() < 500:
    st.warning("⚠️ Your average daily profit is less than ₹500.")

# ================= TARGET =================
st.header("🎯 Daily Target")

target = st.number_input("Enter your daily target (₹)", min_value=0)

if earnings < target:
    remaining = target - earnings
    st.warning(f"⚠️ You need ₹{remaining} more to reach your target!")

    extra_hours = remaining / 100
    st.info(f"💡 Work approx {round(extra_hours,1)} more hours")

elif target > 0:
    st.success("🔥 Target achieved!")

# ================= PERFORMANCE =================
st.header("🏆 Performance")

if not data.empty:
    best_day = data.loc[data["Profit"].idxmax()]
    st.write(f"Best Day: {best_day['Date']}")
    st.write(f"Profit: ₹{best_day['Profit']}")