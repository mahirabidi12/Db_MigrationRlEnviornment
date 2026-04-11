TASK_ID = "hard_shoplocal_formulas"
DIFFICULTY = "hard"
TIMEOUT_SECONDS = 300
MAX_STEPS = 8

TASK_DESCRIPTION = """
ShopLocal → NexGenMart E-Commerce Migration
==============================================

ShopLocal's legacy database (7 tables, sl_ prefix, email/SKU/category-name refs, zero FKs)
must be migrated into 9 enterprise tables. Self-referential category parent resolved by name.
Address extraction from customers. Computed product_performance using GROUP BY across orders
and reviews. All 7 legacy tables must be dropped.

────────────────────────────────────────────────────────────────
 Table 1 / 9 : users
────────────────────────────────────────────────────────────────
4 rows from sl_customers. id INTEGER PRIMARY KEY from cid, first_name TEXT NOT NULL from cust_fname, last_name TEXT NOT NULL from cust_lname, email TEXT NOT NULL UNIQUE from cust_email, phone TEXT (nullable) from cust_phone, registered_at TEXT NOT NULL from cust_joined, is_active INTEGER NOT NULL DEFAULT 1 from cust_is_active.

────────────────────────────────────────────────────────────────
 Table 2 / 9 : user_addresses
────────────────────────────────────────────────────────────────
4 rows extracted from sl_customers. id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL FK→users(id) (same as cid), address_line TEXT NOT NULL from cust_addr_line, city TEXT NOT NULL from cust_addr_city, state TEXT NOT NULL from cust_addr_state, zip_code TEXT NOT NULL from cust_addr_zip, address_type TEXT NOT NULL DEFAULT 'home'.

────────────────────────────────────────────────────────────────
 Table 3 / 9 : categories
────────────────────────────────────────────────────────────────
4 rows from sl_categories. id INTEGER PRIMARY KEY from catid, name TEXT NOT NULL UNIQUE from cat_name, parent_id INTEGER FK→categories(id) — SELF-REFERENTIAL. Resolve by joining cat_parent_name against categories.name. NULL if no parent. Insert parents first.

────────────────────────────────────────────────────────────────
 Table 4 / 9 : products
────────────────────────────────────────────────────────────────
4 rows from sl_products. id INTEGER PRIMARY KEY from pid, sku TEXT NOT NULL UNIQUE from prod_sku, name TEXT NOT NULL from prod_name, category_id INTEGER NOT NULL FK→categories(id) resolved by joining prod_cat_name against categories.name, base_price REAL NOT NULL from prod_price, created_at TEXT NOT NULL from prod_created. Create index idx_products_category on category_id.

────────────────────────────────────────────────────────────────
 Table 5 / 9 : orders
────────────────────────────────────────────────────────────────
4 rows from sl_orders. id INTEGER PRIMARY KEY from oid, user_id INTEGER NOT NULL FK→users(id) resolved by joining ord_cust_email against users.email, order_date TEXT NOT NULL from ord_date, status TEXT NOT NULL from ord_status, total_amount REAL NOT NULL from ord_total. Create index idx_orders_user on user_id.

────────────────────────────────────────────────────────────────
 Table 6 / 9 : order_items
────────────────────────────────────────────────────────────────
6 rows from sl_order_items. id INTEGER PRIMARY KEY from oiid, order_id INTEGER NOT NULL FK→orders(id) from oi_order_id, product_id INTEGER NOT NULL FK→products(id) resolved by joining oi_prod_sku against products.sku, quantity INTEGER NOT NULL from oi_quantity, unit_price REAL NOT NULL from oi_unit_price, subtotal REAL NOT NULL computed as oi_quantity * oi_unit_price.

────────────────────────────────────────────────────────────────
 Table 7 / 9 : product_reviews
────────────────────────────────────────────────────────────────
3 rows from sl_reviews. id INTEGER PRIMARY KEY from rvid, user_id INTEGER NOT NULL FK→users(id) resolved by joining rv_cust_email against users.email, product_id INTEGER NOT NULL FK→products(id) resolved by joining rv_prod_sku against products.sku, rating INTEGER NOT NULL from rv_rating, review_text TEXT (nullable) from rv_text, review_date TEXT NOT NULL from rv_date.

────────────────────────────────────────────────────────────────
 Table 8 / 9 : discount_codes
────────────────────────────────────────────────────────────────
2 rows from sl_coupons. id INTEGER PRIMARY KEY from cpid, code TEXT NOT NULL UNIQUE from cp_code, discount_amount REAL NOT NULL from cp_discount, discount_type TEXT NOT NULL from cp_type, expires_at TEXT (nullable) from cp_expires.

────────────────────────────────────────────────────────────────
 Table 9 / 11 : product_performance
────────────────────────────────────────────────────────────────
4 rows — one per product. id INTEGER PRIMARY KEY, product_id INTEGER NOT NULL UNIQUE FK→products(id), total_orders INTEGER NOT NULL DEFAULT 0 computed as COUNT(DISTINCT order_items.order_id) for this product, total_revenue REAL NOT NULL DEFAULT 0.0 computed as SUM(order_items.subtotal) for this product, avg_rating REAL computed as ROUND(AVG(product_reviews.rating), 2) — NULL if no reviews.

────────────────────────────────────────────────────────────────
 Table 10 / 11 : discount_usage
────────────────────────────────────────────────────────────────
3 rows from sl_coupon_uses. id INTEGER PRIMARY KEY from cuid, discount_id INTEGER NOT NULL FK→discount_codes(id) resolved by joining cu_coupon_code against discount_codes.code, user_id INTEGER NOT NULL FK→users(id) resolved by joining cu_cust_email against users.email, used_at TEXT NOT NULL from cu_used_date, order_id INTEGER NOT NULL FK→orders(id) from cu_order_id.

────────────────────────────────────────────────────────────────
 Table 11 / 11 : daily_revenue
────────────────────────────────────────────────────────────────
4 rows — one per distinct order_date. id INTEGER PRIMARY KEY, order_date TEXT NOT NULL UNIQUE, total_orders INTEGER NOT NULL computed as COUNT(*) of orders on that date, total_revenue REAL NOT NULL computed as SUM(orders.total_amount) on that date.

────────────────────────────────────────────────────────────────
 DROP ALL LEGACY TABLES: sl_customers, sl_categories, sl_products, sl_orders, sl_order_items, sl_reviews, sl_coupons, sl_coupon_uses.
"""

