"""
4_analysis.py

Purpose:
Runs the main business analysis for the DVD Rental project.

This script covers customer value, churn risk, customer behaviour,
category revenue, monthly revenue trends, pricing insight, store performance,
slow-moving inventory, and simple recommendation analysis.

Outputs:
tables/customer_segments.csv
tables/churn_risk_customers.csv
tables/customer_behavior_patterns.csv
tables/monthly_revenue_trend.csv
tables/revenue_by_category.csv
tables/pricing_insight.csv
tables/store_performance_analysis.csv
tables/slow_moving_inventory.csv
tables/recommendation_candidates.csv
exports/business_insights_summary.txt
results/customer_segments.png
results/churn_risk_customers.png
results/customer_behavior_patterns.png
results/monthly_revenue_trend_analysis.png
results/revenue_by_category_analysis.png
results/store_revenue_comparison.png
results/slow_moving_inventory.png
results/recommendation_categories.png
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
from dotenv import load_dotenv


# Create output folders
os.makedirs("tables", exist_ok=True)
os.makedirs("results", exist_ok=True)
os.makedirs("exports", exist_ok=True)


# Load database connection details
load_dotenv()

DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_HOST = "localhost"

connection_url = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(connection_url)


def save_chart(filename):
    """Save the current chart in the results folder."""
    plt.tight_layout()
    plt.savefig(f"results/{filename}", dpi=300)
    plt.close()


# Load merged datasets
customer_df = pd.read_csv("merges/customer_revenue_dataset.csv")
film_category_df = pd.read_csv("merges/film_category_revenue_dataset.csv")
store_df = pd.read_csv("merges/store_performance_dataset.csv")
inventory_df = pd.read_csv("merges/inventory_turnover_dataset.csv")

print("Merged datasets loaded successfully.")


# Customer value segmentation
customer_df["customer_name"] = (
    customer_df["first_name"].astype(str) + " " + customer_df["last_name"].astype(str)
)

customer_df["customer_segment"] = pd.qcut(
    customer_df["total_revenue"],
    q=3,
    labels=["Low Value", "Medium Value", "High Value"],
    duplicates="drop"
)

customer_segments = (
    customer_df
    .groupby("customer_segment", observed=False)
    .agg(
        number_of_customers=("customer_id", "count"),
        total_revenue=("total_revenue", "sum"),
        average_revenue=("total_revenue", "mean"),
        average_payment=("average_payment", "mean")
    )
    .reset_index()
)

customer_segments.to_csv("tables/customer_segments.csv", index=False)

plt.figure(figsize=(8, 5))
sns.barplot(
    data=customer_segments,
    x="customer_segment",
    y="total_revenue"
)
plt.title("Revenue Contribution by Customer Segment")
plt.xlabel("Customer Segment")
plt.ylabel("Total Revenue")
save_chart("customer_segments.png")

print("Customer segmentation completed.")


# Churn risk scoring
customer_df["last_payment_date"] = pd.to_datetime(
    customer_df["last_payment_date"],
    errors="coerce"
)

latest_payment_date = customer_df["last_payment_date"].max()

customer_df["days_since_last_payment"] = (
    latest_payment_date - customer_df["last_payment_date"]
).dt.days

customer_df["days_since_last_payment"] = (
    customer_df["days_since_last_payment"].fillna(999)
)

customer_df["churn_risk"] = pd.cut(
    customer_df["days_since_last_payment"],
    bins=[-1, 30, 90, 9999],
    labels=["Low Risk", "Medium Risk", "High Risk"]
)

churn_summary = (
    customer_df
    .groupby("churn_risk", observed=False)
    .agg(
        number_of_customers=("customer_id", "count"),
        average_revenue=("total_revenue", "mean"),
        total_revenue=("total_revenue", "sum")
    )
    .reset_index()
)

churn_summary.to_csv("tables/churn_risk_customers.csv", index=False)

plt.figure(figsize=(8, 5))
sns.barplot(
    data=churn_summary,
    x="churn_risk",
    y="number_of_customers"
)
plt.title("Customer Churn Risk Distribution")
plt.xlabel("Churn Risk Group")
plt.ylabel("Number of Customers")
save_chart("churn_risk_customers.png")

print("Churn risk analysis completed.")


# Customer behaviour patterns
if "total_rentals" in customer_df.columns:
    activity_column = "total_rentals"
elif "rental_count" in customer_df.columns:
    activity_column = "rental_count"
elif "number_of_rentals" in customer_df.columns:
    activity_column = "number_of_rentals"
elif "payment_count" in customer_df.columns:
    activity_column = "payment_count"
else:
    activity_column = "total_revenue"

customer_df["activity_group"] = pd.qcut(
    customer_df[activity_column].rank(method="first"),
    q=3,
    labels=["Low Activity", "Medium Activity", "High Activity"]
)

customer_behavior_patterns = (
    customer_df
    .groupby("activity_group", observed=False)
    .agg(
        number_of_customers=("customer_id", "count"),
        total_activity=(activity_column, "sum"),
        total_revenue=("total_revenue", "sum"),
        average_revenue=("total_revenue", "mean"),
        average_payment=("average_payment", "mean")
    )
    .reset_index()
)

customer_behavior_patterns.to_csv(
    "tables/customer_behavior_patterns.csv",
    index=False
)

plt.figure(figsize=(8, 5))
sns.barplot(
    data=customer_behavior_patterns,
    x="activity_group",
    y="total_revenue"
)
plt.title("Revenue by Customer Activity Group")
plt.xlabel("Customer Activity Group")
plt.ylabel("Total Revenue")
save_chart("customer_behavior_patterns.png")

print("Customer behaviour analysis completed.")


# Monthly revenue trend
monthly_revenue_query = """
SELECT
    DATE_TRUNC('month', payment_date) AS month,
    SUM(amount) AS total_revenue,
    COUNT(payment_id) AS number_of_payments
