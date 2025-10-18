# BrightCart — Marketing & Sales Dashboard (v2.2 stable)
# Fully working, grouped by week so charts look clean

import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="BrightCart — Marketing & Sales Dashboard",
    page_icon="🛒",
    layout="wide"
)

# -----------------------------
# Load Data
# -----------------------------
DATA_PATH = "data/cleaned/brightcart_clean.csv"

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    df["Week"] = pd.to_datetime(df["Week"], errors="coerce")
    return df

df = load_data(DATA_PATH)

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("Filters")

channels = sorted(df["Channel"].unique().tolist())
selected_channels = st.sidebar.multiselect(
    "Select Channels:",
    options=channels,
    default=channels
)

min_date, max_date = df["Week"].min(), df["Week"].max()
date_range = st.sidebar.date_input(
    "Date range:",
    (min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

mask = df["Channel"].isin(selected_channels)
start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
mask &= (df["Week"] >= start) & (df["Week"] <= end)
fdf = df.loc[mask].copy()

# -----------------------------
# Header & KPIs
# -----------------------------
st.title("BrightCart — Marketing & Sales Dashboard")
st.caption("Portfolio demo • Built with Python, Pandas, Plotly & Streamlit")

total_revenue = fdf["Revenue"].sum()
total_profit = fdf["Profit"].sum()
avg_roas = fdf["ROAS"].mean()
avg_margin = fdf["Profit_Margin"].mean()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"${total_revenue:,.0f}")
col2.metric("Total Profit", f"${total_profit:,.0f}")
col3.metric("Avg ROAS", f"{avg_roas:.2f}x")
col4.metric("Profit Margin", f"{avg_margin:.2f}%")

st.divider()

# -----------------------------
# Tabs
# -----------------------------
tab1, tab2, tab3 = st.tabs(["Overview", "Channel Insights", "Efficiency"])

# ---------- Overview ----------
with tab1:
    st.subheader("💵 Weekly Net Sales vs Ad Spend")

    # ✅ Group by week for clean chart
    weekly = (
        fdf.groupby("Week", as_index=False)[["Net_Sales", "Spend"]]
        .sum()
        .sort_values("Week")
    )

    long_df = weekly.melt(
        id_vars="Week", value_vars=["Net_Sales", "Spend"],
        var_name="Metric", value_name="Value"
    )

    fig1 = px.line(
        long_df, x="Week", y="Value", color="Metric",
        markers=True, template="plotly_white"
    )
    fig1.update_traces(line=dict(width=2))
    fig1.update_layout(height=400, legend_title_text="")
    st.plotly_chart(fig1, use_container_width=True)

# ---------- Channel Insights ----------
with tab2:
    st.subheader("💰 Total Profit by Channel")

    profit_by_channel = (
        fdf.groupby("Channel", as_index=False)["Profit"].sum()
        .sort_values("Profit", ascending=False)
    )
    fig2 = px.bar(profit_by_channel, x="Channel", y="Profit", template="plotly_white")
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("📈 ROAS by Channel")
    roas_by_channel = fdf.groupby("Channel", as_index=False)["ROAS"].mean().round(2)
    st.dataframe(roas_by_channel, use_container_width=True)

# ---------- Efficiency ----------
with tab3:
    st.subheader("⚙️ ROAS vs Spend (bubble = Net Sales)")

    bubble = fdf.groupby("Channel", as_index=False).agg({
        "Spend": "sum",
        "ROAS": "mean",
        "Net_Sales": "sum"
    })
    fig3 = px.scatter(
        bubble, x="Spend", y="ROAS", size="Net_Sales", color="Channel",
        hover_data=["Net_Sales"], template="plotly_white"
    )
    fig3.update_layout(height=400)
    st.plotly_chart(fig3, use_container_width=True)

# -----------------------------
# Insights Summary
# -----------------------------
st.divider()
st.subheader("🔍 Key Insights Summary")

try:
    top_channel = fdf.groupby("Channel")["Profit"].sum().idxmax()
    top_profit = fdf.groupby("Channel")["Profit"].sum().max()

    low_roas = fdf.groupby("Channel")["ROAS"].mean().idxmin()
    low_roas_val = fdf.groupby("Channel")["ROAS"].mean().min()

    st.success(f"💰 **{top_channel}** generated the highest profit (${top_profit:,.0f}).")
    st.warning(f"⚠️ **{low_roas}** has the lowest average ROAS ({low_roas_val:.2f}x).")

    st.info(
        f"Average profit margin: **{avg_margin:.2f}%**, "
        f"Total revenue: **${total_revenue:,.0f}**."
    )
except Exception as e:
    st.error(f"Error generating insights: {e}")
