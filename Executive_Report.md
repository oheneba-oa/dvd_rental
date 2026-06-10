# Executive Report

## DVD Rental Business Analytics Project

**Name:** Oheneba Oduro-Asare
**Roll Number:** 2000250072
**Course:** DSA5102 Big Data Management

---

## 1. Executive Summary

This project analyses the operations of a mid-sized DVD rental company using the restored DVD Rental PostgreSQL database. The company operates through physical stores and keeps records on customers, rentals, payments, films, inventory, staff, and stores. The main business challenge is to understand how customer behaviour, film category performance, store operations, and inventory movement affect revenue and operational efficiency.

The analysis was guided by four objectives. First, customer analytics was used to segment customers by value and assess churn risk. Second, revenue optimization was carried out by examining category-level revenue, rental activity, and pricing-related patterns. Third, inventory and operations analysis was used to compare store performance and identify slow-moving film copies. Fourth, a simple category-based recommendation approach was developed to support promotional targeting.

The workflow was implemented as a reproducible data pipeline. Docker and Docker Compose were used to manage the PostgreSQL and pgAdmin environment. Python scripts were used to validate the database, explore the data, create merged datasets, perform business analysis, generate charts, and produce outputs. A Streamlit dashboard was also developed to communicate insights through KPI cards, charts, tables, and multi-page navigation.

The dashboard supports decision-making by allowing users to review key performance indicators, compare charts, and inspect the generated analysis tables in one interface.

The analysis shows that total customer revenue is concentrated across value segments, with the high-value segment generating **26,009.63** in revenue compared with **15,329.62** from the low-value segment. Sports was the strongest film category, generating **4,892.19** from **1,179 rentals**, while Music was the lowest revenue category, generating **3,071.52** from **830 rentals**. Store performance was fairly balanced, with Store 1 generating **30,628.91** and Store 2 generating **30,683.13**. These findings suggest that management should focus on protecting high-value customers, promoting strong categories, reviewing weak categories, and monitoring slow-moving inventory.

---

## 2. Business Context and Analytical Objectives

The DVD rental company operates in a competitive entertainment environment where customer retention, inventory use, and revenue optimization are important. Management needs evidence-based guidance on which customers generate the most value, which film categories drive revenue, which stores perform best, and which inventory items may be underused.

The project was guided by the following analytical objectives:

### Objective 1: Identify Customer Value and Behaviour

The first objective was to segment customers based on total revenue contribution and payment activity. This helps management understand whether revenue is evenly distributed across customers or concentrated among a smaller high-value group. It also supports loyalty planning and customer retention strategy.

### Objective 2: Evaluate Revenue Drivers

The second objective was to analyse revenue by film category, rental volume, average payment, and rental rate. This helps identify which categories contribute most to business performance and which categories may require promotional support, pricing review, or inventory adjustment.

### Objective 3: Assess Inventory and Store Efficiency

The third objective was to compare store performance using revenue, rental count, customer base, inventory size, revenue per inventory item, and rentals per inventory item. This helps management understand whether each store is using its inventory effectively.

### Objective 4: Develop an Innovation or Custom Analysis

The fourth objective was to create a simple recommendation strategy based on high-performing film categories. This provides a practical starting point for targeted recommendations and promotional campaigns.

---

## 3. Methodology and Data Pipeline

The project followed a structured analytics workflow.

First, the PostgreSQL DVD Rental database was restored and managed using Docker and pgAdmin. A Python validation script connected to the database using SQLAlchemy and psycopg2. The script listed available tables, validated critical tables, generated row counts, and checked basic data quality issues such as missing values and duplicate rows.

Second, exploratory data analysis was conducted using Pandas, Matplotlib, and Seaborn. The exploration stage inspected schemas, data types, missing values, descriptive statistics, and outliers. Initial visualizations were generated for monthly revenue, film category revenue, top customers by revenue, and rentals by store.

Third, merged datasets were created to support deeper business analysis. These datasets included customer revenue, film category revenue, store performance, and inventory turnover. Join keys and join types were documented to ensure transparency. For example, customer revenue analysis joined `customer.customer_id` to `payment.customer_id`, while film category revenue analysis followed the path from payment to rental, inventory, film, film category, and category.

During store performance modelling, customer counts, inventory counts, rental counts, and revenue were calculated separately before being joined to the store table. This was done to avoid revenue overcounting caused by multiple one-to-many joins.

Finally, advanced analysis was conducted and a Streamlit dashboard was developed to communicate the results visually.

---

## 4. Key Findings

### 4.1 Customer Analytics

