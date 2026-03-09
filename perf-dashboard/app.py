import streamlit as st
import pandas as pd
import os
import plotly.express as px

st.set_page_config(page_title="RH Performance Dashboard", layout="wide")

# ------------------------------------------------
# THEME
# ------------------------------------------------

st.markdown("""
<style>
.stApp {
background-color:#0E1117;
color:white;
}

h1,h2,h3{
color:#4CAF50;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# TITLE
# ------------------------------------------------

st.title("RH Performance Dashboard")

# ------------------------------------------------
# NAVIGATION
# ------------------------------------------------

page = st.sidebar.radio(
"Navigation",
["Overall Dashboard","API Performance","GraphQL Performance","Frontend Metrics"]
)

# ------------------------------------------------
# DATA PATH
# ------------------------------------------------

folder = os.path.join(os.path.dirname(__file__), "reports")

api_file = os.path.join(folder,"API_1.csv")
graphql_file = os.path.join(folder,"graphql_1.csv")
ui_file = os.path.join(folder,"UI_1.csv")

# ------------------------------------------------
# LOAD DATA
# ------------------------------------------------

api_df = pd.read_csv(api_file)
graphql_df = pd.read_csv(graphql_file)
ui_df = pd.read_csv(ui_file)

# ------------------------------------------------
# OVERALL DASHBOARD
# ------------------------------------------------

if page == "Overall Dashboard":

    st.header("Overall Performance Overview")

    col1,col2,col3 = st.columns(3)

    col1.metric("Total APIs", len(api_df))
    col2.metric("GraphQL Queries", len(graphql_df))
    col3.metric("Frontend Pages", len(ui_df))

    st.subheader("API Latency Overview")

    fig = px.bar(
        api_df,
        x="APIs",
        y="95% Line",
        title="API p95 Latency"
    )

    st.plotly_chart(fig,use_container_width=True)

    st.subheader("GraphQL Latency Overview")

    fig2 = px.bar(
        graphql_df,
        x="GraphQL (BFF)",
        y="95% Line",
        title="GraphQL p95 Latency"
    )

    st.plotly_chart(fig2,use_container_width=True)

    st.subheader("Frontend Performance Score")

    fig3 = px.bar(
        ui_df,
        x="Pages",
        y="Performance Score",
        title="Frontend Performance Score"
    )

    st.plotly_chart(fig3,use_container_width=True)

# ------------------------------------------------
# API PAGE
# ------------------------------------------------

if page == "API Performance":

    st.header("API Performance Metrics")

    avg = api_df["Average"].mean()
    p95 = api_df["95% Line"].mean()
    p99 = api_df["99% Line"].mean()

    col1,col2,col3 = st.columns(3)

    col1.metric("Average Response",round(avg,2))
    col2.metric("p95",round(p95,2))
    col3.metric("p99",round(p99,2))

    st.dataframe(api_df)

    fig = px.bar(
        api_df,
        x="APIs",
        y=["Average","95% Line","99% Line"],
        barmode="group",
        title="API Latency Comparison"
    )

    st.plotly_chart(fig,use_container_width=True)

    fig2 = px.bar(
        api_df,
        x="APIs",
        y="TPS",
        color="TPS",
        title="API Throughput"
    )

    st.plotly_chart(fig2,use_container_width=True)

# ------------------------------------------------
# GRAPHQL PAGE
# ------------------------------------------------

if page == "GraphQL Performance":

    st.header("GraphQL Performance")

    avg = graphql_df["Average"].mean()
    p95 = graphql_df["95% Line"].mean()

    col1,col2 = st.columns(2)

    col1.metric("Average Latency",round(avg,2))
    col2.metric("p95",round(p95,2))

    st.dataframe(graphql_df)

    fig = px.bar(
        graphql_df,
        x="GraphQL (BFF)",
        y=["Average","95% Line","99% Line"],
        barmode="group",
        title="GraphQL Query Latency"
    )

    st.plotly_chart(fig,use_container_width=True)

# ------------------------------------------------
# FRONTEND PAGE
# ------------------------------------------------

if page == "Frontend Metrics":

    st.header("Frontend / Lighthouse Metrics")

    avg_score = ui_df["Performance Score"].mean()

    st.metric("Avg Performance Score",round(avg_score,2))

    st.dataframe(ui_df)

    fig = px.bar(
        ui_df,
        x="Pages",
        y="Performance Score",
        title="Performance Score by Page"
    )

    st.plotly_chart(fig,use_container_width=True)

    fig2 = px.bar(
        ui_df,
        x="Pages",
        y=["FCP","LCP","TBT"],
        barmode="group",
        title="Frontend Core Web Vitals"
    )

    st.plotly_chart(fig2,use_container_width=True)
