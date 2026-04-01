-- ============================================================
-- NexGenMart Target Schema — Post-Acquisition of ShopLocal
-- 55 tables, proper FKs, NOT NULL, UNIQUE, DEFAULT constraints
-- ZERO table/column name overlap with sl_ prefixed initial schema
-- ============================================================

-- ============================================================
-- GROUP 1: Customer Domain
-- ============================================================

-- TABLE 1: users (12 rows)
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT,
    password_hash TEXT NOT NULL,
    date_of_birth TEXT,
    registered_at TEXT NOT NULL,
    last_active_at TEXT,
    is_active INTEGER NOT NULL DEFAULT 1
);
INSERT INTO users VALUES (1, 'Alice', 'Chen', 'alice@email.com', '555-0101', 'hash_alice_01', '1990-03-15', '2024-01-10 08:00:00', '2024-12-01 10:30:00', 1);
INSERT INTO users VALUES (2, 'Bob', 'Rivera', 'bob@email.com', '555-0102', 'hash_bob_02', '1985-07-22', '2024-01-12 09:15:00', '2024-11-28 14:20:00', 1);
INSERT INTO users VALUES (3, 'Carol', 'Zhang', 'carol@email.com', '555-0103', 'hash_carol_03', '1992-11-08', '2024-01-15 11:30:00', '2024-12-02 09:45:00', 1);
INSERT INTO users VALUES (4, 'Dave', 'Wilson', 'dave@email.com', '555-0104', 'hash_dave_04', '1988-05-30', '2024-01-20 10:00:00', '2024-11-25 16:10:00', 1);
INSERT INTO users VALUES (5, 'Eve', 'Thompson', 'eve@email.com', '555-0105', 'hash_eve_05', '1995-01-17', '2024-02-01 08:30:00', '2024-12-03 11:00:00', 1);
INSERT INTO users VALUES (6, 'Frank', 'Garcia', 'frank@email.com', '555-0106', 'hash_frank_06', '1983-09-25', '2024-02-05 14:00:00', '2024-11-30 08:55:00', 1);
INSERT INTO users VALUES (7, 'Grace', 'Kim', 'grace@email.com', '555-0107', 'hash_grace_07', '1991-12-03', '2024-02-10 09:45:00', '2024-12-01 15:30:00', 1);
INSERT INTO users VALUES (8, 'Henry', 'Patel', 'henry@email.com', '555-0108', 'hash_henry_08', '1987-04-12', '2024-02-15 10:20:00', '2024-11-29 12:40:00', 1);
INSERT INTO users VALUES (9, 'Ivy', 'Santos', 'ivy@email.com', '555-0109', 'hash_ivy_09', '1994-08-19', '2024-03-01 07:00:00', '2024-12-02 17:15:00', 1);
INSERT INTO users VALUES (10, 'Jack', 'Murphy', 'jack@email.com', '555-0110', 'hash_jack_10', '1986-02-28', '2024-03-05 13:10:00', '2024-11-27 09:20:00', 1);
INSERT INTO users VALUES (11, 'Kate', 'Brown', 'kate@email.com', '555-0111', 'hash_kate_11', '1993-06-14', '2024-03-10 08:50:00', '2024-12-03 14:05:00', 1);
INSERT INTO users VALUES (12, 'Leo', 'Martinez', 'leo@email.com', '555-0112', 'hash_leo_12', '1989-10-07', '2024-03-15 11:25:00', '2024-11-26 10:50:00', 1);

-- TABLE 2: user_addresses (16 rows)
CREATE TABLE user_addresses (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    address_type TEXT NOT NULL,
    line1 TEXT NOT NULL,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    postal_code TEXT NOT NULL,
    country TEXT NOT NULL DEFAULT 'US',
    is_default INTEGER NOT NULL DEFAULT 0
);
INSERT INTO user_addresses VALUES (1, 1, 'shipping', '100 Maple St', 'New York', 'NY', '10001', 'US', 1);
INSERT INTO user_addresses VALUES (2, 1, 'billing', '100 Maple St', 'New York', 'NY', '10001', 'US', 0);
INSERT INTO user_addresses VALUES (3, 2, 'shipping', '200 Oak Ave', 'Los Angeles', 'CA', '90001', 'US', 1);
INSERT INTO user_addresses VALUES (4, 3, 'shipping', '300 Pine Rd', 'Chicago', 'IL', '60601', 'US', 1);
INSERT INTO user_addresses VALUES (5, 4, 'shipping', '400 Elm Blvd', 'Houston', 'TX', '77001', 'US', 1);
INSERT INTO user_addresses VALUES (6, 5, 'shipping', '500 Cedar Ln', 'Phoenix', 'AZ', '85001', 'US', 1);
INSERT INTO user_addresses VALUES (7, 5, 'billing', '501 Cedar Ln', 'Phoenix', 'AZ', '85001', 'US', 0);
INSERT INTO user_addresses VALUES (8, 6, 'shipping', '600 Birch Dr', 'Philadelphia', 'PA', '19101', 'US', 1);
INSERT INTO user_addresses VALUES (9, 7, 'shipping', '700 Walnut Ct', 'San Antonio', 'TX', '78201', 'US', 1);
INSERT INTO user_addresses VALUES (10, 8, 'shipping', '800 Spruce Way', 'San Diego', 'CA', '92101', 'US', 1);
INSERT INTO user_addresses VALUES (11, 9, 'shipping', '900 Ash Pl', 'Dallas', 'TX', '75201', 'US', 1);
INSERT INTO user_addresses VALUES (12, 9, 'billing', '900 Ash Pl', 'Dallas', 'TX', '75201', 'US', 0);
INSERT INTO user_addresses VALUES (13, 10, 'shipping', '1000 Poplar St', 'San Jose', 'CA', '95101', 'US', 1);
INSERT INTO user_addresses VALUES (14, 11, 'shipping', '1100 Willow Ave', 'Austin', 'TX', '73301', 'US', 1);
INSERT INTO user_addresses VALUES (15, 12, 'shipping', '1200 Hickory Rd', 'Jacksonville', 'FL', '32099', 'US', 1);
INSERT INTO user_addresses VALUES (16, 12, 'billing', '1200 Hickory Rd', 'Jacksonville', 'FL', '32099', 'US', 0);

-- TABLE 3: user_preferences (12 rows)
CREATE TABLE user_preferences (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL UNIQUE REFERENCES users(id),
    newsletter_opt_in INTEGER NOT NULL DEFAULT 1,
    preferred_language TEXT NOT NULL DEFAULT 'en',
    preferred_currency TEXT NOT NULL DEFAULT 'USD',
    theme TEXT NOT NULL DEFAULT 'light'
);
INSERT INTO user_preferences VALUES (1, 1, 1, 'en', 'USD', 'dark');
INSERT INTO user_preferences VALUES (2, 2, 1, 'en', 'USD', 'light');
INSERT INTO user_preferences VALUES (3, 3, 1, 'zh', 'USD', 'light');
INSERT INTO user_preferences VALUES (4, 4, 0, 'en', 'USD', 'dark');
INSERT INTO user_preferences VALUES (5, 5, 1, 'en', 'USD', 'light');
INSERT INTO user_preferences VALUES (6, 6, 0, 'es', 'USD', 'light');
INSERT INTO user_preferences VALUES (7, 7, 1, 'ko', 'USD', 'dark');
INSERT INTO user_preferences VALUES (8, 8, 1, 'en', 'USD', 'light');
INSERT INTO user_preferences VALUES (9, 9, 1, 'pt', 'USD', 'light');
INSERT INTO user_preferences VALUES (10, 10, 0, 'en', 'USD', 'light');
INSERT INTO user_preferences VALUES (11, 11, 1, 'en', 'USD', 'dark');
INSERT INTO user_preferences VALUES (12, 12, 1, 'es', 'USD', 'light');

-- TABLE 4: user_stats (12 rows)
CREATE TABLE user_stats (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL UNIQUE REFERENCES users(id),
    total_orders INTEGER NOT NULL DEFAULT 0,
    total_spent REAL NOT NULL DEFAULT 0.0,
    average_order_value REAL,
    first_order_at TEXT,
    last_order_at TEXT,
    total_reviews INTEGER NOT NULL DEFAULT 0
);
INSERT INTO user_stats VALUES (1, 1, 3, 2549.97, 849.99, '2024-02-01 10:00:00', '2024-06-15 09:00:00', 2);
INSERT INTO user_stats VALUES (2, 2, 2, 1299.98, 649.99, '2024-02-10 11:30:00', '2024-05-20 14:00:00', 2);
INSERT INTO user_stats VALUES (3, 3, 2, 879.98, 439.99, '2024-02-15 09:45:00', '2024-07-01 10:30:00', 1);
INSERT INTO user_stats VALUES (4, 4, 2, 1649.98, 824.99, '2024-03-01 08:00:00', '2024-06-20 16:00:00', 2);
INSERT INTO user_stats VALUES (5, 5, 2, 459.98, 229.99, '2024-03-10 10:15:00', '2024-07-10 11:45:00', 1);
INSERT INTO user_stats VALUES (6, 6, 2, 1099.98, 549.99, '2024-03-15 14:30:00', '2024-08-01 09:00:00', 1);
INSERT INTO user_stats VALUES (7, 7, 1, 749.99, 749.99, '2024-04-01 08:45:00', '2024-04-01 08:45:00', 2);
INSERT INTO user_stats VALUES (8, 8, 2, 399.98, 199.99, '2024-04-10 10:00:00', '2024-08-15 13:30:00', 1);
INSERT INTO user_stats VALUES (9, 9, 1, 149.99, 149.99, '2024-04-20 09:30:00', '2024-04-20 09:30:00', 1);
INSERT INTO user_stats VALUES (10, 10, 1, 999.99, 999.99, '2024-05-01 11:00:00', '2024-05-01 11:00:00', 1);
INSERT INTO user_stats VALUES (11, 11, 1, 329.99, 329.99, '2024-05-10 08:30:00', '2024-05-10 08:30:00', 1);
INSERT INTO user_stats VALUES (12, 12, 1, 199.99, 199.99, '2024-05-15 14:00:00', '2024-05-15 14:00:00', 0);

-- TABLE 5: user_notes (8 rows)
CREATE TABLE user_notes (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    content TEXT NOT NULL,
    note_type TEXT NOT NULL,
    author TEXT NOT NULL,
    priority TEXT NOT NULL DEFAULT 'normal',
    status TEXT NOT NULL DEFAULT 'open',
    created_at TEXT NOT NULL,
    updated_at TEXT,
    is_internal INTEGER NOT NULL DEFAULT 1
);
INSERT INTO user_notes VALUES (1, 1, 'VIP customer, always expedite shipping', 'flag', 'Agent Smith', 'high', 'open', '2024-02-15 10:00:00', NULL, 1);
INSERT INTO user_notes VALUES (2, 2, 'Prefers email communication only', 'preference', 'Agent Smith', 'normal', 'open', '2024-03-01 09:00:00', NULL, 1);
INSERT INTO user_notes VALUES (3, 3, 'Had billing issue resolved on 2024-03-20', 'incident', 'Agent Jones', 'normal', 'closed', '2024-03-20 14:30:00', '2024-03-21 09:00:00', 1);
INSERT INTO user_notes VALUES (4, 4, 'Requested product recommendations for gaming', 'request', 'Agent Jones', 'low', 'closed', '2024-04-01 11:00:00', '2024-04-02 10:00:00', 1);
INSERT INTO user_notes VALUES (5, 5, 'Interested in bulk orders for office supplies', 'lead', 'Agent Davis', 'high', 'open', '2024-04-15 08:30:00', NULL, 1);
INSERT INTO user_notes VALUES (6, 7, 'Reported slow delivery twice', 'complaint', 'Agent Davis', 'high', 'open', '2024-05-01 10:00:00', NULL, 1);
INSERT INTO user_notes VALUES (7, 9, 'Birthday discount applied manually', 'adjustment', 'Agent Wilson', 'normal', 'closed', '2024-05-10 15:00:00', '2024-05-10 15:30:00', 1);
INSERT INTO user_notes VALUES (8, 11, 'Account verified after security check', 'security', 'Agent Wilson', 'normal', 'closed', '2024-06-01 09:00:00', '2024-06-01 09:45:00', 1);

-- ============================================================
-- GROUP 2: Catalog Domain
-- ============================================================

-- TABLE 6: categories (8 rows)
CREATE TABLE categories (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    slug TEXT NOT NULL UNIQUE,
    description TEXT,
    parent_id INTEGER REFERENCES categories(id),
    is_active INTEGER NOT NULL DEFAULT 1,
    sort_order INTEGER NOT NULL DEFAULT 0,
    image_url TEXT,
    meta_title TEXT,
    meta_description TEXT
);
INSERT INTO categories VALUES (1, 'Electronics', 'electronics', 'Electronic devices and accessories', NULL, 1, 1, 'https://img.nexgenmart.com/cat/electronics.jpg', 'Electronics - NexGenMart', 'Shop the latest electronics');
INSERT INTO categories VALUES (2, 'Computers', 'computers', 'Laptops, desktops and components', 1, 1, 2, 'https://img.nexgenmart.com/cat/computers.jpg', 'Computers - NexGenMart', 'Find your perfect computer');
INSERT INTO categories VALUES (3, 'Audio', 'audio', 'Headphones, speakers and audio gear', 1, 1, 3, 'https://img.nexgenmart.com/cat/audio.jpg', 'Audio - NexGenMart', 'Premium audio equipment');
INSERT INTO categories VALUES (4, 'Home & Kitchen', 'home-kitchen', 'Home appliances and kitchen essentials', NULL, 1, 4, 'https://img.nexgenmart.com/cat/home.jpg', 'Home & Kitchen - NexGenMart', 'Everything for your home');
INSERT INTO categories VALUES (5, 'Wearables', 'wearables', 'Smartwatches and fitness trackers', 1, 1, 5, 'https://img.nexgenmart.com/cat/wearables.jpg', 'Wearables - NexGenMart', 'Stay connected on the go');
INSERT INTO categories VALUES (6, 'Office Supplies', 'office-supplies', 'Desk accessories and office essentials', NULL, 1, 6, 'https://img.nexgenmart.com/cat/office.jpg', 'Office Supplies - NexGenMart', 'Equip your workspace');
INSERT INTO categories VALUES (7, 'Photography', 'photography', 'Cameras and photography equipment', 1, 1, 7, 'https://img.nexgenmart.com/cat/photo.jpg', 'Photography - NexGenMart', 'Capture every moment');
INSERT INTO categories VALUES (8, 'Drinkware', 'drinkware', 'Mugs, bottles and tumblers', 4, 1, 8, 'https://img.nexgenmart.com/cat/drinkware.jpg', 'Drinkware - NexGenMart', 'Sip in style');

-- TABLE 7: brands (6 rows)
CREATE TABLE brands (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    slug TEXT NOT NULL UNIQUE,
    description TEXT,
    logo_url TEXT,
    website_url TEXT,
    country_of_origin TEXT,
    year_founded INTEGER,
    is_active INTEGER NOT NULL DEFAULT 1,
    contact_email TEXT
);
INSERT INTO brands VALUES (1, 'TechPro', 'techpro', 'Premium technology products', 'https://img.nexgenmart.com/brands/techpro.png', 'https://techpro.example.com', 'US', 2010, 1, 'sales@techpro.example.com');
INSERT INTO brands VALUES (2, 'AudioMax', 'audiomax', 'Professional audio equipment', 'https://img.nexgenmart.com/brands/audiomax.png', 'https://audiomax.example.com', 'JP', 2005, 1, 'info@audiomax.example.com');
INSERT INTO brands VALUES (3, 'HomeStyle', 'homestyle', 'Modern home essentials', 'https://img.nexgenmart.com/brands/homestyle.png', 'https://homestyle.example.com', 'US', 2015, 1, 'hello@homestyle.example.com');
INSERT INTO brands VALUES (4, 'FitGear', 'fitgear', 'Fitness and wearable technology', 'https://img.nexgenmart.com/brands/fitgear.png', 'https://fitgear.example.com', 'KR', 2012, 1, 'support@fitgear.example.com');
INSERT INTO brands VALUES (5, 'SnapShot', 'snapshot', 'Photography and imaging', 'https://img.nexgenmart.com/brands/snapshot.png', 'https://snapshot.example.com', 'DE', 2008, 1, 'contact@snapshot.example.com');
INSERT INTO brands VALUES (6, 'DeskMate', 'deskmate', 'Office and desk accessories', 'https://img.nexgenmart.com/brands/deskmate.png', 'https://deskmate.example.com', 'US', 2018, 1, 'sales@deskmate.example.com');

