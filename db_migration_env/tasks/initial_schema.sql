-- ShopLocal Legacy Schema
-- No foreign keys, no indexes, text-based references everywhere

CREATE TABLE sl_customers (
    cid INTEGER PRIMARY KEY,
    cust_fname TEXT NOT NULL,
    cust_lname TEXT NOT NULL,
    cust_email TEXT NOT NULL,
    cust_phone TEXT,
    cust_pass TEXT NOT NULL,
    cust_addr_line1 TEXT,
    cust_addr_city TEXT,
    cust_addr_state TEXT,
    cust_addr_zip TEXT,
    cust_country TEXT DEFAULT 'US',
    cust_dob TEXT,
    cust_joined TEXT,
    cust_last_login TEXT,
    cust_is_active INTEGER DEFAULT 1
);

INSERT INTO sl_customers (cid, cust_fname, cust_lname, cust_email, cust_phone, cust_pass, cust_addr_line1, cust_addr_city, cust_addr_state, cust_addr_zip, cust_country, cust_dob, cust_joined, cust_last_login, cust_is_active) VALUES (1, 'Alice', 'Chen', 'alice@email.com', '555-0101', 'hashed_pw_alice01', '123 Maple St', 'Portland', 'OR', '97201', 'US', '1990-03-15', '2021-01-10', '2025-03-28', 1);
INSERT INTO sl_customers (cid, cust_fname, cust_lname, cust_email, cust_phone, cust_pass, cust_addr_line1, cust_addr_city, cust_addr_state, cust_addr_zip, cust_country, cust_dob, cust_joined, cust_last_login, cust_is_active) VALUES (2, 'Bob', 'Rivera', 'bob@email.com', '555-0102', 'hashed_pw_bob02', '456 Oak Ave', 'Austin', 'TX', '78701', 'US', '1985-07-22', '2021-03-05', '2025-03-25', 1);
INSERT INTO sl_customers (cid, cust_fname, cust_lname, cust_email, cust_phone, cust_pass, cust_addr_line1, cust_addr_city, cust_addr_state, cust_addr_zip, cust_country, cust_dob, cust_joined, cust_last_login, cust_is_active) VALUES (3, 'Carol', 'Zhang', 'carol@email.com', '555-0103', 'hashed_pw_carol03', '789 Pine Rd', 'Seattle', 'WA', '98101', 'US', '1992-11-08', '2021-06-18', '2025-03-27', 1);
INSERT INTO sl_customers (cid, cust_fname, cust_lname, cust_email, cust_phone, cust_pass, cust_addr_line1, cust_addr_city, cust_addr_state, cust_addr_zip, cust_country, cust_dob, cust_joined, cust_last_login, cust_is_active) VALUES (4, 'Dave', 'Wilson', 'dave@email.com', '555-0104', 'hashed_pw_dave04', '321 Elm Blvd', 'Denver', 'CO', '80201', 'US', '1988-01-30', '2022-01-12', '2025-03-20', 1);
INSERT INTO sl_customers (cid, cust_fname, cust_lname, cust_email, cust_phone, cust_pass, cust_addr_line1, cust_addr_city, cust_addr_state, cust_addr_zip, cust_country, cust_dob, cust_joined, cust_last_login, cust_is_active) VALUES (5, 'Eve', 'Thompson', 'eve@email.com', '555-0105', 'hashed_pw_eve05', '654 Birch Ln', 'Miami', 'FL', '33101', 'US', '1995-05-12', '2022-04-20', '2025-03-26', 1);
INSERT INTO sl_customers (cid, cust_fname, cust_lname, cust_email, cust_phone, cust_pass, cust_addr_line1, cust_addr_city, cust_addr_state, cust_addr_zip, cust_country, cust_dob, cust_joined, cust_last_login, cust_is_active) VALUES (6, 'Frank', 'Garcia', 'frank@email.com', '555-0106', 'hashed_pw_frank06', '987 Cedar Ct', 'Chicago', 'IL', '60601', 'US', '1983-09-25', '2022-07-01', '2025-03-15', 1);
INSERT INTO sl_customers (cid, cust_fname, cust_lname, cust_email, cust_phone, cust_pass, cust_addr_line1, cust_addr_city, cust_addr_state, cust_addr_zip, cust_country, cust_dob, cust_joined, cust_last_login, cust_is_active) VALUES (7, 'Grace', 'Kim', 'grace@email.com', '555-0107', 'hashed_pw_grace07', '147 Walnut Dr', 'San Francisco', 'CA', '94101', 'US', '1991-12-03', '2022-09-14', '2025-03-28', 1);
INSERT INTO sl_customers (cid, cust_fname, cust_lname, cust_email, cust_phone, cust_pass, cust_addr_line1, cust_addr_city, cust_addr_state, cust_addr_zip, cust_country, cust_dob, cust_joined, cust_last_login, cust_is_active) VALUES (8, 'Henry', 'Patel', 'henry@email.com', '555-0108', 'hashed_pw_henry08', '258 Spruce Way', 'Boston', 'MA', '02101', 'US', '1987-04-18', '2023-01-22', '2025-03-22', 1);
INSERT INTO sl_customers (cid, cust_fname, cust_lname, cust_email, cust_phone, cust_pass, cust_addr_line1, cust_addr_city, cust_addr_state, cust_addr_zip, cust_country, cust_dob, cust_joined, cust_last_login, cust_is_active) VALUES (9, 'Ivy', 'Santos', 'ivy@email.com', '555-0109', 'hashed_pw_ivy09', '369 Ash Pl', 'Phoenix', 'AZ', '85001', 'US', '1994-08-07', '2023-05-10', '2025-03-24', 1);
INSERT INTO sl_customers (cid, cust_fname, cust_lname, cust_email, cust_phone, cust_pass, cust_addr_line1, cust_addr_city, cust_addr_state, cust_addr_zip, cust_country, cust_dob, cust_joined, cust_last_login, cust_is_active) VALUES (10, 'Jack', 'Murphy', 'jack@email.com', '555-0110', 'hashed_pw_jack10', '480 Poplar St', 'Nashville', 'TN', '37201', 'US', '1986-02-14', '2023-08-03', '2025-03-18', 1);
INSERT INTO sl_customers (cid, cust_fname, cust_lname, cust_email, cust_phone, cust_pass, cust_addr_line1, cust_addr_city, cust_addr_state, cust_addr_zip, cust_country, cust_dob, cust_joined, cust_last_login, cust_is_active) VALUES (11, 'Kate', 'Brown', 'kate@email.com', '555-0111', 'hashed_pw_kate11', '591 Hickory Ave', 'Atlanta', 'GA', '30301', 'US', '1993-06-29', '2024-01-15', '2025-03-27', 1);
INSERT INTO sl_customers (cid, cust_fname, cust_lname, cust_email, cust_phone, cust_pass, cust_addr_line1, cust_addr_city, cust_addr_state, cust_addr_zip, cust_country, cust_dob, cust_joined, cust_last_login, cust_is_active) VALUES (12, 'Leo', 'Martinez', 'leo@email.com', '555-0112', 'hashed_pw_leo12', '702 Sycamore Rd', 'San Diego', 'CA', '92101', 'US', '1989-10-11', '2024-04-28', '2025-03-19', 0);

-- =============================================
-- sl_customer_notes (8 rows)
-- =============================================
CREATE TABLE sl_customer_notes (
    nid INTEGER PRIMARY KEY,
    note_cust_email TEXT NOT NULL,
    note_text TEXT NOT NULL,
    note_type TEXT,
    note_author TEXT,
    note_priority TEXT DEFAULT 'normal',
    note_status TEXT DEFAULT 'open',
    note_created TEXT,
    note_updated TEXT,
    note_is_internal INTEGER DEFAULT 1
);

INSERT INTO sl_customer_notes (nid, note_cust_email, note_text, note_type, note_author, note_priority, note_status, note_created, note_updated, note_is_internal) VALUES (1, 'alice@email.com', 'VIP customer, frequent buyer of electronics', 'flag', 'agent_sarah', 'high', 'active', '2024-06-01', '2024-06-01', 1);
INSERT INTO sl_customer_notes (nid, note_cust_email, note_text, note_type, note_author, note_priority, note_status, note_created, note_updated, note_is_internal) VALUES (2, 'bob@email.com', 'Requested bulk pricing for office supplies', 'request', 'agent_mike', 'normal', 'open', '2024-07-15', '2024-07-20', 0);
INSERT INTO sl_customer_notes (nid, note_cust_email, note_text, note_type, note_author, note_priority, note_status, note_created, note_updated, note_is_internal) VALUES (3, 'carol@email.com', 'Prefers expedited shipping', 'preference', 'agent_sarah', 'low', 'active', '2024-08-10', '2024-08-10', 1);
INSERT INTO sl_customer_notes (nid, note_cust_email, note_text, note_type, note_author, note_priority, note_status, note_created, note_updated, note_is_internal) VALUES (4, 'dave@email.com', 'Had shipping issue with order 1005, resolved with replacement', 'issue', 'agent_mike', 'high', 'resolved', '2024-09-03', '2024-09-10', 1);
INSERT INTO sl_customer_notes (nid, note_cust_email, note_text, note_type, note_author, note_priority, note_status, note_created, note_updated, note_is_internal) VALUES (5, 'eve@email.com', 'Interested in loyalty program enrollment', 'flag', 'agent_jenny', 'normal', 'open', '2024-10-22', '2024-10-22', 0);
INSERT INTO sl_customer_notes (nid, note_cust_email, note_text, note_type, note_author, note_priority, note_status, note_created, note_updated, note_is_internal) VALUES (6, 'frank@email.com', 'Credit hold removed after payment verification', 'billing', 'agent_sarah', 'high', 'resolved', '2024-11-05', '2024-11-08', 1);
INSERT INTO sl_customer_notes (nid, note_cust_email, note_text, note_type, note_author, note_priority, note_status, note_created, note_updated, note_is_internal) VALUES (7, 'grace@email.com', 'Allergic to latex, flag for packaging', 'preference', 'agent_jenny', 'high', 'active', '2025-01-12', '2025-01-12', 1);
INSERT INTO sl_customer_notes (nid, note_cust_email, note_text, note_type, note_author, note_priority, note_status, note_created, note_updated, note_is_internal) VALUES (8, 'henry@email.com', 'Corporate account pending approval', 'request', 'agent_mike', 'normal', 'open', '2025-02-18', '2025-02-20', 0);

-- =============================================
-- sl_products (15 rows)
-- =============================================
CREATE TABLE sl_products (
    pid INTEGER PRIMARY KEY,
    prod_sku TEXT NOT NULL,
    prod_name TEXT NOT NULL,
    prod_desc TEXT,
    prod_cat_name TEXT,
    prod_brand_name TEXT,
    prod_price REAL NOT NULL,
    prod_cost REAL,
    prod_weight REAL,
    prod_dims TEXT,
    prod_is_active INTEGER DEFAULT 1,
    prod_created TEXT,
    prod_updated TEXT
);

INSERT INTO sl_products (pid, prod_sku, prod_name, prod_desc, prod_cat_name, prod_brand_name, prod_price, prod_cost, prod_weight, prod_dims, prod_is_active, prod_created, prod_updated) VALUES (1, 'SL-LAPTOP-001', 'ProBook Laptop 15"', 'High-performance laptop with 16GB RAM and 512GB SSD', 'Computers', 'TechNova', 1299.99, 850.00, 2.1, '35.6x24.8x1.8cm', 1, '2023-01-15', '2025-02-10');
INSERT INTO sl_products (pid, prod_sku, prod_name, prod_desc, prod_cat_name, prod_brand_name, prod_price, prod_cost, prod_weight, prod_dims, prod_is_active, prod_created, prod_updated) VALUES (2, 'SL-PHONE-002', 'SmartEdge Phone X', 'Flagship smartphone with OLED display', 'Phones', 'TechNova', 899.99, 520.00, 0.19, '15.4x7.1x0.8cm', 1, '2023-02-20', '2025-01-15');
INSERT INTO sl_products (pid, prod_sku, prod_name, prod_desc, prod_cat_name, prod_brand_name, prod_price, prod_cost, prod_weight, prod_dims, prod_is_active, prod_created, prod_updated) VALUES (3, 'SL-TABLET-003', 'SlateView Tablet 10"', '10-inch tablet with stylus support', 'Electronics', 'TechNova', 549.99, 310.00, 0.48, '24.5x17.4x0.6cm', 1, '2023-03-10', '2024-12-05');
INSERT INTO sl_products (pid, prod_sku, prod_name, prod_desc, prod_cat_name, prod_brand_name, prod_price, prod_cost, prod_weight, prod_dims, prod_is_active, prod_created, prod_updated) VALUES (4, 'SL-HEADPH-004', 'BassWave Wireless Headphones', 'Noise-cancelling over-ear headphones', 'Electronics', 'SoundCraft', 199.99, 85.00, 0.32, '19x17x8cm', 1, '2023-04-01', '2025-03-01');
INSERT INTO sl_products (pid, prod_sku, prod_name, prod_desc, prod_cat_name, prod_brand_name, prod_price, prod_cost, prod_weight, prod_dims, prod_is_active, prod_created, prod_updated) VALUES (5, 'SL-TSHIRT-005', 'Classic Cotton Tee', '100% organic cotton crew-neck t-shirt', 'Clothing', 'UrbanThread', 29.99, 8.50, 0.2, '30x25x2cm', 1, '2023-05-15', '2025-01-20');
INSERT INTO sl_products (pid, prod_sku, prod_name, prod_desc, prod_cat_name, prod_brand_name, prod_price, prod_cost, prod_weight, prod_dims, prod_is_active, prod_created, prod_updated) VALUES (6, 'SL-JEANS-006', 'Slim Fit Denim Jeans', 'Stretch denim with modern slim fit', 'Clothing', 'UrbanThread', 69.99, 25.00, 0.65, '35x30x5cm', 1, '2023-06-01', '2025-02-14');
INSERT INTO sl_products (pid, prod_sku, prod_name, prod_desc, prod_cat_name, prod_brand_name, prod_price, prod_cost, prod_weight, prod_dims, prod_is_active, prod_created, prod_updated) VALUES (7, 'SL-SNEAK-007', 'RunFlex Sneakers', 'Lightweight running shoes with memory foam sole', 'Shoes', 'UrbanThread', 119.99, 42.00, 0.7, '32x12x11cm', 1, '2023-07-10', '2025-01-30');
INSERT INTO sl_products (pid, prod_sku, prod_name, prod_desc, prod_cat_name, prod_brand_name, prod_price, prod_cost, prod_weight, prod_dims, prod_is_active, prod_created, prod_updated) VALUES (8, 'SL-JACKET-008', 'Weathershield Rain Jacket', 'Waterproof breathable rain jacket', 'Clothing', 'UrbanThread', 149.99, 55.00, 0.45, '40x30x5cm', 1, '2023-08-05', '2024-11-20');
INSERT INTO sl_products (pid, prod_sku, prod_name, prod_desc, prod_cat_name, prod_brand_name, prod_price, prod_cost, prod_weight, prod_dims, prod_is_active, prod_created, prod_updated) VALUES (9, 'SL-BLNDR-009', 'PowerBlend Pro Blender', 'High-speed blender with 10 settings', 'Home & Kitchen', 'HomePlus', 89.99, 35.00, 3.2, '20x20x40cm', 1, '2023-09-12', '2025-02-28');
INSERT INTO sl_products (pid, prod_sku, prod_name, prod_desc, prod_cat_name, prod_brand_name, prod_price, prod_cost, prod_weight, prod_dims, prod_is_active, prod_created, prod_updated) VALUES (10, 'SL-COFFM-010', 'BrewMaster Coffee Maker', '12-cup drip coffee maker with timer', 'Home & Kitchen', 'HomePlus', 79.99, 30.00, 2.8, '22x18x35cm', 1, '2023-10-01', '2025-01-05');
INSERT INTO sl_products (pid, prod_sku, prod_name, prod_desc, prod_cat_name, prod_brand_name, prod_price, prod_cost, prod_weight, prod_dims, prod_is_active, prod_created, prod_updated) VALUES (11, 'SL-WATCH-011', 'ChronoFit Smartwatch', 'Fitness smartwatch with heart rate monitor', 'Accessories', 'TechNova', 249.99, 110.00, 0.05, '4.4x4.4x1.1cm', 1, '2023-11-15', '2025-03-10');
INSERT INTO sl_products (pid, prod_sku, prod_name, prod_desc, prod_cat_name, prod_brand_name, prod_price, prod_cost, prod_weight, prod_dims, prod_is_active, prod_created, prod_updated) VALUES (12, 'SL-BACKP-012', 'TrekPack Laptop Backpack', 'Water-resistant backpack with USB charging port', 'Accessories', 'UrbanThread', 59.99, 18.00, 0.9, '45x30x15cm', 1, '2024-01-10', '2025-02-20');
INSERT INTO sl_products (pid, prod_sku, prod_name, prod_desc, prod_cat_name, prod_brand_name, prod_price, prod_cost, prod_weight, prod_dims, prod_is_active, prod_created, prod_updated) VALUES (13, 'SL-BOOK-013', 'SQL Mastery Handbook', 'Comprehensive guide to database design and optimization', 'Books', 'PageBound', 39.99, 12.00, 0.55, '23x15x3cm', 1, '2024-02-15', '2025-01-10');
INSERT INTO sl_products (pid, prod_sku, prod_name, prod_desc, prod_cat_name, prod_brand_name, prod_price, prod_cost, prod_weight, prod_dims, prod_is_active, prod_created, prod_updated) VALUES (14, 'SL-CHARGER-014', 'QuickCharge USB-C Hub', '7-in-1 USB-C hub with fast charging', 'Electronics', 'TechNova', 49.99, 15.00, 0.12, '10x5x1.5cm', 1, '2024-03-20', '2025-03-05');
INSERT INTO sl_products (pid, prod_sku, prod_name, prod_desc, prod_cat_name, prod_brand_name, prod_price, prod_cost, prod_weight, prod_dims, prod_is_active, prod_created, prod_updated) VALUES (15, 'SL-MUG-015', 'Ceramic Travel Mug', 'Double-walled ceramic mug with silicone lid', 'Home & Kitchen', 'HomePlus', 19.99, 5.50, 0.35, '9x9x14cm', 1, '2024-04-05', '2025-02-01');

-- =============================================
-- sl_categories (8 rows)
-- =============================================
CREATE TABLE sl_categories (
    catid INTEGER PRIMARY KEY,
    cat_name TEXT NOT NULL,
    cat_slug TEXT NOT NULL,
    cat_desc TEXT,
    cat_parent_name TEXT,
    cat_is_active INTEGER DEFAULT 1,
    cat_sort INTEGER DEFAULT 0,
    cat_img TEXT,
    cat_meta_title TEXT,
    cat_meta_desc TEXT
);

INSERT INTO sl_categories (catid, cat_name, cat_slug, cat_desc, cat_parent_name, cat_is_active, cat_sort, cat_img, cat_meta_title, cat_meta_desc) VALUES (1, 'Electronics', 'electronics', 'Gadgets, devices, and electronic accessories', NULL, 1, 1, '/img/cat/electronics.jpg', 'Shop Electronics', 'Browse our wide selection of electronics');
INSERT INTO sl_categories (catid, cat_name, cat_slug, cat_desc, cat_parent_name, cat_is_active, cat_sort, cat_img, cat_meta_title, cat_meta_desc) VALUES (2, 'Computers', 'computers', 'Laptops, desktops, and computer accessories', 'Electronics', 1, 2, '/img/cat/computers.jpg', 'Shop Computers', 'Find the perfect computer for work or play');
INSERT INTO sl_categories (catid, cat_name, cat_slug, cat_desc, cat_parent_name, cat_is_active, cat_sort, cat_img, cat_meta_title, cat_meta_desc) VALUES (3, 'Phones', 'phones', 'Smartphones and mobile accessories', 'Electronics', 1, 3, '/img/cat/phones.jpg', 'Shop Phones', 'Discover the latest smartphones');
INSERT INTO sl_categories (catid, cat_name, cat_slug, cat_desc, cat_parent_name, cat_is_active, cat_sort, cat_img, cat_meta_title, cat_meta_desc) VALUES (4, 'Clothing', 'clothing', 'Apparel for men, women, and children', NULL, 1, 4, '/img/cat/clothing.jpg', 'Shop Clothing', 'Trendy and comfortable clothing for everyone');
INSERT INTO sl_categories (catid, cat_name, cat_slug, cat_desc, cat_parent_name, cat_is_active, cat_sort, cat_img, cat_meta_title, cat_meta_desc) VALUES (5, 'Shoes', 'shoes', 'Footwear for every occasion', 'Clothing', 1, 5, '/img/cat/shoes.jpg', 'Shop Shoes', 'Step up your style with our shoe collection');
INSERT INTO sl_categories (catid, cat_name, cat_slug, cat_desc, cat_parent_name, cat_is_active, cat_sort, cat_img, cat_meta_title, cat_meta_desc) VALUES (6, 'Home & Kitchen', 'home-kitchen', 'Appliances, cookware, and home essentials', NULL, 1, 6, '/img/cat/home.jpg', 'Shop Home & Kitchen', 'Everything for your home and kitchen');
INSERT INTO sl_categories (catid, cat_name, cat_slug, cat_desc, cat_parent_name, cat_is_active, cat_sort, cat_img, cat_meta_title, cat_meta_desc) VALUES (7, 'Accessories', 'accessories', 'Watches, bags, and personal accessories', NULL, 1, 7, '/img/cat/accessories.jpg', 'Shop Accessories', 'Complete your look with our accessories');
INSERT INTO sl_categories (catid, cat_name, cat_slug, cat_desc, cat_parent_name, cat_is_active, cat_sort, cat_img, cat_meta_title, cat_meta_desc) VALUES (8, 'Books', 'books', 'Physical and digital books across all genres', NULL, 1, 8, '/img/cat/books.jpg', 'Shop Books', 'Expand your mind with our book collection');

-- =============================================
-- sl_brands (6 rows)
-- =============================================
CREATE TABLE sl_brands (
    bid INTEGER PRIMARY KEY,
    brand_name TEXT NOT NULL,
    brand_slug TEXT NOT NULL,
    brand_desc TEXT,
    brand_logo TEXT,
    brand_website TEXT,
    brand_country TEXT,
    brand_founded INTEGER,
    brand_is_active INTEGER DEFAULT 1,
    brand_contact_email TEXT
);

