import uuid #genrates Client ID
from decimal import Decimal
from datetime import date
import streamlit as st
import database as db
import pandas as pd

st.set_page_config(
    page_title="Expense Tracker",
    page_icon="₹",
    layout="wide",
)

db.init_db()

st.subheader("Add New Expense")

with st.form("add_expense_form", clear_on_submit=True):
    amount = st.text_input("Amount (₹)", placeholder="e.g. 250.00")
    category = st.selectbox("Category", [
        "Food & Dining", "Transport", "Shopping",
        "Entertainment", "Health & Medical",
        "Utilities & Bills", "Rent", "Education", "Other"
    ])
    description = st.text_input("Description", placeholder="e.g. Lunch at canteen")
    expense_date = st.date_input("Date", value=date.today())
    submitted = st.form_submit_button("Add Expense")
    
if submitted:
    try :
        amount_decimal = Decimal(amount.strip())
        db.create_expense(
            client_id= str(uuid.uuid4()),
            amount= amount_decimal,
            category= category,
            description=description,
            date=expense_date.isoformat(),
            
        )
        st.success("Your expenses added succesfully... Thankyou")
    except ValueError as e:
        st.error(str(e))

st.subheader(" Your enterd expenses")
col1, col2 = st.columns(2)

with col1:
    selected_category = st.selectbox("Filter by Category", 
        ["All", "Food & Dining", "Transport", "Shopping",
        "Entertainment", "Health & Medical",
        "Utilities & Bills", "Rent", "Education", "Other"])

with col2:
    sort_order = st.selectbox("Sort by Date", 
        ["Newest First", "Oldest First"])

expenses = db.get_expenses(
    category=selected_category,
    sort_by_date_desc=(sort_order == "Newest First")
)

if not expenses:
    st.info("You have no expenses added please add your first expense above !!")
else:
    table_data = [{
        "Date": e["date"],
        "Category": e["category"],
        "Description": e["description"],
        "Amount (₹)": f"₹{e['amount_rupees']:,.2f}"
    } for e in expenses]

    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True)

    total = sum(e["amount_rupees"] for e in expenses)
    st.markdown(f"### Total: ₹{total:,.2f}")