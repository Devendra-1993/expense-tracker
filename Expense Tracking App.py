import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# --- Google Sheets authentication ---
scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]
creds = ServiceAccountCredentials.from_json_keyfile_name(
    r'C:\Users\DDeore\Box\Devendra Deore\Python\Expense tracking App\gspread-creds.json', scope)
client = gspread.authorize(creds)

# --- Open your Google Sheet ---
sheet = client.open("Expenses").sheet1

# --- Read data into DataFrame ---
data = sheet.get_all_records()
df = pd.DataFrame(data)

# --- Streamlit UI ---
st.set_page_config(page_title="Expense Tracker", layout="wide")
st.title("💸 Google Sheets Expense Tracker")

# Show current data
st.subheader("📋 Current Expenses")
st.dataframe(df)

# Add new entry form
with st.form("entry_form", clear_on_submit=True):
    name = st.text_input("Name")
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    date = st.date_input("Date", value=datetime.today())
    
    # To avoid errors if df is empty, fallback to some defaults
    categories = df["Expense Category"].unique().tolist() if not df.empty else ["House", "Transportation", "Grocery"]
    category = st.selectbox("Category", categories)
    
    # Assuming you want a fixed list of payers or get them dynamically
    payers = df["Paid By"].unique().tolist() if not df.empty else ["Dev", "Akki"]
    paid_by = st.selectbox("Paid By", payers)
    
    shared = st.selectbox("Shared", ["Yes", "No"])
    submit = st.form_submit_button("Add Expense")

    if submit:
        # Append to Google Sheet
        new_row = [name, amount, date.strftime("%Y-%m-%d"), category, paid_by, shared]
        sheet.append_row(new_row)
        st.success("Expense added!")
        st.experimental_rerun()  # Refresh to show new data