INSERT INTO sl_brands (bid, brand_name, brand_slug, brand_desc, brand_logo, brand_website, brand_country, brand_founded, brand_is_active, brand_contact_email) VALUES (1, 'TechNova', 'technova', 'Leading innovator in consumer electronics', '/img/brand/technova.png', 'https://technova.example.com', 'US', 2010, 1, 'partners@technova.example.com');
INSERT INTO sl_brands (bid, brand_name, brand_slug, brand_desc, brand_logo, brand_website, brand_country, brand_founded, brand_is_active, brand_contact_email) VALUES (2, 'SoundCraft', 'soundcraft', 'Premium audio equipment manufacturer', '/img/brand/soundcraft.png', 'https://soundcraft.example.com', 'JP', 2005, 1, 'sales@soundcraft.example.com');
INSERT INTO sl_brands (bid, brand_name, brand_slug, brand_desc, brand_logo, brand_website, brand_country, brand_founded, brand_is_active, brand_contact_email) VALUES (3, 'UrbanThread', 'urbanthread', 'Sustainable fashion and lifestyle brand', '/img/brand/urbanthread.png', 'https://urbanthread.example.com', 'US', 2015, 1, 'wholesale@urbanthread.example.com');
INSERT INTO sl_brands (bid, brand_name, brand_slug, brand_desc, brand_logo, brand_website, brand_country, brand_founded, brand_is_active, brand_contact_email) VALUES (4, 'HomePlus', 'homeplus', 'Quality home appliances and kitchenware', '/img/brand/homeplus.png', 'https://homeplus.example.com', 'DE', 2008, 1, 'info@homeplus.example.com');
INSERT INTO sl_brands (bid, brand_name, brand_slug, brand_desc, brand_logo, brand_website, brand_country, brand_founded, brand_is_active, brand_contact_email) VALUES (5, 'PageBound', 'pagebound', 'Independent book publisher', '/img/brand/pagebound.png', 'https://pagebound.example.com', 'UK', 2012, 1, 'submissions@pagebound.example.com');
INSERT INTO sl_brands (bid, brand_name, brand_slug, brand_desc, brand_logo, brand_website, brand_country, brand_founded, brand_is_active, brand_contact_email) VALUES (6, 'GreenLeaf', 'greenleaf', 'Eco-friendly products and accessories', '/img/brand/greenleaf.png', 'https://greenleaf.example.com', 'CA', 2018, 0, 'hello@greenleaf.example.com');

-- =============================================
-- sl_product_variants (20 rows)
-- =============================================
CREATE TABLE sl_product_variants (
    vid INTEGER PRIMARY KEY,
    var_prod_sku TEXT NOT NULL,
    var_name TEXT NOT NULL,
    var_sku TEXT NOT NULL,
    var_price_adj REAL DEFAULT 0,
    var_stock INTEGER DEFAULT 0,
    var_color TEXT,
    var_size TEXT,
    var_weight REAL,
    var_is_active INTEGER DEFAULT 1,
    var_created TEXT
);

INSERT INTO sl_product_variants (vid, var_prod_sku, var_name, var_sku, var_price_adj, var_stock, var_color, var_size, var_weight, var_is_active, var_created) VALUES (1, 'SL-LAPTOP-001', 'ProBook 15 Silver 8GB', 'SL-LAPTOP-001-SLV-8', -200.00, 25, 'Silver', '8GB', 2.1, 1, '2023-01-15');
INSERT INTO sl_product_variants (vid, var_prod_sku, var_name, var_sku, var_price_adj, var_stock, var_color, var_size, var_weight, var_is_active, var_created) VALUES (2, 'SL-LAPTOP-001', 'ProBook 15 Space Gray 16GB', 'SL-LAPTOP-001-GRY-16', 0.00, 18, 'Space Gray', '16GB', 2.15, 1, '2023-01-15');
INSERT INTO sl_product_variants (vid, var_prod_sku, var_name, var_sku, var_price_adj, var_stock, var_color, var_size, var_weight, var_is_active, var_created) VALUES (3, 'SL-PHONE-002', 'SmartEdge X Black 128GB', 'SL-PHONE-002-BLK-128', 0.00, 40, 'Black', '128GB', 0.19, 1, '2023-02-20');
INSERT INTO sl_product_variants (vid, var_prod_sku, var_name, var_sku, var_price_adj, var_stock, var_color, var_size, var_weight, var_is_active, var_created) VALUES (4, 'SL-PHONE-002', 'SmartEdge X White 256GB', 'SL-PHONE-002-WHT-256', 100.00, 22, 'White', '256GB', 0.19, 1, '2023-02-20');
INSERT INTO sl_product_variants (vid, var_prod_sku, var_name, var_sku, var_price_adj, var_stock, var_color, var_size, var_weight, var_is_active, var_created) VALUES (5, 'SL-TSHIRT-005', 'Classic Tee White S', 'SL-TSHIRT-005-WHT-S', 0.00, 60, 'White', 'S', 0.18, 1, '2023-05-15');
INSERT INTO sl_product_variants (vid, var_prod_sku, var_name, var_sku, var_price_adj, var_stock, var_color, var_size, var_weight, var_is_active, var_created) VALUES (6, 'SL-TSHIRT-005', 'Classic Tee White M', 'SL-TSHIRT-005-WHT-M', 0.00, 85, 'White', 'M', 0.2, 1, '2023-05-15');
INSERT INTO sl_product_variants (vid, var_prod_sku, var_name, var_sku, var_price_adj, var_stock, var_color, var_size, var_weight, var_is_active, var_created) VALUES (7, 'SL-TSHIRT-005', 'Classic Tee Black L', 'SL-TSHIRT-005-BLK-L', 0.00, 70, 'Black', 'L', 0.22, 1, '2023-05-15');
INSERT INTO sl_product_variants (vid, var_prod_sku, var_name, var_sku, var_price_adj, var_stock, var_color, var_size, var_weight, var_is_active, var_created) VALUES (8, 'SL-JEANS-006', 'Slim Jeans Blue 32', 'SL-JEANS-006-BLU-32', 0.00, 45, 'Blue', '32', 0.65, 1, '2023-06-01');
INSERT INTO sl_product_variants (vid, var_prod_sku, var_name, var_sku, var_price_adj, var_stock, var_color, var_size, var_weight, var_is_active, var_created) VALUES (9, 'SL-JEANS-006', 'Slim Jeans Blue 34', 'SL-JEANS-006-BLU-34', 0.00, 38, 'Blue', '34', 0.67, 1, '2023-06-01');
INSERT INTO sl_product_variants (vid, var_prod_sku, var_name, var_sku, var_price_adj, var_stock, var_color, var_size, var_weight, var_is_active, var_created) VALUES (10, 'SL-JEANS-006', 'Slim Jeans Black 30', 'SL-JEANS-006-BLK-30', 0.00, 30, 'Black', '30', 0.63, 1, '2023-06-01');
INSERT INTO sl_product_variants (vid, var_prod_sku, var_name, var_sku, var_price_adj, var_stock, var_color, var_size, var_weight, var_is_active, var_created) VALUES (11, 'SL-SNEAK-007', 'RunFlex White US9', 'SL-SNEAK-007-WHT-9', 0.00, 20, 'White', 'US9', 0.7, 1, '2023-07-10');
INSERT INTO sl_product_variants (vid, var_prod_sku, var_name, var_sku, var_price_adj, var_stock, var_color, var_size, var_weight, var_is_active, var_created) VALUES (12, 'SL-SNEAK-007', 'RunFlex Black US10', 'SL-SNEAK-007-BLK-10', 0.00, 15, 'Black', 'US10', 0.72, 1, '2023-07-10');
INSERT INTO sl_product_variants (vid, var_prod_sku, var_name, var_sku, var_price_adj, var_stock, var_color, var_size, var_weight, var_is_active, var_created) VALUES (13, 'SL-JACKET-008', 'Rain Jacket Navy M', 'SL-JACKET-008-NVY-M', 0.00, 28, 'Navy', 'M', 0.45, 1, '2023-08-05');
INSERT INTO sl_product_variants (vid, var_prod_sku, var_name, var_sku, var_price_adj, var_stock, var_color, var_size, var_weight, var_is_active, var_created) VALUES (14, 'SL-JACKET-008', 'Rain Jacket Red L', 'SL-JACKET-008-RED-L', 0.00, 22, 'Red', 'L', 0.47, 1, '2023-08-05');
INSERT INTO sl_product_variants (vid, var_prod_sku, var_name, var_sku, var_price_adj, var_stock, var_color, var_size, var_weight, var_is_active, var_created) VALUES (15, 'SL-HEADPH-004', 'BassWave Black', 'SL-HEADPH-004-BLK', 0.00, 50, 'Black', 'OneSize', 0.32, 1, '2023-04-01');
INSERT INTO sl_product_variants (vid, var_prod_sku, var_name, var_sku, var_price_adj, var_stock, var_color, var_size, var_weight, var_is_active, var_created) VALUES (16, 'SL-HEADPH-004', 'BassWave White', 'SL-HEADPH-004-WHT', 0.00, 35, 'White', 'OneSize', 0.32, 1, '2023-04-01');
INSERT INTO sl_product_variants (vid, var_prod_sku, var_name, var_sku, var_price_adj, var_stock, var_color, var_size, var_weight, var_is_active, var_created) VALUES (17, 'SL-WATCH-011', 'ChronoFit Black', 'SL-WATCH-011-BLK', 0.00, 30, 'Black', 'OneSize', 0.05, 1, '2023-11-15');
INSERT INTO sl_product_variants (vid, var_prod_sku, var_name, var_sku, var_price_adj, var_stock, var_color, var_size, var_weight, var_is_active, var_created) VALUES (18, 'SL-WATCH-011', 'ChronoFit Rose Gold', 'SL-WATCH-011-RGD', 30.00, 12, 'Rose Gold', 'OneSize', 0.05, 1, '2023-11-15');
INSERT INTO sl_product_variants (vid, var_prod_sku, var_name, var_sku, var_price_adj, var_stock, var_color, var_size, var_weight, var_is_active, var_created) VALUES (19, 'SL-MUG-015', 'Travel Mug Teal', 'SL-MUG-015-TEL', 0.00, 100, 'Teal', 'OneSize', 0.35, 1, '2024-04-05');
INSERT INTO sl_product_variants (vid, var_prod_sku, var_name, var_sku, var_price_adj, var_stock, var_color, var_size, var_weight, var_is_active, var_created) VALUES (20, 'SL-MUG-015', 'Travel Mug Charcoal', 'SL-MUG-015-CHR', 0.00, 80, 'Charcoal', 'OneSize', 0.35, 1, '2024-04-05');

-- =============================================
-- sl_product_images (18 rows)
-- =============================================
CREATE TABLE sl_product_images (
    imgid INTEGER PRIMARY KEY,
    img_prod_sku TEXT NOT NULL,
    img_url TEXT NOT NULL,
    img_alt TEXT,
    img_sort INTEGER DEFAULT 0,
    img_is_primary INTEGER DEFAULT 0,
    img_width INTEGER,
    img_height INTEGER,
    img_size_kb INTEGER,
    img_mime TEXT DEFAULT 'image/jpeg',
    img_uploaded TEXT
);

INSERT INTO sl_product_images (imgid, img_prod_sku, img_url, img_alt, img_sort, img_is_primary, img_width, img_height, img_size_kb, img_mime, img_uploaded) VALUES (1, 'SL-LAPTOP-001', '/img/products/laptop-001-main.jpg', 'ProBook Laptop 15 front view', 1, 1, 1200, 800, 245, 'image/jpeg', '2023-01-15');
INSERT INTO sl_product_images (imgid, img_prod_sku, img_url, img_alt, img_sort, img_is_primary, img_width, img_height, img_size_kb, img_mime, img_uploaded) VALUES (2, 'SL-LAPTOP-001', '/img/products/laptop-001-side.jpg', 'ProBook Laptop 15 side view', 2, 0, 1200, 800, 198, 'image/jpeg', '2023-01-15');
INSERT INTO sl_product_images (imgid, img_prod_sku, img_url, img_alt, img_sort, img_is_primary, img_width, img_height, img_size_kb, img_mime, img_uploaded) VALUES (3, 'SL-PHONE-002', '/img/products/phone-002-main.jpg', 'SmartEdge Phone X front', 1, 1, 800, 1200, 180, 'image/jpeg', '2023-02-20');
INSERT INTO sl_product_images (imgid, img_prod_sku, img_url, img_alt, img_sort, img_is_primary, img_width, img_height, img_size_kb, img_mime, img_uploaded) VALUES (4, 'SL-TABLET-003', '/img/products/tablet-003-main.jpg', 'SlateView Tablet with stylus', 1, 1, 1000, 750, 210, 'image/jpeg', '2023-03-10');
INSERT INTO sl_product_images (imgid, img_prod_sku, img_url, img_alt, img_sort, img_is_primary, img_width, img_height, img_size_kb, img_mime, img_uploaded) VALUES (5, 'SL-HEADPH-004', '/img/products/headphones-004-main.jpg', 'BassWave headphones on stand', 1, 1, 900, 900, 156, 'image/jpeg', '2023-04-01');
INSERT INTO sl_product_images (imgid, img_prod_sku, img_url, img_alt, img_sort, img_is_primary, img_width, img_height, img_size_kb, img_mime, img_uploaded) VALUES (6, 'SL-TSHIRT-005', '/img/products/tshirt-005-main.jpg', 'Classic Cotton Tee white front', 1, 1, 800, 1000, 120, 'image/jpeg', '2023-05-15');
INSERT INTO sl_product_images (imgid, img_prod_sku, img_url, img_alt, img_sort, img_is_primary, img_width, img_height, img_size_kb, img_mime, img_uploaded) VALUES (7, 'SL-TSHIRT-005', '/img/products/tshirt-005-back.jpg', 'Classic Cotton Tee white back', 2, 0, 800, 1000, 115, 'image/jpeg', '2023-05-15');
INSERT INTO sl_product_images (imgid, img_prod_sku, img_url, img_alt, img_sort, img_is_primary, img_width, img_height, img_size_kb, img_mime, img_uploaded) VALUES (8, 'SL-JEANS-006', '/img/products/jeans-006-main.jpg', 'Slim Fit Denim Jeans front', 1, 1, 800, 1200, 175, 'image/jpeg', '2023-06-01');
INSERT INTO sl_product_images (imgid, img_prod_sku, img_url, img_alt, img_sort, img_is_primary, img_width, img_height, img_size_kb, img_mime, img_uploaded) VALUES (9, 'SL-SNEAK-007', '/img/products/sneakers-007-main.jpg', 'RunFlex Sneakers white pair', 1, 1, 1000, 700, 190, 'image/jpeg', '2023-07-10');
INSERT INTO sl_product_images (imgid, img_prod_sku, img_url, img_alt, img_sort, img_is_primary, img_width, img_height, img_size_kb, img_mime, img_uploaded) VALUES (10, 'SL-JACKET-008', '/img/products/jacket-008-main.jpg', 'Weathershield Rain Jacket navy', 1, 1, 800, 1000, 165, 'image/jpeg', '2023-08-05');
INSERT INTO sl_product_images (imgid, img_prod_sku, img_url, img_alt, img_sort, img_is_primary, img_width, img_height, img_size_kb, img_mime, img_uploaded) VALUES (11, 'SL-BLNDR-009', '/img/products/blender-009-main.jpg', 'PowerBlend Pro Blender with jar', 1, 1, 800, 1000, 140, 'image/jpeg', '2023-09-12');
INSERT INTO sl_product_images (imgid, img_prod_sku, img_url, img_alt, img_sort, img_is_primary, img_width, img_height, img_size_kb, img_mime, img_uploaded) VALUES (12, 'SL-COFFM-010', '/img/products/coffee-010-main.jpg', 'BrewMaster Coffee Maker front', 1, 1, 800, 1000, 155, 'image/jpeg', '2023-10-01');
INSERT INTO sl_product_images (imgid, img_prod_sku, img_url, img_alt, img_sort, img_is_primary, img_width, img_height, img_size_kb, img_mime, img_uploaded) VALUES (13, 'SL-WATCH-011', '/img/products/watch-011-main.jpg', 'ChronoFit Smartwatch on wrist', 1, 1, 900, 900, 130, 'image/jpeg', '2023-11-15');
INSERT INTO sl_product_images (imgid, img_prod_sku, img_url, img_alt, img_sort, img_is_primary, img_width, img_height, img_size_kb, img_mime, img_uploaded) VALUES (14, 'SL-BACKP-012', '/img/products/backpack-012-main.jpg', 'TrekPack Backpack front view', 1, 1, 800, 1000, 185, 'image/jpeg', '2024-01-10');
INSERT INTO sl_product_images (imgid, img_prod_sku, img_url, img_alt, img_sort, img_is_primary, img_width, img_height, img_size_kb, img_mime, img_uploaded) VALUES (15, 'SL-BOOK-013', '/img/products/book-013-main.jpg', 'SQL Mastery Handbook cover', 1, 1, 600, 900, 95, 'image/jpeg', '2024-02-15');
INSERT INTO sl_product_images (imgid, img_prod_sku, img_url, img_alt, img_sort, img_is_primary, img_width, img_height, img_size_kb, img_mime, img_uploaded) VALUES (16, 'SL-CHARGER-014', '/img/products/charger-014-main.jpg', 'QuickCharge USB-C Hub top view', 1, 1, 800, 600, 88, 'image/jpeg', '2024-03-20');
INSERT INTO sl_product_images (imgid, img_prod_sku, img_url, img_alt, img_sort, img_is_primary, img_width, img_height, img_size_kb, img_mime, img_uploaded) VALUES (17, 'SL-MUG-015', '/img/products/mug-015-main.jpg', 'Ceramic Travel Mug teal', 1, 1, 800, 800, 110, 'image/jpeg', '2024-04-05');
INSERT INTO sl_product_images (imgid, img_prod_sku, img_url, img_alt, img_sort, img_is_primary, img_width, img_height, img_size_kb, img_mime, img_uploaded) VALUES (18, 'SL-MUG-015', '/img/products/mug-015-lid.jpg', 'Ceramic Travel Mug lid detail', 2, 0, 600, 600, 72, 'image/jpeg', '2024-04-05');

-- =============================================
-- sl_product_tags (25 rows)
-- =============================================
CREATE TABLE sl_product_tags (
    ptid INTEGER PRIMARY KEY,
    pt_prod_sku TEXT NOT NULL,
    pt_tag_name TEXT NOT NULL,
    pt_added_by TEXT,
    pt_added_at TEXT,
    pt_is_auto INTEGER DEFAULT 0,
    pt_weight REAL DEFAULT 1.0,
    pt_source TEXT,
    pt_relevance REAL DEFAULT 0.8,
    pt_is_approved INTEGER DEFAULT 1
);

INSERT INTO sl_product_tags (ptid, pt_prod_sku, pt_tag_name, pt_added_by, pt_added_at, pt_is_auto, pt_weight, pt_source, pt_relevance, pt_is_approved) VALUES (1, 'SL-LAPTOP-001', 'bestseller', 'admin', '2023-06-01', 0, 1.0, 'manual', 0.95, 1);
INSERT INTO sl_product_tags (ptid, pt_prod_sku, pt_tag_name, pt_added_by, pt_added_at, pt_is_auto, pt_weight, pt_source, pt_relevance, pt_is_approved) VALUES (2, 'SL-LAPTOP-001', 'work-from-home', 'admin', '2023-06-01', 0, 0.8, 'manual', 0.90, 1);
INSERT INTO sl_product_tags (ptid, pt_prod_sku, pt_tag_name, pt_added_by, pt_added_at, pt_is_auto, pt_weight, pt_source, pt_relevance, pt_is_approved) VALUES (3, 'SL-PHONE-002', 'bestseller', 'admin', '2023-03-15', 0, 1.0, 'manual', 0.95, 1);
INSERT INTO sl_product_tags (ptid, pt_prod_sku, pt_tag_name, pt_added_by, pt_added_at, pt_is_auto, pt_weight, pt_source, pt_relevance, pt_is_approved) VALUES (4, 'SL-PHONE-002', 'new-arrival', 'system', '2023-02-20', 1, 0.9, 'auto-rule', 0.85, 1);
INSERT INTO sl_product_tags (ptid, pt_prod_sku, pt_tag_name, pt_added_by, pt_added_at, pt_is_auto, pt_weight, pt_source, pt_relevance, pt_is_approved) VALUES (5, 'SL-TABLET-003', 'portable', 'admin', '2023-04-10', 0, 0.7, 'manual', 0.80, 1);
INSERT INTO sl_product_tags (ptid, pt_prod_sku, pt_tag_name, pt_added_by, pt_added_at, pt_is_auto, pt_weight, pt_source, pt_relevance, pt_is_approved) VALUES (6, 'SL-HEADPH-004', 'gift-idea', 'admin', '2023-11-01', 0, 0.9, 'manual', 0.88, 1);
INSERT INTO sl_product_tags (ptid, pt_prod_sku, pt_tag_name, pt_added_by, pt_added_at, pt_is_auto, pt_weight, pt_source, pt_relevance, pt_is_approved) VALUES (7, 'SL-HEADPH-004', 'wireless', 'system', '2023-04-01', 1, 1.0, 'auto-catalog', 0.99, 1);
INSERT INTO sl_product_tags (ptid, pt_prod_sku, pt_tag_name, pt_added_by, pt_added_at, pt_is_auto, pt_weight, pt_source, pt_relevance, pt_is_approved) VALUES (8, 'SL-TSHIRT-005', 'sustainable', 'admin', '2023-06-20', 0, 0.9, 'manual', 0.92, 1);
INSERT INTO sl_product_tags (ptid, pt_prod_sku, pt_tag_name, pt_added_by, pt_added_at, pt_is_auto, pt_weight, pt_source, pt_relevance, pt_is_approved) VALUES (9, 'SL-TSHIRT-005', 'summer', 'system', '2023-05-15', 1, 0.7, 'auto-season', 0.75, 1);
INSERT INTO sl_product_tags (ptid, pt_prod_sku, pt_tag_name, pt_added_by, pt_added_at, pt_is_auto, pt_weight, pt_source, pt_relevance, pt_is_approved) VALUES (10, 'SL-JEANS-006', 'everyday', 'admin', '2023-07-01', 0, 0.8, 'manual', 0.85, 1);
INSERT INTO sl_product_tags (ptid, pt_prod_sku, pt_tag_name, pt_added_by, pt_added_at, pt_is_auto, pt_weight, pt_source, pt_relevance, pt_is_approved) VALUES (11, 'SL-SNEAK-007', 'sport', 'system', '2023-07-10', 1, 0.9, 'auto-catalog', 0.90, 1);
INSERT INTO sl_product_tags (ptid, pt_prod_sku, pt_tag_name, pt_added_by, pt_added_at, pt_is_auto, pt_weight, pt_source, pt_relevance, pt_is_approved) VALUES (12, 'SL-SNEAK-007', 'new-arrival', 'system', '2023-07-10', 1, 0.8, 'auto-rule', 0.80, 1);
INSERT INTO sl_product_tags (ptid, pt_prod_sku, pt_tag_name, pt_added_by, pt_added_at, pt_is_auto, pt_weight, pt_source, pt_relevance, pt_is_approved) VALUES (13, 'SL-JACKET-008', 'outdoor', 'admin', '2023-09-01', 0, 0.9, 'manual', 0.92, 1);
INSERT INTO sl_product_tags (ptid, pt_prod_sku, pt_tag_name, pt_added_by, pt_added_at, pt_is_auto, pt_weight, pt_source, pt_relevance, pt_is_approved) VALUES (14, 'SL-BLNDR-009', 'kitchen', 'system', '2023-09-12', 1, 1.0, 'auto-catalog', 0.98, 1);
INSERT INTO sl_product_tags (ptid, pt_prod_sku, pt_tag_name, pt_added_by, pt_added_at, pt_is_auto, pt_weight, pt_source, pt_relevance, pt_is_approved) VALUES (15, 'SL-BLNDR-009', 'gift-idea', 'admin', '2023-11-01', 0, 0.8, 'manual', 0.82, 1);
INSERT INTO sl_product_tags (ptid, pt_prod_sku, pt_tag_name, pt_added_by, pt_added_at, pt_is_auto, pt_weight, pt_source, pt_relevance, pt_is_approved) VALUES (16, 'SL-COFFM-010', 'kitchen', 'system', '2023-10-01', 1, 1.0, 'auto-catalog', 0.98, 1);
INSERT INTO sl_product_tags (ptid, pt_prod_sku, pt_tag_name, pt_added_by, pt_added_at, pt_is_auto, pt_weight, pt_source, pt_relevance, pt_is_approved) VALUES (17, 'SL-WATCH-011', 'gift-idea', 'admin', '2023-12-01', 0, 1.0, 'manual', 0.95, 1);
INSERT INTO sl_product_tags (ptid, pt_prod_sku, pt_tag_name, pt_added_by, pt_added_at, pt_is_auto, pt_weight, pt_source, pt_relevance, pt_is_approved) VALUES (18, 'SL-WATCH-011', 'wireless', 'system', '2023-11-15', 1, 0.7, 'auto-catalog', 0.78, 1);
INSERT INTO sl_product_tags (ptid, pt_prod_sku, pt_tag_name, pt_added_by, pt_added_at, pt_is_auto, pt_weight, pt_source, pt_relevance, pt_is_approved) VALUES (19, 'SL-BACKP-012', 'everyday', 'admin', '2024-02-01', 0, 0.8, 'manual', 0.85, 1);
INSERT INTO sl_product_tags (ptid, pt_prod_sku, pt_tag_name, pt_added_by, pt_added_at, pt_is_auto, pt_weight, pt_source, pt_relevance, pt_is_approved) VALUES (20, 'SL-BACKP-012', 'work-from-home', 'admin', '2024-02-01', 0, 0.7, 'manual', 0.78, 1);
INSERT INTO sl_product_tags (ptid, pt_prod_sku, pt_tag_name, pt_added_by, pt_added_at, pt_is_auto, pt_weight, pt_source, pt_relevance, pt_is_approved) VALUES (21, 'SL-BOOK-013', 'bestseller', 'system', '2024-05-01', 1, 0.9, 'auto-sales', 0.88, 1);
INSERT INTO sl_product_tags (ptid, pt_prod_sku, pt_tag_name, pt_added_by, pt_added_at, pt_is_auto, pt_weight, pt_source, pt_relevance, pt_is_approved) VALUES (22, 'SL-CHARGER-014', 'portable', 'system', '2024-03-20', 1, 0.8, 'auto-catalog', 0.85, 1);
INSERT INTO sl_product_tags (ptid, pt_prod_sku, pt_tag_name, pt_added_by, pt_added_at, pt_is_auto, pt_weight, pt_source, pt_relevance, pt_is_approved) VALUES (23, 'SL-CHARGER-014', 'work-from-home', 'admin', '2024-04-01', 0, 0.8, 'manual', 0.82, 1);
INSERT INTO sl_product_tags (ptid, pt_prod_sku, pt_tag_name, pt_added_by, pt_added_at, pt_is_auto, pt_weight, pt_source, pt_relevance, pt_is_approved) VALUES (24, 'SL-MUG-015', 'gift-idea', 'admin', '2024-11-01', 0, 0.9, 'manual', 0.90, 1);
INSERT INTO sl_product_tags (ptid, pt_prod_sku, pt_tag_name, pt_added_by, pt_added_at, pt_is_auto, pt_weight, pt_source, pt_relevance, pt_is_approved) VALUES (25, 'SL-MUG-015', 'sustainable', 'admin', '2024-05-10', 0, 0.7, 'manual', 0.75, 1);