-- TABLE 8: products (15 rows)
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    sku TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    description TEXT,
    category_id INTEGER NOT NULL REFERENCES categories(id),
    brand_id INTEGER REFERENCES brands(id),
    base_price REAL NOT NULL,
    cost_price REAL,
    weight_kg REAL,
    dimensions TEXT,
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL,
    updated_at TEXT
);
INSERT INTO products VALUES (1, 'SL-LAPTOP-001', 'ProBook Laptop 15', 'High-performance 15-inch laptop with 16GB RAM', 2, 1, 999.99, 650.00, 2.1, '35.8x24.2x1.8 cm', 1, '2024-01-05 10:00:00', '2024-06-01 12:00:00');
INSERT INTO products VALUES (2, 'SL-PHONE-002', 'SmartPhone X12', 'Latest smartphone with OLED display', 1, 1, 799.99, 450.00, 0.18, '15.2x7.1x0.8 cm', 1, '2024-01-06 10:00:00', '2024-05-15 09:00:00');
INSERT INTO products VALUES (3, 'SL-HEADPH-003', 'NoiseCancel Pro', 'Wireless noise-cancelling headphones', 3, 2, 249.99, 120.00, 0.25, '18x17x8 cm', 1, '2024-01-07 10:00:00', '2024-04-20 11:00:00');
INSERT INTO products VALUES (4, 'SL-TABLET-004', 'TabletAir 10', '10-inch tablet with stylus support', 2, 1, 499.99, 280.00, 0.45, '24.5x17.4x0.6 cm', 1, '2024-01-08 10:00:00', '2024-06-10 14:00:00');
INSERT INTO products VALUES (5, 'SL-WATCH-005', 'FitWatch Ultra', 'Advanced fitness smartwatch with GPS', 5, 4, 349.99, 180.00, 0.05, '4.4x3.8x1.1 cm', 1, '2024-01-09 10:00:00', '2024-07-01 10:00:00');
INSERT INTO products VALUES (6, 'SL-SPEAKER-006', 'BoomBox 360', 'Portable Bluetooth speaker with 360 sound', 3, 2, 149.99, 65.00, 0.8, '12x12x15 cm', 1, '2024-01-10 10:00:00', '2024-05-20 08:00:00');
INSERT INTO products VALUES (7, 'SL-CAMERA-007', 'SnapShot DSLR 5000', 'Professional DSLR camera 24MP', 7, 5, 1299.99, 750.00, 0.85, '14x10.5x7.8 cm', 1, '2024-01-11 10:00:00', '2024-06-15 10:00:00');
INSERT INTO products VALUES (8, 'SL-KEYBOARD-008', 'MechType Pro', 'Mechanical keyboard with RGB lighting', 6, 6, 129.99, 55.00, 0.95, '44x14x3.5 cm', 1, '2024-01-12 10:00:00', '2024-04-10 09:00:00');
INSERT INTO products VALUES (9, 'SL-MOUSE-009', 'ErgoGlide Mouse', 'Ergonomic wireless mouse', 6, 6, 59.99, 22.00, 0.1, '12x7x4 cm', 1, '2024-01-13 10:00:00', '2024-03-25 11:00:00');
INSERT INTO products VALUES (10, 'SL-MONITOR-010', 'UltraView 27', '27-inch 4K IPS monitor', 2, 1, 449.99, 280.00, 5.5, '61.3x36.4x5.2 cm', 1, '2024-01-14 10:00:00', '2024-07-05 10:00:00');
INSERT INTO products VALUES (11, 'SL-CHARGER-011', 'PowerHub 6-Port', '6-port USB-C fast charger', 1, 1, 49.99, 18.00, 0.3, '10x8x3 cm', 1, '2024-01-15 10:00:00', '2024-05-01 08:00:00');
INSERT INTO products VALUES (12, 'SL-EARBUDS-012', 'AudioMax Buds Pro', 'True wireless earbuds with ANC', 3, 2, 179.99, 75.00, 0.06, '6x6x3 cm', 1, '2024-01-16 10:00:00', '2024-06-20 10:00:00');
INSERT INTO products VALUES (13, 'SL-BLENDER-013', 'HomeStyle Blender X', 'High-power kitchen blender 1200W', 4, 3, 89.99, 40.00, 3.2, '20x20x40 cm', 1, '2024-01-17 10:00:00', '2024-04-15 09:00:00');
INSERT INTO products VALUES (14, 'SL-LAMP-014', 'DeskGlow LED Lamp', 'Adjustable LED desk lamp with USB port', 6, 6, 39.99, 15.00, 0.6, '15x15x45 cm', 1, '2024-01-18 10:00:00', '2024-03-30 10:00:00');
INSERT INTO products VALUES (15, 'SL-MUG-015', 'ThermoSip Travel Mug', 'Insulated stainless steel travel mug 16oz', 8, 3, 24.99, 8.00, 0.35, '8x8x18 cm', 1, '2024-01-19 10:00:00', '2024-05-10 09:00:00');

-- TABLE 9: product_variants (20 rows)
CREATE TABLE product_variants (
    id INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(id),
    variant_name TEXT NOT NULL,
    variant_sku TEXT NOT NULL UNIQUE,
    price_adjustment REAL NOT NULL DEFAULT 0.0,
    stock_quantity INTEGER NOT NULL DEFAULT 0,
    color TEXT,
    size TEXT,
    weight_kg REAL,
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL
);
INSERT INTO product_variants VALUES (1, 1, 'ProBook 15 - Silver 16GB', 'SL-LAPTOP-001-SIL16', 0.0, 25, 'Silver', NULL, 2.1, 1, '2024-01-05 10:00:00');
INSERT INTO product_variants VALUES (2, 1, 'ProBook 15 - Space Gray 32GB', 'SL-LAPTOP-001-GRY32', 200.0, 15, 'Space Gray', NULL, 2.2, 1, '2024-01-05 10:00:00');
INSERT INTO product_variants VALUES (3, 2, 'SmartPhone X12 - Black 128GB', 'SL-PHONE-002-BLK128', 0.0, 50, 'Black', '128GB', 0.18, 1, '2024-01-06 10:00:00');
INSERT INTO product_variants VALUES (4, 2, 'SmartPhone X12 - White 256GB', 'SL-PHONE-002-WHT256', 100.0, 30, 'White', '256GB', 0.18, 1, '2024-01-06 10:00:00');
INSERT INTO product_variants VALUES (5, 3, 'NoiseCancel Pro - Black', 'SL-HEADPH-003-BLK', 0.0, 40, 'Black', NULL, 0.25, 1, '2024-01-07 10:00:00');
INSERT INTO product_variants VALUES (6, 3, 'NoiseCancel Pro - White', 'SL-HEADPH-003-WHT', 0.0, 35, 'White', NULL, 0.25, 1, '2024-01-07 10:00:00');
INSERT INTO product_variants VALUES (7, 4, 'TabletAir 10 - 64GB', 'SL-TABLET-004-64', 0.0, 20, NULL, '64GB', 0.45, 1, '2024-01-08 10:00:00');
INSERT INTO product_variants VALUES (8, 4, 'TabletAir 10 - 128GB', 'SL-TABLET-004-128', 80.0, 18, NULL, '128GB', 0.45, 1, '2024-01-08 10:00:00');
INSERT INTO product_variants VALUES (9, 5, 'FitWatch Ultra - Black S', 'SL-WATCH-005-BLKS', 0.0, 60, 'Black', 'Small', 0.05, 1, '2024-01-09 10:00:00');
INSERT INTO product_variants VALUES (10, 5, 'FitWatch Ultra - Black L', 'SL-WATCH-005-BLKL', 0.0, 45, 'Black', 'Large', 0.05, 1, '2024-01-09 10:00:00');
INSERT INTO product_variants VALUES (11, 6, 'BoomBox 360 - Red', 'SL-SPEAKER-006-RED', 0.0, 30, 'Red', NULL, 0.8, 1, '2024-01-10 10:00:00');
INSERT INTO product_variants VALUES (12, 6, 'BoomBox 360 - Blue', 'SL-SPEAKER-006-BLU', 0.0, 28, 'Blue', NULL, 0.8, 1, '2024-01-10 10:00:00');
INSERT INTO product_variants VALUES (13, 7, 'SnapShot DSLR 5000 - Body Only', 'SL-CAMERA-007-BODY', 0.0, 12, 'Black', NULL, 0.85, 1, '2024-01-11 10:00:00');
INSERT INTO product_variants VALUES (14, 7, 'SnapShot DSLR 5000 - Kit', 'SL-CAMERA-007-KIT', 300.0, 8, 'Black', NULL, 1.2, 1, '2024-01-11 10:00:00');
INSERT INTO product_variants VALUES (15, 8, 'MechType Pro - Blue Switch', 'SL-KEYBOARD-008-BLU', 0.0, 22, NULL, NULL, 0.95, 1, '2024-01-12 10:00:00');
INSERT INTO product_variants VALUES (16, 8, 'MechType Pro - Red Switch', 'SL-KEYBOARD-008-RED', 0.0, 18, NULL, NULL, 0.95, 1, '2024-01-12 10:00:00');
INSERT INTO product_variants VALUES (17, 10, 'UltraView 27 - Standard', 'SL-MONITOR-010-STD', 0.0, 14, 'Black', NULL, 5.5, 1, '2024-01-14 10:00:00');
INSERT INTO product_variants VALUES (18, 12, 'AudioMax Buds Pro - Black', 'SL-EARBUDS-012-BLK', 0.0, 55, 'Black', NULL, 0.06, 1, '2024-01-16 10:00:00');
INSERT INTO product_variants VALUES (19, 15, 'ThermoSip Mug - Navy', 'SL-MUG-015-NVY', 0.0, 100, 'Navy', '16oz', 0.35, 1, '2024-01-19 10:00:00');
INSERT INTO product_variants VALUES (20, 15, 'ThermoSip Mug - Red', 'SL-MUG-015-RED', 0.0, 85, 'Red', '16oz', 0.35, 1, '2024-01-19 10:00:00');

-- TABLE 10: product_images (18 rows)
CREATE TABLE product_images (
    id INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(id),
    image_url TEXT NOT NULL,
    alt_text TEXT,
    sort_order INTEGER NOT NULL DEFAULT 0,
    is_primary INTEGER NOT NULL DEFAULT 0,
    width INTEGER,
    height INTEGER,
    file_size_kb INTEGER,
    mime_type TEXT NOT NULL DEFAULT 'image/jpeg',
    uploaded_at TEXT NOT NULL
);
INSERT INTO product_images VALUES (1, 1, 'https://img.nexgenmart.com/products/laptop-001-main.jpg', 'ProBook Laptop 15 front view', 0, 1, 1200, 800, 245, 'image/jpeg', '2024-01-05 10:30:00');
INSERT INTO product_images VALUES (2, 1, 'https://img.nexgenmart.com/products/laptop-001-side.jpg', 'ProBook Laptop 15 side view', 1, 0, 1200, 800, 198, 'image/jpeg', '2024-01-05 10:31:00');
INSERT INTO product_images VALUES (3, 2, 'https://img.nexgenmart.com/products/phone-002-main.jpg', 'SmartPhone X12 front view', 0, 1, 800, 1200, 180, 'image/jpeg', '2024-01-06 10:30:00');
INSERT INTO product_images VALUES (4, 3, 'https://img.nexgenmart.com/products/headph-003-main.jpg', 'NoiseCancel Pro headphones', 0, 1, 1000, 1000, 210, 'image/jpeg', '2024-01-07 10:30:00');
INSERT INTO product_images VALUES (5, 4, 'https://img.nexgenmart.com/products/tablet-004-main.jpg', 'TabletAir 10 front view', 0, 1, 1200, 900, 230, 'image/jpeg', '2024-01-08 10:30:00');
INSERT INTO product_images VALUES (6, 5, 'https://img.nexgenmart.com/products/watch-005-main.jpg', 'FitWatch Ultra on wrist', 0, 1, 800, 800, 150, 'image/jpeg', '2024-01-09 10:30:00');
INSERT INTO product_images VALUES (7, 6, 'https://img.nexgenmart.com/products/speaker-006-main.jpg', 'BoomBox 360 speaker', 0, 1, 1000, 1000, 190, 'image/jpeg', '2024-01-10 10:30:00');
INSERT INTO product_images VALUES (8, 7, 'https://img.nexgenmart.com/products/camera-007-main.jpg', 'SnapShot DSLR 5000 body', 0, 1, 1400, 1000, 320, 'image/jpeg', '2024-01-11 10:30:00');
INSERT INTO product_images VALUES (9, 7, 'https://img.nexgenmart.com/products/camera-007-kit.jpg', 'SnapShot DSLR 5000 with lens kit', 1, 0, 1400, 1000, 340, 'image/jpeg', '2024-01-11 10:31:00');
INSERT INTO product_images VALUES (10, 8, 'https://img.nexgenmart.com/products/keyboard-008-main.jpg', 'MechType Pro keyboard top view', 0, 1, 1200, 600, 175, 'image/jpeg', '2024-01-12 10:30:00');
INSERT INTO product_images VALUES (11, 9, 'https://img.nexgenmart.com/products/mouse-009-main.jpg', 'ErgoGlide Mouse ergonomic view', 0, 1, 800, 800, 130, 'image/jpeg', '2024-01-13 10:30:00');
INSERT INTO product_images VALUES (12, 10, 'https://img.nexgenmart.com/products/monitor-010-main.jpg', 'UltraView 27 monitor front', 0, 1, 1400, 900, 280, 'image/jpeg', '2024-01-14 10:30:00');
INSERT INTO product_images VALUES (13, 11, 'https://img.nexgenmart.com/products/charger-011-main.jpg', 'PowerHub 6-Port charger', 0, 1, 800, 800, 120, 'image/jpeg', '2024-01-15 10:30:00');
INSERT INTO product_images VALUES (14, 12, 'https://img.nexgenmart.com/products/earbuds-012-main.jpg', 'AudioMax Buds Pro in case', 0, 1, 800, 800, 140, 'image/jpeg', '2024-01-16 10:30:00');
INSERT INTO product_images VALUES (15, 13, 'https://img.nexgenmart.com/products/blender-013-main.jpg', 'HomeStyle Blender X', 0, 1, 800, 1200, 200, 'image/jpeg', '2024-01-17 10:30:00');
INSERT INTO product_images VALUES (16, 14, 'https://img.nexgenmart.com/products/lamp-014-main.jpg', 'DeskGlow LED Lamp on desk', 0, 1, 1000, 1000, 160, 'image/jpeg', '2024-01-18 10:30:00');
INSERT INTO product_images VALUES (17, 15, 'https://img.nexgenmart.com/products/mug-015-main.jpg', 'ThermoSip Travel Mug navy', 0, 1, 800, 1000, 110, 'image/jpeg', '2024-01-19 10:30:00');
INSERT INTO product_images VALUES (18, 15, 'https://img.nexgenmart.com/products/mug-015-red.jpg', 'ThermoSip Travel Mug red', 1, 0, 800, 1000, 112, 'image/jpeg', '2024-01-19 10:31:00');

-- TABLE 11: tags (10 rows)
CREATE TABLE tags (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    slug TEXT NOT NULL UNIQUE,
    description TEXT,
    usage_count INTEGER NOT NULL DEFAULT 0,
    is_trending INTEGER NOT NULL DEFAULT 0,
    color TEXT,
    created_by_id INTEGER REFERENCES users(id),
    created_at TEXT NOT NULL,
    is_active INTEGER NOT NULL DEFAULT 1
);
INSERT INTO tags VALUES (1, 'Best Seller', 'best-seller', 'Top selling products', 5, 1, '#FF5733', 1, '2024-01-10 08:00:00', 1);
INSERT INTO tags VALUES (2, 'New Arrival', 'new-arrival', 'Recently added products', 4, 1, '#33FF57', 1, '2024-01-10 08:00:00', 1);
INSERT INTO tags VALUES (3, 'Premium', 'premium', 'High-end premium products', 3, 0, '#3357FF', 1, '2024-01-10 08:00:00', 1);
INSERT INTO tags VALUES (4, 'Eco-Friendly', 'eco-friendly', 'Environmentally conscious products', 2, 0, '#57FF33', 3, '2024-01-15 09:00:00', 1);
INSERT INTO tags VALUES (5, 'Limited Edition', 'limited-edition', 'Limited availability items', 2, 1, '#FF33A1', 5, '2024-02-01 10:00:00', 1);
INSERT INTO tags VALUES (6, 'Gift Idea', 'gift-idea', 'Great gift options', 3, 0, '#FFD700', 7, '2024-02-10 11:00:00', 1);
INSERT INTO tags VALUES (7, 'Budget Pick', 'budget-pick', 'Affordable quality choices', 3, 0, '#00CED1', 9, '2024-03-01 08:00:00', 1);
INSERT INTO tags VALUES (8, 'Work From Home', 'work-from-home', 'Essential WFH gear', 2, 1, '#8A2BE2', 11, '2024-03-10 09:00:00', 1);
INSERT INTO tags VALUES (9, 'Travel Essential', 'travel-essential', 'Must-have travel items', 1, 0, '#FF6347', 5, '2024-03-15 10:00:00', 1);
INSERT INTO tags VALUES (10, 'Clearance', 'clearance', 'Items on clearance sale', 0, 0, '#DC143C', 1, '2024-04-01 08:00:00', 1);

