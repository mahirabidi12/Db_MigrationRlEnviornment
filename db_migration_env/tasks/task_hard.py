"""Task 3 (Hard): Full-Stack E-Commerce SaaS Platform Schema Overhaul.

Initial: 20 heavily denormalized tables simulating a legacy e-commerce platform
where relationships are stored via email/name/sku/code text references.

Target: 16 fully normalized tables with proper integer FK references.

Migration requirements:
  - Replace ALL email/name/sku/code references with integer FK IDs
  - Normalize customer_addresses, products, product_images, categories,
    inventory, orders, order_items, payments, reviews, coupons, coupon_usage,
    wishlists, returns, purchase_orders, notifications
  - Merge shipping table into orders (as shipping_* columns)
  - Drop audit_log (legacy, not needed)
  - Maintain full referential integrity across 16 target tables

This requires:
  - Resolving text-based references (emails, SKUs, names) to integer IDs
  - Self-referential FK (categories.parent_id)
  - Merging shipping data into orders
  - Dropping 4 tables (audit_log, shipping removed; net 20->16)
  - Complex FK chains (order_items -> orders -> customers, etc.)
  - Handling nullable FKs (coupons.created_by_id, returns.processed_by_id)

Expected steps: 80-150
"""

TASK_ID = "hard_ecommerce_overhaul"
TASK_DESCRIPTION = (
    "Overhaul a legacy e-commerce platform from 20 denormalized tables into 16 "
    "normalized tables with proper integer FK references. "
    "(1) Replace all email/name/sku/code text references with integer FK IDs across "
    "all tables: customer_email->customer_id, product_sku->product_id, "
    "warehouse_name->warehouse_id, supplier_name->supplier_id, coupon_code->coupon_id, "
    "carrier_name kept as text but shipping merged into orders. "
    "(2) Normalize categories with self-referential parent_id FK. "
    "(3) Normalize orders to use shipping_address_id FK to customer_addresses. "
    "(4) Drop redundant columns (order_items.product_name/product_price replaced by product_id FK). "
    "(5) Merge shipping table into orders as shipping_carrier, shipping_tracking_number, "
    "shipping_status, shipped_date, estimated_delivery, actual_delivery columns. "
    "(6) Drop audit_log table entirely. "
    "Preserve all data with full referential integrity across 16 target tables."
)
DIFFICULTY = "hard"
MAX_STEPS = 150

