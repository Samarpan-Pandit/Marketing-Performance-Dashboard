#-----------------------------
# Import Libraries
#-----------------------------
import streamlit as st
import pandas as pd
import plotly.express as px
# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Marketing Performance Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.block-container{
    padding-top:2rem;
    padding-bottom:2rem;
}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# -----------------------------
# Dashboard Title
# -----------------------------
st.title("📊 Marketing Performance Dashboard")

st.markdown("""
Analyze marketing campaign performance, customer engagement,
marketing channels, ROI, and conversions through an interactive dashboard.
""")

st.divider()

# -----------------------------
# Load Dataset
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_marketing_data.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_data()

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("🔍 Dashboard Filters")

campaign_filter = st.sidebar.multiselect(
    "Campaign Type",
    options=sorted(df["Campaign_Type"].unique()),
    default=sorted(df["Campaign_Type"].unique())
)

channel_filter = st.sidebar.multiselect(
    "Marketing Channel",
    options=sorted(df["Channel_Used"].unique()),
    default=sorted(df["Channel_Used"].unique())
)

customer_filter = st.sidebar.multiselect(
    "Customer Segment",
    options=sorted(df["Customer_Segment"].unique()),
    default=sorted(df["Customer_Segment"].unique())
)

language_filter = st.sidebar.multiselect(
    "Language",
    options=sorted(df["Language"].unique()),
    default=sorted(df["Language"].unique())
)

# -----------------------------
# Apply Filters
# -----------------------------
filtered_df = df[
    (df["Campaign_Type"].isin(campaign_filter)) &
    (df["Channel_Used"].isin(channel_filter)) &
    (df["Customer_Segment"].isin(customer_filter)) &
    (df["Language"].isin(language_filter))
]
# ============================================================
# KPI CALCULATIONS
# ============================================================

total_revenue = filtered_df["Revenue"].sum()

total_cost = filtered_df["Acquisition_Cost"].sum()

total_campaigns = filtered_df["Campaign_ID"].nunique()

total_impressions = filtered_df["Impressions"].sum()

total_clicks = filtered_df["Clicks"].sum()

total_leads = filtered_df["Leads"].sum()

total_conversions = filtered_df["Conversions"].sum()

average_roi = filtered_df["ROI"].mean()

average_ctr = filtered_df["CTR"].mean()

average_conversion_rate = filtered_df["Conversion_Rate"].mean()

average_engagement = filtered_df["Engagement_Score"].mean()

# ============================================================
# KPI DASHBOARD
# ============================================================

st.subheader("📈 Marketing KPIs")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "💰 Total Revenue",
        f"₹ {total_revenue:,.0f}"
    )

with col2:
    st.metric(
        "💸 Total Cost",
        f"₹ {total_cost:,.2f}"
    )

with col3:
    st.metric(
        "📢 Campaigns",
        total_campaigns
    )

with col4:
    st.metric(
        "👀 Impressions",
        f"{total_impressions:,}"
    )

st.markdown("---")

col5, col6, col7, col8 = st.columns(4)

with col5:
    st.metric(
        "🖱️ Clicks",
        f"{total_clicks:,}"
    )

with col6:
    st.metric(
        "🎯 Leads",
        f"{total_leads:,}"
    )

with col7:
    st.metric(
        "✅ Conversions",
        f"{total_conversions:,}"
    )

with col8:
    st.metric(
        "📊 Average ROI",
        f"{average_roi:.2f}%"
    )

st.markdown("---")

col9, col10, col11 = st.columns(3)

with col9:
    st.metric(
        "📈 Average CTR",
        f"{average_ctr:.2f}%"
    )

with col10:
    st.metric(
        "🔄 Conversion Rate",
        f"{average_conversion_rate:.2f}%"
    )

with col11:
    st.metric(
        "❤️ Engagement Score",
        f"{average_engagement:.2f}"
    )

# ============================================================
# FILTERED DATASET
# ============================================================

st.markdown("---")

with st.expander("📄 View Filtered Dataset"):

    st.dataframe(filtered_df)

    st.write(f"Rows : {filtered_df.shape[0]}")

    st.write(f"Columns : {filtered_df.shape[1]}")

# ============================================================
# CAMPAIGN PERFORMANCE ANALYSIS
# ============================================================

