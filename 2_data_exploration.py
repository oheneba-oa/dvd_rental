"""
2_data_exploration.py

Purpose:
This script performs exploratory data analysis on the DVD Rental database.
It inspects table structures, checks missing values, creates descriptive
statistics, identifies simple outliers, and produces business-related charts.

Outputs:
- tables/schema_summary.csv
- tables/missing_values_summary.csv
- tables/descriptive_statistics.csv
- tables/outlier_summary.csv
- results/monthly_revenue.png
- results/top_film_categories_by_revenue.png
- results/top_customers_by_revenue.png
- results/rentals_by_store.png
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
from dotenv import load_dotenv



# Load database connection details

load_dotenv()

DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")


DB_HOST = "localhost"



# Create database connection

connection_url = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(connection_url)



# Create output folders

os.makedirs("tables", exist_ok=True)
os.makedirs("results", exist_ok=True)



# Define helper function for saving charts

def save_chart(filename):
    """
    Saves the current matplotlib chart into the results folder.
    """
    plt.tight_layout()
    plt.savefig(f"results/{filename}", dpi=300)
    plt.close()


# A try-except block is used so that database connection or query errors
# are displayed clearly instead of stopping the script without context.
try:
    with engine.connect() as connection:
        print("Database connection successful.")

        
        # Get all base tables
        # This query retrieves only real/base tables from the public schema.
        # Views are excluded because this stage focuses on the original tables.
        tables_query = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        AND table_type = 'BASE TABLE'
        ORDER BY table_name;
        """

        tables_df = pd.read_sql(tables_query, connection)
        table_names = tables_df["table_name"].tolist()

        print("Tables found:")
        print(table_names)

        
        # Schema and data type inspection
        # This section records each table's column names and data types.
        # It helps document the structure of the database before analysis.
        schema_results = []

        for table in table_names:
            schema_query = f"""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_schema = 'public'
            AND table_name = '{table}'
            ORDER BY ordinal_position;
            """

            schema_df = pd.read_sql(schema_query, connection)

            for _, row in schema_df.iterrows():
                schema_results.append({
                    "table_name": table,
                    "column_name": row["column_name"],
                    "data_type": row["data_type"]
                })

        schema_summary_df = pd.DataFrame(schema_results)
        schema_summary_df.to_csv("tables/schema_summary.csv", index=False)

        print("Schema summary saved to tables/schema_summary.csv")

        
        # Missing values check
        # A sample of up to 1000 rows is checked from each table to identify
        # missing values without loading very large tables unnecessarily.
        missing_results = []

        for table in table_names:
            df = pd.read_sql(
                f'SELECT * FROM "{table}" LIMIT 1000;',
                connection
            )

            for column in df.columns:
                missing_results.append({
                    "table_name": table,
                    "column_name": column,
                    "sample_rows_checked": len(df),
                    "missing_values": df[column].isnull().sum()
                })

        missing_df = pd.DataFrame(missing_results)
        missing_df.to_csv("tables/missing_values_summary.csv", index=False)

        print("Missing values summary saved to tables/missing_values_summary.csv")

        
        # Descriptive statistics for key numeric tables
        # Descriptive statistics are calculated only for selected numeric tables
        # because these tables contain revenue, rental, inventory, and film metrics.
        key_numeric_tables = ["payment", "film", "rental", "inventory"]

        descriptive_results = []

        for table in key_numeric_tables:
            df = pd.read_sql(f'SELECT * FROM "{table}";', connection)
            numeric_df = df.select_dtypes(include=["number"])

            if not numeric_df.empty:
                stats_df = numeric_df.describe().T
                stats_df["table_name"] = table
                stats_df["column_name"] = stats_df.index
                descriptive_results.append(stats_df.reset_index(drop=True))

        descriptive_statistics_df = pd.concat(
            descriptive_results,
            ignore_index=True
        )

        descriptive_statistics_df.to_csv(
            "tables/descriptive_statistics.csv",
            index=False
        )

        print("Descriptive statistics saved to tables/descriptive_statistics.csv")

        
        # Simple outlier check using IQR method
        # The IQR method identifies possible outliers by comparing values
        # against lower and upper statistical boundaries.
        outlier_results = []

        for table in key_numeric_tables:
            df = pd.read_sql(f'SELECT * FROM "{table}";', connection)
            numeric_df = df.select_dtypes(include=["number"])

            for column in numeric_df.columns:
                q1 = numeric_df[column].quantile(0.25)
                q3 = numeric_df[column].quantile(0.75)
                iqr = q3 - q1

                lower_bound = q1 - 1.5 * iqr
                upper_bound = q3 + 1.5 * iqr

                outlier_count = numeric_df[
                    (numeric_df[column] < lower_bound) |
                    (numeric_df[column] > upper_bound)
                ].shape[0]

                outlier_results.append({
                    "table_name": table,
                    "column_name": column,
                    "lower_bound": lower_bound,
                    "upper_bound": upper_bound,
                    "outlier_count": outlier_count
                })

        outlier_df = pd.DataFrame(outlier_results)
        outlier_df.to_csv("tables/outlier_summary.csv", index=False)

        print("Outlier summary saved to tables/outlier_summary.csv")

        
        # Visualization 1: Monthly revenue trend
        # This chart shows how revenue changes over time by grouping payments by month.
        monthly_revenue_query = """
        SELECT
            DATE_TRUNC('month', payment_date) AS month,
            SUM(amount) AS total_revenue
        FROM payment
        GROUP BY month
        ORDER BY month;
        """

        monthly_revenue_df = pd.read_sql(monthly_revenue_query, connection)

        plt.figure(figsize=(10, 5))
        sns.lineplot(
            data=monthly_revenue_df,
            x="month",
            y="total_revenue",
            marker="o"
        )
        plt.title("Monthly Revenue Trend")
        plt.xlabel("Month")
        plt.ylabel("Total Revenue")
        plt.xticks(rotation=45)
        save_chart("monthly_revenue.png")

        print("Chart saved: results/monthly_revenue.png")

        
        # Visualization 2: Top film categories by revenue
        # This chart identifies which film categories generate the highest revenue.
        category_revenue_query = """
        SELECT
            c.name AS category,
            SUM(p.amount) AS total_revenue
        FROM payment p
        JOIN rental r ON p.rental_id = r.rental_id
        JOIN inventory i ON r.inventory_id = i.inventory_id
        JOIN film f ON i.film_id = f.film_id
        JOIN film_category fc ON f.film_id = fc.film_id
        JOIN category c ON fc.category_id = c.category_id
        GROUP BY c.name
        ORDER BY total_revenue DESC;
        """

        category_revenue_df = pd.read_sql(category_revenue_query, connection)

        plt.figure(figsize=(10, 5))
        sns.barplot(
            data=category_revenue_df,
            x="total_revenue",
            y="category"
        )
        plt.title("Film Categories by Revenue")
        plt.xlabel("Total Revenue")
        plt.ylabel("Film Category")
        save_chart("top_film_categories_by_revenue.png")

        print("Chart saved: results/top_film_categories_by_revenue.png")

        
        # Visualization 3: Top 10 customers by revenue
        # This chart identifies the customers contributing the most revenue.
        top_customers_query = """
        SELECT
            CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
            SUM(p.amount) AS total_revenue
        FROM payment p
        JOIN customer c ON p.customer_id = c.customer_id
        GROUP BY customer_name
        ORDER BY total_revenue DESC
        LIMIT 10;
        """

        top_customers_df = pd.read_sql(top_customers_query, connection)

        plt.figure(figsize=(10, 5))
        sns.barplot(
            data=top_customers_df,
            x="total_revenue",
            y="customer_name"
        )
        plt.title("Top 10 Customers by Revenue")
        plt.xlabel("Total Revenue")
        plt.ylabel("Customer")
        save_chart("top_customers_by_revenue.png")

        print("Chart saved: results/top_customers_by_revenue.png")

        
        # Visualization 4: Number of rentals by store
        # This chart compares rental activity between stores.
        # DISTINCT is used for consistency with later analysis scripts.
        rentals_by_store_query = """
        SELECT
            s.store_id,
            COUNT(DISTINCT r.rental_id) AS total_rentals
        FROM rental r
        JOIN inventory i ON r.inventory_id = i.inventory_id
        JOIN store s ON i.store_id = s.store_id
        GROUP BY s.store_id
        ORDER BY s.store_id;
        """

        rentals_by_store_df = pd.read_sql(rentals_by_store_query, connection)

        plt.figure(figsize=(7, 5))
        sns.barplot(
            data=rentals_by_store_df,
            x="store_id",
            y="total_rentals"
        )
        plt.title("Total Rentals by Store")
        plt.xlabel("Store ID")
        plt.ylabel("Total Rentals")
        save_chart("rentals_by_store.png")

        print("Chart saved: results/rentals_by_store.png")

        print("\nExploratory data analysis completed successfully.")

except Exception as error:
    print("Exploratory data analysis failed.")
    print("Error:", error)