INITIAL_SQL = """
CREATE TABLE sl_customers (
    cid INTEGER PRIMARY KEY,
    cust_fname TEXT NOT NULL,
    cust_lname TEXT NOT NULL,
    cust_email TEXT NOT NULL,
    cust_phone TEXT,
    cust_addr_line TEXT,
    cust_addr_city TEXT,
    cust_addr_state TEXT,
    cust_addr_zip TEXT,
    cust_joined TEXT,
    cust_is_active INTEGER DEFAULT 1
);

INSERT INTO sl_customers VALUES (1, 'Alice', 'Chen', 'alice@shop.com', '555-0101', '123 Maple St', 'Portland', 'OR', '97201', '2022-01-10', 1);
INSERT INTO sl_customers VALUES (2, 'Bob', 'Rivera', 'bob@shop.com', '555-0102', '456 Oak Ave', 'Austin', 'TX', '78701', '2022-03-05', 1);
INSERT INTO sl_customers VALUES (3, 'Carol', 'Zhang', 'carol@shop.com', '555-0103', '789 Pine Rd', 'Seattle', 'WA', '98101', '2022-06-18', 1);
INSERT INTO sl_customers VALUES (4, 'Dave', 'Wilson', 'dave@shop.com', '555-0104', '321 Elm Blvd', 'Denver', 'CO', '80201', '2023-01-12', 1);

CREATE TABLE sl_categories (
    catid INTEGER PRIMARY KEY,
    cat_name TEXT NOT NULL,
    cat_parent_name TEXT
);

INSERT INTO sl_categories VALUES (1, 'Electronics', NULL);
INSERT INTO sl_categories VALUES (2, 'Clothing', NULL);
INSERT INTO sl_categories VALUES (3, 'Phones', 'Electronics');
INSERT INTO sl_categories VALUES (4, 'Laptops', 'Electronics');

CREATE TABLE sl_products (
    pid INTEGER PRIMARY KEY,
    prod_sku TEXT NOT NULL,
    prod_name TEXT NOT NULL,
    prod_cat_name TEXT NOT NULL,
    prod_price REAL NOT NULL,
    prod_created TEXT
);

INSERT INTO sl_products VALUES (1, 'SKU-PHONE-001', 'SmartPhone X', 'Phones', 899.99, '2023-01-15');
INSERT INTO sl_products VALUES (2, 'SKU-LAPTOP-002', 'ProBook 15', 'Laptops', 1299.99, '2023-02-20');
INSERT INTO sl_products VALUES (3, 'SKU-TSHIRT-003', 'Cotton Tee', 'Clothing', 29.99, '2023-03-10');
INSERT INTO sl_products VALUES (4, 'SKU-JEANS-004', 'Slim Jeans', 'Clothing', 69.99, '2023-04-01');

CREATE TABLE sl_orders (
    oid INTEGER PRIMARY KEY,
    ord_cust_email TEXT NOT NULL,
    ord_date TEXT NOT NULL,
    ord_status TEXT DEFAULT 'pending',
    ord_total REAL NOT NULL
);

INSERT INTO sl_orders VALUES (1001, 'alice@shop.com', '2024-01-10', 'delivered', 929.98);
INSERT INTO sl_orders VALUES (1002, 'bob@shop.com', '2024-01-15', 'delivered', 1299.99);
INSERT INTO sl_orders VALUES (1003, 'carol@shop.com', '2024-02-01', 'delivered', 99.97);
INSERT INTO sl_orders VALUES (1004, 'dave@shop.com', '2024-03-05', 'processing', 69.99);

CREATE TABLE sl_order_items (
    oiid INTEGER PRIMARY KEY,
    oi_order_id INTEGER NOT NULL,
    oi_prod_sku TEXT NOT NULL,
    oi_quantity INTEGER NOT NULL,
    oi_unit_price REAL NOT NULL
);

INSERT INTO sl_order_items VALUES (1, 1001, 'SKU-PHONE-001', 1, 899.99);
INSERT INTO sl_order_items VALUES (2, 1001, 'SKU-TSHIRT-003', 1, 29.99);
INSERT INTO sl_order_items VALUES (3, 1002, 'SKU-LAPTOP-002', 1, 1299.99);
INSERT INTO sl_order_items VALUES (4, 1003, 'SKU-TSHIRT-003', 2, 29.99);
INSERT INTO sl_order_items VALUES (5, 1003, 'SKU-JEANS-004', 1, 69.99);
INSERT INTO sl_order_items VALUES (6, 1004, 'SKU-JEANS-004', 1, 69.99);

CREATE TABLE sl_reviews (
    rvid INTEGER PRIMARY KEY,
    rv_cust_email TEXT NOT NULL,
    rv_prod_sku TEXT NOT NULL,
    rv_rating INTEGER NOT NULL,
    rv_text TEXT,
    rv_date TEXT
);

INSERT INTO sl_reviews VALUES (1, 'alice@shop.com', 'SKU-PHONE-001', 5, 'Excellent phone!', '2024-02-01');
INSERT INTO sl_reviews VALUES (2, 'bob@shop.com', 'SKU-LAPTOP-002', 4, 'Great performance', '2024-02-15');
INSERT INTO sl_reviews VALUES (3, 'carol@shop.com', 'SKU-TSHIRT-003', 3, 'Decent quality', '2024-03-01');

CREATE TABLE sl_coupons (
    cpid INTEGER PRIMARY KEY,
    cp_code TEXT NOT NULL,
    cp_discount REAL NOT NULL,
    cp_type TEXT NOT NULL,
    cp_expires TEXT
);

INSERT INTO sl_coupons VALUES (1, 'SAVE10', 10.0, 'percentage', '2024-12-31');
INSERT INTO sl_coupons VALUES (2, 'FLAT20', 20.0, 'fixed', '2024-06-30');

CREATE TABLE sl_coupon_uses (
    cuid INTEGER PRIMARY KEY,
    cu_coupon_code TEXT NOT NULL,
    cu_cust_email TEXT NOT NULL,
    cu_order_id INTEGER NOT NULL,
    cu_used_date TEXT NOT NULL
);

INSERT INTO sl_coupon_uses VALUES (1, 'SAVE10', 'alice@shop.com', 1001, '2024-01-10');
INSERT INTO sl_coupon_uses VALUES (2, 'FLAT20', 'carol@shop.com', 1003, '2024-02-01');
INSERT INTO sl_coupon_uses VALUES (3, 'SAVE10', 'dave@shop.com', 1004, '2024-03-05');
"""