st.markdown("---")
st.header("📢 Campaign Performance")

campaign_summary = (
    filtered_df
    .groupby("Campaign_Type")
    .agg({
        "Revenue": "sum",
        "ROI": "mean",
        "Conversions": "sum",
        "Engagement_Score": "mean"
    })
    .reset_index()
)
#Revenue Chart:
fig1 = px.bar(
    campaign_summary,
    x="Campaign_Type",
    y="Revenue",
    color="Campaign_Type",
    text_auto=True,
    title="Revenue by Campaign Type"
)
fig1.update_layout(
    xaxis_title="Campaign Type",
    yaxis_title="Revenue",
    showlegend=False
)
st.plotly_chart(fig1, use_container_width=True)
#ROI Chart:
fig2 = px.bar(
    campaign_summary,
    x="Campaign_Type",
    y="ROI",
    color="Campaign_Type",
    text_auto=".2f",
    title="Average ROI by Campaign Type"
)
fig2.update_layout(
    xaxis_title="Campaign Type",
    yaxis_title="Average ROI (%)",
    showlegend=False
)
st.plotly_chart(fig2, use_container_width=True)

col1, col2 = st.columns(2)
#Left Column: Conversions Chart:
with col1:
    fig3 = px.bar(
        campaign_summary,
        x="Campaign_Type",
        y="Conversions",
        color="Campaign_Type",
        text_auto=True,
        title="Conversions by Campaign Type"
    )
    fig3.update_layout(showlegend=False)
    st.plotly_chart(fig3, use_container_width=True)

#Right Column: Engagement Score Chart:
with col2:
    fig4 = px.bar(
        campaign_summary,
        x="Campaign_Type",
        y="Engagement_Score",
        color="Campaign_Type",
        text_auto=".2f",
        title="Average Engagement Score"
    )
    fig4.update_layout(showlegend=False)
    st.plotly_chart(fig4, use_container_width=True)

# ============================================================
# CHANNEL-WISE COMPARISON
# ============================================================

st.markdown("---")
st.header("📡 Channel-wise Comparison")

# Create a copy of the filtered data
channel_df = filtered_df.copy()

# Split multiple channels into separate rows
channel_df["Channel_Used"] = channel_df["Channel_Used"].str.split(",")

channel_df = channel_df.explode("Channel_Used")

# Remove extra spaces
channel_df["Channel_Used"] = channel_df["Channel_Used"].str.strip()

# Summarize data
channel_summary = (
    channel_df.groupby("Channel_Used")
    .agg({
        "Revenue": "sum",
        "Acquisition_Cost": "sum",
        "ROI": "mean",
        "CTR": "mean",
        "Conversion_Rate": "mean"
    })
    .reset_index()
)

#Revenue By Channel:
fig5 = px.bar(
    channel_summary,
    x="Channel_Used",
    y="Revenue",
    color="Channel_Used",
    text_auto=True,
    title="Revenue by Marketing Channel"
)
fig5.update_layout(
    xaxis_title="Marketing Channel",
    yaxis_title="Revenue",
    showlegend=False
)
st.plotly_chart(fig5, use_container_width=True)

#Cost By Channel:
fig6 = px.bar(
    channel_summary,
    x="Channel_Used",
    y="Acquisition_Cost",
    color="Channel_Used",
    text_auto=True,
    title="Acquisition Cost by Channel"
)
fig6.update_layout(
    xaxis_title="Marketing Channel",
    yaxis_title="Cost",
    showlegend=False
)
st.plotly_chart(fig6, use_container_width=True)

col3, col4 = st.columns(2)
#Left Side: ROI:
with col3:
    fig7 = px.bar(
        channel_summary,
        x="Channel_Used",
        y="ROI",
        color="Channel_Used",
        text_auto=".2f",
        title="Average ROI by Channel"
    )
    fig7.update_layout(showlegend=False)
    st.plotly_chart(fig7, use_container_width=True)

#Right Side: CTR:
with col4:
    fig8 = px.bar(
        channel_summary,
        x="Channel_Used",
        y="CTR",
        color="Channel_Used",
        text_auto=".2f",
        title="Average CTR by Channel"
    )
    fig8.update_layout(showlegend=False)
    st.plotly_chart(fig8, use_container_width=True)

