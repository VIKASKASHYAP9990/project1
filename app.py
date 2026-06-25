import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
import os

# Set page configurations
st.set_page_config(layout="wide", page_title="Sales Analysis Dashboard")

# Inject custom premium CSS styling
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
    /* Global Styles */
    .stApp {
        background-color: #0B0F19;
    }
    
    body, [class*="css"], p, span, label, div, select, button, input {
        font-family: 'Inter', sans-serif !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        color: #F8FAFC !important;
        letter-spacing: -0.02em;
    }
    
    /* Title styling */
    .main-title {
        background: linear-gradient(135deg, #8B5CF6 0%, #6366F1 50%, #06B6D4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Outfit', sans-serif;
        font-size: 2.8rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    
    /* Subtext description */
    .sub-title {
        color: #94A3B8;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        font-weight: 400;
        line-height: 1.6;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0E1322 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    [data-testid="stSidebar"] .stMarkdown p {
        color: #94A3B8;
    }
    
    /* KPI Cards Styling */
    .kpi-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 20px;
        margin-bottom: 25px;
    }
    
    .kpi-card {
        background: rgba(17, 24, 39, 0.55);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 16px;
        padding: 22px;
        display: flex;
        align-items: center;
        gap: 18px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
        transition: transform 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-4px);
        border-color: rgba(99, 102, 241, 0.4);
        box-shadow: 0 8px 30px rgba(99, 102, 241, 0.15);
    }
    
    .kpi-icon-box {
        width: 52px;
        height: 52px;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        flex-shrink: 0;
    }
    
    .kpi-content {
        display: flex;
        flex-direction: column;
    }
    
    .kpi-title {
        font-size: 0.8rem;
        font-weight: 600;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 4px;
    }
    
    .kpi-value {
        font-size: 1.65rem;
        font-weight: 700;
        color: #F8FAFC;
        font-family: 'Outfit', sans-serif;
        line-height: 1.25;
    }
    
    .kpi-delta {
        font-size: 0.82rem;
        font-weight: 600;
        margin-top: 5px;
        display: inline-flex;
        align-items: center;
        gap: 4px;
    }
    
    .delta-positive {
        color: #10B981;
    }
    
    .delta-negative {
        color: #EF4444;
    }
    
    .delta-neutral {
        color: #94A3B8;
    }
    
    /* Layout card wrappers */
    .chart-card {
        background: rgba(17, 24, 39, 0.45);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }
    
    /* DataFrame formatting */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
    }
    
    /* Styled Table Card */
    .table-card {
        background: rgba(15, 23, 42, 0.7);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(99, 102, 241, 0.15);
        border-radius: 20px;
        padding: 28px;
        margin-top: 12px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25), inset 0 1px 0 rgba(255,255,255,0.04);
    }
    
    .table-header-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 20px;
        flex-wrap: wrap;
        gap: 12px;
    }
    
    .table-title {
        font-family: 'Outfit', sans-serif;
        font-size: 1.3rem;
        font-weight: 700;
        color: #F8FAFC;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .table-title-icon {
        width: 36px;
        height: 36px;
        background: rgba(99, 102, 241, 0.15);
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
    }

    .table-meta {
        display: flex;
        gap: 16px;
        flex-wrap: wrap;
    }
    
    .table-badge {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 8px;
        padding: 5px 12px;
        font-size: 0.78rem;
        font-weight: 600;
        color: #94A3B8;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    
    .table-badge span {
        color: #F8FAFC;
        font-weight: 700;
    }

    /* Update Button */
    .stButton > button[data-testid="update-btn"],
    div[data-testid="stButton"] > button {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 8px 22px !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        letter-spacing: 0.02em !important;
        box-shadow: 0 4px 14px rgba(16, 185, 129, 0.25) !important;
        transition: all 0.25s ease !important;
        display: flex !important;
        align-items: center !important;
        gap: 6px !important;
    }
    div[data-testid="stButton"] > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4) !important;
    }
    
    /* Buttons Customization */
    .stDownloadButton button {
        background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.2) !important;
        transition: all 0.3s ease !important;
    }
    .stDownloadButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.3) !important;
        border: none !important;
    }
    
    /* Date pickers and other sidebar widgets */
    div[data-baseweb="select"] > div {
        background-color: #1E293B !important;
        border-color: rgba(255, 255, 255, 0.08) !important;
        border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)