The customer base was segmented into three value groups: low value, medium value, and high value. The high-value segment contained **200 customers** and generated **26,009.63** in revenue, with an average revenue of **130.05** per customer. The medium-value segment contained **199 customers** and generated **19,972.79**, while the low-value segment contained **200 customers** and generated **15,329.62**.

This shows that the high-value segment contributes significantly more revenue than the low-value segment even though both groups contain almost the same number of customers. The average payment also rises across the segments, from **3.94** for low-value customers to **4.47** for high-value customers.

Churn risk was estimated using days since last payment. The results showed **598 customers** in the low-risk group, **1 customer** in the medium-risk group, and **0 customers** in the high-risk group. This suggests that, based on payment recency, the customer base appears largely active within the available dataset.

**Business implication:**
The company should protect high-value customers through loyalty benefits, personalized offers, and targeted communication. Since most customers fall into the low-risk churn category, management should focus less on broad reactivation and more on strengthening repeat engagement among already active customers.

---

### 4.2 Revenue Optimization

Film category revenue analysis showed clear differences across categories. The top five categories by revenue were:

1. **Sports:** 4,892.19 from 1,179 rentals
2. **Sci-Fi:** 4,336.01 from 1,101 rentals
3. **Animation:** 4,245.31 from 1,166 rentals
4. **Drama:** 4,118.46 from 1,060 rentals
5. **Comedy:** 4,002.48 from 941 rentals

Sports was the strongest category by revenue and rental volume. It also had the highest average payment among the top categories at **4.52**. This suggests that Sports titles are both popular and financially valuable.

The lowest five categories by revenue were:

1. **Horror:** 3,401.27 from 846 rentals
2. **Classics:** 3,353.38 from 939 rentals
3. **Children:** 3,309.39 from 945 rentals
4. **Travel:** 3,227.36 from 837 rentals
5. **Music:** 3,071.52 from 830 rentals

Music was the weakest category by total revenue, while Travel also showed relatively low revenue despite having the highest average rental rate among the lowest five categories at **3.24**. This may suggest that demand, not just price, is affecting performance.

**Business implication:**
The company should promote strong categories such as Sports, Sci-Fi, Animation, Drama, and Comedy more aggressively. Low-performing categories such as Music, Travel, and Children should be reviewed for demand, visibility, pricing, and inventory allocation.

---

### 4.3 Inventory and Operations

Store performance was fairly balanced. Store 1 had **326 customers**, **2,270 inventory items**, and generated **30,628.91** in revenue. Store 2 had **273 customers**, **2,311 inventory items**, and generated **30,683.13** in revenue.

Although Store 1 had more customers, Store 2 generated slightly higher revenue. Store 1 recorded revenue per inventory item of **13.49**, while Store 2 recorded **13.28**. Store 1 had **3.49 rentals per inventory item**, while Store 2 had **3.51 rentals per inventory item**.

This suggests that both stores perform at similar levels, but Store 2 appears to generate slightly more revenue with fewer customers. Store 1, however, generates slightly higher revenue per inventory item.

Slow-moving inventory analysis identified film copies with very low rental counts. One inventory item, **Academy Dinosaur**, recorded **0 rentals** and **0.00** revenue. Other slow-moving titles included **Mixed Doors**, **Musketeers Wait**, **Galaxy Sweethearts**, and **Rocky War**, each recording only **1 rental**.

**Business implication:**
Management should monitor inventory turnover regularly. Slow-moving films should be reviewed for promotion, relocation, or reduced duplication. Store-level inventory allocation should also be reviewed because the two stores show slightly different customer and inventory efficiency patterns.

---

### 4.4 Recommendation and Custom Analysis

A simple category-based recommendation strategy was developed using total revenue and total rentals. The high-priority recommendation categories were:

* Sports
* Sci-Fi
* Animation
* Drama
* Comedy

These categories have strong revenue performance and should be used as the foundation for recommendations and promotional campaigns. For example, if a customer rents from Sports or Sci-Fi, the company can recommend other high-performing titles from the same category.

Medium-priority categories included New, Action, and Foreign. These categories still performed well and can support secondary promotional campaigns.

**Business implication:**
The company can begin improving recommendations without immediately implementing a complex machine learning system. A simple category-based recommendation rule can be implemented immediately and later improved with customer-level rental history.

---

## 5. Recommendations

### Recommendation 1: Protect High-Value Customers

The high-value customer segment generated **26,009.63**, which is about **10,680.01** more than the low-value segment. Management should provide loyalty benefits, personalized offers, and early access to popular titles for this group.