#Conversion Rate By Channel:
fig9 = px.bar(
    channel_summary,
    x="Channel_Used",
    y="Conversion_Rate",
    color="Channel_Used",
    text_auto=".2f",
    title="Average Conversion Rate by Channel"
)
fig9.update_layout(
    xaxis_title="Marketing Channel",
    yaxis_title="Conversion Rate",
    showlegend=False
)
st.plotly_chart(fig9, use_container_width=True)

# ============================================================
# ENGAGEMENT TRENDS
# ============================================================

st.markdown("---")
st.header("📈 Engagement Trends")

# Create Monthly Summary
monthly_summary = (
    filtered_df
    .groupby(["Year", "Month_Number", "Month"])
    .agg({
        "Engagement_Score": "mean",
        "Revenue": "sum",
        "Conversions": "sum"
    })
    .reset_index()
    .sort_values(["Year", "Month_Number"])
)

# Create Month-Year label
monthly_summary["Month_Year"] = (
    monthly_summary["Month"] + " " +
    monthly_summary["Year"].astype(str)
)
#Engagement Score Trend:
fig10 = px.line(
    monthly_summary,
    x="Month_Year",
    y="Engagement_Score",
    markers=True,
    title="Monthly Engagement Score Trend"
)
fig10.update_layout(
    xaxis_title="Month",
    yaxis_title="Average Engagement Score"
)
st.plotly_chart(fig10, use_container_width=True)
#Revenue Trend:
fig11 = px.line(
    monthly_summary,
    x="Month_Year",
    y="Revenue",
    markers=True,
    title="Monthly Revenue Trend"
)
fig11.update_layout(
    xaxis_title="Month",
    yaxis_title="Revenue"
)
st.plotly_chart(fig11, use_container_width=True)

col5, col6 = st.columns(2)
#Left Side: Monthly Conversions:
with col5:
    fig12 = px.line(
        monthly_summary,
        x="Month_Year",
        y="Conversions",
        markers=True,
        title="Monthly Conversions"
    )
    fig12.update_layout(
        xaxis_title="Month",
        yaxis_title="Conversions"
    )
    st.plotly_chart(fig12, use_container_width=True)

#Right Side: Engagement By Month:
with col6:
    fig13 = px.bar(
        monthly_summary,
        x="Month_Year",
        y="Engagement_Score",
        color="Month_Year",
        text_auto=".2f",
        title="Average Engagement by Month"
    )
    fig13.update_layout(
        xaxis_title="Month",
        yaxis_title="Engagement Score",
        showlegend=False
    )
    st.plotly_chart(fig13, use_container_width=True)

# ============================================================
# SALES CONVERSION INSIGHTS
# ============================================================

st.markdown("---")
st.header("🎯 Sales Conversion Insights")
# Funnel Data
funnel_df = pd.DataFrame({
    "Stage": [
        "Impressions",
        "Clicks",
        "Leads",
        "Conversions"
    ],
    "Count": [
        filtered_df["Impressions"].sum(),
        filtered_df["Clicks"].sum(),
        filtered_df["Leads"].sum(),
        filtered_df["Conversions"].sum()
    ]
})
fig14 = px.funnel(
    funnel_df,
    x="Count",
    y="Stage",
    title="Marketing Conversion Funnel"
)
st.plotly_chart(fig14, use_container_width=True)

#Campaign Conversion Analysis:
campaign_conversion = (
    filtered_df
    .groupby("Campaign_Type")["Conversions"]
    .sum()
    .reset_index()
)
fig15 = px.bar(
    campaign_conversion,
    x="Campaign_Type",
    y="Conversions",
    color="Campaign_Type",
    text_auto=True,
    title="Conversions by Campaign Type"
)
fig15.update_layout(
    showlegend=False,
    xaxis_title="Campaign Type",
    yaxis_title="Conversions"
)
st.plotly_chart(fig15, use_container_width=True)

#Customer Segment Conversion Analysis:
segment_conversion = (
    filtered_df
    .groupby("Customer_Segment")["Conversions"]
    .sum()
    .reset_index()
)
fig16 = px.bar(
    segment_conversion,
    x="Customer_Segment",
    y="Conversions",
    color="Customer_Segment",
    text_auto=True,
    title="Conversions by Customer Segment"
)
fig16.update_layout(
    showlegend=False,
    xaxis_title="Customer Segment",
    yaxis_title="Conversions"
)
st.plotly_chart(fig16, use_container_width=True)