# Main Title and Description
st.markdown('<div class="main-title">Sales Data Analysis Dashboard</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Upload a sales CSV/XLSX (default: <code>superstore.csv</code>) with columns: '
    '<strong>Order ID, Product, Category, Sales, Profit, Date, Region</strong>. Use the sidebar filters to explore KPIs and charts.</div>',
    unsafe_allow_html=True
)

# Helper function to generate default CSV if not exists
if not os.path.exists("superstore.csv"):
    try:
        from generate_data import create_mock_superstore
        create_mock_superstore()
        st.toast("Generated mock superstore dataset automatically!", icon="📊")
    except Exception as e:
        pass

@st.cache_data
def load_data_from_path(path):
    try:
        if str(path).lower().endswith((".xls", ".xlsx")):
            df = pd.read_excel(path, engine="openpyxl")
        else:
            df = pd.read_csv(path, low_memory=False)
    except Exception:
        df = pd.read_csv(path, low_memory=False)
    df.columns = [c.strip() for c in df.columns]
    return df

def standardize_and_clean(df):
    cols = {c: c.strip() for c in df.columns}
    date_candidates = [c for c in df.columns if "date" in c.lower()]
    if date_candidates:
        date_col = date_candidates[0]
    else:
        raise ValueError("No date column found. Ensure CSV has a Date or Order Date column.")
        
    rename_map = {}
    for c in df.columns:
        lc = c.lower()
        if lc in ("order id", "order_id", "orderid"):
            rename_map[c] = "Order ID"
        elif "product" in lc:
            rename_map[c] = "Product"
        elif lc in ("category", "cat"):
            rename_map[c] = "Category"
        elif "sub" in lc and "cat" in lc:
            rename_map[c] = "Sub-Category"
        elif lc in ("region",):
            rename_map[c] = "Region"
        elif lc in ("state", "province"):
            rename_map[c] = "State"
        elif lc in ("profit",):
            rename_map[c] = "Profit"
        elif lc in ("sales", "sale"):
            rename_map[c] = "Sales"
        elif "customer" in lc:
            rename_map[c] = "Customer ID"
            
    df = df.rename(columns=rename_map)
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df = df.rename(columns={date_col: "Order Date"})
    
    for col in ["Sales", "Profit"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        else:
            df[col] = np.nan
            
    df = df.dropna(subset=["Order Date", "Sales"])
    
    if "Order ID" in df.columns:
        df = df.drop_duplicates(subset=["Order ID", "Product"], keep="first")
        
    df["Year"] = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.to_period("M").dt.to_timestamp()
    df["MonthStart"] = df["Month"]
    df["Quarter"] = df["Order Date"].dt.to_period("Q").astype(str)
    
    df["Profit"] = pd.to_numeric(df["Profit"], errors="coerce")
    df["Profit Margin"] = df["Profit"] / df["Sales"]
    
    if "Region" not in df.columns and "State" in df.columns:
        df["Region"] = df["State"]
        
    for c in df.select_dtypes(include="object").columns:
        df[c] = df[c].str.strip()
    return df

# Load default file or uploaded file
df = None
try:
    df = load_data_from_path("superstore.csv")
    df = standardize_and_clean(df)
except Exception:
    uploaded = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx", "xls"])
    if uploaded is not None:
        df = load_data_from_path(uploaded)
        df = standardize_and_clean(df)
    else:
        st.warning("No dataset loaded. Upload a CSV/XLSX or place 'superstore.csv' in the app folder.")
        st.stop()

# Sidebar filters
st.sidebar.header("Filters")
min_date = df["Order Date"].min().date()
max_date = df["Order Date"].max().date()
date_range = st.sidebar.date_input("Date range", [min_date, max_date], min_value=min_date, max_value=max_date)

regions = sorted(df["Region"].dropna().unique().tolist())
selected_regions = st.sidebar.multiselect("Region", options=regions, default=regions)

categories = sorted(df["Category"].dropna().unique().tolist())
selected_categories = st.sidebar.multiselect("Category", options=categories, default=categories)

product_search = st.sidebar.text_input("Product search (contains)")

@st.cache_data
def apply_filters(df, start_date, end_date, regions, categories, product_search):
    d = df.copy()
    d = d[(d["Order Date"] >= pd.to_datetime(start_date)) & (d["Order Date"] <= pd.to_datetime(end_date))]
    if regions:
        d = d[d["Region"].isin(regions)]
    if categories:
        d = d[d["Category"].isin(categories)]
    if product_search and product_search.strip():
        d = d[d["Product"].str.contains(product_search, case=False, na=False)]
    return d

start_date, end_date = date_range[0], date_range[1]
filtered = apply_filters(df, start_date, end_date, selected_regions, selected_categories, product_search)

# Key metrics
total_sales = filtered["Sales"].sum()
total_profit = filtered["Profit"].sum()
avg_margin = filtered["Profit Margin"].mean()
total_orders = filtered["Order ID"].nunique() if "Order ID" in filtered.columns else len(filtered)
avg_order_value = total_sales / total_orders if total_orders > 0 else 0

# MoM and YoY
monthly = filtered.groupby("Month").agg(Sales=("Sales", "sum")).reset_index().sort_values("Month")
if len(monthly) >= 2:
    mom_growth = (monthly["Sales"].iloc[-1] - monthly["Sales"].iloc[-2]) / monthly["Sales"].iloc[-2] if monthly["Sales"].iloc[-2] != 0 else np.nan
else:
    mom_growth = np.nan
yearly = filtered.groupby("Year").agg(Sales=("Sales", "sum")).reset_index().sort_values("Year")
if len(yearly) >= 2:
    yoy_growth = (yearly["Sales"].iloc[-1] - yearly["Sales"].iloc[-2]) / yearly["Sales"].iloc[-2] if yearly["Sales"].iloc[-2] != 0 else np.nan
else:
    yoy_growth = np.nan

# Custom Plotly Theme Wrapper
def apply_plotly_theme(fig, title=""):
    fig.update_layout(
        title={
            'text': title,
            'font': {'family': 'Outfit', 'size': 18, 'color': '#F8FAFC'},
            'y': 0.95,
            'x': 0.05,
            'xanchor': 'left',
            'yanchor': 'top'
        },
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'family': 'Inter', 'color': '#94A3B8'},
        margin=dict(l=40, r=20, t=65, b=40),
        xaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.04)',
            linecolor='rgba(255, 255, 255, 0.06)',
            tickfont=dict(color='#94A3B8'),
            title=dict(font=dict(color='#94A3B8')),
            zeroline=False
        ),
        yaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.04)',
            linecolor='rgba(255, 255, 255, 0.06)',
            tickfont=dict(color='#94A3B8'),
            title=dict(font=dict(color='#94A3B8')),
            zeroline=False
        ),
        legend=dict(
            bgcolor='rgba(15, 23, 42, 0.6)',
            bordercolor='rgba(255, 255, 255, 0.06)',
            borderwidth=1,
            font=dict(color='#94A3B8')
        ),
        hoverlabel=dict(
            bgcolor='#1E293B',
            font_size=13,
            font_family='Inter',
            font_color='#F8FAFC',
            bordercolor='rgba(255, 255, 255, 0.1)'
        )
    )
    return fig