-- =============================================
-- sl_tags (10 rows)
-- =============================================
CREATE TABLE sl_tags (
    tid INTEGER PRIMARY KEY,
    tag_name TEXT NOT NULL,
    tag_slug TEXT NOT NULL,
    tag_desc TEXT,
    tag_use_count INTEGER DEFAULT 0,
    tag_is_trending INTEGER DEFAULT 0,
    tag_color TEXT,
    tag_created_by TEXT,
    tag_created TEXT,
    tag_is_active INTEGER DEFAULT 1
);

INSERT INTO sl_tags (tid, tag_name, tag_slug, tag_desc, tag_use_count, tag_is_trending, tag_color, tag_created_by, tag_created, tag_is_active) VALUES (1, 'bestseller', 'bestseller', 'Top-selling products', 3, 1, '#FF5733', 'admin', '2023-01-01', 1);
INSERT INTO sl_tags (tid, tag_name, tag_slug, tag_desc, tag_use_count, tag_is_trending, tag_color, tag_created_by, tag_created, tag_is_active) VALUES (2, 'new-arrival', 'new-arrival', 'Recently added products', 2, 1, '#33C1FF', 'admin', '2023-01-01', 1);
INSERT INTO sl_tags (tid, tag_name, tag_slug, tag_desc, tag_use_count, tag_is_trending, tag_color, tag_created_by, tag_created, tag_is_active) VALUES (3, 'gift-idea', 'gift-idea', 'Great gift suggestions', 4, 1, '#FF33A8', 'admin', '2023-01-01', 1);
INSERT INTO sl_tags (tid, tag_name, tag_slug, tag_desc, tag_use_count, tag_is_trending, tag_color, tag_created_by, tag_created, tag_is_active) VALUES (4, 'work-from-home', 'work-from-home', 'Products for remote work', 3, 0, '#33FF57', 'admin', '2023-01-01', 1);
INSERT INTO sl_tags (tid, tag_name, tag_slug, tag_desc, tag_use_count, tag_is_trending, tag_color, tag_created_by, tag_created, tag_is_active) VALUES (5, 'sustainable', 'sustainable', 'Eco-friendly and sustainable products', 2, 0, '#57FF33', 'admin', '2023-03-15', 1);
INSERT INTO sl_tags (tid, tag_name, tag_slug, tag_desc, tag_use_count, tag_is_trending, tag_color, tag_created_by, tag_created, tag_is_active) VALUES (6, 'summer', 'summer', 'Seasonal summer picks', 1, 0, '#FFD700', 'system', '2023-05-01', 1);
INSERT INTO sl_tags (tid, tag_name, tag_slug, tag_desc, tag_use_count, tag_is_trending, tag_color, tag_created_by, tag_created, tag_is_active) VALUES (7, 'wireless', 'wireless', 'Wireless and cable-free products', 2, 0, '#8A2BE2', 'system', '2023-04-01', 1);
INSERT INTO sl_tags (tid, tag_name, tag_slug, tag_desc, tag_use_count, tag_is_trending, tag_color, tag_created_by, tag_created, tag_is_active) VALUES (8, 'portable', 'portable', 'Compact and portable items', 2, 0, '#20B2AA', 'admin', '2023-04-10', 1);
INSERT INTO sl_tags (tid, tag_name, tag_slug, tag_desc, tag_use_count, tag_is_trending, tag_color, tag_created_by, tag_created, tag_is_active) VALUES (9, 'everyday', 'everyday', 'Everyday essentials', 2, 0, '#696969', 'admin', '2023-07-01', 1);
INSERT INTO sl_tags (tid, tag_name, tag_slug, tag_desc, tag_use_count, tag_is_trending, tag_color, tag_created_by, tag_created, tag_is_active) VALUES (10, 'sport', 'sport', 'Sports and fitness products', 1, 0, '#FF4500', 'system', '2023-07-10', 1);

-- =============================================
-- sl_orders (20 rows)
-- =============================================
CREATE TABLE sl_orders (
    oid INTEGER PRIMARY KEY,
    ord_cust_email TEXT NOT NULL,
    ord_date TEXT NOT NULL,
    ord_status TEXT DEFAULT 'pending',
    ord_ship_line1 TEXT,
    ord_ship_city TEXT,
    ord_ship_state TEXT,
    ord_ship_zip TEXT,
    ord_ship_country TEXT DEFAULT 'US',
    ord_subtotal REAL,
    ord_tax REAL,
    ord_ship_cost REAL,
    ord_discount REAL DEFAULT 0,
    ord_total REAL,
    ord_notes TEXT
);

INSERT INTO sl_orders (oid, ord_cust_email, ord_date, ord_status, ord_ship_line1, ord_ship_city, ord_ship_state, ord_ship_zip, ord_ship_country, ord_subtotal, ord_tax, ord_ship_cost, ord_discount, ord_total, ord_notes) VALUES (1001, 'alice@email.com', '2024-09-15', 'delivered', '123 Maple St', 'Portland', 'OR', '97201', 'US', 1299.99, 104.00, 0.00, 0.00, 1403.99, NULL);
INSERT INTO sl_orders (oid, ord_cust_email, ord_date, ord_status, ord_ship_line1, ord_ship_city, ord_ship_state, ord_ship_zip, ord_ship_country, ord_subtotal, ord_tax, ord_ship_cost, ord_discount, ord_total, ord_notes) VALUES (1002, 'bob@email.com', '2024-09-20', 'delivered', '456 Oak Ave', 'Austin', 'TX', '78701', 'US', 929.98, 74.40, 9.99, 0.00, 1014.37, NULL);
INSERT INTO sl_orders (oid, ord_cust_email, ord_date, ord_status, ord_ship_line1, ord_ship_city, ord_ship_state, ord_ship_zip, ord_ship_country, ord_subtotal, ord_tax, ord_ship_cost, ord_discount, ord_total, ord_notes) VALUES (1003, 'carol@email.com', '2024-10-01', 'delivered', '789 Pine Rd', 'Seattle', 'WA', '98101', 'US', 199.99, 20.00, 5.99, 0.00, 225.98, 'Gift wrap requested');
INSERT INTO sl_orders (oid, ord_cust_email, ord_date, ord_status, ord_ship_line1, ord_ship_city, ord_ship_state, ord_ship_zip, ord_ship_country, ord_subtotal, ord_tax, ord_ship_cost, ord_discount, ord_total, ord_notes) VALUES (1004, 'dave@email.com', '2024-10-10', 'delivered', '321 Elm Blvd', 'Denver', 'CO', '80201', 'US', 89.98, 7.20, 5.99, 10.00, 93.17, 'Used coupon FALL10');
INSERT INTO sl_orders (oid, ord_cust_email, ord_date, ord_status, ord_ship_line1, ord_ship_city, ord_ship_state, ord_ship_zip, ord_ship_country, ord_subtotal, ord_tax, ord_ship_cost, ord_discount, ord_total, ord_notes) VALUES (1005, 'eve@email.com', '2024-10-18', 'delivered', '654 Birch Ln', 'Miami', 'FL', '33101', 'US', 549.99, 38.50, 0.00, 0.00, 588.49, NULL);
INSERT INTO sl_orders (oid, ord_cust_email, ord_date, ord_status, ord_ship_line1, ord_ship_city, ord_ship_state, ord_ship_zip, ord_ship_country, ord_subtotal, ord_tax, ord_ship_cost, ord_discount, ord_total, ord_notes) VALUES (1006, 'frank@email.com', '2024-11-02', 'delivered', '987 Cedar Ct', 'Chicago', 'IL', '60601', 'US', 319.98, 32.00, 0.00, 0.00, 351.98, NULL);
INSERT INTO sl_orders (oid, ord_cust_email, ord_date, ord_status, ord_ship_line1, ord_ship_city, ord_ship_state, ord_ship_zip, ord_ship_country, ord_subtotal, ord_tax, ord_ship_cost, ord_discount, ord_total, ord_notes) VALUES (1007, 'grace@email.com', '2024-11-15', 'delivered', '147 Walnut Dr', 'San Francisco', 'CA', '94101', 'US', 899.99, 81.00, 0.00, 50.00, 930.99, 'VIP discount applied');
INSERT INTO sl_orders (oid, ord_cust_email, ord_date, ord_status, ord_ship_line1, ord_ship_city, ord_ship_state, ord_ship_zip, ord_ship_country, ord_subtotal, ord_tax, ord_ship_cost, ord_discount, ord_total, ord_notes) VALUES (1008, 'henry@email.com', '2024-11-28', 'delivered', '258 Spruce Way', 'Boston', 'MA', '02101', 'US', 169.98, 10.63, 5.99, 0.00, 186.60, 'Black Friday order');
INSERT INTO sl_orders (oid, ord_cust_email, ord_date, ord_status, ord_ship_line1, ord_ship_city, ord_ship_state, ord_ship_zip, ord_ship_country, ord_subtotal, ord_tax, ord_ship_cost, ord_discount, ord_total, ord_notes) VALUES (1009, 'ivy@email.com', '2024-12-05', 'delivered', '369 Ash Pl', 'Phoenix', 'AZ', '85001', 'US', 279.98, 23.52, 0.00, 0.00, 303.50, NULL);
INSERT INTO sl_orders (oid, ord_cust_email, ord_date, ord_status, ord_ship_line1, ord_ship_city, ord_ship_state, ord_ship_zip, ord_ship_country, ord_subtotal, ord_tax, ord_ship_cost, ord_discount, ord_total, ord_notes) VALUES (1010, 'jack@email.com', '2024-12-12', 'delivered', '480 Poplar St', 'Nashville', 'TN', '37201', 'US', 39.99, 3.70, 5.99, 0.00, 49.68, NULL);
INSERT INTO sl_orders (oid, ord_cust_email, ord_date, ord_status, ord_ship_line1, ord_ship_city, ord_ship_state, ord_ship_zip, ord_ship_country, ord_subtotal, ord_tax, ord_ship_cost, ord_discount, ord_total, ord_notes) VALUES (1011, 'kate@email.com', '2024-12-20', 'delivered', '591 Hickory Ave', 'Atlanta', 'GA', '30301', 'US', 499.97, 40.00, 0.00, 25.00, 514.97, 'Holiday sale');
INSERT INTO sl_orders (oid, ord_cust_email, ord_date, ord_status, ord_ship_line1, ord_ship_city, ord_ship_state, ord_ship_zip, ord_ship_country, ord_subtotal, ord_tax, ord_ship_cost, ord_discount, ord_total, ord_notes) VALUES (1012, 'alice@email.com', '2025-01-05', 'delivered', '123 Maple St', 'Portland', 'OR', '97201', 'US', 249.99, 20.00, 0.00, 0.00, 269.99, NULL);
INSERT INTO sl_orders (oid, ord_cust_email, ord_date, ord_status, ord_ship_line1, ord_ship_city, ord_ship_state, ord_ship_zip, ord_ship_country, ord_subtotal, ord_tax, ord_ship_cost, ord_discount, ord_total, ord_notes) VALUES (1013, 'leo@email.com', '2025-01-15', 'delivered', '702 Sycamore Rd', 'San Diego', 'CA', '92101', 'US', 119.99, 10.80, 5.99, 0.00, 136.78, NULL);
INSERT INTO sl_orders (oid, ord_cust_email, ord_date, ord_status, ord_ship_line1, ord_ship_city, ord_ship_state, ord_ship_zip, ord_ship_country, ord_subtotal, ord_tax, ord_ship_cost, ord_discount, ord_total, ord_notes) VALUES (1014, 'bob@email.com', '2025-01-28', 'shipped', '456 Oak Ave', 'Austin', 'TX', '78701', 'US', 149.99, 12.38, 5.99, 0.00, 168.36, NULL);
INSERT INTO sl_orders (oid, ord_cust_email, ord_date, ord_status, ord_ship_line1, ord_ship_city, ord_ship_state, ord_ship_zip, ord_ship_country, ord_subtotal, ord_tax, ord_ship_cost, ord_discount, ord_total, ord_notes) VALUES (1015, 'carol@email.com', '2025-02-10', 'shipped', '789 Pine Rd', 'Seattle', 'WA', '98101', 'US', 69.99, 7.00, 5.99, 0.00, 82.98, NULL);
INSERT INTO sl_orders (oid, ord_cust_email, ord_date, ord_status, ord_ship_line1, ord_ship_city, ord_ship_state, ord_ship_zip, ord_ship_country, ord_subtotal, ord_tax, ord_ship_cost, ord_discount, ord_total, ord_notes) VALUES (1016, 'eve@email.com', '2025-02-20', 'processing', '654 Birch Ln', 'Miami', 'FL', '33101', 'US', 1349.98, 94.50, 0.00, 0.00, 1444.48, 'Large order');
INSERT INTO sl_orders (oid, ord_cust_email, ord_date, ord_status, ord_ship_line1, ord_ship_city, ord_ship_state, ord_ship_zip, ord_ship_country, ord_subtotal, ord_tax, ord_ship_cost, ord_discount, ord_total, ord_notes) VALUES (1017, 'grace@email.com', '2025-03-01', 'processing', '147 Walnut Dr', 'San Francisco', 'CA', '94101', 'US', 59.99, 5.40, 5.99, 0.00, 71.38, NULL);
INSERT INTO sl_orders (oid, ord_cust_email, ord_date, ord_status, ord_ship_line1, ord_ship_city, ord_ship_state, ord_ship_zip, ord_ship_country, ord_subtotal, ord_tax, ord_ship_cost, ord_discount, ord_total, ord_notes) VALUES (1018, 'henry@email.com', '2025-03-10', 'pending', '258 Spruce Way', 'Boston', 'MA', '02101', 'US', 79.99, 5.00, 5.99, 0.00, 90.98, NULL);
INSERT INTO sl_orders (oid, ord_cust_email, ord_date, ord_status, ord_ship_line1, ord_ship_city, ord_ship_state, ord_ship_zip, ord_ship_country, ord_subtotal, ord_tax, ord_ship_cost, ord_discount, ord_total, ord_notes) VALUES (1019, 'ivy@email.com', '2025-03-15', 'pending', '369 Ash Pl', 'Phoenix', 'AZ', '85001', 'US', 49.99, 4.20, 5.99, 5.00, 55.18, 'Used coupon SPRING5');
INSERT INTO sl_orders (oid, ord_cust_email, ord_date, ord_status, ord_ship_line1, ord_ship_city, ord_ship_state, ord_ship_zip, ord_ship_country, ord_subtotal, ord_tax, ord_ship_cost, ord_discount, ord_total, ord_notes) VALUES (1020, 'dave@email.com', '2025-03-22', 'cancelled', '321 Elm Blvd', 'Denver', 'CO', '80201', 'US', 899.99, 63.00, 0.00, 0.00, 962.99, 'Customer cancelled');

-- =============================================
-- sl_order_items (35 rows)
-- =============================================
CREATE TABLE sl_order_items (
    oiid INTEGER PRIMARY KEY,
    oi_order_id INTEGER NOT NULL,
    oi_prod_sku TEXT NOT NULL,
    oi_prod_name TEXT NOT NULL,
    oi_prod_price REAL NOT NULL,
    oi_variant_sku TEXT,
    oi_qty INTEGER DEFAULT 1,
    oi_subtotal REAL,
    oi_discount REAL DEFAULT 0,
    oi_tax REAL DEFAULT 0,
    oi_status TEXT DEFAULT 'active'
);

