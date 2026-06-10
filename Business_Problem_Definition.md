# Business Problem Definition

## 1. Executive Summary

This project analyses the PostgreSQL DVD Rental database for a mid-sized DVD rental business seeking to improve customer value, revenue performance, inventory usage, and store efficiency. The business challenge is to understand which customers generate the most revenue, which film categories drive performance, how efficiently stores use inventory, and how simple recommendation strategies can improve promotional targeting. Four analytical objectives guide the project. First, customer analytics is used to segment customers by value and assess churn risk, supporting retention decisions. Second, revenue optimization examines category performance, rental activity, and pricing patterns to identify strong and weak revenue areas. Third, inventory and operations analysis compares store performance and identifies slow-moving stock to improve resource allocation. Fourth, a category-based recommendation approach supports innovation by suggesting promotional priorities. The analysis follows a reproducible pipeline involving Docker-based database setup, PostgreSQL validation, exploratory data analysis, merged dataset creation, business analysis, visualizations, dashboard development, and executive reporting.

---

## 2. Analytical Objectives

### Objective 1: Customer Intelligence

To identify customer value groups, payment behaviour, and churn risk so that the business can prioritize customer retention and engagement strategies.

### Objective 2: Revenue Optimization

To determine which film categories and pricing patterns contribute most to revenue so that management can improve promotions and revenue planning.

### Objective 3: Inventory and Operations

To assess store performance, inventory turnover, and slow-moving stock so that the company can improve operational efficiency and stock allocation.

### Objective 4: Innovation or Custom Analysis

To develop a simple category-based recommendation strategy that can support promotional targeting and future recommendation system development.

---

## 3. Analytical Questions

### Customer Intelligence

1. Which customer segments contribute the most revenue to the business?
2. Which customers or customer groups show signs of churn risk based on payment recency?

### Revenue Optimization

3. Which film categories generate the highest and lowest revenue?
4. How do rental activity, average payment, and rental rate relate to category revenue performance?

### Inventory and Operations

5. Which store performs better in terms of revenue, rentals, customers, and inventory efficiency?
6. Which inventory items are slow-moving and may require promotion, relocation, or reduced stock levels?

### Innovation or Custom Analysis

7. Which film categories should be prioritized for recommendations and promotional campaigns?
8. How can a simple category-based recommendation approach support future customer targeting?

---

## 4. Dataset Note

The question scenario refers to three physical stores. However, the restored PostgreSQL DVD Rental sample database used for this project contains two store records. Therefore, store-level analysis is based on the two stores available in the database.