TARGET_SQL = """
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT,
    registered_at TEXT NOT NULL,
    is_active INTEGER NOT NULL DEFAULT 1
);

INSERT INTO users VALUES (1, 'Alice', 'Chen', 'alice@shop.com', '555-0101', '2022-01-10', 1);
INSERT INTO users VALUES (2, 'Bob', 'Rivera', 'bob@shop.com', '555-0102', '2022-03-05', 1);
INSERT INTO users VALUES (3, 'Carol', 'Zhang', 'carol@shop.com', '555-0103', '2022-06-18', 1);
INSERT INTO users VALUES (4, 'Dave', 'Wilson', 'dave@shop.com', '555-0104', '2023-01-12', 1);

CREATE TABLE user_addresses (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    address_line TEXT NOT NULL,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    zip_code TEXT NOT NULL,
    address_type TEXT NOT NULL DEFAULT 'home'
);

INSERT INTO user_addresses VALUES (1, 1, '123 Maple St', 'Portland', 'OR', '97201', 'home');
INSERT INTO user_addresses VALUES (2, 2, '456 Oak Ave', 'Austin', 'TX', '78701', 'home');
INSERT INTO user_addresses VALUES (3, 3, '789 Pine Rd', 'Seattle', 'WA', '98101', 'home');
INSERT INTO user_addresses VALUES (4, 4, '321 Elm Blvd', 'Denver', 'CO', '80201', 'home');

CREATE TABLE categories (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    parent_id INTEGER REFERENCES categories(id)
);

INSERT INTO categories VALUES (1, 'Electronics', NULL);
INSERT INTO categories VALUES (2, 'Clothing', NULL);
INSERT INTO categories VALUES (3, 'Phones', 1);
INSERT INTO categories VALUES (4, 'Laptops', 1);

CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    sku TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    category_id INTEGER NOT NULL REFERENCES categories(id),
    base_price REAL NOT NULL,
    created_at TEXT NOT NULL
);
CREATE INDEX idx_products_category ON products(category_id);

INSERT INTO products VALUES (1, 'SKU-PHONE-001', 'SmartPhone X', 3, 899.99, '2023-01-15');
INSERT INTO products VALUES (2, 'SKU-LAPTOP-002', 'ProBook 15', 4, 1299.99, '2023-02-20');
INSERT INTO products VALUES (3, 'SKU-TSHIRT-003', 'Cotton Tee', 2, 29.99, '2023-03-10');
INSERT INTO products VALUES (4, 'SKU-JEANS-004', 'Slim Jeans', 2, 69.99, '2023-04-01');

CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    order_date TEXT NOT NULL,
    status TEXT NOT NULL,
    total_amount REAL NOT NULL
);
CREATE INDEX idx_orders_user ON orders(user_id);

INSERT INTO orders VALUES (1001, 1, '2024-01-10', 'delivered', 929.98);
INSERT INTO orders VALUES (1002, 2, '2024-01-15', 'delivered', 1299.99);
INSERT INTO orders VALUES (1003, 3, '2024-02-01', 'delivered', 99.97);
INSERT INTO orders VALUES (1004, 4, '2024-03-05', 'processing', 69.99);

CREATE TABLE order_items (
    id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id),
    product_id INTEGER NOT NULL REFERENCES products(id),
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    subtotal REAL NOT NULL
);

INSERT INTO order_items VALUES (1, 1001, 1, 1, 899.99, 899.99);
INSERT INTO order_items VALUES (2, 1001, 3, 1, 29.99, 29.99);
INSERT INTO order_items VALUES (3, 1002, 2, 1, 1299.99, 1299.99);
INSERT INTO order_items VALUES (4, 1003, 3, 2, 29.99, 59.98);
INSERT INTO order_items VALUES (5, 1003, 4, 1, 69.99, 69.99);
INSERT INTO order_items VALUES (6, 1004, 4, 1, 69.99, 69.99);

CREATE TABLE product_reviews (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    product_id INTEGER NOT NULL REFERENCES products(id),
    rating INTEGER NOT NULL,
    review_text TEXT,
    review_date TEXT NOT NULL
);

INSERT INTO product_reviews VALUES (1, 1, 1, 5, 'Excellent phone!', '2024-02-01');
INSERT INTO product_reviews VALUES (2, 2, 2, 4, 'Great performance', '2024-02-15');
INSERT INTO product_reviews VALUES (3, 3, 3, 3, 'Decent quality', '2024-03-01');

CREATE TABLE discount_codes (
    id INTEGER PRIMARY KEY,
    code TEXT NOT NULL UNIQUE,
    discount_amount REAL NOT NULL,
    discount_type TEXT NOT NULL,
    expires_at TEXT
);

INSERT INTO discount_codes VALUES (1, 'SAVE10', 10.0, 'percentage', '2024-12-31');
INSERT INTO discount_codes VALUES (2, 'FLAT20', 20.0, 'fixed', '2024-06-30');

CREATE TABLE product_performance (
    id INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL UNIQUE REFERENCES products(id),
    total_orders INTEGER NOT NULL DEFAULT 0,
    total_revenue REAL NOT NULL DEFAULT 0.0,
    avg_rating REAL
);

INSERT INTO product_performance VALUES (1, 1, 1, 899.99, 5.0);
INSERT INTO product_performance VALUES (2, 2, 1, 1299.99, 4.0);
INSERT INTO product_performance VALUES (3, 3, 2, 89.97, 3.0);
INSERT INTO product_performance VALUES (4, 4, 2, 139.98, NULL);

CREATE TABLE discount_usage (
    id INTEGER PRIMARY KEY,
    discount_id INTEGER NOT NULL REFERENCES discount_codes(id),
    user_id INTEGER NOT NULL REFERENCES users(id),
    used_at TEXT NOT NULL,
    order_id INTEGER NOT NULL REFERENCES orders(id)
);

INSERT INTO discount_usage VALUES (1, 1, 1, '2024-01-10', 1001);
INSERT INTO discount_usage VALUES (2, 2, 3, '2024-02-01', 1003);
INSERT INTO discount_usage VALUES (3, 1, 4, '2024-03-05', 1004);

CREATE TABLE daily_revenue (
    id INTEGER PRIMARY KEY,
    order_date TEXT NOT NULL UNIQUE,
    total_orders INTEGER NOT NULL,
    total_revenue REAL NOT NULL
);

INSERT INTO daily_revenue VALUES (1, '2024-01-10', 1, 929.98);
INSERT INTO daily_revenue VALUES (2, '2024-01-15', 1, 1299.99);
INSERT INTO daily_revenue VALUES (3, '2024-02-01', 1, 99.97);
INSERT INTO daily_revenue VALUES (4, '2024-03-05', 1, 69.99);
"""
