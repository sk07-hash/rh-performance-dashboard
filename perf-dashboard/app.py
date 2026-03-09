import streamlit as st
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="RH Performance Dashboard", layout="wide")

st.title("RH Performance Dashboard")

# --------------------------
# SIDEBAR NAVIGATION
# --------------------------

page = st.sidebar.radio(
"Navigation",
["Overall Dashboard","API Performance","GraphQL Performance","Frontend Metrics"]
)

# --------------------------
# LOAD DATA
# --------------------------

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

# --------------------------
# FUNCTIONS
# --------------------------

def gauge(title,value):

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text':title},
        gauge={'axis':{'range':[0,100]}}
    ))

    return fig


def regression(curr,prev):

    return round(((curr-prev)/prev)*100,2)

# =====================================================
# OVERALL DASHBOARD
# =====================================================

if page == "Overall Dashboard":

    st.header("System Overview")

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("Total APIs",len(api_df))
    c2.metric("GraphQL Queries",len(graphql_df))
    c3.metric("Frontend Pages",len(ui_df))
    c4.metric("Avg API p95",round(api_df["95% Line"].mean(),2))

    st.divider()

    # -------- API --------

    st.subheader("API Latency")

    fig = px.bar(api_df,x="APIs",y="95% Line",color="95% Line")
    st.plotly_chart(fig,use_container_width=True)

    st.dataframe(api_df,use_container_width=True)

    if len(api_files) > 1:

        prev_api = pd.read_csv(os.path.join(folder,api_files[-2]))

        rows=[]

        for i,row in api_df.iterrows():

            api=row["APIs"]

            prev_row=prev_api[prev_api["APIs"]==api]

            if not prev_row.empty:

                prev=prev_row.iloc[0]["95% Line"]
                curr=row["95% Line"]

                rows.append({
                    "API":api,
                    "Change %":regression(curr,prev)
                })

        reg_df=pd.DataFrame(rows)

        fig = px.bar(reg_df,x="API",y="Change %",title="API Regression %")
        st.plotly_chart(fig,use_container_width=True)

        st.dataframe(reg_df,use_container_width=True)

    # -------- GRAPHQL --------

    st.subheader("GraphQL Latency")

    fig = px.bar(graphql_df,x="GraphQL (BFF)",y="95% Line",color="95% Line")
    st.plotly_chart(fig,use_container_width=True)

    st.dataframe(graphql_df,use_container_width=True)

    if len(graphql_files) > 1:

        prev = pd.read_csv(os.path.join(folder,graphql_files[-2]))

        rows=[]

        for i,row in graphql_df.iterrows():

            q=row["GraphQL (BFF)"]

            prev_row=prev[prev["GraphQL (BFF)"]==q]

            if not prev_row.empty:

                prev_val=prev_row.iloc[0]["95% Line"]
                curr=row["95% Line"]

                rows.append({
                    "Query":q,
                    "Change %":regression(curr,prev_val)
                })

        reg_df=pd.DataFrame(rows)

        fig = px.bar(reg_df,x="Query",y="Change %",title="GraphQL Regression %")
        st.plotly_chart(fig,use_container_width=True)

        st.dataframe(reg_df,use_container_width=True)

    # -------- FRONTEND --------

    st.subheader("Frontend Performance")

    col1,col2,col3,col4 = st.columns(4)

    for i,row in ui_df.iterrows():

        if i==0: col1.plotly_chart(gauge(row["Pages"],row["Performance Score"]),use_container_width=True)
        if i==1: col2.plotly_chart(gauge(row["Pages"],row["Performance Score"]),use_container_width=True)
        if i==2: col3.plotly_chart(gauge(row["Pages"],row["Performance Score"]),use_container_width=True)
        if i==3: col4.plotly_chart(gauge(row["Pages"],row["Performance Score"]),use_container_width=True)

    st.subheader("SEO Scores")

    col1,col2,col3,col4 = st.columns(4)

    for i,row in ui_df.iterrows():

        if i==0: col1.plotly_chart(gauge(row["Pages"]+" SEO",row["SEO Score"]),use_container_width=True)
        if i==1: col2.plotly_chart(gauge(row["Pages"]+" SEO",row["SEO Score"]),use_container_width=True)
        if i==2: col3.plotly_chart(gauge(row["Pages"]+" SEO",row["SEO Score"]),use_container_width=True)
        if i==3: col4.plotly_chart(gauge(row["Pages"]+" SEO",row["SEO Score"]),use_container_width=True)

    st.dataframe(ui_df,use_container_width=True)