-- TABLE 12: product_tags (25 rows junction)
CREATE TABLE product_tags (
    id INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(id),
    tag_id INTEGER NOT NULL REFERENCES tags(id),
    added_by_id INTEGER REFERENCES users(id),
    added_at TEXT NOT NULL,
    is_auto_tagged INTEGER NOT NULL DEFAULT 0,
    weight REAL NOT NULL DEFAULT 1.0,
    source TEXT NOT NULL DEFAULT 'manual',
    relevance_score REAL,
    is_approved INTEGER NOT NULL DEFAULT 1
);
INSERT INTO product_tags VALUES (1, 1, 1, 1, '2024-02-01 10:00:00', 0, 1.0, 'manual', 0.95, 1);
INSERT INTO product_tags VALUES (2, 1, 3, 1, '2024-02-01 10:00:00', 0, 0.9, 'manual', 0.90, 1);
INSERT INTO product_tags VALUES (3, 1, 8, 11, '2024-03-10 09:30:00', 0, 0.8, 'manual', 0.85, 1);
INSERT INTO product_tags VALUES (4, 2, 1, 1, '2024-02-01 10:00:00', 0, 1.0, 'manual', 0.92, 1);
INSERT INTO product_tags VALUES (5, 2, 2, 1, '2024-02-01 10:00:00', 1, 1.0, 'algorithm', 0.88, 1);
INSERT INTO product_tags VALUES (6, 3, 1, 3, '2024-02-15 09:00:00', 0, 1.0, 'manual', 0.93, 1);
INSERT INTO product_tags VALUES (7, 3, 9, 5, '2024-03-15 10:00:00', 0, 0.7, 'manual', 0.80, 1);
INSERT INTO product_tags VALUES (8, 4, 2, 1, '2024-01-20 10:00:00', 1, 1.0, 'algorithm', 0.87, 1);
INSERT INTO product_tags VALUES (9, 5, 2, 1, '2024-01-25 10:00:00', 1, 1.0, 'algorithm', 0.89, 1);
INSERT INTO product_tags VALUES (10, 5, 4, 3, '2024-02-10 09:00:00', 0, 0.8, 'manual', 0.75, 1);
INSERT INTO product_tags VALUES (11, 6, 6, 7, '2024-02-10 11:00:00', 0, 0.9, 'manual', 0.85, 1);
INSERT INTO product_tags VALUES (12, 6, 7, 9, '2024-03-01 08:30:00', 0, 1.0, 'manual', 0.90, 1);
INSERT INTO product_tags VALUES (13, 7, 3, 1, '2024-02-01 10:00:00', 0, 1.0, 'manual', 0.95, 1);
INSERT INTO product_tags VALUES (14, 7, 5, 5, '2024-02-01 10:00:00', 0, 0.9, 'manual', 0.88, 1);
INSERT INTO product_tags VALUES (15, 8, 1, 1, '2024-03-01 08:00:00', 0, 1.0, 'manual', 0.91, 1);
INSERT INTO product_tags VALUES (16, 8, 8, 11, '2024-03-10 09:30:00', 0, 0.9, 'manual', 0.87, 1);
INSERT INTO product_tags VALUES (17, 9, 7, 9, '2024-03-01 08:30:00', 0, 1.0, 'manual', 0.93, 1);
INSERT INTO product_tags VALUES (18, 10, 3, 1, '2024-02-01 10:00:00', 0, 0.9, 'manual', 0.88, 1);
INSERT INTO product_tags VALUES (19, 10, 8, 11, '2024-03-10 09:30:00', 0, 0.8, 'manual', 0.82, 1);
INSERT INTO product_tags VALUES (20, 11, 7, 9, '2024-03-01 08:30:00', 0, 1.0, 'manual', 0.94, 1);
INSERT INTO product_tags VALUES (21, 12, 2, 1, '2024-01-20 10:00:00', 1, 1.0, 'algorithm', 0.86, 1);
INSERT INTO product_tags VALUES (22, 13, 6, 7, '2024-02-10 11:00:00', 0, 0.8, 'manual', 0.80, 1);
INSERT INTO product_tags VALUES (23, 14, 7, 9, '2024-03-01 08:30:00', 0, 1.0, 'manual', 0.92, 1);
INSERT INTO product_tags VALUES (24, 15, 6, 7, '2024-02-10 11:00:00', 0, 0.9, 'manual', 0.88, 1);
INSERT INTO product_tags VALUES (25, 15, 9, 5, '2024-03-15 10:00:00', 0, 0.8, 'manual', 0.82, 1);

-- TABLE 13: product_attributes (20 rows)
CREATE TABLE product_attributes (
    id INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(id),
    attribute_name TEXT NOT NULL,
    attribute_value TEXT NOT NULL,
    attribute_type TEXT NOT NULL DEFAULT 'text',
    sort_order INTEGER NOT NULL DEFAULT 0,
    is_filterable INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL
);
INSERT INTO product_attributes VALUES (1, 1, 'Processor', 'Intel Core i7-13700H', 'text', 1, 1, '2024-01-05 10:00:00');
INSERT INTO product_attributes VALUES (2, 1, 'RAM', '16GB DDR5', 'text', 2, 1, '2024-01-05 10:00:00');
INSERT INTO product_attributes VALUES (3, 1, 'Storage', '512GB NVMe SSD', 'text', 3, 1, '2024-01-05 10:00:00');
INSERT INTO product_attributes VALUES (4, 2, 'Screen Size', '6.7 inches', 'text', 1, 1, '2024-01-06 10:00:00');
INSERT INTO product_attributes VALUES (5, 2, 'Battery', '5000 mAh', 'text', 2, 0, '2024-01-06 10:00:00');
INSERT INTO product_attributes VALUES (6, 3, 'Driver Size', '40mm', 'text', 1, 0, '2024-01-07 10:00:00');
INSERT INTO product_attributes VALUES (7, 3, 'Battery Life', '30 hours', 'text', 2, 1, '2024-01-07 10:00:00');
INSERT INTO product_attributes VALUES (8, 4, 'Screen Size', '10.9 inches', 'text', 1, 1, '2024-01-08 10:00:00');
INSERT INTO product_attributes VALUES (9, 5, 'Water Resistance', 'IP68', 'text', 1, 1, '2024-01-09 10:00:00');
INSERT INTO product_attributes VALUES (10, 5, 'Battery Life', '14 days', 'text', 2, 1, '2024-01-09 10:00:00');
INSERT INTO product_attributes VALUES (11, 6, 'Bluetooth Version', '5.3', 'text', 1, 0, '2024-01-10 10:00:00');
INSERT INTO product_attributes VALUES (12, 7, 'Megapixels', '24.2 MP', 'text', 1, 1, '2024-01-11 10:00:00');
INSERT INTO product_attributes VALUES (13, 7, 'ISO Range', '100-51200', 'text', 2, 0, '2024-01-11 10:00:00');
INSERT INTO product_attributes VALUES (14, 8, 'Switch Type', 'Cherry MX', 'text', 1, 1, '2024-01-12 10:00:00');
INSERT INTO product_attributes VALUES (15, 9, 'DPI', '16000', 'number', 1, 1, '2024-01-13 10:00:00');
INSERT INTO product_attributes VALUES (16, 10, 'Resolution', '3840x2160', 'text', 1, 1, '2024-01-14 10:00:00');
INSERT INTO product_attributes VALUES (17, 10, 'Refresh Rate', '60Hz', 'text', 2, 1, '2024-01-14 10:00:00');
INSERT INTO product_attributes VALUES (18, 13, 'Wattage', '1200W', 'text', 1, 0, '2024-01-17 10:00:00');
INSERT INTO product_attributes VALUES (19, 14, 'Brightness', '800 lumens', 'text', 1, 0, '2024-01-18 10:00:00');
INSERT INTO product_attributes VALUES (20, 15, 'Capacity', '16 oz', 'text', 1, 1, '2024-01-19 10:00:00');

-- TABLE 14: product_price_history (15 rows)
CREATE TABLE product_price_history (
    id INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(id),
    old_price REAL NOT NULL,
    new_price REAL NOT NULL,
    changed_at TEXT NOT NULL,
    changed_by TEXT NOT NULL DEFAULT 'system',
    reason TEXT
);
INSERT INTO product_price_history VALUES (1, 1, 1099.99, 999.99, '2024-03-01 08:00:00', 'admin', 'Price reduction for spring sale');
INSERT INTO product_price_history VALUES (2, 2, 849.99, 799.99, '2024-03-15 08:00:00', 'admin', 'Competitive pricing adjustment');
INSERT INTO product_price_history VALUES (3, 3, 279.99, 249.99, '2024-04-01 08:00:00', 'system', 'Promotional pricing');
INSERT INTO product_price_history VALUES (4, 4, 549.99, 499.99, '2024-04-10 08:00:00', 'admin', 'New model incoming');
INSERT INTO product_price_history VALUES (5, 5, 399.99, 349.99, '2024-05-01 08:00:00', 'system', 'Summer sale');
INSERT INTO product_price_history VALUES (6, 6, 169.99, 149.99, '2024-05-15 08:00:00', 'admin', 'Volume discount rollout');
INSERT INTO product_price_history VALUES (7, 7, 1399.99, 1299.99, '2024-06-01 08:00:00', 'admin', 'Anniversary sale');
INSERT INTO product_price_history VALUES (8, 8, 149.99, 129.99, '2024-04-15 08:00:00', 'system', 'Market adjustment');
INSERT INTO product_price_history VALUES (9, 9, 69.99, 59.99, '2024-03-20 08:00:00', 'admin', 'Clearance prep');
INSERT INTO product_price_history VALUES (10, 10, 499.99, 449.99, '2024-06-15 08:00:00', 'system', 'Mid-year sale');
INSERT INTO product_price_history VALUES (11, 11, 59.99, 49.99, '2024-05-01 08:00:00', 'admin', 'Bundle pricing');
INSERT INTO product_price_history VALUES (12, 12, 199.99, 179.99, '2024-06-01 08:00:00', 'system', 'Competitive match');
INSERT INTO product_price_history VALUES (13, 13, 99.99, 89.99, '2024-04-20 08:00:00', 'admin', 'Spring promo');
INSERT INTO product_price_history VALUES (14, 14, 44.99, 39.99, '2024-03-25 08:00:00', 'system', 'New pricing tier');
INSERT INTO product_price_history VALUES (15, 15, 29.99, 24.99, '2024-05-05 08:00:00', 'admin', 'Everyday low price');

-- ============================================================
-- GROUP 3: Order Domain
-- ============================================================

-- TABLE 15: orders (20 rows)
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    shipping_address_id INTEGER NOT NULL REFERENCES user_addresses(id),
    billing_address_id INTEGER REFERENCES user_addresses(id),
    order_date TEXT NOT NULL,
    status TEXT NOT NULL,
    subtotal REAL NOT NULL,
    tax_amount REAL NOT NULL DEFAULT 0.0,
    shipping_cost REAL NOT NULL DEFAULT 0.0,
    discount_amount REAL NOT NULL DEFAULT 0.0,
    total_amount REAL NOT NULL,
    notes TEXT
);
INSERT INTO orders VALUES (1, 1, 1, 2, '2024-02-01 10:00:00', 'delivered', 999.99, 80.00, 0.00, 0.00, 1079.99, NULL);
INSERT INTO orders VALUES (2, 1, 1, 2, '2024-03-15 14:30:00', 'delivered', 249.99, 20.00, 5.99, 0.00, 275.98, NULL);
INSERT INTO orders VALUES (3, 1, 1, NULL, '2024-06-15 09:00:00', 'delivered', 1299.99, 104.00, 0.00, 0.00, 1403.99, 'Gift wrap requested');
INSERT INTO orders VALUES (4, 2, 3, NULL, '2024-02-10 11:30:00', 'delivered', 799.99, 64.00, 0.00, 0.00, 863.99, NULL);
INSERT INTO orders VALUES (5, 2, 3, NULL, '2024-05-20 14:00:00', 'delivered', 499.99, 40.00, 9.99, 0.00, 549.98, NULL);
INSERT INTO orders VALUES (6, 3, 4, NULL, '2024-02-15 09:45:00', 'delivered', 449.99, 36.00, 5.99, 0.00, 491.98, NULL);
INSERT INTO orders VALUES (7, 3, 4, NULL, '2024-07-01 10:30:00', 'shipped', 429.99, 34.40, 0.00, 25.00, 439.39, 'Applied loyalty discount');
INSERT INTO orders VALUES (8, 4, 5, NULL, '2024-03-01 08:00:00', 'delivered', 999.99, 80.00, 0.00, 0.00, 1079.99, NULL);
INSERT INTO orders VALUES (9, 4, 5, NULL, '2024-06-20 16:00:00', 'delivered', 649.99, 52.00, 9.99, 0.00, 711.98, NULL);
INSERT INTO orders VALUES (10, 5, 6, 7, '2024-03-10 10:15:00', 'delivered', 179.99, 14.40, 5.99, 0.00, 200.38, NULL);
INSERT INTO orders VALUES (11, 5, 6, NULL, '2024-07-10 11:45:00', 'processing', 279.99, 22.40, 0.00, 20.00, 282.39, 'First-time discount applied');
INSERT INTO orders VALUES (12, 6, 8, NULL, '2024-03-15 14:30:00', 'delivered', 749.99, 60.00, 0.00, 0.00, 809.99, NULL);
INSERT INTO orders VALUES (13, 6, 8, NULL, '2024-08-01 09:00:00', 'delivered', 349.99, 28.00, 5.99, 0.00, 383.98, NULL);
INSERT INTO orders VALUES (14, 7, 9, NULL, '2024-04-01 08:45:00', 'delivered', 749.99, 60.00, 0.00, 50.00, 759.99, 'Birthday promotion');
INSERT INTO orders VALUES (15, 8, 10, NULL, '2024-04-10 10:00:00', 'delivered', 129.99, 10.40, 5.99, 0.00, 146.38, NULL);
INSERT INTO orders VALUES (16, 8, 10, NULL, '2024-08-15 13:30:00', 'returned', 269.99, 21.60, 5.99, 0.00, 297.58, 'Wrong size ordered');
INSERT INTO orders VALUES (17, 9, 11, 12, '2024-04-20 09:30:00', 'delivered', 149.99, 12.00, 5.99, 0.00, 167.98, NULL);
INSERT INTO orders VALUES (18, 10, 13, NULL, '2024-05-01 11:00:00', 'delivered', 999.99, 80.00, 0.00, 0.00, 1079.99, NULL);
INSERT INTO orders VALUES (19, 11, 14, NULL, '2024-05-10 08:30:00', 'shipped', 329.99, 26.40, 5.99, 0.00, 362.38, NULL);
INSERT INTO orders VALUES (20, 12, 15, 16, '2024-05-15 14:00:00', 'processing', 199.99, 16.00, 5.99, 10.00, 211.98, 'Coupon applied');

-- TABLE 16: order_items (35 rows)
CREATE TABLE order_items (
    id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id),
    product_id INTEGER NOT NULL REFERENCES products(id),
    variant_id INTEGER REFERENCES product_variants(id),
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    subtotal REAL NOT NULL,
    discount_amount REAL NOT NULL DEFAULT 0.0,
    tax_amount REAL NOT NULL DEFAULT 0.0,
    status TEXT NOT NULL DEFAULT 'confirmed'
);
INSERT INTO order_items VALUES (1, 1, 1, 1, 1, 999.99, 999.99, 0.00, 80.00, 'delivered');
INSERT INTO order_items VALUES (2, 2, 3, 5, 1, 249.99, 249.99, 0.00, 20.00, 'delivered');
INSERT INTO order_items VALUES (3, 3, 7, 13, 1, 1299.99, 1299.99, 0.00, 104.00, 'delivered');
INSERT INTO order_items VALUES (4, 4, 2, 3, 1, 799.99, 799.99, 0.00, 64.00, 'delivered');
INSERT INTO order_items VALUES (5, 5, 4, 7, 1, 499.99, 499.99, 0.00, 40.00, 'delivered');
INSERT INTO order_items VALUES (6, 6, 10, 17, 1, 449.99, 449.99, 0.00, 36.00, 'delivered');
INSERT INTO order_items VALUES (7, 7, 5, 9, 1, 349.99, 349.99, 0.00, 28.00, 'shipped');
INSERT INTO order_items VALUES (8, 7, 9, NULL, 1, 59.99, 59.99, 0.00, 4.80, 'shipped');
INSERT INTO order_items VALUES (9, 7, 15, 19, 1, 24.99, 24.99, 0.00, 2.00, 'shipped');
INSERT INTO order_items VALUES (10, 8, 1, 2, 1, 1199.99, 1199.99, 0.00, 96.00, 'delivered');
INSERT INTO order_items VALUES (11, 9, 5, 10, 1, 349.99, 349.99, 0.00, 28.00, 'delivered');
INSERT INTO order_items VALUES (12, 9, 6, 11, 1, 149.99, 149.99, 0.00, 12.00, 'delivered');
INSERT INTO order_items VALUES (13, 9, 15, 20, 1, 24.99, 24.99, 0.00, 2.00, 'delivered');
INSERT INTO order_items VALUES (14, 10, 12, 18, 1, 179.99, 179.99, 0.00, 14.40, 'delivered');
INSERT INTO order_items VALUES (15, 11, 3, 6, 1, 249.99, 249.99, 0.00, 20.00, 'processing');
INSERT INTO order_items VALUES (16, 11, 14, NULL, 1, 39.99, 39.99, 0.00, 3.20, 'processing');
INSERT INTO order_items VALUES (17, 12, 1, 1, 1, 999.99, 999.99, 0.00, 80.00, 'delivered');
INSERT INTO order_items VALUES (18, 12, 6, 12, 1, 149.99, 149.99, 0.00, 12.00, 'delivered');
INSERT INTO order_items VALUES (19, 13, 5, 9, 1, 349.99, 349.99, 0.00, 28.00, 'delivered');
INSERT INTO order_items VALUES (20, 14, 4, 8, 1, 579.99, 579.99, 0.00, 46.40, 'delivered');
INSERT INTO order_items VALUES (21, 14, 6, 11, 1, 149.99, 149.99, 0.00, 12.00, 'delivered');
INSERT INTO order_items VALUES (22, 15, 8, 15, 1, 129.99, 129.99, 0.00, 10.40, 'delivered');
INSERT INTO order_items VALUES (23, 16, 3, 5, 1, 249.99, 249.99, 0.00, 20.00, 'returned');
INSERT INTO order_items VALUES (24, 16, 15, 19, 1, 24.99, 24.99, 0.00, 2.00, 'delivered');
INSERT INTO order_items VALUES (25, 17, 6, 12, 1, 149.99, 149.99, 0.00, 12.00, 'delivered');
INSERT INTO order_items VALUES (26, 18, 1, 1, 1, 999.99, 999.99, 0.00, 80.00, 'delivered');
INSERT INTO order_items VALUES (27, 19, 5, 10, 1, 349.99, 349.99, 0.00, 28.00, 'shipped');
INSERT INTO order_items VALUES (28, 20, 12, 18, 1, 179.99, 179.99, 0.00, 14.40, 'processing');
INSERT INTO order_items VALUES (29, 20, 15, 20, 1, 24.99, 24.99, 0.00, 2.00, 'processing');
INSERT INTO order_items VALUES (30, 8, 11, NULL, 1, 49.99, 49.99, 0.00, 4.00, 'delivered');
INSERT INTO order_items VALUES (31, 9, 8, 16, 1, 129.99, 129.99, 0.00, 10.40, 'delivered');
INSERT INTO order_items VALUES (32, 12, 14, NULL, 2, 39.99, 79.98, 0.00, 6.40, 'delivered');
INSERT INTO order_items VALUES (33, 13, 11, NULL, 2, 49.99, 99.98, 0.00, 8.00, 'delivered');
INSERT INTO order_items VALUES (34, 14, 9, NULL, 1, 59.99, 59.99, 0.00, 4.80, 'delivered');
INSERT INTO order_items VALUES (35, 19, 14, NULL, 1, 39.99, 39.99, 0.00, 3.20, 'shipped');