### Recommendation 2: Increase Engagement Among Active Customers

Since **598 customers** were classified as low churn risk, the customer base appears largely active. The company should focus on increasing rental frequency rather than only trying to recover inactive customers.

### Recommendation 3: Promote High-Performing Categories

Sports, Sci-Fi, Animation, Drama, and Comedy should be prioritized in promotions because they are the strongest revenue categories. Sports alone generated **4,892.19** from **1,179 rentals**.

### Recommendation 4: Review Low-Performing Categories

Music, Travel, Children, Classics, and Horror should be reviewed. Music generated the lowest revenue at **3,071.52**, while Travel generated **3,227.36** despite having a relatively high average rental rate. Management should investigate whether these categories need better promotion, revised pricing, or lower inventory allocation.

### Recommendation 5: Improve Store-Level Inventory Decisions

Store 1 and Store 2 generated similar revenue, but their customer and inventory profiles differ. Store 2 generated slightly higher total revenue despite having fewer customers, while Store 1 had slightly better revenue per inventory item. Management should study the inventory mix and customer behaviour at both stores to improve stock allocation.

### Recommendation 6: Act on Slow-Moving Inventory

Films with zero or very low rental counts should be reviewed. **Academy Dinosaur** recorded no rentals and no revenue in the inventory analysis, while several other titles recorded only one rental. These titles may need promotion, relocation, or reduced duplicate copies.

### Recommendation 7: Start with a Simple Recommendation Engine

A category-based recommendation approach should be implemented using high-performing categories. This can be done before investing in advanced machine learning. The first version can recommend popular films from the same category a customer has already rented.

---

## 6. Ethical Considerations and Data Limitations

The analysis uses customer, payment, rental, and inventory data. Although this project uses a sample database, the same ethical principles apply to real business data. Customer names and emails should be handled responsibly and should not be exposed unnecessarily in public dashboards or reports.

There are also limitations. The data represents historical transactions and may not fully reflect current customer preferences. The database does not include external factors such as competitor activity, streaming service adoption, customer satisfaction, marketing campaigns, or local economic conditions.

Churn risk was estimated using payment recency, not customer feedback or subscription cancellation behaviour. The recommendation method is also simple and category-based. It is useful as a starting point, but a more advanced system would require customer-level rental history, genre preferences, time patterns, and possibly collaborative filtering.

---

## 7. Technical Appendix

### Tools Used

* Docker and Docker Compose for service setup
* PostgreSQL as the database system
* pgAdmin for database management
* Python for data processing and analysis
* Pandas for data manipulation
* SQLAlchemy and psycopg2 for database connectivity
* Matplotlib and Seaborn for visualization
* Streamlit for dashboard development

### Main Project Scripts

* `1_setup_validate.py`: connects to PostgreSQL, lists tables, validates critical tables, counts rows, checks missing values and duplicates, and exports validation outputs.
* `2_data_exploration.py`: performs schema inspection, missing value checks, descriptive statistics, outlier checks, and initial visualizations.
* `3_data_relationships.py`: creates merged datasets for customer revenue, category revenue, store performance, and inventory turnover.
* `4_analysis.py`: performs customer segmentation, churn risk analysis, revenue optimization, pricing insight, inventory analysis, and recommendation candidate analysis.
* `5_dashboard.py`: presents the insights through a Streamlit dashboard.

### Output Folders

* `tables/`: stores summary tables and analysis outputs.
* `merges/`: stores merged analysis-ready datasets.
* `results/`: stores generated visualizations.
* `exports/`: stores text reports and business summaries.

### Key Assumptions

1. Revenue is measured using the `payment.amount` field.
2. Customer value is estimated using total payment amount.
3. Rental activity is measured using distinct rental count.
4. Store performance is compared using customers, rentals, inventory, and revenue.
5. Churn risk is estimated using days since last payment.
6. Recommendation priority is based on category revenue and rental activity.
7. Store performance calculations use grouped subqueries to avoid revenue overcounting.

---

## 8. Conclusion

The DVD Rental analysis shows how a structured data analytics workflow can support business decision-making. The project validated the database, explored the data, created merged datasets, performed advanced analysis, and presented the findings in a dashboard.

The analysis shows that high-value customers generate substantially more revenue than low-value customers, Sports is the strongest film category, Music is the weakest category by revenue, and both stores perform at similar revenue levels. The business should focus on protecting high-value customers, promoting strong categories, reviewing weak categories, improving inventory decisions, and starting with a simple recommendation system.

These actions can help the company improve customer engagement, revenue performance, and operational efficiency.
