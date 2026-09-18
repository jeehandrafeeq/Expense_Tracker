import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
import os

st.set_page_config(page_title="Expense Tracker",
                   page_icon="💰",
                   layout="wide")

st.title("💰 Personal Expense Tracker")

FILE = "expense.csv"

# Create file if it doesn't exist
if not os.path.exists(FILE):
    df = pd.DataFrame(columns=[
        "Date",
        "Type",
        "Category",
        "Amount",
        "Description"
    ])
    df.to_csv(FILE, index=False)

df = pd.read_csv(FILE)

# Sidebar
st.sidebar.header("Add Transaction")

transaction_date = st.sidebar.date_input("Date", date.today())

transaction_type = st.sidebar.selectbox(
    "Type",
    ["Income", "Expense"]
)

category = st.sidebar.selectbox(
    "Category",
    [
        "Salary",
        "Food",
        "Transport",
        "Shopping",
        "Bills",
        "Education",
        "Health",
        "Entertainment",
        "Other"
    ]
)

amount = st.sidebar.number_input(
    "Amount",
    min_value=0.0,
    step=100.0
)

description = st.sidebar.text_input("Description")

if st.sidebar.button("Add Transaction"):

    new = pd.DataFrame({
        "Date":[transaction_date],
        "Type":[transaction_type],
        "Category":[category],
        "Amount":[amount],
        "Description":[description]
    })

    df = pd.concat([df,new],ignore_index=True)
    df.to_csv(FILE,index=False)

    st.success("Transaction Added")
    st.rerun()

# Metrics

income = df[df["Type"]=="Income"]["Amount"].sum()
expense = df[df["Type"]=="Expense"]["Amount"].sum()
balance = income-expense

c1,c2,c3 = st.columns(3)

c1.metric("Income",f"Rs {income:,.0f}")
c2.metric("Expense",f"Rs {expense:,.0f}")
c3.metric("Balance",f"Rs {balance:,.0f}")

st.divider()

st.subheader("Transaction History")
st.dataframe(df,use_container_width=True)

st.download_button(
    "Download CSV",
    df.to_csv(index=False),
    file_name="Expense_Report.csv",
    mime="text/csv"
)

st.divider()

col1,col2 = st.columns(2)

# Pie Chart
with col1:

    st.subheader("Expenses by Category")

    exp = df[df["Type"]=="Expense"]

    if not exp.empty:

        chart = exp.groupby("Category")["Amount"].sum()

        fig,ax=plt.subplots()

        ax.pie(chart,
               labels=chart.index,
               autopct="%1.1f%%")

        st.pyplot(fig)

# Bar Chart
with col2:

    st.subheader("Income vs Expense")

    summary = df.groupby("Type")["Amount"].sum()

    fig,ax=plt.subplots()

    ax.bar(summary.index,summary.values)

    ax.set_ylabel("Amount")

    st.pyplot(fig)