#Conversion Distribution:
fig17 = px.pie(
    campaign_conversion,
    names="Campaign_Type",
    values="Conversions",
    title="Conversion Distribution by Campaign Type",
    hole=0.45
)
st.plotly_chart(fig17, use_container_width=True)

# ============================================================
# CUSTOMER ANALYSIS
# ============================================================

st.markdown("---")
st.header("👥 Customer Analysis")

customer_summary = (
    filtered_df
    .groupby("Customer_Segment")
    .agg({
        "Revenue": "sum",
        "ROI": "mean",
        "Engagement_Score": "mean",
        "Conversions": "sum"
    })
    .reset_index()
)

#Revenue By Customer Segment:
fig18 = px.bar(
    customer_summary,
    x="Customer_Segment",
    y="Revenue",
    color="Customer_Segment",
    text_auto=True,
    title="Revenue by Customer Segment"
)
fig18.update_layout(
    xaxis_title="Customer Segment",
    yaxis_title="Revenue (₹)",
    showlegend=False
)
st.plotly_chart(fig18, use_container_width=True)

col7, col8 = st.columns(2)

#Left Side: Average ROI by Customer Segment:
with col7:
    fig19 = px.bar(
        customer_summary,
        x="Customer_Segment",
        y="ROI",
        color="Customer_Segment",
        text_auto=".2f",
        title="Average ROI by Customer Segment"
    )
    fig19.update_layout(
        showlegend=False,
        xaxis_title="Customer Segment",
        yaxis_title="Average ROI (%)"
    )
    st.plotly_chart(fig19, use_container_width=True)

#Right Side: Average Engagement Score by Customer Segment:
with col8:
    fig20 = px.bar(
        customer_summary,
        x="Customer_Segment",
        y="Engagement_Score",
        color="Customer_Segment",
        text_auto=".2f",
        title="Average Engagement Score by Customer Segment"
    )
    fig20.update_layout(
        showlegend=False,
        xaxis_title="Customer Segment",
        yaxis_title="Engagement Score"
    )
    st.plotly_chart(fig20, use_container_width=True)

#Customer Segment Distribution:
customer_distribution = (
    filtered_df["Customer_Segment"]
    .value_counts()
    .reset_index()
)
customer_distribution.columns = [
    "Customer_Segment",
    "Count"
]
fig21 = px.pie(
    customer_distribution,
    names="Customer_Segment",
    values="Count",
    hole=0.45,
    title="Customer Segment Distribution"
)
st.plotly_chart(fig21, use_container_width=True)

# ============================================================
# TARGET AUDIENCE & LANGUAGE ANALYSIS
# ============================================================

st.markdown("---")
st.header("🎯 Target Audience & 🌐 Language Analysis")

#Target Audience Summery:
target_summary = (
    filtered_df
    .groupby("Target_Audience")
    .agg({
        "Revenue": "sum",
        "ROI": "mean",
        "Conversions": "sum",
        "Engagement_Score": "mean"
    })
    .reset_index()
)

#Revenue by Target Audience:
fig22 = px.bar(
    target_summary,
    x="Target_Audience",
    y="Revenue",
    color="Target_Audience",
    text_auto=True,
    title="Revenue by Target Audience"
)
fig22.update_layout(
    showlegend=False,
    xaxis_title="Target Audience",
    yaxis_title="Revenue (₹)"
)
st.plotly_chart(fig22, use_container_width=True)

col9, col10 = st.columns(2)

#Left Side: Average ROI by Target Audience:
with col9:
    fig23 = px.bar(
        target_summary,
        x="Target_Audience",
        y="ROI",
        color="Target_Audience",
        text_auto=".2f",
        title="Average ROI by Target Audience"
    )
    fig23.update_layout(
        showlegend=False,
        xaxis_title="Target Audience",
        yaxis_title="Average ROI (%)"
    )
    st.plotly_chart(fig23, use_container_width=True)

#Right Side: Average Engagement Score by Target Audience:
with col10:
    fig24 = px.bar(
        target_summary,
        x="Target_Audience",
        y="Engagement_Score",
        color="Target_Audience",
        text_auto=".2f",
        title="Average Engagement Score by Target Audience"
    )
    fig24.update_layout(
        showlegend=False,
        xaxis_title="Target Audience",
        yaxis_title="Engagement Score"
    )
    st.plotly_chart(fig24, use_container_width=True)