INSERT INTO sl_order_items (oiid, oi_order_id, oi_prod_sku, oi_prod_name, oi_prod_price, oi_variant_sku, oi_qty, oi_subtotal, oi_discount, oi_tax, oi_status) VALUES (1, 1001, 'SL-LAPTOP-001', 'ProBook Laptop 15"', 1299.99, 'SL-LAPTOP-001-GRY-16', 1, 1299.99, 0.00, 104.00, 'delivered');
INSERT INTO sl_order_items (oiid, oi_order_id, oi_prod_sku, oi_prod_name, oi_prod_price, oi_variant_sku, oi_qty, oi_subtotal, oi_discount, oi_tax, oi_status) VALUES (2, 1002, 'SL-PHONE-002', 'SmartEdge Phone X', 899.99, 'SL-PHONE-002-BLK-128', 1, 899.99, 0.00, 72.00, 'delivered');
INSERT INTO sl_order_items (oiid, oi_order_id, oi_prod_sku, oi_prod_name, oi_prod_price, oi_variant_sku, oi_qty, oi_subtotal, oi_discount, oi_tax, oi_status) VALUES (3, 1002, 'SL-TSHIRT-005', 'Classic Cotton Tee', 29.99, 'SL-TSHIRT-005-WHT-M', 1, 29.99, 0.00, 2.40, 'delivered');
INSERT INTO sl_order_items (oiid, oi_order_id, oi_prod_sku, oi_prod_name, oi_prod_price, oi_variant_sku, oi_qty, oi_subtotal, oi_discount, oi_tax, oi_status) VALUES (4, 1003, 'SL-HEADPH-004', 'BassWave Wireless Headphones', 199.99, 'SL-HEADPH-004-BLK', 1, 199.99, 0.00, 20.00, 'delivered');
INSERT INTO sl_order_items (oiid, oi_order_id, oi_prod_sku, oi_prod_name, oi_prod_price, oi_variant_sku, oi_qty, oi_subtotal, oi_discount, oi_tax, oi_status) VALUES (5, 1004, 'SL-TSHIRT-005', 'Classic Cotton Tee', 29.99, 'SL-TSHIRT-005-BLK-L', 2, 59.98, 5.00, 4.40, 'delivered');
INSERT INTO sl_order_items (oiid, oi_order_id, oi_prod_sku, oi_prod_name, oi_prod_price, oi_variant_sku, oi_qty, oi_subtotal, oi_discount, oi_tax, oi_status) VALUES (6, 1004, 'SL-MUG-015', 'Ceramic Travel Mug', 19.99, 'SL-MUG-015-TEL', 1, 19.99, 5.00, 1.20, 'delivered');
INSERT INTO sl_order_items (oiid, oi_order_id, oi_prod_sku, oi_prod_name, oi_prod_price, oi_variant_sku, oi_qty, oi_subtotal, oi_discount, oi_tax, oi_status) VALUES (7, 1004, 'SL-MUG-015', 'Ceramic Travel Mug', 19.99, 'SL-MUG-015-CHR', 1, 19.99, 0.00, 1.60, 'delivered');
INSERT INTO sl_order_items (oiid, oi_order_id, oi_prod_sku, oi_prod_name, oi_prod_price, oi_variant_sku, oi_qty, oi_subtotal, oi_discount, oi_tax, oi_status) VALUES (8, 1005, 'SL-TABLET-003', 'SlateView Tablet 10"', 549.99, NULL, 1, 549.99, 0.00, 38.50, 'delivered');
INSERT INTO sl_order_items (oiid, oi_order_id, oi_prod_sku, oi_prod_name, oi_prod_price, oi_variant_sku, oi_qty, oi_subtotal, oi_discount, oi_tax, oi_status) VALUES (9, 1006, 'SL-JEANS-006', 'Slim Fit Denim Jeans', 69.99, 'SL-JEANS-006-BLU-32', 2, 139.98, 0.00, 14.00, 'delivered');
INSERT INTO sl_order_items (oiid, oi_order_id, oi_prod_sku, oi_prod_name, oi_prod_price, oi_variant_sku, oi_qty, oi_subtotal, oi_discount, oi_tax, oi_status) VALUES (10, 1006, 'SL-JACKET-008', 'Weathershield Rain Jacket', 149.99, 'SL-JACKET-008-NVY-M', 1, 149.99, 0.00, 15.00, 'delivered');
INSERT INTO sl_order_items (oiid, oi_order_id, oi_prod_sku, oi_prod_name, oi_prod_price, oi_variant_sku, oi_qty, oi_subtotal, oi_discount, oi_tax, oi_status) VALUES (11, 1006, 'SL-TSHIRT-005', 'Classic Cotton Tee', 29.99, 'SL-TSHIRT-005-WHT-S', 1, 29.99, 0.00, 3.00, 'delivered');
INSERT INTO sl_order_items (oiid, oi_order_id, oi_prod_sku, oi_prod_name, oi_prod_price, oi_variant_sku, oi_qty, oi_subtotal, oi_discount, oi_tax, oi_status) VALUES (12, 1007, 'SL-PHONE-002', 'SmartEdge Phone X', 899.99, 'SL-PHONE-002-WHT-256', 1, 899.99, 50.00, 81.00, 'delivered');
INSERT INTO sl_order_items (oiid, oi_order_id, oi_prod_sku, oi_prod_name, oi_prod_price, oi_variant_sku, oi_qty, oi_subtotal, oi_discount, oi_tax, oi_status) VALUES (13, 1008, 'SL-SNEAK-007', 'RunFlex Sneakers', 119.99, 'SL-SNEAK-007-WHT-9', 1, 119.99, 0.00, 7.50, 'delivered');
INSERT INTO sl_order_items (oiid, oi_order_id, oi_prod_sku, oi_prod_name, oi_prod_price, oi_variant_sku, oi_qty, oi_subtotal, oi_discount, oi_tax, oi_status) VALUES (14, 1008, 'SL-CHARGER-014', 'QuickCharge USB-C Hub', 49.99, NULL, 1, 49.99, 0.00, 3.13, 'delivered');
INSERT INTO sl_order_items (oiid, oi_order_id, oi_prod_sku, oi_prod_name, oi_prod_price, oi_variant_sku, oi_qty, oi_subtotal, oi_discount, oi_tax, oi_status) VALUES (15, 1009, 'SL-WATCH-011', 'ChronoFit Smartwatch', 249.99, 'SL-WATCH-011-BLK', 1, 249.99, 0.00, 21.00, 'delivered');
INSERT INTO sl_order_items (oiid, oi_order_id, oi_prod_sku, oi_prod_name, oi_prod_price, oi_variant_sku, oi_qty, oi_subtotal, oi_discount, oi_tax, oi_status) VALUES (16, 1009, 'SL-TSHIRT-005', 'Classic Cotton Tee', 29.99, 'SL-TSHIRT-005-WHT-M', 1, 29.99, 0.00, 2.52, 'delivered');
INSERT INTO sl_order_items (oiid, oi_order_id, oi_prod_sku, oi_prod_name, oi_prod_price, oi_variant_sku, oi_qty, oi_subtotal, oi_discount, oi_tax, oi_status) VALUES (17, 1010, 'SL-BOOK-013', 'SQL Mastery Handbook', 39.99, NULL, 1, 39.99, 0.00, 3.70, 'delivered');
INSERT INTO sl_order_items (oiid, oi_order_id, oi_prod_sku, oi_prod_name, oi_prod_price, oi_variant_sku, oi_qty, oi_subtotal, oi_discount, oi_tax, oi_status) VALUES (18, 1011, 'SL-WATCH-011', 'ChronoFit Smartwatch', 249.99, 'SL-WATCH-011-RGD', 1, 249.99, 12.50, 20.00, 'delivered');
INSERT INTO sl_order_items (oiid, oi_order_id, oi_prod_sku, oi_prod_name, oi_prod_price, oi_variant_sku, oi_qty, oi_subtotal, oi_discount, oi_tax, oi_status) VALUES (19, 1011, 'SL-HEADPH-004', 'BassWave Wireless Headphones', 199.99, 'SL-HEADPH-004-WHT', 1, 199.99, 12.50, 16.00, 'delivered');
INSERT INTO sl_order_items (oiid, oi_order_id, oi_prod_sku, oi_prod_name, oi_prod_price, oi_variant_sku, oi_qty, oi_subtotal, oi_discount, oi_tax, oi_status) VALUES (20, 1011, 'SL-CHARGER-014', 'QuickCharge USB-C Hub', 49.99, NULL, 1, 49.99, 0.00, 4.00, 'delivered');
INSERT INTO sl_order_items (oiid, oi_order_id, oi_prod_sku, oi_prod_name, oi_prod_price, oi_variant_sku, oi_qty, oi_subtotal, oi_discount, oi_tax, oi_status) VALUES (21, 1012, 'SL-WATCH-011', 'ChronoFit Smartwatch', 249.99, 'SL-WATCH-011-BLK', 1, 249.99, 0.00, 20.00, 'delivered');
INSERT INTO sl_order_items (oiid, oi_order_id, oi_prod_sku, oi_prod_name, oi_prod_price, oi_variant_sku, oi_qty, oi_subtotal, oi_discount, oi_tax, oi_status) VALUES (22, 1013, 'SL-SNEAK-007', 'RunFlex Sneakers', 119.99, 'SL-SNEAK-007-BLK-10', 1, 119.99, 0.00, 10.80, 'delivered');
INSERT INTO sl_order_items (oiid, oi_order_id, oi_prod_sku, oi_prod_name, oi_prod_price, oi_variant_sku, oi_qty, oi_subtotal, oi_discount, oi_tax, oi_status) VALUES (23, 1014, 'SL-JACKET-008', 'Weathershield Rain Jacket', 149.99, 'SL-JACKET-008-RED-L', 1, 149.99, 0.00, 12.38, 'shipped');
INSERT INTO sl_order_items (oiid, oi_order_id, oi_prod_sku, oi_prod_name, oi_prod_price, oi_variant_sku, oi_qty, oi_subtotal, oi_discount, oi_tax, oi_status) VALUES (24, 1015, 'SL-JEANS-006', 'Slim Fit Denim Jeans', 69.99, 'SL-JEANS-006-BLK-30', 1, 69.99, 0.00, 7.00, 'shipped');
INSERT INTO sl_order_items (oiid, oi_order_id, oi_prod_sku, oi_prod_name, oi_prod_price, oi_variant_sku, oi_qty, oi_subtotal, oi_discount, oi_tax, oi_status) VALUES (25, 1016, 'SL-LAPTOP-001', 'ProBook Laptop 15"', 1299.99, 'SL-LAPTOP-001-SLV-8', 1, 1299.99, 0.00, 91.00, 'processing');
INSERT INTO sl_order_items (oiid, oi_order_id, oi_prod_sku, oi_prod_name, oi_prod_price, oi_variant_sku, oi_qty, oi_subtotal, oi_discount, oi_tax, oi_status) VALUES (26, 1016, 'SL-CHARGER-014', 'QuickCharge USB-C Hub', 49.99, NULL, 1, 49.99, 0.00, 3.50, 'processing');
INSERT INTO sl_order_items (oiid, oi_order_id, oi_prod_sku, oi_prod_name, oi_prod_price, oi_variant_sku, oi_qty, oi_subtotal, oi_discount, oi_tax, oi_status) VALUES (27, 1017, 'SL-BACKP-012', 'TrekPack Laptop Backpack', 59.99, NULL, 1, 59.99, 0.00, 5.40, 'processing');
INSERT INTO sl_order_items (oiid, oi_order_id, oi_prod_sku, oi_prod_name, oi_prod_price, oi_variant_sku, oi_qty, oi_subtotal, oi_discount, oi_tax, oi_status) VALUES (28, 1018, 'SL-COFFM-010', 'BrewMaster Coffee Maker', 79.99, NULL, 1, 79.99, 0.00, 5.00, 'pending');
INSERT INTO sl_order_items (oiid, oi_order_id, oi_prod_sku, oi_prod_name, oi_prod_price, oi_variant_sku, oi_qty, oi_subtotal, oi_discount, oi_tax, oi_status) VALUES (29, 1019, 'SL-CHARGER-014', 'QuickCharge USB-C Hub', 49.99, NULL, 1, 49.99, 5.00, 4.20, 'pending');
INSERT INTO sl_order_items (oiid, oi_order_id, oi_prod_sku, oi_prod_name, oi_prod_price, oi_variant_sku, oi_qty, oi_subtotal, oi_discount, oi_tax, oi_status) VALUES (30, 1020, 'SL-PHONE-002', 'SmartEdge Phone X', 899.99, 'SL-PHONE-002-BLK-128', 1, 899.99, 0.00, 63.00, 'cancelled');
INSERT INTO sl_order_items (oiid, oi_order_id, oi_prod_sku, oi_prod_name, oi_prod_price, oi_variant_sku, oi_qty, oi_subtotal, oi_discount, oi_tax, oi_status) VALUES (31, 1001, 'SL-CHARGER-014', 'QuickCharge USB-C Hub', 49.99, NULL, 0, 0.00, 0.00, 0.00, 'cancelled');
INSERT INTO sl_order_items (oiid, oi_order_id, oi_prod_sku, oi_prod_name, oi_prod_price, oi_variant_sku, oi_qty, oi_subtotal, oi_discount, oi_tax, oi_status) VALUES (32, 1003, 'SL-MUG-015', 'Ceramic Travel Mug', 19.99, 'SL-MUG-015-TEL', 2, 39.98, 0.00, 4.00, 'delivered');
INSERT INTO sl_order_items (oiid, oi_order_id, oi_prod_sku, oi_prod_name, oi_prod_price, oi_variant_sku, oi_qty, oi_subtotal, oi_discount, oi_tax, oi_status) VALUES (33, 1007, 'SL-BACKP-012', 'TrekPack Laptop Backpack', 59.99, NULL, 1, 59.99, 0.00, 5.40, 'delivered');
INSERT INTO sl_order_items (oiid, oi_order_id, oi_prod_sku, oi_prod_name, oi_prod_price, oi_variant_sku, oi_qty, oi_subtotal, oi_discount, oi_tax, oi_status) VALUES (34, 1012, 'SL-BLNDR-009', 'PowerBlend Pro Blender', 89.99, NULL, 1, 89.99, 0.00, 7.20, 'delivered');
INSERT INTO sl_order_items (oiid, oi_order_id, oi_prod_sku, oi_prod_name, oi_prod_price, oi_variant_sku, oi_qty, oi_subtotal, oi_discount, oi_tax, oi_status) VALUES (35, 1009, 'SL-MUG-015', 'Ceramic Travel Mug', 19.99, 'SL-MUG-015-CHR', 1, 19.99, 0.00, 1.68, 'delivered');

-- =============================================
-- sl_payments (20 rows)
-- =============================================
CREATE TABLE sl_payments (
    payid INTEGER PRIMARY KEY,
    pay_order_id INTEGER NOT NULL,
    pay_cust_email TEXT NOT NULL,
    pay_amount REAL NOT NULL,
    pay_method TEXT,
    pay_status TEXT DEFAULT 'pending',
    pay_txn_id TEXT,
    pay_gateway TEXT,
    pay_processed_at TEXT,
    pay_currency TEXT DEFAULT 'USD',
    pay_fee REAL DEFAULT 0
);

INSERT INTO sl_payments (payid, pay_order_id, pay_cust_email, pay_amount, pay_method, pay_status, pay_txn_id, pay_gateway, pay_processed_at, pay_currency, pay_fee) VALUES (1, 1001, 'alice@email.com', 1403.99, 'credit_card', 'completed', 'TXN-20240915-001', 'stripe', '2024-09-15 10:23:00', 'USD', 40.72);
INSERT INTO sl_payments (payid, pay_order_id, pay_cust_email, pay_amount, pay_method, pay_status, pay_txn_id, pay_gateway, pay_processed_at, pay_currency, pay_fee) VALUES (2, 1002, 'bob@email.com', 1014.37, 'credit_card', 'completed', 'TXN-20240920-002', 'stripe', '2024-09-20 14:05:00', 'USD', 29.42);
INSERT INTO sl_payments (payid, pay_order_id, pay_cust_email, pay_amount, pay_method, pay_status, pay_txn_id, pay_gateway, pay_processed_at, pay_currency, pay_fee) VALUES (3, 1003, 'carol@email.com', 225.98, 'paypal', 'completed', 'TXN-20241001-003', 'paypal', '2024-10-01 09:12:00', 'USD', 6.78);
INSERT INTO sl_payments (payid, pay_order_id, pay_cust_email, pay_amount, pay_method, pay_status, pay_txn_id, pay_gateway, pay_processed_at, pay_currency, pay_fee) VALUES (4, 1004, 'dave@email.com', 93.17, 'debit_card', 'completed', 'TXN-20241010-004', 'stripe', '2024-10-10 11:45:00', 'USD', 2.70);
INSERT INTO sl_payments (payid, pay_order_id, pay_cust_email, pay_amount, pay_method, pay_status, pay_txn_id, pay_gateway, pay_processed_at, pay_currency, pay_fee) VALUES (5, 1005, 'eve@email.com', 588.49, 'credit_card', 'completed', 'TXN-20241018-005', 'stripe', '2024-10-18 16:30:00', 'USD', 17.07);
INSERT INTO sl_payments (payid, pay_order_id, pay_cust_email, pay_amount, pay_method, pay_status, pay_txn_id, pay_gateway, pay_processed_at, pay_currency, pay_fee) VALUES (6, 1006, 'frank@email.com', 351.98, 'credit_card', 'completed', 'TXN-20241102-006', 'stripe', '2024-11-02 13:20:00', 'USD', 10.21);
INSERT INTO sl_payments (payid, pay_order_id, pay_cust_email, pay_amount, pay_method, pay_status, pay_txn_id, pay_gateway, pay_processed_at, pay_currency, pay_fee) VALUES (7, 1007, 'grace@email.com', 930.99, 'credit_card', 'completed', 'TXN-20241115-007', 'stripe', '2024-11-15 10:55:00', 'USD', 27.00);
INSERT INTO sl_payments (payid, pay_order_id, pay_cust_email, pay_amount, pay_method, pay_status, pay_txn_id, pay_gateway, pay_processed_at, pay_currency, pay_fee) VALUES (8, 1008, 'henry@email.com', 186.60, 'paypal', 'completed', 'TXN-20241128-008', 'paypal', '2024-11-28 08:10:00', 'USD', 5.60);
INSERT INTO sl_payments (payid, pay_order_id, pay_cust_email, pay_amount, pay_method, pay_status, pay_txn_id, pay_gateway, pay_processed_at, pay_currency, pay_fee) VALUES (9, 1009, 'ivy@email.com', 303.50, 'credit_card', 'completed', 'TXN-20241205-009', 'stripe', '2024-12-05 15:40:00', 'USD', 8.80);
INSERT INTO sl_payments (payid, pay_order_id, pay_cust_email, pay_amount, pay_method, pay_status, pay_txn_id, pay_gateway, pay_processed_at, pay_currency, pay_fee) VALUES (10, 1010, 'jack@email.com', 49.68, 'debit_card', 'completed', 'TXN-20241212-010', 'stripe', '2024-12-12 12:05:00', 'USD', 1.44);
INSERT INTO sl_payments (payid, pay_order_id, pay_cust_email, pay_amount, pay_method, pay_status, pay_txn_id, pay_gateway, pay_processed_at, pay_currency, pay_fee) VALUES (11, 1011, 'kate@email.com', 514.97, 'credit_card', 'completed', 'TXN-20241220-011', 'stripe', '2024-12-20 17:22:00', 'USD', 14.93);
INSERT INTO sl_payments (payid, pay_order_id, pay_cust_email, pay_amount, pay_method, pay_status, pay_txn_id, pay_gateway, pay_processed_at, pay_currency, pay_fee) VALUES (12, 1012, 'alice@email.com', 269.99, 'credit_card', 'completed', 'TXN-20250105-012', 'stripe', '2025-01-05 09:30:00', 'USD', 7.83);
INSERT INTO sl_payments (payid, pay_order_id, pay_cust_email, pay_amount, pay_method, pay_status, pay_txn_id, pay_gateway, pay_processed_at, pay_currency, pay_fee) VALUES (13, 1013, 'leo@email.com', 136.78, 'paypal', 'completed', 'TXN-20250115-013', 'paypal', '2025-01-15 14:18:00', 'USD', 4.10);
INSERT INTO sl_payments (payid, pay_order_id, pay_cust_email, pay_amount, pay_method, pay_status, pay_txn_id, pay_gateway, pay_processed_at, pay_currency, pay_fee) VALUES (14, 1014, 'bob@email.com', 168.36, 'credit_card', 'completed', 'TXN-20250128-014', 'stripe', '2025-01-28 11:45:00', 'USD', 4.88);
INSERT INTO sl_payments (payid, pay_order_id, pay_cust_email, pay_amount, pay_method, pay_status, pay_txn_id, pay_gateway, pay_processed_at, pay_currency, pay_fee) VALUES (15, 1015, 'carol@email.com', 82.98, 'debit_card', 'completed', 'TXN-20250210-015', 'stripe', '2025-02-10 10:00:00', 'USD', 2.41);
INSERT INTO sl_payments (payid, pay_order_id, pay_cust_email, pay_amount, pay_method, pay_status, pay_txn_id, pay_gateway, pay_processed_at, pay_currency, pay_fee) VALUES (16, 1016, 'eve@email.com', 1444.48, 'credit_card', 'completed', 'TXN-20250220-016', 'stripe', '2025-02-20 16:50:00', 'USD', 41.89);
INSERT INTO sl_payments (payid, pay_order_id, pay_cust_email, pay_amount, pay_method, pay_status, pay_txn_id, pay_gateway, pay_processed_at, pay_currency, pay_fee) VALUES (17, 1017, 'grace@email.com', 71.38, 'paypal', 'completed', 'TXN-20250301-017', 'paypal', '2025-03-01 13:25:00', 'USD', 2.14);
INSERT INTO sl_payments (payid, pay_order_id, pay_cust_email, pay_amount, pay_method, pay_status, pay_txn_id, pay_gateway, pay_processed_at, pay_currency, pay_fee) VALUES (18, 1018, 'henry@email.com', 90.98, 'credit_card', 'pending', 'TXN-20250310-018', 'stripe', NULL, 'USD', 0.00);
INSERT INTO sl_payments (payid, pay_order_id, pay_cust_email, pay_amount, pay_method, pay_status, pay_txn_id, pay_gateway, pay_processed_at, pay_currency, pay_fee) VALUES (19, 1019, 'ivy@email.com', 55.18, 'debit_card', 'pending', 'TXN-20250315-019', 'stripe', NULL, 'USD', 0.00);
INSERT INTO sl_payments (payid, pay_order_id, pay_cust_email, pay_amount, pay_method, pay_status, pay_txn_id, pay_gateway, pay_processed_at, pay_currency, pay_fee) VALUES (20, 1020, 'dave@email.com', 962.99, 'credit_card', 'refunded', 'TXN-20250322-020', 'stripe', '2025-03-22 09:15:00', 'USD', 27.93);

-- =============================================
-- sl_refunds (6 rows)
-- =============================================
CREATE TABLE sl_refunds (
    rfid INTEGER PRIMARY KEY,
    rf_order_id INTEGER NOT NULL,
    rf_cust_email TEXT NOT NULL,
    rf_amount REAL NOT NULL,
    rf_reason TEXT,
    rf_status TEXT DEFAULT 'requested',
    rf_method TEXT,
    rf_requested_at TEXT,
    rf_processed_at TEXT,
    rf_processed_by TEXT,
    rf_notes TEXT
);

INSERT INTO sl_refunds (rfid, rf_order_id, rf_cust_email, rf_amount, rf_reason, rf_status, rf_method, rf_requested_at, rf_processed_at, rf_processed_by, rf_notes) VALUES (1, 1020, 'dave@email.com', 962.99, 'Customer cancelled order', 'completed', 'original_payment', '2025-03-22', '2025-03-23', 'agent_sarah', 'Full refund for cancelled order');
INSERT INTO sl_refunds (rfid, rf_order_id, rf_cust_email, rf_amount, rf_reason, rf_status, rf_method, rf_requested_at, rf_processed_at, rf_processed_by, rf_notes) VALUES (2, 1003, 'carol@email.com', 39.98, 'Defective mugs received', 'completed', 'store_credit', '2024-10-15', '2024-10-18', 'agent_mike', 'Partial refund for 2 damaged mugs');
INSERT INTO sl_refunds (rfid, rf_order_id, rf_cust_email, rf_amount, rf_reason, rf_status, rf_method, rf_requested_at, rf_processed_at, rf_processed_by, rf_notes) VALUES (3, 1004, 'dave@email.com', 19.99, 'Wrong color received', 'completed', 'original_payment', '2024-10-20', '2024-10-22', 'agent_jenny', 'Refund for charcoal mug, wanted teal');
INSERT INTO sl_refunds (rfid, rf_order_id, rf_cust_email, rf_amount, rf_reason, rf_status, rf_method, rf_requested_at, rf_processed_at, rf_processed_by, rf_notes) VALUES (4, 1008, 'henry@email.com', 49.99, 'Item not as described', 'processing', 'original_payment', '2024-12-10', NULL, NULL, 'USB-C hub missing ports');
INSERT INTO sl_refunds (rfid, rf_order_id, rf_cust_email, rf_amount, rf_reason, rf_status, rf_method, rf_requested_at, rf_processed_at, rf_processed_by, rf_notes) VALUES (5, 1006, 'frank@email.com', 29.99, 'Size too small', 'completed', 'original_payment', '2024-11-15', '2024-11-18', 'agent_sarah', 'Refund for t-shirt, wrong size ordered');
INSERT INTO sl_refunds (rfid, rf_order_id, rf_cust_email, rf_amount, rf_reason, rf_status, rf_method, rf_requested_at, rf_processed_at, rf_processed_by, rf_notes) VALUES (6, 1013, 'leo@email.com', 119.99, 'Shoes too tight', 'requested', 'original_payment', '2025-02-01', NULL, NULL, 'Customer wants exchange or refund');

-- =============================================
-- sl_warehouses (4 rows)
-- =============================================
CREATE TABLE sl_warehouses (
    wid INTEGER PRIMARY KEY,
    wh_name TEXT NOT NULL,
    wh_code TEXT NOT NULL,
    wh_addr TEXT,
    wh_city TEXT,
    wh_state TEXT,
    wh_zip TEXT,
    wh_country TEXT DEFAULT 'US',
    wh_mgr_email TEXT,
    wh_phone TEXT,
    wh_capacity INTEGER,
    wh_is_active INTEGER DEFAULT 1
);