-- TABLE 17: order_status_history (30 rows)
CREATE TABLE order_status_history (
    id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id),
    from_status TEXT,
    to_status TEXT NOT NULL,
    changed_at TEXT NOT NULL,
    changed_by TEXT NOT NULL DEFAULT 'system',
    notes TEXT
);
INSERT INTO order_status_history VALUES (1, 1, NULL, 'pending', '2024-02-01 10:00:00', 'system', 'Order placed');
INSERT INTO order_status_history VALUES (2, 1, 'pending', 'processing', '2024-02-01 10:05:00', 'system', 'Payment confirmed');
INSERT INTO order_status_history VALUES (3, 1, 'processing', 'shipped', '2024-02-02 08:00:00', 'warehouse', 'Shipped from East Hub');
INSERT INTO order_status_history VALUES (4, 1, 'shipped', 'delivered', '2024-02-05 14:30:00', 'carrier', 'Delivered to door');
INSERT INTO order_status_history VALUES (5, 2, NULL, 'pending', '2024-03-15 14:30:00', 'system', 'Order placed');
INSERT INTO order_status_history VALUES (6, 2, 'pending', 'processing', '2024-03-15 14:35:00', 'system', 'Payment confirmed');
INSERT INTO order_status_history VALUES (7, 2, 'processing', 'shipped', '2024-03-16 09:00:00', 'warehouse', 'Shipped from Central Depot');
INSERT INTO order_status_history VALUES (8, 2, 'shipped', 'delivered', '2024-03-19 11:00:00', 'carrier', 'Delivered');
INSERT INTO order_status_history VALUES (9, 3, NULL, 'pending', '2024-06-15 09:00:00', 'system', 'Order placed');
INSERT INTO order_status_history VALUES (10, 3, 'pending', 'delivered', '2024-06-20 16:00:00', 'system', 'Express delivery');
INSERT INTO order_status_history VALUES (11, 4, NULL, 'pending', '2024-02-10 11:30:00', 'system', 'Order placed');
INSERT INTO order_status_history VALUES (12, 4, 'pending', 'delivered', '2024-02-15 10:00:00', 'carrier', 'Delivered');
INSERT INTO order_status_history VALUES (13, 5, NULL, 'pending', '2024-05-20 14:00:00', 'system', 'Order placed');
INSERT INTO order_status_history VALUES (14, 5, 'pending', 'delivered', '2024-05-25 12:00:00', 'carrier', 'Delivered');
INSERT INTO order_status_history VALUES (15, 6, NULL, 'pending', '2024-02-15 09:45:00', 'system', 'Order placed');
INSERT INTO order_status_history VALUES (16, 6, 'pending', 'delivered', '2024-02-20 14:00:00', 'carrier', 'Delivered');
INSERT INTO order_status_history VALUES (17, 7, NULL, 'pending', '2024-07-01 10:30:00', 'system', 'Order placed');
INSERT INTO order_status_history VALUES (18, 7, 'pending', 'shipped', '2024-07-02 08:00:00', 'warehouse', 'Shipped');
INSERT INTO order_status_history VALUES (19, 8, NULL, 'pending', '2024-03-01 08:00:00', 'system', 'Order placed');
INSERT INTO order_status_history VALUES (20, 8, 'pending', 'delivered', '2024-03-06 15:00:00', 'carrier', 'Delivered');
INSERT INTO order_status_history VALUES (21, 9, NULL, 'pending', '2024-06-20 16:00:00', 'system', 'Order placed');
INSERT INTO order_status_history VALUES (22, 9, 'pending', 'delivered', '2024-06-25 11:00:00', 'carrier', 'Delivered');
INSERT INTO order_status_history VALUES (23, 10, NULL, 'pending', '2024-03-10 10:15:00', 'system', 'Order placed');
INSERT INTO order_status_history VALUES (24, 10, 'pending', 'delivered', '2024-03-14 13:00:00', 'carrier', 'Delivered');
INSERT INTO order_status_history VALUES (25, 11, NULL, 'pending', '2024-07-10 11:45:00', 'system', 'Order placed');
INSERT INTO order_status_history VALUES (26, 11, 'pending', 'processing', '2024-07-10 12:00:00', 'system', 'Payment confirmed');
INSERT INTO order_status_history VALUES (27, 16, NULL, 'pending', '2024-08-15 13:30:00', 'system', 'Order placed');
INSERT INTO order_status_history VALUES (28, 16, 'pending', 'delivered', '2024-08-20 10:00:00', 'carrier', 'Delivered');
INSERT INTO order_status_history VALUES (29, 16, 'delivered', 'returned', '2024-08-25 09:00:00', 'customer', 'Return initiated');
INSERT INTO order_status_history VALUES (30, 20, NULL, 'pending', '2024-05-15 14:00:00', 'system', 'Order placed');

-- ============================================================
-- GROUP 4: Payment Domain
-- ============================================================

-- TABLE 18: payments (20 rows)
CREATE TABLE payments (
    id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id),
    user_id INTEGER NOT NULL REFERENCES users(id),
    amount REAL NOT NULL,
    payment_method TEXT NOT NULL,
    status TEXT NOT NULL,
    transaction_ref TEXT,
    gateway TEXT NOT NULL,
    processed_at TEXT NOT NULL,
    currency TEXT NOT NULL DEFAULT 'USD',
    processing_fee REAL NOT NULL DEFAULT 0.0
);
INSERT INTO payments VALUES (1, 1, 1, 1079.99, 'credit_card', 'completed', 'TXN-20240201-001', 'stripe', '2024-02-01 10:02:00', 'USD', 31.32);
INSERT INTO payments VALUES (2, 2, 1, 275.98, 'credit_card', 'completed', 'TXN-20240315-002', 'stripe', '2024-03-15 14:32:00', 'USD', 8.00);
INSERT INTO payments VALUES (3, 3, 1, 1403.99, 'credit_card', 'completed', 'TXN-20240615-003', 'stripe', '2024-06-15 09:03:00', 'USD', 40.72);
INSERT INTO payments VALUES (4, 4, 2, 863.99, 'debit_card', 'completed', 'TXN-20240210-004', 'stripe', '2024-02-10 11:32:00', 'USD', 25.06);
INSERT INTO payments VALUES (5, 5, 2, 549.98, 'credit_card', 'completed', 'TXN-20240520-005', 'stripe', '2024-05-20 14:02:00', 'USD', 15.95);
INSERT INTO payments VALUES (6, 6, 3, 491.98, 'paypal', 'completed', 'TXN-20240215-006', 'paypal', '2024-02-15 09:47:00', 'USD', 14.27);
INSERT INTO payments VALUES (7, 7, 3, 439.39, 'credit_card', 'completed', 'TXN-20240701-007', 'stripe', '2024-07-01 10:32:00', 'USD', 12.74);
INSERT INTO payments VALUES (8, 8, 4, 1079.99, 'credit_card', 'completed', 'TXN-20240301-008', 'stripe', '2024-03-01 08:02:00', 'USD', 31.32);
INSERT INTO payments VALUES (9, 9, 4, 711.98, 'debit_card', 'completed', 'TXN-20240620-009', 'stripe', '2024-06-20 16:02:00', 'USD', 20.65);
INSERT INTO payments VALUES (10, 10, 5, 200.38, 'paypal', 'completed', 'TXN-20240310-010', 'paypal', '2024-03-10 10:17:00', 'USD', 5.81);
INSERT INTO payments VALUES (11, 11, 5, 282.39, 'credit_card', 'pending', 'TXN-20240710-011', 'stripe', '2024-07-10 11:47:00', 'USD', 8.19);
INSERT INTO payments VALUES (12, 12, 6, 809.99, 'credit_card', 'completed', 'TXN-20240315-012', 'stripe', '2024-03-15 14:32:00', 'USD', 23.49);
INSERT INTO payments VALUES (13, 13, 6, 383.98, 'credit_card', 'completed', 'TXN-20240801-013', 'stripe', '2024-08-01 09:02:00', 'USD', 11.14);
INSERT INTO payments VALUES (14, 14, 7, 759.99, 'credit_card', 'completed', 'TXN-20240401-014', 'stripe', '2024-04-01 08:47:00', 'USD', 22.04);
INSERT INTO payments VALUES (15, 15, 8, 146.38, 'debit_card', 'completed', 'TXN-20240410-015', 'stripe', '2024-04-10 10:02:00', 'USD', 4.24);
INSERT INTO payments VALUES (16, 16, 8, 297.58, 'credit_card', 'refunded', 'TXN-20240815-016', 'stripe', '2024-08-15 13:32:00', 'USD', 8.63);
INSERT INTO payments VALUES (17, 17, 9, 167.98, 'paypal', 'completed', 'TXN-20240420-017', 'paypal', '2024-04-20 09:32:00', 'USD', 4.87);
INSERT INTO payments VALUES (18, 18, 10, 1079.99, 'credit_card', 'completed', 'TXN-20240501-018', 'stripe', '2024-05-01 11:02:00', 'USD', 31.32);
INSERT INTO payments VALUES (19, 19, 11, 362.38, 'credit_card', 'completed', 'TXN-20240510-019', 'stripe', '2024-05-10 08:32:00', 'USD', 10.51);
INSERT INTO payments VALUES (20, 20, 12, 211.98, 'debit_card', 'pending', 'TXN-20240515-020', 'stripe', '2024-05-15 14:02:00', 'USD', 6.15);

-- TABLE 19: refunds (6 rows)
CREATE TABLE refunds (
    id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id),
    payment_id INTEGER NOT NULL REFERENCES payments(id),
    user_id INTEGER NOT NULL REFERENCES users(id),
    amount REAL NOT NULL,
    reason TEXT NOT NULL,
    status TEXT NOT NULL,
    refund_method TEXT NOT NULL,
    requested_at TEXT NOT NULL,
    processed_at TEXT,
    processed_by TEXT,
    notes TEXT
);
INSERT INTO refunds VALUES (1, 16, 16, 8, 249.99, 'Wrong size - headphones too tight', 'completed', 'original_payment', '2024-08-25 09:00:00', '2024-08-27 10:00:00', 'Agent Smith', 'Full refund for returned headphones');
INSERT INTO refunds VALUES (2, 7, 7, 3, 25.00, 'Late delivery compensation', 'completed', 'store_credit', '2024-07-05 10:00:00', '2024-07-06 09:00:00', 'Agent Jones', 'Partial credit for delay');
INSERT INTO refunds VALUES (3, 9, 9, 4, 24.99, 'Defective mug lid', 'completed', 'original_payment', '2024-07-01 08:00:00', '2024-07-03 11:00:00', 'Agent Davis', 'Refund for defective item');
INSERT INTO refunds VALUES (4, 14, 14, 7, 50.00, 'Birthday promo overcharge', 'completed', 'original_payment', '2024-04-05 10:00:00', '2024-04-06 09:00:00', 'Agent Wilson', 'Price adjustment refund');
INSERT INTO refunds VALUES (5, 12, 12, 6, 39.99, 'Lamp arrived damaged', 'processing', 'original_payment', '2024-04-01 14:00:00', NULL, NULL, 'Awaiting inspection');
INSERT INTO refunds VALUES (6, 5, 5, 2, 49.99, 'Changed mind on tablet case', 'completed', 'store_credit', '2024-06-01 10:00:00', '2024-06-02 09:00:00', 'Agent Smith', 'Store credit issued');

-- TABLE 20: gift_cards (5 rows)
CREATE TABLE gift_cards (
    id INTEGER PRIMARY KEY,
    code TEXT NOT NULL UNIQUE,
    balance REAL NOT NULL,
    initial_amount REAL NOT NULL,
    purchaser_id INTEGER REFERENCES users(id),
    recipient_email TEXT,
    message TEXT,
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL,
    expires_at TEXT,
    last_used_at TEXT
);
INSERT INTO gift_cards VALUES (1, 'GC-NEXGEN-1001', 50.00, 50.00, 1, 'friend@email.com', 'Happy Birthday!', 1, '2024-02-14 10:00:00', '2025-02-14 10:00:00', NULL);
INSERT INTO gift_cards VALUES (2, 'GC-NEXGEN-1002', 25.00, 100.00, 3, 'carol.friend@email.com', 'Enjoy shopping!', 1, '2024-03-01 09:00:00', '2025-03-01 09:00:00', '2024-06-15 14:00:00');
INSERT INTO gift_cards VALUES (3, 'GC-NEXGEN-1003', 75.00, 75.00, 5, 'eve.sister@email.com', 'For you!', 1, '2024-04-10 11:00:00', '2025-04-10 11:00:00', NULL);
INSERT INTO gift_cards VALUES (4, 'GC-NEXGEN-1004', 0.00, 25.00, 7, 'grace.mom@email.com', 'Mothers Day gift', 0, '2024-05-01 08:00:00', '2025-05-01 08:00:00', '2024-07-20 10:00:00');
INSERT INTO gift_cards VALUES (5, 'GC-NEXGEN-1005', 200.00, 200.00, 10, NULL, NULL, 1, '2024-06-01 10:00:00', '2025-06-01 10:00:00', NULL);

-- TABLE 21: gift_card_transactions (8 rows)
CREATE TABLE gift_card_transactions (
    id INTEGER PRIMARY KEY,
    gift_card_id INTEGER NOT NULL REFERENCES gift_cards(id),
    order_id INTEGER REFERENCES orders(id),
    amount REAL NOT NULL,
    transaction_type TEXT NOT NULL,
    created_at TEXT NOT NULL,
    notes TEXT
);
INSERT INTO gift_card_transactions VALUES (1, 1, NULL, 50.00, 'purchase', '2024-02-14 10:00:00', 'Gift card purchased');
INSERT INTO gift_card_transactions VALUES (2, 2, NULL, 100.00, 'purchase', '2024-03-01 09:00:00', 'Gift card purchased');
INSERT INTO gift_card_transactions VALUES (3, 2, 7, -25.00, 'redemption', '2024-06-15 14:00:00', 'Applied to order #7');
INSERT INTO gift_card_transactions VALUES (4, 2, 14, -50.00, 'redemption', '2024-07-10 10:00:00', 'Applied to order #14');
INSERT INTO gift_card_transactions VALUES (5, 3, NULL, 75.00, 'purchase', '2024-04-10 11:00:00', 'Gift card purchased');
INSERT INTO gift_card_transactions VALUES (6, 4, NULL, 25.00, 'purchase', '2024-05-01 08:00:00', 'Gift card purchased');
INSERT INTO gift_card_transactions VALUES (7, 4, 17, -25.00, 'redemption', '2024-07-20 10:00:00', 'Applied to order #17');
INSERT INTO gift_card_transactions VALUES (8, 5, NULL, 200.00, 'purchase', '2024-06-01 10:00:00', 'Corporate gift card');

-- ============================================================
-- GROUP 5: Inventory Domain
-- ============================================================

-- TABLE 22: warehouses (4 rows)
CREATE TABLE warehouses (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    code TEXT NOT NULL UNIQUE,
    address TEXT NOT NULL,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    postal_code TEXT NOT NULL,
    country TEXT NOT NULL DEFAULT 'US',
    manager_email TEXT,
    phone TEXT,
    capacity INTEGER,
    is_active INTEGER NOT NULL DEFAULT 1
);
INSERT INTO warehouses VALUES (1, 'East Hub', 'WH-EAST', '500 Industrial Pkwy', 'Newark', 'NJ', '07102', 'US', 'mgr.east@nexgenmart.com', '201-555-0001', 50000, 1);
INSERT INTO warehouses VALUES (2, 'West Hub', 'WH-WEST', '800 Commerce Dr', 'Ontario', 'CA', '91761', 'US', 'mgr.west@nexgenmart.com', '909-555-0002', 60000, 1);
INSERT INTO warehouses VALUES (3, 'Central Depot', 'WH-CENTRAL', '300 Logistics Blvd', 'Dallas', 'TX', '75247', 'US', 'mgr.central@nexgenmart.com', '214-555-0003', 75000, 1);
INSERT INTO warehouses VALUES (4, 'South Center', 'WH-SOUTH', '200 Distribution Way', 'Atlanta', 'GA', '30301', 'US', 'mgr.south@nexgenmart.com', '404-555-0004', 40000, 1);

