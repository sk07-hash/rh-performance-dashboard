import streamlit as st
import pandas as pd
import os
import plotly.express as px

# --------------------------------------------------
# Page Config
# --------------------------------------------------

st.set_page_config(page_title="RH Performance Dashboard", layout="wide")

# --------------------------------------------------
# Dark Theme
# --------------------------------------------------

st.markdown("""
<style>

.stApp {
    background-color: #0E1117;
    color: white;
}

h1, h2, h3 {
    color: #4CAF50;
}

[data-testid="metric-container"] {
    background-color: #1E1E1E;
    border-radius: 10px;
    padding: 15px;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Title
# --------------------------------------------------

st.title("RH Performance Dashboard")

# --------------------------------------------------
# Reports Folder
# --------------------------------------------------

folder = "reports"

if not os.path.exists(folder):
    st.error("Reports folder not found in repository.")
    st.stop()

files = [f for f in os.listdir(folder) if f.endswith(".csv")]

if len(files) == 0:
    st.warning("No reports available.")
    st.stop()

# --------------------------------------------------
# Run Selection
# --------------------------------------------------

files = sorted(files)

selected_file = st.selectbox(
    "Select Performance Run",
    files
)

file_path = os.path.join(folder, selected_file)

df = pd.read_csv(file_path)

# --------------------------------------------------
# Clean Columns
# --------------------------------------------------

df.columns = df.columns.str.strip()

numeric_cols = ["Average","95% Line","99% Line","Max","TPS"]

for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# --------------------------------------------------
# Summary Metrics
# --------------------------------------------------

avg = df["Average"].mean()
p95 = df["95% Line"].mean()
p99 = df["99% Line"].mean()
tps = df["TPS"].sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Average Response Time", round(avg,2))
col2.metric("p95 Response Time", round(p95,2))
col3.metric("p99 Response Time", round(p99,2))
col4.metric("Total TPS", round(tps,2))

# --------------------------------------------------
# SLA Detection
# --------------------------------------------------

sla = 500

df["Status"] = df["95% Line"].apply(
    lambda x: "OK" if x < sla else "SLOW"
)

# --------------------------------------------------
# API Performance Table
# --------------------------------------------------

st.subheader("API Performance")

st.dataframe(
    df[["APIs","Average","95% Line","99% Line","TPS","Status"]],
    use_container_width=True
)

# --------------------------------------------------
# Chart 1 - Response Time Comparison
# --------------------------------------------------

st.subheader("API Response Time Comparison")

fig = px.bar(
    df,
    x="APIs",
    y=["Average","95% Line","99% Line"],
    barmode="group",
    title="Average vs p95 vs p99"
)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# Chart 2 - TPS Chart
# --------------------------------------------------

st.subheader("API Throughput")

fig2 = px.bar(
    df,
    x="APIs",
    y="TPS",
    color="TPS",
    title="Transactions Per Second"
)

st.plotly_chart(fig2, use_container_width=True)

# --------------------------------------------------
# SLA Violations
# --------------------------------------------------

st.subheader("SLA Violations")

violations = df[df["Status"] == "SLOW"]

if violations.empty:
    st.success("No SLA violations")
else:
    st.warning("APIs exceeding SLA (p95 > 500ms)")
    st.dataframe(
        violations[["APIs","95% Line","TPS"]],
        use_container_width=True
    )

# --------------------------------------------------
# Trend Across Runs
# --------------------------------------------------

st.subheader("Performance Trend Across Runs")

trend_data = []

for f in files:

    temp = pd.read_csv(os.path.join(folder, f))

    temp.columns = temp.columns.str.strip()

    for col in numeric_cols:
        if col in temp.columns:
            temp[col] = pd.to_numeric(temp[col], errors="coerce")

    trend_data.append({
        "Run": f,
        "Average": temp["Average"].mean(),
        "p95": temp["95% Line"].mean()
    })

trend_df = pd.DataFrame(trend_data)

fig3 = px.line(
    trend_df,
    x="Run",
    y=["Average","p95"],
    markers=True,
    title="Performance Trend"
)

st.plotly_chart(fig3, use_container_width=True)