INITIAL_SQL = """
-- ============================================================
-- TABLE 1: customers (8 rows, 12 columns)
-- ============================================================
CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT,
    password_hash TEXT NOT NULL,
    registration_date TEXT NOT NULL,
    last_login TEXT,
    is_active INTEGER NOT NULL DEFAULT 1,
    loyalty_points INTEGER NOT NULL DEFAULT 0,
    referral_code TEXT,
    referred_by_email TEXT
);

INSERT INTO customers VALUES (1, 'Alice', 'Johnson', 'alice@example.com', '555-0101', 'pbkdf2_sha256$a1b2c3', '2023-01-15', '2024-11-20', 1, 1250, 'ALICE10', NULL);
INSERT INTO customers VALUES (2, 'Bob', 'Smith', 'bob@example.com', '555-0202', 'pbkdf2_sha256$d4e5f6', '2023-03-22', '2024-11-18', 1, 870, 'BOB20', 'alice@example.com');
INSERT INTO customers VALUES (3, 'Carol', 'Lee', 'carol@example.com', '555-0303', 'pbkdf2_sha256$g7h8i9', '2023-05-10', '2024-11-15', 1, 2100, 'CAROL30', NULL);
INSERT INTO customers VALUES (4, 'Dave', 'Brown', 'dave@example.com', '555-0404', 'pbkdf2_sha256$j0k1l2', '2023-07-01', '2024-10-30', 0, 340, 'DAVE40', 'carol@example.com');
INSERT INTO customers VALUES (5, 'Eve', 'Martinez', 'eve@example.com', '555-0505', 'pbkdf2_sha256$m3n4o5', '2023-08-18', '2024-11-19', 1, 1580, 'EVE50', 'alice@example.com');
INSERT INTO customers VALUES (6, 'Frank', 'Wilson', 'frank@example.com', '555-0606', 'pbkdf2_sha256$p6q7r8', '2023-10-05', '2024-11-10', 1, 620, 'FRANK60', NULL);
INSERT INTO customers VALUES (7, 'Grace', 'Kim', 'grace@example.com', '555-0707', 'pbkdf2_sha256$s9t0u1', '2024-01-12', '2024-11-21', 1, 450, 'GRACE70', 'bob@example.com');
INSERT INTO customers VALUES (8, 'Hank', 'Davis', 'hank@example.com', '555-0808', 'pbkdf2_sha256$v2w3x4', '2024-03-25', '2024-09-05', 0, 90, 'HANK80', 'carol@example.com');

-- ============================================================
-- TABLE 2: customer_addresses (12 rows, 12 columns)
-- ============================================================
CREATE TABLE customer_addresses (
    id INTEGER PRIMARY KEY,
    customer_email TEXT NOT NULL,
    address_type TEXT NOT NULL,
    line1 TEXT NOT NULL,
    line2 TEXT,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    zip TEXT NOT NULL,
    country TEXT NOT NULL DEFAULT 'US',
    is_default INTEGER NOT NULL DEFAULT 0,
    phone TEXT,
    instructions TEXT
);

INSERT INTO customer_addresses VALUES (1, 'alice@example.com', 'shipping', '123 Oak St', 'Apt 4B', 'Austin', 'TX', '78701', 'US', 1, '555-0101', 'Leave at door');
INSERT INTO customer_addresses VALUES (2, 'alice@example.com', 'billing', '123 Oak St', 'Apt 4B', 'Austin', 'TX', '78701', 'US', 0, '555-0101', NULL);
INSERT INTO customer_addresses VALUES (3, 'bob@example.com', 'shipping', '456 Pine Ave', NULL, 'Portland', 'OR', '97201', 'US', 1, '555-0202', 'Ring bell twice');
INSERT INTO customer_addresses VALUES (4, 'bob@example.com', 'billing', '789 Elm Blvd', 'Suite 100', 'Portland', 'OR', '97202', 'US', 0, '555-0202', NULL);
INSERT INTO customer_addresses VALUES (5, 'carol@example.com', 'shipping', '321 Maple Dr', NULL, 'Chicago', 'IL', '60601', 'US', 1, '555-0303', NULL);
INSERT INTO customer_addresses VALUES (6, 'carol@example.com', 'billing', '321 Maple Dr', NULL, 'Chicago', 'IL', '60601', 'US', 0, '555-0303', NULL);
INSERT INTO customer_addresses VALUES (7, 'dave@example.com', 'shipping', '654 Cedar Ln', 'Unit 7', 'Miami', 'FL', '33101', 'US', 1, '555-0404', 'Gate code 1234');
INSERT INTO customer_addresses VALUES (8, 'eve@example.com', 'shipping', '987 Birch Rd', NULL, 'Denver', 'CO', '80201', 'US', 1, '555-0505', NULL);
INSERT INTO customer_addresses VALUES (9, 'eve@example.com', 'billing', '987 Birch Rd', NULL, 'Denver', 'CO', '80201', 'US', 0, '555-0505', NULL);
INSERT INTO customer_addresses VALUES (10, 'frank@example.com', 'shipping', '147 Walnut St', NULL, 'Seattle', 'WA', '98101', 'US', 1, '555-0606', 'Side entrance');
INSERT INTO customer_addresses VALUES (11, 'grace@example.com', 'shipping', '258 Spruce Ave', 'Floor 3', 'Boston', 'MA', '02101', 'US', 1, '555-0707', NULL);
INSERT INTO customer_addresses VALUES (12, 'hank@example.com', 'shipping', '369 Ash Ct', NULL, 'Phoenix', 'AZ', '85001', 'US', 1, '555-0808', 'Back porch');

-- ============================================================
-- TABLE 3: products (10 rows, 13 columns)
-- ============================================================
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    sku TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    description TEXT,
    category_name TEXT,
    subcategory_name TEXT,
    price REAL NOT NULL,
    cost REAL NOT NULL,
    weight_kg REAL,
    dimensions TEXT,
    brand TEXT,
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL
);

INSERT INTO products VALUES (1, 'ELEC-LAPTOP-001', 'ProBook Laptop 15', 'High-performance laptop with 16GB RAM', 'Electronics', 'Laptops', 999.99, 650.00, 2.1, '35x24x2 cm', 'TechBrand', 1, '2023-01-10');
INSERT INTO products VALUES (2, 'ELEC-PHONE-001', 'SmartPhone X12', 'Latest smartphone with OLED display', 'Electronics', 'Phones', 799.99, 480.00, 0.19, '15x7x0.8 cm', 'TechBrand', 1, '2023-02-15');
INSERT INTO products VALUES (3, 'ELEC-TABLET-001', 'TabletPro 10', '10-inch tablet with stylus support', 'Electronics', 'Tablets', 549.99, 320.00, 0.48, '25x17x0.7 cm', 'TechBrand', 1, '2023-03-20');
INSERT INTO products VALUES (4, 'HOME-CHAIR-001', 'ErgoChair Plus', 'Ergonomic office chair with lumbar support', 'Home & Office', 'Furniture', 349.99, 180.00, 15.5, '65x65x120 cm', 'ComfortCo', 1, '2023-04-01');
INSERT INTO products VALUES (5, 'HOME-DESK-001', 'StandDesk Pro', 'Electric standing desk adjustable height', 'Home & Office', 'Furniture', 599.99, 310.00, 35.0, '150x75x120 cm', 'ComfortCo', 1, '2023-04-15');
INSERT INTO products VALUES (6, 'CLOTH-SHIRT-001', 'Classic Oxford Shirt', 'Cotton oxford button-down shirt', 'Clothing', 'Shirts', 59.99, 22.00, 0.3, NULL, 'StyleWear', 1, '2023-05-01');
INSERT INTO products VALUES (7, 'CLOTH-JEANS-001', 'Slim Fit Jeans', 'Dark wash slim fit denim jeans', 'Clothing', 'Pants', 79.99, 30.00, 0.8, NULL, 'StyleWear', 1, '2023-05-10');
INSERT INTO products VALUES (8, 'BOOK-TECH-001', 'Database Design Mastery', 'Comprehensive guide to database design', 'Books', 'Technology', 45.99, 12.00, 0.7, '23x15x3 cm', 'TechPress', 1, '2023-06-01');
INSERT INTO products VALUES (9, 'BOOK-FICTION-001', 'The Last Algorithm', 'Sci-fi thriller about rogue AI', 'Books', 'Fiction', 16.99, 5.00, 0.4, '20x13x2 cm', 'NovelHouse', 1, '2023-06-15');
INSERT INTO products VALUES (10, 'SPORT-YOGA-001', 'Premium Yoga Mat', 'Non-slip eco-friendly yoga mat', 'Sports', 'Yoga', 39.99, 14.00, 1.2, '180x60x0.6 cm', 'FitGear', 0, '2023-07-01');

-- ============================================================
-- TABLE 4: product_images (15 rows, 11 columns)
-- ============================================================
CREATE TABLE product_images (
    id INTEGER PRIMARY KEY,
    product_sku TEXT NOT NULL,
    url TEXT NOT NULL,
    alt_text TEXT,
    sort_order INTEGER NOT NULL DEFAULT 0,
    is_primary INTEGER NOT NULL DEFAULT 0,
    width INTEGER,
    height INTEGER,
    file_size INTEGER,
    mime_type TEXT NOT NULL DEFAULT 'image/jpeg',
    uploaded_at TEXT NOT NULL
);

INSERT INTO product_images VALUES (1, 'ELEC-LAPTOP-001', 'https://cdn.shop.com/laptop-front.jpg', 'ProBook Laptop front view', 1, 1, 1200, 900, 245000, 'image/jpeg', '2023-01-10');
INSERT INTO product_images VALUES (2, 'ELEC-LAPTOP-001', 'https://cdn.shop.com/laptop-side.jpg', 'ProBook Laptop side view', 2, 0, 1200, 900, 198000, 'image/jpeg', '2023-01-10');
INSERT INTO product_images VALUES (3, 'ELEC-PHONE-001', 'https://cdn.shop.com/phone-front.jpg', 'SmartPhone X12 front', 1, 1, 800, 1200, 180000, 'image/jpeg', '2023-02-15');
INSERT INTO product_images VALUES (4, 'ELEC-PHONE-001', 'https://cdn.shop.com/phone-back.jpg', 'SmartPhone X12 back', 2, 0, 800, 1200, 165000, 'image/jpeg', '2023-02-15');
INSERT INTO product_images VALUES (5, 'ELEC-TABLET-001', 'https://cdn.shop.com/tablet-front.jpg', 'TabletPro 10 front', 1, 1, 1000, 750, 210000, 'image/jpeg', '2023-03-20');
INSERT INTO product_images VALUES (6, 'HOME-CHAIR-001', 'https://cdn.shop.com/chair-main.jpg', 'ErgoChair Plus main view', 1, 1, 1000, 1000, 320000, 'image/jpeg', '2023-04-01');
INSERT INTO product_images VALUES (7, 'HOME-CHAIR-001', 'https://cdn.shop.com/chair-detail.jpg', 'ErgoChair Plus lumbar detail', 2, 0, 800, 800, 150000, 'image/jpeg', '2023-04-01');
INSERT INTO product_images VALUES (8, 'HOME-DESK-001', 'https://cdn.shop.com/desk-main.jpg', 'StandDesk Pro main view', 1, 1, 1200, 800, 280000, 'image/jpeg', '2023-04-15');
INSERT INTO product_images VALUES (9, 'CLOTH-SHIRT-001', 'https://cdn.shop.com/shirt-main.jpg', 'Classic Oxford Shirt front', 1, 1, 800, 1000, 175000, 'image/jpeg', '2023-05-01');
INSERT INTO product_images VALUES (10, 'CLOTH-JEANS-001', 'https://cdn.shop.com/jeans-main.jpg', 'Slim Fit Jeans front', 1, 1, 800, 1200, 190000, 'image/jpeg', '2023-05-10');
INSERT INTO product_images VALUES (11, 'BOOK-TECH-001', 'https://cdn.shop.com/dbbook-cover.jpg', 'Database Design Mastery cover', 1, 1, 600, 900, 120000, 'image/jpeg', '2023-06-01');
INSERT INTO product_images VALUES (12, 'BOOK-FICTION-001', 'https://cdn.shop.com/lastalgo-cover.jpg', 'The Last Algorithm cover', 1, 1, 600, 900, 110000, 'image/jpeg', '2023-06-15');
INSERT INTO product_images VALUES (13, 'SPORT-YOGA-001', 'https://cdn.shop.com/yogamat-main.jpg', 'Premium Yoga Mat rolled', 1, 1, 1000, 800, 200000, 'image/jpeg', '2023-07-01');
INSERT INTO product_images VALUES (14, 'SPORT-YOGA-001', 'https://cdn.shop.com/yogamat-flat.jpg', 'Premium Yoga Mat flat', 2, 0, 1200, 600, 230000, 'image/jpeg', '2023-07-01');
INSERT INTO product_images VALUES (15, 'ELEC-TABLET-001', 'https://cdn.shop.com/tablet-stylus.jpg', 'TabletPro 10 with stylus', 2, 0, 1000, 750, 195000, 'image/jpeg', '2023-03-20');

-- ============================================================
-- TABLE 5: categories (6 rows, 11 columns)
-- ============================================================
CREATE TABLE categories (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    slug TEXT NOT NULL UNIQUE,
    description TEXT,
    parent_category_name TEXT,
    image_url TEXT,
    sort_order INTEGER NOT NULL DEFAULT 0,
    is_active INTEGER NOT NULL DEFAULT 1,
    meta_title TEXT,
    meta_description TEXT,
    product_count INTEGER NOT NULL DEFAULT 0
);

INSERT INTO categories VALUES (1, 'Electronics', 'electronics', 'Electronic devices and gadgets', NULL, 'https://cdn.shop.com/cat-electronics.jpg', 1, 1, 'Electronics Store', 'Shop electronics online', 3);
INSERT INTO categories VALUES (2, 'Home & Office', 'home-office', 'Home and office furniture and supplies', NULL, 'https://cdn.shop.com/cat-home.jpg', 2, 1, 'Home & Office', 'Furniture and office supplies', 2);
INSERT INTO categories VALUES (3, 'Clothing', 'clothing', 'Apparel and fashion', NULL, 'https://cdn.shop.com/cat-clothing.jpg', 3, 1, 'Clothing Store', 'Fashion and apparel', 2);
INSERT INTO categories VALUES (4, 'Books', 'books', 'Books and publications', NULL, 'https://cdn.shop.com/cat-books.jpg', 4, 1, 'Bookstore', 'Books for everyone', 2);
INSERT INTO categories VALUES (5, 'Sports', 'sports', 'Sports and fitness equipment', NULL, 'https://cdn.shop.com/cat-sports.jpg', 5, 1, 'Sports Store', 'Sports and fitness gear', 1);
INSERT INTO categories VALUES (6, 'Laptops', 'laptops', 'Laptop computers', 'Electronics', 'https://cdn.shop.com/cat-laptops.jpg', 1, 1, 'Laptops', 'Shop laptops', 1);

-- ============================================================
-- TABLE 6: inventory (10 rows, 11 columns)
-- ============================================================
CREATE TABLE inventory (
    id INTEGER PRIMARY KEY,
    product_sku TEXT NOT NULL,
    warehouse_name TEXT NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 0,
    reserved INTEGER NOT NULL DEFAULT 0,
    available INTEGER NOT NULL DEFAULT 0,
    reorder_point INTEGER NOT NULL DEFAULT 10,
    reorder_qty INTEGER NOT NULL DEFAULT 50,
    last_restock TEXT,
    last_sold TEXT,
    cost_per_unit REAL
);

INSERT INTO inventory VALUES (1, 'ELEC-LAPTOP-001', 'East Coast Hub', 45, 5, 40, 10, 50, '2024-10-01', '2024-11-20', 650.00);
INSERT INTO inventory VALUES (2, 'ELEC-PHONE-001', 'East Coast Hub', 120, 12, 108, 20, 100, '2024-10-15', '2024-11-21', 480.00);
INSERT INTO inventory VALUES (3, 'ELEC-TABLET-001', 'West Coast Depot', 60, 3, 57, 15, 50, '2024-09-20', '2024-11-18', 320.00);
INSERT INTO inventory VALUES (4, 'HOME-CHAIR-001', 'Central Warehouse', 30, 2, 28, 5, 20, '2024-08-15', '2024-11-15', 180.00);
INSERT INTO inventory VALUES (5, 'HOME-DESK-001', 'Central Warehouse', 15, 1, 14, 5, 10, '2024-09-01', '2024-11-10', 310.00);
INSERT INTO inventory VALUES (6, 'CLOTH-SHIRT-001', 'East Coast Hub', 200, 10, 190, 30, 100, '2024-10-20', '2024-11-21', 22.00);
INSERT INTO inventory VALUES (7, 'CLOTH-JEANS-001', 'West Coast Depot', 150, 8, 142, 25, 80, '2024-10-10', '2024-11-19', 30.00);
INSERT INTO inventory VALUES (8, 'BOOK-TECH-001', 'East Coast Hub', 80, 0, 80, 20, 50, '2024-11-01', '2024-11-17', 12.00);
INSERT INTO inventory VALUES (9, 'BOOK-FICTION-001', 'West Coast Depot', 300, 15, 285, 50, 200, '2024-11-05', '2024-11-21', 5.00);
INSERT INTO inventory VALUES (10, 'SPORT-YOGA-001', 'Central Warehouse', 0, 0, 0, 10, 50, '2024-06-01', '2024-08-15', 14.00);

-- ============================================================
-- TABLE 7: warehouses (3 rows, 12 columns)
-- ============================================================
CREATE TABLE warehouses (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    code TEXT NOT NULL UNIQUE,
    address TEXT NOT NULL,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    zip TEXT NOT NULL,
    country TEXT NOT NULL DEFAULT 'US',
    manager_email TEXT,
    phone TEXT,
    capacity INTEGER NOT NULL DEFAULT 10000,
    is_active INTEGER NOT NULL DEFAULT 1
);

INSERT INTO warehouses VALUES (1, 'East Coast Hub', 'ECH', '100 Warehouse Rd', 'Newark', 'NJ', '07101', 'US', 'alice@example.com', '555-9001', 50000, 1);
INSERT INTO warehouses VALUES (2, 'West Coast Depot', 'WCD', '200 Logistics Blvd', 'Los Angeles', 'CA', '90001', 'US', 'carol@example.com', '555-9002', 40000, 1);
INSERT INTO warehouses VALUES (3, 'Central Warehouse', 'CWH', '300 Distribution Ave', 'Dallas', 'TX', '75201', 'US', 'frank@example.com', '555-9003', 60000, 1);

-- ============================================================
-- TABLE 8: orders (15 rows, 14 columns)
-- ============================================================
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    customer_email TEXT NOT NULL,
    order_date TEXT NOT NULL,
    status TEXT NOT NULL,
    shipping_address_line1 TEXT,
    shipping_city TEXT,
    shipping_state TEXT,
    shipping_zip TEXT,
    subtotal REAL NOT NULL,
    tax REAL NOT NULL,
    shipping_cost REAL NOT NULL DEFAULT 0.0,
    total REAL NOT NULL,
    payment_method TEXT,
    notes TEXT
);

INSERT INTO orders VALUES (1, 'alice@example.com', '2024-01-15', 'delivered', '123 Oak St', 'Austin', 'TX', '78701', 999.99, 82.50, 15.00, 1097.49, 'credit_card', NULL);
INSERT INTO orders VALUES (2, 'alice@example.com', '2024-02-20', 'delivered', '123 Oak St', 'Austin', 'TX', '78701', 59.99, 4.95, 5.99, 70.93, 'credit_card', 'Gift wrap please');
INSERT INTO orders VALUES (3, 'bob@example.com', '2024-03-05', 'delivered', '456 Pine Ave', 'Portland', 'OR', '97201', 799.99, 0.00, 12.00, 811.99, 'paypal', NULL);
INSERT INTO orders VALUES (4, 'bob@example.com', '2024-04-10', 'delivered', '456 Pine Ave', 'Portland', 'OR', '97201', 349.99, 28.00, 25.00, 402.99, 'credit_card', NULL);
INSERT INTO orders VALUES (5, 'carol@example.com', '2024-04-22', 'delivered', '321 Maple Dr', 'Chicago', 'IL', '60601', 1149.98, 94.87, 20.00, 1264.85, 'credit_card', NULL);
INSERT INTO orders VALUES (6, 'carol@example.com', '2024-05-15', 'delivered', '321 Maple Dr', 'Chicago', 'IL', '60601', 62.98, 5.20, 5.99, 74.17, 'paypal', NULL);
INSERT INTO orders VALUES (7, 'dave@example.com', '2024-06-01', 'returned', '654 Cedar Ln', 'Miami', 'FL', '33101', 79.99, 5.60, 7.99, 93.58, 'credit_card', NULL);
INSERT INTO orders VALUES (8, 'eve@example.com', '2024-06-18', 'delivered', '987 Birch Rd', 'Denver', 'CO', '80201', 549.99, 38.50, 10.00, 598.49, 'credit_card', 'Expedited shipping');
INSERT INTO orders VALUES (9, 'eve@example.com', '2024-07-04', 'delivered', '987 Birch Rd', 'Denver', 'CO', '80201', 45.99, 3.22, 3.99, 53.20, 'paypal', NULL);
INSERT INTO orders VALUES (10, 'frank@example.com', '2024-07-20', 'shipped', '147 Walnut St', 'Seattle', 'WA', '98101', 599.99, 54.00, 0.00, 653.99, 'credit_card', NULL);
INSERT INTO orders VALUES (11, 'frank@example.com', '2024-08-05', 'delivered', '147 Walnut St', 'Seattle', 'WA', '98101', 16.99, 1.53, 3.99, 22.51, 'paypal', NULL);
INSERT INTO orders VALUES (12, 'grace@example.com', '2024-08-22', 'processing', '258 Spruce Ave', 'Boston', 'MA', '02101', 859.98, 53.32, 15.00, 928.30, 'credit_card', NULL);
INSERT INTO orders VALUES (13, 'grace@example.com', '2024-09-10', 'delivered', '258 Spruce Ave', 'Boston', 'MA', '02101', 39.99, 2.50, 5.99, 48.48, 'credit_card', NULL);
INSERT INTO orders VALUES (14, 'hank@example.com', '2024-09-28', 'cancelled', '369 Ash Ct', 'Phoenix', 'AZ', '85001', 129.98, 10.79, 7.99, 148.76, 'paypal', 'Changed my mind');
INSERT INTO orders VALUES (15, 'alice@example.com', '2024-10-15', 'delivered', '123 Oak St', 'Austin', 'TX', '78701', 96.98, 8.00, 5.99, 110.97, 'credit_card', NULL);

-- ============================================================
-- TABLE 9: order_items (25 rows, 11 columns)
-- ============================================================
CREATE TABLE order_items (
    id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    product_sku TEXT NOT NULL,
    product_name TEXT NOT NULL,
    product_price REAL NOT NULL,
    quantity INTEGER NOT NULL,
    subtotal REAL NOT NULL,
    discount_amount REAL NOT NULL DEFAULT 0.0,
    tax_amount REAL NOT NULL DEFAULT 0.0,
    status TEXT NOT NULL DEFAULT 'fulfilled',
    tracking_number TEXT
);

INSERT INTO order_items VALUES (1, 1, 'ELEC-LAPTOP-001', 'ProBook Laptop 15', 999.99, 1, 999.99, 0.00, 82.50, 'delivered', 'TRK-1001');
INSERT INTO order_items VALUES (2, 2, 'CLOTH-SHIRT-001', 'Classic Oxford Shirt', 59.99, 1, 59.99, 0.00, 4.95, 'delivered', 'TRK-1002');
INSERT INTO order_items VALUES (3, 3, 'ELEC-PHONE-001', 'SmartPhone X12', 799.99, 1, 799.99, 0.00, 0.00, 'delivered', 'TRK-1003');
INSERT INTO order_items VALUES (4, 4, 'HOME-CHAIR-001', 'ErgoChair Plus', 349.99, 1, 349.99, 0.00, 28.00, 'delivered', 'TRK-1004');
INSERT INTO order_items VALUES (5, 5, 'ELEC-LAPTOP-001', 'ProBook Laptop 15', 999.99, 1, 999.99, 0.00, 82.50, 'delivered', 'TRK-1005A');
INSERT INTO order_items VALUES (6, 5, 'HOME-CHAIR-001', 'ErgoChair Plus', 349.99, 1, 349.99, 200.00, 12.37, 'delivered', 'TRK-1005A');
INSERT INTO order_items VALUES (7, 6, 'BOOK-TECH-001', 'Database Design Mastery', 45.99, 1, 45.99, 0.00, 3.80, 'delivered', 'TRK-1006');
INSERT INTO order_items VALUES (8, 6, 'BOOK-FICTION-001', 'The Last Algorithm', 16.99, 1, 16.99, 0.00, 1.40, 'delivered', 'TRK-1006');
INSERT INTO order_items VALUES (9, 7, 'CLOTH-JEANS-001', 'Slim Fit Jeans', 79.99, 1, 79.99, 0.00, 5.60, 'returned', 'TRK-1007');
INSERT INTO order_items VALUES (10, 8, 'ELEC-TABLET-001', 'TabletPro 10', 549.99, 1, 549.99, 0.00, 38.50, 'delivered', 'TRK-1008');
INSERT INTO order_items VALUES (11, 9, 'BOOK-TECH-001', 'Database Design Mastery', 45.99, 1, 45.99, 0.00, 3.22, 'delivered', 'TRK-1009');
INSERT INTO order_items VALUES (12, 10, 'HOME-DESK-001', 'StandDesk Pro', 599.99, 1, 599.99, 0.00, 54.00, 'shipped', 'TRK-1010');
INSERT INTO order_items VALUES (13, 11, 'BOOK-FICTION-001', 'The Last Algorithm', 16.99, 1, 16.99, 0.00, 1.53, 'delivered', 'TRK-1011');
INSERT INTO order_items VALUES (14, 12, 'ELEC-PHONE-001', 'SmartPhone X12', 799.99, 1, 799.99, 0.00, 49.60, 'processing', NULL);
INSERT INTO order_items VALUES (15, 12, 'CLOTH-SHIRT-001', 'Classic Oxford Shirt', 59.99, 1, 59.99, 0.00, 3.72, 'processing', NULL);
INSERT INTO order_items VALUES (16, 13, 'SPORT-YOGA-001', 'Premium Yoga Mat', 39.99, 1, 39.99, 0.00, 2.50, 'delivered', 'TRK-1013');
INSERT INTO order_items VALUES (17, 14, 'CLOTH-SHIRT-001', 'Classic Oxford Shirt', 59.99, 1, 59.99, 0.00, 4.97, 'cancelled', NULL);
INSERT INTO order_items VALUES (18, 14, 'CLOTH-JEANS-001', 'Slim Fit Jeans', 79.99, 1, 79.99, 10.00, 5.82, 'cancelled', NULL);
INSERT INTO order_items VALUES (19, 15, 'BOOK-TECH-001', 'Database Design Mastery', 45.99, 1, 45.99, 0.00, 3.80, 'delivered', 'TRK-1015A');
INSERT INTO order_items VALUES (20, 15, 'BOOK-FICTION-001', 'The Last Algorithm', 16.99, 3, 50.97, 0.00, 4.21, 'delivered', 'TRK-1015A');
INSERT INTO order_items VALUES (21, 1, 'SPORT-YOGA-001', 'Premium Yoga Mat', 39.99, 0, 0.00, 0.00, 0.00, 'cancelled', NULL);
INSERT INTO order_items VALUES (22, 3, 'CLOTH-SHIRT-001', 'Classic Oxford Shirt', 59.99, 0, 0.00, 0.00, 0.00, 'cancelled', NULL);
INSERT INTO order_items VALUES (23, 5, 'BOOK-FICTION-001', 'The Last Algorithm', 16.99, 0, 0.00, 0.00, 0.00, 'cancelled', NULL);
INSERT INTO order_items VALUES (24, 8, 'CLOTH-JEANS-001', 'Slim Fit Jeans', 79.99, 0, 0.00, 0.00, 0.00, 'cancelled', NULL);
INSERT INTO order_items VALUES (25, 12, 'BOOK-TECH-001', 'Database Design Mastery', 45.99, 0, 0.00, 0.00, 0.00, 'cancelled', NULL);

-- ============================================================
-- TABLE 10: payments (15 rows, 11 columns)
-- ============================================================
CREATE TABLE payments (
    id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    customer_email TEXT NOT NULL,
    amount REAL NOT NULL,
    method TEXT NOT NULL,
    status TEXT NOT NULL,
    transaction_id TEXT,
    gateway TEXT NOT NULL DEFAULT 'stripe',
    processed_at TEXT,
    currency TEXT NOT NULL DEFAULT 'USD',
    refund_amount REAL NOT NULL DEFAULT 0.0
);

INSERT INTO payments VALUES (1, 1, 'alice@example.com', 1097.49, 'credit_card', 'completed', 'TXN-A001', 'stripe', '2024-01-15 10:30:00', 'USD', 0.00);
INSERT INTO payments VALUES (2, 2, 'alice@example.com', 70.93, 'credit_card', 'completed', 'TXN-A002', 'stripe', '2024-02-20 14:15:00', 'USD', 0.00);
INSERT INTO payments VALUES (3, 3, 'bob@example.com', 811.99, 'paypal', 'completed', 'TXN-B001', 'paypal', '2024-03-05 09:45:00', 'USD', 0.00);
INSERT INTO payments VALUES (4, 4, 'bob@example.com', 402.99, 'credit_card', 'completed', 'TXN-B002', 'stripe', '2024-04-10 16:20:00', 'USD', 0.00);
INSERT INTO payments VALUES (5, 5, 'carol@example.com', 1264.85, 'credit_card', 'completed', 'TXN-C001', 'stripe', '2024-04-22 11:00:00', 'USD', 0.00);
INSERT INTO payments VALUES (6, 6, 'carol@example.com', 74.17, 'paypal', 'completed', 'TXN-C002', 'paypal', '2024-05-15 13:30:00', 'USD', 0.00);
INSERT INTO payments VALUES (7, 7, 'dave@example.com', 93.58, 'credit_card', 'refunded', 'TXN-D001', 'stripe', '2024-06-01 10:00:00', 'USD', 93.58);
INSERT INTO payments VALUES (8, 8, 'eve@example.com', 598.49, 'credit_card', 'completed', 'TXN-E001', 'stripe', '2024-06-18 15:45:00', 'USD', 0.00);
INSERT INTO payments VALUES (9, 9, 'eve@example.com', 53.20, 'paypal', 'completed', 'TXN-E002', 'paypal', '2024-07-04 12:00:00', 'USD', 0.00);
INSERT INTO payments VALUES (10, 10, 'frank@example.com', 653.99, 'credit_card', 'completed', 'TXN-F001', 'stripe', '2024-07-20 09:15:00', 'USD', 0.00);
INSERT INTO payments VALUES (11, 11, 'frank@example.com', 22.51, 'paypal', 'completed', 'TXN-F002', 'paypal', '2024-08-05 17:30:00', 'USD', 0.00);
INSERT INTO payments VALUES (12, 12, 'grace@example.com', 928.30, 'credit_card', 'pending', 'TXN-G001', 'stripe', '2024-08-22 10:45:00', 'USD', 0.00);
INSERT INTO payments VALUES (13, 13, 'grace@example.com', 48.48, 'credit_card', 'completed', 'TXN-G002', 'stripe', '2024-09-10 14:00:00', 'USD', 0.00);
INSERT INTO payments VALUES (14, 14, 'hank@example.com', 148.76, 'paypal', 'refunded', 'TXN-H001', 'paypal', '2024-09-28 11:20:00', 'USD', 148.76);
INSERT INTO payments VALUES (15, 15, 'alice@example.com', 110.97, 'credit_card', 'completed', 'TXN-A003', 'stripe', '2024-10-15 16:00:00', 'USD', 0.00);

-- ============================================================
-- TABLE 11: shipping (12 rows, 11 columns)
-- ============================================================
CREATE TABLE shipping (
    id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    carrier_name TEXT NOT NULL,
    tracking_number TEXT,
    status TEXT NOT NULL,
    shipped_date TEXT,
    estimated_delivery TEXT,
    actual_delivery TEXT,
    weight REAL,
    cost REAL NOT NULL DEFAULT 0.0,
    signature_required INTEGER NOT NULL DEFAULT 0
);

INSERT INTO shipping VALUES (1, 1, 'FedEx', 'FDX-90001', 'delivered', '2024-01-16', '2024-01-20', '2024-01-19', 2.5, 15.00, 1);
INSERT INTO shipping VALUES (2, 2, 'USPS', 'USPS-90002', 'delivered', '2024-02-21', '2024-02-25', '2024-02-24', 0.5, 5.99, 0);
INSERT INTO shipping VALUES (3, 3, 'UPS', 'UPS-90003', 'delivered', '2024-03-06', '2024-03-10', '2024-03-09', 0.4, 12.00, 1);
INSERT INTO shipping VALUES (4, 4, 'FedEx', 'FDX-90004', 'delivered', '2024-04-11', '2024-04-15', '2024-04-14', 16.0, 25.00, 1);
INSERT INTO shipping VALUES (5, 5, 'FedEx', 'FDX-90005', 'delivered', '2024-04-23', '2024-04-27', '2024-04-26', 18.0, 20.00, 1);
INSERT INTO shipping VALUES (6, 6, 'USPS', 'USPS-90006', 'delivered', '2024-05-16', '2024-05-20', '2024-05-19', 1.2, 5.99, 0);
INSERT INTO shipping VALUES (7, 7, 'UPS', 'UPS-90007', 'returned', '2024-06-02', '2024-06-06', '2024-06-05', 1.0, 7.99, 0);
INSERT INTO shipping VALUES (8, 8, 'FedEx', 'FDX-90008', 'delivered', '2024-06-19', '2024-06-23', '2024-06-22', 0.7, 10.00, 0);
INSERT INTO shipping VALUES (9, 9, 'USPS', 'USPS-90009', 'delivered', '2024-07-05', '2024-07-09', '2024-07-08', 0.8, 3.99, 0);
INSERT INTO shipping VALUES (10, 10, 'FedEx', 'FDX-90010', 'in_transit', '2024-07-21', '2024-07-25', NULL, 36.0, 0.00, 1);
INSERT INTO shipping VALUES (11, 11, 'USPS', 'USPS-90011', 'delivered', '2024-08-06', '2024-08-10', '2024-08-09', 0.5, 3.99, 0);
INSERT INTO shipping VALUES (12, 15, 'UPS', 'UPS-90012', 'delivered', '2024-10-16', '2024-10-20', '2024-10-19', 1.5, 5.99, 0);

-- ============================================================
-- TABLE 12: reviews (12 rows, 11 columns)
-- ============================================================
CREATE TABLE reviews (
    id INTEGER PRIMARY KEY,
    product_sku TEXT NOT NULL,
    customer_email TEXT NOT NULL,
    rating INTEGER NOT NULL,
    title TEXT,
    body TEXT,
    is_verified INTEGER NOT NULL DEFAULT 0,
    is_approved INTEGER NOT NULL DEFAULT 1,
    helpful_count INTEGER NOT NULL DEFAULT 0,
    reported_count INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL
);

INSERT INTO reviews VALUES (1, 'ELEC-LAPTOP-001', 'alice@example.com', 5, 'Amazing laptop', 'Fast and reliable, great battery life', 1, 1, 24, 0, '2024-01-25');
INSERT INTO reviews VALUES (2, 'ELEC-PHONE-001', 'bob@example.com', 4, 'Great phone', 'Excellent display but camera could be better', 1, 1, 18, 0, '2024-03-15');
INSERT INTO reviews VALUES (3, 'HOME-CHAIR-001', 'bob@example.com', 5, 'Perfect for WFH', 'My back pain is gone after switching to this chair', 1, 1, 31, 0, '2024-04-20');
INSERT INTO reviews VALUES (4, 'ELEC-LAPTOP-001', 'carol@example.com', 4, 'Solid machine', 'Good performance, a bit heavy', 1, 1, 12, 0, '2024-05-01');
INSERT INTO reviews VALUES (5, 'HOME-CHAIR-001', 'carol@example.com', 3, 'Decent chair', 'Comfortable but armrests are wobbly', 1, 1, 8, 1, '2024-05-10');
INSERT INTO reviews VALUES (6, 'CLOTH-JEANS-001', 'dave@example.com', 2, 'Poor fit', 'Sizing runs small, had to return', 1, 1, 5, 0, '2024-06-10');
INSERT INTO reviews VALUES (7, 'ELEC-TABLET-001', 'eve@example.com', 5, 'Love this tablet', 'Perfect for drawing and note taking', 1, 1, 20, 0, '2024-06-28');
INSERT INTO reviews VALUES (8, 'BOOK-TECH-001', 'eve@example.com', 4, 'Great reference', 'Well-written database guide', 1, 1, 15, 0, '2024-07-10');
INSERT INTO reviews VALUES (9, 'HOME-DESK-001', 'frank@example.com', 5, 'Best desk ever', 'Smooth motor, very sturdy', 1, 1, 27, 0, '2024-07-30');
INSERT INTO reviews VALUES (10, 'BOOK-FICTION-001', 'frank@example.com', 3, 'OK read', 'Interesting premise but slow middle', 1, 1, 6, 0, '2024-08-12');
INSERT INTO reviews VALUES (11, 'ELEC-PHONE-001', 'grace@example.com', 5, 'Incredible phone', 'Best phone I have ever owned', 1, 0, 0, 0, '2024-09-15');
INSERT INTO reviews VALUES (12, 'SPORT-YOGA-001', 'grace@example.com', 4, 'Nice mat', 'Good grip and easy to clean', 1, 1, 9, 0, '2024-09-20');

-- ============================================================
-- TABLE 13: coupons (6 rows, 12 columns)
-- ============================================================
CREATE TABLE coupons (
    id INTEGER PRIMARY KEY,
    code TEXT NOT NULL UNIQUE,
    description TEXT,
    discount_type TEXT NOT NULL,
    discount_value REAL NOT NULL,
    min_order_amount REAL NOT NULL DEFAULT 0.0,
    max_uses INTEGER,
    current_uses INTEGER NOT NULL DEFAULT 0,
    valid_from TEXT NOT NULL,
    valid_until TEXT,
    is_active INTEGER NOT NULL DEFAULT 1,
    created_by_email TEXT
);

INSERT INTO coupons VALUES (1, 'WELCOME10', 'Welcome discount 10%', 'percentage', 10.0, 50.00, 1000, 156, '2024-01-01', '2024-12-31', 1, 'alice@example.com');
INSERT INTO coupons VALUES (2, 'SUMMER25', 'Summer sale $25 off', 'fixed', 25.0, 100.00, 500, 89, '2024-06-01', '2024-08-31', 0, 'carol@example.com');
INSERT INTO coupons VALUES (3, 'FREESHIP', 'Free shipping on all orders', 'shipping', 100.0, 0.00, NULL, 312, '2024-01-01', NULL, 1, 'alice@example.com');
INSERT INTO coupons VALUES (4, 'VIP20', 'VIP customer 20% off', 'percentage', 20.0, 200.00, 100, 23, '2024-03-01', '2025-03-01', 1, 'carol@example.com');
INSERT INTO coupons VALUES (5, 'FLASH50', 'Flash sale $50 off electronics', 'fixed', 50.0, 500.00, 50, 50, '2024-11-01', '2024-11-03', 0, NULL);
INSERT INTO coupons VALUES (6, 'LOYALTY15', 'Loyalty program 15% off', 'percentage', 15.0, 75.00, NULL, 45, '2024-06-01', NULL, 1, 'eve@example.com');

-- ============================================================
-- TABLE 14: coupon_usage (8 rows, 10 columns)
-- ============================================================
CREATE TABLE coupon_usage (
    id INTEGER PRIMARY KEY,
    coupon_code TEXT NOT NULL,
    customer_email TEXT NOT NULL,
    order_id INTEGER NOT NULL,
    discount_applied REAL NOT NULL,
    used_at TEXT NOT NULL,
    ip_address TEXT,
    user_agent TEXT,
    session_id TEXT,
    is_first_use INTEGER NOT NULL DEFAULT 0
);

INSERT INTO coupon_usage VALUES (1, 'WELCOME10', 'bob@example.com', 3, 80.00, '2024-03-05 09:40:00', '192.168.1.10', 'Mozilla/5.0 Chrome/120', 'sess-b001', 1);
INSERT INTO coupon_usage VALUES (2, 'FREESHIP', 'carol@example.com', 5, 20.00, '2024-04-22 10:55:00', '192.168.1.20', 'Mozilla/5.0 Safari/17', 'sess-c001', 1);
INSERT INTO coupon_usage VALUES (3, 'SUMMER25', 'eve@example.com', 8, 25.00, '2024-06-18 15:40:00', '192.168.1.30', 'Mozilla/5.0 Firefox/121', 'sess-e001', 1);
INSERT INTO coupon_usage VALUES (4, 'VIP20', 'carol@example.com', 6, 12.60, '2024-05-15 13:25:00', '192.168.1.20', 'Mozilla/5.0 Safari/17', 'sess-c002', 0);
INSERT INTO coupon_usage VALUES (5, 'FREESHIP', 'frank@example.com', 10, 0.00, '2024-07-20 09:10:00', '192.168.1.40', 'Mozilla/5.0 Chrome/122', 'sess-f001', 1);
INSERT INTO coupon_usage VALUES (6, 'LOYALTY15', 'alice@example.com', 15, 14.55, '2024-10-15 15:55:00', '192.168.1.50', 'Mozilla/5.0 Chrome/123', 'sess-a003', 1);
INSERT INTO coupon_usage VALUES (7, 'WELCOME10', 'grace@example.com', 12, 85.99, '2024-08-22 10:40:00', '192.168.1.60', 'Mozilla/5.0 Edge/120', 'sess-g001', 1);
INSERT INTO coupon_usage VALUES (8, 'SUMMER25', 'hank@example.com', 14, 25.00, '2024-09-28 11:15:00', '192.168.1.70', 'Mozilla/5.0 Chrome/121', 'sess-h001', 1);

-- ============================================================
-- TABLE 15: wishlists (10 rows, 11 columns)
-- ============================================================
CREATE TABLE wishlists (
    id INTEGER PRIMARY KEY,
    customer_email TEXT NOT NULL,
    product_sku TEXT NOT NULL,
    added_at TEXT NOT NULL,
    priority INTEGER NOT NULL DEFAULT 0,
    notes TEXT,
    is_public INTEGER NOT NULL DEFAULT 0,
    price_at_add REAL NOT NULL,
    current_price REAL NOT NULL,
    notify_on_sale INTEGER NOT NULL DEFAULT 0,
    source_page TEXT
);

INSERT INTO wishlists VALUES (1, 'alice@example.com', 'ELEC-PHONE-001', '2024-02-01', 1, 'Want for birthday', 1, 799.99, 799.99, 1, '/products/smartphone-x12');
INSERT INTO wishlists VALUES (2, 'alice@example.com', 'HOME-DESK-001', '2024-03-10', 2, NULL, 0, 599.99, 599.99, 1, '/products/standdesk-pro');
INSERT INTO wishlists VALUES (3, 'bob@example.com', 'ELEC-TABLET-001', '2024-04-05', 1, 'For drawing', 1, 549.99, 549.99, 0, '/products/tabletpro-10');
INSERT INTO wishlists VALUES (4, 'carol@example.com', 'CLOTH-JEANS-001', '2024-05-20', 0, NULL, 0, 79.99, 79.99, 0, '/products/slim-jeans');
INSERT INTO wishlists VALUES (5, 'dave@example.com', 'ELEC-LAPTOP-001', '2024-06-15', 1, 'Need for work', 0, 999.99, 999.99, 1, '/products/probook-laptop');
INSERT INTO wishlists VALUES (6, 'eve@example.com', 'HOME-CHAIR-001', '2024-07-01', 2, 'Home office upgrade', 1, 349.99, 349.99, 1, '/products/ergochair');
INSERT INTO wishlists VALUES (7, 'eve@example.com', 'CLOTH-SHIRT-001', '2024-07-10', 0, NULL, 0, 59.99, 59.99, 0, '/products/oxford-shirt');
INSERT INTO wishlists VALUES (8, 'frank@example.com', 'ELEC-PHONE-001', '2024-08-01', 1, 'Upgrade from old phone', 0, 799.99, 799.99, 1, '/products/smartphone-x12');
INSERT INTO wishlists VALUES (9, 'grace@example.com', 'HOME-DESK-001', '2024-09-05', 1, NULL, 1, 599.99, 599.99, 0, '/products/standdesk-pro');
INSERT INTO wishlists VALUES (10, 'hank@example.com', 'BOOK-TECH-001', '2024-09-20', 0, 'Study material', 0, 45.99, 45.99, 0, '/products/db-design-book');

-- ============================================================
-- TABLE 16: returns (6 rows, 11 columns)
-- ============================================================
CREATE TABLE returns (
    id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    customer_email TEXT NOT NULL,
    reason TEXT NOT NULL,
    status TEXT NOT NULL,
    requested_at TEXT NOT NULL,
    approved_at TEXT,
    refund_amount REAL,
    refund_method TEXT,
    processed_by_email TEXT,
    notes TEXT
);

INSERT INTO returns VALUES (1, 7, 'dave@example.com', 'Wrong size', 'completed', '2024-06-05', '2024-06-06', 93.58, 'original_method', 'alice@example.com', 'Full refund issued');
INSERT INTO returns VALUES (2, 14, 'hank@example.com', 'Changed mind', 'completed', '2024-09-29', '2024-09-30', 148.76, 'original_method', 'carol@example.com', 'Cancelled before shipping');
INSERT INTO returns VALUES (3, 5, 'carol@example.com', 'Defective armrest', 'approved', '2024-05-15', '2024-05-16', 149.99, 'store_credit', 'alice@example.com', 'Partial refund for chair only');
INSERT INTO returns VALUES (4, 11, 'frank@example.com', 'Book damaged in transit', 'pending', '2024-08-12', NULL, NULL, NULL, NULL, 'Awaiting photos from customer');
INSERT INTO returns VALUES (5, 9, 'eve@example.com', 'Duplicate order', 'completed', '2024-07-09', '2024-07-10', 53.20, 'original_method', 'carol@example.com', 'Full refund');
INSERT INTO returns VALUES (6, 2, 'alice@example.com', 'Wrong color received', 'rejected', '2024-03-01', '2024-03-02', 0.00, NULL, 'eve@example.com', 'Color matches order specification');

-- ============================================================
-- TABLE 17: suppliers (4 rows, 12 columns)
-- ============================================================
CREATE TABLE suppliers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    contact_name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT,
    address TEXT,
    city TEXT,
    country TEXT NOT NULL DEFAULT 'US',
    payment_terms TEXT NOT NULL DEFAULT 'net30',
    lead_time_days INTEGER NOT NULL DEFAULT 14,
    rating REAL,
    is_active INTEGER NOT NULL DEFAULT 1
);

INSERT INTO suppliers VALUES (1, 'TechSource Inc', 'Mike Chen', 'mike@techsource.com', '555-8001', '500 Tech Park Dr', 'San Jose', 'US', 'net30', 10, 4.8, 1);
INSERT INTO suppliers VALUES (2, 'FurnitureWorld', 'Lisa Park', 'lisa@furnitureworld.com', '555-8002', '250 Industrial Way', 'Grand Rapids', 'US', 'net45', 21, 4.5, 1);
INSERT INTO suppliers VALUES (3, 'GlobalTextiles', 'Raj Patel', 'raj@globaltextiles.com', '555-8003', '88 Cotton Mill Rd', 'Charlotte', 'US', 'net30', 14, 4.2, 1);
INSERT INTO suppliers VALUES (4, 'BookDistributors Co', 'Anna Berg', 'anna@bookdist.com', '555-8004', '175 Library Ln', 'Nashville', 'US', 'net60', 7, 4.9, 1);

-- ============================================================
-- TABLE 18: purchase_orders (10 rows, 12 columns)
-- ============================================================
CREATE TABLE purchase_orders (
    id INTEGER PRIMARY KEY,
    supplier_name TEXT NOT NULL,
    product_sku TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    unit_cost REAL NOT NULL,
    total_cost REAL NOT NULL,
    status TEXT NOT NULL,
    ordered_date TEXT NOT NULL,
    expected_date TEXT,
    received_date TEXT,
    warehouse_name TEXT NOT NULL,
    notes TEXT
);

INSERT INTO purchase_orders VALUES (1, 'TechSource Inc', 'ELEC-LAPTOP-001', 50, 650.00, 32500.00, 'received', '2024-09-15', '2024-09-25', '2024-09-24', 'East Coast Hub', NULL);
INSERT INTO purchase_orders VALUES (2, 'TechSource Inc', 'ELEC-PHONE-001', 100, 480.00, 48000.00, 'received', '2024-10-01', '2024-10-11', '2024-10-10', 'East Coast Hub', 'Bulk discount applied');
INSERT INTO purchase_orders VALUES (3, 'TechSource Inc', 'ELEC-TABLET-001', 60, 320.00, 19200.00, 'received', '2024-09-10', '2024-09-20', '2024-09-19', 'West Coast Depot', NULL);
INSERT INTO purchase_orders VALUES (4, 'FurnitureWorld', 'HOME-CHAIR-001', 25, 180.00, 4500.00, 'received', '2024-08-01', '2024-08-22', '2024-08-20', 'Central Warehouse', NULL);
INSERT INTO purchase_orders VALUES (5, 'FurnitureWorld', 'HOME-DESK-001', 15, 310.00, 4650.00, 'received', '2024-08-15', '2024-09-05', '2024-09-03', 'Central Warehouse', 'Fragile handling required');
INSERT INTO purchase_orders VALUES (6, 'GlobalTextiles', 'CLOTH-SHIRT-001', 200, 22.00, 4400.00, 'received', '2024-10-05', '2024-10-19', '2024-10-18', 'East Coast Hub', NULL);
INSERT INTO purchase_orders VALUES (7, 'GlobalTextiles', 'CLOTH-JEANS-001', 100, 30.00, 3000.00, 'shipped', '2024-11-01', '2024-11-15', NULL, 'West Coast Depot', NULL);
INSERT INTO purchase_orders VALUES (8, 'BookDistributors Co', 'BOOK-TECH-001', 80, 12.00, 960.00, 'received', '2024-10-25', '2024-11-01', '2024-10-31', 'East Coast Hub', NULL);
INSERT INTO purchase_orders VALUES (9, 'BookDistributors Co', 'BOOK-FICTION-001', 300, 5.00, 1500.00, 'received', '2024-10-28', '2024-11-04', '2024-11-03', 'West Coast Depot', 'New print run');
INSERT INTO purchase_orders VALUES (10, 'FurnitureWorld', 'SPORT-YOGA-001', 50, 14.00, 700.00, 'ordered', '2024-11-15', '2024-12-06', NULL, 'Central Warehouse', 'Restock discontinued item');

-- ============================================================
-- TABLE 19: notifications (15 rows, 11 columns)
-- ============================================================
CREATE TABLE notifications (
    id INTEGER PRIMARY KEY,
    recipient_email TEXT NOT NULL,
    type TEXT NOT NULL,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    is_read INTEGER NOT NULL DEFAULT 0,
    channel TEXT NOT NULL DEFAULT 'email',
    priority TEXT NOT NULL DEFAULT 'normal',
    action_url TEXT,
    related_order_id INTEGER,
    created_at TEXT NOT NULL
);

INSERT INTO notifications VALUES (1, 'alice@example.com', 'order_confirmed', 'Order Confirmed', 'Your order #1 has been confirmed', 1, 'email', 'normal', '/orders/1', 1, '2024-01-15 10:35:00');
INSERT INTO notifications VALUES (2, 'alice@example.com', 'order_shipped', 'Order Shipped', 'Your order #1 has been shipped via FedEx', 1, 'email', 'normal', '/orders/1', 1, '2024-01-16 09:00:00');
INSERT INTO notifications VALUES (3, 'bob@example.com', 'order_confirmed', 'Order Confirmed', 'Your order #3 has been confirmed', 1, 'email', 'normal', '/orders/3', 3, '2024-03-05 09:50:00');
INSERT INTO notifications VALUES (4, 'carol@example.com', 'order_delivered', 'Order Delivered', 'Your order #5 has been delivered', 1, 'email', 'normal', '/orders/5', 5, '2024-04-26 14:00:00');
INSERT INTO notifications VALUES (5, 'dave@example.com', 'return_approved', 'Return Approved', 'Your return for order #7 has been approved', 1, 'email', 'high', '/returns/1', 7, '2024-06-06 10:00:00');
INSERT INTO notifications VALUES (6, 'eve@example.com', 'order_confirmed', 'Order Confirmed', 'Your order #8 has been confirmed', 1, 'email', 'normal', '/orders/8', 8, '2024-06-18 15:50:00');
INSERT INTO notifications VALUES (7, 'frank@example.com', 'order_shipped', 'Order Shipped', 'Your order #10 has been shipped via FedEx', 0, 'email', 'normal', '/orders/10', 10, '2024-07-21 09:00:00');
INSERT INTO notifications VALUES (8, 'grace@example.com', 'order_confirmed', 'Order Confirmed', 'Your order #12 is being processed', 1, 'email', 'normal', '/orders/12', 12, '2024-08-22 10:50:00');
INSERT INTO notifications VALUES (9, 'hank@example.com', 'order_cancelled', 'Order Cancelled', 'Your order #14 has been cancelled', 1, 'email', 'high', '/orders/14', 14, '2024-09-28 12:00:00');
INSERT INTO notifications VALUES (10, 'alice@example.com', 'promotion', 'Summer Sale', 'Up to 25% off on all electronics', 0, 'email', 'low', '/sale/summer', NULL, '2024-06-01 08:00:00');
INSERT INTO notifications VALUES (11, 'bob@example.com', 'promotion', 'Summer Sale', 'Up to 25% off on all electronics', 1, 'email', 'low', '/sale/summer', NULL, '2024-06-01 08:00:00');
INSERT INTO notifications VALUES (12, 'carol@example.com', 'review_reminder', 'Leave a Review', 'How was your ProBook Laptop 15?', 0, 'push', 'low', '/reviews/new?product=1', NULL, '2024-05-05 10:00:00');
INSERT INTO notifications VALUES (13, 'eve@example.com', 'price_drop', 'Price Drop Alert', 'ErgoChair Plus is now on sale', 1, 'push', 'normal', '/products/ergochair', NULL, '2024-07-15 12:00:00');
INSERT INTO notifications VALUES (14, 'frank@example.com', 'return_update', 'Return Update', 'Your return for order #11 is under review', 0, 'email', 'normal', '/returns/4', 11, '2024-08-13 09:00:00');
INSERT INTO notifications VALUES (15, 'grace@example.com', 'order_delivered', 'Order Delivered', 'Your order #13 has been delivered', 1, 'email', 'normal', '/orders/13', 13, '2024-09-14 16:00:00');

-- ============================================================
-- TABLE 20: audit_log (20 rows, 11 columns)
-- ============================================================
CREATE TABLE audit_log (
    id INTEGER PRIMARY KEY,
    user_email TEXT NOT NULL,
    action TEXT NOT NULL,
    entity_type TEXT NOT NULL,
    entity_id INTEGER,
    old_value TEXT,
    new_value TEXT,
    ip_address TEXT,
    user_agent TEXT,
    timestamp TEXT NOT NULL,
    session_id TEXT
);

INSERT INTO audit_log VALUES (1, 'alice@example.com', 'login', 'session', NULL, NULL, NULL, '192.168.1.50', 'Mozilla/5.0 Chrome/123', '2024-01-15 10:00:00', 'sess-a001');
INSERT INTO audit_log VALUES (2, 'alice@example.com', 'create_order', 'order', 1, NULL, 'created', '192.168.1.50', 'Mozilla/5.0 Chrome/123', '2024-01-15 10:30:00', 'sess-a001');
INSERT INTO audit_log VALUES (3, 'bob@example.com', 'login', 'session', NULL, NULL, NULL, '192.168.1.10', 'Mozilla/5.0 Chrome/120', '2024-03-05 09:30:00', 'sess-b001');
INSERT INTO audit_log VALUES (4, 'bob@example.com', 'create_order', 'order', 3, NULL, 'created', '192.168.1.10', 'Mozilla/5.0 Chrome/120', '2024-03-05 09:45:00', 'sess-b001');
INSERT INTO audit_log VALUES (5, 'carol@example.com', 'login', 'session', NULL, NULL, NULL, '192.168.1.20', 'Mozilla/5.0 Safari/17', '2024-04-22 10:30:00', 'sess-c001');
INSERT INTO audit_log VALUES (6, 'carol@example.com', 'create_order', 'order', 5, NULL, 'created', '192.168.1.20', 'Mozilla/5.0 Safari/17', '2024-04-22 10:55:00', 'sess-c001');
INSERT INTO audit_log VALUES (7, 'dave@example.com', 'login', 'session', NULL, NULL, NULL, '192.168.1.25', 'Mozilla/5.0 Firefox/120', '2024-06-01 09:45:00', 'sess-d001');
INSERT INTO audit_log VALUES (8, 'dave@example.com', 'create_order', 'order', 7, NULL, 'created', '192.168.1.25', 'Mozilla/5.0 Firefox/120', '2024-06-01 10:00:00', 'sess-d001');
INSERT INTO audit_log VALUES (9, 'dave@example.com', 'request_return', 'return', 1, NULL, 'requested', '192.168.1.25', 'Mozilla/5.0 Firefox/120', '2024-06-05 14:00:00', 'sess-d002');
INSERT INTO audit_log VALUES (10, 'eve@example.com', 'login', 'session', NULL, NULL, NULL, '192.168.1.30', 'Mozilla/5.0 Firefox/121', '2024-06-18 15:30:00', 'sess-e001');
INSERT INTO audit_log VALUES (11, 'eve@example.com', 'create_order', 'order', 8, NULL, 'created', '192.168.1.30', 'Mozilla/5.0 Firefox/121', '2024-06-18 15:45:00', 'sess-e001');
INSERT INTO audit_log VALUES (12, 'frank@example.com', 'login', 'session', NULL, NULL, NULL, '192.168.1.40', 'Mozilla/5.0 Chrome/122', '2024-07-20 09:00:00', 'sess-f001');
INSERT INTO audit_log VALUES (13, 'frank@example.com', 'create_order', 'order', 10, NULL, 'created', '192.168.1.40', 'Mozilla/5.0 Chrome/122', '2024-07-20 09:15:00', 'sess-f001');
INSERT INTO audit_log VALUES (14, 'grace@example.com', 'login', 'session', NULL, NULL, NULL, '192.168.1.60', 'Mozilla/5.0 Edge/120', '2024-08-22 10:30:00', 'sess-g001');
INSERT INTO audit_log VALUES (15, 'grace@example.com', 'create_order', 'order', 12, NULL, 'created', '192.168.1.60', 'Mozilla/5.0 Edge/120', '2024-08-22 10:45:00', 'sess-g001');
INSERT INTO audit_log VALUES (16, 'hank@example.com', 'login', 'session', NULL, NULL, NULL, '192.168.1.70', 'Mozilla/5.0 Chrome/121', '2024-09-28 11:00:00', 'sess-h001');
INSERT INTO audit_log VALUES (17, 'hank@example.com', 'create_order', 'order', 14, NULL, 'created', '192.168.1.70', 'Mozilla/5.0 Chrome/121', '2024-09-28 11:20:00', 'sess-h001');
INSERT INTO audit_log VALUES (18, 'hank@example.com', 'cancel_order', 'order', 14, 'processing', 'cancelled', '192.168.1.70', 'Mozilla/5.0 Chrome/121', '2024-09-28 11:30:00', 'sess-h001');
INSERT INTO audit_log VALUES (19, 'alice@example.com', 'update_profile', 'customer', 1, 'old_phone', '555-0101', '192.168.1.50', 'Mozilla/5.0 Chrome/123', '2024-10-01 14:00:00', 'sess-a002');
INSERT INTO audit_log VALUES (20, 'alice@example.com', 'create_order', 'order', 15, NULL, 'created', '192.168.1.50', 'Mozilla/5.0 Chrome/123', '2024-10-15 15:55:00', 'sess-a003');
"""