INSERT INTO sl_warehouses (wid, wh_name, wh_code, wh_addr, wh_city, wh_state, wh_zip, wh_country, wh_mgr_email, wh_phone, wh_capacity, wh_is_active) VALUES (1, 'East Hub', 'WH-EAST', '100 Industrial Pkwy', 'Newark', 'NJ', '07101', 'US', 'mgr.east@shoplocal.com', '555-9001', 50000, 1);
INSERT INTO sl_warehouses (wid, wh_name, wh_code, wh_addr, wh_city, wh_state, wh_zip, wh_country, wh_mgr_email, wh_phone, wh_capacity, wh_is_active) VALUES (2, 'West Hub', 'WH-WEST', '200 Commerce Dr', 'Reno', 'NV', '89501', 'US', 'mgr.west@shoplocal.com', '555-9002', 45000, 1);
INSERT INTO sl_warehouses (wid, wh_name, wh_code, wh_addr, wh_city, wh_state, wh_zip, wh_country, wh_mgr_email, wh_phone, wh_capacity, wh_is_active) VALUES (3, 'Central Depot', 'WH-CENT', '300 Logistics Blvd', 'Memphis', 'TN', '38101', 'US', 'mgr.central@shoplocal.com', '555-9003', 60000, 1);
INSERT INTO sl_warehouses (wid, wh_name, wh_code, wh_addr, wh_city, wh_state, wh_zip, wh_country, wh_mgr_email, wh_phone, wh_capacity, wh_is_active) VALUES (4, 'South Center', 'WH-SOUTH', '400 Freight Rd', 'Dallas', 'TX', '75201', 'US', 'mgr.south@shoplocal.com', '555-9004', 35000, 1);

-- =============================================
-- sl_inventory (15 rows)
-- =============================================
CREATE TABLE sl_inventory (
    invid INTEGER PRIMARY KEY,
    inv_prod_sku TEXT NOT NULL,
    inv_wh_name TEXT NOT NULL,
    inv_qty INTEGER DEFAULT 0,
    inv_reserved INTEGER DEFAULT 0,
    inv_available INTEGER DEFAULT 0,
    inv_reorder_pt INTEGER DEFAULT 10,
    inv_reorder_qty INTEGER DEFAULT 50,
    inv_last_restock TEXT,
    inv_last_sold TEXT,
    inv_cost REAL
);

INSERT INTO sl_inventory (invid, inv_prod_sku, inv_wh_name, inv_qty, inv_reserved, inv_available, inv_reorder_pt, inv_reorder_qty, inv_last_restock, inv_last_sold, inv_cost) VALUES (1, 'SL-LAPTOP-001', 'East Hub', 30, 5, 25, 10, 20, '2025-02-01', '2025-03-20', 850.00);
INSERT INTO sl_inventory (invid, inv_prod_sku, inv_wh_name, inv_qty, inv_reserved, inv_available, inv_reorder_pt, inv_reorder_qty, inv_last_restock, inv_last_sold, inv_cost) VALUES (2, 'SL-LAPTOP-001', 'West Hub', 15, 2, 13, 10, 20, '2025-01-15', '2025-03-18', 850.00);
INSERT INTO sl_inventory (invid, inv_prod_sku, inv_wh_name, inv_qty, inv_reserved, inv_available, inv_reorder_pt, inv_reorder_qty, inv_last_restock, inv_last_sold, inv_cost) VALUES (3, 'SL-PHONE-002', 'East Hub', 50, 8, 42, 15, 30, '2025-02-15', '2025-03-22', 520.00);
INSERT INTO sl_inventory (invid, inv_prod_sku, inv_wh_name, inv_qty, inv_reserved, inv_available, inv_reorder_pt, inv_reorder_qty, inv_last_restock, inv_last_sold, inv_cost) VALUES (4, 'SL-PHONE-002', 'Central Depot', 35, 3, 32, 15, 30, '2025-01-20', '2025-03-15', 520.00);
INSERT INTO sl_inventory (invid, inv_prod_sku, inv_wh_name, inv_qty, inv_reserved, inv_available, inv_reorder_pt, inv_reorder_qty, inv_last_restock, inv_last_sold, inv_cost) VALUES (5, 'SL-TSHIRT-005', 'Central Depot', 200, 10, 190, 50, 100, '2025-03-01', '2025-03-25', 8.50);
INSERT INTO sl_inventory (invid, inv_prod_sku, inv_wh_name, inv_qty, inv_reserved, inv_available, inv_reorder_pt, inv_reorder_qty, inv_last_restock, inv_last_sold, inv_cost) VALUES (6, 'SL-HEADPH-004', 'West Hub', 80, 5, 75, 20, 40, '2025-02-10', '2025-03-20', 85.00);
INSERT INTO sl_inventory (invid, inv_prod_sku, inv_wh_name, inv_qty, inv_reserved, inv_available, inv_reorder_pt, inv_reorder_qty, inv_last_restock, inv_last_sold, inv_cost) VALUES (7, 'SL-JEANS-006', 'East Hub', 100, 8, 92, 25, 50, '2025-02-20', '2025-03-18', 25.00);
INSERT INTO sl_inventory (invid, inv_prod_sku, inv_wh_name, inv_qty, inv_reserved, inv_available, inv_reorder_pt, inv_reorder_qty, inv_last_restock, inv_last_sold, inv_cost) VALUES (8, 'SL-SNEAK-007', 'South Center', 40, 3, 37, 10, 25, '2025-01-25', '2025-03-10', 42.00);
INSERT INTO sl_inventory (invid, inv_prod_sku, inv_wh_name, inv_qty, inv_reserved, inv_available, inv_reorder_pt, inv_reorder_qty, inv_last_restock, inv_last_sold, inv_cost) VALUES (9, 'SL-BLNDR-009', 'Central Depot', 25, 2, 23, 8, 15, '2025-01-10', '2025-03-05', 35.00);
INSERT INTO sl_inventory (invid, inv_prod_sku, inv_wh_name, inv_qty, inv_reserved, inv_available, inv_reorder_pt, inv_reorder_qty, inv_last_restock, inv_last_sold, inv_cost) VALUES (10, 'SL-COFFM-010', 'East Hub', 18, 1, 17, 8, 15, '2025-02-05', '2025-03-10', 30.00);
INSERT INTO sl_inventory (invid, inv_prod_sku, inv_wh_name, inv_qty, inv_reserved, inv_available, inv_reorder_pt, inv_reorder_qty, inv_last_restock, inv_last_sold, inv_cost) VALUES (11, 'SL-WATCH-011', 'West Hub', 35, 4, 31, 10, 20, '2025-02-25', '2025-03-22', 110.00);
INSERT INTO sl_inventory (invid, inv_prod_sku, inv_wh_name, inv_qty, inv_reserved, inv_available, inv_reorder_pt, inv_reorder_qty, inv_last_restock, inv_last_sold, inv_cost) VALUES (12, 'SL-BACKP-012', 'Central Depot', 60, 5, 55, 15, 30, '2025-03-01', '2025-03-20', 18.00);
INSERT INTO sl_inventory (invid, inv_prod_sku, inv_wh_name, inv_qty, inv_reserved, inv_available, inv_reorder_pt, inv_reorder_qty, inv_last_restock, inv_last_sold, inv_cost) VALUES (13, 'SL-BOOK-013', 'East Hub', 45, 0, 45, 10, 30, '2025-01-05', '2025-03-12', 12.00);
INSERT INTO sl_inventory (invid, inv_prod_sku, inv_wh_name, inv_qty, inv_reserved, inv_available, inv_reorder_pt, inv_reorder_qty, inv_last_restock, inv_last_sold, inv_cost) VALUES (14, 'SL-CHARGER-014', 'South Center', 90, 6, 84, 20, 50, '2025-02-28', '2025-03-25', 15.00);
INSERT INTO sl_inventory (invid, inv_prod_sku, inv_wh_name, inv_qty, inv_reserved, inv_available, inv_reorder_pt, inv_reorder_qty, inv_last_restock, inv_last_sold, inv_cost) VALUES (15, 'SL-MUG-015', 'Central Depot', 150, 10, 140, 30, 60, '2025-03-05', '2025-03-26', 5.50);

-- =============================================
-- sl_suppliers (5 rows)
-- =============================================
CREATE TABLE sl_suppliers (
    sid INTEGER PRIMARY KEY,
    sup_name TEXT NOT NULL,
    sup_contact TEXT,
    sup_email TEXT,
    sup_phone TEXT,
    sup_addr TEXT,
    sup_city TEXT,
    sup_country TEXT,
    sup_terms TEXT,
    sup_lead_days INTEGER,
    sup_rating REAL,
    sup_is_active INTEGER DEFAULT 1
);

INSERT INTO sl_suppliers (sid, sup_name, sup_contact, sup_email, sup_phone, sup_addr, sup_city, sup_country, sup_terms, sup_lead_days, sup_rating, sup_is_active) VALUES (1, 'GlobalTech Supply', 'James Wong', 'james@globaltech.example.com', '555-8001', '88 Tech Park Rd', 'Shenzhen', 'CN', 'Net 30', 14, 4.5, 1);
INSERT INTO sl_suppliers (sid, sup_name, sup_contact, sup_email, sup_phone, sup_addr, sup_city, sup_country, sup_terms, sup_lead_days, sup_rating, sup_is_active) VALUES (2, 'FabricWorld Inc', 'Maria Lopez', 'maria@fabricworld.example.com', '555-8002', '45 Textile Ave', 'Dhaka', 'BD', 'Net 45', 21, 4.2, 1);
INSERT INTO sl_suppliers (sid, sup_name, sup_contact, sup_email, sup_phone, sup_addr, sup_city, sup_country, sup_terms, sup_lead_days, sup_rating, sup_is_active) VALUES (3, 'HomeGoods Direct', 'Tom Fischer', 'tom@homegoods.example.com', '555-8003', '12 Factory Ln', 'Stuttgart', 'DE', 'Net 30', 18, 4.7, 1);
INSERT INTO sl_suppliers (sid, sup_name, sup_contact, sup_email, sup_phone, sup_addr, sup_city, sup_country, sup_terms, sup_lead_days, sup_rating, sup_is_active) VALUES (4, 'BookPrint Co', 'Sarah Mills', 'sarah@bookprint.example.com', '555-8004', '200 Press Blvd', 'London', 'UK', 'Net 60', 10, 4.8, 1);
INSERT INTO sl_suppliers (sid, sup_name, sup_contact, sup_email, sup_phone, sup_addr, sup_city, sup_country, sup_terms, sup_lead_days, sup_rating, sup_is_active) VALUES (5, 'AudioParts Ltd', 'Kenji Tanaka', 'kenji@audioparts.example.com', '555-8005', '7 Sound St', 'Osaka', 'JP', 'Net 30', 12, 4.4, 1);

-- =============================================
-- sl_purchase_orders (12 rows)
-- =============================================
CREATE TABLE sl_purchase_orders (
    poid INTEGER PRIMARY KEY,
    po_sup_name TEXT NOT NULL,
    po_prod_sku TEXT NOT NULL,
    po_qty INTEGER NOT NULL,
    po_unit_cost REAL,
    po_total REAL,
    po_status TEXT DEFAULT 'pending',
    po_ordered TEXT,
    po_expected TEXT,
    po_received TEXT,
    po_wh_name TEXT,
    po_notes TEXT
);

INSERT INTO sl_purchase_orders (poid, po_sup_name, po_prod_sku, po_qty, po_unit_cost, po_total, po_status, po_ordered, po_expected, po_received, po_wh_name, po_notes) VALUES (1, 'GlobalTech Supply', 'SL-LAPTOP-001', 20, 850.00, 17000.00, 'received', '2024-12-01', '2024-12-15', '2024-12-14', 'East Hub', 'Q1 restock');
INSERT INTO sl_purchase_orders (poid, po_sup_name, po_prod_sku, po_qty, po_unit_cost, po_total, po_status, po_ordered, po_expected, po_received, po_wh_name, po_notes) VALUES (2, 'GlobalTech Supply', 'SL-PHONE-002', 30, 520.00, 15600.00, 'received', '2024-12-05', '2024-12-19', '2024-12-20', 'East Hub', 'Holiday restock');
INSERT INTO sl_purchase_orders (poid, po_sup_name, po_prod_sku, po_qty, po_unit_cost, po_total, po_status, po_ordered, po_expected, po_received, po_wh_name, po_notes) VALUES (3, 'FabricWorld Inc', 'SL-TSHIRT-005', 100, 8.50, 850.00, 'received', '2025-01-10', '2025-01-31', '2025-02-02', 'Central Depot', 'Spring collection');
INSERT INTO sl_purchase_orders (poid, po_sup_name, po_prod_sku, po_qty, po_unit_cost, po_total, po_status, po_ordered, po_expected, po_received, po_wh_name, po_notes) VALUES (4, 'FabricWorld Inc', 'SL-JEANS-006', 50, 25.00, 1250.00, 'received', '2025-01-10', '2025-01-31', '2025-02-01', 'East Hub', NULL);
INSERT INTO sl_purchase_orders (poid, po_sup_name, po_prod_sku, po_qty, po_unit_cost, po_total, po_status, po_ordered, po_expected, po_received, po_wh_name, po_notes) VALUES (5, 'AudioParts Ltd', 'SL-HEADPH-004', 40, 85.00, 3400.00, 'received', '2025-01-15', '2025-01-27', '2025-01-28', 'West Hub', NULL);
INSERT INTO sl_purchase_orders (poid, po_sup_name, po_prod_sku, po_qty, po_unit_cost, po_total, po_status, po_ordered, po_expected, po_received, po_wh_name, po_notes) VALUES (6, 'HomeGoods Direct', 'SL-BLNDR-009', 15, 35.00, 525.00, 'received', '2024-12-20', '2025-01-07', '2025-01-08', 'Central Depot', NULL);
INSERT INTO sl_purchase_orders (poid, po_sup_name, po_prod_sku, po_qty, po_unit_cost, po_total, po_status, po_ordered, po_expected, po_received, po_wh_name, po_notes) VALUES (7, 'HomeGoods Direct', 'SL-COFFM-010', 15, 30.00, 450.00, 'received', '2025-01-20', '2025-02-07', '2025-02-05', 'East Hub', 'Fast delivery');
INSERT INTO sl_purchase_orders (poid, po_sup_name, po_prod_sku, po_qty, po_unit_cost, po_total, po_status, po_ordered, po_expected, po_received, po_wh_name, po_notes) VALUES (8, 'BookPrint Co', 'SL-BOOK-013', 30, 12.00, 360.00, 'received', '2024-12-15', '2024-12-25', '2024-12-24', 'East Hub', NULL);
INSERT INTO sl_purchase_orders (poid, po_sup_name, po_prod_sku, po_qty, po_unit_cost, po_total, po_status, po_ordered, po_expected, po_received, po_wh_name, po_notes) VALUES (9, 'GlobalTech Supply', 'SL-CHARGER-014', 50, 15.00, 750.00, 'shipped', '2025-03-01', '2025-03-15', NULL, 'South Center', 'In transit');
INSERT INTO sl_purchase_orders (poid, po_sup_name, po_prod_sku, po_qty, po_unit_cost, po_total, po_status, po_ordered, po_expected, po_received, po_wh_name, po_notes) VALUES (10, 'HomeGoods Direct', 'SL-MUG-015', 60, 5.50, 330.00, 'shipped', '2025-03-05', '2025-03-23', NULL, 'Central Depot', NULL);
INSERT INTO sl_purchase_orders (poid, po_sup_name, po_prod_sku, po_qty, po_unit_cost, po_total, po_status, po_ordered, po_expected, po_received, po_wh_name, po_notes) VALUES (11, 'FabricWorld Inc', 'SL-SNEAK-007', 25, 42.00, 1050.00, 'pending', '2025-03-15', '2025-04-05', NULL, 'South Center', 'New color options');
INSERT INTO sl_purchase_orders (poid, po_sup_name, po_prod_sku, po_qty, po_unit_cost, po_total, po_status, po_ordered, po_expected, po_received, po_wh_name, po_notes) VALUES (12, 'GlobalTech Supply', 'SL-WATCH-011', 20, 110.00, 2200.00, 'pending', '2025-03-18', '2025-04-01', NULL, 'West Hub', 'Q2 forecast');

-- =============================================
-- sl_stock_movements (18 rows)
-- =============================================
CREATE TABLE sl_stock_movements (
    smid INTEGER PRIMARY KEY,
    sm_prod_sku TEXT NOT NULL,
    sm_wh_name TEXT NOT NULL,
    sm_type TEXT NOT NULL,
    sm_qty INTEGER NOT NULL,
    sm_ref_id TEXT,
    sm_notes TEXT,
    sm_by_email TEXT,
    sm_created TEXT,
    sm_cost REAL
);

INSERT INTO sl_stock_movements (smid, sm_prod_sku, sm_wh_name, sm_type, sm_qty, sm_ref_id, sm_notes, sm_by_email, sm_created, sm_cost) VALUES (1, 'SL-LAPTOP-001', 'East Hub', 'inbound', 20, 'PO-1', 'Received from GlobalTech', 'mgr.east@shoplocal.com', '2024-12-14', 17000.00);
INSERT INTO sl_stock_movements (smid, sm_prod_sku, sm_wh_name, sm_type, sm_qty, sm_ref_id, sm_notes, sm_by_email, sm_created, sm_cost) VALUES (2, 'SL-PHONE-002', 'East Hub', 'inbound', 30, 'PO-2', 'Received from GlobalTech', 'mgr.east@shoplocal.com', '2024-12-20', 15600.00);
INSERT INTO sl_stock_movements (smid, sm_prod_sku, sm_wh_name, sm_type, sm_qty, sm_ref_id, sm_notes, sm_by_email, sm_created, sm_cost) VALUES (3, 'SL-LAPTOP-001', 'East Hub', 'outbound', -1, 'ORD-1001', 'Shipped to customer', 'mgr.east@shoplocal.com', '2024-09-16', 850.00);
INSERT INTO sl_stock_movements (smid, sm_prod_sku, sm_wh_name, sm_type, sm_qty, sm_ref_id, sm_notes, sm_by_email, sm_created, sm_cost) VALUES (4, 'SL-PHONE-002', 'East Hub', 'outbound', -1, 'ORD-1002', 'Shipped to customer', 'mgr.east@shoplocal.com', '2024-09-21', 520.00);
INSERT INTO sl_stock_movements (smid, sm_prod_sku, sm_wh_name, sm_type, sm_qty, sm_ref_id, sm_notes, sm_by_email, sm_created, sm_cost) VALUES (5, 'SL-TSHIRT-005', 'Central Depot', 'inbound', 100, 'PO-3', 'Received from FabricWorld', 'mgr.central@shoplocal.com', '2025-02-02', 850.00);
INSERT INTO sl_stock_movements (smid, sm_prod_sku, sm_wh_name, sm_type, sm_qty, sm_ref_id, sm_notes, sm_by_email, sm_created, sm_cost) VALUES (6, 'SL-TSHIRT-005', 'Central Depot', 'outbound', -2, 'ORD-1004', 'Shipped to customer', 'mgr.central@shoplocal.com', '2024-10-11', 17.00);
INSERT INTO sl_stock_movements (smid, sm_prod_sku, sm_wh_name, sm_type, sm_qty, sm_ref_id, sm_notes, sm_by_email, sm_created, sm_cost) VALUES (7, 'SL-HEADPH-004', 'West Hub', 'inbound', 40, 'PO-5', 'Received from AudioParts', 'mgr.west@shoplocal.com', '2025-01-28', 3400.00);
INSERT INTO sl_stock_movements (smid, sm_prod_sku, sm_wh_name, sm_type, sm_qty, sm_ref_id, sm_notes, sm_by_email, sm_created, sm_cost) VALUES (8, 'SL-HEADPH-004', 'West Hub', 'outbound', -1, 'ORD-1003', 'Shipped to customer', 'mgr.west@shoplocal.com', '2024-10-02', 85.00);
INSERT INTO sl_stock_movements (smid, sm_prod_sku, sm_wh_name, sm_type, sm_qty, sm_ref_id, sm_notes, sm_by_email, sm_created, sm_cost) VALUES (9, 'SL-JEANS-006', 'East Hub', 'inbound', 50, 'PO-4', 'Received from FabricWorld', 'mgr.east@shoplocal.com', '2025-02-01', 1250.00);
INSERT INTO sl_stock_movements (smid, sm_prod_sku, sm_wh_name, sm_type, sm_qty, sm_ref_id, sm_notes, sm_by_email, sm_created, sm_cost) VALUES (10, 'SL-JEANS-006', 'East Hub', 'outbound', -2, 'ORD-1006', 'Shipped to customer', 'mgr.east@shoplocal.com', '2024-11-03', 50.00);
INSERT INTO sl_stock_movements (smid, sm_prod_sku, sm_wh_name, sm_type, sm_qty, sm_ref_id, sm_notes, sm_by_email, sm_created, sm_cost) VALUES (11, 'SL-WATCH-011', 'West Hub', 'outbound', -1, 'ORD-1009', 'Shipped to customer', 'mgr.west@shoplocal.com', '2024-12-06', 110.00);
INSERT INTO sl_stock_movements (smid, sm_prod_sku, sm_wh_name, sm_type, sm_qty, sm_ref_id, sm_notes, sm_by_email, sm_created, sm_cost) VALUES (12, 'SL-LAPTOP-001', 'East Hub', 'transfer', -5, 'TRF-001', 'Transfer to West Hub', 'mgr.east@shoplocal.com', '2025-01-10', 4250.00);
INSERT INTO sl_stock_movements (smid, sm_prod_sku, sm_wh_name, sm_type, sm_qty, sm_ref_id, sm_notes, sm_by_email, sm_created, sm_cost) VALUES (13, 'SL-LAPTOP-001', 'West Hub', 'transfer', 5, 'TRF-001', 'Transfer from East Hub', 'mgr.west@shoplocal.com', '2025-01-10', 4250.00);
INSERT INTO sl_stock_movements (smid, sm_prod_sku, sm_wh_name, sm_type, sm_qty, sm_ref_id, sm_notes, sm_by_email, sm_created, sm_cost) VALUES (14, 'SL-BLNDR-009', 'Central Depot', 'inbound', 15, 'PO-6', 'Received from HomeGoods', 'mgr.central@shoplocal.com', '2025-01-08', 525.00);
INSERT INTO sl_stock_movements (smid, sm_prod_sku, sm_wh_name, sm_type, sm_qty, sm_ref_id, sm_notes, sm_by_email, sm_created, sm_cost) VALUES (15, 'SL-BOOK-013', 'East Hub', 'inbound', 30, 'PO-8', 'Received from BookPrint', 'mgr.east@shoplocal.com', '2024-12-24', 360.00);
INSERT INTO sl_stock_movements (smid, sm_prod_sku, sm_wh_name, sm_type, sm_qty, sm_ref_id, sm_notes, sm_by_email, sm_created, sm_cost) VALUES (16, 'SL-MUG-015', 'Central Depot', 'outbound', -3, 'ORD-1004', 'Shipped to customer', 'mgr.central@shoplocal.com', '2024-10-11', 16.50);
INSERT INTO sl_stock_movements (smid, sm_prod_sku, sm_wh_name, sm_type, sm_qty, sm_ref_id, sm_notes, sm_by_email, sm_created, sm_cost) VALUES (17, 'SL-COFFM-010', 'East Hub', 'inbound', 15, 'PO-7', 'Received from HomeGoods', 'mgr.east@shoplocal.com', '2025-02-05', 450.00);
INSERT INTO sl_stock_movements (smid, sm_prod_sku, sm_wh_name, sm_type, sm_qty, sm_ref_id, sm_notes, sm_by_email, sm_created, sm_cost) VALUES (18, 'SL-CHARGER-014', 'South Center', 'outbound', -1, 'ORD-1008', 'Shipped to customer', 'mgr.south@shoplocal.com', '2024-11-29', 15.00);

