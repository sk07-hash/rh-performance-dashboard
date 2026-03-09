import streamlit as st
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="RH Performance Dashboard", layout="wide")

# -----------------------------------------------------
# STYLE
# -----------------------------------------------------

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

# -----------------------------------------------------
# TITLE
# -----------------------------------------------------

st.title("RH Performance Dashboard")

# -----------------------------------------------------
# SIDEBAR
# -----------------------------------------------------

st.sidebar.title("Navigation")

page = st.sidebar.radio(
"",
["Overall Dashboard","API Performance","GraphQL Performance","Frontend Metrics"]
)

# -----------------------------------------------------
# LOAD DATA
# -----------------------------------------------------

folder = os.path.join(os.path.dirname(__file__), "reports")

api_df = pd.read_csv(os.path.join(folder,"API_1.csv"))
graphql_df = pd.read_csv(os.path.join(folder,"graphql_1.csv"))
ui_df = pd.read_csv(os.path.join(folder,"UI_1.csv"))

api_df.columns = api_df.columns.str.strip()
graphql_df.columns = graphql_df.columns.str.strip()
ui_df.columns = ui_df.columns.str.strip()

# -----------------------------------------------------
# GAUGE FUNCTION
# -----------------------------------------------------

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

# -----------------------------------------------------
# OVERALL DASHBOARD
# -----------------------------------------------------

if page == "Overall Dashboard":

    st.header("System Performance Overview")

    col1,col2,col3,col4 = st.columns(4)

    col1.markdown(f"""
    <div class="metric-card">
    <div class="metric-title">Total APIs</div>
    <div class="metric-value">{len(api_df)}</div>
    </div>
    """,unsafe_allow_html=True)

    col2.markdown(f"""
    <div class="metric-card">
    <div class="metric-title">GraphQL Queries</div>
    <div class="metric-value">{len(graphql_df)}</div>
    </div>
    """,unsafe_allow_html=True)

    col3.markdown(f"""
    <div class="metric-card">
    <div class="metric-title">Frontend Pages</div>
    <div class="metric-value">{len(ui_df)}</div>
    </div>
    """,unsafe_allow_html=True)

    col4.markdown(f"""
    <div class="metric-card">
    <div class="metric-title">Avg API p95</div>
    <div class="metric-value">{round(api_df['95% Line'].mean(),2)}</div>
    </div>
    """,unsafe_allow_html=True)

    st.divider()

    colA,colB = st.columns(2)

    with colA:

        st.subheader("API Latency Overview")

        fig = px.bar(
            api_df,
            x="APIs",
            y="95% Line",
            color="95% Line",
            color_continuous_scale="teal"
        )

        st.plotly_chart(fig,use_container_width=True)

    with colB:

        st.subheader("GraphQL Latency")

        fig = px.bar(
            graphql_df,
            x="GraphQL (BFF)",
            y="95% Line",
            color="95% Line",
            color_continuous_scale="oranges"
        )

        st.plotly_chart(fig,use_container_width=True)

    st.divider()

    st.subheader("Frontend Performance Scores")

    col1,col2,col3,col4 = st.columns(4)

    for i,row in ui_df.iterrows():

        if row["Pages"]=="Homepage":
            with col1:
                st.plotly_chart(create_gauge("Homepage Score",row["Performance Score"]),use_container_width=True)

        if row["Pages"]=="CG":
            with col2:
                st.plotly_chart(create_gauge("CG Score",row["Performance Score"]),use_container_width=True)

        if row["Pages"]=="PG":
            with col3:
                st.plotly_chart(create_gauge("PG Score",row["Performance Score"]),use_container_width=True)

        if row["Pages"]=="PDP":
            with col4:
                st.plotly_chart(create_gauge("PDP Score",row["Performance Score"]),use_container_width=True)

    st.subheader("SEO Scores")

    col1,col2,col3,col4 = st.columns(4)

    for i,row in ui_df.iterrows():

        if row["Pages"]=="Homepage":
            with col1:
                st.plotly_chart(create_gauge("Homepage SEO",row["SEO Score"]),use_container_width=True)

        if row["Pages"]=="CG":
            with col2:
                st.plotly_chart(create_gauge("CG SEO",row["SEO Score"]),use_container_width=True)

        if row["Pages"]=="PG":
            with col3:
                st.plotly_chart(create_gauge("PG SEO",row["SEO Score"]),use_container_width=True)

        if row["Pages"]=="PDP":
            with col4:
                st.plotly_chart(create_gauge("PDP SEO",row["SEO Score"]),use_container_width=True)

# -----------------------------------------------------
# API PAGE
# -----------------------------------------------------

if page == "API Performance":

    st.header("API Performance")

    tab1,tab2 = st.tabs(["Charts","Data"])

    with tab1:

        col1,col2 = st.columns(2)

        with col1:

            fig = px.bar(
                api_df,
                x="APIs",
                y=["Average","95% Line","99% Line"],
                barmode="group"
            )

            st.plotly_chart(fig,use_container_width=True)

        with col2:

            fig = px.pie(
                api_df,
                names="APIs",
                values="TPS"
            )

            st.plotly_chart(fig,use_container_width=True)

        fig = px.scatter(
            api_df,
            x="Average",
            y="95% Line",
            size="TPS",
            color="APIs"
        )

        st.plotly_chart(fig,use_container_width=True)

    with tab2:

        st.dataframe(api_df,use_container_width=True)

# -----------------------------------------------------
# GRAPHQL PAGE
# -----------------------------------------------------

if page == "GraphQL Performance":

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

        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True))
        )

        st.plotly_chart(fig,use_container_width=True)

        fig2 = px.bar(
            graphql_df,
            x="GraphQL (BFF)",
            y="95% Line",
            color="95% Line"
        )

        st.plotly_chart(fig2,use_container_width=True)

    with tab2:

        st.dataframe(graphql_df,use_container_width=True)

# -----------------------------------------------------
# FRONTEND PAGE
# -----------------------------------------------------

if page == "Frontend Metrics":

    st.header("Frontend Metrics")

    tab1,tab2 = st.tabs(["Charts","Data"])

    with tab1:

        st.subheader("Performance Score Gauges")

        col1,col2,col3,col4 = st.columns(4)

        for i,row in ui_df.iterrows():

            if i==0:
                with col1:
                    st.plotly_chart(create_gauge(row["Pages"],row["Performance Score"]),use_container_width=True)

            if i==1:
                with col2:
                    st.plotly_chart(create_gauge(row["Pages"],row["Performance Score"]),use_container_width=True)

            if i==2:
                with col3:
                    st.plotly_chart(create_gauge(row["Pages"],row["Performance Score"]),use_container_width=True)

            if i==3:
                with col4:
                    st.plotly_chart(create_gauge(row["Pages"],row["Performance Score"]),use_container_width=True)

        st.subheader("Core Web Vitals")

        fig = px.imshow(
            ui_df[["FCP","LCP","TBT","CLS"]],
            labels=dict(x="Metric",y="Page"),
            y=ui_df["Pages"],
            color_continuous_scale="RdYlGn_r"
        )

        st.plotly_chart(fig,use_container_width=True)

        st.subheader("Page Performance")

        fig2 = px.bar(
            ui_df,
            x="Pages",
            y="Performance Score",
            color="Performance Score"
        )

        st.plotly_chart(fig2,use_container_width=True)

    with tab2:

        st.dataframe(ui_df,use_container_width=True)