TARGET_SQL = """
-- ============================================================
-- TABLE 1: customers (8 rows) — referred_by_email -> referred_by_id FK
-- ============================================================
CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT,
    password_hash TEXT NOT NULL,
    registration_date TEXT NOT NULL,
    last_login TEXT,
    is_active INTEGER NOT NULL DEFAULT 1,
    loyalty_points INTEGER NOT NULL DEFAULT 0,
    referral_code TEXT,
    referred_by_id INTEGER,
    FOREIGN KEY (referred_by_id) REFERENCES customers(id)
);

INSERT INTO customers VALUES (1, 'Alice', 'Johnson', 'alice@example.com', '555-0101', 'pbkdf2_sha256$a1b2c3', '2023-01-15', '2024-11-20', 1, 1250, 'ALICE10', NULL);
INSERT INTO customers VALUES (2, 'Bob', 'Smith', 'bob@example.com', '555-0202', 'pbkdf2_sha256$d4e5f6', '2023-03-22', '2024-11-18', 1, 870, 'BOB20', 1);
INSERT INTO customers VALUES (3, 'Carol', 'Lee', 'carol@example.com', '555-0303', 'pbkdf2_sha256$g7h8i9', '2023-05-10', '2024-11-15', 1, 2100, 'CAROL30', NULL);
INSERT INTO customers VALUES (4, 'Dave', 'Brown', 'dave@example.com', '555-0404', 'pbkdf2_sha256$j0k1l2', '2023-07-01', '2024-10-30', 0, 340, 'DAVE40', 3);
INSERT INTO customers VALUES (5, 'Eve', 'Martinez', 'eve@example.com', '555-0505', 'pbkdf2_sha256$m3n4o5', '2023-08-18', '2024-11-19', 1, 1580, 'EVE50', 1);
INSERT INTO customers VALUES (6, 'Frank', 'Wilson', 'frank@example.com', '555-0606', 'pbkdf2_sha256$p6q7r8', '2023-10-05', '2024-11-10', 1, 620, 'FRANK60', NULL);
INSERT INTO customers VALUES (7, 'Grace', 'Kim', 'grace@example.com', '555-0707', 'pbkdf2_sha256$s9t0u1', '2024-01-12', '2024-11-21', 1, 450, 'GRACE70', 2);
INSERT INTO customers VALUES (8, 'Hank', 'Davis', 'hank@example.com', '555-0808', 'pbkdf2_sha256$v2w3x4', '2024-03-25', '2024-09-05', 0, 90, 'HANK80', 3);

-- ============================================================
-- TABLE 2: customer_addresses (12 rows) — customer_email -> customer_id FK
-- ============================================================
CREATE TABLE customer_addresses (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    address_type TEXT NOT NULL,
    line1 TEXT NOT NULL,
    line2 TEXT,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    zip TEXT NOT NULL,
    country TEXT NOT NULL DEFAULT 'US',
    is_default INTEGER NOT NULL DEFAULT 0,
    phone TEXT,
    instructions TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

INSERT INTO customer_addresses VALUES (1, 1, 'shipping', '123 Oak St', 'Apt 4B', 'Austin', 'TX', '78701', 'US', 1, '555-0101', 'Leave at door');
INSERT INTO customer_addresses VALUES (2, 1, 'billing', '123 Oak St', 'Apt 4B', 'Austin', 'TX', '78701', 'US', 0, '555-0101', NULL);
INSERT INTO customer_addresses VALUES (3, 2, 'shipping', '456 Pine Ave', NULL, 'Portland', 'OR', '97201', 'US', 1, '555-0202', 'Ring bell twice');
INSERT INTO customer_addresses VALUES (4, 2, 'billing', '789 Elm Blvd', 'Suite 100', 'Portland', 'OR', '97202', 'US', 0, '555-0202', NULL);
INSERT INTO customer_addresses VALUES (5, 3, 'shipping', '321 Maple Dr', NULL, 'Chicago', 'IL', '60601', 'US', 1, '555-0303', NULL);
INSERT INTO customer_addresses VALUES (6, 3, 'billing', '321 Maple Dr', NULL, 'Chicago', 'IL', '60601', 'US', 0, '555-0303', NULL);
INSERT INTO customer_addresses VALUES (7, 4, 'shipping', '654 Cedar Ln', 'Unit 7', 'Miami', 'FL', '33101', 'US', 1, '555-0404', 'Gate code 1234');
INSERT INTO customer_addresses VALUES (8, 5, 'shipping', '987 Birch Rd', NULL, 'Denver', 'CO', '80201', 'US', 1, '555-0505', NULL);
INSERT INTO customer_addresses VALUES (9, 5, 'billing', '987 Birch Rd', NULL, 'Denver', 'CO', '80201', 'US', 0, '555-0505', NULL);
INSERT INTO customer_addresses VALUES (10, 6, 'shipping', '147 Walnut St', NULL, 'Seattle', 'WA', '98101', 'US', 1, '555-0606', 'Side entrance');
INSERT INTO customer_addresses VALUES (11, 7, 'shipping', '258 Spruce Ave', 'Floor 3', 'Boston', 'MA', '02101', 'US', 1, '555-0707', NULL);
INSERT INTO customer_addresses VALUES (12, 8, 'shipping', '369 Ash Ct', NULL, 'Phoenix', 'AZ', '85001', 'US', 1, '555-0808', 'Back porch');

-- ============================================================
-- TABLE 3: categories (6 rows) — parent_category_name -> parent_id FK
-- ============================================================
CREATE TABLE categories (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    slug TEXT NOT NULL UNIQUE,
    description TEXT,
    parent_id INTEGER,
    image_url TEXT,
    sort_order INTEGER NOT NULL DEFAULT 0,
    is_active INTEGER NOT NULL DEFAULT 1,
    meta_title TEXT,
    meta_description TEXT,
    product_count INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (parent_id) REFERENCES categories(id)
);

INSERT INTO categories VALUES (1, 'Electronics', 'electronics', 'Electronic devices and gadgets', NULL, 'https://cdn.shop.com/cat-electronics.jpg', 1, 1, 'Electronics Store', 'Shop electronics online', 3);
INSERT INTO categories VALUES (2, 'Home & Office', 'home-office', 'Home and office furniture and supplies', NULL, 'https://cdn.shop.com/cat-home.jpg', 2, 1, 'Home & Office', 'Furniture and office supplies', 2);
INSERT INTO categories VALUES (3, 'Clothing', 'clothing', 'Apparel and fashion', NULL, 'https://cdn.shop.com/cat-clothing.jpg', 3, 1, 'Clothing Store', 'Fashion and apparel', 2);
INSERT INTO categories VALUES (4, 'Books', 'books', 'Books and publications', NULL, 'https://cdn.shop.com/cat-books.jpg', 4, 1, 'Bookstore', 'Books for everyone', 2);
INSERT INTO categories VALUES (5, 'Sports', 'sports', 'Sports and fitness equipment', NULL, 'https://cdn.shop.com/cat-sports.jpg', 5, 1, 'Sports Store', 'Sports and fitness gear', 1);
INSERT INTO categories VALUES (6, 'Laptops', 'laptops', 'Laptop computers', 1, 'https://cdn.shop.com/cat-laptops.jpg', 1, 1, 'Laptops', 'Shop laptops', 1);

-- ============================================================
-- TABLE 4: products (10 rows) — category_name/subcategory_name -> category_id FK
-- ============================================================
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    sku TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    description TEXT,
    category_id INTEGER,
    price REAL NOT NULL,
    cost REAL NOT NULL,
    weight_kg REAL,
    dimensions TEXT,
    brand TEXT,
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

INSERT INTO products VALUES (1, 'ELEC-LAPTOP-001', 'ProBook Laptop 15', 'High-performance laptop with 16GB RAM', 6, 999.99, 650.00, 2.1, '35x24x2 cm', 'TechBrand', 1, '2023-01-10');
INSERT INTO products VALUES (2, 'ELEC-PHONE-001', 'SmartPhone X12', 'Latest smartphone with OLED display', 1, 799.99, 480.00, 0.19, '15x7x0.8 cm', 'TechBrand', 1, '2023-02-15');
INSERT INTO products VALUES (3, 'ELEC-TABLET-001', 'TabletPro 10', '10-inch tablet with stylus support', 1, 549.99, 320.00, 0.48, '25x17x0.7 cm', 'TechBrand', 1, '2023-03-20');
INSERT INTO products VALUES (4, 'HOME-CHAIR-001', 'ErgoChair Plus', 'Ergonomic office chair with lumbar support', 2, 349.99, 180.00, 15.5, '65x65x120 cm', 'ComfortCo', 1, '2023-04-01');
INSERT INTO products VALUES (5, 'HOME-DESK-001', 'StandDesk Pro', 'Electric standing desk adjustable height', 2, 599.99, 310.00, 35.0, '150x75x120 cm', 'ComfortCo', 1, '2023-04-15');
INSERT INTO products VALUES (6, 'CLOTH-SHIRT-001', 'Classic Oxford Shirt', 'Cotton oxford button-down shirt', 3, 59.99, 22.00, 0.3, NULL, 'StyleWear', 1, '2023-05-01');
INSERT INTO products VALUES (7, 'CLOTH-JEANS-001', 'Slim Fit Jeans', 'Dark wash slim fit denim jeans', 3, 79.99, 30.00, 0.8, NULL, 'StyleWear', 1, '2023-05-10');
INSERT INTO products VALUES (8, 'BOOK-TECH-001', 'Database Design Mastery', 'Comprehensive guide to database design', 4, 45.99, 12.00, 0.7, '23x15x3 cm', 'TechPress', 1, '2023-06-01');
INSERT INTO products VALUES (9, 'BOOK-FICTION-001', 'The Last Algorithm', 'Sci-fi thriller about rogue AI', 4, 16.99, 5.00, 0.4, '20x13x2 cm', 'NovelHouse', 1, '2023-06-15');
INSERT INTO products VALUES (10, 'SPORT-YOGA-001', 'Premium Yoga Mat', 'Non-slip eco-friendly yoga mat', 5, 39.99, 14.00, 1.2, '180x60x0.6 cm', 'FitGear', 0, '2023-07-01');

-- ============================================================
-- TABLE 5: product_images (15 rows) — product_sku -> product_id FK
-- ============================================================
CREATE TABLE product_images (
    id INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL,
    url TEXT NOT NULL,
    alt_text TEXT,
    sort_order INTEGER NOT NULL DEFAULT 0,
    is_primary INTEGER NOT NULL DEFAULT 0,
    width INTEGER,
    height INTEGER,
    file_size INTEGER,
    mime_type TEXT NOT NULL DEFAULT 'image/jpeg',
    uploaded_at TEXT NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(id)
);

INSERT INTO product_images VALUES (1, 1, 'https://cdn.shop.com/laptop-front.jpg', 'ProBook Laptop front view', 1, 1, 1200, 900, 245000, 'image/jpeg', '2023-01-10');
INSERT INTO product_images VALUES (2, 1, 'https://cdn.shop.com/laptop-side.jpg', 'ProBook Laptop side view', 2, 0, 1200, 900, 198000, 'image/jpeg', '2023-01-10');
INSERT INTO product_images VALUES (3, 2, 'https://cdn.shop.com/phone-front.jpg', 'SmartPhone X12 front', 1, 1, 800, 1200, 180000, 'image/jpeg', '2023-02-15');
INSERT INTO product_images VALUES (4, 2, 'https://cdn.shop.com/phone-back.jpg', 'SmartPhone X12 back', 2, 0, 800, 1200, 165000, 'image/jpeg', '2023-02-15');
INSERT INTO product_images VALUES (5, 3, 'https://cdn.shop.com/tablet-front.jpg', 'TabletPro 10 front', 1, 1, 1000, 750, 210000, 'image/jpeg', '2023-03-20');
INSERT INTO product_images VALUES (6, 4, 'https://cdn.shop.com/chair-main.jpg', 'ErgoChair Plus main view', 1, 1, 1000, 1000, 320000, 'image/jpeg', '2023-04-01');
INSERT INTO product_images VALUES (7, 4, 'https://cdn.shop.com/chair-detail.jpg', 'ErgoChair Plus lumbar detail', 2, 0, 800, 800, 150000, 'image/jpeg', '2023-04-01');
INSERT INTO product_images VALUES (8, 5, 'https://cdn.shop.com/desk-main.jpg', 'StandDesk Pro main view', 1, 1, 1200, 800, 280000, 'image/jpeg', '2023-04-15');
INSERT INTO product_images VALUES (9, 6, 'https://cdn.shop.com/shirt-main.jpg', 'Classic Oxford Shirt front', 1, 1, 800, 1000, 175000, 'image/jpeg', '2023-05-01');
INSERT INTO product_images VALUES (10, 7, 'https://cdn.shop.com/jeans-main.jpg', 'Slim Fit Jeans front', 1, 1, 800, 1200, 190000, 'image/jpeg', '2023-05-10');
INSERT INTO product_images VALUES (11, 8, 'https://cdn.shop.com/dbbook-cover.jpg', 'Database Design Mastery cover', 1, 1, 600, 900, 120000, 'image/jpeg', '2023-06-01');
INSERT INTO product_images VALUES (12, 9, 'https://cdn.shop.com/lastalgo-cover.jpg', 'The Last Algorithm cover', 1, 1, 600, 900, 110000, 'image/jpeg', '2023-06-15');
INSERT INTO product_images VALUES (13, 10, 'https://cdn.shop.com/yogamat-main.jpg', 'Premium Yoga Mat rolled', 1, 1, 1000, 800, 200000, 'image/jpeg', '2023-07-01');
INSERT INTO product_images VALUES (14, 10, 'https://cdn.shop.com/yogamat-flat.jpg', 'Premium Yoga Mat flat', 2, 0, 1200, 600, 230000, 'image/jpeg', '2023-07-01');
INSERT INTO product_images VALUES (15, 3, 'https://cdn.shop.com/tablet-stylus.jpg', 'TabletPro 10 with stylus', 2, 0, 1000, 750, 195000, 'image/jpeg', '2023-03-20');

-- ============================================================
-- TABLE 6: warehouses (3 rows) — unchanged structurally
-- ============================================================
CREATE TABLE warehouses (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    code TEXT NOT NULL UNIQUE,
    address TEXT NOT NULL,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    zip TEXT NOT NULL,
    country TEXT NOT NULL DEFAULT 'US',
    manager_email TEXT,
    phone TEXT,
    capacity INTEGER NOT NULL DEFAULT 10000,
    is_active INTEGER NOT NULL DEFAULT 1
);

INSERT INTO warehouses VALUES (1, 'East Coast Hub', 'ECH', '100 Warehouse Rd', 'Newark', 'NJ', '07101', 'US', 'alice@example.com', '555-9001', 50000, 1);
INSERT INTO warehouses VALUES (2, 'West Coast Depot', 'WCD', '200 Logistics Blvd', 'Los Angeles', 'CA', '90001', 'US', 'carol@example.com', '555-9002', 40000, 1);
INSERT INTO warehouses VALUES (3, 'Central Warehouse', 'CWH', '300 Distribution Ave', 'Dallas', 'TX', '75201', 'US', 'frank@example.com', '555-9003', 60000, 1);

-- ============================================================
-- TABLE 7: inventory (10 rows) — product_sku -> product_id, warehouse_name -> warehouse_id
-- ============================================================
CREATE TABLE inventory (
    id INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL,
    warehouse_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 0,
    reserved INTEGER NOT NULL DEFAULT 0,
    available INTEGER NOT NULL DEFAULT 0,
    reorder_point INTEGER NOT NULL DEFAULT 10,
    reorder_qty INTEGER NOT NULL DEFAULT 50,
    last_restock TEXT,
    last_sold TEXT,
    cost_per_unit REAL,
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (warehouse_id) REFERENCES warehouses(id)
);

INSERT INTO inventory VALUES (1, 1, 1, 45, 5, 40, 10, 50, '2024-10-01', '2024-11-20', 650.00);
INSERT INTO inventory VALUES (2, 2, 1, 120, 12, 108, 20, 100, '2024-10-15', '2024-11-21', 480.00);
INSERT INTO inventory VALUES (3, 3, 2, 60, 3, 57, 15, 50, '2024-09-20', '2024-11-18', 320.00);
INSERT INTO inventory VALUES (4, 4, 3, 30, 2, 28, 5, 20, '2024-08-15', '2024-11-15', 180.00);
INSERT INTO inventory VALUES (5, 5, 3, 15, 1, 14, 5, 10, '2024-09-01', '2024-11-10', 310.00);
INSERT INTO inventory VALUES (6, 6, 1, 200, 10, 190, 30, 100, '2024-10-20', '2024-11-21', 22.00);
INSERT INTO inventory VALUES (7, 7, 2, 150, 8, 142, 25, 80, '2024-10-10', '2024-11-19', 30.00);
INSERT INTO inventory VALUES (8, 8, 1, 80, 0, 80, 20, 50, '2024-11-01', '2024-11-17', 12.00);
INSERT INTO inventory VALUES (9, 9, 2, 300, 15, 285, 50, 200, '2024-11-05', '2024-11-21', 5.00);
INSERT INTO inventory VALUES (10, 10, 3, 0, 0, 0, 10, 50, '2024-06-01', '2024-08-15', 14.00);

-- ============================================================
-- TABLE 8: suppliers (4 rows) — unchanged structurally
-- ============================================================
CREATE TABLE suppliers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    contact_name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT,
    address TEXT,
    city TEXT,
    country TEXT NOT NULL DEFAULT 'US',
    payment_terms TEXT NOT NULL DEFAULT 'net30',
    lead_time_days INTEGER NOT NULL DEFAULT 14,
    rating REAL,
    is_active INTEGER NOT NULL DEFAULT 1
);

INSERT INTO suppliers VALUES (1, 'TechSource Inc', 'Mike Chen', 'mike@techsource.com', '555-8001', '500 Tech Park Dr', 'San Jose', 'US', 'net30', 10, 4.8, 1);
INSERT INTO suppliers VALUES (2, 'FurnitureWorld', 'Lisa Park', 'lisa@furnitureworld.com', '555-8002', '250 Industrial Way', 'Grand Rapids', 'US', 'net45', 21, 4.5, 1);
INSERT INTO suppliers VALUES (3, 'GlobalTextiles', 'Raj Patel', 'raj@globaltextiles.com', '555-8003', '88 Cotton Mill Rd', 'Charlotte', 'US', 'net30', 14, 4.2, 1);
INSERT INTO suppliers VALUES (4, 'BookDistributors Co', 'Anna Berg', 'anna@bookdist.com', '555-8004', '175 Library Ln', 'Nashville', 'US', 'net60', 7, 4.9, 1);

-- ============================================================
-- TABLE 9: orders (15 rows) — customer_email -> customer_id, shipping address -> shipping_address_id FK
--          shipping table merged in as extra columns
-- ============================================================
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_date TEXT NOT NULL,
    status TEXT NOT NULL,
    shipping_address_id INTEGER,
    subtotal REAL NOT NULL,
    tax REAL NOT NULL,
    shipping_cost REAL NOT NULL DEFAULT 0.0,
    total REAL NOT NULL,
    payment_method TEXT,
    notes TEXT,
    shipping_carrier TEXT,
    shipping_tracking_number TEXT,
    shipping_status TEXT,
    shipped_date TEXT,
    estimated_delivery TEXT,
    actual_delivery TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (shipping_address_id) REFERENCES customer_addresses(id)
);

INSERT INTO orders VALUES (1, 1, '2024-01-15', 'delivered', 1, 999.99, 82.50, 15.00, 1097.49, 'credit_card', NULL, 'FedEx', 'FDX-90001', 'delivered', '2024-01-16', '2024-01-20', '2024-01-19');
INSERT INTO orders VALUES (2, 1, '2024-02-20', 'delivered', 1, 59.99, 4.95, 5.99, 70.93, 'credit_card', 'Gift wrap please', 'USPS', 'USPS-90002', 'delivered', '2024-02-21', '2024-02-25', '2024-02-24');
INSERT INTO orders VALUES (3, 2, '2024-03-05', 'delivered', 3, 799.99, 0.00, 12.00, 811.99, 'paypal', NULL, 'UPS', 'UPS-90003', 'delivered', '2024-03-06', '2024-03-10', '2024-03-09');
INSERT INTO orders VALUES (4, 2, '2024-04-10', 'delivered', 3, 349.99, 28.00, 25.00, 402.99, 'credit_card', NULL, 'FedEx', 'FDX-90004', 'delivered', '2024-04-11', '2024-04-15', '2024-04-14');
INSERT INTO orders VALUES (5, 3, '2024-04-22', 'delivered', 5, 1149.98, 94.87, 20.00, 1264.85, 'credit_card', NULL, 'FedEx', 'FDX-90005', 'delivered', '2024-04-23', '2024-04-27', '2024-04-26');
INSERT INTO orders VALUES (6, 3, '2024-05-15', 'delivered', 5, 62.98, 5.20, 5.99, 74.17, 'paypal', NULL, 'USPS', 'USPS-90006', 'delivered', '2024-05-16', '2024-05-20', '2024-05-19');
INSERT INTO orders VALUES (7, 4, '2024-06-01', 'returned', 7, 79.99, 5.60, 7.99, 93.58, 'credit_card', NULL, 'UPS', 'UPS-90007', 'returned', '2024-06-02', '2024-06-06', '2024-06-05');
INSERT INTO orders VALUES (8, 5, '2024-06-18', 'delivered', 8, 549.99, 38.50, 10.00, 598.49, 'credit_card', 'Expedited shipping', 'FedEx', 'FDX-90008', 'delivered', '2024-06-19', '2024-06-23', '2024-06-22');
INSERT INTO orders VALUES (9, 5, '2024-07-04', 'delivered', 8, 45.99, 3.22, 3.99, 53.20, 'paypal', NULL, 'USPS', 'USPS-90009', 'delivered', '2024-07-05', '2024-07-09', '2024-07-08');
INSERT INTO orders VALUES (10, 6, '2024-07-20', 'shipped', 10, 599.99, 54.00, 0.00, 653.99, 'credit_card', NULL, 'FedEx', 'FDX-90010', 'in_transit', '2024-07-21', '2024-07-25', NULL);
INSERT INTO orders VALUES (11, 6, '2024-08-05', 'delivered', 10, 16.99, 1.53, 3.99, 22.51, 'paypal', NULL, 'USPS', 'USPS-90011', 'delivered', '2024-08-06', '2024-08-10', '2024-08-09');
INSERT INTO orders VALUES (12, 7, '2024-08-22', 'processing', 11, 859.98, 53.32, 15.00, 928.30, 'credit_card', NULL, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO orders VALUES (13, 7, '2024-09-10', 'delivered', 11, 39.99, 2.50, 5.99, 48.48, 'credit_card', NULL, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO orders VALUES (14, 8, '2024-09-28', 'cancelled', 12, 129.98, 10.79, 7.99, 148.76, 'paypal', 'Changed my mind', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO orders VALUES (15, 1, '2024-10-15', 'delivered', 1, 96.98, 8.00, 5.99, 110.97, 'credit_card', NULL, 'UPS', 'UPS-90012', 'delivered', '2024-10-16', '2024-10-20', '2024-10-19');

-- ============================================================
-- TABLE 10: order_items (25 rows) — product_sku -> product_id, drop product_name/product_price
-- ============================================================
CREATE TABLE order_items (
    id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    subtotal REAL NOT NULL,
    discount_amount REAL NOT NULL DEFAULT 0.0,
    tax_amount REAL NOT NULL DEFAULT 0.0,
    status TEXT NOT NULL DEFAULT 'fulfilled',
    tracking_number TEXT,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

INSERT INTO order_items VALUES (1, 1, 1, 1, 999.99, 0.00, 82.50, 'delivered', 'TRK-1001');
INSERT INTO order_items VALUES (2, 2, 6, 1, 59.99, 0.00, 4.95, 'delivered', 'TRK-1002');
INSERT INTO order_items VALUES (3, 3, 2, 1, 799.99, 0.00, 0.00, 'delivered', 'TRK-1003');
INSERT INTO order_items VALUES (4, 4, 4, 1, 349.99, 0.00, 28.00, 'delivered', 'TRK-1004');
INSERT INTO order_items VALUES (5, 5, 1, 1, 999.99, 0.00, 82.50, 'delivered', 'TRK-1005A');
INSERT INTO order_items VALUES (6, 5, 4, 1, 349.99, 200.00, 12.37, 'delivered', 'TRK-1005A');
INSERT INTO order_items VALUES (7, 6, 8, 1, 45.99, 0.00, 3.80, 'delivered', 'TRK-1006');
INSERT INTO order_items VALUES (8, 6, 9, 1, 16.99, 0.00, 1.40, 'delivered', 'TRK-1006');
INSERT INTO order_items VALUES (9, 7, 7, 1, 79.99, 0.00, 5.60, 'returned', 'TRK-1007');
INSERT INTO order_items VALUES (10, 8, 3, 1, 549.99, 0.00, 38.50, 'delivered', 'TRK-1008');
INSERT INTO order_items VALUES (11, 9, 8, 1, 45.99, 0.00, 3.22, 'delivered', 'TRK-1009');
INSERT INTO order_items VALUES (12, 10, 5, 1, 599.99, 0.00, 54.00, 'shipped', 'TRK-1010');
INSERT INTO order_items VALUES (13, 11, 9, 1, 16.99, 0.00, 1.53, 'delivered', 'TRK-1011');
INSERT INTO order_items VALUES (14, 12, 2, 1, 799.99, 0.00, 49.60, 'processing', NULL);
INSERT INTO order_items VALUES (15, 12, 6, 1, 59.99, 0.00, 3.72, 'processing', NULL);
INSERT INTO order_items VALUES (16, 13, 10, 1, 39.99, 0.00, 2.50, 'delivered', 'TRK-1013');
INSERT INTO order_items VALUES (17, 14, 6, 1, 59.99, 0.00, 4.97, 'cancelled', NULL);
INSERT INTO order_items VALUES (18, 14, 7, 1, 79.99, 10.00, 5.82, 'cancelled', NULL);
INSERT INTO order_items VALUES (19, 15, 8, 1, 45.99, 0.00, 3.80, 'delivered', 'TRK-1015A');
INSERT INTO order_items VALUES (20, 15, 9, 3, 50.97, 0.00, 4.21, 'delivered', 'TRK-1015A');
INSERT INTO order_items VALUES (21, 1, 10, 0, 0.00, 0.00, 0.00, 'cancelled', NULL);
INSERT INTO order_items VALUES (22, 3, 6, 0, 0.00, 0.00, 0.00, 'cancelled', NULL);
INSERT INTO order_items VALUES (23, 5, 9, 0, 0.00, 0.00, 0.00, 'cancelled', NULL);
INSERT INTO order_items VALUES (24, 8, 7, 0, 0.00, 0.00, 0.00, 'cancelled', NULL);
INSERT INTO order_items VALUES (25, 12, 8, 0, 0.00, 0.00, 0.00, 'cancelled', NULL);

-- ============================================================
-- TABLE 11: payments (15 rows) — customer_email -> customer_id
-- ============================================================
CREATE TABLE payments (
    id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    customer_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    method TEXT NOT NULL,
    status TEXT NOT NULL,
    transaction_id TEXT,
    gateway TEXT NOT NULL DEFAULT 'stripe',
    processed_at TEXT,
    currency TEXT NOT NULL DEFAULT 'USD',
    refund_amount REAL NOT NULL DEFAULT 0.0,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

INSERT INTO payments VALUES (1, 1, 1, 1097.49, 'credit_card', 'completed', 'TXN-A001', 'stripe', '2024-01-15 10:30:00', 'USD', 0.00);
INSERT INTO payments VALUES (2, 2, 1, 70.93, 'credit_card', 'completed', 'TXN-A002', 'stripe', '2024-02-20 14:15:00', 'USD', 0.00);
INSERT INTO payments VALUES (3, 3, 2, 811.99, 'paypal', 'completed', 'TXN-B001', 'paypal', '2024-03-05 09:45:00', 'USD', 0.00);
INSERT INTO payments VALUES (4, 4, 2, 402.99, 'credit_card', 'completed', 'TXN-B002', 'stripe', '2024-04-10 16:20:00', 'USD', 0.00);
INSERT INTO payments VALUES (5, 5, 3, 1264.85, 'credit_card', 'completed', 'TXN-C001', 'stripe', '2024-04-22 11:00:00', 'USD', 0.00);
INSERT INTO payments VALUES (6, 6, 3, 74.17, 'paypal', 'completed', 'TXN-C002', 'paypal', '2024-05-15 13:30:00', 'USD', 0.00);
INSERT INTO payments VALUES (7, 7, 4, 93.58, 'credit_card', 'refunded', 'TXN-D001', 'stripe', '2024-06-01 10:00:00', 'USD', 93.58);
INSERT INTO payments VALUES (8, 8, 5, 598.49, 'credit_card', 'completed', 'TXN-E001', 'stripe', '2024-06-18 15:45:00', 'USD', 0.00);
INSERT INTO payments VALUES (9, 9, 5, 53.20, 'paypal', 'completed', 'TXN-E002', 'paypal', '2024-07-04 12:00:00', 'USD', 0.00);
INSERT INTO payments VALUES (10, 10, 6, 653.99, 'credit_card', 'completed', 'TXN-F001', 'stripe', '2024-07-20 09:15:00', 'USD', 0.00);
INSERT INTO payments VALUES (11, 11, 6, 22.51, 'paypal', 'completed', 'TXN-F002', 'paypal', '2024-08-05 17:30:00', 'USD', 0.00);
INSERT INTO payments VALUES (12, 12, 7, 928.30, 'credit_card', 'pending', 'TXN-G001', 'stripe', '2024-08-22 10:45:00', 'USD', 0.00);
INSERT INTO payments VALUES (13, 13, 7, 48.48, 'credit_card', 'completed', 'TXN-G002', 'stripe', '2024-09-10 14:00:00', 'USD', 0.00);
INSERT INTO payments VALUES (14, 14, 8, 148.76, 'paypal', 'refunded', 'TXN-H001', 'paypal', '2024-09-28 11:20:00', 'USD', 148.76);
INSERT INTO payments VALUES (15, 15, 1, 110.97, 'credit_card', 'completed', 'TXN-A003', 'stripe', '2024-10-15 16:00:00', 'USD', 0.00);

-- ============================================================
-- TABLE 12: reviews (12 rows) — product_sku -> product_id, customer_email -> customer_id
-- ============================================================
CREATE TABLE reviews (
    id INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL,
    customer_id INTEGER NOT NULL,
    rating INTEGER NOT NULL,
    title TEXT,
    body TEXT,
    is_verified INTEGER NOT NULL DEFAULT 0,
    is_approved INTEGER NOT NULL DEFAULT 1,
    helpful_count INTEGER NOT NULL DEFAULT 0,
    reported_count INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

INSERT INTO reviews VALUES (1, 1, 1, 5, 'Amazing laptop', 'Fast and reliable, great battery life', 1, 1, 24, 0, '2024-01-25');
INSERT INTO reviews VALUES (2, 2, 2, 4, 'Great phone', 'Excellent display but camera could be better', 1, 1, 18, 0, '2024-03-15');
INSERT INTO reviews VALUES (3, 4, 2, 5, 'Perfect for WFH', 'My back pain is gone after switching to this chair', 1, 1, 31, 0, '2024-04-20');
INSERT INTO reviews VALUES (4, 1, 3, 4, 'Solid machine', 'Good performance, a bit heavy', 1, 1, 12, 0, '2024-05-01');
INSERT INTO reviews VALUES (5, 4, 3, 3, 'Decent chair', 'Comfortable but armrests are wobbly', 1, 1, 8, 1, '2024-05-10');
INSERT INTO reviews VALUES (6, 7, 4, 2, 'Poor fit', 'Sizing runs small, had to return', 1, 1, 5, 0, '2024-06-10');
INSERT INTO reviews VALUES (7, 3, 5, 5, 'Love this tablet', 'Perfect for drawing and note taking', 1, 1, 20, 0, '2024-06-28');
INSERT INTO reviews VALUES (8, 8, 5, 4, 'Great reference', 'Well-written database guide', 1, 1, 15, 0, '2024-07-10');
INSERT INTO reviews VALUES (9, 5, 6, 5, 'Best desk ever', 'Smooth motor, very sturdy', 1, 1, 27, 0, '2024-07-30');
INSERT INTO reviews VALUES (10, 9, 6, 3, 'OK read', 'Interesting premise but slow middle', 1, 1, 6, 0, '2024-08-12');
INSERT INTO reviews VALUES (11, 2, 7, 5, 'Incredible phone', 'Best phone I have ever owned', 1, 0, 0, 0, '2024-09-15');
INSERT INTO reviews VALUES (12, 10, 7, 4, 'Nice mat', 'Good grip and easy to clean', 1, 1, 9, 0, '2024-09-20');

-- ============================================================
-- TABLE 13: coupons (6 rows) — created_by_email -> created_by_id FK (nullable)
-- ============================================================
CREATE TABLE coupons (
    id INTEGER PRIMARY KEY,
    code TEXT NOT NULL UNIQUE,
    description TEXT,
    discount_type TEXT NOT NULL,
    discount_value REAL NOT NULL,
    min_order_amount REAL NOT NULL DEFAULT 0.0,
    max_uses INTEGER,
    current_uses INTEGER NOT NULL DEFAULT 0,
    valid_from TEXT NOT NULL,
    valid_until TEXT,
    is_active INTEGER NOT NULL DEFAULT 1,
    created_by_id INTEGER,
    FOREIGN KEY (created_by_id) REFERENCES customers(id)
);

INSERT INTO coupons VALUES (1, 'WELCOME10', 'Welcome discount 10%', 'percentage', 10.0, 50.00, 1000, 156, '2024-01-01', '2024-12-31', 1, 1);
INSERT INTO coupons VALUES (2, 'SUMMER25', 'Summer sale $25 off', 'fixed', 25.0, 100.00, 500, 89, '2024-06-01', '2024-08-31', 0, 3);
INSERT INTO coupons VALUES (3, 'FREESHIP', 'Free shipping on all orders', 'shipping', 100.0, 0.00, NULL, 312, '2024-01-01', NULL, 1, 1);
INSERT INTO coupons VALUES (4, 'VIP20', 'VIP customer 20% off', 'percentage', 20.0, 200.00, 100, 23, '2024-03-01', '2025-03-01', 1, 3);
INSERT INTO coupons VALUES (5, 'FLASH50', 'Flash sale $50 off electronics', 'fixed', 50.0, 500.00, 50, 50, '2024-11-01', '2024-11-03', 0, NULL);
INSERT INTO coupons VALUES (6, 'LOYALTY15', 'Loyalty program 15% off', 'percentage', 15.0, 75.00, NULL, 45, '2024-06-01', NULL, 1, 5);

-- ============================================================
-- TABLE 14: coupon_usage (8 rows) — coupon_code -> coupon_id, customer_email -> customer_id
-- ============================================================
CREATE TABLE coupon_usage (
    id INTEGER PRIMARY KEY,
    coupon_id INTEGER NOT NULL,
    customer_id INTEGER NOT NULL,
    order_id INTEGER NOT NULL,
    discount_applied REAL NOT NULL,
    used_at TEXT NOT NULL,
    ip_address TEXT,
    user_agent TEXT,
    session_id TEXT,
    is_first_use INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (coupon_id) REFERENCES coupons(id),
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (order_id) REFERENCES orders(id)
);

INSERT INTO coupon_usage VALUES (1, 1, 2, 3, 80.00, '2024-03-05 09:40:00', '192.168.1.10', 'Mozilla/5.0 Chrome/120', 'sess-b001', 1);
INSERT INTO coupon_usage VALUES (2, 3, 3, 5, 20.00, '2024-04-22 10:55:00', '192.168.1.20', 'Mozilla/5.0 Safari/17', 'sess-c001', 1);
INSERT INTO coupon_usage VALUES (3, 2, 5, 8, 25.00, '2024-06-18 15:40:00', '192.168.1.30', 'Mozilla/5.0 Firefox/121', 'sess-e001', 1);
INSERT INTO coupon_usage VALUES (4, 4, 3, 6, 12.60, '2024-05-15 13:25:00', '192.168.1.20', 'Mozilla/5.0 Safari/17', 'sess-c002', 0);
INSERT INTO coupon_usage VALUES (5, 3, 6, 10, 0.00, '2024-07-20 09:10:00', '192.168.1.40', 'Mozilla/5.0 Chrome/122', 'sess-f001', 1);
INSERT INTO coupon_usage VALUES (6, 6, 1, 15, 14.55, '2024-10-15 15:55:00', '192.168.1.50', 'Mozilla/5.0 Chrome/123', 'sess-a003', 1);
INSERT INTO coupon_usage VALUES (7, 1, 7, 12, 85.99, '2024-08-22 10:40:00', '192.168.1.60', 'Mozilla/5.0 Edge/120', 'sess-g001', 1);
INSERT INTO coupon_usage VALUES (8, 2, 8, 14, 25.00, '2024-09-28 11:15:00', '192.168.1.70', 'Mozilla/5.0 Chrome/121', 'sess-h001', 1);

-- ============================================================
-- TABLE 15: wishlists (10 rows) — customer_email -> customer_id, product_sku -> product_id
-- ============================================================
CREATE TABLE wishlists (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    added_at TEXT NOT NULL,
    priority INTEGER NOT NULL DEFAULT 0,
    notes TEXT,
    is_public INTEGER NOT NULL DEFAULT 0,
    price_at_add REAL NOT NULL,
    current_price REAL NOT NULL,
    notify_on_sale INTEGER NOT NULL DEFAULT 0,
    source_page TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

INSERT INTO wishlists VALUES (1, 1, 2, '2024-02-01', 1, 'Want for birthday', 1, 799.99, 799.99, 1, '/products/smartphone-x12');
INSERT INTO wishlists VALUES (2, 1, 5, '2024-03-10', 2, NULL, 0, 599.99, 599.99, 1, '/products/standdesk-pro');
INSERT INTO wishlists VALUES (3, 2, 3, '2024-04-05', 1, 'For drawing', 1, 549.99, 549.99, 0, '/products/tabletpro-10');
INSERT INTO wishlists VALUES (4, 3, 7, '2024-05-20', 0, NULL, 0, 79.99, 79.99, 0, '/products/slim-jeans');
INSERT INTO wishlists VALUES (5, 4, 1, '2024-06-15', 1, 'Need for work', 0, 999.99, 999.99, 1, '/products/probook-laptop');
INSERT INTO wishlists VALUES (6, 5, 4, '2024-07-01', 2, 'Home office upgrade', 1, 349.99, 349.99, 1, '/products/ergochair');
INSERT INTO wishlists VALUES (7, 5, 6, '2024-07-10', 0, NULL, 0, 59.99, 59.99, 0, '/products/oxford-shirt');
INSERT INTO wishlists VALUES (8, 6, 2, '2024-08-01', 1, 'Upgrade from old phone', 0, 799.99, 799.99, 1, '/products/smartphone-x12');
INSERT INTO wishlists VALUES (9, 7, 5, '2024-09-05', 1, NULL, 1, 599.99, 599.99, 0, '/products/standdesk-pro');
INSERT INTO wishlists VALUES (10, 8, 8, '2024-09-20', 0, 'Study material', 0, 45.99, 45.99, 0, '/products/db-design-book');

-- ============================================================
-- TABLE 16: returns (6 rows) — customer_email -> customer_id, processed_by_email -> processed_by_id
-- ============================================================
CREATE TABLE returns (
    id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    customer_id INTEGER NOT NULL,
    reason TEXT NOT NULL,
    status TEXT NOT NULL,
    requested_at TEXT NOT NULL,
    approved_at TEXT,
    refund_amount REAL,
    refund_method TEXT,
    processed_by_id INTEGER,
    notes TEXT,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (processed_by_id) REFERENCES customers(id)
);

INSERT INTO returns VALUES (1, 7, 4, 'Wrong size', 'completed', '2024-06-05', '2024-06-06', 93.58, 'original_method', 1, 'Full refund issued');
INSERT INTO returns VALUES (2, 14, 8, 'Changed mind', 'completed', '2024-09-29', '2024-09-30', 148.76, 'original_method', 3, 'Cancelled before shipping');
INSERT INTO returns VALUES (3, 5, 3, 'Defective armrest', 'approved', '2024-05-15', '2024-05-16', 149.99, 'store_credit', 1, 'Partial refund for chair only');
INSERT INTO returns VALUES (4, 11, 6, 'Book damaged in transit', 'pending', '2024-08-12', NULL, NULL, NULL, NULL, 'Awaiting photos from customer');
INSERT INTO returns VALUES (5, 9, 5, 'Duplicate order', 'completed', '2024-07-09', '2024-07-10', 53.20, 'original_method', 3, 'Full refund');
INSERT INTO returns VALUES (6, 2, 1, 'Wrong color received', 'rejected', '2024-03-01', '2024-03-02', 0.00, NULL, 5, 'Color matches order specification');

-- ============================================================
-- TABLE 17: purchase_orders (10 rows) — supplier_name -> supplier_id, product_sku -> product_id, warehouse_name -> warehouse_id
-- ============================================================
CREATE TABLE purchase_orders (
    id INTEGER PRIMARY KEY,
    supplier_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_cost REAL NOT NULL,
    total_cost REAL NOT NULL,
    status TEXT NOT NULL,
    ordered_date TEXT NOT NULL,
    expected_date TEXT,
    received_date TEXT,
    warehouse_id INTEGER NOT NULL,
    notes TEXT,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(id),
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (warehouse_id) REFERENCES warehouses(id)
);

INSERT INTO purchase_orders VALUES (1, 1, 1, 50, 650.00, 32500.00, 'received', '2024-09-15', '2024-09-25', '2024-09-24', 1, NULL);
INSERT INTO purchase_orders VALUES (2, 1, 2, 100, 480.00, 48000.00, 'received', '2024-10-01', '2024-10-11', '2024-10-10', 1, 'Bulk discount applied');
INSERT INTO purchase_orders VALUES (3, 1, 3, 60, 320.00, 19200.00, 'received', '2024-09-10', '2024-09-20', '2024-09-19', 2, NULL);
INSERT INTO purchase_orders VALUES (4, 2, 4, 25, 180.00, 4500.00, 'received', '2024-08-01', '2024-08-22', '2024-08-20', 3, NULL);
INSERT INTO purchase_orders VALUES (5, 2, 5, 15, 310.00, 4650.00, 'received', '2024-08-15', '2024-09-05', '2024-09-03', 3, 'Fragile handling required');
INSERT INTO purchase_orders VALUES (6, 3, 6, 200, 22.00, 4400.00, 'received', '2024-10-05', '2024-10-19', '2024-10-18', 1, NULL);
INSERT INTO purchase_orders VALUES (7, 3, 7, 100, 30.00, 3000.00, 'shipped', '2024-11-01', '2024-11-15', NULL, 2, NULL);
INSERT INTO purchase_orders VALUES (8, 4, 8, 80, 12.00, 960.00, 'received', '2024-10-25', '2024-11-01', '2024-10-31', 1, NULL);
INSERT INTO purchase_orders VALUES (9, 4, 9, 300, 5.00, 1500.00, 'received', '2024-10-28', '2024-11-04', '2024-11-03', 2, 'New print run');
INSERT INTO purchase_orders VALUES (10, 2, 10, 50, 14.00, 700.00, 'ordered', '2024-11-15', '2024-12-06', NULL, 3, 'Restock discontinued item');

-- ============================================================
-- TABLE 18: notifications (15 rows) — recipient_email -> recipient_id
-- ============================================================
CREATE TABLE notifications (
    id INTEGER PRIMARY KEY,
    recipient_id INTEGER NOT NULL,
    type TEXT NOT NULL,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    is_read INTEGER NOT NULL DEFAULT 0,
    channel TEXT NOT NULL DEFAULT 'email',
    priority TEXT NOT NULL DEFAULT 'normal',
    action_url TEXT,
    related_order_id INTEGER,
    created_at TEXT NOT NULL,
    FOREIGN KEY (recipient_id) REFERENCES customers(id),
    FOREIGN KEY (related_order_id) REFERENCES orders(id)
);

INSERT INTO notifications VALUES (1, 1, 'order_confirmed', 'Order Confirmed', 'Your order #1 has been confirmed', 1, 'email', 'normal', '/orders/1', 1, '2024-01-15 10:35:00');
INSERT INTO notifications VALUES (2, 1, 'order_shipped', 'Order Shipped', 'Your order #1 has been shipped via FedEx', 1, 'email', 'normal', '/orders/1', 1, '2024-01-16 09:00:00');
INSERT INTO notifications VALUES (3, 2, 'order_confirmed', 'Order Confirmed', 'Your order #3 has been confirmed', 1, 'email', 'normal', '/orders/3', 3, '2024-03-05 09:50:00');
INSERT INTO notifications VALUES (4, 3, 'order_delivered', 'Order Delivered', 'Your order #5 has been delivered', 1, 'email', 'normal', '/orders/5', 5, '2024-04-26 14:00:00');
INSERT INTO notifications VALUES (5, 4, 'return_approved', 'Return Approved', 'Your return for order #7 has been approved', 1, 'email', 'high', '/returns/1', 7, '2024-06-06 10:00:00');
INSERT INTO notifications VALUES (6, 5, 'order_confirmed', 'Order Confirmed', 'Your order #8 has been confirmed', 1, 'email', 'normal', '/orders/8', 8, '2024-06-18 15:50:00');
INSERT INTO notifications VALUES (7, 6, 'order_shipped', 'Order Shipped', 'Your order #10 has been shipped via FedEx', 0, 'email', 'normal', '/orders/10', 10, '2024-07-21 09:00:00');
INSERT INTO notifications VALUES (8, 7, 'order_confirmed', 'Order Confirmed', 'Your order #12 is being processed', 1, 'email', 'normal', '/orders/12', 12, '2024-08-22 10:50:00');
INSERT INTO notifications VALUES (9, 8, 'order_cancelled', 'Order Cancelled', 'Your order #14 has been cancelled', 1, 'email', 'high', '/orders/14', 14, '2024-09-28 12:00:00');
INSERT INTO notifications VALUES (10, 1, 'promotion', 'Summer Sale', 'Up to 25% off on all electronics', 0, 'email', 'low', '/sale/summer', NULL, '2024-06-01 08:00:00');
INSERT INTO notifications VALUES (11, 2, 'promotion', 'Summer Sale', 'Up to 25% off on all electronics', 1, 'email', 'low', '/sale/summer', NULL, '2024-06-01 08:00:00');
INSERT INTO notifications VALUES (12, 3, 'review_reminder', 'Leave a Review', 'How was your ProBook Laptop 15?', 0, 'push', 'low', '/reviews/new?product=1', NULL, '2024-05-05 10:00:00');
INSERT INTO notifications VALUES (13, 5, 'price_drop', 'Price Drop Alert', 'ErgoChair Plus is now on sale', 1, 'push', 'normal', '/products/ergochair', NULL, '2024-07-15 12:00:00');
INSERT INTO notifications VALUES (14, 6, 'return_update', 'Return Update', 'Your return for order #11 is under review', 0, 'email', 'normal', '/returns/4', 11, '2024-08-13 09:00:00');
INSERT INTO notifications VALUES (15, 7, 'order_delivered', 'Order Delivered', 'Your order #13 has been delivered', 1, 'email', 'normal', '/orders/13', 13, '2024-09-14 16:00:00');

-- ============================================================
-- DROPPED TABLES: audit_log (legacy), shipping (merged into orders)
-- ============================================================

-- ============================================================
-- NEW COMPUTED/ANALYTICS TABLES (not in initial schema)
-- ============================================================

CREATE TABLE product_stats (
    id INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL UNIQUE,
    total_sold INTEGER NOT NULL DEFAULT 0,
    total_revenue REAL NOT NULL DEFAULT 0.0,
    avg_rating REAL,
    review_count INTEGER NOT NULL DEFAULT 0,
    wishlist_count INTEGER NOT NULL DEFAULT 0,
    return_rate REAL NOT NULL DEFAULT 0.0,
    FOREIGN KEY (product_id) REFERENCES products(id)
);
INSERT INTO product_stats VALUES (1, 1, 3, 3299.97, 4.5, 2, 1, 0.0);
INSERT INTO product_stats VALUES (2, 2, 4, 1199.96, 4.0, 2, 2, 0.0);
INSERT INTO product_stats VALUES (3, 3, 2, 399.98, 4.0, 1, 0, 0.0);
INSERT INTO product_stats VALUES (4, 4, 3, 2399.97, 5.0, 1, 1, 0.33);
INSERT INTO product_stats VALUES (5, 5, 3, 749.97, 3.5, 2, 1, 0.0);
INSERT INTO product_stats VALUES (6, 6, 2, 599.98, 5.0, 1, 1, 0.0);
INSERT INTO product_stats VALUES (7, 7, 2, 59.98, 3.0, 1, 2, 0.0);
INSERT INTO product_stats VALUES (8, 8, 3, 239.97, 4.0, 1, 1, 0.0);
INSERT INTO product_stats VALUES (9, 9, 2, 119.98, NULL, 0, 0, 0.0);
INSERT INTO product_stats VALUES (10, 10, 1, 39.99, 5.0, 1, 1, 0.0);

CREATE TABLE customer_stats (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL UNIQUE,
    total_orders INTEGER NOT NULL DEFAULT 0,
    total_spent REAL NOT NULL DEFAULT 0.0,
    avg_order_value REAL,
    total_reviews INTEGER NOT NULL DEFAULT 0,
    loyalty_tier TEXT NOT NULL DEFAULT 'bronze',
    first_order_date TEXT,
    last_order_date TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);
INSERT INTO customer_stats VALUES (1, 1, 3, 1839.95, 613.32, 2, 'gold', '2024-03-15', '2024-07-20');
INSERT INTO customer_stats VALUES (2, 2, 2, 1579.97, 789.99, 2, 'gold', '2024-04-02', '2024-06-15');
INSERT INTO customer_stats VALUES (3, 3, 2, 859.97, 429.99, 2, 'silver', '2024-04-20', '2024-05-28');
INSERT INTO customer_stats VALUES (4, 4, 2, 1549.97, 775.0, 1, 'silver', '2024-05-10', '2024-08-18');
INSERT INTO customer_stats VALUES (5, 5, 2, 699.97, 350.0, 2, 'silver', '2024-06-15', '2024-07-22');
INSERT INTO customer_stats VALUES (6, 6, 2, 1119.97, 560.0, 1, 'silver', '2024-07-01', '2024-08-10');
INSERT INTO customer_stats VALUES (7, 7, 2, 1289.97, 645.0, 2, 'gold', '2024-08-20', '2024-09-15');
INSERT INTO customer_stats VALUES (8, 8, 1, 169.98, 169.98, 0, 'bronze', '2024-09-25', '2024-09-25');

CREATE TABLE category_tree (
    id INTEGER PRIMARY KEY,
    category_id INTEGER NOT NULL UNIQUE,
    parent_id INTEGER,
    depth INTEGER NOT NULL DEFAULT 0,
    path TEXT NOT NULL,
    product_count INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (category_id) REFERENCES categories(id),
    FOREIGN KEY (parent_id) REFERENCES categories(id)
);
INSERT INTO category_tree VALUES (1, 1, NULL, 0, '/electronics', 4);
INSERT INTO category_tree VALUES (2, 2, NULL, 0, '/furniture', 2);
INSERT INTO category_tree VALUES (3, 3, 1, 1, '/electronics/laptops', 2);
INSERT INTO category_tree VALUES (4, 4, 1, 1, '/electronics/accessories', 2);
INSERT INTO category_tree VALUES (5, 5, 2, 1, '/furniture/office', 2);
INSERT INTO category_tree VALUES (6, 6, NULL, 0, '/outdoor', 2);

CREATE TABLE shipping_zones (
    id INTEGER PRIMARY KEY,
    state TEXT NOT NULL,
    zone_name TEXT NOT NULL,
    base_rate REAL NOT NULL,
    per_kg_rate REAL NOT NULL,
    estimated_days_min INTEGER NOT NULL,
    estimated_days_max INTEGER NOT NULL,
    is_active INTEGER NOT NULL DEFAULT 1
);
INSERT INTO shipping_zones VALUES (1, 'NY', 'Northeast', 5.99, 0.50, 2, 5, 1);
INSERT INTO shipping_zones VALUES (2, 'CA', 'West Coast', 7.99, 0.75, 3, 7, 1);
INSERT INTO shipping_zones VALUES (3, 'TX', 'South Central', 6.99, 0.60, 2, 6, 1);
INSERT INTO shipping_zones VALUES (4, 'IL', 'Midwest', 5.99, 0.55, 2, 5, 1);
INSERT INTO shipping_zones VALUES (5, 'WA', 'Pacific NW', 7.99, 0.70, 3, 7, 1);
INSERT INTO shipping_zones VALUES (6, 'FL', 'Southeast', 6.49, 0.55, 2, 6, 1);
INSERT INTO shipping_zones VALUES (7, 'CO', 'Mountain', 6.99, 0.65, 3, 6, 1);

CREATE TABLE order_status_history (
    id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    status TEXT NOT NULL,
    changed_at TEXT NOT NULL,
    changed_by TEXT NOT NULL DEFAULT 'system',
    notes TEXT,
    FOREIGN KEY (order_id) REFERENCES orders(id)
);
INSERT INTO order_status_history VALUES (1, 1, 'pending', '2024-03-15 10:00:00', 'system', 'Order placed');
INSERT INTO order_status_history VALUES (2, 1, 'confirmed', '2024-03-15 10:05:00', 'system', 'Payment confirmed');
INSERT INTO order_status_history VALUES (3, 1, 'shipped', '2024-03-17 09:00:00', 'system', 'Shipped via UPS');
INSERT INTO order_status_history VALUES (4, 1, 'delivered', '2024-03-20 14:30:00', 'system', 'Delivered');
INSERT INTO order_status_history VALUES (5, 2, 'pending', '2024-04-02 14:30:00', 'system', 'Order placed');
INSERT INTO order_status_history VALUES (6, 2, 'confirmed', '2024-04-02 14:35:00', 'system', 'Payment confirmed');
INSERT INTO order_status_history VALUES (7, 2, 'shipped', '2024-04-04 08:00:00', 'system', 'Shipped via FedEx');
INSERT INTO order_status_history VALUES (8, 2, 'delivered', '2024-04-08 11:00:00', 'system', 'Delivered');
INSERT INTO order_status_history VALUES (9, 14, 'pending', '2024-09-25 14:00:00', 'system', 'Order placed');
INSERT INTO order_status_history VALUES (10, 14, 'cancelled', '2024-09-28 12:00:00', 'customer', 'Customer requested cancellation');

CREATE TABLE supplier_products (
    id INTEGER PRIMARY KEY,
    supplier_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    unit_cost REAL NOT NULL,
    lead_time_days INTEGER NOT NULL,
    is_preferred INTEGER NOT NULL DEFAULT 0,
    min_order_qty INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);
INSERT INTO supplier_products VALUES (1, 1, 1, 750.00, 14, 1, 5);
INSERT INTO supplier_products VALUES (2, 1, 2, 180.00, 10, 1, 10);
INSERT INTO supplier_products VALUES (3, 2, 3, 130.00, 7, 1, 20);
INSERT INTO supplier_products VALUES (4, 2, 4, 550.00, 14, 1, 3);
INSERT INTO supplier_products VALUES (5, 3, 5, 160.00, 5, 1, 10);
INSERT INTO supplier_products VALUES (6, 3, 6, 200.00, 7, 1, 5);
INSERT INTO supplier_products VALUES (7, 4, 7, 15.00, 3, 1, 50);
INSERT INTO supplier_products VALUES (8, 4, 8, 50.00, 5, 1, 20);
INSERT INTO supplier_products VALUES (9, 1, 9, 35.00, 7, 0, 15);
INSERT INTO supplier_products VALUES (10, 2, 10, 22.00, 5, 1, 30);

CREATE TABLE inventory_movements (
    id INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL,
    warehouse_id INTEGER NOT NULL,
    movement_type TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    reference_id INTEGER,
    notes TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (warehouse_id) REFERENCES warehouses(id)
);
INSERT INTO inventory_movements VALUES (1, 1, 1, 'restock', 50, NULL, 'Initial stock', '2024-01-15 10:00:00');
INSERT INTO inventory_movements VALUES (2, 1, 1, 'sale', -1, 1, 'Order #1', '2024-03-15 10:05:00');
INSERT INTO inventory_movements VALUES (3, 2, 1, 'restock', 100, NULL, 'Initial stock', '2024-01-15 10:00:00');
INSERT INTO inventory_movements VALUES (4, 2, 2, 'sale', -2, 2, 'Order #2', '2024-04-02 14:35:00');
INSERT INTO inventory_movements VALUES (5, 5, 2, 'restock', 30, NULL, 'Restocked', '2024-05-01 09:00:00');
INSERT INTO inventory_movements VALUES (6, 5, 2, 'sale', -1, 5, 'Order #5', '2024-06-15 12:30:00');
INSERT INTO inventory_movements VALUES (7, 4, 1, 'return', 1, 1, 'Return from order #5', '2024-06-25 10:00:00');
INSERT INTO inventory_movements VALUES (8, 8, 3, 'sale', -1, 12, 'Order #12', '2024-08-22 10:55:00');
"""