-- =============================================
-- sl_shipments (18 rows)
-- =============================================
CREATE TABLE sl_shipments (
    shid INTEGER PRIMARY KEY,
    sh_order_id INTEGER NOT NULL,
    sh_carrier_name TEXT,
    sh_tracking TEXT,
    sh_status TEXT DEFAULT 'preparing',
    sh_shipped TEXT,
    sh_est_delivery TEXT,
    sh_actual_delivery TEXT,
    sh_weight REAL,
    sh_cost REAL,
    sh_signature INTEGER DEFAULT 0
);

INSERT INTO sl_shipments (shid, sh_order_id, sh_carrier_name, sh_tracking, sh_status, sh_shipped, sh_est_delivery, sh_actual_delivery, sh_weight, sh_cost, sh_signature) VALUES (1, 1001, 'FastShip Express', 'FS-100001-US', 'delivered', '2024-09-16', '2024-09-19', '2024-09-18', 2.3, 0.00, 1);
INSERT INTO sl_shipments (shid, sh_order_id, sh_carrier_name, sh_tracking, sh_status, sh_shipped, sh_est_delivery, sh_actual_delivery, sh_weight, sh_cost, sh_signature) VALUES (2, 1002, 'FastShip Express', 'FS-100002-US', 'delivered', '2024-09-21', '2024-09-24', '2024-09-24', 0.39, 9.99, 0);
INSERT INTO sl_shipments (shid, sh_order_id, sh_carrier_name, sh_tracking, sh_status, sh_shipped, sh_est_delivery, sh_actual_delivery, sh_weight, sh_cost, sh_signature) VALUES (3, 1003, 'EcoShip Ground', 'ES-200001-US', 'delivered', '2024-10-02', '2024-10-07', '2024-10-06', 1.02, 5.99, 0);
INSERT INTO sl_shipments (shid, sh_order_id, sh_carrier_name, sh_tracking, sh_status, sh_shipped, sh_est_delivery, sh_actual_delivery, sh_weight, sh_cost, sh_signature) VALUES (4, 1004, 'EcoShip Ground', 'ES-200002-US', 'delivered', '2024-10-11', '2024-10-16', '2024-10-15', 0.75, 5.99, 0);
INSERT INTO sl_shipments (shid, sh_order_id, sh_carrier_name, sh_tracking, sh_status, sh_shipped, sh_est_delivery, sh_actual_delivery, sh_weight, sh_cost, sh_signature) VALUES (5, 1005, 'FastShip Express', 'FS-100003-US', 'delivered', '2024-10-19', '2024-10-22', '2024-10-21', 0.48, 0.00, 0);
INSERT INTO sl_shipments (shid, sh_order_id, sh_carrier_name, sh_tracking, sh_status, sh_shipped, sh_est_delivery, sh_actual_delivery, sh_weight, sh_cost, sh_signature) VALUES (6, 1006, 'FastShip Express', 'FS-100004-US', 'delivered', '2024-11-03', '2024-11-06', '2024-11-05', 1.3, 0.00, 0);
INSERT INTO sl_shipments (shid, sh_order_id, sh_carrier_name, sh_tracking, sh_status, sh_shipped, sh_est_delivery, sh_actual_delivery, sh_weight, sh_cost, sh_signature) VALUES (7, 1007, 'PrimeLogistics', 'PL-300001-US', 'delivered', '2024-11-16', '2024-11-18', '2024-11-18', 1.09, 0.00, 1);
INSERT INTO sl_shipments (shid, sh_order_id, sh_carrier_name, sh_tracking, sh_status, sh_shipped, sh_est_delivery, sh_actual_delivery, sh_weight, sh_cost, sh_signature) VALUES (8, 1008, 'EcoShip Ground', 'ES-200003-US', 'delivered', '2024-11-29', '2024-12-04', '2024-12-03', 0.82, 5.99, 0);
INSERT INTO sl_shipments (shid, sh_order_id, sh_carrier_name, sh_tracking, sh_status, sh_shipped, sh_est_delivery, sh_actual_delivery, sh_weight, sh_cost, sh_signature) VALUES (9, 1009, 'FastShip Express', 'FS-100005-US', 'delivered', '2024-12-06', '2024-12-09', '2024-12-08', 0.6, 0.00, 0);
INSERT INTO sl_shipments (shid, sh_order_id, sh_carrier_name, sh_tracking, sh_status, sh_shipped, sh_est_delivery, sh_actual_delivery, sh_weight, sh_cost, sh_signature) VALUES (10, 1010, 'EcoShip Ground', 'ES-200004-US', 'delivered', '2024-12-13', '2024-12-18', '2024-12-17', 0.55, 5.99, 0);
INSERT INTO sl_shipments (shid, sh_order_id, sh_carrier_name, sh_tracking, sh_status, sh_shipped, sh_est_delivery, sh_actual_delivery, sh_weight, sh_cost, sh_signature) VALUES (11, 1011, 'PrimeLogistics', 'PL-300002-US', 'delivered', '2024-12-21', '2024-12-23', '2024-12-23', 0.49, 0.00, 1);
INSERT INTO sl_shipments (shid, sh_order_id, sh_carrier_name, sh_tracking, sh_status, sh_shipped, sh_est_delivery, sh_actual_delivery, sh_weight, sh_cost, sh_signature) VALUES (12, 1012, 'FastShip Express', 'FS-100006-US', 'delivered', '2025-01-06', '2025-01-09', '2025-01-08', 3.25, 0.00, 0);
INSERT INTO sl_shipments (shid, sh_order_id, sh_carrier_name, sh_tracking, sh_status, sh_shipped, sh_est_delivery, sh_actual_delivery, sh_weight, sh_cost, sh_signature) VALUES (13, 1013, 'EcoShip Ground', 'ES-200005-US', 'delivered', '2025-01-16', '2025-01-21', '2025-01-20', 0.7, 5.99, 0);
INSERT INTO sl_shipments (shid, sh_order_id, sh_carrier_name, sh_tracking, sh_status, sh_shipped, sh_est_delivery, sh_actual_delivery, sh_weight, sh_cost, sh_signature) VALUES (14, 1014, 'FastShip Express', 'FS-100007-US', 'in_transit', '2025-01-29', '2025-02-01', NULL, 0.47, 5.99, 0);
INSERT INTO sl_shipments (shid, sh_order_id, sh_carrier_name, sh_tracking, sh_status, sh_shipped, sh_est_delivery, sh_actual_delivery, sh_weight, sh_cost, sh_signature) VALUES (15, 1015, 'EcoShip Ground', 'ES-200006-US', 'in_transit', '2025-02-11', '2025-02-16', NULL, 0.65, 5.99, 0);
INSERT INTO sl_shipments (shid, sh_order_id, sh_carrier_name, sh_tracking, sh_status, sh_shipped, sh_est_delivery, sh_actual_delivery, sh_weight, sh_cost, sh_signature) VALUES (16, 1016, 'PrimeLogistics', 'PL-300003-US', 'preparing', NULL, NULL, NULL, 2.22, 0.00, 1);
INSERT INTO sl_shipments (shid, sh_order_id, sh_carrier_name, sh_tracking, sh_status, sh_shipped, sh_est_delivery, sh_actual_delivery, sh_weight, sh_cost, sh_signature) VALUES (17, 1017, 'EcoShip Ground', 'ES-200007-US', 'preparing', NULL, NULL, NULL, 0.9, 5.99, 0);
INSERT INTO sl_shipments (shid, sh_order_id, sh_carrier_name, sh_tracking, sh_status, sh_shipped, sh_est_delivery, sh_actual_delivery, sh_weight, sh_cost, sh_signature) VALUES (18, 1018, 'EcoShip Ground', 'ES-200008-US', 'preparing', NULL, NULL, NULL, 2.8, 5.99, 0);

-- =============================================
-- sl_carriers (4 rows)
-- =============================================
CREATE TABLE sl_carriers (
    crid INTEGER PRIMARY KEY,
    cr_name TEXT NOT NULL,
    cr_code TEXT NOT NULL,
    cr_website TEXT,
    cr_phone TEXT,
    cr_tracking_url TEXT,
    cr_is_active INTEGER DEFAULT 1,
    cr_avg_days INTEGER,
    cr_rating REAL,
    cr_contact_email TEXT
);

INSERT INTO sl_carriers (crid, cr_name, cr_code, cr_website, cr_phone, cr_tracking_url, cr_is_active, cr_avg_days, cr_rating, cr_contact_email) VALUES (1, 'FastShip Express', 'FSE', 'https://fastship.example.com', '555-7001', 'https://fastship.example.com/track/{tracking}', 1, 3, 4.6, 'support@fastship.example.com');
INSERT INTO sl_carriers (crid, cr_name, cr_code, cr_website, cr_phone, cr_tracking_url, cr_is_active, cr_avg_days, cr_rating, cr_contact_email) VALUES (2, 'EcoShip Ground', 'ESG', 'https://ecoship.example.com', '555-7002', 'https://ecoship.example.com/track/{tracking}', 1, 5, 4.2, 'help@ecoship.example.com');
INSERT INTO sl_carriers (crid, cr_name, cr_code, cr_website, cr_phone, cr_tracking_url, cr_is_active, cr_avg_days, cr_rating, cr_contact_email) VALUES (3, 'PrimeLogistics', 'PLG', 'https://primelogistics.example.com', '555-7003', 'https://primelogistics.example.com/track/{tracking}', 1, 2, 4.8, 'biz@primelogistics.example.com');
INSERT INTO sl_carriers (crid, cr_name, cr_code, cr_website, cr_phone, cr_tracking_url, cr_is_active, cr_avg_days, cr_rating, cr_contact_email) VALUES (4, 'BudgetFreight', 'BGF', 'https://budgetfreight.example.com', '555-7004', 'https://budgetfreight.example.com/track/{tracking}', 0, 7, 3.5, 'cs@budgetfreight.example.com');

-- =============================================
-- sl_shipping_zones (8 rows)
-- =============================================
CREATE TABLE sl_shipping_zones (
    szid INTEGER PRIMARY KEY,
    sz_name TEXT NOT NULL,
    sz_states TEXT,
    sz_base_rate REAL,
    sz_per_kg REAL,
    sz_min_days INTEGER,
    sz_max_days INTEGER,
    sz_is_active INTEGER DEFAULT 1,
    sz_carrier_name TEXT,
    sz_free_threshold REAL
);

INSERT INTO sl_shipping_zones (szid, sz_name, sz_states, sz_base_rate, sz_per_kg, sz_min_days, sz_max_days, sz_is_active, sz_carrier_name, sz_free_threshold) VALUES (1, 'Northeast', 'NY,NJ,PA,MA,CT,RI,VT,NH,ME', 5.99, 1.50, 2, 4, 1, 'FastShip Express', 75.00);
INSERT INTO sl_shipping_zones (szid, sz_name, sz_states, sz_base_rate, sz_per_kg, sz_min_days, sz_max_days, sz_is_active, sz_carrier_name, sz_free_threshold) VALUES (2, 'Southeast', 'FL,GA,SC,NC,VA,TN,AL,MS,LA,AR', 5.99, 1.75, 3, 5, 1, 'EcoShip Ground', 75.00);
INSERT INTO sl_shipping_zones (szid, sz_name, sz_states, sz_base_rate, sz_per_kg, sz_min_days, sz_max_days, sz_is_active, sz_carrier_name, sz_free_threshold) VALUES (3, 'Midwest', 'IL,OH,MI,IN,WI,MN,IA,MO,KS,NE,SD,ND', 6.99, 1.75, 3, 5, 1, 'EcoShip Ground', 100.00);
INSERT INTO sl_shipping_zones (szid, sz_name, sz_states, sz_base_rate, sz_per_kg, sz_min_days, sz_max_days, sz_is_active, sz_carrier_name, sz_free_threshold) VALUES (4, 'Southwest', 'TX,AZ,NM,OK', 6.99, 2.00, 3, 6, 1, 'FastShip Express', 100.00);
INSERT INTO sl_shipping_zones (szid, sz_name, sz_states, sz_base_rate, sz_per_kg, sz_min_days, sz_max_days, sz_is_active, sz_carrier_name, sz_free_threshold) VALUES (5, 'West Coast', 'CA,OR,WA', 5.99, 1.50, 2, 4, 1, 'PrimeLogistics', 75.00);
INSERT INTO sl_shipping_zones (szid, sz_name, sz_states, sz_base_rate, sz_per_kg, sz_min_days, sz_max_days, sz_is_active, sz_carrier_name, sz_free_threshold) VALUES (6, 'Mountain', 'CO,UT,NV,ID,MT,WY', 7.99, 2.25, 4, 6, 1, 'EcoShip Ground', 100.00);
INSERT INTO sl_shipping_zones (szid, sz_name, sz_states, sz_base_rate, sz_per_kg, sz_min_days, sz_max_days, sz_is_active, sz_carrier_name, sz_free_threshold) VALUES (7, 'Pacific', 'HI,AK', 12.99, 3.50, 5, 10, 1, 'FastShip Express', 150.00);
INSERT INTO sl_shipping_zones (szid, sz_name, sz_states, sz_base_rate, sz_per_kg, sz_min_days, sz_max_days, sz_is_active, sz_carrier_name, sz_free_threshold) VALUES (8, 'National Express', 'ALL', 9.99, 2.00, 1, 3, 1, 'PrimeLogistics', 200.00);

-- =============================================
-- sl_returns (8 rows)
-- =============================================
CREATE TABLE sl_returns (
    rtid INTEGER PRIMARY KEY,
    rt_order_id INTEGER NOT NULL,
    rt_cust_email TEXT NOT NULL,
    rt_reason TEXT,
    rt_status TEXT DEFAULT 'requested',
    rt_requested TEXT,
    rt_approved TEXT,
    rt_refund_amount REAL,
    rt_method TEXT,
    rt_handler_email TEXT,
    rt_notes TEXT
);

INSERT INTO sl_returns (rtid, rt_order_id, rt_cust_email, rt_reason, rt_status, rt_requested, rt_approved, rt_refund_amount, rt_method, rt_handler_email, rt_notes) VALUES (1, 1003, 'carol@email.com', 'Defective product', 'completed', '2024-10-12', '2024-10-14', 39.98, 'store_credit', 'agent_sarah@shoplocal.com', 'Two mugs arrived cracked');
INSERT INTO sl_returns (rtid, rt_order_id, rt_cust_email, rt_reason, rt_status, rt_requested, rt_approved, rt_refund_amount, rt_method, rt_handler_email, rt_notes) VALUES (2, 1004, 'dave@email.com', 'Wrong item received', 'completed', '2024-10-18', '2024-10-19', 19.99, 'refund', 'agent_mike@shoplocal.com', 'Received charcoal instead of teal mug');
INSERT INTO sl_returns (rtid, rt_order_id, rt_cust_email, rt_reason, rt_status, rt_requested, rt_approved, rt_refund_amount, rt_method, rt_handler_email, rt_notes) VALUES (3, 1006, 'frank@email.com', 'Size too small', 'completed', '2024-11-10', '2024-11-12', 29.99, 'refund', 'agent_sarah@shoplocal.com', 'T-shirt size S too tight');
INSERT INTO sl_returns (rtid, rt_order_id, rt_cust_email, rt_reason, rt_status, rt_requested, rt_approved, rt_refund_amount, rt_method, rt_handler_email, rt_notes) VALUES (4, 1008, 'henry@email.com', 'Item not as described', 'approved', '2024-12-08', '2024-12-10', 49.99, 'refund', 'agent_jenny@shoplocal.com', 'USB-C hub missing 2 of 7 ports');
INSERT INTO sl_returns (rtid, rt_order_id, rt_cust_email, rt_reason, rt_status, rt_requested, rt_approved, rt_refund_amount, rt_method, rt_handler_email, rt_notes) VALUES (5, 1013, 'leo@email.com', 'Does not fit', 'requested', '2025-01-28', NULL, 119.99, 'refund', NULL, 'Sneakers too narrow');
INSERT INTO sl_returns (rtid, rt_order_id, rt_cust_email, rt_reason, rt_status, rt_requested, rt_approved, rt_refund_amount, rt_method, rt_handler_email, rt_notes) VALUES (6, 1009, 'ivy@email.com', 'Changed mind', 'denied', '2024-12-20', '2024-12-22', 0.00, NULL, 'agent_mike@shoplocal.com', 'Past return window');
INSERT INTO sl_returns (rtid, rt_order_id, rt_cust_email, rt_reason, rt_status, rt_requested, rt_approved, rt_refund_amount, rt_method, rt_handler_email, rt_notes) VALUES (7, 1011, 'kate@email.com', 'Better price found', 'requested', '2025-01-05', NULL, 49.99, 'refund', NULL, 'Wants to return USB-C hub');
INSERT INTO sl_returns (rtid, rt_order_id, rt_cust_email, rt_reason, rt_status, rt_requested, rt_approved, rt_refund_amount, rt_method, rt_handler_email, rt_notes) VALUES (8, 1020, 'dave@email.com', 'Order cancelled', 'completed', '2025-03-22', '2025-03-22', 962.99, 'refund', 'agent_sarah@shoplocal.com', 'Full order cancellation');

-- =============================================
-- sl_coupons (6 rows)
-- =============================================
CREATE TABLE sl_coupons (
    cpid INTEGER PRIMARY KEY,
    cp_code TEXT NOT NULL,
    cp_desc TEXT,
    cp_type TEXT,
    cp_value REAL,
    cp_min_order REAL DEFAULT 0,
    cp_max_uses INTEGER,
    cp_used INTEGER DEFAULT 0,
    cp_valid_from TEXT,
    cp_valid_to TEXT,
    cp_is_active INTEGER DEFAULT 1,
    cp_created_by TEXT
);

INSERT INTO sl_coupons (cpid, cp_code, cp_desc, cp_type, cp_value, cp_min_order, cp_max_uses, cp_used, cp_valid_from, cp_valid_to, cp_is_active, cp_created_by) VALUES (1, 'WELCOME10', 'Welcome discount for new customers', 'percentage', 10.0, 25.00, 500, 142, '2024-01-01', '2025-12-31', 1, 'admin');
INSERT INTO sl_coupons (cpid, cp_code, cp_desc, cp_type, cp_value, cp_min_order, cp_max_uses, cp_used, cp_valid_from, cp_valid_to, cp_is_active, cp_created_by) VALUES (2, 'FALL10', 'Fall season $10 off', 'fixed', 10.0, 50.00, 200, 88, '2024-09-01', '2024-11-30', 0, 'admin');
INSERT INTO sl_coupons (cpid, cp_code, cp_desc, cp_type, cp_value, cp_min_order, cp_max_uses, cp_used, cp_valid_from, cp_valid_to, cp_is_active, cp_created_by) VALUES (3, 'HOLIDAY25', 'Holiday season 25% off', 'percentage', 25.0, 100.00, 300, 156, '2024-11-25', '2024-12-31', 0, 'admin');
INSERT INTO sl_coupons (cpid, cp_code, cp_desc, cp_type, cp_value, cp_min_order, cp_max_uses, cp_used, cp_valid_from, cp_valid_to, cp_is_active, cp_created_by) VALUES (4, 'SPRING5', 'Spring $5 off any order', 'fixed', 5.0, 20.00, 1000, 23, '2025-03-01', '2025-05-31', 1, 'admin');
INSERT INTO sl_coupons (cpid, cp_code, cp_desc, cp_type, cp_value, cp_min_order, cp_max_uses, cp_used, cp_valid_from, cp_valid_to, cp_is_active, cp_created_by) VALUES (5, 'VIP50', 'VIP customer $50 off', 'fixed', 50.0, 200.00, 50, 12, '2024-01-01', '2025-12-31', 1, 'admin');
INSERT INTO sl_coupons (cpid, cp_code, cp_desc, cp_type, cp_value, cp_min_order, cp_max_uses, cp_used, cp_valid_from, cp_valid_to, cp_is_active, cp_created_by) VALUES (6, 'FREESHIP', 'Free shipping on orders over $75', 'free_shipping', 0.0, 75.00, 999, 210, '2024-06-01', '2025-06-30', 1, 'admin');

-- =============================================
-- sl_coupon_uses (10 rows)
-- =============================================
CREATE TABLE sl_coupon_uses (
    cuid INTEGER PRIMARY KEY,
    cu_code TEXT NOT NULL,
    cu_cust_email TEXT NOT NULL,
    cu_order_id INTEGER NOT NULL,
    cu_discount REAL,
    cu_used_at TEXT,
    cu_ip TEXT,
    cu_ua TEXT,
    cu_session TEXT,
    cu_is_first INTEGER DEFAULT 0
);