-- TABLE 23: inventory_levels (15 rows)
CREATE TABLE inventory_levels (
    id INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(id),
    warehouse_id INTEGER NOT NULL REFERENCES warehouses(id),
    quantity INTEGER NOT NULL DEFAULT 0,
    reserved INTEGER NOT NULL DEFAULT 0,
    available INTEGER NOT NULL DEFAULT 0,
    reorder_point INTEGER NOT NULL DEFAULT 10,
    reorder_quantity INTEGER NOT NULL DEFAULT 50,
    last_restocked_at TEXT,
    last_sold_at TEXT,
    unit_cost REAL
);
INSERT INTO inventory_levels VALUES (1, 1, 1, 30, 5, 25, 10, 50, '2024-06-01 08:00:00', '2024-11-15 10:00:00', 650.00);
INSERT INTO inventory_levels VALUES (2, 2, 1, 45, 3, 42, 15, 60, '2024-05-15 08:00:00', '2024-11-20 09:00:00', 450.00);
INSERT INTO inventory_levels VALUES (3, 3, 2, 60, 8, 52, 20, 80, '2024-06-10 08:00:00', '2024-11-18 11:00:00', 120.00);
INSERT INTO inventory_levels VALUES (4, 4, 2, 25, 2, 23, 10, 40, '2024-06-20 08:00:00', '2024-11-10 14:00:00', 280.00);
INSERT INTO inventory_levels VALUES (5, 5, 3, 70, 10, 60, 20, 100, '2024-07-01 08:00:00', '2024-11-22 10:00:00', 180.00);
INSERT INTO inventory_levels VALUES (6, 6, 3, 40, 5, 35, 15, 60, '2024-05-20 08:00:00', '2024-11-05 09:00:00', 65.00);
INSERT INTO inventory_levels VALUES (7, 7, 1, 15, 2, 13, 5, 20, '2024-06-15 08:00:00', '2024-10-20 11:00:00', 750.00);
INSERT INTO inventory_levels VALUES (8, 8, 4, 35, 3, 32, 10, 50, '2024-04-10 08:00:00', '2024-11-01 10:00:00', 55.00);
INSERT INTO inventory_levels VALUES (9, 9, 4, 80, 5, 75, 25, 100, '2024-03-25 08:00:00', '2024-11-12 09:00:00', 22.00);
INSERT INTO inventory_levels VALUES (10, 10, 2, 18, 1, 17, 8, 30, '2024-07-05 08:00:00', '2024-10-25 14:00:00', 280.00);
INSERT INTO inventory_levels VALUES (11, 11, 3, 100, 10, 90, 30, 150, '2024-05-01 08:00:00', '2024-11-20 10:00:00', 18.00);
INSERT INTO inventory_levels VALUES (12, 12, 1, 55, 7, 48, 20, 80, '2024-06-20 08:00:00', '2024-11-18 11:00:00', 75.00);
INSERT INTO inventory_levels VALUES (13, 13, 4, 50, 4, 46, 15, 60, '2024-04-15 08:00:00', '2024-10-30 09:00:00', 40.00);
INSERT INTO inventory_levels VALUES (14, 14, 3, 65, 6, 59, 20, 80, '2024-03-30 08:00:00', '2024-11-08 10:00:00', 15.00);
INSERT INTO inventory_levels VALUES (15, 15, 4, 120, 15, 105, 30, 150, '2024-05-10 08:00:00', '2024-11-25 09:00:00', 8.00);

-- TABLE 24: vendors (5 rows)
CREATE TABLE vendors (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    contact_person TEXT,
    email TEXT UNIQUE,
    phone TEXT,
    address TEXT,
    city TEXT,
    country TEXT,
    payment_terms TEXT,
    lead_time_days INTEGER NOT NULL DEFAULT 14,
    quality_rating REAL,
    is_active INTEGER NOT NULL DEFAULT 1
);
INSERT INTO vendors VALUES (1, 'TechSupply Co', 'John Baker', 'john@techsupply.com', '800-555-1001', '100 Tech Park Dr', 'San Jose', 'US', 'Net 30', 7, 4.5, 1);
INSERT INTO vendors VALUES (2, 'GlobalParts Ltd', 'Maria Gonzalez', 'maria@globalparts.com', '800-555-1002', '50 Import Blvd', 'Shenzhen', 'CN', 'Net 45', 21, 4.2, 1);
INSERT INTO vendors VALUES (3, 'HomeGoods Direct', 'Sarah Lee', 'sarah@homegoods.com', '800-555-1003', '75 Consumer Way', 'Chicago', 'US', 'Net 30', 10, 4.0, 1);
INSERT INTO vendors VALUES (4, 'AudioTech Inc', 'David Park', 'david@audiotech.com', '800-555-1004', '200 Sound Ave', 'Tokyo', 'JP', 'Net 60', 28, 4.7, 1);
INSERT INTO vendors VALUES (5, 'OfficePro Supply', 'Linda White', 'linda@officepro.com', '800-555-1005', '30 Office Park', 'Austin', 'US', 'Net 15', 5, 4.3, 1);

-- TABLE 25: vendor_products (15 rows junction)
CREATE TABLE vendor_products (
    id INTEGER PRIMARY KEY,
    vendor_id INTEGER NOT NULL REFERENCES vendors(id),
    product_id INTEGER NOT NULL REFERENCES products(id),
    unit_cost REAL NOT NULL,
    lead_time_days INTEGER NOT NULL,
    is_preferred INTEGER NOT NULL DEFAULT 0,
    min_order_quantity INTEGER NOT NULL DEFAULT 1
);
INSERT INTO vendor_products VALUES (1, 1, 1, 650.00, 7, 1, 5);
INSERT INTO vendor_products VALUES (2, 1, 2, 450.00, 7, 1, 10);
INSERT INTO vendor_products VALUES (3, 1, 4, 280.00, 7, 1, 5);
INSERT INTO vendor_products VALUES (4, 1, 10, 280.00, 10, 0, 5);
INSERT INTO vendor_products VALUES (5, 1, 11, 18.00, 5, 1, 50);
INSERT INTO vendor_products VALUES (6, 2, 2, 430.00, 21, 0, 20);
INSERT INTO vendor_products VALUES (7, 2, 5, 180.00, 21, 1, 15);
INSERT INTO vendor_products VALUES (8, 2, 10, 260.00, 25, 1, 10);
INSERT INTO vendor_products VALUES (9, 3, 13, 40.00, 10, 1, 20);
INSERT INTO vendor_products VALUES (10, 3, 15, 8.00, 10, 1, 50);
INSERT INTO vendor_products VALUES (11, 4, 3, 120.00, 28, 1, 10);
INSERT INTO vendor_products VALUES (12, 4, 6, 65.00, 28, 1, 15);
INSERT INTO vendor_products VALUES (13, 4, 12, 75.00, 28, 1, 10);
INSERT INTO vendor_products VALUES (14, 5, 8, 55.00, 5, 1, 10);
INSERT INTO vendor_products VALUES (15, 5, 9, 22.00, 5, 1, 20);

-- TABLE 26: purchase_orders (12 rows)
CREATE TABLE purchase_orders (
    id INTEGER PRIMARY KEY,
    vendor_id INTEGER NOT NULL REFERENCES vendors(id),
    status TEXT NOT NULL,
    ordered_date TEXT NOT NULL,
    expected_date TEXT,
    received_date TEXT,
    warehouse_id INTEGER NOT NULL REFERENCES warehouses(id),
    total_cost REAL NOT NULL,
    notes TEXT
);
INSERT INTO purchase_orders VALUES (1, 1, 'received', '2024-01-15 10:00:00', '2024-01-22 10:00:00', '2024-01-21 09:00:00', 1, 32500.00, 'Initial laptop stock');
INSERT INTO purchase_orders VALUES (2, 1, 'received', '2024-01-20 10:00:00', '2024-01-27 10:00:00', '2024-01-26 14:00:00', 1, 22500.00, 'Phone restock');
INSERT INTO purchase_orders VALUES (3, 2, 'received', '2024-02-01 10:00:00', '2024-02-22 10:00:00', '2024-02-20 11:00:00', 3, 18000.00, 'Watch bulk order');
INSERT INTO purchase_orders VALUES (4, 4, 'received', '2024-02-10 10:00:00', '2024-03-10 10:00:00', '2024-03-08 09:00:00', 2, 9600.00, 'Headphones and speakers');
INSERT INTO purchase_orders VALUES (5, 3, 'received', '2024-02-15 10:00:00', '2024-02-25 10:00:00', '2024-02-24 10:00:00', 4, 2800.00, 'Blender and mug stock');
INSERT INTO purchase_orders VALUES (6, 5, 'received', '2024-03-01 10:00:00', '2024-03-06 10:00:00', '2024-03-05 15:00:00', 4, 1990.00, 'Keyboard and mouse restock');
INSERT INTO purchase_orders VALUES (7, 1, 'received', '2024-04-01 10:00:00', '2024-04-08 10:00:00', '2024-04-07 09:00:00', 2, 14000.00, 'Tablet restock');
INSERT INTO purchase_orders VALUES (8, 2, 'received', '2024-05-01 10:00:00', '2024-05-22 10:00:00', '2024-05-21 11:00:00', 2, 7800.00, 'Monitor restock');
INSERT INTO purchase_orders VALUES (9, 4, 'shipped', '2024-06-01 10:00:00', '2024-06-29 10:00:00', NULL, 1, 7500.00, 'Earbuds restock');
INSERT INTO purchase_orders VALUES (10, 3, 'received', '2024-06-15 10:00:00', '2024-06-25 10:00:00', '2024-06-24 14:00:00', 4, 1200.00, 'Travel mug restock');
INSERT INTO purchase_orders VALUES (11, 5, 'ordered', '2024-07-01 10:00:00', '2024-07-06 10:00:00', NULL, 3, 2200.00, 'Office supplies restock');
INSERT INTO purchase_orders VALUES (12, 1, 'ordered', '2024-07-15 10:00:00', '2024-07-22 10:00:00', NULL, 1, 9000.00, 'Charger bulk order');

-- TABLE 27: purchase_order_lines (12 rows)
CREATE TABLE purchase_order_lines (
    id INTEGER PRIMARY KEY,
    purchase_order_id INTEGER NOT NULL REFERENCES purchase_orders(id),
    product_id INTEGER NOT NULL REFERENCES products(id),
    quantity INTEGER NOT NULL,
    unit_cost REAL NOT NULL,
    total_cost REAL NOT NULL
);
INSERT INTO purchase_order_lines VALUES (1, 1, 1, 50, 650.00, 32500.00);
INSERT INTO purchase_order_lines VALUES (2, 2, 2, 50, 450.00, 22500.00);
INSERT INTO purchase_order_lines VALUES (3, 3, 5, 100, 180.00, 18000.00);
INSERT INTO purchase_order_lines VALUES (4, 4, 3, 80, 120.00, 9600.00);
INSERT INTO purchase_order_lines VALUES (5, 5, 13, 40, 40.00, 1600.00);
INSERT INTO purchase_order_lines VALUES (6, 5, 15, 150, 8.00, 1200.00);
INSERT INTO purchase_order_lines VALUES (7, 6, 8, 25, 55.00, 1375.00);
INSERT INTO purchase_order_lines VALUES (8, 6, 9, 28, 22.00, 616.00);
INSERT INTO purchase_order_lines VALUES (9, 7, 4, 50, 280.00, 14000.00);
INSERT INTO purchase_order_lines VALUES (10, 8, 10, 30, 260.00, 7800.00);
INSERT INTO purchase_order_lines VALUES (11, 9, 12, 100, 75.00, 7500.00);
INSERT INTO purchase_order_lines VALUES (12, 10, 15, 150, 8.00, 1200.00);

-- TABLE 28: inventory_movements (18 rows)
CREATE TABLE inventory_movements (
    id INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(id),
    warehouse_id INTEGER NOT NULL REFERENCES warehouses(id),
    movement_type TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    reference_id TEXT,
    notes TEXT,
    performed_by TEXT,
    created_at TEXT NOT NULL,
    unit_cost REAL
);
INSERT INTO inventory_movements VALUES (1, 1, 1, 'inbound', 50, 'PO-1', 'Initial stock from TechSupply', 'warehouse_mgr', '2024-01-21 09:00:00', 650.00);
INSERT INTO inventory_movements VALUES (2, 2, 1, 'inbound', 50, 'PO-2', 'Phone stock from TechSupply', 'warehouse_mgr', '2024-01-26 14:00:00', 450.00);
INSERT INTO inventory_movements VALUES (3, 5, 3, 'inbound', 100, 'PO-3', 'Watch bulk from GlobalParts', 'warehouse_mgr', '2024-02-20 11:00:00', 180.00);
INSERT INTO inventory_movements VALUES (4, 3, 2, 'inbound', 80, 'PO-4', 'Headphones from AudioTech', 'warehouse_mgr', '2024-03-08 09:00:00', 120.00);
INSERT INTO inventory_movements VALUES (5, 1, 1, 'outbound', -1, 'ORD-1', 'Sold to customer', 'system', '2024-02-01 10:30:00', 650.00);
INSERT INTO inventory_movements VALUES (6, 2, 1, 'outbound', -1, 'ORD-4', 'Sold to customer', 'system', '2024-02-10 12:00:00', 450.00);
INSERT INTO inventory_movements VALUES (7, 3, 2, 'outbound', -1, 'ORD-2', 'Sold to customer', 'system', '2024-03-15 15:00:00', 120.00);
INSERT INTO inventory_movements VALUES (8, 13, 4, 'inbound', 40, 'PO-5', 'Blender stock from HomeGoods', 'warehouse_mgr', '2024-02-24 10:00:00', 40.00);
INSERT INTO inventory_movements VALUES (9, 15, 4, 'inbound', 150, 'PO-5', 'Mug stock from HomeGoods', 'warehouse_mgr', '2024-02-24 10:30:00', 8.00);
INSERT INTO inventory_movements VALUES (10, 8, 4, 'inbound', 25, 'PO-6', 'Keyboard stock from OfficePro', 'warehouse_mgr', '2024-03-05 15:00:00', 55.00);
INSERT INTO inventory_movements VALUES (11, 9, 4, 'inbound', 28, 'PO-6', 'Mouse stock from OfficePro', 'warehouse_mgr', '2024-03-05 15:30:00', 22.00);
INSERT INTO inventory_movements VALUES (12, 4, 2, 'inbound', 50, 'PO-7', 'Tablet restock from TechSupply', 'warehouse_mgr', '2024-04-07 09:00:00', 280.00);
INSERT INTO inventory_movements VALUES (13, 10, 2, 'inbound', 30, 'PO-8', 'Monitor restock from GlobalParts', 'warehouse_mgr', '2024-05-21 11:00:00', 260.00);
INSERT INTO inventory_movements VALUES (14, 1, 1, 'outbound', -1, 'ORD-8', 'Sold to customer', 'system', '2024-03-01 08:30:00', 650.00);
INSERT INTO inventory_movements VALUES (15, 7, 1, 'outbound', -1, 'ORD-3', 'Sold to customer', 'system', '2024-06-15 09:30:00', 750.00);
INSERT INTO inventory_movements VALUES (16, 15, 4, 'inbound', 150, 'PO-10', 'Mug restock from HomeGoods', 'warehouse_mgr', '2024-06-24 14:00:00', 8.00);
INSERT INTO inventory_movements VALUES (17, 3, 2, 'return_inbound', 1, 'RET-1', 'Customer return - headphones', 'warehouse_mgr', '2024-08-28 10:00:00', 120.00);
INSERT INTO inventory_movements VALUES (18, 1, 1, 'transfer_out', -5, 'XFER-001', 'Transfer to West Hub', 'warehouse_mgr', '2024-04-15 09:00:00', 650.00);

-- ============================================================
-- GROUP 6: Shipping Domain
-- ============================================================

-- TABLE 29: shipping_carriers (4 rows)
CREATE TABLE shipping_carriers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    code TEXT NOT NULL UNIQUE,
    website_url TEXT,
    phone TEXT,
    tracking_url_template TEXT,
    is_active INTEGER NOT NULL DEFAULT 1,
    avg_delivery_days INTEGER,
    quality_rating REAL,
    contact_email TEXT
);
INSERT INTO shipping_carriers VALUES (1, 'FastShip Express', 'FSE', 'https://fastship.example.com', '800-555-2001', 'https://fastship.example.com/track/{tracking}', 1, 3, 4.5, 'support@fastship.example.com');
INSERT INTO shipping_carriers VALUES (2, 'EcoFreight', 'ECO', 'https://ecofreight.example.com', '800-555-2002', 'https://ecofreight.example.com/track/{tracking}', 1, 5, 4.2, 'help@ecofreight.example.com');
INSERT INTO shipping_carriers VALUES (3, 'PrimeLogistics', 'PRL', 'https://primelogistics.example.com', '800-555-2003', 'https://primelogistics.example.com/track/{tracking}', 1, 2, 4.8, 'cs@primelogistics.example.com');
INSERT INTO shipping_carriers VALUES (4, 'BudgetShip', 'BGS', 'https://budgetship.example.com', '800-555-2004', 'https://budgetship.example.com/track/{tracking}', 1, 7, 3.9, 'info@budgetship.example.com');

-- TABLE 30: delivery_zones (8 rows)
CREATE TABLE delivery_zones (
    id INTEGER PRIMARY KEY,
    zone_name TEXT NOT NULL,
    states_covered TEXT NOT NULL,
    base_rate REAL NOT NULL,
    per_kg_rate REAL NOT NULL,
    min_delivery_days INTEGER NOT NULL,
    max_delivery_days INTEGER NOT NULL,
    is_active INTEGER NOT NULL DEFAULT 1,
    free_shipping_threshold REAL
);
INSERT INTO delivery_zones VALUES (1, 'Northeast', 'NY,NJ,CT,MA,PA,NH,VT,ME,RI', 5.99, 1.50, 2, 5, 1, 75.00);
INSERT INTO delivery_zones VALUES (2, 'Southeast', 'FL,GA,NC,SC,VA,AL,TN,MS,LA', 6.99, 1.75, 3, 6, 1, 100.00);
INSERT INTO delivery_zones VALUES (3, 'Midwest', 'IL,OH,MI,IN,WI,MN,MO,IA,KS', 7.99, 2.00, 3, 7, 1, 100.00);
INSERT INTO delivery_zones VALUES (4, 'Southwest', 'TX,AZ,NM,OK,AR', 6.99, 1.75, 3, 6, 1, 100.00);
INSERT INTO delivery_zones VALUES (5, 'West Coast', 'CA,OR,WA,NV', 5.99, 1.50, 2, 5, 1, 75.00);
INSERT INTO delivery_zones VALUES (6, 'Mountain', 'CO,UT,MT,WY,ID', 8.99, 2.25, 4, 8, 1, 125.00);
INSERT INTO delivery_zones VALUES (7, 'Plains', 'NE,SD,ND', 9.99, 2.50, 4, 8, 1, 150.00);
INSERT INTO delivery_zones VALUES (8, 'Hawaii & Alaska', 'HI,AK', 14.99, 3.50, 7, 14, 1, 200.00);

