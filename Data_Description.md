# Data Description

## DVD Rental Big Data Management Project

## 1. Dataset Overview

The project uses the PostgreSQL DVD Rental sample database. The database represents the operations of a DVD rental business and contains information about customers, films, rentals, payments, inventory, staff, stores, and film categories.

The data supports business analysis across customer behaviour, revenue performance, store operations, inventory efficiency, and recommendation opportunities.

## 2. Main Tables Used

### customer

The `customer` table contains customer information.

Important fields include:

* `customer_id`: unique customer identifier
* `store_id`: store linked to the customer
* `first_name`: customer first name
* `last_name`: customer last name
* `email`: customer email address
* `active`: customer activity status
* `create_date`: date the customer record was created

This table was used for customer segmentation, customer value analysis, and churn risk analysis.

---

### payment

The `payment` table contains customer payment transactions.

Important fields include:

* `payment_id`: unique payment identifier
* `customer_id`: customer linked to the payment
* `staff_id`: staff member who handled the transaction
* `rental_id`: rental linked to the payment
* `amount`: payment amount
* `payment_date`: date and time of payment

This table was used as the main source for revenue analysis.

---

### rental

The `rental` table contains rental transaction records.

Important fields include:

* `rental_id`: unique rental identifier
* `rental_date`: date and time the rental occurred
* `inventory_id`: inventory item rented
* `customer_id`: customer who rented the item
* `return_date`: date and time the item was returned
* `staff_id`: staff member involved in the rental

This table was used to analyse rental activity, customer behaviour, and inventory movement.

---

### film

The `film` table contains film information.

Important fields include:

* `film_id`: unique film identifier
* `title`: film title
* `description`: film description
* `release_year`: film release year
* `language_id`: film language
* `rental_duration`: rental duration
* `rental_rate`: rental price
* `length`: film length
* `replacement_cost`: replacement cost
* `rating`: film rating
* `special_features`: film feature list

This table was used for film-level analysis, pricing insight, and inventory analysis.

---

### category

The `category` table contains film category information.

Important fields include:

* `category_id`: unique category identifier
* `name`: category name

This table was used to analyse revenue and rental activity by film category.

---

### film_category

The `film_category` table links films to categories.

Important fields include:

* `film_id`: film identifier
* `category_id`: category identifier

This table was used as a bridge between the `film` and `category` tables.

---

### inventory

The `inventory` table contains physical film copy records.

Important fields include:

* `inventory_id`: unique inventory item identifier
* `film_id`: film linked to the inventory item
* `store_id`: store where the item is located

This table was used for inventory turnover, store performance, and slow-moving inventory analysis.

---

### store

The `store` table contains store-level information.

Important fields include:

* `store_id`: unique store identifier
* `manager_staff_id`: manager assigned to the store
* `address_id`: store address identifier

This table was used for store performance analysis.

---

### staff

The `staff` table contains staff information.

Important fields include:

* `staff_id`: unique staff identifier
* `first_name`: staff first name
* `last_name`: staff last name
* `address_id`: staff address identifier
* `store_id`: store where the staff member works
* `active`: staff activity status
* `username`: staff username

This table supports store and transaction context.

---

## 3. Key Relationships Used

### Customer to Payment

```text
customer.customer_id = payment.customer_id
```

This relationship was used to calculate customer revenue, average payment, and last payment date.

### Payment to Rental

```text
payment.rental_id = rental.rental_id
```

This relationship was used to connect revenue to rental activity.

### Rental to Inventory

```text
rental.inventory_id = inventory.inventory_id
```

This relationship was used to connect rentals to specific film copies.

### Inventory to Film

```text
inventory.film_id = film.film_id
```

This relationship was used to identify which films were rented.

### Film to Category

```text
film.film_id = film_category.film_id
film_category.category_id = category.category_id
```

This relationship was used to analyse revenue and rentals by film category.

### Store to Inventory

```text
store.store_id = inventory.store_id
```

This relationship was used to compare store-level inventory and rental performance.

### Store to Customer

```text
store.store_id = customer.store_id
```

This relationship was used to compare customer distribution across stores.

---

## 4. Merged Datasets Created

### customer_revenue_dataset.csv

This dataset combines customer and payment data.

Main purpose:

* customer value analysis
* customer segmentation
* payment frequency analysis
* churn risk analysis

Main fields:

* `customer_id`
* `first_name`
* `last_name`
* `email`
* `active`
* `store_id`
* `total_payments`
* `total_revenue`
* `average_payment`
* `last_payment_date`

---

### film_category_revenue_dataset.csv

This dataset combines film, category, inventory, rental, and payment data.

Main purpose:

* category revenue analysis
* rental activity by category
* pricing insight
* recommendation candidate analysis

Main fields:

* `film_id`
* `title`
* `rating`
* `rental_rate`
* `replacement_cost`
* `length`
* `category`
* `total_rentals`
* `total_revenue`
* `average_payment`

---

### store_performance_dataset.csv

This dataset compares store-level performance.

Main purpose:

* store revenue comparison
* store customer comparison
* store inventory comparison
* revenue per inventory item
* rentals per inventory item

Main fields:

* `store_id`
* `total_customers`
* `total_inventory_items`
* `total_rentals`
* `total_revenue`

---

### inventory_turnover_dataset.csv

This dataset measures inventory movement.

Main purpose:

* inventory turnover analysis
* slow-moving inventory identification
* film-level rental performance
* store-level stock review

Main fields:

* `inventory_id`
* `store_id`
* `film_id`
* `title`
* `rating`
* `rental_rate`
* `category`
* `rental_count`
* `total_revenue`
* `last_rental_date`

---

## 5. Data Quality Checks

The database validation and exploration scripts checked:

* available tables
* critical table presence
* row counts
* missing values
* duplicate rows
* schema and data types
* descriptive statistics
* simple outliers using the IQR method

The validation confirmed that the critical DVD Rental tables were available for analysis.

## 6. Analytical Variables

### Revenue

Revenue was measured using:

```text
payment.amount
```

### Customer Value

Customer value was estimated using:

```text
SUM(payment.amount) per customer
```

### Rental Activity

Rental activity was measured using:

```text
COUNT(rental.rental_id)
```

### Churn Risk

Churn risk was estimated using:

```text
days since last payment
```

### Inventory Turnover

Inventory turnover was measured using:

```text
rental count per inventory item
```

### Store Performance

Store performance was assessed using:

* total customers
* total inventory items
* total rentals
* total revenue
* revenue per inventory item
* rentals per inventory item

## 7. Limitations

The data is historical and may not fully represent current customer behaviour. It does not include customer satisfaction, competitor activity, marketing campaigns, streaming service impact, or demographic information.

Churn risk was estimated from payment recency rather than direct cancellation or feedback data. The recommendation method was also simple and category-based rather than a full machine learning recommendation engine.

## 8. Ethical Considerations

The database contains customer names and emails. In a real business environment, such information should be handled carefully and should not be exposed unnecessarily in public reports or dashboards.

Analysis outputs should focus on aggregated insights rather than individual customer identities unless there is a clear business reason and proper data governance controls.