INSERT INTO sl_coupon_uses (cuid, cu_code, cu_cust_email, cu_order_id, cu_discount, cu_used_at, cu_ip, cu_ua, cu_session, cu_is_first) VALUES (1, 'FALL10', 'dave@email.com', 1004, 10.00, '2024-10-10 11:40:00', '192.168.1.104', 'Mozilla/5.0 Chrome/120', 'sess_dave_1004', 0);
INSERT INTO sl_coupon_uses (cuid, cu_code, cu_cust_email, cu_order_id, cu_discount, cu_used_at, cu_ip, cu_ua, cu_session, cu_is_first) VALUES (2, 'VIP50', 'grace@email.com', 1007, 50.00, '2024-11-15 10:50:00', '192.168.1.107', 'Mozilla/5.0 Safari/17', 'sess_grace_1007', 0);
INSERT INTO sl_coupon_uses (cuid, cu_code, cu_cust_email, cu_order_id, cu_discount, cu_used_at, cu_ip, cu_ua, cu_session, cu_is_first) VALUES (3, 'HOLIDAY25', 'kate@email.com', 1011, 25.00, '2024-12-20 17:18:00', '192.168.1.111', 'Mozilla/5.0 Chrome/121', 'sess_kate_1011', 1);
INSERT INTO sl_coupon_uses (cuid, cu_code, cu_cust_email, cu_order_id, cu_discount, cu_used_at, cu_ip, cu_ua, cu_session, cu_is_first) VALUES (4, 'SPRING5', 'ivy@email.com', 1019, 5.00, '2025-03-15 14:20:00', '192.168.1.109', 'Mozilla/5.0 Firefox/123', 'sess_ivy_1019', 0);
INSERT INTO sl_coupon_uses (cuid, cu_code, cu_cust_email, cu_order_id, cu_discount, cu_used_at, cu_ip, cu_ua, cu_session, cu_is_first) VALUES (5, 'WELCOME10', 'kate@email.com', 1011, 0.00, '2024-12-20 17:15:00', '192.168.1.111', 'Mozilla/5.0 Chrome/121', 'sess_kate_1011', 1);
INSERT INTO sl_coupon_uses (cuid, cu_code, cu_cust_email, cu_order_id, cu_discount, cu_used_at, cu_ip, cu_ua, cu_session, cu_is_first) VALUES (6, 'FREESHIP', 'alice@email.com', 1001, 0.00, '2024-09-15 10:20:00', '192.168.1.101', 'Mozilla/5.0 Chrome/119', 'sess_alice_1001', 0);
INSERT INTO sl_coupon_uses (cuid, cu_code, cu_cust_email, cu_order_id, cu_discount, cu_used_at, cu_ip, cu_ua, cu_session, cu_is_first) VALUES (7, 'FREESHIP', 'eve@email.com', 1005, 0.00, '2024-10-18 16:25:00', '192.168.1.105', 'Mozilla/5.0 Safari/17', 'sess_eve_1005', 0);
INSERT INTO sl_coupon_uses (cuid, cu_code, cu_cust_email, cu_order_id, cu_discount, cu_used_at, cu_ip, cu_ua, cu_session, cu_is_first) VALUES (8, 'FREESHIP', 'frank@email.com', 1006, 0.00, '2024-11-02 13:15:00', '192.168.1.106', 'Mozilla/5.0 Chrome/120', 'sess_frank_1006', 0);
INSERT INTO sl_coupon_uses (cuid, cu_code, cu_cust_email, cu_order_id, cu_discount, cu_used_at, cu_ip, cu_ua, cu_session, cu_is_first) VALUES (9, 'FREESHIP', 'alice@email.com', 1012, 0.00, '2025-01-05 09:25:00', '192.168.1.101', 'Mozilla/5.0 Chrome/121', 'sess_alice_1012', 0);
INSERT INTO sl_coupon_uses (cuid, cu_code, cu_cust_email, cu_order_id, cu_discount, cu_used_at, cu_ip, cu_ua, cu_session, cu_is_first) VALUES (10, 'WELCOME10', 'leo@email.com', 1013, 0.00, '2025-01-15 14:10:00', '192.168.1.112', 'Mozilla/5.0 Firefox/122', 'sess_leo_1013', 1);

-- =============================================
-- sl_campaigns (5 rows)
-- =============================================
CREATE TABLE sl_campaigns (
    cmpid INTEGER PRIMARY KEY,
    cmp_name TEXT NOT NULL,
    cmp_desc TEXT,
    cmp_type TEXT,
    cmp_start TEXT,
    cmp_end TEXT,
    cmp_budget REAL,
    cmp_spent REAL DEFAULT 0,
    cmp_status TEXT DEFAULT 'draft',
    cmp_target_audience TEXT,
    cmp_created_by TEXT
);

INSERT INTO sl_campaigns (cmpid, cmp_name, cmp_desc, cmp_type, cmp_start, cmp_end, cmp_budget, cmp_spent, cmp_status, cmp_target_audience, cmp_created_by) VALUES (1, 'Fall Sale 2024', 'Annual fall clearance sale', 'seasonal', '2024-09-01', '2024-11-30', 5000.00, 4850.00, 'completed', 'all_customers', 'admin');
INSERT INTO sl_campaigns (cmpid, cmp_name, cmp_desc, cmp_type, cmp_start, cmp_end, cmp_budget, cmp_spent, cmp_status, cmp_target_audience, cmp_created_by) VALUES (2, 'Holiday Blitz 2024', 'Black Friday through New Year promotions', 'holiday', '2024-11-25', '2024-12-31', 10000.00, 9200.00, 'completed', 'all_customers', 'admin');
INSERT INTO sl_campaigns (cmpid, cmp_name, cmp_desc, cmp_type, cmp_start, cmp_end, cmp_budget, cmp_spent, cmp_status, cmp_target_audience, cmp_created_by) VALUES (3, 'New Year Clearance', 'Post-holiday inventory clearance', 'clearance', '2025-01-02', '2025-01-31', 3000.00, 2100.00, 'completed', 'bargain_hunters', 'admin');
INSERT INTO sl_campaigns (cmpid, cmp_name, cmp_desc, cmp_type, cmp_start, cmp_end, cmp_budget, cmp_spent, cmp_status, cmp_target_audience, cmp_created_by) VALUES (4, 'Spring Collection Launch', 'Promote new spring clothing line', 'launch', '2025-03-01', '2025-04-30', 7500.00, 1800.00, 'active', 'fashion_enthusiasts', 'admin');
INSERT INTO sl_campaigns (cmpid, cmp_name, cmp_desc, cmp_type, cmp_start, cmp_end, cmp_budget, cmp_spent, cmp_status, cmp_target_audience, cmp_created_by) VALUES (5, 'Tech Upgrade Month', 'Electronics trade-in and upgrade deals', 'promotional', '2025-04-01', '2025-04-30', 8000.00, 0.00, 'scheduled', 'tech_buyers', 'admin');

-- =============================================
-- sl_wishlists (12 rows)
-- =============================================
CREATE TABLE sl_wishlists (
    wlid INTEGER PRIMARY KEY,
    wl_cust_email TEXT NOT NULL,
    wl_prod_sku TEXT NOT NULL,
    wl_added TEXT,
    wl_priority INTEGER DEFAULT 0,
    wl_notes TEXT,
    wl_is_public INTEGER DEFAULT 0,
    wl_price_at_add REAL,
    wl_notify_sale INTEGER DEFAULT 1,
    wl_source TEXT
);

INSERT INTO sl_wishlists (wlid, wl_cust_email, wl_prod_sku, wl_added, wl_priority, wl_notes, wl_is_public, wl_price_at_add, wl_notify_sale, wl_source) VALUES (1, 'alice@email.com', 'SL-PHONE-002', '2024-11-01', 1, 'Want for birthday', 0, 899.99, 1, 'product_page');
INSERT INTO sl_wishlists (wlid, wl_cust_email, wl_prod_sku, wl_added, wl_priority, wl_notes, wl_is_public, wl_price_at_add, wl_notify_sale, wl_source) VALUES (2, 'bob@email.com', 'SL-LAPTOP-001', '2024-10-15', 2, 'For work upgrade', 1, 1299.99, 1, 'search');
INSERT INTO sl_wishlists (wlid, wl_cust_email, wl_prod_sku, wl_added, wl_priority, wl_notes, wl_is_public, wl_price_at_add, wl_notify_sale, wl_source) VALUES (3, 'carol@email.com', 'SL-WATCH-011', '2024-12-01', 1, 'Holiday gift idea', 1, 249.99, 1, 'recommendation');
INSERT INTO sl_wishlists (wlid, wl_cust_email, wl_prod_sku, wl_added, wl_priority, wl_notes, wl_is_public, wl_price_at_add, wl_notify_sale, wl_source) VALUES (4, 'dave@email.com', 'SL-HEADPH-004', '2025-01-10', 0, NULL, 0, 199.99, 1, 'product_page');
INSERT INTO sl_wishlists (wlid, wl_cust_email, wl_prod_sku, wl_added, wl_priority, wl_notes, wl_is_public, wl_price_at_add, wl_notify_sale, wl_source) VALUES (5, 'eve@email.com', 'SL-JACKET-008', '2025-01-20', 1, 'Need for hiking trip', 0, 149.99, 0, 'category_browse');
INSERT INTO sl_wishlists (wlid, wl_cust_email, wl_prod_sku, wl_added, wl_priority, wl_notes, wl_is_public, wl_price_at_add, wl_notify_sale, wl_source) VALUES (6, 'frank@email.com', 'SL-COFFM-010', '2024-12-15', 0, NULL, 1, 79.99, 1, 'product_page');
INSERT INTO sl_wishlists (wlid, wl_cust_email, wl_prod_sku, wl_added, wl_priority, wl_notes, wl_is_public, wl_price_at_add, wl_notify_sale, wl_source) VALUES (7, 'grace@email.com', 'SL-BOOK-013', '2025-02-01', 0, 'Want to learn SQL', 0, 39.99, 0, 'search');
INSERT INTO sl_wishlists (wlid, wl_cust_email, wl_prod_sku, wl_added, wl_priority, wl_notes, wl_is_public, wl_price_at_add, wl_notify_sale, wl_source) VALUES (8, 'henry@email.com', 'SL-BLNDR-009', '2025-02-10', 1, 'Kitchen upgrade', 1, 89.99, 1, 'recommendation');
INSERT INTO sl_wishlists (wlid, wl_cust_email, wl_prod_sku, wl_added, wl_priority, wl_notes, wl_is_public, wl_price_at_add, wl_notify_sale, wl_source) VALUES (9, 'ivy@email.com', 'SL-BACKP-012', '2025-02-15', 2, 'For travel', 0, 59.99, 1, 'product_page');
INSERT INTO sl_wishlists (wlid, wl_cust_email, wl_prod_sku, wl_added, wl_priority, wl_notes, wl_is_public, wl_price_at_add, wl_notify_sale, wl_source) VALUES (10, 'jack@email.com', 'SL-TABLET-003', '2025-03-01', 1, NULL, 1, 549.99, 1, 'search');
INSERT INTO sl_wishlists (wlid, wl_cust_email, wl_prod_sku, wl_added, wl_priority, wl_notes, wl_is_public, wl_price_at_add, wl_notify_sale, wl_source) VALUES (11, 'kate@email.com', 'SL-SNEAK-007', '2025-03-05', 0, 'Running shoes', 0, 119.99, 1, 'category_browse');
INSERT INTO sl_wishlists (wlid, wl_cust_email, wl_prod_sku, wl_added, wl_priority, wl_notes, wl_is_public, wl_price_at_add, wl_notify_sale, wl_source) VALUES (12, 'leo@email.com', 'SL-CHARGER-014', '2025-03-10', 0, NULL, 0, 49.99, 0, 'product_page');

-- =============================================
-- sl_email_subs (10 rows)
-- =============================================
CREATE TABLE sl_email_subs (
    esid INTEGER PRIMARY KEY,
    es_email TEXT NOT NULL,
    es_cust_email TEXT,
    es_subscribed_at TEXT,
    es_status TEXT DEFAULT 'active',
    es_source TEXT,
    es_preferences TEXT,
    es_last_sent TEXT,
    es_open_rate REAL DEFAULT 0,
    es_bounce_count INTEGER DEFAULT 0
);

INSERT INTO sl_email_subs (esid, es_email, es_cust_email, es_subscribed_at, es_status, es_source, es_preferences, es_last_sent, es_open_rate, es_bounce_count) VALUES (1, 'alice@email.com', 'alice@email.com', '2021-01-10', 'active', 'signup', 'deals,new_arrivals', '2025-03-20', 0.72, 0);
INSERT INTO sl_email_subs (esid, es_email, es_cust_email, es_subscribed_at, es_status, es_source, es_preferences, es_last_sent, es_open_rate, es_bounce_count) VALUES (2, 'bob@email.com', 'bob@email.com', '2021-03-05', 'active', 'signup', 'deals', '2025-03-20', 0.45, 0);
INSERT INTO sl_email_subs (esid, es_email, es_cust_email, es_subscribed_at, es_status, es_source, es_preferences, es_last_sent, es_open_rate, es_bounce_count) VALUES (3, 'carol@email.com', 'carol@email.com', '2021-06-18', 'active', 'signup', 'deals,new_arrivals,blog', '2025-03-20', 0.68, 0);
INSERT INTO sl_email_subs (esid, es_email, es_cust_email, es_subscribed_at, es_status, es_source, es_preferences, es_last_sent, es_open_rate, es_bounce_count) VALUES (4, 'dave@email.com', 'dave@email.com', '2022-01-12', 'unsubscribed', 'signup', 'deals', '2024-08-15', 0.20, 0);
INSERT INTO sl_email_subs (esid, es_email, es_cust_email, es_subscribed_at, es_status, es_source, es_preferences, es_last_sent, es_open_rate, es_bounce_count) VALUES (5, 'eve@email.com', 'eve@email.com', '2022-04-20', 'active', 'checkout', 'deals,new_arrivals', '2025-03-20', 0.55, 0);
INSERT INTO sl_email_subs (esid, es_email, es_cust_email, es_subscribed_at, es_status, es_source, es_preferences, es_last_sent, es_open_rate, es_bounce_count) VALUES (6, 'frank@email.com', 'frank@email.com', '2022-07-01', 'active', 'checkout', 'deals', '2025-03-20', 0.38, 1);
INSERT INTO sl_email_subs (esid, es_email, es_cust_email, es_subscribed_at, es_status, es_source, es_preferences, es_last_sent, es_open_rate, es_bounce_count) VALUES (7, 'grace@email.com', 'grace@email.com', '2022-09-14', 'active', 'signup', 'new_arrivals,blog', '2025-03-20', 0.80, 0);
INSERT INTO sl_email_subs (esid, es_email, es_cust_email, es_subscribed_at, es_status, es_source, es_preferences, es_last_sent, es_open_rate, es_bounce_count) VALUES (8, 'newsletter_fan@gmail.com', NULL, '2024-05-10', 'active', 'footer_form', 'deals,blog', '2025-03-20', 0.60, 0);
INSERT INTO sl_email_subs (esid, es_email, es_cust_email, es_subscribed_at, es_status, es_source, es_preferences, es_last_sent, es_open_rate, es_bounce_count) VALUES (9, 'techdeals@outlook.com', NULL, '2024-08-22', 'active', 'popup', 'deals', '2025-03-20', 0.35, 2);
INSERT INTO sl_email_subs (esid, es_email, es_cust_email, es_subscribed_at, es_status, es_source, es_preferences, es_last_sent, es_open_rate, es_bounce_count) VALUES (10, 'leo@email.com', 'leo@email.com', '2024-04-28', 'active', 'signup', 'deals,new_arrivals', '2025-03-20', 0.50, 0);

-- =============================================
-- sl_tickets (10 rows)
-- =============================================
CREATE TABLE sl_tickets (
    tkid INTEGER PRIMARY KEY,
    tk_cust_email TEXT NOT NULL,
    tk_agent_name TEXT,
    tk_subject TEXT NOT NULL,
    tk_priority TEXT DEFAULT 'normal',
    tk_status TEXT DEFAULT 'open',
    tk_channel TEXT,
    tk_created TEXT,
    tk_updated TEXT,
    tk_resolved TEXT,
    tk_satisfaction INTEGER
);

INSERT INTO sl_tickets (tkid, tk_cust_email, tk_agent_name, tk_subject, tk_priority, tk_status, tk_channel, tk_created, tk_updated, tk_resolved, tk_satisfaction) VALUES (1, 'carol@email.com', 'Sarah Wilson', 'Damaged mugs in order 1003', 'high', 'closed', 'email', '2024-10-12', '2024-10-18', '2024-10-18', 4);
INSERT INTO sl_tickets (tkid, tk_cust_email, tk_agent_name, tk_subject, tk_priority, tk_status, tk_channel, tk_created, tk_updated, tk_resolved, tk_satisfaction) VALUES (2, 'dave@email.com', 'Mike Johnson', 'Wrong mug color in order 1004', 'normal', 'closed', 'chat', '2024-10-18', '2024-10-22', '2024-10-22', 5);
INSERT INTO sl_tickets (tkid, tk_cust_email, tk_agent_name, tk_subject, tk_priority, tk_status, tk_channel, tk_created, tk_updated, tk_resolved, tk_satisfaction) VALUES (3, 'frank@email.com', 'Sarah Wilson', 'T-shirt size issue order 1006', 'normal', 'closed', 'email', '2024-11-10', '2024-11-18', '2024-11-18', 4);
INSERT INTO sl_tickets (tkid, tk_cust_email, tk_agent_name, tk_subject, tk_priority, tk_status, tk_channel, tk_created, tk_updated, tk_resolved, tk_satisfaction) VALUES (4, 'henry@email.com', 'Jenny Lee', 'USB-C hub missing ports', 'high', 'open', 'email', '2024-12-08', '2025-01-05', NULL, NULL);
INSERT INTO sl_tickets (tkid, tk_cust_email, tk_agent_name, tk_subject, tk_priority, tk_status, tk_channel, tk_created, tk_updated, tk_resolved, tk_satisfaction) VALUES (5, 'alice@email.com', 'Mike Johnson', 'Tracking not updating for order 1012', 'low', 'closed', 'chat', '2025-01-07', '2025-01-08', '2025-01-08', 5);
INSERT INTO sl_tickets (tkid, tk_cust_email, tk_agent_name, tk_subject, tk_priority, tk_status, tk_channel, tk_created, tk_updated, tk_resolved, tk_satisfaction) VALUES (6, 'leo@email.com', 'Jenny Lee', 'Sneakers too narrow order 1013', 'normal', 'open', 'email', '2025-01-28', '2025-02-05', NULL, NULL);
INSERT INTO sl_tickets (tkid, tk_cust_email, tk_agent_name, tk_subject, tk_priority, tk_status, tk_channel, tk_created, tk_updated, tk_resolved, tk_satisfaction) VALUES (7, 'eve@email.com', 'Sarah Wilson', 'When will order 1016 ship?', 'low', 'open', 'chat', '2025-03-01', '2025-03-05', NULL, NULL);
INSERT INTO sl_tickets (tkid, tk_cust_email, tk_agent_name, tk_subject, tk_priority, tk_status, tk_channel, tk_created, tk_updated, tk_resolved, tk_satisfaction) VALUES (8, 'bob@email.com', 'Mike Johnson', 'Order 1014 delivery estimate', 'normal', 'open', 'phone', '2025-02-05', '2025-02-10', NULL, NULL);
INSERT INTO sl_tickets (tkid, tk_cust_email, tk_agent_name, tk_subject, tk_priority, tk_status, tk_channel, tk_created, tk_updated, tk_resolved, tk_satisfaction) VALUES (9, 'kate@email.com', 'Jenny Lee', 'Return request for USB-C hub', 'normal', 'open', 'email', '2025-01-05', '2025-01-10', NULL, NULL);
INSERT INTO sl_tickets (tkid, tk_cust_email, tk_agent_name, tk_subject, tk_priority, tk_status, tk_channel, tk_created, tk_updated, tk_resolved, tk_satisfaction) VALUES (10, 'ivy@email.com', 'Mike Johnson', 'Return window question', 'low', 'closed', 'chat', '2024-12-20', '2024-12-22', '2024-12-22', 2);

-- =============================================
-- sl_ticket_msgs (15 rows)
-- =============================================
CREATE TABLE sl_ticket_msgs (
    tmid INTEGER PRIMARY KEY,
    tm_ticket_id INTEGER NOT NULL,
    tm_sender_email TEXT NOT NULL,
    tm_sender_type TEXT NOT NULL,
    tm_body TEXT NOT NULL,
    tm_is_internal INTEGER DEFAULT 0,
    tm_attachments TEXT,
    tm_created TEXT,
    tm_read_at TEXT,
    tm_edited INTEGER DEFAULT 0
);

INSERT INTO sl_ticket_msgs (tmid, tm_ticket_id, tm_sender_email, tm_sender_type, tm_body, tm_is_internal, tm_attachments, tm_created, tm_read_at, tm_edited) VALUES (1, 1, 'carol@email.com', 'customer', 'Hi, I received my order 1003 but both mugs have cracks. Can I get a replacement or refund?', 0, 'crack_photo.jpg', '2024-10-12 09:00:00', '2024-10-12 09:30:00', 0);
INSERT INTO sl_ticket_msgs (tmid, tm_ticket_id, tm_sender_email, tm_sender_type, tm_body, tm_is_internal, tm_attachments, tm_created, tm_read_at, tm_edited) VALUES (2, 1, 'agent_sarah@shoplocal.com', 'agent', 'Sorry about that! We will issue a store credit for the damaged mugs right away.', 0, NULL, '2024-10-12 10:15:00', '2024-10-12 11:00:00', 0);
INSERT INTO sl_ticket_msgs (tmid, tm_ticket_id, tm_sender_email, tm_sender_type, tm_body, tm_is_internal, tm_attachments, tm_created, tm_read_at, tm_edited) VALUES (3, 2, 'dave@email.com', 'customer', 'I ordered a teal mug but received charcoal. Order 1004.', 0, NULL, '2024-10-18 14:00:00', '2024-10-18 14:10:00', 0);
INSERT INTO sl_ticket_msgs (tmid, tm_ticket_id, tm_sender_email, tm_sender_type, tm_body, tm_is_internal, tm_attachments, tm_created, tm_read_at, tm_edited) VALUES (4, 2, 'agent_mike@shoplocal.com', 'agent', 'Apologies for the mix-up. Refund has been processed to your original payment method.', 0, NULL, '2024-10-18 14:30:00', '2024-10-18 15:00:00', 0);
INSERT INTO sl_ticket_msgs (tmid, tm_ticket_id, tm_sender_email, tm_sender_type, tm_body, tm_is_internal, tm_attachments, tm_created, tm_read_at, tm_edited) VALUES (5, 3, 'frank@email.com', 'customer', 'The Classic Cotton Tee size S is way too small. I usually wear S in other brands.', 0, NULL, '2024-11-10 11:00:00', '2024-11-10 13:00:00', 0);
INSERT INTO sl_ticket_msgs (tmid, tm_ticket_id, tm_sender_email, tm_sender_type, tm_body, tm_is_internal, tm_attachments, tm_created, tm_read_at, tm_edited) VALUES (6, 3, 'agent_sarah@shoplocal.com', 'agent', 'We understand. Our sizing runs small. We have initiated a return and refund for you.', 0, NULL, '2024-11-10 14:00:00', '2024-11-10 16:00:00', 0);
INSERT INTO sl_ticket_msgs (tmid, tm_ticket_id, tm_sender_email, tm_sender_type, tm_body, tm_is_internal, tm_attachments, tm_created, tm_read_at, tm_edited) VALUES (7, 4, 'henry@email.com', 'customer', 'The USB-C hub says 7-in-1 but only has 5 ports. Missing the SD card reader and HDMI.', 0, 'hub_photo.jpg', '2024-12-08 10:00:00', '2024-12-08 11:00:00', 0);
INSERT INTO sl_ticket_msgs (tmid, tm_ticket_id, tm_sender_email, tm_sender_type, tm_body, tm_is_internal, tm_attachments, tm_created, tm_read_at, tm_edited) VALUES (8, 4, 'agent_jenny@shoplocal.com', 'agent', 'Thank you for the photos. We are investigating this with our supplier.', 0, NULL, '2024-12-08 14:00:00', '2024-12-09 09:00:00', 0);
INSERT INTO sl_ticket_msgs (tmid, tm_ticket_id, tm_sender_email, tm_sender_type, tm_body, tm_is_internal, tm_attachments, tm_created, tm_read_at, tm_edited) VALUES (9, 4, 'agent_jenny@shoplocal.com', 'agent', 'Internal: flagged batch issue with SL-CHARGER-014 from GlobalTech. Check other orders.', 1, NULL, '2024-12-09 10:00:00', NULL, 0);
INSERT INTO sl_ticket_msgs (tmid, tm_ticket_id, tm_sender_email, tm_sender_type, tm_body, tm_is_internal, tm_attachments, tm_created, tm_read_at, tm_edited) VALUES (10, 5, 'alice@email.com', 'customer', 'My tracking number FS-100006-US has not updated in 2 days. Is everything OK?', 0, NULL, '2025-01-07 16:00:00', '2025-01-07 16:30:00', 0);
INSERT INTO sl_ticket_msgs (tmid, tm_ticket_id, tm_sender_email, tm_sender_type, tm_body, tm_is_internal, tm_attachments, tm_created, tm_read_at, tm_edited) VALUES (11, 5, 'agent_mike@shoplocal.com', 'agent', 'The carrier had a scanning delay. Your package is on its way and should arrive tomorrow.', 0, NULL, '2025-01-07 17:00:00', '2025-01-07 18:00:00', 0);
INSERT INTO sl_ticket_msgs (tmid, tm_ticket_id, tm_sender_email, tm_sender_type, tm_body, tm_is_internal, tm_attachments, tm_created, tm_read_at, tm_edited) VALUES (12, 6, 'leo@email.com', 'customer', 'The RunFlex sneakers in US10 are too narrow for me. Can I return them?', 0, NULL, '2025-01-28 10:00:00', '2025-01-28 11:00:00', 0);
INSERT INTO sl_ticket_msgs (tmid, tm_ticket_id, tm_sender_email, tm_sender_type, tm_body, tm_is_internal, tm_attachments, tm_created, tm_read_at, tm_edited) VALUES (13, 6, 'agent_jenny@shoplocal.com', 'agent', 'You are within the return window. I have started a return for you. Please ship back within 14 days.', 0, NULL, '2025-01-28 13:00:00', '2025-01-29 09:00:00', 0);
INSERT INTO sl_ticket_msgs (tmid, tm_ticket_id, tm_sender_email, tm_sender_type, tm_body, tm_is_internal, tm_attachments, tm_created, tm_read_at, tm_edited) VALUES (14, 7, 'eve@email.com', 'customer', 'I placed order 1016 on Feb 20. It still says processing. When will it ship?', 0, NULL, '2025-03-01 12:00:00', '2025-03-01 14:00:00', 0);
INSERT INTO sl_ticket_msgs (tmid, tm_ticket_id, tm_sender_email, tm_sender_type, tm_body, tm_is_internal, tm_attachments, tm_created, tm_read_at, tm_edited) VALUES (15, 10, 'ivy@email.com', 'customer', 'How long is the return window? I might want to return an item from order 1009.', 0, NULL, '2024-12-20 15:00:00', '2024-12-20 15:30:00', 0);