-- TABLE 31: zone_carrier_rates (8 rows junction)
CREATE TABLE zone_carrier_rates (
    id INTEGER PRIMARY KEY,
    zone_id INTEGER NOT NULL REFERENCES delivery_zones(id),
    carrier_id INTEGER NOT NULL REFERENCES shipping_carriers(id),
    rate_multiplier REAL NOT NULL DEFAULT 1.0,
    is_active INTEGER NOT NULL DEFAULT 1
);
INSERT INTO zone_carrier_rates VALUES (1, 1, 1, 1.0, 1);
INSERT INTO zone_carrier_rates VALUES (2, 1, 3, 1.5, 1);
INSERT INTO zone_carrier_rates VALUES (3, 2, 2, 1.0, 1);
INSERT INTO zone_carrier_rates VALUES (4, 3, 4, 0.85, 1);
INSERT INTO zone_carrier_rates VALUES (5, 4, 1, 1.1, 1);
INSERT INTO zone_carrier_rates VALUES (6, 5, 3, 1.2, 1);
INSERT INTO zone_carrier_rates VALUES (7, 6, 2, 1.3, 1);
INSERT INTO zone_carrier_rates VALUES (8, 8, 1, 2.0, 1);

-- TABLE 32: shipments (18 rows)
CREATE TABLE shipments (
    id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id),
    carrier_id INTEGER NOT NULL REFERENCES shipping_carriers(id),
    tracking_number TEXT,
    status TEXT NOT NULL,
    shipped_at TEXT,
    estimated_delivery_at TEXT,
    actual_delivery_at TEXT,
    weight_kg REAL,
    cost REAL NOT NULL,
    requires_signature INTEGER NOT NULL DEFAULT 0
);
INSERT INTO shipments VALUES (1, 1, 3, 'PRL-100001', 'delivered', '2024-02-02 08:00:00', '2024-02-04 18:00:00', '2024-02-05 14:30:00', 2.1, 0.00, 1);
INSERT INTO shipments VALUES (2, 2, 1, 'FSE-200001', 'delivered', '2024-03-16 09:00:00', '2024-03-19 18:00:00', '2024-03-19 11:00:00', 0.25, 5.99, 0);
INSERT INTO shipments VALUES (3, 3, 3, 'PRL-100002', 'delivered', '2024-06-16 08:00:00', '2024-06-18 18:00:00', '2024-06-20 16:00:00', 0.85, 0.00, 1);
INSERT INTO shipments VALUES (4, 4, 2, 'ECO-300001', 'delivered', '2024-02-11 09:00:00', '2024-02-16 18:00:00', '2024-02-15 10:00:00', 0.18, 0.00, 0);
INSERT INTO shipments VALUES (5, 5, 1, 'FSE-200002', 'delivered', '2024-05-21 08:00:00', '2024-05-24 18:00:00', '2024-05-25 12:00:00', 0.45, 9.99, 0);
INSERT INTO shipments VALUES (6, 6, 4, 'BGS-400001', 'delivered', '2024-02-16 10:00:00', '2024-02-23 18:00:00', '2024-02-20 14:00:00', 5.5, 5.99, 0);
INSERT INTO shipments VALUES (7, 7, 1, 'FSE-200003', 'in_transit', '2024-07-02 08:00:00', '2024-07-05 18:00:00', NULL, 0.5, 0.00, 0);
INSERT INTO shipments VALUES (8, 8, 3, 'PRL-100003', 'delivered', '2024-03-02 08:00:00', '2024-03-04 18:00:00', '2024-03-06 15:00:00', 2.4, 0.00, 1);
INSERT INTO shipments VALUES (9, 9, 2, 'ECO-300002', 'delivered', '2024-06-21 09:00:00', '2024-06-26 18:00:00', '2024-06-25 11:00:00', 1.3, 9.99, 0);
INSERT INTO shipments VALUES (10, 10, 1, 'FSE-200004', 'delivered', '2024-03-11 08:00:00', '2024-03-14 18:00:00', '2024-03-14 13:00:00', 0.06, 5.99, 0);
INSERT INTO shipments VALUES (11, 12, 3, 'PRL-100004', 'delivered', '2024-03-16 08:00:00', '2024-03-18 18:00:00', '2024-03-18 14:00:00', 3.5, 0.00, 1);
INSERT INTO shipments VALUES (12, 13, 2, 'ECO-300003', 'delivered', '2024-08-02 09:00:00', '2024-08-07 18:00:00', '2024-08-06 10:00:00', 0.35, 5.99, 0);
INSERT INTO shipments VALUES (13, 14, 1, 'FSE-200005', 'delivered', '2024-04-02 08:00:00', '2024-04-05 18:00:00', '2024-04-04 15:00:00', 1.35, 0.00, 0);
INSERT INTO shipments VALUES (14, 15, 4, 'BGS-400002', 'delivered', '2024-04-11 10:00:00', '2024-04-18 18:00:00', '2024-04-16 11:00:00', 0.95, 5.99, 0);
INSERT INTO shipments VALUES (15, 16, 2, 'ECO-300004', 'returned', '2024-08-16 09:00:00', '2024-08-21 18:00:00', '2024-08-20 10:00:00', 0.6, 5.99, 0);
INSERT INTO shipments VALUES (16, 17, 4, 'BGS-400003', 'delivered', '2024-04-21 10:00:00', '2024-04-28 18:00:00', '2024-04-26 14:00:00', 0.8, 5.99, 0);
INSERT INTO shipments VALUES (17, 18, 3, 'PRL-100005', 'delivered', '2024-05-02 08:00:00', '2024-05-04 18:00:00', '2024-05-04 10:00:00', 2.1, 0.00, 1);
INSERT INTO shipments VALUES (18, 19, 1, 'FSE-200006', 'in_transit', '2024-05-11 08:00:00', '2024-05-14 18:00:00', NULL, 0.65, 5.99, 0);

-- TABLE 33: shipment_items (35 rows)
CREATE TABLE shipment_items (
    id INTEGER PRIMARY KEY,
    shipment_id INTEGER NOT NULL REFERENCES shipments(id),
    order_item_id INTEGER NOT NULL REFERENCES order_items(id),
    quantity INTEGER NOT NULL
);
INSERT INTO shipment_items VALUES (1, 1, 1, 1);
INSERT INTO shipment_items VALUES (2, 2, 2, 1);
INSERT INTO shipment_items VALUES (3, 3, 3, 1);
INSERT INTO shipment_items VALUES (4, 4, 4, 1);
INSERT INTO shipment_items VALUES (5, 5, 5, 1);
INSERT INTO shipment_items VALUES (6, 6, 6, 1);
INSERT INTO shipment_items VALUES (7, 7, 7, 1);
INSERT INTO shipment_items VALUES (8, 7, 8, 1);
INSERT INTO shipment_items VALUES (9, 7, 9, 1);
INSERT INTO shipment_items VALUES (10, 8, 10, 1);
INSERT INTO shipment_items VALUES (11, 8, 30, 1);
INSERT INTO shipment_items VALUES (12, 9, 11, 1);
INSERT INTO shipment_items VALUES (13, 9, 12, 1);
INSERT INTO shipment_items VALUES (14, 9, 13, 1);
INSERT INTO shipment_items VALUES (15, 9, 31, 1);
INSERT INTO shipment_items VALUES (16, 10, 14, 1);
INSERT INTO shipment_items VALUES (17, 11, 17, 1);
INSERT INTO shipment_items VALUES (18, 11, 18, 1);
INSERT INTO shipment_items VALUES (19, 11, 32, 2);
INSERT INTO shipment_items VALUES (20, 12, 19, 1);
INSERT INTO shipment_items VALUES (21, 12, 33, 2);
INSERT INTO shipment_items VALUES (22, 13, 20, 1);
INSERT INTO shipment_items VALUES (23, 13, 21, 1);
INSERT INTO shipment_items VALUES (24, 13, 34, 1);
INSERT INTO shipment_items VALUES (25, 14, 22, 1);
INSERT INTO shipment_items VALUES (26, 15, 23, 1);
INSERT INTO shipment_items VALUES (27, 15, 24, 1);
INSERT INTO shipment_items VALUES (28, 16, 25, 1);
INSERT INTO shipment_items VALUES (29, 17, 26, 1);
INSERT INTO shipment_items VALUES (30, 18, 27, 1);
INSERT INTO shipment_items VALUES (31, 18, 35, 1);
INSERT INTO shipment_items VALUES (32, 10, 15, 1);
INSERT INTO shipment_items VALUES (33, 10, 16, 1);
INSERT INTO shipment_items VALUES (34, 6, 6, 1);
INSERT INTO shipment_items VALUES (35, 16, 25, 1);

-- TABLE 34: return_requests (8 rows)
CREATE TABLE return_requests (
    id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id),
    user_id INTEGER NOT NULL REFERENCES users(id),
    reason TEXT NOT NULL,
    status TEXT NOT NULL,
    requested_at TEXT NOT NULL,
    approved_at TEXT,
    refund_amount REAL,
    refund_method TEXT,
    handled_by INTEGER REFERENCES users(id),
    notes TEXT
);
INSERT INTO return_requests VALUES (1, 16, 8, 'Wrong size headphones', 'approved', '2024-08-25 09:00:00', '2024-08-26 10:00:00', 249.99, 'original_payment', 1, 'Headphones returned in original packaging');
INSERT INTO return_requests VALUES (2, 7, 3, 'Late delivery', 'approved', '2024-07-05 10:00:00', '2024-07-05 14:00:00', 25.00, 'store_credit', 3, 'Partial credit for delay');
INSERT INTO return_requests VALUES (3, 9, 4, 'Defective mug lid', 'approved', '2024-07-01 08:00:00', '2024-07-02 09:00:00', 24.99, 'original_payment', 5, 'Replacement offered');
INSERT INTO return_requests VALUES (4, 14, 7, 'Overcharged', 'approved', '2024-04-05 10:00:00', '2024-04-05 15:00:00', 50.00, 'original_payment', 7, 'Price adjustment');
INSERT INTO return_requests VALUES (5, 12, 6, 'Damaged lamp on arrival', 'pending', '2024-04-01 14:00:00', NULL, 39.99, 'original_payment', NULL, 'Photos submitted');
INSERT INTO return_requests VALUES (6, 5, 2, 'Changed mind', 'approved', '2024-06-01 10:00:00', '2024-06-01 16:00:00', 49.99, 'store_credit', 9, 'No restocking fee');
INSERT INTO return_requests VALUES (7, 13, 6, 'Product not as described', 'denied', '2024-08-10 09:00:00', NULL, NULL, NULL, 11, 'Product matches listing');
INSERT INTO return_requests VALUES (8, 19, 11, 'Duplicate order', 'pending', '2024-05-12 08:00:00', NULL, 362.38, 'original_payment', NULL, 'Investigating');

-- TABLE 35: return_items (10 rows)
CREATE TABLE return_items (
    id INTEGER PRIMARY KEY,
    return_request_id INTEGER NOT NULL REFERENCES return_requests(id),
    order_item_id INTEGER NOT NULL REFERENCES order_items(id),
    quantity INTEGER NOT NULL,
    reason TEXT NOT NULL,
    condition TEXT NOT NULL DEFAULT 'unopened'
);
INSERT INTO return_items VALUES (1, 1, 23, 1, 'Wrong size headphones', 'opened');
INSERT INTO return_items VALUES (2, 2, 7, 1, 'Late delivery compensation', 'kept');
INSERT INTO return_items VALUES (3, 2, 8, 1, 'Late delivery compensation', 'kept');
INSERT INTO return_items VALUES (4, 3, 13, 1, 'Defective mug lid', 'defective');
INSERT INTO return_items VALUES (5, 4, 20, 1, 'Birthday promo overcharge', 'kept');
INSERT INTO return_items VALUES (6, 5, 32, 1, 'Lamp arrived damaged', 'damaged');
INSERT INTO return_items VALUES (7, 6, 5, 1, 'Changed mind on tablet', 'unopened');
INSERT INTO return_items VALUES (8, 7, 19, 1, 'Product not as described', 'opened');
INSERT INTO return_items VALUES (9, 8, 27, 1, 'Duplicate order - watch', 'unopened');
INSERT INTO return_items VALUES (10, 8, 35, 1, 'Duplicate order - lamp', 'unopened');

-- ============================================================
-- GROUP 7: Marketing Domain
-- ============================================================

-- TABLE 36: discount_codes (6 rows)
CREATE TABLE discount_codes (
    id INTEGER PRIMARY KEY,
    code TEXT NOT NULL UNIQUE,
    description TEXT,
    discount_type TEXT NOT NULL,
    discount_value REAL NOT NULL,
    minimum_order REAL,
    max_redemptions INTEGER,
    times_redeemed INTEGER NOT NULL DEFAULT 0,
    valid_from TEXT NOT NULL,
    valid_until TEXT,
    is_active INTEGER NOT NULL DEFAULT 1,
    created_by TEXT
);
INSERT INTO discount_codes VALUES (1, 'WELCOME10', 'Welcome discount for new customers', 'percentage', 10.0, 50.00, 1000, 85, '2024-01-01 00:00:00', '2024-12-31 23:59:59', 1, 'marketing_team');
INSERT INTO discount_codes VALUES (2, 'SUMMER25', 'Summer sale - $25 off', 'fixed', 25.00, 100.00, 500, 120, '2024-06-01 00:00:00', '2024-08-31 23:59:59', 0, 'marketing_team');
INSERT INTO discount_codes VALUES (3, 'FREESHIP', 'Free shipping on any order', 'free_shipping', 0.0, 0.00, NULL, 200, '2024-01-01 00:00:00', '2024-12-31 23:59:59', 1, 'marketing_team');
INSERT INTO discount_codes VALUES (4, 'VIP20', 'VIP customer 20% off', 'percentage', 20.0, 200.00, 100, 15, '2024-03-01 00:00:00', '2024-12-31 23:59:59', 1, 'admin');
INSERT INTO discount_codes VALUES (5, 'BIRTHDAY15', 'Birthday month 15% discount', 'percentage', 15.0, 25.00, NULL, 45, '2024-01-01 00:00:00', '2024-12-31 23:59:59', 1, 'admin');
INSERT INTO discount_codes VALUES (6, 'FLASH50', 'Flash sale - 50% off select items', 'percentage', 50.0, 0.00, 50, 50, '2024-07-04 00:00:00', '2024-07-04 23:59:59', 0, 'marketing_team');

-- TABLE 37: discount_redemptions (10 rows)
CREATE TABLE discount_redemptions (
    id INTEGER PRIMARY KEY,
    discount_code_id INTEGER NOT NULL REFERENCES discount_codes(id),
    user_id INTEGER NOT NULL REFERENCES users(id),
    order_id INTEGER NOT NULL REFERENCES orders(id),
    discount_applied REAL NOT NULL,
    redeemed_at TEXT NOT NULL,
    ip_address TEXT,
    user_agent TEXT,
    session_id TEXT,
    is_first_purchase INTEGER NOT NULL DEFAULT 0
);
INSERT INTO discount_redemptions VALUES (1, 1, 5, 11, 20.00, '2024-07-10 11:45:00', '192.168.1.50', 'Mozilla/5.0', 'sess_abc123', 1);
INSERT INTO discount_redemptions VALUES (2, 2, 3, 7, 25.00, '2024-07-01 10:30:00', '192.168.1.30', 'Chrome/120.0', 'sess_def456', 0);
INSERT INTO discount_redemptions VALUES (3, 5, 7, 14, 50.00, '2024-04-01 08:45:00', '192.168.1.70', 'Safari/17.0', 'sess_ghi789', 0);
INSERT INTO discount_redemptions VALUES (4, 1, 12, 20, 10.00, '2024-05-15 14:00:00', '192.168.1.120', 'Firefox/121.0', 'sess_jkl012', 1);
INSERT INTO discount_redemptions VALUES (5, 3, 1, 1, 0.00, '2024-02-01 10:00:00', '192.168.1.10', 'Chrome/119.0', 'sess_mno345', 0);
INSERT INTO discount_redemptions VALUES (6, 3, 4, 8, 0.00, '2024-03-01 08:00:00', '192.168.1.40', 'Safari/16.0', 'sess_pqr678', 0);
INSERT INTO discount_redemptions VALUES (7, 3, 10, 18, 0.00, '2024-05-01 11:00:00', '192.168.1.100', 'Chrome/120.0', 'sess_stu901', 0);
INSERT INTO discount_redemptions VALUES (8, 4, 1, 3, 0.00, '2024-06-15 09:00:00', '192.168.1.10', 'Chrome/121.0', 'sess_vwx234', 0);
INSERT INTO discount_redemptions VALUES (9, 2, 6, 13, 0.00, '2024-08-01 09:00:00', '192.168.1.60', 'Firefox/120.0', 'sess_yza567', 0);
INSERT INTO discount_redemptions VALUES (10, 1, 9, 17, 0.00, '2024-04-20 09:30:00', '192.168.1.90', 'Chrome/119.0', 'sess_bcd890', 1);

-- TABLE 38: marketing_campaigns (5 rows)
CREATE TABLE marketing_campaigns (
    id INTEGER PRIMARY KEY,
    campaign_name TEXT NOT NULL,
    description TEXT,
    campaign_type TEXT NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT,
    budget REAL,
    amount_spent REAL NOT NULL DEFAULT 0.0,
    status TEXT NOT NULL,
    target_audience TEXT,
    created_by TEXT
);
INSERT INTO marketing_campaigns VALUES (1, 'Spring Launch 2024', 'Spring product launch campaign', 'email', '2024-03-01 00:00:00', '2024-04-30 23:59:59', 5000.00, 3200.00, 'completed', 'all_users', 'marketing_team');
INSERT INTO marketing_campaigns VALUES (2, 'Summer Blowout', 'Major summer clearance event', 'multi_channel', '2024-06-01 00:00:00', '2024-08-31 23:59:59', 15000.00, 12500.00, 'completed', 'active_buyers', 'marketing_team');
INSERT INTO marketing_campaigns VALUES (3, 'Back to School', 'Back to school electronics sale', 'social_media', '2024-08-15 00:00:00', '2024-09-15 23:59:59', 8000.00, 4500.00, 'active', 'students_parents', 'marketing_team');
INSERT INTO marketing_campaigns VALUES (4, 'Holiday Preview', 'Early holiday shopping campaign', 'email', '2024-11-01 00:00:00', '2024-11-30 23:59:59', 10000.00, 0.00, 'planned', 'all_users', 'admin');
INSERT INTO marketing_campaigns VALUES (5, 'New Year Flash Sales', 'Flash sales for new year', 'push_notification', '2025-01-01 00:00:00', '2025-01-07 23:59:59', 3000.00, 0.00, 'planned', 'vip_customers', 'admin');