# =====================================================
# API PAGE
# =====================================================

elif page == "API Performance":

    st.header("API Performance")

    tabs = st.tabs(["Charts","Data","Regression"])

    with tabs[0]:

        fig = px.bar(api_df,x="APIs",y=["Average","95% Line","99% Line"],barmode="group")
        st.plotly_chart(fig,use_container_width=True)

        fig = px.pie(api_df,names="APIs",values="TPS")
        st.plotly_chart(fig,use_container_width=True)

        fig = px.scatter(api_df,x="Average",y="95% Line",size="TPS",color="APIs")
        st.plotly_chart(fig,use_container_width=True)

    with tabs[1]:

        st.dataframe(api_df,use_container_width=True)

    with tabs[2]:

        if len(api_files) > 1:

            prev_api = pd.read_csv(os.path.join(folder,api_files[-2]))

            rows=[]

            for i,row in api_df.iterrows():

                api=row["APIs"]

                prev_row=prev_api[prev_api["APIs"]==api]

                if not prev_row.empty:

                    prev=prev_row.iloc[0]["95% Line"]
                    curr=row["95% Line"]

                    rows.append({
                        "API":api,
                        "Previous p95":prev,
                        "Current p95":curr,
                        "Change %":regression(curr,prev)
                    })

            reg_df=pd.DataFrame(rows)

            st.dataframe(reg_df,use_container_width=True)

# =====================================================
# GRAPHQL PAGE
# =====================================================

elif page == "GraphQL Performance":

    st.header("GraphQL Performance")

    tabs = st.tabs(["Charts","Data","Regression"])

    with tabs[0]:

        fig = px.bar(graphql_df,x="GraphQL (BFF)",y="95% Line")
        st.plotly_chart(fig,use_container_width=True)

        radar = go.Figure()

        for i,row in graphql_df.iterrows():

            radar.add_trace(go.Scatterpolar(
                r=[row["Average"],row["95% Line"],row["99% Line"]],
                theta=["Average","p95","p99"],
                fill='toself',
                name=row["GraphQL (BFF)"]
            ))

        st.plotly_chart(radar,use_container_width=True)

    with tabs[1]:

        st.dataframe(graphql_df,use_container_width=True)

    with tabs[2]:

        if len(graphql_files) > 1:

            prev = pd.read_csv(os.path.join(folder,graphql_files[-2]))

            rows=[]

            for i,row in graphql_df.iterrows():

                q=row["GraphQL (BFF)"]

                prev_row=prev[prev["GraphQL (BFF)"]==q]

                if not prev_row.empty:

                    prev_val=prev_row.iloc[0]["95% Line"]
                    curr=row["95% Line"]

                    rows.append({
                        "Query":q,
                        "Previous p95":prev_val,
                        "Current p95":curr,
                        "Change %":regression(curr,prev_val)
                    })

            reg_df=pd.DataFrame(rows)

            st.dataframe(reg_df,use_container_width=True)

# =====================================================
# FRONTEND PAGE
# =====================================================

elif page == "Frontend Metrics":

    st.header("Frontend Metrics")

    col1,col2,col3,col4 = st.columns(4)

    for i,row in ui_df.iterrows():

        if i==0: col1.plotly_chart(gauge(row["Pages"],row["Performance Score"]),use_container_width=True)
        if i==1: col2.plotly_chart(gauge(row["Pages"],row["Performance Score"]),use_container_width=True)
        if i==2: col3.plotly_chart(gauge(row["Pages"],row["Performance Score"]),use_container_width=True)
        if i==3: col4.plotly_chart(gauge(row["Pages"],row["Performance Score"]),use_container_width=True)

    st.subheader("Core Web Vitals")

    fig = px.imshow(
        ui_df[["FCP","LCP","TBT","CLS"]],
        labels=dict(x="Metric",y="Page"),
        y=ui_df["Pages"],
        color_continuous_scale="RdYlGn_r"
    )

    st.plotly_chart(fig,use_container_width=True)

    st.dataframe(ui_df,use_container_width=True)
