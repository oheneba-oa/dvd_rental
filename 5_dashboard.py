"""
5_dashboard.py

Purpose:
This Streamlit dashboard presents the main business insights from the
DVD Rental analysis project in a visually polished and interactive format.

Run with:
streamlit run 5_dashboard.py
"""

import pandas as pd
import streamlit as st
import plotly.express as px


# ------------------------------------------------------------
# 1. Page setup
# ------------------------------------------------------------
st.set_page_config(
    page_title="DVD Rental Business Dashboard",
    page_icon="🎬",
    layout="wide"
)


# ------------------------------------------------------------
# 2. Custom CSS for dashboard design
# ------------------------------------------------------------
st.markdown(
    """
    <style>
    /* Main app background */
    .stApp {
        background-color: #F7F8FA;
    }

    [data-testid="stAppViewContainer"] {
        background-color: #F7F8FA;
    }

    /* Keep Streamlit top bar visible but slim */
    [data-testid="stHeader"] {
        background-color: #F7F8FA !important;
        height: 2.5rem !important;
    }

    [data-testid="stToolbar"] {
        background-color: transparent !important;
        padding: 0px 8px !important;
        box-shadow: none !important;
    }

    [data-testid="stToolbar"] * {
        color: #111827 !important;
        fill: #111827 !important;
        stroke: #111827 !important;
    }

    header button {
        color: #111827 !important;
    }

    header svg {
        fill: #111827 !important;
        stroke: #111827 !important;
    }

    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }

    .dashboard-title {
        font-size: 38px;
        font-weight: 800;
        color: #111827;
        margin-bottom: 0px;
    }

    .dashboard-subtitle {
        font-size: 17px;
        color: #4B5563;
        margin-bottom: 25px;
    }

    .section-header {
        font-size: 24px;
        font-weight: 800;
        color: #111827;
        margin-top: 24px;
        margin-bottom: 12px;
    }

    .insight-box {
        background-color: #FFFFFF;
        padding: 18px 20px;
        border-radius: 14px;
        border-left: 5px solid #2563EB;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.06);
        margin-bottom: 18px;
        color: #374151;
        font-size: 15px;
        line-height: 1.6;
    }

    .metric-card {
        background-color: #FFFFFF;
        padding: 22px;
        border-radius: 16px;
        box-shadow: 0px 2px 10px rgba(0,0,0,0.07);
        text-align: center;
        border: 1px solid #E5E7EB;
        min-height: 118px;
    }

    .metric-label {
        font-size: 14px;
        color: #6B7280;
        margin-bottom: 8px;
    }

    .metric-value {
        font-size: 26px;
        font-weight: 800;
        color: #111827;
        line-height: 1.2;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #111827;
    }

    [data-testid="stSidebar"] * {
        color: white;
    }

    div[role="radiogroup"] label {
        padding: 6px 0px;
        font-weight: 600;
    }

    /* Pretty table styling */
    .table-card {
        background-color: #FFFFFF;
        border-radius: 16px;
        padding: 18px;
        box-shadow: 0px 2px 10px rgba(0,0,0,0.07);
        border: 1px solid #E5E7EB;
        margin-bottom: 25px;
    }

    .table-title {
        font-size: 18px;
        font-weight: 800;
        color: #111827;
        margin-bottom: 12px;
    }

    .table-scroll {
        overflow-x: auto;
        max-height: 420px;
        overflow-y: auto;
        border-radius: 12px;
        border: 1px solid #E5E7EB;
    }

    table.pretty-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 14px;
        color: #111827;
        background-color: white;
    }

    table.pretty-table thead tr {
        background-color: #111827;
        color: #FFFFFF;
    }

    table.pretty-table th {
        padding: 12px 14px;
        text-align: left;
        font-weight: 700;
        border-bottom: 1px solid #E5E7EB;
        white-space: nowrap;
    }

    table.pretty-table td {
        padding: 11px 14px;
        border-bottom: 1px solid #E5E7EB;
        white-space: nowrap;
    }

    table.pretty-table tbody tr:nth-child(even) {
        background-color: #F9FAFB;
    }

    table.pretty-table tbody tr:hover {
        background-color: #EFF6FF;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ------------------------------------------------------------
# 3. Load analysis outputs
# ------------------------------------------------------------
@st.cache_data
def load_data():
    customer_segments = pd.read_csv("tables/customer_segments.csv")
    churn_risk = pd.read_csv("tables/churn_risk_customers.csv")
    revenue_by_category = pd.read_csv("tables/revenue_by_category.csv")
    store_performance = pd.read_csv("tables/store_performance_analysis.csv")
    slow_inventory = pd.read_csv("tables/slow_moving_inventory.csv")
    recommendations = pd.read_csv("tables/recommendation_candidates.csv")
    pricing = pd.read_csv("tables/pricing_insight.csv")

    return (
        customer_segments,
        churn_risk,
        revenue_by_category,
        store_performance,
        slow_inventory,
        recommendations,
        pricing
    )


(
    customer_segments,
    churn_risk,
    revenue_by_category,
    store_performance,
    slow_inventory,
    recommendations,
    pricing
) = load_data()


# ------------------------------------------------------------
# 4. Helper functions
# ------------------------------------------------------------
def format_money(value):
    """
    Formats numeric values as money.
    """
    return f"${value:,.2f}"


def metric_card(label, value):
    """
    Creates a custom KPI card.
    """
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def section_header(text):
    """
    Creates a styled section heading.
    """
    st.markdown(
        f'<div class="section-header">{text}</div>',
        unsafe_allow_html=True
    )


def insight_box(text):
    """
    Creates a styled insight box.
    """
    st.markdown(
        f'<div class="insight-box">{text}</div>',
        unsafe_allow_html=True
    )


def pretty_table(title, data, money_cols=None, number_cols=None, decimal_cols=None):
    """
    Displays a styled HTML table instead of the default Streamlit dataframe.
    """

    money_cols = money_cols or []
    number_cols = number_cols or []
    decimal_cols = decimal_cols or []

    display_df = data.copy()

    # Make column names easier to read
    display_df.columns = [
        col.replace("_", " ").title()
        for col in display_df.columns
    ]

    money_cols = [col.replace("_", " ").title() for col in money_cols]
    number_cols = [col.replace("_", " ").title() for col in number_cols]
    decimal_cols = [col.replace("_", " ").title() for col in decimal_cols]

    for col in display_df.columns:
        if col in money_cols:
            display_df[col] = display_df[col].apply(
                lambda x: f"${x:,.2f}" if pd.notnull(x) else "-"
            )
        elif col in number_cols:
            display_df[col] = display_df[col].apply(
                lambda x: f"{x:,.0f}" if pd.notnull(x) else "-"
            )
        elif col in decimal_cols:
            display_df[col] = display_df[col].apply(
                lambda x: f"{x:,.2f}" if pd.notnull(x) else "-"
            )

    html_table = display_df.to_html(
        index=False,
        classes="pretty-table",
        escape=False
    )

    st.markdown(
        f"""
        <div class="table-card">
            <div class="table-title">{title}</div>
            <div class="table-scroll">
                {html_table}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def plot_bar(data, x, y, title, orientation="v", color=None):
    """
    Creates a clean Plotly bar chart.
    If the color column is numeric, Plotly will show a vertical color scale.
    """

    chart_data = data.copy()

    fig = px.bar(
        chart_data,
        x=x,
        y=y,
        orientation=orientation,
        title=title,
        color=color,
        text_auto=".2s",
        template="plotly_white",
        color_continuous_scale="Plasma",
        color_discrete_sequence=[
            "#2563EB",
            "#F97316",
            "#10B981",
            "#8B5CF6",
            "#EF4444",
            "#14B8A6",
            "#F59E0B",
            "#6366F1"
        ],
        labels={
            "store_id": "Store ID",
            "total_revenue": "Total Revenue",
            "rentals_per_inventory_item": "Rentals per Inventory Item",
            "total_rentals": "Total Rentals",
            "customer_segment": "Customer Segment",
            "churn_risk": "Churn Risk",
            "category": "Category",
            "recommendation_priority": "Recommendation Priority"
        }
    )

    fig.update_layout(
        title_font_size=20,
        title_font_color="#111827",
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        font=dict(size=13, color="#111827"),
        margin=dict(l=35, r=35, t=65, b=45),
        height=430,
        xaxis=dict(
            title_font=dict(color="#111827", size=14),
            tickfont=dict(color="#111827", size=12),
            gridcolor="#E5E7EB",
            zerolinecolor="#9CA3AF"
        ),
        yaxis=dict(
            title_font=dict(color="#111827", size=14),
            tickfont=dict(color="#111827", size=12),
            gridcolor="#E5E7EB",
            zerolinecolor="#9CA3AF"
        ),
        coloraxis_colorbar=dict(
            title=dict(
                text=color.replace("_", " ").title() if color else "",
                font=dict(color="#111827", size=13)
            ),
            tickfont=dict(color="#111827", size=12),
            outlinecolor="#E5E7EB",
            outlinewidth=1
        ),
        legend=dict(
            font=dict(color="#111827"),
            bgcolor="rgba(255,255,255,0.95)",
            bordercolor="#E5E7EB",
            borderwidth=1
        )
    )

    fig.update_traces(
        marker_line_width=0,
        textposition="outside",
        textfont=dict(color="#111827")
    )

    return fig


# ------------------------------------------------------------
# 5. Sidebar navigation
# ------------------------------------------------------------
st.sidebar.markdown("## 🎬 DVD Rental")
st.sidebar.markdown("Business Analytics Dashboard")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    [
        "Executive Overview",
        "Customer Analytics",
        "Revenue Optimization",
        "Inventory and Operations",
        "Recommendation Insights"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("© OOA Inc.")


# ------------------------------------------------------------
# 6. Executive Overview
# ------------------------------------------------------------
if page == "Executive Overview":
    st.markdown(
        '<p class="dashboard-title">DVD Rental Business Dashboard</p>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<p class="dashboard-subtitle">Executive view of revenue, customers, stores, inventory and recommendation opportunities.</p>',
        unsafe_allow_html=True
    )

    total_revenue = revenue_by_category["total_revenue"].sum()
    total_rentals = revenue_by_category["total_rentals"].sum()
    total_customers = customer_segments["number_of_customers"].sum()
    best_category = revenue_by_category.sort_values(
        by="total_revenue",
        ascending=False
    ).iloc[0]["category"]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        metric_card("Total Revenue", format_money(total_revenue))
    with col2:
        metric_card("Total Rentals", f"{total_rentals:,.0f}")
    with col3:
        metric_card("Total Customers", f"{total_customers:,.0f}")
    with col4:
        metric_card("Top Category", best_category)

    st.markdown("<br>", unsafe_allow_html=True)

    insight_box(
        "The business generated balanced store-level revenue, while customer value and film category performance show clear opportunities for targeted promotions and better inventory decisions."
    )

    col1, col2 = st.columns([1.2, 1])

    with col1:
        section_header("Revenue by Film Category")
        fig = plot_bar(
            revenue_by_category.sort_values("total_revenue", ascending=True),
            x="total_revenue",
            y="category",
            title="Film Category Revenue Ranking",
            orientation="h"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        section_header("Store Revenue Comparison")
        fig = plot_bar(
            store_performance,
            x="store_id",
            y="total_revenue",
            title="Revenue by Store",
            color="store_id"
        )
        st.plotly_chart(fig, use_container_width=True)

    pretty_table(
        "Store Performance Table",
        store_performance,
        money_cols=["total_revenue", "revenue_per_inventory_item"],
        number_cols=[
            "store_id",
            "total_customers",
            "total_inventory_items",
            "total_rentals"
        ],
        decimal_cols=["rentals_per_inventory_item"]
    )


# ------------------------------------------------------------
# 7. Customer Analytics
# ------------------------------------------------------------
elif page == "Customer Analytics":
    st.markdown(
        '<p class="dashboard-title">Customer Analytics</p>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<p class="dashboard-subtitle">Customer value segmentation and churn risk summary.</p>',
        unsafe_allow_html=True
    )

    high_value = customer_segments.sort_values(
        "total_revenue",
        ascending=False
    ).iloc[0]

    low_value = customer_segments.sort_values(
        "total_revenue",
        ascending=True
    ).iloc[0]

    low_risk_customers = churn_risk.loc[
        churn_risk["churn_risk"] == "Low Risk",
        "number_of_customers"
    ].iloc[0]

    col1, col2, col3 = st.columns(3)

    with col1:
        metric_card("Highest Value Segment", high_value["customer_segment"])
    with col2:
        metric_card("High Segment Revenue", format_money(high_value["total_revenue"]))
    with col3:
        metric_card("Low-Risk Customers", f"{low_risk_customers:,.0f}")

    st.markdown("<br>", unsafe_allow_html=True)

    insight_box(
        f"The high-value customer segment generated {format_money(high_value['total_revenue'])}, while the low-value segment generated {format_money(low_value['total_revenue'])}. This shows that customer value is not evenly distributed."
    )

    col1, col2 = st.columns(2)

    with col1:
        section_header("Revenue by Customer Segment")
        fig = plot_bar(
            customer_segments,
            x="customer_segment",
            y="total_revenue",
            title="Customer Segment Revenue",
            color="customer_segment"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        section_header("Churn Risk Distribution")
        fig = plot_bar(
            churn_risk,
            x="churn_risk",
            y="number_of_customers",
            title="Customers by Churn Risk",
            color="churn_risk"
        )
        st.plotly_chart(fig, use_container_width=True)

    pretty_table(
        "Customer Segment Summary",
        customer_segments,
        money_cols=["total_revenue", "average_revenue", "average_payment"],
        number_cols=["number_of_customers"]
    )

    pretty_table(
        "Churn Risk Summary",
        churn_risk,
        money_cols=["average_revenue", "total_revenue"],
        number_cols=["number_of_customers"]
    )


# ------------------------------------------------------------
# 8. Revenue Optimization
# ------------------------------------------------------------
elif page == "Revenue Optimization":
    st.markdown(
        '<p class="dashboard-title">Revenue Optimization</p>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<p class="dashboard-subtitle">Category revenue, rental activity and pricing-related insights.</p>',
        unsafe_allow_html=True
    )

    top_category = revenue_by_category.iloc[0]
    weakest_category = revenue_by_category.iloc[-1]

    col1, col2, col3 = st.columns(3)

    with col1:
        metric_card("Top Category", top_category["category"])
    with col2:
        metric_card("Top Category Revenue", format_money(top_category["total_revenue"]))
    with col3:
        metric_card("Weakest Category", weakest_category["category"])

    st.markdown("<br>", unsafe_allow_html=True)

    insight_box(
        f"{top_category['category']} is the strongest category with {format_money(top_category['total_revenue'])} from {top_category['total_rentals']:,.0f} rentals. {weakest_category['category']} is the weakest category by revenue."
    )

    col1, col2 = st.columns(2)

    with col1:
        section_header("Top Revenue Categories")
        top_categories = revenue_by_category.head(8).sort_values(
            "total_revenue",
            ascending=True
        )

        fig = plot_bar(
            top_categories,
            x="total_revenue",
            y="category",
            title="Top 8 Revenue Categories",
            orientation="h"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        section_header("Lowest Revenue Categories")
        low_categories = revenue_by_category.tail(8).sort_values(
            "total_revenue",
            ascending=True
        )

        fig = plot_bar(
            low_categories,
            x="total_revenue",
            y="category",
            title="Lowest 8 Revenue Categories",
            orientation="h"
        )
        st.plotly_chart(fig, use_container_width=True)

    section_header("Rental Volume by Category")
    fig = plot_bar(
        revenue_by_category.sort_values("total_rentals", ascending=True),
        x="total_rentals",
        y="category",
        title="Total Rentals by Category",
        orientation="h"
    )
    st.plotly_chart(fig, use_container_width=True)

    pretty_table(
        "Pricing Insight Table",
        pricing.sort_values(by="total_revenue", ascending=False).head(25),
        money_cols=["rental_rate", "total_revenue", "revenue_per_rental"],
        number_cols=["total_rentals"]
    )


# ------------------------------------------------------------
# 9. Inventory and Operations
# ------------------------------------------------------------
elif page == "Inventory and Operations":
    st.markdown(
        '<p class="dashboard-title">Inventory and Operations</p>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<p class="dashboard-subtitle">Store comparison and slow-moving inventory analysis.</p>',
        unsafe_allow_html=True
    )

    best_store = store_performance.sort_values(
        "total_revenue",
        ascending=False
    ).iloc[0]

    efficient_store = store_performance.sort_values(
        "rentals_per_inventory_item",
        ascending=False
    ).iloc[0]

    col1, col2, col3 = st.columns(3)

    with col1:
        metric_card("Best Store by Revenue", f"Store {int(best_store['store_id'])}")
    with col2:
        metric_card("Best Store Revenue", format_money(best_store["total_revenue"]))
    with col3:
        metric_card("Most Efficient Store", f"Store {int(efficient_store['store_id'])}")

    st.markdown("<br>", unsafe_allow_html=True)

    insight_box(
        f"Store {int(best_store['store_id'])} generated the highest revenue, while Store {int(efficient_store['store_id'])} had the highest rentals per inventory item."
    )

    col1, col2 = st.columns(2)

    with col1:
        section_header("Store Revenue")
        fig = plot_bar(
            store_performance,
            x="store_id",
            y="total_revenue",
            title="Total Revenue by Store",
            color="store_id"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        section_header("Rentals per Inventory Item")
        fig = plot_bar(
            store_performance,
            x="store_id",
            y="rentals_per_inventory_item",
            title="Inventory Efficiency by Store",
            color="store_id"
        )
        st.plotly_chart(fig, use_container_width=True)

    section_header("Slow-Moving Inventory")
    fig = plot_bar(
        slow_inventory.sort_values("rental_count", ascending=True),
        x="rental_count",
        y="title",
        title="Slow-Moving Film Copies",
        orientation="h"
    )
    st.plotly_chart(fig, use_container_width=True)

    pretty_table(
        "Slow-Moving Inventory Table",
        slow_inventory,
        money_cols=["rental_rate", "total_revenue"],
        number_cols=["inventory_id", "store_id", "film_id", "rental_count"]
    )


# ------------------------------------------------------------
# 10. Recommendation Insights
# ------------------------------------------------------------
elif page == "Recommendation Insights":
    st.markdown(
        '<p class="dashboard-title">Recommendation Insights</p>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<p class="dashboard-subtitle">Category-based recommendation priorities for promotions.</p>',
        unsafe_allow_html=True
    )

    high_priority = recommendations[
        recommendations["recommendation_priority"] == "High Priority"
    ]

    medium_priority = recommendations[
        recommendations["recommendation_priority"] == "Medium Priority"
    ]

    col1, col2, col3 = st.columns(3)

    with col1:
        metric_card("High Priority Categories", f"{len(high_priority)}")
    with col2:
        metric_card("Medium Priority Categories", f"{len(medium_priority)}")
    with col3:
        metric_card("Best Recommendation Category", recommendations.iloc[0]["category"])

    st.markdown("<br>", unsafe_allow_html=True)

    insight_box(
        "The first recommendation strategy should focus on high-performing categories. This gives the business a simple, practical recommendation engine without requiring complex machine learning."
    )

    section_header("Recommended Categories for Promotion")
    recommendation_view = recommendations.sort_values(
        "total_revenue",
        ascending=True
    )

    fig = plot_bar(
        recommendation_view,
        x="total_revenue",
        y="category",
        title="Recommendation Priority by Category Revenue",
        orientation="h",
        color="recommendation_priority"
    )
    st.plotly_chart(fig, use_container_width=True)

    pretty_table(
        "Recommendation Priority Table",
        recommendations.sort_values(by="total_revenue", ascending=False),
        money_cols=[
            "total_revenue",
            "average_payment",
            "average_rental_rate"
        ],
        number_cols=["total_rentals"]
    )

    st.markdown(
        """
        <div class="insight-box">
        <b>How this can be used:</b><br>
        If a customer rents from a strong category such as Sports, Sci-Fi, Animation, Drama or Comedy,
        the company can recommend other popular titles from the same category. This is a realistic
        first step before building a more advanced customer-level recommendation model.
        </div>
        """,
        unsafe_allow_html=True
    )