-- TABLE 39: campaign_discount_links (5 rows junction)
CREATE TABLE campaign_discount_links (
    id INTEGER PRIMARY KEY,
    campaign_id INTEGER NOT NULL REFERENCES marketing_campaigns(id),
    discount_code_id INTEGER NOT NULL REFERENCES discount_codes(id),
    created_at TEXT NOT NULL
);
INSERT INTO campaign_discount_links VALUES (1, 1, 1, '2024-03-01 00:00:00');
INSERT INTO campaign_discount_links VALUES (2, 2, 2, '2024-06-01 00:00:00');
INSERT INTO campaign_discount_links VALUES (3, 2, 6, '2024-07-01 00:00:00');
INSERT INTO campaign_discount_links VALUES (4, 3, 1, '2024-08-15 00:00:00');
INSERT INTO campaign_discount_links VALUES (5, 4, 4, '2024-11-01 00:00:00');

-- TABLE 40: saved_lists (12 rows)
CREATE TABLE saved_lists (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    name TEXT NOT NULL DEFAULT 'My Wishlist',
    is_public INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    updated_at TEXT
);
INSERT INTO saved_lists VALUES (1, 1, 'My Wishlist', 0, '2024-02-01 10:00:00', '2024-06-15 09:00:00');
INSERT INTO saved_lists VALUES (2, 2, 'Tech Wants', 1, '2024-02-10 11:30:00', '2024-05-20 14:00:00');
INSERT INTO saved_lists VALUES (3, 3, 'My Wishlist', 0, '2024-02-15 09:45:00', '2024-07-01 10:30:00');
INSERT INTO saved_lists VALUES (4, 4, 'Gaming Setup', 0, '2024-03-01 08:00:00', '2024-06-20 16:00:00');
INSERT INTO saved_lists VALUES (5, 5, 'Office Upgrade', 1, '2024-03-10 10:15:00', '2024-07-10 11:45:00');
INSERT INTO saved_lists VALUES (6, 6, 'My Wishlist', 0, '2024-03-15 14:30:00', '2024-08-01 09:00:00');
INSERT INTO saved_lists VALUES (7, 7, 'Gift Ideas', 1, '2024-04-01 08:45:00', '2024-04-01 08:45:00');
INSERT INTO saved_lists VALUES (8, 8, 'My Wishlist', 0, '2024-04-10 10:00:00', '2024-08-15 13:30:00');
INSERT INTO saved_lists VALUES (9, 9, 'Home Essentials', 0, '2024-04-20 09:30:00', '2024-04-20 09:30:00');
INSERT INTO saved_lists VALUES (10, 10, 'My Wishlist', 0, '2024-05-01 11:00:00', '2024-05-01 11:00:00');
INSERT INTO saved_lists VALUES (11, 11, 'Birthday List', 1, '2024-05-10 08:30:00', '2024-05-10 08:30:00');
INSERT INTO saved_lists VALUES (12, 12, 'My Wishlist', 0, '2024-05-15 14:00:00', '2024-05-15 14:00:00');

-- TABLE 41: saved_list_items (12 rows)
CREATE TABLE saved_list_items (
    id INTEGER PRIMARY KEY,
    saved_list_id INTEGER NOT NULL REFERENCES saved_lists(id),
    product_id INTEGER NOT NULL REFERENCES products(id),
    added_at TEXT NOT NULL,
    priority TEXT NOT NULL DEFAULT 'medium',
    notes TEXT,
    price_when_added REAL,
    notify_on_sale INTEGER NOT NULL DEFAULT 0
);
INSERT INTO saved_list_items VALUES (1, 1, 7, '2024-02-05 10:00:00', 'high', 'Want the kit version', 1299.99, 1);
INSERT INTO saved_list_items VALUES (2, 2, 1, '2024-02-15 09:00:00', 'high', 'Need for work', 999.99, 1);
INSERT INTO saved_list_items VALUES (3, 2, 10, '2024-03-01 10:00:00', 'medium', 'Dual monitor setup', 449.99, 0);
INSERT INTO saved_list_items VALUES (4, 3, 5, '2024-03-10 08:00:00', 'medium', NULL, 349.99, 1);
INSERT INTO saved_list_items VALUES (5, 4, 8, '2024-03-15 09:00:00', 'high', 'Cherry MX Blue', 129.99, 0);
INSERT INTO saved_list_items VALUES (6, 5, 14, '2024-04-01 10:00:00', 'low', 'For home office', 39.99, 0);
INSERT INTO saved_list_items VALUES (7, 6, 2, '2024-04-10 11:00:00', 'high', 'Upgrade from current phone', 799.99, 1);
INSERT INTO saved_list_items VALUES (8, 7, 15, '2024-04-15 09:00:00', 'medium', 'Gift for dad', 24.99, 0);
INSERT INTO saved_list_items VALUES (9, 7, 6, '2024-04-15 09:30:00', 'medium', 'Gift for mom', 149.99, 0);
INSERT INTO saved_list_items VALUES (10, 9, 13, '2024-05-01 10:00:00', 'high', 'Need a good blender', 89.99, 1);
INSERT INTO saved_list_items VALUES (11, 11, 3, '2024-05-15 08:00:00', 'high', 'Birthday present to self', 249.99, 1);
INSERT INTO saved_list_items VALUES (12, 12, 11, '2024-05-20 14:00:00', 'low', NULL, 49.99, 0);

-- TABLE 42: newsletter_subscribers (10 rows)
CREATE TABLE newsletter_subscribers (
    id INTEGER PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    user_id INTEGER REFERENCES users(id),
    subscribed_at TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'active',
    source TEXT,
    content_preferences TEXT,
    last_email_sent_at TEXT,
    open_rate REAL,
    bounce_count INTEGER NOT NULL DEFAULT 0
);
INSERT INTO newsletter_subscribers VALUES (1, 'alice@email.com', 1, '2024-01-10 08:00:00', 'active', 'registration', 'deals,new_products', '2024-11-01 09:00:00', 0.72, 0);
INSERT INTO newsletter_subscribers VALUES (2, 'bob@email.com', 2, '2024-01-12 09:15:00', 'active', 'registration', 'deals', '2024-11-01 09:00:00', 0.55, 0);
INSERT INTO newsletter_subscribers VALUES (3, 'carol@email.com', 3, '2024-01-15 11:30:00', 'active', 'registration', 'new_products,reviews', '2024-11-01 09:00:00', 0.68, 0);
INSERT INTO newsletter_subscribers VALUES (4, 'eve@email.com', 5, '2024-02-01 08:30:00', 'active', 'checkout', 'deals,new_products', '2024-11-01 09:00:00', 0.80, 0);
INSERT INTO newsletter_subscribers VALUES (5, 'grace@email.com', 7, '2024-02-10 09:45:00', 'active', 'registration', 'deals', '2024-11-01 09:00:00', 0.62, 0);
INSERT INTO newsletter_subscribers VALUES (6, 'henry@email.com', 8, '2024-02-15 10:20:00', 'active', 'popup', 'reviews,deals', '2024-11-01 09:00:00', 0.45, 1);
INSERT INTO newsletter_subscribers VALUES (7, 'ivy@email.com', 9, '2024-03-01 07:00:00', 'active', 'registration', 'new_products', '2024-11-01 09:00:00', 0.70, 0);
INSERT INTO newsletter_subscribers VALUES (8, 'kate@email.com', 11, '2024-03-10 08:50:00', 'active', 'registration', 'deals,new_products', '2024-11-01 09:00:00', 0.75, 0);
INSERT INTO newsletter_subscribers VALUES (9, 'leo@email.com', 12, '2024-03-15 11:25:00', 'active', 'checkout', 'deals', '2024-11-01 09:00:00', 0.50, 0);
INSERT INTO newsletter_subscribers VALUES (10, 'promo@example.com', NULL, '2024-04-01 10:00:00', 'unsubscribed', 'landing_page', 'deals', '2024-06-01 09:00:00', 0.10, 2);

-- ============================================================
-- GROUP 8: Support Domain
-- ============================================================

-- TABLE 43: support_agents (4 rows)
CREATE TABLE support_agents (
    id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT,
    department TEXT NOT NULL,
    role TEXT NOT NULL,
    is_active INTEGER NOT NULL DEFAULT 1,
    hire_date TEXT NOT NULL,
    skills TEXT,
    average_rating REAL
);
INSERT INTO support_agents VALUES (1, 'Agent Smith', 'smith@nexgenmart.com', '555-8001', 'Customer Service', 'senior_agent', 1, '2023-01-15', 'returns,billing,escalation', 4.7);
INSERT INTO support_agents VALUES (2, 'Agent Jones', 'jones@nexgenmart.com', '555-8002', 'Technical Support', 'agent', 1, '2023-06-01', 'tech_support,troubleshooting', 4.3);
INSERT INTO support_agents VALUES (3, 'Agent Davis', 'davis@nexgenmart.com', '555-8003', 'Customer Service', 'agent', 1, '2023-09-15', 'orders,shipping,complaints', 4.5);
INSERT INTO support_agents VALUES (4, 'Agent Wilson', 'wilson@nexgenmart.com', '555-8004', 'Billing', 'lead_agent', 1, '2022-11-01', 'billing,refunds,gift_cards', 4.8);

-- TABLE 44: support_tickets (10 rows)
CREATE TABLE support_tickets (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    assigned_agent_id INTEGER REFERENCES support_agents(id),
    subject TEXT NOT NULL,
    priority TEXT NOT NULL DEFAULT 'medium',
    status TEXT NOT NULL,
    channel TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT,
    resolved_at TEXT,
    satisfaction_score INTEGER
);
INSERT INTO support_tickets VALUES (1, 8, 1, 'Wrong headphones size received', 'high', 'resolved', 'email', '2024-08-25 09:00:00', '2024-08-27 10:00:00', '2024-08-27 10:00:00', 4);
INSERT INTO support_tickets VALUES (2, 3, 2, 'Late delivery on order #7', 'medium', 'resolved', 'chat', '2024-07-05 10:00:00', '2024-07-06 09:00:00', '2024-07-06 09:00:00', 3);
INSERT INTO support_tickets VALUES (3, 4, 3, 'Defective travel mug lid', 'medium', 'resolved', 'phone', '2024-07-01 08:00:00', '2024-07-03 11:00:00', '2024-07-03 11:00:00', 5);
INSERT INTO support_tickets VALUES (4, 7, 4, 'Birthday discount not applied correctly', 'high', 'resolved', 'email', '2024-04-05 10:00:00', '2024-04-06 09:00:00', '2024-04-06 09:00:00', 5);
INSERT INTO support_tickets VALUES (5, 6, 1, 'Lamp arrived damaged', 'high', 'open', 'email', '2024-04-01 14:00:00', '2024-04-02 09:00:00', NULL, NULL);
INSERT INTO support_tickets VALUES (6, 2, 3, 'Want to return tablet accessory', 'low', 'resolved', 'chat', '2024-06-01 10:00:00', '2024-06-02 09:00:00', '2024-06-02 09:00:00', 4);
INSERT INTO support_tickets VALUES (7, 5, 2, 'Question about bulk order pricing', 'medium', 'open', 'email', '2024-04-15 08:30:00', '2024-04-16 10:00:00', NULL, NULL);
INSERT INTO support_tickets VALUES (8, 11, 4, 'Account security verification', 'high', 'resolved', 'phone', '2024-06-01 09:00:00', '2024-06-01 09:45:00', '2024-06-01 09:45:00', 5);
INSERT INTO support_tickets VALUES (9, 6, 2, 'Product not as described', 'medium', 'closed', 'chat', '2024-08-10 09:00:00', '2024-08-12 10:00:00', '2024-08-12 10:00:00', 2);
INSERT INTO support_tickets VALUES (10, 11, 1, 'Duplicate order concern', 'high', 'open', 'email', '2024-05-12 08:00:00', '2024-05-13 09:00:00', NULL, NULL);

-- TABLE 45: ticket_messages (15 rows)
CREATE TABLE ticket_messages (
    id INTEGER PRIMARY KEY,
    ticket_id INTEGER NOT NULL REFERENCES support_tickets(id),
    sender_type TEXT NOT NULL,
    sender_id INTEGER NOT NULL,
    message_body TEXT NOT NULL,
    is_internal INTEGER NOT NULL DEFAULT 0,
    attachments TEXT,
    created_at TEXT NOT NULL,
    read_at TEXT,
    is_edited INTEGER NOT NULL DEFAULT 0
);
INSERT INTO ticket_messages VALUES (1, 1, 'customer', 8, 'I received headphones that are too tight. Order #16. Please help with a return.', 0, NULL, '2024-08-25 09:00:00', '2024-08-25 09:30:00', 0);
INSERT INTO ticket_messages VALUES (2, 1, 'agent', 1, 'I am sorry to hear that. I have initiated a return for you. Please ship them back within 14 days.', 0, NULL, '2024-08-25 09:35:00', '2024-08-25 10:00:00', 0);
INSERT INTO ticket_messages VALUES (3, 1, 'agent', 1, 'Internal note: Customer is a repeat buyer, expedite refund.', 1, NULL, '2024-08-25 09:36:00', NULL, 0);
INSERT INTO ticket_messages VALUES (4, 2, 'customer', 3, 'My order #7 was supposed to arrive by July 3 but it is still in transit.', 0, NULL, '2024-07-05 10:00:00', '2024-07-05 10:15:00', 0);
INSERT INTO ticket_messages VALUES (5, 2, 'agent', 2, 'I apologize for the delay. I have issued a $25 store credit to your account.', 0, NULL, '2024-07-05 10:20:00', '2024-07-05 11:00:00', 0);
INSERT INTO ticket_messages VALUES (6, 3, 'customer', 4, 'The lid on my travel mug from order #9 is cracked. It leaks.', 0, 'photo_lid.jpg', '2024-07-01 08:00:00', '2024-07-01 08:30:00', 0);
INSERT INTO ticket_messages VALUES (7, 3, 'agent', 3, 'Thank you for the photo. We will send a replacement mug right away.', 0, NULL, '2024-07-01 08:45:00', '2024-07-01 09:00:00', 0);
INSERT INTO ticket_messages VALUES (8, 4, 'customer', 7, 'I was told I would get 15% off for my birthday but I was charged full price on order #14.', 0, NULL, '2024-04-05 10:00:00', '2024-04-05 10:30:00', 0);
INSERT INTO ticket_messages VALUES (9, 4, 'agent', 4, 'You are right, the discount was not applied correctly. I have issued a $50 refund.', 0, NULL, '2024-04-05 10:45:00', '2024-04-05 11:00:00', 0);
INSERT INTO ticket_messages VALUES (10, 5, 'customer', 6, 'My desk lamp arrived with a cracked base. Order #12. Attaching photos.', 0, 'lamp_damage_1.jpg,lamp_damage_2.jpg', '2024-04-01 14:00:00', '2024-04-01 14:30:00', 0);
INSERT INTO ticket_messages VALUES (11, 5, 'agent', 1, 'Thank you for reporting this. We are reviewing your photos and will get back to you shortly.', 0, NULL, '2024-04-02 09:00:00', '2024-04-02 09:30:00', 0);
INSERT INTO ticket_messages VALUES (12, 7, 'customer', 5, 'I am interested in ordering 50 units of the PowerHub charger for our office. Is there a bulk discount?', 0, NULL, '2024-04-15 08:30:00', '2024-04-15 09:00:00', 0);
INSERT INTO ticket_messages VALUES (13, 7, 'agent', 2, 'Great question! For orders of 50+ units we offer 15% off. Let me prepare a quote.', 0, NULL, '2024-04-16 10:00:00', '2024-04-16 10:30:00', 0);
INSERT INTO ticket_messages VALUES (14, 8, 'customer', 11, 'I received a security alert about my account. Can you verify everything is okay?', 0, NULL, '2024-06-01 09:00:00', '2024-06-01 09:10:00', 0);
INSERT INTO ticket_messages VALUES (15, 8, 'agent', 4, 'I have verified your account. Everything looks secure. The alert was triggered by a login from a new device.', 0, NULL, '2024-06-01 09:30:00', '2024-06-01 09:45:00', 0);

-- ============================================================
-- GROUP 9: Content Domain
-- ============================================================