#Conversions By Target Audience:
fig25 = px.bar(
    target_summary,
    x="Target_Audience",
    y="Conversions",
    color="Target_Audience",
    text_auto=True,
    title="Conversions by Target Audience"
)
fig25.update_layout(
    showlegend=False,
    xaxis_title="Target Audience",
    yaxis_title="Conversions"
)
st.plotly_chart(fig25, use_container_width=True)

#Language Summery:
language_summary = (
    filtered_df
    .groupby("Language")
    .agg({
        "Revenue": "sum",
        "ROI": "mean",
        "Engagement_Score": "mean",
        "Conversions": "sum"
    })
    .reset_index()
)

#Revenue By Language:
fig26 = px.bar(
    language_summary,
    x="Language",
    y="Revenue",
    color="Language",
    text_auto=True,
    title="Revenue by Language"
)
fig26.update_layout(
    showlegend=False,
    xaxis_title="Language",
    yaxis_title="Revenue (₹)"
)
st.plotly_chart(fig26, use_container_width=True)

col11, col12 = st.columns(2)

#Left Side: Average ROI by Language:
with col11:
    fig27 = px.bar(
        language_summary,
        x="Language",
        y="ROI",
        color="Language",
        text_auto=".2f",
        title="Average ROI by Language"
    )
    fig27.update_layout(
        showlegend=False,
        xaxis_title="Language",
        yaxis_title="Average ROI (%)"
    )
    st.plotly_chart(fig27, use_container_width=True)

#Right Side: Average Engagement Score by Language:
with col12:
    fig28 = px.bar(
        language_summary,
        x="Language",
        y="Engagement_Score",
        color="Language",
        text_auto=".2f",
        title="Average Engagement Score by Language"
    )
    fig28.update_layout(
        showlegend=False,
        xaxis_title="Language",
        yaxis_title="Engagement Score"
    )
    st.plotly_chart(fig28, use_container_width=True)

#Conversion Distribution By Language:
fig29 = px.pie(
    language_summary,
    names="Language",
    values="Conversions",
    hole=0.45,
    title="Conversion Distribution by Language"
)
st.plotly_chart(fig29, use_container_width=True)

# ============================================================
# DASHBOARD SUMMARY
# ============================================================

st.markdown("---")
st.header("📋 Dashboard Summary")
summary_col1, summary_col2, summary_col3 = st.columns(3)
with summary_col1:
    st.success(f"📢 Campaign Types: {filtered_df['Campaign_Type'].nunique()}")
with summary_col2:
    st.info(f"📡 Marketing Channels: {channel_df['Channel_Used'].nunique()}")
with summary_col3:
    st.warning(f"👥 Customer Segments: {filtered_df['Customer_Segment'].nunique()}")

#Dataset Information:
st.subheader("📊 Dataset Information")
info1, info2, info3 = st.columns(3)
with info1:
    st.metric("Rows", f"{len(filtered_df):,}")
with info2:
    st.metric("Columns", filtered_df.shape[1])
with info3:
    st.metric("Languages", filtered_df["Language"].nunique())


#Download Filtered Dataset:
st.markdown("---")
st.subheader("⬇ Download Filtered Dataset")
csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 Download Filtered Data (CSV)",
    data=csv,
    file_name="filtered_marketing_data.csv",
    mime="text/csv",
)

#Dashboard Information:
st.markdown("---")
st.subheader("ℹ Dashboard Information")
st.info(
    """
This dashboard provides insights into marketing campaign performance.

It includes:

• Marketing KPI Analysis

• Campaign Performance

• Channel-wise Comparison

• Engagement Trends

• Sales Conversion Insights

• Customer Analysis

• Target Audience Analysis

• Language Analysis

Built using:

• Streamlit

• Pandas

• Plotly
"""
)

#Professional Footer:
st.markdown("---")
st.markdown(
    """
<div style='text-align:center; padding:15px;'>

### 📈 Marketing Performance Dashboard

Developed using **Python • Streamlit • Plotly**

Data Analytics Capstone Project

© 2026

</div>
""",
unsafe_allow_html=True
)