FROM payment
GROUP BY month
ORDER BY month;
"""

monthly_revenue_trend = pd.read_sql(monthly_revenue_query, engine)

monthly_revenue_trend.to_csv(
    "tables/monthly_revenue_trend.csv",
    index=False
)

plt.figure(figsize=(10, 5))
sns.lineplot(
    data=monthly_revenue_trend,
    x="month",
    y="total_revenue",
    marker="o"
)
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Total Revenue")
plt.xticks(rotation=45)
save_chart("monthly_revenue_trend_analysis.png")

print("Monthly revenue trend analysis completed.")


# Revenue by film category
revenue_by_category = (
    film_category_df
    .groupby("category")
    .agg(
        total_revenue=("total_revenue", "sum"),
        total_rentals=("total_rentals", "sum"),
        average_payment=("average_payment", "mean"),
        average_rental_rate=("rental_rate", "mean")
    )
    .reset_index()
    .sort_values(by="total_revenue", ascending=False)
)

revenue_by_category.to_csv("tables/revenue_by_category.csv", index=False)

plt.figure(figsize=(10, 6))
sns.barplot(
    data=revenue_by_category,
    x="total_revenue",
    y="category"
)
plt.title("Revenue by Film Category")
plt.xlabel("Total Revenue")
plt.ylabel("Film Category")
save_chart("revenue_by_category_analysis.png")

print("Revenue by category analysis completed.")


# Pricing insight
pricing_insight = film_category_df[
    ["title", "category", "rental_rate", "total_rentals", "total_revenue"]
].copy()

pricing_insight["revenue_per_rental"] = (
    pricing_insight["total_revenue"] / pricing_insight["total_rentals"]
)

pricing_insight["revenue_per_rental"] = (
    pricing_insight["revenue_per_rental"]
    .replace([float("inf")], 0)
    .fillna(0)
)

pricing_insight.to_csv("tables/pricing_insight.csv", index=False)

print("Pricing insight table created.")


# Store performance
store_df["revenue_per_inventory_item"] = (
    store_df["total_revenue"] / store_df["total_inventory_items"]
)

store_df["rentals_per_inventory_item"] = (
    store_df["total_rentals"] / store_df["total_inventory_items"]
)

store_df.to_csv("tables/store_performance_analysis.csv", index=False)

plt.figure(figsize=(7, 5))
sns.barplot(
    data=store_df,
    x="store_id",
    y="total_revenue"
)
plt.title("Revenue Comparison by Store")
plt.xlabel("Store ID")
plt.ylabel("Total Revenue")
save_chart("store_revenue_comparison.png")

print("Store performance analysis completed.")


# Slow-moving inventory
slow_moving_inventory = (
    inventory_df
    .sort_values(by=["rental_count", "total_revenue"], ascending=[True, True])
    .head(20)
)

slow_moving_inventory.to_csv("tables/slow_moving_inventory.csv", index=False)

plt.figure(figsize=(10, 6))
sns.barplot(
    data=slow_moving_inventory,
    x="rental_count",
    y="title"
)
plt.title("Top 20 Slow-Moving Inventory Items")
plt.xlabel("Rental Count")
plt.ylabel("Film Title")
save_chart("slow_moving_inventory.png")

print("Slow-moving inventory analysis completed.")


# Simple recommendation analysis
recommendation_candidates = revenue_by_category.copy()

recommendation_candidates["recommendation_priority"] = pd.qcut(
    recommendation_candidates["total_revenue"],
    q=3,
    labels=["Low Priority", "Medium Priority", "High Priority"],
    duplicates="drop"
)

recommendation_candidates.to_csv(
    "tables/recommendation_candidates.csv",
    index=False
)

top_recommendation_categories = recommendation_candidates.sort_values(
    by="total_revenue",
    ascending=False
).head(8)

plt.figure(figsize=(10, 5))
sns.barplot(
    data=top_recommendation_categories,
    x="total_revenue",
    y="category"
)
plt.title("Recommended Categories for Promotion")
plt.xlabel("Total Revenue")
plt.ylabel("Category")
save_chart("recommendation_categories.png")

print("Recommendation analysis completed.")


# Business insights summary
top_customer_segment = customer_segments.sort_values(
    by="total_revenue",
    ascending=False
).iloc[0]

top_activity_group = customer_behavior_patterns.sort_values(
    by="total_revenue",
    ascending=False
).iloc[0]

top_month = monthly_revenue_trend.sort_values(
    by="total_revenue",
    ascending=False
).iloc[0]

top_category = revenue_by_category.iloc[0]
lowest_category = revenue_by_category.iloc[-1]

best_store = store_df.sort_values(
    by="total_revenue",
    ascending=False
).iloc[0]

highest_churn_group = churn_summary.sort_values(
    by="number_of_customers",
    ascending=False
).iloc[0]

summary = f"""
BUSINESS INSIGHTS SUMMARY
=========================

