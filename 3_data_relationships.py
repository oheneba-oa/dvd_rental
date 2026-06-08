"""
3_data_relationships.py

Purpose:
This script creates merged datasets from the DVD Rental database.
The merged datasets will be used for customer analytics, revenue analysis,
inventory analysis, and store performance analysis.

Outputs:
- merges/customer_revenue_dataset.csv
- merges/film_category_revenue_dataset.csv
- merges/store_performance_dataset.csv
- merges/inventory_turnover_dataset.csv
- exports/data_relationships_report.txt
"""

import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv


# ------------------------------------------------------------
# 1. Load database connection details
# ------------------------------------------------------------
load_dotenv()

DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_HOST = "localhost"


# ------------------------------------------------------------
# 2. Create database connection
# ------------------------------------------------------------
connection_url = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(connection_url)


# ------------------------------------------------------------
# 3. Create output folders
# ------------------------------------------------------------
os.makedirs("merges", exist_ok=True)
os.makedirs("exports", exist_ok=True)


try:
    with engine.connect() as connection:
        print("Database connection successful.")

        # ------------------------------------------------------------
        # 4. Customer revenue dataset
        # ------------------------------------------------------------
        # Purpose:
        # This dataset combines customer and payment data to understand
        # customer value, payment frequency, and recency.
        #
        # Join key:
        # customer.customer_id = payment.customer_id
        #
        # LEFT JOIN is used so that all customers are retained,
        # even if some have no payment record.
        customer_revenue_query = """
        SELECT
            c.customer_id,
            c.first_name,
            c.last_name,
            c.email,
            c.active,
            c.create_date,
            c.store_id,
            COUNT(p.payment_id) AS total_payments,
            COALESCE(SUM(p.amount), 0) AS total_revenue,
            COALESCE(AVG(p.amount), 0) AS average_payment,
            MAX(p.payment_date) AS last_payment_date
        FROM customer c
        LEFT JOIN payment p
            ON c.customer_id = p.customer_id
        GROUP BY
            c.customer_id,
            c.first_name,
            c.last_name,
            c.email,
            c.active,
            c.create_date,
            c.store_id
        ORDER BY total_revenue DESC;
        """

        customer_revenue_df = pd.read_sql(customer_revenue_query, connection)

        customer_revenue_df.to_csv(
            "merges/customer_revenue_dataset.csv",
            index=False
        )

        print("Saved: merges/customer_revenue_dataset.csv")

        # ------------------------------------------------------------
        # 5. Film category revenue dataset
        # ------------------------------------------------------------
        # Purpose:
        # This dataset links films to categories, rentals, and payments.
        # It helps identify which film categories generate the most revenue.
        #
        # Join path:
        # payment -> rental -> inventory -> film -> film_category -> category
        #
        # COUNT(DISTINCT r.rental_id) is used to avoid possible duplicate
        # rental counts after joining payment records.
        film_category_revenue_query = """
        SELECT
            f.film_id,
            f.title,
            f.rating,
            f.rental_rate,
            f.replacement_cost,
            f.length,
            c.name AS category,
            COUNT(DISTINCT r.rental_id) AS total_rentals,
            COALESCE(SUM(p.amount), 0) AS total_revenue,
            COALESCE(AVG(p.amount), 0) AS average_payment
        FROM film f
        JOIN film_category fc
            ON f.film_id = fc.film_id
        JOIN category c
            ON fc.category_id = c.category_id
        LEFT JOIN inventory i
            ON f.film_id = i.film_id
        LEFT JOIN rental r
            ON i.inventory_id = r.inventory_id
        LEFT JOIN payment p
            ON r.rental_id = p.rental_id
        GROUP BY
            f.film_id,
            f.title,
            f.rating,
            f.rental_rate,
            f.replacement_cost,
            f.length,
            c.name
        ORDER BY total_revenue DESC;
        """

        film_category_revenue_df = pd.read_sql(
            film_category_revenue_query,
            connection
        )

        film_category_revenue_df.to_csv(
            "merges/film_category_revenue_dataset.csv",
            index=False
        )

        print("Saved: merges/film_category_revenue_dataset.csv")

        # ------------------------------------------------------------
        # 6. Store performance dataset
        # ------------------------------------------------------------
        # Purpose:
        # This dataset compares stores using customer count, inventory count,
        # rental count, and revenue.
        #
        # Important correction:
        # Customer, inventory, rental, and payment metrics are calculated in
        # separate grouped subqueries before being joined together.
        # This prevents revenue from being multiplied by duplicate join paths.
        store_performance_query = """
        WITH customer_counts AS (
            SELECT
                store_id,
                COUNT(customer_id) AS total_customers
            FROM customer
            GROUP BY store_id
        ),

        inventory_counts AS (
            SELECT
                store_id,
                COUNT(inventory_id) AS total_inventory_items
            FROM inventory
            GROUP BY store_id
        ),

        rental_revenue AS (
            SELECT
                i.store_id,
                COUNT(DISTINCT r.rental_id) AS total_rentals,
                COALESCE(SUM(p.amount), 0) AS total_revenue
            FROM inventory i
            LEFT JOIN rental r
                ON i.inventory_id = r.inventory_id
            LEFT JOIN payment p
                ON r.rental_id = p.rental_id
            GROUP BY i.store_id
        )

        SELECT
            s.store_id,
            COALESCE(cc.total_customers, 0) AS total_customers,
            COALESCE(ic.total_inventory_items, 0) AS total_inventory_items,
            COALESCE(rr.total_rentals, 0) AS total_rentals,
            COALESCE(rr.total_revenue, 0) AS total_revenue
        FROM store s
        LEFT JOIN customer_counts cc
            ON s.store_id = cc.store_id
        LEFT JOIN inventory_counts ic
            ON s.store_id = ic.store_id
        LEFT JOIN rental_revenue rr
            ON s.store_id = rr.store_id
        ORDER BY s.store_id;
        """

        store_performance_df = pd.read_sql(
            store_performance_query,
            connection
        )

        store_performance_df.to_csv(
            "merges/store_performance_dataset.csv",
            index=False
        )

        print("Saved: merges/store_performance_dataset.csv")

        # ------------------------------------------------------------
        # 7. Inventory turnover dataset
        # ------------------------------------------------------------
        # Purpose:
        # This dataset measures how often each film copy is rented.
        # It helps identify fast-moving and slow-moving inventory.
        #
        # Join path:
        # inventory -> film -> film_category -> category -> rental -> payment
        #
        # COUNT(DISTINCT r.rental_id) is used to avoid possible duplicate
        # rental counts after joining payment records.
        inventory_turnover_query = """
        SELECT
            i.inventory_id,
            i.store_id,
            f.film_id,
            f.title,
            f.rating,
            f.rental_rate,
            c.name AS category,
            COUNT(DISTINCT r.rental_id) AS rental_count,
            COALESCE(SUM(p.amount), 0) AS total_revenue,
            MAX(r.rental_date) AS last_rental_date
        FROM inventory i
        JOIN film f
            ON i.film_id = f.film_id
        JOIN film_category fc
            ON f.film_id = fc.film_id
        JOIN category c
            ON fc.category_id = c.category_id
        LEFT JOIN rental r
            ON i.inventory_id = r.inventory_id
        LEFT JOIN payment p
            ON r.rental_id = p.rental_id
        GROUP BY
            i.inventory_id,
            i.store_id,
            f.film_id,
            f.title,
            f.rating,
            f.rental_rate,
            c.name
        ORDER BY rental_count DESC;
        """

        inventory_turnover_df = pd.read_sql(
            inventory_turnover_query,
            connection
        )

        inventory_turnover_df.to_csv(
            "merges/inventory_turnover_dataset.csv",
            index=False
        )

        print("Saved: merges/inventory_turnover_dataset.csv")

        # ------------------------------------------------------------
        # 8. Validate merged outputs
        # ------------------------------------------------------------
        validation_summary = {
            "customer_revenue_dataset_rows": len(customer_revenue_df),
            "film_category_revenue_dataset_rows": len(film_category_revenue_df),
            "store_performance_dataset_rows": len(store_performance_df),
            "inventory_turnover_dataset_rows": len(inventory_turnover_df),
            "customer_revenue_columns": len(customer_revenue_df.columns),
            "film_category_revenue_columns": len(film_category_revenue_df.columns),
            "store_performance_columns": len(store_performance_df.columns),
            "inventory_turnover_columns": len(inventory_turnover_df.columns),
        }

        # ------------------------------------------------------------
        # 9. Write relationship report
        # ------------------------------------------------------------
        report = f"""
DATA RELATIONSHIP AND MERGE REPORT
==================================

Purpose:
This report documents the merged datasets created for the DVD Rental analysis.

1. Customer Revenue Dataset
---------------------------
Output file:
merges/customer_revenue_dataset.csv

Tables used:
customer, payment

Join key:
customer.customer_id = payment.customer_id

Join type:
LEFT JOIN

Reason:
The customer table is the base table because the analysis focuses on customer value.
A LEFT JOIN keeps all customers, including customers with no payment records.

Rows created:
{validation_summary["customer_revenue_dataset_rows"]}

Columns created:
{validation_summary["customer_revenue_columns"]}


2. Film Category Revenue Dataset
--------------------------------
Output file:
merges/film_category_revenue_dataset.csv

Tables used:
film, film_category, category, inventory, rental, payment

Join path:
film.film_id = film_category.film_id
film_category.category_id = category.category_id
film.film_id = inventory.film_id
inventory.inventory_id = rental.inventory_id
rental.rental_id = payment.rental_id

Join type:
Combination of INNER JOIN and LEFT JOIN

Reason:
INNER JOIN is used where category relationships are required.
LEFT JOIN is used for rental and payment records so films can still appear
even if some inventory copies have no rental or payment record.
COUNT(DISTINCT rental.rental_id) is used to protect rental counts from possible
duplication after joining payment records.

Rows created:
{validation_summary["film_category_revenue_dataset_rows"]}

Columns created:
{validation_summary["film_category_revenue_columns"]}


3. Store Performance Dataset
----------------------------
Output file:
merges/store_performance_dataset.csv

Tables used:
store, customer, inventory, rental, payment

Join keys:
store.store_id = customer.store_id
store.store_id = inventory.store_id
inventory.inventory_id = rental.inventory_id
rental.rental_id = payment.rental_id

Join type:
Grouped subqueries with LEFT JOIN

Reason:
Customer counts, inventory counts, rental counts, and revenue are calculated
separately before joining to the store table. This avoids revenue duplication
that can happen when multiple one-to-many relationships are joined directly
in a single query.

Rows created:
{validation_summary["store_performance_dataset_rows"]}

Columns created:
{validation_summary["store_performance_columns"]}


4. Inventory Turnover Dataset
-----------------------------
Output file:
merges/inventory_turnover_dataset.csv

Tables used:
inventory, film, film_category, category, rental, payment

Join keys:
inventory.film_id = film.film_id
film.film_id = film_category.film_id
film_category.category_id = category.category_id
inventory.inventory_id = rental.inventory_id
rental.rental_id = payment.rental_id

Join type:
Combination of INNER JOIN and LEFT JOIN

Reason:
Inventory and film details are required for stock analysis.
LEFT JOIN is used for rental and payment data so that slow-moving or unrented
inventory can still be identified.
COUNT(DISTINCT rental.rental_id) is used to protect rental counts from possible
duplication after joining payment records.

Rows created:
{validation_summary["inventory_turnover_dataset_rows"]}

Columns created:
{validation_summary["inventory_turnover_columns"]}


Assumptions and Limitations:
----------------------------
1. Revenue is measured using the payment.amount field.
2. Rental activity is measured using distinct rental_id counts.
3. Customer value is estimated using total payment amount.
4. Store performance is compared using revenue, rentals, customers, and inventory.
5. Store performance uses grouped subqueries to avoid revenue overcounting.
6. Some historical records may not fully represent current customer behaviour.
7. This script creates analysis-ready datasets but does not yet make final
   business recommendations. Those are developed in 4_analysis.py.
"""

        with open(
            "exports/data_relationships_report.txt",
            "w",
            encoding="utf-8"
        ) as file:
            file.write(report)

        print("Saved: exports/data_relationships_report.txt")

        print("\nData relationship mapping completed successfully.")

except Exception as error:
    print("Data relationship mapping failed.")
    print("Error:", error)