# KPI cards creation
def make_kpi_card(title, value, delta_val=None, delta_type="neutral", icon_svg=""):
    delta_class = f"delta-{delta_type}"
    delta_symbol = "▲" if delta_type == "positive" else ("▼" if delta_type == "negative" else "")
    delta_html = f'<span class="kpi-delta {delta_class}">{delta_symbol} {delta_val}</span>' if delta_val else ''
    
    icon_bg_map = {
        "sales": "rgba(99, 102, 241, 0.15)",
        "profit": "rgba(16, 185, 129, 0.15)",
        "margin": "rgba(245, 158, 11, 0.15)",
        "growth": "rgba(6, 182, 212, 0.15)"
    }
    icon_color_map = {
        "sales": "#6366F1",
        "profit": "#10B981",
        "margin": "#F59E0B",
        "growth": "#06B6D4"
    }
    
    bg_color = icon_bg_map.get(icon_svg, "rgba(255, 255, 255, 0.05)")
    icon_color = icon_color_map.get(icon_svg, "#F3F4F6")
    
    svgs = {
        "sales": '<svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><line x1="12" y1="1" x2="12" y2="23"></line><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>',
        "profit": '<svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>',
        "margin": '<svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="10"></circle><line x1="14.5" y1="9.5" x2="9.5" y2="14.5"></line><circle cx="9.5" cy="9.5" r="1.5"></circle><circle cx="14.5" cy="14.5" r="1.5"></circle></svg>',
        "growth": '<svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline><polyline points="17 6 23 6 23 12"></polyline></svg>'
    }
    
    svg_icon = svgs.get(icon_svg, "")
    
    return f"""
    <div class="kpi-card">
        <div class="kpi-icon-box" style="background: {bg_color}; color: {icon_color};">
            {svg_icon}
        </div>
        <div class="kpi-content">
            <span class="kpi-title">{title}</span>
            <span class="kpi-value">{value}</span>
            {delta_html}
        </div>
    </div>
    """