-- TABLE 46: product_reviews (15 rows)
CREATE TABLE product_reviews (
    id INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(id),
    user_id INTEGER NOT NULL REFERENCES users(id),
    rating INTEGER NOT NULL,
    title TEXT,
    body TEXT,
    is_verified_purchase INTEGER NOT NULL DEFAULT 0,
    is_approved INTEGER NOT NULL DEFAULT 0,
    helpful_votes INTEGER NOT NULL DEFAULT 0,
    reported_count INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL
);
INSERT INTO product_reviews VALUES (1, 1, 1, 5, 'Best laptop I have owned', 'Fast, lightweight, and the display is gorgeous. Highly recommend for developers.', 1, 1, 24, 0, '2024-02-10 10:00:00');
INSERT INTO product_reviews VALUES (2, 2, 2, 4, 'Great phone, minor quirks', 'Camera is amazing but battery could be better. Overall solid device.', 1, 1, 15, 0, '2024-02-20 11:00:00');
INSERT INTO product_reviews VALUES (3, 3, 1, 5, 'Incredible noise cancellation', 'These headphones block everything. Perfect for the office and flights.', 1, 1, 30, 0, '2024-03-20 09:00:00');
INSERT INTO product_reviews VALUES (4, 4, 4, 4, 'Solid tablet for the price', 'Great for media consumption. Stylus works well for note-taking.', 1, 1, 12, 0, '2024-04-01 10:00:00');
INSERT INTO product_reviews VALUES (5, 5, 4, 5, 'Love this smartwatch', 'GPS tracking is accurate and battery lasts over a week. Best fitness watch.', 1, 1, 18, 0, '2024-07-01 09:00:00');
INSERT INTO product_reviews VALUES (6, 6, 7, 4, 'Great portable speaker', 'Sound quality is impressive for the size. Takes it everywhere.', 1, 1, 8, 0, '2024-04-15 10:00:00');
INSERT INTO product_reviews VALUES (7, 7, 7, 5, 'Professional quality camera', 'The image quality at this price point is unbeatable. Highly recommend.', 0, 1, 22, 0, '2024-05-01 11:00:00');
INSERT INTO product_reviews VALUES (8, 8, 2, 4, 'Satisfying typing experience', 'Cherry MX switches feel great. RGB is a nice bonus. Slightly loud.', 1, 1, 10, 0, '2024-05-10 09:00:00');
INSERT INTO product_reviews VALUES (9, 10, 3, 5, 'Stunning 4K display', 'Colors are vibrant and accurate. Perfect for photo editing.', 1, 1, 16, 0, '2024-03-01 10:00:00');
INSERT INTO product_reviews VALUES (10, 12, 5, 4, 'Great earbuds overall', 'ANC works well. Comfortable for long listening sessions. Case is bulky.', 1, 1, 7, 0, '2024-04-01 10:00:00');
INSERT INTO product_reviews VALUES (11, 1, 10, 4, 'Solid workstation laptop', 'Handles multitasking well. Wish the trackpad was a bit bigger.', 1, 1, 9, 0, '2024-05-15 10:00:00');
INSERT INTO product_reviews VALUES (12, 5, 9, 5, 'Changed my workout routine', 'The sleep tracking and heart rate monitor are incredibly accurate.', 1, 1, 14, 0, '2024-05-01 09:00:00');
INSERT INTO product_reviews VALUES (13, 8, 6, 3, 'Good but not great', 'Keys feel nice but the software for RGB customization is clunky.', 1, 1, 5, 1, '2024-04-10 10:00:00');
INSERT INTO product_reviews VALUES (14, 15, 8, 4, 'Keeps drinks hot all day', 'Great insulation. Fits in my car cup holder. Lid could be better though.', 1, 1, 6, 0, '2024-05-20 09:00:00');
INSERT INTO product_reviews VALUES (15, 9, 11, 5, 'Perfect ergonomic mouse', 'No more wrist pain! Smooth tracking and great battery life.', 1, 1, 11, 0, '2024-05-25 10:00:00');

-- TABLE 47: review_responses (5 rows)
CREATE TABLE review_responses (
    id INTEGER PRIMARY KEY,
    review_id INTEGER NOT NULL REFERENCES product_reviews(id),
    agent_id INTEGER NOT NULL REFERENCES support_agents(id),
    response_body TEXT NOT NULL,
    created_at TEXT NOT NULL,
    is_public INTEGER NOT NULL DEFAULT 1
);
INSERT INTO review_responses VALUES (1, 1, 1, 'Thank you for the wonderful review, Alice! We are glad you love the ProBook.', '2024-02-11 09:00:00', 1);
INSERT INTO review_responses VALUES (2, 3, 1, 'We appreciate the detailed feedback! The NoiseCancel Pro is one of our bestsellers.', '2024-03-21 10:00:00', 1);
INSERT INTO review_responses VALUES (3, 7, 2, 'Great to hear you are enjoying the DSLR 5000! Check out our photography tips blog.', '2024-05-02 09:00:00', 1);
INSERT INTO review_responses VALUES (4, 13, 3, 'Thank you for the feedback. We are working on improving the RGB software in the next update.', '2024-04-11 10:00:00', 1);
INSERT INTO review_responses VALUES (5, 14, 3, 'Glad you like the ThermoSip! We have a new lid design coming in Q3.', '2024-05-21 09:00:00', 1);

-- TABLE 48: content_pages (5 rows)
CREATE TABLE content_pages (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    slug TEXT NOT NULL UNIQUE,
    body TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'draft',
    author_id INTEGER REFERENCES users(id),
    meta_title TEXT,
    meta_description TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT,
    is_public INTEGER NOT NULL DEFAULT 0
);
INSERT INTO content_pages VALUES (1, 'About NexGenMart', 'about-us', 'NexGenMart is your one-stop shop for quality electronics and home goods. Founded after acquiring ShopLocal, we combine local expertise with enterprise-grade service.', 'published', 1, 'About Us - NexGenMart', 'Learn about NexGenMart and our mission', '2024-01-01 10:00:00', '2024-06-01 10:00:00', 1);
INSERT INTO content_pages VALUES (2, 'Shipping Policy', 'shipping-policy', 'We offer free shipping on orders over $75 to most US destinations. Standard delivery takes 3-7 business days. Express delivery available for select zones.', 'published', 1, 'Shipping Policy - NexGenMart', 'NexGenMart shipping and delivery information', '2024-01-01 10:00:00', '2024-03-15 10:00:00', 1);
INSERT INTO content_pages VALUES (3, 'Return Policy', 'return-policy', 'Easy returns within 30 days of delivery. Items must be in original packaging. Refunds processed within 5-7 business days after inspection.', 'published', 1, 'Return Policy - NexGenMart', 'How to return items at NexGenMart', '2024-01-01 10:00:00', '2024-04-01 10:00:00', 1);
INSERT INTO content_pages VALUES (4, 'Privacy Policy', 'privacy-policy', 'NexGenMart is committed to protecting your privacy. We collect only the data necessary to process your orders and improve your experience.', 'published', 1, 'Privacy Policy - NexGenMart', 'NexGenMart privacy and data protection', '2024-01-01 10:00:00', '2024-02-01 10:00:00', 1);
INSERT INTO content_pages VALUES (5, 'Holiday Gift Guide 2024', 'holiday-gift-guide-2024', 'Our curated selection of the best gifts for the 2024 holiday season. From tech gadgets to home essentials, find the perfect present.', 'draft', 3, 'Holiday Gift Guide 2024 - NexGenMart', 'Best holiday gift ideas from NexGenMart', '2024-10-01 10:00:00', NULL, 0);

-- TABLE 49: promotional_banners (6 rows)
CREATE TABLE promotional_banners (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    image_url TEXT NOT NULL,
    target_url TEXT,
    display_position TEXT NOT NULL,
    starts_at TEXT NOT NULL,
    ends_at TEXT,
    is_active INTEGER NOT NULL DEFAULT 1,
    click_count INTEGER NOT NULL DEFAULT 0,
    impression_count INTEGER NOT NULL DEFAULT 0,
    created_by TEXT
);
INSERT INTO promotional_banners VALUES (1, 'Spring Tech Sale', 'https://img.nexgenmart.com/banners/spring-tech.jpg', '/collections/electronics', 'homepage_hero', '2024-03-01 00:00:00', '2024-04-30 23:59:59', 0, 1520, 25000, 'marketing_team');
INSERT INTO promotional_banners VALUES (2, 'Summer Blowout', 'https://img.nexgenmart.com/banners/summer-sale.jpg', '/sale/summer', 'homepage_hero', '2024-06-01 00:00:00', '2024-08-31 23:59:59', 0, 3200, 48000, 'marketing_team');
INSERT INTO promotional_banners VALUES (3, 'Free Shipping Over $75', 'https://img.nexgenmart.com/banners/free-ship.jpg', '/shipping-policy', 'top_bar', '2024-01-01 00:00:00', '2024-12-31 23:59:59', 1, 890, 120000, 'marketing_team');
INSERT INTO promotional_banners VALUES (4, 'New Arrivals Weekly', 'https://img.nexgenmart.com/banners/new-arrivals.jpg', '/collections/new', 'sidebar', '2024-01-01 00:00:00', '2024-12-31 23:59:59', 1, 2100, 85000, 'marketing_team');
INSERT INTO promotional_banners VALUES (5, 'Back to School Deals', 'https://img.nexgenmart.com/banners/back-school.jpg', '/sale/back-to-school', 'homepage_hero', '2024-08-15 00:00:00', '2024-09-15 23:59:59', 1, 780, 12000, 'marketing_team');
INSERT INTO promotional_banners VALUES (6, 'Holiday Preview 2024', 'https://img.nexgenmart.com/banners/holiday-preview.jpg', '/collections/holiday', 'homepage_secondary', '2024-11-01 00:00:00', '2024-12-31 23:59:59', 1, 0, 0, 'admin');

-- ============================================================
-- GROUP 10: Finance Domain
-- ============================================================

-- TABLE 50: tax_rules (6 rows)
CREATE TABLE tax_rules (
    id INTEGER PRIMARY KEY,
    jurisdiction TEXT NOT NULL,
    rate REAL NOT NULL,
    tax_name TEXT NOT NULL,
    tax_type TEXT NOT NULL,
    is_active INTEGER NOT NULL DEFAULT 1,
    effective_from TEXT NOT NULL,
    effective_until TEXT,
    applies_to TEXT NOT NULL DEFAULT 'all',
    created_at TEXT NOT NULL
);
INSERT INTO tax_rules VALUES (1, 'NY', 0.08, 'New York Sales Tax', 'sales', 1, '2024-01-01 00:00:00', NULL, 'all', '2024-01-01 00:00:00');
INSERT INTO tax_rules VALUES (2, 'CA', 0.0725, 'California Sales Tax', 'sales', 1, '2024-01-01 00:00:00', NULL, 'all', '2024-01-01 00:00:00');
INSERT INTO tax_rules VALUES (3, 'TX', 0.0625, 'Texas Sales Tax', 'sales', 1, '2024-01-01 00:00:00', NULL, 'all', '2024-01-01 00:00:00');
INSERT INTO tax_rules VALUES (4, 'IL', 0.0625, 'Illinois Sales Tax', 'sales', 1, '2024-01-01 00:00:00', NULL, 'all', '2024-01-01 00:00:00');
INSERT INTO tax_rules VALUES (5, 'FL', 0.06, 'Florida Sales Tax', 'sales', 1, '2024-01-01 00:00:00', NULL, 'all', '2024-01-01 00:00:00');
INSERT INTO tax_rules VALUES (6, 'AZ', 0.056, 'Arizona Transaction Privilege Tax', 'sales', 1, '2024-01-01 00:00:00', NULL, 'all', '2024-01-01 00:00:00');

-- TABLE 51: tax_rate_history (6 rows)
CREATE TABLE tax_rate_history (
    id INTEGER PRIMARY KEY,
    tax_rule_id INTEGER NOT NULL REFERENCES tax_rules(id),
    old_rate REAL NOT NULL,
    new_rate REAL NOT NULL,
    changed_at TEXT NOT NULL,
    reason TEXT
);
INSERT INTO tax_rate_history VALUES (1, 1, 0.08875, 0.08, '2024-01-01 00:00:00', 'State rate adjustment');
INSERT INTO tax_rate_history VALUES (2, 2, 0.075, 0.0725, '2024-01-01 00:00:00', 'Annual rate review');
INSERT INTO tax_rate_history VALUES (3, 3, 0.065, 0.0625, '2024-01-01 00:00:00', 'Legislative change');
INSERT INTO tax_rate_history VALUES (4, 4, 0.065, 0.0625, '2024-01-01 00:00:00', 'Rate harmonization');
INSERT INTO tax_rate_history VALUES (5, 5, 0.065, 0.06, '2024-01-01 00:00:00', 'Rate reduction');
INSERT INTO tax_rate_history VALUES (6, 6, 0.06, 0.056, '2024-01-01 00:00:00', 'Annual adjustment');

-- ============================================================
-- GROUP 11: Analytics Domain (ALL NEW computed tables)
-- ============================================================

-- TABLE 52: product_performance (15 rows)
CREATE TABLE product_performance (
    id INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL UNIQUE REFERENCES products(id),
    total_units_sold INTEGER NOT NULL DEFAULT 0,
    total_revenue REAL NOT NULL DEFAULT 0.0,
    average_rating REAL,
    review_count INTEGER NOT NULL DEFAULT 0,
    wishlist_count INTEGER NOT NULL DEFAULT 0,
    return_count INTEGER NOT NULL DEFAULT 0,
    conversion_rate REAL
);
INSERT INTO product_performance VALUES (1, 1, 4, 4199.96, 4.5, 2, 1, 0, 0.12);
INSERT INTO product_performance VALUES (2, 2, 1, 799.99, 4.0, 1, 1, 0, 0.08);
INSERT INTO product_performance VALUES (3, 3, 2, 499.98, 5.0, 1, 1, 1, 0.15);
INSERT INTO product_performance VALUES (4, 4, 2, 1079.98, 4.0, 1, 0, 0, 0.10);
INSERT INTO product_performance VALUES (5, 5, 3, 1049.97, 5.0, 2, 1, 0, 0.18);
INSERT INTO product_performance VALUES (6, 6, 3, 449.97, 4.0, 1, 1, 0, 0.14);
INSERT INTO product_performance VALUES (7, 7, 1, 1299.99, 5.0, 1, 1, 0, 0.06);
INSERT INTO product_performance VALUES (8, 8, 2, 259.98, 3.5, 2, 1, 0, 0.11);
INSERT INTO product_performance VALUES (9, 9, 1, 59.99, 5.0, 1, 0, 0, 0.09);
INSERT INTO product_performance VALUES (10, 10, 1, 449.99, 5.0, 1, 1, 0, 0.07);
INSERT INTO product_performance VALUES (11, 11, 3, 149.97, 0.0, 0, 1, 0, 0.20);
INSERT INTO product_performance VALUES (12, 12, 2, 359.98, 4.0, 1, 0, 0, 0.13);
INSERT INTO product_performance VALUES (13, 13, 0, 0.0, 0.0, 0, 1, 0, 0.05);
INSERT INTO product_performance VALUES (14, 14, 3, 119.97, 0.0, 0, 1, 1, 0.16);
INSERT INTO product_performance VALUES (15, 15, 4, 99.96, 4.0, 1, 1, 1, 0.22);

-- TABLE 53: category_performance (8 rows)
CREATE TABLE category_performance (
    id INTEGER PRIMARY KEY,
    category_id INTEGER NOT NULL UNIQUE REFERENCES categories(id),
    product_count INTEGER NOT NULL DEFAULT 0,
    total_revenue REAL NOT NULL DEFAULT 0.0,
    average_product_rating REAL,
    top_product_id INTEGER REFERENCES products(id)
);
INSERT INTO category_performance VALUES (1, 1, 3, 1309.96, 4.0, 2);
INSERT INTO category_performance VALUES (2, 2, 3, 5729.93, 4.5, 1);
INSERT INTO category_performance VALUES (3, 3, 3, 1309.93, 4.33, 3);
INSERT INTO category_performance VALUES (4, 4, 1, 0.0, 0.0, 13);
INSERT INTO category_performance VALUES (5, 5, 1, 1049.97, 5.0, 5);
INSERT INTO category_performance VALUES (6, 6, 3, 439.94, 4.0, 8);
INSERT INTO category_performance VALUES (7, 7, 1, 1299.99, 5.0, 7);
INSERT INTO category_performance VALUES (8, 8, 1, 99.96, 4.0, 15);

-- TABLE 54: daily_revenue_summary (5 rows)
CREATE TABLE daily_revenue_summary (
    id INTEGER PRIMARY KEY,
    summary_date TEXT NOT NULL UNIQUE,
    order_count INTEGER NOT NULL,
    total_revenue REAL NOT NULL,
    total_tax REAL NOT NULL,
    total_shipping REAL NOT NULL,
    total_discounts REAL NOT NULL,
    average_order_value REAL NOT NULL
);
INSERT INTO daily_revenue_summary VALUES (1, '2024-02-01', 1, 1079.99, 80.00, 0.00, 0.00, 1079.99);
INSERT INTO daily_revenue_summary VALUES (2, '2024-03-01', 1, 1079.99, 80.00, 0.00, 0.00, 1079.99);
INSERT INTO daily_revenue_summary VALUES (3, '2024-03-15', 2, 1085.97, 80.00, 5.99, 0.00, 542.99);
INSERT INTO daily_revenue_summary VALUES (4, '2024-04-01', 1, 759.99, 60.00, 0.00, 50.00, 759.99);
INSERT INTO daily_revenue_summary VALUES (5, '2024-05-01', 1, 1079.99, 80.00, 0.00, 0.00, 1079.99);

-- TABLE 55: user_cohort_analysis (4 rows)
CREATE TABLE user_cohort_analysis (
    id INTEGER PRIMARY KEY,
    cohort_month TEXT NOT NULL,
    cohort_size INTEGER NOT NULL,
    orders_month_1 INTEGER NOT NULL DEFAULT 0,
    orders_month_2 INTEGER NOT NULL DEFAULT 0,
    revenue_month_1 REAL NOT NULL DEFAULT 0.0,
    revenue_month_2 REAL NOT NULL DEFAULT 0.0,
    retention_rate REAL
);
INSERT INTO user_cohort_analysis VALUES (1, '2024-01', 4, 5, 4, 4283.95, 3393.94, 0.75);
INSERT INTO user_cohort_analysis VALUES (2, '2024-02', 4, 4, 3, 2996.34, 2282.36, 0.75);
INSERT INTO user_cohort_analysis VALUES (3, '2024-03', 4, 4, 2, 2470.33, 1711.97, 0.50);
INSERT INTO user_cohort_analysis VALUES (4, '2024-04', 0, 0, 0, 0.0, 0.0, 0.0);
