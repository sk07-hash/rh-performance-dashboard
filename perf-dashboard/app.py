import streamlit as st
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="RH Performance Dashboard", layout="wide")

# ---------------- STYLE ---------------- #

st.markdown("""
<style>

.stApp{
background-color:#0E1117;
color:white;
}

.metric-card{
background:#1c1f26;
padding:20px;
border-radius:12px;
text-align:center;
box-shadow:0px 2px 10px rgba(0,0,0,0.6);
}

.metric-title{
font-size:14px;
color:#9aa0a6;
}

.metric-value{
font-size:28px;
font-weight:bold;
color:white;
}

h1,h2,h3{
color:#4CAF50;
}

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ---------------- #

st.title("RH Performance Dashboard")

# ---------------- SIDEBAR ---------------- #

st.sidebar.title("Navigation")

page = st.sidebar.radio(
"",
["Overall Dashboard","API Performance","GraphQL Performance","Frontend Metrics"]
)

# ---------------- DATA ---------------- #

folder = os.path.join(os.path.dirname(__file__), "reports")

api_files = sorted([f for f in os.listdir(folder) if f.startswith("API_")])
graphql_files = sorted([f for f in os.listdir(folder) if f.startswith("graphql_")])
ui_files = sorted([f for f in os.listdir(folder) if f.startswith("UI_")])

api_df = pd.read_csv(os.path.join(folder, api_files[-1]))
graphql_df = pd.read_csv(os.path.join(folder, graphql_files[-1]))
ui_df = pd.read_csv(os.path.join(folder, ui_files[-1]))

api_df.columns = api_df.columns.str.strip()
graphql_df.columns = graphql_df.columns.str.strip()
ui_df.columns = ui_df.columns.str.strip()

# ---------------- FUNCTIONS ---------------- #

def create_gauge(title,value):

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title},
        gauge={
            'axis': {'range': [0,100]},
            'bar': {'color': "#00C49F"},
            'steps': [
                {'range':[0,50],'color':"#8B0000"},
                {'range':[50,80],'color':"#FFA500"},
                {'range':[80,100],'color':"#006400"}
            ]
        }
    ))

    return fig


def regression(current,previous):

    return round(((current-previous)/previous)*100,2)

# ---------------- OVERALL DASHBOARD ---------------- #

if page=="Overall Dashboard":

    st.header("System Performance Overview")

    col1,col2,col3,col4 = st.columns(4)

    col1.metric("Total APIs",len(api_df))
    col2.metric("GraphQL Queries",len(graphql_df))
    col3.metric("Frontend Pages",len(ui_df))
    col4.metric("Avg API p95",round(api_df["95% Line"].mean(),2))

    st.divider()

    colA,colB = st.columns(2)

    with colA:

        st.subheader("API Latency")

        fig = px.bar(api_df,x="APIs",y="95% Line",color="95% Line")
        st.plotly_chart(fig,use_container_width=True)

    with colB:

        st.subheader("GraphQL Latency")

        fig = px.bar(graphql_df,x="GraphQL (BFF)",y="95% Line",color="95% Line")
        st.plotly_chart(fig,use_container_width=True)

    # ---------- FRONTEND GAUGES ---------- #

    st.subheader("Frontend Performance")

    col1,col2,col3,col4 = st.columns(4)

    for i,row in ui_df.iterrows():

        if i==0:
            col1.plotly_chart(create_gauge(row["Pages"],row["Performance Score"]),use_container_width=True)

        if i==1:
            col2.plotly_chart(create_gauge(row["Pages"],row["Performance Score"]),use_container_width=True)

        if i==2:
            col3.plotly_chart(create_gauge(row["Pages"],row["Performance Score"]),use_container_width=True)

        if i==3:
            col4.plotly_chart(create_gauge(row["Pages"],row["Performance Score"]),use_container_width=True)

    st.subheader("SEO Scores")

    col1,col2,col3,col4 = st.columns(4)

    for i,row in ui_df.iterrows():

        if i==0:
            col1.plotly_chart(create_gauge(row["Pages"]+" SEO",row["SEO Score"]),use_container_width=True)

        if i==1:
            col2.plotly_chart(create_gauge(row["Pages"]+" SEO",row["SEO Score"]),use_container_width=True)

        if i==2:
            col3.plotly_chart(create_gauge(row["Pages"]+" SEO",row["SEO Score"]),use_container_width=True)

        if i==3:
            col4.plotly_chart(create_gauge(row["Pages"]+" SEO",row["SEO Score"]),use_container_width=True)

    # ---------- REGRESSION CHARTS ---------- #

    st.divider()
    st.header("Regression Analysis")

    if len(api_files) > 1:

        prev_api = pd.read_csv(os.path.join(folder, api_files[-2]))

        regression_data = []

        for i,row in api_df.iterrows():

            api=row["APIs"]

            prev_row = prev_api[prev_api["APIs"]==api]

            if not prev_row.empty:

                prev = prev_row.iloc[0]["95% Line"]
                curr = row["95% Line"]

                regression_data.append({
                    "API":api,
                    "Change %":regression(curr,prev)
                })

        reg_df=pd.DataFrame(regression_data)

        fig = px.bar(reg_df,x="API",y="Change %",title="API Regression %")

        st.plotly_chart(fig,use_container_width=True)

    if len(graphql_files) > 1:

        prev_graphql = pd.read_csv(os.path.join(folder, graphql_files[-2]))

        regression_data = []

        for i,row in graphql_df.iterrows():

            query=row["GraphQL (BFF)"]

            prev_row = prev_graphql[prev_graphql["GraphQL (BFF)"]==query]

            if not prev_row.empty:

                prev = prev_row.iloc[0]["95% Line"]
                curr = row["95% Line"]

                regression_data.append({
                    "Query":query,
                    "Change %":regression(curr,prev)
                })

        reg_df=pd.DataFrame(regression_data)

        fig = px.bar(reg_df,x="Query",y="Change %",title="GraphQL Regression %")

        st.plotly_chart(fig,use_container_width=True)

# ---------------- API PAGE ---------------- #

if page=="API Performance":

    st.header("API Performance")

    tab1,tab2 = st.tabs(["Charts","Data"])

    with tab1:

        fig = px.bar(api_df,x="APIs",y=["Average","95% Line","99% Line"],barmode="group")
        st.plotly_chart(fig,use_container_width=True)

        fig = px.pie(api_df,names="APIs",values="TPS")
        st.plotly_chart(fig,use_container_width=True)

        fig = px.scatter(api_df,x="Average",y="95% Line",size="TPS",color="APIs")
        st.plotly_chart(fig,use_container_width=True)

    with tab2:

        st.dataframe(api_df,use_container_width=True)

# ---------------- GRAPHQL PAGE ---------------- #

if page=="GraphQL Performance":

    st.header("GraphQL Performance")

    tab1,tab2 = st.tabs(["Charts","Data"])

    with tab1:

        fig = go.Figure()

        for i,row in graphql_df.iterrows():

            fig.add_trace(go.Scatterpolar(
                r=[row["Average"],row["95% Line"],row["99% Line"]],
                theta=["Average","p95","p99"],
                fill='toself',
                name=row["GraphQL (BFF)"]
            ))

        st.plotly_chart(fig,use_container_width=True)

        fig = px.bar(graphql_df,x="GraphQL (BFF)",y="95% Line")
        st.plotly_chart(fig,use_container_width=True)

    with tab2:

        st.dataframe(graphql_df,use_container_width=True)

# ---------------- FRONTEND PAGE ---------------- #

if page=="Frontend Metrics":

    st.header("Frontend Metrics")

    col1,col2,col3,col4 = st.columns(4)

    for i,row in ui_df.iterrows():

        if i==0:
            col1.plotly_chart(create_gauge(row["Pages"],row["Performance Score"]),use_container_width=True)

        if i==1:
            col2.plotly_chart(create_gauge(row["Pages"],row["Performance Score"]),use_container_width=True)

        if i==2:
            col3.plotly_chart(create_gauge(row["Pages"],row["Performance Score"]),use_container_width=True)

        if i==3:
            col4.plotly_chart(create_gauge(row["Pages"],row["Performance Score"]),use_container_width=True)

    st.subheader("Core Web Vitals")

    fig = px.imshow(
        ui_df[["FCP","LCP","TBT","CLS"]],
        labels=dict(x="Metric",y="Page"),
        y=ui_df["Pages"],
        color_continuous_scale="RdYlGn_r"
    )

    st.plotly_chart(fig,use_container_width=True)

    st.subheader("Data")

    st.dataframe(ui_df,use_container_width=True)