-- =============================================
-- sl_agents (4 rows)
-- =============================================
CREATE TABLE sl_agents (
    agid INTEGER PRIMARY KEY,
    ag_name TEXT NOT NULL,
    ag_email TEXT NOT NULL,
    ag_phone TEXT,
    ag_dept TEXT,
    ag_role TEXT,
    ag_is_active INTEGER DEFAULT 1,
    ag_hired TEXT,
    ag_skills TEXT,
    ag_avg_rating REAL
);

INSERT INTO sl_agents (agid, ag_name, ag_email, ag_phone, ag_dept, ag_role, ag_is_active, ag_hired, ag_skills, ag_avg_rating) VALUES (1, 'Sarah Wilson', 'agent_sarah@shoplocal.com', '555-6001', 'support', 'senior_agent', 1, '2020-03-15', 'returns,billing,escalations', 4.7);
INSERT INTO sl_agents (agid, ag_name, ag_email, ag_phone, ag_dept, ag_role, ag_is_active, ag_hired, ag_skills, ag_avg_rating) VALUES (2, 'Mike Johnson', 'agent_mike@shoplocal.com', '555-6002', 'support', 'agent', 1, '2021-08-01', 'shipping,tracking,general', 4.5);
INSERT INTO sl_agents (agid, ag_name, ag_email, ag_phone, ag_dept, ag_role, ag_is_active, ag_hired, ag_skills, ag_avg_rating) VALUES (3, 'Jenny Lee', 'agent_jenny@shoplocal.com', '555-6003', 'support', 'agent', 1, '2022-05-20', 'products,returns,technical', 4.3);
INSERT INTO sl_agents (agid, ag_name, ag_email, ag_phone, ag_dept, ag_role, ag_is_active, ag_hired, ag_skills, ag_avg_rating) VALUES (4, 'Tom Bradley', 'agent_tom@shoplocal.com', '555-6004', 'support', 'team_lead', 1, '2019-01-10', 'all,management,training', 4.8);

-- =============================================
-- sl_pages (5 rows)
-- =============================================
CREATE TABLE sl_pages (
    pgid INTEGER PRIMARY KEY,
    pg_title TEXT NOT NULL,
    pg_slug TEXT NOT NULL,
    pg_body TEXT,
    pg_status TEXT DEFAULT 'draft',
    pg_author_email TEXT,
    pg_meta_title TEXT,
    pg_meta_desc TEXT,
    pg_created TEXT,
    pg_updated TEXT,
    pg_is_public INTEGER DEFAULT 0
);

INSERT INTO sl_pages (pgid, pg_title, pg_slug, pg_body, pg_status, pg_author_email, pg_meta_title, pg_meta_desc, pg_created, pg_updated, pg_is_public) VALUES (1, 'About Us', 'about-us', 'ShopLocal is a small e-commerce company dedicated to bringing quality products at fair prices. Founded in 2020, we serve customers nationwide with fast shipping and great support.', 'published', 'admin@shoplocal.com', 'About ShopLocal', 'Learn about our mission and values', '2021-01-01', '2024-06-15', 1);
INSERT INTO sl_pages (pgid, pg_title, pg_slug, pg_body, pg_status, pg_author_email, pg_meta_title, pg_meta_desc, pg_created, pg_updated, pg_is_public) VALUES (2, 'Return Policy', 'return-policy', 'Items may be returned within 30 days of delivery. Items must be in original condition with tags attached. Refunds are processed within 5-7 business days.', 'published', 'admin@shoplocal.com', 'Return Policy', 'Our hassle-free return policy', '2021-01-01', '2025-01-10', 1);
INSERT INTO sl_pages (pgid, pg_title, pg_slug, pg_body, pg_status, pg_author_email, pg_meta_title, pg_meta_desc, pg_created, pg_updated, pg_is_public) VALUES (3, 'Shipping Information', 'shipping-info', 'We ship to all 50 US states. Standard shipping takes 3-7 business days. Express shipping takes 1-3 business days. Free shipping on orders over $75.', 'published', 'admin@shoplocal.com', 'Shipping Info', 'Shipping rates and delivery times', '2021-01-01', '2025-02-20', 1);
INSERT INTO sl_pages (pgid, pg_title, pg_slug, pg_body, pg_status, pg_author_email, pg_meta_title, pg_meta_desc, pg_created, pg_updated, pg_is_public) VALUES (4, 'Privacy Policy', 'privacy-policy', 'We take your privacy seriously. We collect only the data necessary to process your orders and improve your shopping experience. We never sell your data to third parties.', 'published', 'admin@shoplocal.com', 'Privacy Policy', 'How we protect your data', '2021-01-01', '2024-12-01', 1);
INSERT INTO sl_pages (pgid, pg_title, pg_slug, pg_body, pg_status, pg_author_email, pg_meta_title, pg_meta_desc, pg_created, pg_updated, pg_is_public) VALUES (5, 'Spring 2025 Lookbook', 'spring-2025-lookbook', 'Check out our curated spring collection featuring the latest trends in fashion and accessories.', 'draft', 'admin@shoplocal.com', 'Spring 2025 Lookbook', 'Spring fashion trends and picks', '2025-02-15', '2025-03-01', 0);

-- =============================================
-- sl_reviews (15 rows)
-- =============================================
CREATE TABLE sl_reviews (
    rvid INTEGER PRIMARY KEY,
    rv_prod_sku TEXT NOT NULL,
    rv_cust_email TEXT NOT NULL,
    rv_rating INTEGER NOT NULL,
    rv_title TEXT,
    rv_body TEXT,
    rv_is_verified INTEGER DEFAULT 0,
    rv_is_approved INTEGER DEFAULT 1,
    rv_helpful INTEGER DEFAULT 0,
    rv_reported INTEGER DEFAULT 0,
    rv_created TEXT
);

INSERT INTO sl_reviews (rvid, rv_prod_sku, rv_cust_email, rv_rating, rv_title, rv_body, rv_is_verified, rv_is_approved, rv_helpful, rv_reported, rv_created) VALUES (1, 'SL-LAPTOP-001', 'alice@email.com', 5, 'Amazing laptop!', 'Fast, lightweight, and the battery lasts all day. Perfect for work and streaming.', 1, 1, 12, 0, '2024-09-25');
INSERT INTO sl_reviews (rvid, rv_prod_sku, rv_cust_email, rv_rating, rv_title, rv_body, rv_is_verified, rv_is_approved, rv_helpful, rv_reported, rv_created) VALUES (2, 'SL-PHONE-002', 'bob@email.com', 4, 'Great phone, pricey though', 'Excellent camera and display. A bit expensive but worth it for the features.', 1, 1, 8, 0, '2024-10-05');
INSERT INTO sl_reviews (rvid, rv_prod_sku, rv_cust_email, rv_rating, rv_title, rv_body, rv_is_verified, rv_is_approved, rv_helpful, rv_reported, rv_created) VALUES (3, 'SL-HEADPH-004', 'carol@email.com', 5, 'Best noise cancelling', 'These headphones block out everything. Sound quality is superb. Highly recommend.', 1, 1, 15, 0, '2024-10-10');
INSERT INTO sl_reviews (rvid, rv_prod_sku, rv_cust_email, rv_rating, rv_title, rv_body, rv_is_verified, rv_is_approved, rv_helpful, rv_reported, rv_created) VALUES (4, 'SL-TSHIRT-005', 'dave@email.com', 3, 'Runs small', 'Nice fabric quality but runs at least one size smaller than expected. Order up.', 1, 1, 20, 0, '2024-10-20');
INSERT INTO sl_reviews (rvid, rv_prod_sku, rv_cust_email, rv_rating, rv_title, rv_body, rv_is_verified, rv_is_approved, rv_helpful, rv_reported, rv_created) VALUES (5, 'SL-TABLET-003', 'eve@email.com', 4, 'Great for reading and drawing', 'The stylus support is fantastic. Screen could be a bit brighter outdoors.', 1, 1, 6, 0, '2024-10-28');
INSERT INTO sl_reviews (rvid, rv_prod_sku, rv_cust_email, rv_rating, rv_title, rv_body, rv_is_verified, rv_is_approved, rv_helpful, rv_reported, rv_created) VALUES (6, 'SL-JEANS-006', 'frank@email.com', 4, 'Comfortable everyday jeans', 'Good stretch and fit. Held up well after multiple washes.', 1, 1, 4, 0, '2024-11-15');
INSERT INTO sl_reviews (rvid, rv_prod_sku, rv_cust_email, rv_rating, rv_title, rv_body, rv_is_verified, rv_is_approved, rv_helpful, rv_reported, rv_created) VALUES (7, 'SL-PHONE-002', 'grace@email.com', 5, 'Love this phone', 'Switched from another brand and could not be happier. Fast, beautiful screen.', 1, 1, 10, 0, '2024-11-25');
INSERT INTO sl_reviews (rvid, rv_prod_sku, rv_cust_email, rv_rating, rv_title, rv_body, rv_is_verified, rv_is_approved, rv_helpful, rv_reported, rv_created) VALUES (8, 'SL-SNEAK-007', 'henry@email.com', 4, 'Lightweight runners', 'Very comfortable for running. The memory foam insole is great.', 1, 1, 7, 0, '2024-12-10');
INSERT INTO sl_reviews (rvid, rv_prod_sku, rv_cust_email, rv_rating, rv_title, rv_body, rv_is_verified, rv_is_approved, rv_helpful, rv_reported, rv_created) VALUES (9, 'SL-WATCH-011', 'ivy@email.com', 5, 'Feature-packed smartwatch', 'Tracks everything accurately. Battery lasts 4 days. Love the sleep tracking.', 1, 1, 9, 0, '2024-12-15');
INSERT INTO sl_reviews (rvid, rv_prod_sku, rv_cust_email, rv_rating, rv_title, rv_body, rv_is_verified, rv_is_approved, rv_helpful, rv_reported, rv_created) VALUES (10, 'SL-BOOK-013', 'jack@email.com', 5, 'Must-have SQL reference', 'Clear explanations with practical examples. Helped me pass my certification.', 1, 1, 18, 0, '2024-12-22');
INSERT INTO sl_reviews (rvid, rv_prod_sku, rv_cust_email, rv_rating, rv_title, rv_body, rv_is_verified, rv_is_approved, rv_helpful, rv_reported, rv_created) VALUES (11, 'SL-WATCH-011', 'kate@email.com', 4, 'Beautiful rose gold version', 'Looks elegant. Wish the band was slightly wider though.', 1, 1, 5, 0, '2024-12-28');
INSERT INTO sl_reviews (rvid, rv_prod_sku, rv_cust_email, rv_rating, rv_title, rv_body, rv_is_verified, rv_is_approved, rv_helpful, rv_reported, rv_created) VALUES (12, 'SL-CHARGER-014', 'henry@email.com', 2, 'Missing ports', 'Advertised as 7-in-1 but mine only has 5 ports. Disappointed.', 1, 1, 22, 0, '2024-12-12');
INSERT INTO sl_reviews (rvid, rv_prod_sku, rv_cust_email, rv_rating, rv_title, rv_body, rv_is_verified, rv_is_approved, rv_helpful, rv_reported, rv_created) VALUES (13, 'SL-BLNDR-009', 'alice@email.com', 4, 'Powerful blender', 'Makes smoothies in seconds. A bit loud but that is expected for the power.', 1, 1, 3, 0, '2025-01-15');
INSERT INTO sl_reviews (rvid, rv_prod_sku, rv_cust_email, rv_rating, rv_title, rv_body, rv_is_verified, rv_is_approved, rv_helpful, rv_reported, rv_created) VALUES (14, 'SL-SNEAK-007', 'leo@email.com', 2, 'Too narrow', 'If you have wide feet, skip these. Very uncomfortable after 30 minutes.', 1, 1, 11, 0, '2025-01-25');
INSERT INTO sl_reviews (rvid, rv_prod_sku, rv_cust_email, rv_rating, rv_title, rv_body, rv_is_verified, rv_is_approved, rv_helpful, rv_reported, rv_created) VALUES (15, 'SL-MUG-015', 'dave@email.com', 1, 'Arrived broken', 'Both mugs arrived with cracks. Packaging was terrible. Disappointed.', 0, 1, 14, 1, '2024-10-22');

-- =============================================
-- sl_banners (6 rows)
-- =============================================
CREATE TABLE sl_banners (
    bnid INTEGER PRIMARY KEY,
    bn_title TEXT NOT NULL,
    bn_img_url TEXT NOT NULL,
    bn_link TEXT,
    bn_position TEXT,
    bn_start TEXT,
    bn_end TEXT,
    bn_is_active INTEGER DEFAULT 1,
    bn_clicks INTEGER DEFAULT 0,
    bn_impressions INTEGER DEFAULT 0,
    bn_created_by TEXT
);

INSERT INTO sl_banners (bnid, bn_title, bn_img_url, bn_link, bn_position, bn_start, bn_end, bn_is_active, bn_clicks, bn_impressions, bn_created_by) VALUES (1, 'Spring Sale - Up to 30% Off', '/img/banners/spring-sale.jpg', '/sale/spring-2025', 'hero', '2025-03-01', '2025-04-30', 1, 1245, 28500, 'admin');
INSERT INTO sl_banners (bnid, bn_title, bn_img_url, bn_link, bn_position, bn_start, bn_end, bn_is_active, bn_clicks, bn_impressions, bn_created_by) VALUES (2, 'New Tech Arrivals', '/img/banners/tech-arrivals.jpg', '/category/electronics', 'hero', '2025-02-15', '2025-03-31', 1, 890, 22000, 'admin');
INSERT INTO sl_banners (bnid, bn_title, bn_img_url, bn_link, bn_position, bn_start, bn_end, bn_is_active, bn_clicks, bn_impressions, bn_created_by) VALUES (3, 'Free Shipping Over $75', '/img/banners/free-shipping.jpg', '/shipping-info', 'sidebar', '2024-06-01', '2025-06-30', 1, 3200, 95000, 'admin');
INSERT INTO sl_banners (bnid, bn_title, bn_img_url, bn_link, bn_position, bn_start, bn_end, bn_is_active, bn_clicks, bn_impressions, bn_created_by) VALUES (4, 'Holiday Deals - Ended', '/img/banners/holiday-deals.jpg', '/sale/holiday-2024', 'hero', '2024-11-25', '2024-12-31', 0, 5400, 120000, 'admin');
INSERT INTO sl_banners (bnid, bn_title, bn_img_url, bn_link, bn_position, bn_start, bn_end, bn_is_active, bn_clicks, bn_impressions, bn_created_by) VALUES (5, 'Download Our App', '/img/banners/app-download.jpg', '/app', 'footer', '2024-01-01', '2025-12-31', 1, 780, 45000, 'admin');
INSERT INTO sl_banners (bnid, bn_title, bn_img_url, bn_link, bn_position, bn_start, bn_end, bn_is_active, bn_clicks, bn_impressions, bn_created_by) VALUES (6, 'Join Loyalty Program', '/img/banners/loyalty.jpg', '/loyalty', 'sidebar', '2025-01-15', '2025-12-31', 1, 450, 18000, 'admin');

-- =============================================
-- sl_tax_rates (6 rows)
-- =============================================
CREATE TABLE sl_tax_rates (
    txid INTEGER PRIMARY KEY,
    tx_state TEXT NOT NULL,
    tx_rate REAL NOT NULL,
    tx_name TEXT,
    tx_type TEXT DEFAULT 'sales',
    tx_is_active INTEGER DEFAULT 1,
    tx_effective_from TEXT,
    tx_effective_to TEXT,
    tx_applies_to TEXT DEFAULT 'all',
    tx_created TEXT
);

INSERT INTO sl_tax_rates (txid, tx_state, tx_rate, tx_name, tx_type, tx_is_active, tx_effective_from, tx_effective_to, tx_applies_to, tx_created) VALUES (1, 'CA', 9.00, 'California Sales Tax', 'sales', 1, '2024-01-01', NULL, 'all', '2024-01-01');
INSERT INTO sl_tax_rates (txid, tx_state, tx_rate, tx_name, tx_type, tx_is_active, tx_effective_from, tx_effective_to, tx_applies_to, tx_created) VALUES (2, 'TX', 8.25, 'Texas Sales Tax', 'sales', 1, '2024-01-01', NULL, 'all', '2024-01-01');
INSERT INTO sl_tax_rates (txid, tx_state, tx_rate, tx_name, tx_type, tx_is_active, tx_effective_from, tx_effective_to, tx_applies_to, tx_created) VALUES (3, 'WA', 10.00, 'Washington Sales Tax', 'sales', 1, '2024-01-01', NULL, 'all', '2024-01-01');
INSERT INTO sl_tax_rates (txid, tx_state, tx_rate, tx_name, tx_type, tx_is_active, tx_effective_from, tx_effective_to, tx_applies_to, tx_created) VALUES (4, 'FL', 7.00, 'Florida Sales Tax', 'sales', 1, '2024-01-01', NULL, 'all', '2024-01-01');
INSERT INTO sl_tax_rates (txid, tx_state, tx_rate, tx_name, tx_type, tx_is_active, tx_effective_from, tx_effective_to, tx_applies_to, tx_created) VALUES (5, 'OR', 0.00, 'Oregon No Sales Tax', 'sales', 1, '2024-01-01', NULL, 'all', '2024-01-01');
INSERT INTO sl_tax_rates (txid, tx_state, tx_rate, tx_name, tx_type, tx_is_active, tx_effective_from, tx_effective_to, tx_applies_to, tx_created) VALUES (6, 'IL', 10.25, 'Illinois Sales Tax', 'sales', 1, '2024-01-01', NULL, 'all', '2024-01-01');

-- =============================================
-- sl_gift_cards (5 rows)
-- =============================================
CREATE TABLE sl_gift_cards (
    gcid INTEGER PRIMARY KEY,
    gc_code TEXT NOT NULL,
    gc_balance REAL NOT NULL,
    gc_initial_amt REAL NOT NULL,
    gc_cust_email TEXT,
    gc_recipient_email TEXT,
    gc_message TEXT,
    gc_is_active INTEGER DEFAULT 1,
    gc_created TEXT,
    gc_expires TEXT,
    gc_last_used TEXT
);

INSERT INTO sl_gift_cards (gcid, gc_code, gc_balance, gc_initial_amt, gc_cust_email, gc_recipient_email, gc_message, gc_is_active, gc_created, gc_expires, gc_last_used) VALUES (1, 'GC-ABCD-1234', 25.00, 50.00, 'alice@email.com', 'carol@email.com', 'Happy Birthday Carol!', 1, '2024-11-01', '2025-11-01', '2025-01-15');
INSERT INTO sl_gift_cards (gcid, gc_code, gc_balance, gc_initial_amt, gc_cust_email, gc_recipient_email, gc_message, gc_is_active, gc_created, gc_expires, gc_last_used) VALUES (2, 'GC-EFGH-5678', 100.00, 100.00, 'bob@email.com', 'dave@email.com', 'Merry Christmas!', 1, '2024-12-20', '2025-12-20', NULL);
INSERT INTO sl_gift_cards (gcid, gc_code, gc_balance, gc_initial_amt, gc_cust_email, gc_recipient_email, gc_message, gc_is_active, gc_created, gc_expires, gc_last_used) VALUES (3, 'GC-IJKL-9012', 0.00, 25.00, 'grace@email.com', 'henry@email.com', 'Thanks for your help!', 0, '2024-08-15', '2025-08-15', '2024-11-28');
INSERT INTO sl_gift_cards (gcid, gc_code, gc_balance, gc_initial_amt, gc_cust_email, gc_recipient_email, gc_message, gc_is_active, gc_created, gc_expires, gc_last_used) VALUES (4, 'GC-MNOP-3456', 75.00, 75.00, 'kate@email.com', 'ivy@email.com', 'Enjoy some shopping!', 1, '2025-02-14', '2026-02-14', NULL);
INSERT INTO sl_gift_cards (gcid, gc_code, gc_balance, gc_initial_amt, gc_cust_email, gc_recipient_email, gc_message, gc_is_active, gc_created, gc_expires, gc_last_used) VALUES (5, 'GC-QRST-7890', 39.98, 50.00, 'frank@email.com', 'eve@email.com', 'Just because!', 1, '2025-01-10', '2026-01-10', '2025-02-20');