# Render KPI cards
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(make_kpi_card("Total Sales", f"${total_sales:,.2f}", icon_svg="sales"), unsafe_allow_html=True)
with col2:
    st.markdown(make_kpi_card("Total Profit", f"${total_profit:,.2f}", icon_svg="profit"), unsafe_allow_html=True)
with col3:
    st.markdown(make_kpi_card("Avg Profit Margin", f"{avg_margin:.2%}" if not np.isnan(avg_margin) else "N/A", icon_svg="margin"), unsafe_allow_html=True)
with col4:
    g_type = "positive" if not np.isnan(mom_growth) and mom_growth >= 0 else ("negative" if not np.isnan(mom_growth) else "neutral")
    yoy_text = f"{yoy_growth:+.1%} YoY" if not np.isnan(yoy_growth) else None
    yoy_type = "positive" if not np.isnan(yoy_growth) and yoy_growth >= 0 else ("negative" if not np.isnan(yoy_growth) else "neutral")
    st.markdown(make_kpi_card("MoM Sales Growth", f"{mom_growth:+.2%}" if not np.isnan(mom_growth) else "N/A", delta_val=yoy_text, delta_type=yoy_type, icon_svg="growth"), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Time series chart
monthly_filtered = filtered.groupby("Month").agg(Sales=("Sales", "sum"), Profit=("Profit", "sum")).reset_index().sort_values("Month")
monthly_filtered["Sales_MA3"] = monthly_filtered["Sales"].rolling(3).mean()

fig_ts = go.Figure()
fig_ts.add_trace(go.Scatter(
    x=monthly_filtered["Month"], y=monthly_filtered["Sales"], 
    mode="lines+markers", name="Sales", 
    line=dict(shape='spline', width=3, color='#6366F1'),
    marker=dict(size=6)
))
fig_ts.add_trace(go.Scatter(
    x=monthly_filtered["Month"], y=monthly_filtered["Profit"], 
    mode="lines+markers", name="Profit", 
    line=dict(shape='spline', width=3, color='#10B981'),
    marker=dict(size=6)
))
fig_ts.add_trace(go.Scatter(
    x=monthly_filtered["Month"], y=monthly_filtered["Sales_MA3"], 
    mode="lines", name="Sales MA (3)", 
    line=dict(dash="dash", width=2, color='#F59E0B')
))
fig_ts.update_layout(hovermode="x unified")
apply_plotly_theme(fig_ts, "Monthly Sales and Profit Trends")

# Top products
if "Product" in filtered.columns:
    prod_agg = filtered.groupby("Product").agg(
        Sales=("Sales", "sum"), 
        Profit=("Profit", "sum"), 
        Orders=("Order ID", "nunique") if "Order ID" in filtered.columns else ("Sales", "count")
    ).reset_index()
    prod_agg = prod_agg.sort_values("Sales", ascending=False).head(10)
    
    fig_prod = px.bar(
        prod_agg, x="Sales", y="Product", orientation="h", text="Sales",
        color="Sales", color_continuous_scale="purples",
        hover_data=["Profit", "Orders"]
    )
    fig_prod.update_layout(yaxis={"categoryorder":"total ascending"}, coloraxis_showscale=False)
    apply_plotly_theme(fig_prod, "Top 10 Products by Sales")
    fig_prod.update_traces(texttemplate='$%{text:,.2s}', textposition='outside')
else:
    fig_prod = go.Figure()
    apply_plotly_theme(fig_prod, "No Product Column Available")

# Category chart
if "Sub-Category" in filtered.columns:
    fig_cat = px.treemap(
        filtered, path=["Category", "Sub-Category"], values="Sales",
        color="Sales", color_continuous_scale="blues"
    )
    apply_plotly_theme(fig_cat, "Sales by Category and Sub-Category Breakdown")
else:
    cat_agg = filtered.groupby("Category").agg(Sales=("Sales", "sum")).reset_index()
    fig_cat = px.pie(
        cat_agg, names="Category", values="Sales",
        color_discrete_sequence=['#6366F1', '#10B981', '#F59E0B']
    )
    apply_plotly_theme(fig_cat, "Sales by Category Share")

# Region chart
region_col = "Region" if "Region" in filtered.columns else ("State" if "State" in filtered.columns else None)
if region_col:
    region_agg = filtered.groupby(region_col).agg(Sales=("Sales", "sum")).reset_index().sort_values("Sales", ascending=False)
    fig_region = px.bar(
        region_agg, x="Sales", y=region_col, orientation="h",
        color="Sales", color_continuous_scale="teal"
    )
    fig_region.update_layout(coloraxis_showscale=False, yaxis={"categoryorder":"total ascending"})
    apply_plotly_theme(fig_region, f"Sales by {region_col}")
    fig_region.update_traces(texttemplate='$%{x:,.2s}', textposition='outside')
else:
    fig_region = go.Figure()
    apply_plotly_theme(fig_region, "No Region/State Column Available")

# Profit margin heatmap
if "Category" in filtered.columns and region_col:
    heat = filtered.groupby(["Category", region_col]).agg(ProfitMargin=("Profit Margin", "mean")).reset_index()
    heat_pivot = heat.pivot(index="Category", columns=region_col, values="ProfitMargin").fillna(0)
    
    # Custom elegant RdYlGn color map suited for dark theme
    custom_rdylgn = [
        [0.0, '#EF4444'],   # Rose
        [0.5, '#F59E0B'],   # Amber
        [1.0, '#10B981']    # Emerald
    ]
    fig_heat = px.imshow(
        heat_pivot, text_auto=".2f", aspect="auto", 
        color_continuous_scale=custom_rdylgn
    )
    apply_plotly_theme(fig_heat, "Average Profit Margin by Category and Region Matrix")
else:
    fig_heat = go.Figure()
    apply_plotly_theme(fig_heat, "Profit Margin Heatmap Not Available for This Dataset")

# Page Layout structure
left, right = st.columns((2, 1))

with left:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig_ts, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig_prod, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig_region, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig_cat, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Full width heatmap card
st.markdown('<div class="chart-card">', unsafe_allow_html=True)
st.plotly_chart(fig_heat, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Data table and download section
st.markdown("""
<div class="table-card">
    <div class="table-header-row">
        <div class="table-title">
            <div class="table-title-icon">&#128202;</div>
            Filtered Data Details
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Table metadata badges
badge_col1, badge_col2, badge_col3, badge_col4 = st.columns([1, 1, 1, 2])
with badge_col1:
    st.markdown(f"""
    <div class="table-badge">&#128196; Rows <span>{len(filtered):,}</span></div>
    """, unsafe_allow_html=True)
with badge_col2:
    st.markdown(f"""
    <div class="table-badge">&#128290; Columns <span>{len(filtered.columns)}</span></div>
    """, unsafe_allow_html=True)
with badge_col3:
    st.markdown(f"""
    <div class="table-badge">&#127758; Regions <span>{filtered['Region'].nunique() if 'Region' in filtered.columns else 'N/A'}</span></div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Update / Refresh button + Download button side by side
btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 4])
with btn_col1:
    if st.button("&#x21BB; Update", help="Clear cache and refresh all data and charts"):
        st.cache_data.clear()
        st.rerun()
with btn_col2:
    def to_csv_bytes(df):
        return df.to_csv(index=False).encode("utf-8")
    csv_bytes = to_csv_bytes(filtered)
    st.download_button(
        "&#x2B07; Download CSV",
        data=csv_bytes,
        file_name="filtered_sales.csv",
        mime="text/csv"
    )

st.markdown("<br>", unsafe_allow_html=True)

# Styled dataframe inside a background card
st.markdown('<div style="background: rgba(15,23,42,0.6); border: 1px solid rgba(99,102,241,0.12); border-radius: 16px; padding: 16px;">', unsafe_allow_html=True)
st.dataframe(
    filtered.reset_index(drop=True),
    use_container_width=True,
    height=420
)
st.markdown('</div>', unsafe_allow_html=True)