1. Customer Analytics
---------------------
The customer base was grouped into value segments using total revenue.
Total historical revenue was used as a simple measure of customer lifetime value.

The segment contributing the highest revenue is:

Segment: {top_customer_segment["customer_segment"]}
Total Revenue: {top_customer_segment["total_revenue"]:.2f}
Number of Customers: {top_customer_segment["number_of_customers"]}

This shows that customer value is not evenly distributed. The business should
protect high-value customers through loyalty offers and targeted promotions.

Churn Risk:
The largest churn risk group is:

Risk Group: {highest_churn_group["churn_risk"]}
Number of Customers: {highest_churn_group["number_of_customers"]}

Customers with longer periods since their last payment should be monitored and
targeted with reactivation offers where necessary.

Customer Behaviour:
The activity group contributing the highest revenue is:

Activity Group: {top_activity_group["activity_group"]}
Total Revenue: {top_activity_group["total_revenue"]:.2f}
Total Activity: {top_activity_group["total_activity"]}

This shows that customer activity is useful to track when planning repeat rental
campaigns.


2. Revenue Optimization
-----------------------
The highest revenue film category is:

Category: {top_category["category"]}
Total Revenue: {top_category["total_revenue"]:.2f}
Total Rentals: {top_category["total_rentals"]}

The lowest revenue film category is:

Category: {lowest_category["category"]}
Total Revenue: {lowest_category["total_revenue"]:.2f}
Total Rentals: {lowest_category["total_rentals"]}

The strongest revenue month is:

Month: {top_month["month"]}
Total Revenue: {top_month["total_revenue"]:.2f}
Number of Payments: {top_month["number_of_payments"]}

High-performing categories should receive more promotion. Low-performing
categories should be reviewed for pricing, demand, and inventory allocation.
Monthly revenue trends should also be monitored for planning campaigns.


3. Inventory and Operations
---------------------------
The best-performing store by revenue is:

Store ID: {best_store["store_id"]}
Total Revenue: {best_store["total_revenue"]:.2f}
Total Rentals: {best_store["total_rentals"]}
Total Inventory Items: {best_store["total_inventory_items"]}

Store-level differences should be reviewed to understand whether performance is
driven by customer base, inventory selection, or rental activity.


4. Innovation / Custom Analysis
-------------------------------
A simple recommendation approach was created using category revenue and rental
performance. Strong categories can be used as the first basis for customer
recommendations and promotional campaigns.

Recommended action:
If a customer rents from a strong category, the business can suggest other films
from that same high-performing category.


Quantified Business Recommendations
-----------------------------------
1. Protect high-value customers with loyalty campaigns and targeted offers.
2. Monitor customers with longer payment gaps and use reactivation offers where necessary.
3. Use customer activity groups to design repeat rental campaigns.
4. Promote the strongest film categories more aggressively.
5. Review low-performing categories for possible pricing or inventory changes.
6. Monitor monthly revenue trends to support campaign timing.
7. Monitor slow-moving inventory and consider reducing duplicate copies.
8. Compare store-level inventory efficiency to improve stock allocation.
"""

with open("exports/business_insights_summary.txt", "w", encoding="utf-8") as file:
    file.write(summary)

print("Saved: exports/business_insights_summary.txt")
print("\nAdvanced business analysis completed successfully.")