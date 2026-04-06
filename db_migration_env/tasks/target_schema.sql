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

INSERT INTO users VALUES (1, 'Alice', 'Chen', 'alice@email.com', '555-0101', 'hashed_pw_alice01', '1990-03-15', '2021-01-10', '2025-03-28', 1);
INSERT INTO users VALUES (2, 'Bob', 'Rivera', 'bob@email.com', '555-0102', 'hashed_pw_bob02', '1985-07-22', '2021-03-05', '2025-03-25', 1);
INSERT INTO users VALUES (3, 'Carol', 'Zhang', 'carol@email.com', '555-0103', 'hashed_pw_carol03', '1992-11-08', '2021-06-18', '2025-03-27', 1);
INSERT INTO users VALUES (4, 'Dave', 'Wilson', 'dave@email.com', '555-0104', 'hashed_pw_dave04', '1988-01-30', '2022-01-12', '2025-03-20', 1);
INSERT INTO users VALUES (5, 'Eve', 'Thompson', 'eve@email.com', '555-0105', 'hashed_pw_eve05', '1995-05-12', '2022-04-20', '2025-03-26', 1);
INSERT INTO users VALUES (6, 'Frank', 'Garcia', 'frank@email.com', '555-0106', 'hashed_pw_frank06', '1983-09-25', '2022-07-01', '2025-03-15', 1);
INSERT INTO users VALUES (7, 'Grace', 'Kim', 'grace@email.com', '555-0107', 'hashed_pw_grace07', '1991-12-03', '2022-09-14', '2025-03-28', 1);
INSERT INTO users VALUES (8, 'Henry', 'Patel', 'henry@email.com', '555-0108', 'hashed_pw_henry08', '1987-04-18', '2023-01-22', '2025-03-22', 1);
INSERT INTO users VALUES (9, 'Ivy', 'Santos', 'ivy@email.com', '555-0109', 'hashed_pw_ivy09', '1994-08-07', '2023-05-10', '2025-03-24', 1);
INSERT INTO users VALUES (10, 'Jack', 'Murphy', 'jack@email.com', '555-0110', 'hashed_pw_jack10', '1986-02-14', '2023-08-03', '2025-03-18', 1);
INSERT INTO users VALUES (11, 'Kate', 'Brown', 'kate@email.com', '555-0111', 'hashed_pw_kate11', '1993-06-29', '2024-01-15', '2025-03-27', 1);
INSERT INTO users VALUES (12, 'Leo', 'Martinez', 'leo@email.com', '555-0112', 'hashed_pw_leo12', '1989-10-11', '2024-04-28', '2025-03-19', 0);

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

INSERT INTO user_addresses VALUES (1, 1, 'shipping', '123 Maple St', 'Portland', 'OR', '97201', 'US', 1);
INSERT INTO user_addresses VALUES (2, 2, 'shipping', '456 Oak Ave', 'Austin', 'TX', '78701', 'US', 1);
INSERT INTO user_addresses VALUES (3, 3, 'shipping', '789 Pine Rd', 'Seattle', 'WA', '98101', 'US', 1);
INSERT INTO user_addresses VALUES (4, 4, 'shipping', '321 Elm Blvd', 'Denver', 'CO', '80201', 'US', 1);
INSERT INTO user_addresses VALUES (5, 5, 'shipping', '654 Birch Ln', 'Miami', 'FL', '33101', 'US', 1);
INSERT INTO user_addresses VALUES (6, 6, 'shipping', '987 Cedar Ct', 'Chicago', 'IL', '60601', 'US', 1);
INSERT INTO user_addresses VALUES (7, 7, 'shipping', '147 Walnut Dr', 'San Francisco', 'CA', '94101', 'US', 1);
INSERT INTO user_addresses VALUES (8, 8, 'shipping', '258 Spruce Way', 'Boston', 'MA', '02101', 'US', 1);
INSERT INTO user_addresses VALUES (9, 9, 'shipping', '369 Ash Pl', 'Phoenix', 'AZ', '85001', 'US', 1);
INSERT INTO user_addresses VALUES (10, 10, 'shipping', '480 Poplar St', 'Nashville', 'TN', '37201', 'US', 1);
INSERT INTO user_addresses VALUES (11, 11, 'shipping', '591 Hickory Ave', 'Atlanta', 'GA', '30301', 'US', 1);
INSERT INTO user_addresses VALUES (12, 12, 'shipping', '702 Sycamore Rd', 'San Diego', 'CA', '92101', 'US', 1);
INSERT INTO user_addresses VALUES (13, 1, 'billing', '123 Maple St', 'Portland', 'OR', '97201', 'US', 0);
INSERT INTO user_addresses VALUES (14, 5, 'billing', '654 Birch Ln', 'Miami', 'FL', '33101', 'US', 0);
INSERT INTO user_addresses VALUES (15, 9, 'billing', '369 Ash Pl', 'Phoenix', 'AZ', '85001', 'US', 0);
INSERT INTO user_addresses VALUES (16, 12, 'billing', '702 Sycamore Rd', 'San Diego', 'CA', '92101', 'US', 0);

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

INSERT INTO user_stats VALUES (1, 1, 2, 1673.98, 836.99, '2024-09-15', '2025-01-05', 2);
INSERT INTO user_stats VALUES (2, 2, 2, 1182.73, 591.37, '2024-09-20', '2025-01-28', 1);
INSERT INTO user_stats VALUES (3, 3, 2, 308.96, 154.48, '2024-10-01', '2025-02-10', 1);
INSERT INTO user_stats VALUES (4, 4, 2, 1056.16, 528.08, '2024-10-10', '2025-03-22', 2);
INSERT INTO user_stats VALUES (5, 5, 2, 2032.97, 1016.49, '2024-10-18', '2025-02-20', 1);
INSERT INTO user_stats VALUES (6, 6, 1, 351.98, 351.98, '2024-11-02', '2024-11-02', 1);
INSERT INTO user_stats VALUES (7, 7, 2, 1002.37, 501.19, '2024-11-15', '2025-03-01', 1);
INSERT INTO user_stats VALUES (8, 8, 2, 277.58, 138.79, '2024-11-28', '2025-03-10', 2);
INSERT INTO user_stats VALUES (9, 9, 2, 358.68, 179.34, '2024-12-05', '2025-03-15', 1);
INSERT INTO user_stats VALUES (10, 10, 1, 49.68, 49.68, '2024-12-12', '2024-12-12', 1);
INSERT INTO user_stats VALUES (11, 11, 1, 514.97, 514.97, '2024-12-20', '2024-12-20', 1);
INSERT INTO user_stats VALUES (12, 12, 1, 136.78, 136.78, '2025-01-15', '2025-01-15', 1);

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

INSERT INTO user_notes VALUES (1, 1, 'VIP customer, frequent buyer of electronics', 'flag', 'agent_sarah', 'high', 'active', '2024-06-01', '2024-06-01', 1);
INSERT INTO user_notes VALUES (2, 2, 'Requested bulk pricing for office supplies', 'request', 'agent_mike', 'normal', 'open', '2024-07-15', '2024-07-20', 0);
INSERT INTO user_notes VALUES (3, 3, 'Prefers expedited shipping', 'preference', 'agent_sarah', 'low', 'active', '2024-08-10', '2024-08-10', 1);
INSERT INTO user_notes VALUES (4, 4, 'Had shipping issue with order 1005, resolved with replacement', 'issue', 'agent_mike', 'high', 'resolved', '2024-09-03', '2024-09-10', 1);
INSERT INTO user_notes VALUES (5, 5, 'Interested in loyalty program enrollment', 'flag', 'agent_jenny', 'normal', 'open', '2024-10-22', '2024-10-22', 0);
INSERT INTO user_notes VALUES (6, 6, 'Credit hold removed after payment verification', 'billing', 'agent_sarah', 'high', 'resolved', '2024-11-05', '2024-11-08', 1);
INSERT INTO user_notes VALUES (7, 7, 'Allergic to latex, flag for packaging', 'preference', 'agent_jenny', 'high', 'active', '2025-01-12', '2025-01-12', 1);
INSERT INTO user_notes VALUES (8, 8, 'Corporate account pending approval', 'request', 'agent_mike', 'normal', 'open', '2025-02-18', '2025-02-20', 0);

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

INSERT INTO categories VALUES (1, 'Electronics', 'electronics', 'Gadgets, devices, and electronic accessories', NULL, 1, 1, '/img/cat/electronics.jpg', 'Shop Electronics', 'Browse our wide selection of electronics');
INSERT INTO categories VALUES (2, 'Computers', 'computers', 'Laptops, desktops, and computer accessories', 1, 1, 2, '/img/cat/computers.jpg', 'Shop Computers', 'Find the perfect computer for work or play');
INSERT INTO categories VALUES (3, 'Phones', 'phones', 'Smartphones and mobile accessories', 1, 1, 3, '/img/cat/phones.jpg', 'Shop Phones', 'Discover the latest smartphones');
INSERT INTO categories VALUES (4, 'Clothing', 'clothing', 'Apparel for men, women, and children', NULL, 1, 4, '/img/cat/clothing.jpg', 'Shop Clothing', 'Trendy and comfortable clothing for everyone');
INSERT INTO categories VALUES (5, 'Shoes', 'shoes', 'Footwear for every occasion', 4, 1, 5, '/img/cat/shoes.jpg', 'Shop Shoes', 'Step up your style with our shoe collection');
INSERT INTO categories VALUES (6, 'Home & Kitchen', 'home-kitchen', 'Appliances, cookware, and home essentials', NULL, 1, 6, '/img/cat/home.jpg', 'Shop Home & Kitchen', 'Everything for your home and kitchen');
INSERT INTO categories VALUES (7, 'Accessories', 'accessories', 'Watches, bags, and personal accessories', NULL, 1, 7, '/img/cat/accessories.jpg', 'Shop Accessories', 'Complete your look with our accessories');
INSERT INTO categories VALUES (8, 'Books', 'books', 'Physical and digital books across all genres', NULL, 1, 8, '/img/cat/books.jpg', 'Shop Books', 'Expand your mind with our book collection');

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

INSERT INTO brands VALUES (1, 'TechNova', 'technova', 'Leading innovator in consumer electronics', '/img/brand/technova.png', 'https://technova.example.com', 'US', 2010, 1, 'partners@technova.example.com');
INSERT INTO brands VALUES (2, 'SoundCraft', 'soundcraft', 'Premium audio equipment manufacturer', '/img/brand/soundcraft.png', 'https://soundcraft.example.com', 'JP', 2005, 1, 'sales@soundcraft.example.com');
INSERT INTO brands VALUES (3, 'UrbanThread', 'urbanthread', 'Sustainable fashion and lifestyle brand', '/img/brand/urbanthread.png', 'https://urbanthread.example.com', 'US', 2015, 1, 'wholesale@urbanthread.example.com');
INSERT INTO brands VALUES (4, 'HomePlus', 'homeplus', 'Quality home appliances and kitchenware', '/img/brand/homeplus.png', 'https://homeplus.example.com', 'DE', 2008, 1, 'info@homeplus.example.com');
INSERT INTO brands VALUES (5, 'PageBound', 'pagebound', 'Independent book publisher', '/img/brand/pagebound.png', 'https://pagebound.example.com', 'UK', 2012, 1, 'submissions@pagebound.example.com');
INSERT INTO brands VALUES (6, 'GreenLeaf', 'greenleaf', 'Eco-friendly products and accessories', '/img/brand/greenleaf.png', 'https://greenleaf.example.com', 'CA', 2018, 0, 'hello@greenleaf.example.com');

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

INSERT INTO products VALUES (1, 'SL-LAPTOP-001', 'ProBook Laptop 15"', 'High-performance laptop with 16GB RAM and 512GB SSD', 2, 1, 1299.99, 850.0, 2.1, '35.6x24.8x1.8cm', 1, '2023-01-15', '2025-02-10');
INSERT INTO products VALUES (2, 'SL-PHONE-002', 'SmartEdge Phone X', 'Flagship smartphone with OLED display', 3, 1, 899.99, 520.0, 0.19, '15.4x7.1x0.8cm', 1, '2023-02-20', '2025-01-15');
INSERT INTO products VALUES (3, 'SL-TABLET-003', 'SlateView Tablet 10"', '10-inch tablet with stylus support', 1, 1, 549.99, 310.0, 0.48, '24.5x17.4x0.6cm', 1, '2023-03-10', '2024-12-05');
INSERT INTO products VALUES (4, 'SL-HEADPH-004', 'BassWave Wireless Headphones', 'Noise-cancelling over-ear headphones', 1, 2, 199.99, 85.0, 0.32, '19x17x8cm', 1, '2023-04-01', '2025-03-01');
INSERT INTO products VALUES (5, 'SL-TSHIRT-005', 'Classic Cotton Tee', '100% organic cotton crew-neck t-shirt', 4, 3, 29.99, 8.5, 0.2, '30x25x2cm', 1, '2023-05-15', '2025-01-20');
INSERT INTO products VALUES (6, 'SL-JEANS-006', 'Slim Fit Denim Jeans', 'Stretch denim with modern slim fit', 4, 3, 69.99, 25.0, 0.65, '35x30x5cm', 1, '2023-06-01', '2025-02-14');
INSERT INTO products VALUES (7, 'SL-SNEAK-007', 'RunFlex Sneakers', 'Lightweight running shoes with memory foam sole', 5, 3, 119.99, 42.0, 0.7, '32x12x11cm', 1, '2023-07-10', '2025-01-30');
INSERT INTO products VALUES (8, 'SL-JACKET-008', 'Weathershield Rain Jacket', 'Waterproof breathable rain jacket', 4, 3, 149.99, 55.0, 0.45, '40x30x5cm', 1, '2023-08-05', '2024-11-20');
INSERT INTO products VALUES (9, 'SL-BLNDR-009', 'PowerBlend Pro Blender', 'High-speed blender with 10 settings', 6, 4, 89.99, 35.0, 3.2, '20x20x40cm', 1, '2023-09-12', '2025-02-28');
INSERT INTO products VALUES (10, 'SL-COFFM-010', 'BrewMaster Coffee Maker', '12-cup drip coffee maker with timer', 6, 4, 79.99, 30.0, 2.8, '22x18x35cm', 1, '2023-10-01', '2025-01-05');
INSERT INTO products VALUES (11, 'SL-WATCH-011', 'ChronoFit Smartwatch', 'Fitness smartwatch with heart rate monitor', 7, 1, 249.99, 110.0, 0.05, '4.4x4.4x1.1cm', 1, '2023-11-15', '2025-03-10');
INSERT INTO products VALUES (12, 'SL-BACKP-012', 'TrekPack Laptop Backpack', 'Water-resistant backpack with USB charging port', 7, 3, 59.99, 18.0, 0.9, '45x30x15cm', 1, '2024-01-10', '2025-02-20');
INSERT INTO products VALUES (13, 'SL-BOOK-013', 'SQL Mastery Handbook', 'Comprehensive guide to database design and optimization', 8, 5, 39.99, 12.0, 0.55, '23x15x3cm', 1, '2024-02-15', '2025-01-10');
INSERT INTO products VALUES (14, 'SL-CHARGER-014', 'QuickCharge USB-C Hub', '7-in-1 USB-C hub with fast charging', 1, 1, 49.99, 15.0, 0.12, '10x5x1.5cm', 1, '2024-03-20', '2025-03-05');
INSERT INTO products VALUES (15, 'SL-MUG-015', 'Ceramic Travel Mug', 'Double-walled ceramic mug with silicone lid', 6, 4, 19.99, 5.5, 0.35, '9x9x14cm', 1, '2024-04-05', '2025-02-01');

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

INSERT INTO product_variants VALUES (1, 1, 'ProBook 15 Silver 8GB', 'SL-LAPTOP-001-SLV-8', -200.0, 25, 'Silver', '8GB', 2.1, 1, '2023-01-15');
INSERT INTO product_variants VALUES (2, 1, 'ProBook 15 Space Gray 16GB', 'SL-LAPTOP-001-GRY-16', 0.0, 18, 'Space Gray', '16GB', 2.15, 1, '2023-01-15');
INSERT INTO product_variants VALUES (3, 2, 'SmartEdge X Black 128GB', 'SL-PHONE-002-BLK-128', 0.0, 40, 'Black', '128GB', 0.19, 1, '2023-02-20');
INSERT INTO product_variants VALUES (4, 2, 'SmartEdge X White 256GB', 'SL-PHONE-002-WHT-256', 100.0, 22, 'White', '256GB', 0.19, 1, '2023-02-20');
INSERT INTO product_variants VALUES (5, 5, 'Classic Tee White S', 'SL-TSHIRT-005-WHT-S', 0.0, 60, 'White', 'S', 0.18, 1, '2023-05-15');
INSERT INTO product_variants VALUES (6, 5, 'Classic Tee White M', 'SL-TSHIRT-005-WHT-M', 0.0, 85, 'White', 'M', 0.2, 1, '2023-05-15');
INSERT INTO product_variants VALUES (7, 5, 'Classic Tee Black L', 'SL-TSHIRT-005-BLK-L', 0.0, 70, 'Black', 'L', 0.22, 1, '2023-05-15');
INSERT INTO product_variants VALUES (8, 6, 'Slim Jeans Blue 32', 'SL-JEANS-006-BLU-32', 0.0, 45, 'Blue', '32', 0.65, 1, '2023-06-01');
INSERT INTO product_variants VALUES (9, 6, 'Slim Jeans Blue 34', 'SL-JEANS-006-BLU-34', 0.0, 38, 'Blue', '34', 0.67, 1, '2023-06-01');
INSERT INTO product_variants VALUES (10, 6, 'Slim Jeans Black 30', 'SL-JEANS-006-BLK-30', 0.0, 30, 'Black', '30', 0.63, 1, '2023-06-01');
INSERT INTO product_variants VALUES (11, 7, 'RunFlex White US9', 'SL-SNEAK-007-WHT-9', 0.0, 20, 'White', 'US9', 0.7, 1, '2023-07-10');
INSERT INTO product_variants VALUES (12, 7, 'RunFlex Black US10', 'SL-SNEAK-007-BLK-10', 0.0, 15, 'Black', 'US10', 0.72, 1, '2023-07-10');
INSERT INTO product_variants VALUES (13, 8, 'Rain Jacket Navy M', 'SL-JACKET-008-NVY-M', 0.0, 28, 'Navy', 'M', 0.45, 1, '2023-08-05');
INSERT INTO product_variants VALUES (14, 8, 'Rain Jacket Red L', 'SL-JACKET-008-RED-L', 0.0, 22, 'Red', 'L', 0.47, 1, '2023-08-05');
INSERT INTO product_variants VALUES (15, 4, 'BassWave Black', 'SL-HEADPH-004-BLK', 0.0, 50, 'Black', 'OneSize', 0.32, 1, '2023-04-01');
INSERT INTO product_variants VALUES (16, 4, 'BassWave White', 'SL-HEADPH-004-WHT', 0.0, 35, 'White', 'OneSize', 0.32, 1, '2023-04-01');
INSERT INTO product_variants VALUES (17, 11, 'ChronoFit Black', 'SL-WATCH-011-BLK', 0.0, 30, 'Black', 'OneSize', 0.05, 1, '2023-11-15');
INSERT INTO product_variants VALUES (18, 11, 'ChronoFit Rose Gold', 'SL-WATCH-011-RGD', 30.0, 12, 'Rose Gold', 'OneSize', 0.05, 1, '2023-11-15');
INSERT INTO product_variants VALUES (19, 15, 'Travel Mug Teal', 'SL-MUG-015-TEL', 0.0, 100, 'Teal', 'OneSize', 0.35, 1, '2024-04-05');
INSERT INTO product_variants VALUES (20, 15, 'Travel Mug Charcoal', 'SL-MUG-015-CHR', 0.0, 80, 'Charcoal', 'OneSize', 0.35, 1, '2024-04-05');

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

INSERT INTO product_images VALUES (1, 1, '/img/products/laptop-001-main.jpg', 'ProBook Laptop 15 front view', 1, 1, 1200, 800, 245, 'image/jpeg', '2023-01-15');
INSERT INTO product_images VALUES (2, 1, '/img/products/laptop-001-side.jpg', 'ProBook Laptop 15 side view', 2, 0, 1200, 800, 198, 'image/jpeg', '2023-01-15');
INSERT INTO product_images VALUES (3, 2, '/img/products/phone-002-main.jpg', 'SmartEdge Phone X front', 1, 1, 800, 1200, 180, 'image/jpeg', '2023-02-20');
INSERT INTO product_images VALUES (4, 3, '/img/products/tablet-003-main.jpg', 'SlateView Tablet with stylus', 1, 1, 1000, 750, 210, 'image/jpeg', '2023-03-10');
INSERT INTO product_images VALUES (5, 4, '/img/products/headphones-004-main.jpg', 'BassWave headphones on stand', 1, 1, 900, 900, 156, 'image/jpeg', '2023-04-01');
INSERT INTO product_images VALUES (6, 5, '/img/products/tshirt-005-main.jpg', 'Classic Cotton Tee white front', 1, 1, 800, 1000, 120, 'image/jpeg', '2023-05-15');
INSERT INTO product_images VALUES (7, 5, '/img/products/tshirt-005-back.jpg', 'Classic Cotton Tee white back', 2, 0, 800, 1000, 115, 'image/jpeg', '2023-05-15');
INSERT INTO product_images VALUES (8, 6, '/img/products/jeans-006-main.jpg', 'Slim Fit Denim Jeans front', 1, 1, 800, 1200, 175, 'image/jpeg', '2023-06-01');
INSERT INTO product_images VALUES (9, 7, '/img/products/sneakers-007-main.jpg', 'RunFlex Sneakers white pair', 1, 1, 1000, 700, 190, 'image/jpeg', '2023-07-10');
INSERT INTO product_images VALUES (10, 8, '/img/products/jacket-008-main.jpg', 'Weathershield Rain Jacket navy', 1, 1, 800, 1000, 165, 'image/jpeg', '2023-08-05');
INSERT INTO product_images VALUES (11, 9, '/img/products/blender-009-main.jpg', 'PowerBlend Pro Blender with jar', 1, 1, 800, 1000, 140, 'image/jpeg', '2023-09-12');
INSERT INTO product_images VALUES (12, 10, '/img/products/coffee-010-main.jpg', 'BrewMaster Coffee Maker front', 1, 1, 800, 1000, 155, 'image/jpeg', '2023-10-01');
INSERT INTO product_images VALUES (13, 11, '/img/products/watch-011-main.jpg', 'ChronoFit Smartwatch on wrist', 1, 1, 900, 900, 130, 'image/jpeg', '2023-11-15');
INSERT INTO product_images VALUES (14, 12, '/img/products/backpack-012-main.jpg', 'TrekPack Backpack front view', 1, 1, 800, 1000, 185, 'image/jpeg', '2024-01-10');
INSERT INTO product_images VALUES (15, 13, '/img/products/book-013-main.jpg', 'SQL Mastery Handbook cover', 1, 1, 600, 900, 95, 'image/jpeg', '2024-02-15');
INSERT INTO product_images VALUES (16, 14, '/img/products/charger-014-main.jpg', 'QuickCharge USB-C Hub top view', 1, 1, 800, 600, 88, 'image/jpeg', '2024-03-20');
INSERT INTO product_images VALUES (17, 15, '/img/products/mug-015-main.jpg', 'Ceramic Travel Mug teal', 1, 1, 800, 800, 110, 'image/jpeg', '2024-04-05');
INSERT INTO product_images VALUES (18, 15, '/img/products/mug-015-lid.jpg', 'Ceramic Travel Mug lid detail', 2, 0, 600, 600, 72, 'image/jpeg', '2024-04-05');

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

INSERT INTO tags VALUES (1, 'bestseller', 'bestseller', 'Top-selling products', 3, 1, '#FF5733', 1, '2023-01-01', 1);
INSERT INTO tags VALUES (2, 'new-arrival', 'new-arrival', 'Recently added products', 2, 1, '#33C1FF', 1, '2023-01-01', 1);
INSERT INTO tags VALUES (3, 'gift-idea', 'gift-idea', 'Great gift suggestions', 4, 1, '#FF33A8', 1, '2023-01-01', 1);
INSERT INTO tags VALUES (4, 'work-from-home', 'work-from-home', 'Products for remote work', 3, 0, '#33FF57', 1, '2023-01-01', 1);
INSERT INTO tags VALUES (5, 'sustainable', 'sustainable', 'Eco-friendly and sustainable products', 2, 0, '#57FF33', 1, '2023-03-15', 1);
INSERT INTO tags VALUES (6, 'summer', 'summer', 'Seasonal summer picks', 1, 0, '#FFD700', NULL, '2023-05-01', 1);
INSERT INTO tags VALUES (7, 'wireless', 'wireless', 'Wireless and cable-free products', 2, 0, '#8A2BE2', NULL, '2023-04-01', 1);
INSERT INTO tags VALUES (8, 'portable', 'portable', 'Compact and portable items', 2, 0, '#20B2AA', 1, '2023-04-10', 1);
INSERT INTO tags VALUES (9, 'everyday', 'everyday', 'Everyday essentials', 2, 0, '#696969', 1, '2023-07-01', 1);
INSERT INTO tags VALUES (10, 'sport', 'sport', 'Sports and fitness products', 1, 0, '#FF4500', NULL, '2023-07-10', 1);

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

INSERT INTO product_tags VALUES (1, 1, 1, 1, '2023-06-01', 0, 1.0, 'manual', 0.95, 1);
INSERT INTO product_tags VALUES (2, 1, 4, 1, '2023-06-01', 0, 0.8, 'manual', 0.9, 1);
INSERT INTO product_tags VALUES (3, 2, 1, 1, '2023-03-15', 0, 1.0, 'manual', 0.95, 1);
INSERT INTO product_tags VALUES (4, 2, 2, NULL, '2023-02-20', 1, 0.9, 'auto-rule', 0.85, 1);
INSERT INTO product_tags VALUES (5, 3, 8, 1, '2023-04-10', 0, 0.7, 'manual', 0.8, 1);
INSERT INTO product_tags VALUES (6, 4, 3, 1, '2023-11-01', 0, 0.9, 'manual', 0.88, 1);
INSERT INTO product_tags VALUES (7, 4, 7, NULL, '2023-04-01', 1, 1.0, 'auto-catalog', 0.99, 1);
INSERT INTO product_tags VALUES (8, 5, 5, 1, '2023-06-20', 0, 0.9, 'manual', 0.92, 1);
INSERT INTO product_tags VALUES (9, 5, 6, NULL, '2023-05-15', 1, 0.7, 'auto-season', 0.75, 1);
INSERT INTO product_tags VALUES (10, 6, 9, 1, '2023-07-01', 0, 0.8, 'manual', 0.85, 1);
INSERT INTO product_tags VALUES (11, 7, 10, NULL, '2023-07-10', 1, 0.9, 'auto-catalog', 0.9, 1);
INSERT INTO product_tags VALUES (12, 7, 2, NULL, '2023-07-10', 1, 0.8, 'auto-rule', 0.8, 1);
INSERT INTO product_tags VALUES (13, 9, 3, 1, '2023-11-01', 0, 0.8, 'manual', 0.82, 1);
INSERT INTO product_tags VALUES (14, 11, 3, 1, '2023-12-01', 0, 1.0, 'manual', 0.95, 1);
INSERT INTO product_tags VALUES (15, 11, 7, NULL, '2023-11-15', 1, 0.7, 'auto-catalog', 0.78, 1);
INSERT INTO product_tags VALUES (16, 12, 9, 1, '2024-02-01', 0, 0.8, 'manual', 0.85, 1);
INSERT INTO product_tags VALUES (17, 12, 4, 1, '2024-02-01', 0, 0.7, 'manual', 0.78, 1);
INSERT INTO product_tags VALUES (18, 13, 1, NULL, '2024-05-01', 1, 0.9, 'auto-sales', 0.88, 1);
INSERT INTO product_tags VALUES (19, 14, 8, NULL, '2024-03-20', 1, 0.8, 'auto-catalog', 0.85, 1);
INSERT INTO product_tags VALUES (20, 14, 4, 1, '2024-04-01', 0, 0.8, 'manual', 0.82, 1);
INSERT INTO product_tags VALUES (21, 15, 3, 1, '2024-11-01', 0, 0.9, 'manual', 0.9, 1);
INSERT INTO product_tags VALUES (22, 15, 5, 1, '2024-05-10', 0, 0.7, 'manual', 0.75, 1);

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

INSERT INTO orders VALUES (1001, 1, 1, 13, '2024-09-15', 'delivered', 1299.99, 104.0, 0.0, 0.0, 1403.99, NULL);
INSERT INTO orders VALUES (1002, 2, 2, NULL, '2024-09-20', 'delivered', 929.98, 74.4, 9.99, 0.0, 1014.37, NULL);
INSERT INTO orders VALUES (1003, 3, 3, NULL, '2024-10-01', 'delivered', 199.99, 20.0, 5.99, 0.0, 225.98, 'Gift wrap requested');
INSERT INTO orders VALUES (1004, 4, 4, NULL, '2024-10-10', 'delivered', 89.98, 7.2, 5.99, 10.0, 93.17, 'Used coupon FALL10');
INSERT INTO orders VALUES (1005, 5, 5, 14, '2024-10-18', 'delivered', 549.99, 38.5, 0.0, 0.0, 588.49, NULL);
INSERT INTO orders VALUES (1006, 6, 6, NULL, '2024-11-02', 'delivered', 319.98, 32.0, 0.0, 0.0, 351.98, NULL);
INSERT INTO orders VALUES (1007, 7, 7, NULL, '2024-11-15', 'delivered', 899.99, 81.0, 0.0, 50.0, 930.99, 'VIP discount applied');
INSERT INTO orders VALUES (1008, 8, 8, NULL, '2024-11-28', 'delivered', 169.98, 10.63, 5.99, 0.0, 186.6, 'Black Friday order');
INSERT INTO orders VALUES (1009, 9, 9, 15, '2024-12-05', 'delivered', 279.98, 23.52, 0.0, 0.0, 303.5, NULL);
INSERT INTO orders VALUES (1010, 10, 10, NULL, '2024-12-12', 'delivered', 39.99, 3.7, 5.99, 0.0, 49.68, NULL);
INSERT INTO orders VALUES (1011, 11, 11, NULL, '2024-12-20', 'delivered', 499.97, 40.0, 0.0, 25.0, 514.97, 'Holiday sale');
INSERT INTO orders VALUES (1012, 1, 1, 13, '2025-01-05', 'delivered', 249.99, 20.0, 0.0, 0.0, 269.99, NULL);
INSERT INTO orders VALUES (1013, 12, 12, 16, '2025-01-15', 'delivered', 119.99, 10.8, 5.99, 0.0, 136.78, NULL);
INSERT INTO orders VALUES (1014, 2, 2, NULL, '2025-01-28', 'shipped', 149.99, 12.38, 5.99, 0.0, 168.36, NULL);
INSERT INTO orders VALUES (1015, 3, 3, NULL, '2025-02-10', 'shipped', 69.99, 7.0, 5.99, 0.0, 82.98, NULL);
INSERT INTO orders VALUES (1016, 5, 5, 14, '2025-02-20', 'processing', 1349.98, 94.5, 0.0, 0.0, 1444.48, 'Large order');
INSERT INTO orders VALUES (1017, 7, 7, NULL, '2025-03-01', 'processing', 59.99, 5.4, 5.99, 0.0, 71.38, NULL);
INSERT INTO orders VALUES (1018, 8, 8, NULL, '2025-03-10', 'pending', 79.99, 5.0, 5.99, 0.0, 90.98, NULL);
INSERT INTO orders VALUES (1019, 9, 9, 15, '2025-03-15', 'pending', 49.99, 4.2, 5.99, 5.0, 55.18, 'Used coupon SPRING5');
INSERT INTO orders VALUES (1020, 4, 4, NULL, '2025-03-22', 'cancelled', 899.99, 63.0, 0.0, 0.0, 962.99, 'Customer cancelled');

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

INSERT INTO order_items VALUES (1, 1001, 1, 2, 1, 1299.99, 1299.99, 0.0, 104.0, 'delivered');
INSERT INTO order_items VALUES (2, 1002, 2, 3, 1, 899.99, 899.99, 0.0, 72.0, 'delivered');
INSERT INTO order_items VALUES (3, 1002, 5, 6, 1, 29.99, 29.99, 0.0, 2.4, 'delivered');
INSERT INTO order_items VALUES (4, 1003, 4, 15, 1, 199.99, 199.99, 0.0, 20.0, 'delivered');
INSERT INTO order_items VALUES (5, 1004, 5, 7, 2, 29.99, 59.98, 5.0, 4.4, 'delivered');
INSERT INTO order_items VALUES (6, 1004, 15, 19, 1, 19.99, 19.99, 5.0, 1.2, 'delivered');
INSERT INTO order_items VALUES (7, 1004, 15, 20, 1, 19.99, 19.99, 0.0, 1.6, 'delivered');
INSERT INTO order_items VALUES (8, 1005, 3, NULL, 1, 549.99, 549.99, 0.0, 38.5, 'delivered');
INSERT INTO order_items VALUES (9, 1006, 6, 8, 2, 69.99, 139.98, 0.0, 14.0, 'delivered');
INSERT INTO order_items VALUES (10, 1006, 8, 13, 1, 149.99, 149.99, 0.0, 15.0, 'delivered');
INSERT INTO order_items VALUES (11, 1006, 5, 5, 1, 29.99, 29.99, 0.0, 3.0, 'delivered');
INSERT INTO order_items VALUES (12, 1007, 2, 4, 1, 899.99, 899.99, 50.0, 81.0, 'delivered');
INSERT INTO order_items VALUES (13, 1008, 7, 11, 1, 119.99, 119.99, 0.0, 7.5, 'delivered');
INSERT INTO order_items VALUES (14, 1008, 14, NULL, 1, 49.99, 49.99, 0.0, 3.13, 'delivered');
INSERT INTO order_items VALUES (15, 1009, 11, 17, 1, 249.99, 249.99, 0.0, 21.0, 'delivered');
INSERT INTO order_items VALUES (16, 1009, 5, 6, 1, 29.99, 29.99, 0.0, 2.52, 'delivered');
INSERT INTO order_items VALUES (17, 1010, 13, NULL, 1, 39.99, 39.99, 0.0, 3.7, 'delivered');
INSERT INTO order_items VALUES (18, 1011, 11, 18, 1, 249.99, 249.99, 12.5, 20.0, 'delivered');
INSERT INTO order_items VALUES (19, 1011, 4, 16, 1, 199.99, 199.99, 12.5, 16.0, 'delivered');
INSERT INTO order_items VALUES (20, 1011, 14, NULL, 1, 49.99, 49.99, 0.0, 4.0, 'delivered');
INSERT INTO order_items VALUES (21, 1012, 11, 17, 1, 249.99, 249.99, 0.0, 20.0, 'delivered');
INSERT INTO order_items VALUES (22, 1013, 7, 12, 1, 119.99, 119.99, 0.0, 10.8, 'delivered');
INSERT INTO order_items VALUES (23, 1014, 8, 14, 1, 149.99, 149.99, 0.0, 12.38, 'shipped');
INSERT INTO order_items VALUES (24, 1015, 6, 10, 1, 69.99, 69.99, 0.0, 7.0, 'shipped');
INSERT INTO order_items VALUES (25, 1016, 1, 1, 1, 1299.99, 1299.99, 0.0, 91.0, 'processing');
INSERT INTO order_items VALUES (26, 1016, 14, NULL, 1, 49.99, 49.99, 0.0, 3.5, 'processing');
INSERT INTO order_items VALUES (27, 1017, 12, NULL, 1, 59.99, 59.99, 0.0, 5.4, 'processing');
INSERT INTO order_items VALUES (28, 1018, 10, NULL, 1, 79.99, 79.99, 0.0, 5.0, 'pending');
INSERT INTO order_items VALUES (29, 1019, 14, NULL, 1, 49.99, 49.99, 5.0, 4.2, 'pending');
INSERT INTO order_items VALUES (30, 1020, 2, 3, 1, 899.99, 899.99, 0.0, 63.0, 'cancelled');
INSERT INTO order_items VALUES (31, 1001, 14, NULL, 0, 49.99, 0.0, 0.0, 0.0, 'cancelled');
INSERT INTO order_items VALUES (32, 1003, 15, 19, 2, 19.99, 39.98, 0.0, 4.0, 'delivered');
INSERT INTO order_items VALUES (33, 1007, 12, NULL, 1, 59.99, 59.99, 0.0, 5.4, 'delivered');
INSERT INTO order_items VALUES (34, 1012, 9, NULL, 1, 89.99, 89.99, 0.0, 7.2, 'delivered');
INSERT INTO order_items VALUES (35, 1009, 15, 20, 1, 19.99, 19.99, 0.0, 1.68, 'delivered');

CREATE TABLE order_status_history (
    id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id),
    from_status TEXT,
    to_status TEXT NOT NULL,
    changed_at TEXT NOT NULL,
    changed_by TEXT NOT NULL DEFAULT 'system',
    notes TEXT
);

INSERT INTO order_status_history VALUES (1, 1001, NULL, 'pending', '2024-09-15', 'system', 'Order placed');
INSERT INTO order_status_history VALUES (2, 1001, 'pending', 'processing', '2024-09-15', 'system', 'Payment confirmed');
INSERT INTO order_status_history VALUES (3, 1001, 'processing', 'shipped', '2024-09-15', 'warehouse', 'Shipped');
INSERT INTO order_status_history VALUES (4, 1001, 'shipped', 'delivered', '2024-09-15', 'carrier', 'Delivered');
INSERT INTO order_status_history VALUES (5, 1002, NULL, 'pending', '2024-09-20', 'system', 'Order placed');
INSERT INTO order_status_history VALUES (6, 1002, 'pending', 'processing', '2024-09-20', 'system', 'Payment confirmed');
INSERT INTO order_status_history VALUES (7, 1002, 'processing', 'shipped', '2024-09-20', 'warehouse', 'Shipped');
INSERT INTO order_status_history VALUES (8, 1002, 'shipped', 'delivered', '2024-09-20', 'carrier', 'Delivered');
INSERT INTO order_status_history VALUES (9, 1003, NULL, 'pending', '2024-10-01', 'system', 'Order placed');
INSERT INTO order_status_history VALUES (10, 1003, 'pending', 'processing', '2024-10-01', 'system', 'Payment confirmed');
INSERT INTO order_status_history VALUES (11, 1003, 'processing', 'shipped', '2024-10-01', 'warehouse', 'Shipped');
INSERT INTO order_status_history VALUES (12, 1003, 'shipped', 'delivered', '2024-10-01', 'carrier', 'Delivered');
INSERT INTO order_status_history VALUES (13, 1004, NULL, 'pending', '2024-10-10', 'system', 'Order placed');
INSERT INTO order_status_history VALUES (14, 1004, 'pending', 'processing', '2024-10-10', 'system', 'Payment confirmed');
INSERT INTO order_status_history VALUES (15, 1004, 'processing', 'shipped', '2024-10-10', 'warehouse', 'Shipped');
INSERT INTO order_status_history VALUES (16, 1004, 'shipped', 'delivered', '2024-10-10', 'carrier', 'Delivered');
INSERT INTO order_status_history VALUES (17, 1005, NULL, 'pending', '2024-10-18', 'system', 'Order placed');
INSERT INTO order_status_history VALUES (18, 1005, 'pending', 'processing', '2024-10-18', 'system', 'Payment confirmed');
INSERT INTO order_status_history VALUES (19, 1005, 'processing', 'shipped', '2024-10-18', 'warehouse', 'Shipped');
INSERT INTO order_status_history VALUES (20, 1005, 'shipped', 'delivered', '2024-10-18', 'carrier', 'Delivered');
INSERT INTO order_status_history VALUES (21, 1006, NULL, 'pending', '2024-11-02', 'system', 'Order placed');
INSERT INTO order_status_history VALUES (22, 1006, 'pending', 'processing', '2024-11-02', 'system', 'Payment confirmed');
INSERT INTO order_status_history VALUES (23, 1006, 'processing', 'shipped', '2024-11-02', 'warehouse', 'Shipped');
INSERT INTO order_status_history VALUES (24, 1006, 'shipped', 'delivered', '2024-11-02', 'carrier', 'Delivered');
INSERT INTO order_status_history VALUES (25, 1007, NULL, 'pending', '2024-11-15', 'system', 'Order placed');
INSERT INTO order_status_history VALUES (26, 1007, 'pending', 'processing', '2024-11-15', 'system', 'Payment confirmed');
INSERT INTO order_status_history VALUES (27, 1007, 'processing', 'shipped', '2024-11-15', 'warehouse', 'Shipped');
INSERT INTO order_status_history VALUES (28, 1007, 'shipped', 'delivered', '2024-11-15', 'carrier', 'Delivered');
INSERT INTO order_status_history VALUES (29, 1008, NULL, 'pending', '2024-11-28', 'system', 'Order placed');
INSERT INTO order_status_history VALUES (30, 1008, 'pending', 'processing', '2024-11-28', 'system', 'Payment confirmed');
INSERT INTO order_status_history VALUES (31, 1008, 'processing', 'shipped', '2024-11-28', 'warehouse', 'Shipped');
INSERT INTO order_status_history VALUES (32, 1008, 'shipped', 'delivered', '2024-11-28', 'carrier', 'Delivered');
INSERT INTO order_status_history VALUES (33, 1009, NULL, 'pending', '2024-12-05', 'system', 'Order placed');
INSERT INTO order_status_history VALUES (34, 1009, 'pending', 'processing', '2024-12-05', 'system', 'Payment confirmed');
INSERT INTO order_status_history VALUES (35, 1009, 'processing', 'shipped', '2024-12-05', 'warehouse', 'Shipped');
INSERT INTO order_status_history VALUES (36, 1009, 'shipped', 'delivered', '2024-12-05', 'carrier', 'Delivered');
INSERT INTO order_status_history VALUES (37, 1010, NULL, 'pending', '2024-12-12', 'system', 'Order placed');
INSERT INTO order_status_history VALUES (38, 1010, 'pending', 'processing', '2024-12-12', 'system', 'Payment confirmed');
INSERT INTO order_status_history VALUES (39, 1010, 'processing', 'shipped', '2024-12-12', 'warehouse', 'Shipped');
INSERT INTO order_status_history VALUES (40, 1010, 'shipped', 'delivered', '2024-12-12', 'carrier', 'Delivered');
INSERT INTO order_status_history VALUES (41, 1011, NULL, 'pending', '2024-12-20', 'system', 'Order placed');
INSERT INTO order_status_history VALUES (42, 1011, 'pending', 'processing', '2024-12-20', 'system', 'Payment confirmed');
INSERT INTO order_status_history VALUES (43, 1011, 'processing', 'shipped', '2024-12-20', 'warehouse', 'Shipped');
INSERT INTO order_status_history VALUES (44, 1011, 'shipped', 'delivered', '2024-12-20', 'carrier', 'Delivered');
INSERT INTO order_status_history VALUES (45, 1012, NULL, 'pending', '2025-01-05', 'system', 'Order placed');
INSERT INTO order_status_history VALUES (46, 1012, 'pending', 'processing', '2025-01-05', 'system', 'Payment confirmed');
INSERT INTO order_status_history VALUES (47, 1012, 'processing', 'shipped', '2025-01-05', 'warehouse', 'Shipped');
INSERT INTO order_status_history VALUES (48, 1012, 'shipped', 'delivered', '2025-01-05', 'carrier', 'Delivered');
INSERT INTO order_status_history VALUES (49, 1013, NULL, 'pending', '2025-01-15', 'system', 'Order placed');
INSERT INTO order_status_history VALUES (50, 1013, 'pending', 'processing', '2025-01-15', 'system', 'Payment confirmed');
INSERT INTO order_status_history VALUES (51, 1013, 'processing', 'shipped', '2025-01-15', 'warehouse', 'Shipped');
INSERT INTO order_status_history VALUES (52, 1013, 'shipped', 'delivered', '2025-01-15', 'carrier', 'Delivered');
INSERT INTO order_status_history VALUES (53, 1014, NULL, 'pending', '2025-01-28', 'system', 'Order placed');
INSERT INTO order_status_history VALUES (54, 1014, 'pending', 'processing', '2025-01-28', 'system', 'Payment confirmed');
INSERT INTO order_status_history VALUES (55, 1014, 'processing', 'shipped', '2025-01-28', 'warehouse', 'Shipped');
INSERT INTO order_status_history VALUES (56, 1015, NULL, 'pending', '2025-02-10', 'system', 'Order placed');
INSERT INTO order_status_history VALUES (57, 1015, 'pending', 'processing', '2025-02-10', 'system', 'Payment confirmed');
INSERT INTO order_status_history VALUES (58, 1015, 'processing', 'shipped', '2025-02-10', 'warehouse', 'Shipped');
INSERT INTO order_status_history VALUES (59, 1016, NULL, 'pending', '2025-02-20', 'system', 'Order placed');
INSERT INTO order_status_history VALUES (60, 1016, 'pending', 'processing', '2025-02-20', 'system', 'Payment confirmed');
INSERT INTO order_status_history VALUES (61, 1017, NULL, 'pending', '2025-03-01', 'system', 'Order placed');
INSERT INTO order_status_history VALUES (62, 1017, 'pending', 'processing', '2025-03-01', 'system', 'Payment confirmed');
INSERT INTO order_status_history VALUES (63, 1018, NULL, 'pending', '2025-03-10', 'system', 'Order placed');
INSERT INTO order_status_history VALUES (64, 1019, NULL, 'pending', '2025-03-15', 'system', 'Order placed');
INSERT INTO order_status_history VALUES (65, 1020, NULL, 'pending', '2025-03-22', 'system', 'Order placed');
INSERT INTO order_status_history VALUES (66, 1020, 'pending', 'cancelled', '2025-03-22', 'customer', 'Customer cancelled');

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

INSERT INTO payments VALUES (1, 1001, 1, 1403.99, 'credit_card', 'completed', 'TXN-20240915-001', 'stripe', '2024-09-15 10:23:00', 'USD', 40.72);
INSERT INTO payments VALUES (2, 1002, 2, 1014.37, 'credit_card', 'completed', 'TXN-20240920-002', 'stripe', '2024-09-20 14:05:00', 'USD', 29.42);
INSERT INTO payments VALUES (3, 1003, 3, 225.98, 'paypal', 'completed', 'TXN-20241001-003', 'paypal', '2024-10-01 09:12:00', 'USD', 6.78);
INSERT INTO payments VALUES (4, 1004, 4, 93.17, 'debit_card', 'completed', 'TXN-20241010-004', 'stripe', '2024-10-10 11:45:00', 'USD', 2.7);
INSERT INTO payments VALUES (5, 1005, 5, 588.49, 'credit_card', 'completed', 'TXN-20241018-005', 'stripe', '2024-10-18 16:30:00', 'USD', 17.07);
INSERT INTO payments VALUES (6, 1006, 6, 351.98, 'credit_card', 'completed', 'TXN-20241102-006', 'stripe', '2024-11-02 13:20:00', 'USD', 10.21);
INSERT INTO payments VALUES (7, 1007, 7, 930.99, 'credit_card', 'completed', 'TXN-20241115-007', 'stripe', '2024-11-15 10:55:00', 'USD', 27.0);
INSERT INTO payments VALUES (8, 1008, 8, 186.6, 'paypal', 'completed', 'TXN-20241128-008', 'paypal', '2024-11-28 08:10:00', 'USD', 5.6);
INSERT INTO payments VALUES (9, 1009, 9, 303.5, 'credit_card', 'completed', 'TXN-20241205-009', 'stripe', '2024-12-05 15:40:00', 'USD', 8.8);
INSERT INTO payments VALUES (10, 1010, 10, 49.68, 'debit_card', 'completed', 'TXN-20241212-010', 'stripe', '2024-12-12 12:05:00', 'USD', 1.44);
INSERT INTO payments VALUES (11, 1011, 11, 514.97, 'credit_card', 'completed', 'TXN-20241220-011', 'stripe', '2024-12-20 17:22:00', 'USD', 14.93);
INSERT INTO payments VALUES (12, 1012, 1, 269.99, 'credit_card', 'completed', 'TXN-20250105-012', 'stripe', '2025-01-05 09:30:00', 'USD', 7.83);
INSERT INTO payments VALUES (13, 1013, 12, 136.78, 'paypal', 'completed', 'TXN-20250115-013', 'paypal', '2025-01-15 14:18:00', 'USD', 4.1);
INSERT INTO payments VALUES (14, 1014, 2, 168.36, 'credit_card', 'completed', 'TXN-20250128-014', 'stripe', '2025-01-28 11:45:00', 'USD', 4.88);
INSERT INTO payments VALUES (15, 1015, 3, 82.98, 'debit_card', 'completed', 'TXN-20250210-015', 'stripe', '2025-02-10 10:00:00', 'USD', 2.41);
INSERT INTO payments VALUES (16, 1016, 5, 1444.48, 'credit_card', 'completed', 'TXN-20250220-016', 'stripe', '2025-02-20 16:50:00', 'USD', 41.89);
INSERT INTO payments VALUES (17, 1017, 7, 71.38, 'paypal', 'completed', 'TXN-20250301-017', 'paypal', '2025-03-01 13:25:00', 'USD', 2.14);
INSERT INTO payments VALUES (18, 1018, 8, 90.98, 'credit_card', 'pending', 'TXN-20250310-018', 'stripe', '2025-03-10', 'USD', 0.0);
INSERT INTO payments VALUES (19, 1019, 9, 55.18, 'debit_card', 'pending', 'TXN-20250315-019', 'stripe', '2025-03-15', 'USD', 0.0);
INSERT INTO payments VALUES (20, 1020, 4, 962.99, 'credit_card', 'refunded', 'TXN-20250322-020', 'stripe', '2025-03-22 09:15:00', 'USD', 27.93);

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

INSERT INTO refunds VALUES (1, 1020, 20, 4, 962.99, 'Customer cancelled order', 'completed', 'original_payment', '2025-03-22', '2025-03-23', 'agent_sarah', 'Full refund for cancelled order');
INSERT INTO refunds VALUES (2, 1003, 3, 3, 39.98, 'Defective mugs received', 'completed', 'store_credit', '2024-10-15', '2024-10-18', 'agent_mike', 'Partial refund for 2 damaged mugs');
INSERT INTO refunds VALUES (3, 1004, 4, 4, 19.99, 'Wrong color received', 'completed', 'original_payment', '2024-10-20', '2024-10-22', 'agent_jenny', 'Refund for charcoal mug, wanted teal');
INSERT INTO refunds VALUES (4, 1008, 8, 8, 49.99, 'Item not as described', 'processing', 'original_payment', '2024-12-10', NULL, NULL, 'USB-C hub missing ports');
INSERT INTO refunds VALUES (5, 1006, 6, 6, 29.99, 'Size too small', 'completed', 'original_payment', '2024-11-15', '2024-11-18', 'agent_sarah', 'Refund for t-shirt, wrong size ordered');
INSERT INTO refunds VALUES (6, 1013, 13, 12, 119.99, 'Shoes too tight', 'requested', 'original_payment', '2025-02-01', NULL, NULL, 'Customer wants exchange or refund');

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

INSERT INTO gift_cards VALUES (1, 'GC-ABCD-1234', 25.0, 50.0, 1, 'carol@email.com', 'Happy Birthday Carol!', 1, '2024-11-01', '2025-11-01', '2025-01-15');
INSERT INTO gift_cards VALUES (2, 'GC-EFGH-5678', 100.0, 100.0, 2, 'dave@email.com', 'Merry Christmas!', 1, '2024-12-20', '2025-12-20', NULL);
INSERT INTO gift_cards VALUES (3, 'GC-IJKL-9012', 0.0, 25.0, 7, 'henry@email.com', 'Thanks for your help!', 0, '2024-08-15', '2025-08-15', '2024-11-28');
INSERT INTO gift_cards VALUES (4, 'GC-MNOP-3456', 75.0, 75.0, 11, 'ivy@email.com', 'Enjoy some shopping!', 1, '2025-02-14', '2026-02-14', NULL);
INSERT INTO gift_cards VALUES (5, 'GC-QRST-7890', 39.98, 50.0, 6, 'eve@email.com', 'Just because!', 1, '2025-01-10', '2026-01-10', '2025-02-20');

CREATE TABLE gift_card_transactions (
    id INTEGER PRIMARY KEY,
    gift_card_id INTEGER NOT NULL REFERENCES gift_cards(id),
    order_id INTEGER REFERENCES orders(id),
    amount REAL NOT NULL,
    transaction_type TEXT NOT NULL,
    created_at TEXT NOT NULL,
    notes TEXT
);

INSERT INTO gift_card_transactions VALUES (1, 1, NULL, 50.0, 'purchase', '2024-02-14 10:00:00', 'Gift card purchased');
INSERT INTO gift_card_transactions VALUES (2, 2, NULL, 100.0, 'purchase', '2024-03-01 09:00:00', 'Gift card purchased');
INSERT INTO gift_card_transactions VALUES (3, 2, 1007, -25.0, 'redemption', '2024-06-15 14:00:00', 'Applied to order #7');
INSERT INTO gift_card_transactions VALUES (4, 2, 1014, -50.0, 'redemption', '2024-07-10 10:00:00', 'Applied to order #14');
INSERT INTO gift_card_transactions VALUES (5, 3, NULL, 75.0, 'purchase', '2024-04-10 11:00:00', 'Gift card purchased');
INSERT INTO gift_card_transactions VALUES (6, 4, NULL, 25.0, 'purchase', '2024-05-01 08:00:00', 'Gift card purchased');
INSERT INTO gift_card_transactions VALUES (7, 4, 1017, -25.0, 'redemption', '2024-07-20 10:00:00', 'Applied to order #17');
INSERT INTO gift_card_transactions VALUES (8, 5, NULL, 200.0, 'purchase', '2024-06-01 10:00:00', 'Corporate gift card');

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

INSERT INTO warehouses VALUES (1, 'East Hub', 'WH-EAST', '100 Industrial Pkwy', 'Newark', 'NJ', '07101', 'US', 'mgr.east@shoplocal.com', '555-9001', 50000, 1);
INSERT INTO warehouses VALUES (2, 'West Hub', 'WH-WEST', '200 Commerce Dr', 'Reno', 'NV', '89501', 'US', 'mgr.west@shoplocal.com', '555-9002', 45000, 1);
INSERT INTO warehouses VALUES (3, 'Central Depot', 'WH-CENT', '300 Logistics Blvd', 'Memphis', 'TN', '38101', 'US', 'mgr.central@shoplocal.com', '555-9003', 60000, 1);
INSERT INTO warehouses VALUES (4, 'South Center', 'WH-SOUTH', '400 Freight Rd', 'Dallas', 'TX', '75201', 'US', 'mgr.south@shoplocal.com', '555-9004', 35000, 1);

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

INSERT INTO inventory_levels VALUES (1, 1, 1, 30, 5, 25, 10, 20, '2025-02-01', '2025-03-20', 850.0);
INSERT INTO inventory_levels VALUES (2, 1, 2, 15, 2, 13, 10, 20, '2025-01-15', '2025-03-18', 850.0);
INSERT INTO inventory_levels VALUES (3, 2, 1, 50, 8, 42, 15, 30, '2025-02-15', '2025-03-22', 520.0);
INSERT INTO inventory_levels VALUES (4, 2, 3, 35, 3, 32, 15, 30, '2025-01-20', '2025-03-15', 520.0);
INSERT INTO inventory_levels VALUES (5, 5, 3, 200, 10, 190, 50, 100, '2025-03-01', '2025-03-25', 8.5);
INSERT INTO inventory_levels VALUES (6, 4, 2, 80, 5, 75, 20, 40, '2025-02-10', '2025-03-20', 85.0);
INSERT INTO inventory_levels VALUES (7, 6, 1, 100, 8, 92, 25, 50, '2025-02-20', '2025-03-18', 25.0);
INSERT INTO inventory_levels VALUES (8, 7, 4, 40, 3, 37, 10, 25, '2025-01-25', '2025-03-10', 42.0);
INSERT INTO inventory_levels VALUES (9, 9, 3, 25, 2, 23, 8, 15, '2025-01-10', '2025-03-05', 35.0);
INSERT INTO inventory_levels VALUES (10, 10, 1, 18, 1, 17, 8, 15, '2025-02-05', '2025-03-10', 30.0);
INSERT INTO inventory_levels VALUES (11, 11, 2, 35, 4, 31, 10, 20, '2025-02-25', '2025-03-22', 110.0);
INSERT INTO inventory_levels VALUES (12, 12, 3, 60, 5, 55, 15, 30, '2025-03-01', '2025-03-20', 18.0);
INSERT INTO inventory_levels VALUES (13, 13, 1, 45, 0, 45, 10, 30, '2025-01-05', '2025-03-12', 12.0);
INSERT INTO inventory_levels VALUES (14, 14, 4, 90, 6, 84, 20, 50, '2025-02-28', '2025-03-25', 15.0);
INSERT INTO inventory_levels VALUES (15, 15, 3, 150, 10, 140, 30, 60, '2025-03-05', '2025-03-26', 5.5);

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

INSERT INTO vendors VALUES (1, 'GlobalTech Supply', 'James Wong', 'james@globaltech.example.com', '555-8001', '88 Tech Park Rd', 'Shenzhen', 'CN', 'Net 30', 14, 4.5, 1);
INSERT INTO vendors VALUES (2, 'FabricWorld Inc', 'Maria Lopez', 'maria@fabricworld.example.com', '555-8002', '45 Textile Ave', 'Dhaka', 'BD', 'Net 45', 21, 4.2, 1);
INSERT INTO vendors VALUES (3, 'HomeGoods Direct', 'Tom Fischer', 'tom@homegoods.example.com', '555-8003', '12 Factory Ln', 'Stuttgart', 'DE', 'Net 30', 18, 4.7, 1);
INSERT INTO vendors VALUES (4, 'BookPrint Co', 'Sarah Mills', 'sarah@bookprint.example.com', '555-8004', '200 Press Blvd', 'London', 'UK', 'Net 60', 10, 4.8, 1);
INSERT INTO vendors VALUES (5, 'AudioParts Ltd', 'Kenji Tanaka', 'kenji@audioparts.example.com', '555-8005', '7 Sound St', 'Osaka', 'JP', 'Net 30', 12, 4.4, 1);

CREATE TABLE vendor_products (
    id INTEGER PRIMARY KEY,
    vendor_id INTEGER NOT NULL REFERENCES vendors(id),
    product_id INTEGER NOT NULL REFERENCES products(id),
    unit_cost REAL NOT NULL,
    lead_time_days INTEGER NOT NULL,
    is_preferred INTEGER NOT NULL DEFAULT 0,
    min_order_quantity INTEGER NOT NULL DEFAULT 1
);

INSERT INTO vendor_products VALUES (1, 1, 1, 850.0, 14, 1, 1);
INSERT INTO vendor_products VALUES (2, 1, 2, 520.0, 14, 1, 1);
INSERT INTO vendor_products VALUES (3, 2, 5, 8.5, 21, 1, 1);
INSERT INTO vendor_products VALUES (4, 2, 6, 25.0, 21, 1, 1);
INSERT INTO vendor_products VALUES (5, 5, 4, 85.0, 12, 1, 1);
INSERT INTO vendor_products VALUES (6, 3, 9, 35.0, 18, 1, 1);
INSERT INTO vendor_products VALUES (7, 3, 10, 30.0, 18, 0, 1);
INSERT INTO vendor_products VALUES (8, 4, 13, 12.0, 10, 0, 1);
INSERT INTO vendor_products VALUES (9, 1, 14, 15.0, 14, 0, 1);
INSERT INTO vendor_products VALUES (10, 3, 15, 5.5, 18, 0, 1);
INSERT INTO vendor_products VALUES (11, 2, 7, 42.0, 21, 0, 1);
INSERT INTO vendor_products VALUES (12, 1, 11, 110.0, 14, 0, 1);

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

INSERT INTO purchase_orders VALUES (1, 1, 'received', '2024-12-01', '2024-12-15', '2024-12-14', 1, 17000.0, 'Q1 restock');
INSERT INTO purchase_orders VALUES (2, 1, 'received', '2024-12-05', '2024-12-19', '2024-12-20', 1, 15600.0, 'Holiday restock');
INSERT INTO purchase_orders VALUES (3, 2, 'received', '2025-01-10', '2025-01-31', '2025-02-02', 3, 850.0, 'Spring collection');
INSERT INTO purchase_orders VALUES (4, 2, 'received', '2025-01-10', '2025-01-31', '2025-02-01', 1, 1250.0, NULL);
INSERT INTO purchase_orders VALUES (5, 5, 'received', '2025-01-15', '2025-01-27', '2025-01-28', 2, 3400.0, NULL);
INSERT INTO purchase_orders VALUES (6, 3, 'received', '2024-12-20', '2025-01-07', '2025-01-08', 3, 525.0, NULL);
INSERT INTO purchase_orders VALUES (7, 3, 'received', '2025-01-20', '2025-02-07', '2025-02-05', 1, 450.0, 'Fast delivery');
INSERT INTO purchase_orders VALUES (8, 4, 'received', '2024-12-15', '2024-12-25', '2024-12-24', 1, 360.0, NULL);
INSERT INTO purchase_orders VALUES (9, 1, 'shipped', '2025-03-01', '2025-03-15', NULL, 4, 750.0, 'In transit');
INSERT INTO purchase_orders VALUES (10, 3, 'shipped', '2025-03-05', '2025-03-23', NULL, 3, 330.0, NULL);
INSERT INTO purchase_orders VALUES (11, 2, 'pending', '2025-03-15', '2025-04-05', NULL, 4, 1050.0, 'New color options');
INSERT INTO purchase_orders VALUES (12, 1, 'pending', '2025-03-18', '2025-04-01', NULL, 2, 2200.0, 'Q2 forecast');

CREATE TABLE purchase_order_lines (
    id INTEGER PRIMARY KEY,
    purchase_order_id INTEGER NOT NULL REFERENCES purchase_orders(id),
    product_id INTEGER NOT NULL REFERENCES products(id),
    quantity INTEGER NOT NULL,
    unit_cost REAL NOT NULL,
    total_cost REAL NOT NULL
);

INSERT INTO purchase_order_lines VALUES (1, 1, 1, 20, 850.0, 17000.0);
INSERT INTO purchase_order_lines VALUES (2, 2, 2, 30, 520.0, 15600.0);
INSERT INTO purchase_order_lines VALUES (3, 3, 5, 100, 8.5, 850.0);
INSERT INTO purchase_order_lines VALUES (4, 4, 6, 50, 25.0, 1250.0);
INSERT INTO purchase_order_lines VALUES (5, 5, 4, 40, 85.0, 3400.0);
INSERT INTO purchase_order_lines VALUES (6, 6, 9, 15, 35.0, 525.0);
INSERT INTO purchase_order_lines VALUES (7, 7, 10, 15, 30.0, 450.0);
INSERT INTO purchase_order_lines VALUES (8, 8, 13, 30, 12.0, 360.0);
INSERT INTO purchase_order_lines VALUES (9, 9, 14, 50, 15.0, 750.0);
INSERT INTO purchase_order_lines VALUES (10, 10, 15, 60, 5.5, 330.0);
INSERT INTO purchase_order_lines VALUES (11, 11, 7, 25, 42.0, 1050.0);
INSERT INTO purchase_order_lines VALUES (12, 12, 11, 20, 110.0, 2200.0);

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

INSERT INTO inventory_movements VALUES (1, 1, 1, 'inbound', 20, 'PO-1', 'Received from GlobalTech', 'mgr.east@shoplocal.com', '2024-12-14', 17000.0);
INSERT INTO inventory_movements VALUES (2, 2, 1, 'inbound', 30, 'PO-2', 'Received from GlobalTech', 'mgr.east@shoplocal.com', '2024-12-20', 15600.0);
INSERT INTO inventory_movements VALUES (3, 1, 1, 'outbound', -1, 'ORD-1001', 'Shipped to customer', 'mgr.east@shoplocal.com', '2024-09-16', 850.0);
INSERT INTO inventory_movements VALUES (4, 2, 1, 'outbound', -1, 'ORD-1002', 'Shipped to customer', 'mgr.east@shoplocal.com', '2024-09-21', 520.0);
INSERT INTO inventory_movements VALUES (5, 5, 3, 'inbound', 100, 'PO-3', 'Received from FabricWorld', 'mgr.central@shoplocal.com', '2025-02-02', 850.0);
INSERT INTO inventory_movements VALUES (6, 5, 3, 'outbound', -2, 'ORD-1004', 'Shipped to customer', 'mgr.central@shoplocal.com', '2024-10-11', 17.0);
INSERT INTO inventory_movements VALUES (7, 4, 2, 'inbound', 40, 'PO-5', 'Received from AudioParts', 'mgr.west@shoplocal.com', '2025-01-28', 3400.0);
INSERT INTO inventory_movements VALUES (8, 4, 2, 'outbound', -1, 'ORD-1003', 'Shipped to customer', 'mgr.west@shoplocal.com', '2024-10-02', 85.0);
INSERT INTO inventory_movements VALUES (9, 6, 1, 'inbound', 50, 'PO-4', 'Received from FabricWorld', 'mgr.east@shoplocal.com', '2025-02-01', 1250.0);
INSERT INTO inventory_movements VALUES (10, 6, 1, 'outbound', -2, 'ORD-1006', 'Shipped to customer', 'mgr.east@shoplocal.com', '2024-11-03', 50.0);
INSERT INTO inventory_movements VALUES (11, 11, 2, 'outbound', -1, 'ORD-1009', 'Shipped to customer', 'mgr.west@shoplocal.com', '2024-12-06', 110.0);
INSERT INTO inventory_movements VALUES (12, 1, 1, 'transfer', -5, 'TRF-001', 'Transfer to West Hub', 'mgr.east@shoplocal.com', '2025-01-10', 4250.0);
INSERT INTO inventory_movements VALUES (13, 1, 2, 'transfer', 5, 'TRF-001', 'Transfer from East Hub', 'mgr.west@shoplocal.com', '2025-01-10', 4250.0);
INSERT INTO inventory_movements VALUES (14, 9, 3, 'inbound', 15, 'PO-6', 'Received from HomeGoods', 'mgr.central@shoplocal.com', '2025-01-08', 525.0);
INSERT INTO inventory_movements VALUES (15, 13, 1, 'inbound', 30, 'PO-8', 'Received from BookPrint', 'mgr.east@shoplocal.com', '2024-12-24', 360.0);
INSERT INTO inventory_movements VALUES (16, 15, 3, 'outbound', -3, 'ORD-1004', 'Shipped to customer', 'mgr.central@shoplocal.com', '2024-10-11', 16.5);
INSERT INTO inventory_movements VALUES (17, 10, 1, 'inbound', 15, 'PO-7', 'Received from HomeGoods', 'mgr.east@shoplocal.com', '2025-02-05', 450.0);
INSERT INTO inventory_movements VALUES (18, 14, 4, 'outbound', -1, 'ORD-1008', 'Shipped to customer', 'mgr.south@shoplocal.com', '2024-11-29', 15.0);

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

INSERT INTO shipping_carriers VALUES (1, 'FastShip Express', 'FSE', 'https://fastship.example.com', '555-7001', 'https://fastship.example.com/track/{tracking}', 1, 3, 4.6, 'support@fastship.example.com');
INSERT INTO shipping_carriers VALUES (2, 'EcoShip Ground', 'ESG', 'https://ecoship.example.com', '555-7002', 'https://ecoship.example.com/track/{tracking}', 1, 5, 4.2, 'help@ecoship.example.com');
INSERT INTO shipping_carriers VALUES (3, 'PrimeLogistics', 'PLG', 'https://primelogistics.example.com', '555-7003', 'https://primelogistics.example.com/track/{tracking}', 1, 2, 4.8, 'biz@primelogistics.example.com');
INSERT INTO shipping_carriers VALUES (4, 'BudgetFreight', 'BGF', 'https://budgetfreight.example.com', '555-7004', 'https://budgetfreight.example.com/track/{tracking}', 0, 7, 3.5, 'cs@budgetfreight.example.com');

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

INSERT INTO delivery_zones VALUES (1, 'Northeast', 'NY,NJ,PA,MA,CT,RI,VT,NH,ME', 5.99, 1.5, 2, 4, 1, 'FastShip Express');
INSERT INTO delivery_zones VALUES (2, 'Southeast', 'FL,GA,SC,NC,VA,TN,AL,MS,LA,AR', 5.99, 1.75, 3, 5, 1, 'EcoShip Ground');
INSERT INTO delivery_zones VALUES (3, 'Midwest', 'IL,OH,MI,IN,WI,MN,IA,MO,KS,NE,SD,ND', 6.99, 1.75, 3, 5, 1, 'EcoShip Ground');
INSERT INTO delivery_zones VALUES (4, 'Southwest', 'TX,AZ,NM,OK', 6.99, 2.0, 3, 6, 1, 'FastShip Express');
INSERT INTO delivery_zones VALUES (5, 'West Coast', 'CA,OR,WA', 5.99, 1.5, 2, 4, 1, 'PrimeLogistics');
INSERT INTO delivery_zones VALUES (6, 'Mountain', 'CO,UT,NV,ID,MT,WY', 7.99, 2.25, 4, 6, 1, 'EcoShip Ground');
INSERT INTO delivery_zones VALUES (7, 'Pacific', 'HI,AK', 12.99, 3.5, 5, 10, 1, 'FastShip Express');
INSERT INTO delivery_zones VALUES (8, 'National Express', 'ALL', 9.99, 2.0, 1, 3, 1, 'PrimeLogistics');

CREATE TABLE zone_carrier_rates (
    id INTEGER PRIMARY KEY,
    zone_id INTEGER NOT NULL REFERENCES delivery_zones(id),
    carrier_id INTEGER NOT NULL REFERENCES shipping_carriers(id),
    rate_multiplier REAL NOT NULL DEFAULT 1.0,
    is_active INTEGER NOT NULL DEFAULT 1
);

INSERT INTO zone_carrier_rates VALUES (1, 1, 1, 1.0, 1);
INSERT INTO zone_carrier_rates VALUES (2, 2, 2, 1.0, 1);
INSERT INTO zone_carrier_rates VALUES (3, 3, 2, 1.0, 1);
INSERT INTO zone_carrier_rates VALUES (4, 4, 1, 1.0, 1);
INSERT INTO zone_carrier_rates VALUES (5, 5, 3, 1.0, 1);
INSERT INTO zone_carrier_rates VALUES (6, 6, 2, 1.0, 1);
INSERT INTO zone_carrier_rates VALUES (7, 7, 1, 1.0, 1);
INSERT INTO zone_carrier_rates VALUES (8, 8, 3, 1.0, 1);

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

INSERT INTO shipments VALUES (1, 1001, 1, 'FS-100001-US', 'delivered', '2024-09-16', '2024-09-19', '2024-09-18', 2.3, 0.0, 1);
INSERT INTO shipments VALUES (2, 1002, 1, 'FS-100002-US', 'delivered', '2024-09-21', '2024-09-24', '2024-09-24', 0.39, 9.99, 0);
INSERT INTO shipments VALUES (3, 1003, 2, 'ES-200001-US', 'delivered', '2024-10-02', '2024-10-07', '2024-10-06', 1.02, 5.99, 0);
INSERT INTO shipments VALUES (4, 1004, 2, 'ES-200002-US', 'delivered', '2024-10-11', '2024-10-16', '2024-10-15', 0.75, 5.99, 0);
INSERT INTO shipments VALUES (5, 1005, 1, 'FS-100003-US', 'delivered', '2024-10-19', '2024-10-22', '2024-10-21', 0.48, 0.0, 0);
INSERT INTO shipments VALUES (6, 1006, 1, 'FS-100004-US', 'delivered', '2024-11-03', '2024-11-06', '2024-11-05', 1.3, 0.0, 0);
INSERT INTO shipments VALUES (7, 1007, 3, 'PL-300001-US', 'delivered', '2024-11-16', '2024-11-18', '2024-11-18', 1.09, 0.0, 1);
INSERT INTO shipments VALUES (8, 1008, 2, 'ES-200003-US', 'delivered', '2024-11-29', '2024-12-04', '2024-12-03', 0.82, 5.99, 0);
INSERT INTO shipments VALUES (9, 1009, 1, 'FS-100005-US', 'delivered', '2024-12-06', '2024-12-09', '2024-12-08', 0.6, 0.0, 0);
INSERT INTO shipments VALUES (10, 1010, 2, 'ES-200004-US', 'delivered', '2024-12-13', '2024-12-18', '2024-12-17', 0.55, 5.99, 0);
INSERT INTO shipments VALUES (11, 1011, 3, 'PL-300002-US', 'delivered', '2024-12-21', '2024-12-23', '2024-12-23', 0.49, 0.0, 1);
INSERT INTO shipments VALUES (12, 1012, 1, 'FS-100006-US', 'delivered', '2025-01-06', '2025-01-09', '2025-01-08', 3.25, 0.0, 0);
INSERT INTO shipments VALUES (13, 1013, 2, 'ES-200005-US', 'delivered', '2025-01-16', '2025-01-21', '2025-01-20', 0.7, 5.99, 0);
INSERT INTO shipments VALUES (14, 1014, 1, 'FS-100007-US', 'in_transit', '2025-01-29', '2025-02-01', NULL, 0.47, 5.99, 0);
INSERT INTO shipments VALUES (15, 1015, 2, 'ES-200006-US', 'in_transit', '2025-02-11', '2025-02-16', NULL, 0.65, 5.99, 0);
INSERT INTO shipments VALUES (16, 1016, 3, 'PL-300003-US', 'preparing', NULL, NULL, NULL, 2.22, 0.0, 1);
INSERT INTO shipments VALUES (17, 1017, 2, 'ES-200007-US', 'preparing', NULL, NULL, NULL, 0.9, 5.99, 0);
INSERT INTO shipments VALUES (18, 1018, 2, 'ES-200008-US', 'preparing', NULL, NULL, NULL, 2.8, 5.99, 0);

CREATE TABLE shipment_items (
    id INTEGER PRIMARY KEY,
    shipment_id INTEGER NOT NULL REFERENCES shipments(id),
    order_item_id INTEGER NOT NULL REFERENCES order_items(id),
    quantity INTEGER NOT NULL
);

INSERT INTO shipment_items VALUES (1, 1, 1, 1);
INSERT INTO shipment_items VALUES (2, 1, 31, 0);
INSERT INTO shipment_items VALUES (3, 2, 2, 1);
INSERT INTO shipment_items VALUES (4, 2, 3, 1);
INSERT INTO shipment_items VALUES (5, 3, 4, 1);
INSERT INTO shipment_items VALUES (6, 3, 32, 2);
INSERT INTO shipment_items VALUES (7, 4, 5, 2);
INSERT INTO shipment_items VALUES (8, 4, 6, 1);
INSERT INTO shipment_items VALUES (9, 4, 7, 1);
INSERT INTO shipment_items VALUES (10, 5, 8, 1);
INSERT INTO shipment_items VALUES (11, 6, 9, 2);
INSERT INTO shipment_items VALUES (12, 6, 10, 1);
INSERT INTO shipment_items VALUES (13, 6, 11, 1);
INSERT INTO shipment_items VALUES (14, 7, 12, 1);
INSERT INTO shipment_items VALUES (15, 7, 33, 1);
INSERT INTO shipment_items VALUES (16, 8, 13, 1);
INSERT INTO shipment_items VALUES (17, 8, 14, 1);
INSERT INTO shipment_items VALUES (18, 9, 15, 1);
INSERT INTO shipment_items VALUES (19, 9, 16, 1);
INSERT INTO shipment_items VALUES (20, 9, 35, 1);
INSERT INTO shipment_items VALUES (21, 10, 17, 1);
INSERT INTO shipment_items VALUES (22, 11, 18, 1);
INSERT INTO shipment_items VALUES (23, 11, 19, 1);
INSERT INTO shipment_items VALUES (24, 11, 20, 1);
INSERT INTO shipment_items VALUES (25, 12, 21, 1);
INSERT INTO shipment_items VALUES (26, 12, 34, 1);
INSERT INTO shipment_items VALUES (27, 13, 22, 1);
INSERT INTO shipment_items VALUES (28, 14, 23, 1);
INSERT INTO shipment_items VALUES (29, 15, 24, 1);
INSERT INTO shipment_items VALUES (30, 16, 25, 1);
INSERT INTO shipment_items VALUES (31, 16, 26, 1);
INSERT INTO shipment_items VALUES (32, 17, 27, 1);
INSERT INTO shipment_items VALUES (33, 18, 28, 1);

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

INSERT INTO return_requests VALUES (1, 1003, 3, 'Defective product', 'completed', '2024-10-12', '2024-10-14', 39.98, 'store_credit', 1, 'Two mugs arrived cracked');
INSERT INTO return_requests VALUES (2, 1004, 4, 'Wrong item received', 'completed', '2024-10-18', '2024-10-19', 19.99, 'refund', 2, 'Received charcoal instead of teal mug');
INSERT INTO return_requests VALUES (3, 1006, 6, 'Size too small', 'completed', '2024-11-10', '2024-11-12', 29.99, 'refund', 1, 'T-shirt size S too tight');
INSERT INTO return_requests VALUES (4, 1008, 8, 'Item not as described', 'approved', '2024-12-08', '2024-12-10', 49.99, 'refund', 3, 'USB-C hub missing 2 of 7 ports');
INSERT INTO return_requests VALUES (5, 1013, 12, 'Does not fit', 'requested', '2025-01-28', NULL, 119.99, 'refund', NULL, 'Sneakers too narrow');
INSERT INTO return_requests VALUES (6, 1009, 9, 'Changed mind', 'denied', '2024-12-20', '2024-12-22', 0.0, NULL, 2, 'Past return window');
INSERT INTO return_requests VALUES (7, 1011, 11, 'Better price found', 'requested', '2025-01-05', NULL, 49.99, 'refund', NULL, 'Wants to return USB-C hub');
INSERT INTO return_requests VALUES (8, 1020, 4, 'Order cancelled', 'completed', '2025-03-22', '2025-03-22', 962.99, 'refund', 1, 'Full order cancellation');

CREATE TABLE return_items (
    id INTEGER PRIMARY KEY,
    return_request_id INTEGER NOT NULL REFERENCES return_requests(id),
    order_item_id INTEGER NOT NULL REFERENCES order_items(id),
    quantity INTEGER NOT NULL,
    reason TEXT NOT NULL,
    condition TEXT NOT NULL DEFAULT 'unopened'
);

INSERT INTO return_items VALUES (1, 1, 4, 1, 'Defective product', 'opened');
INSERT INTO return_items VALUES (2, 2, 5, 1, 'Wrong item received', 'opened');
INSERT INTO return_items VALUES (3, 3, 9, 1, 'Size too small', 'opened');
INSERT INTO return_items VALUES (4, 4, 13, 1, 'Item not as described', 'opened');
INSERT INTO return_items VALUES (5, 5, 22, 1, 'Does not fit', 'opened');
INSERT INTO return_items VALUES (6, 6, 15, 1, 'Changed mind', 'opened');
INSERT INTO return_items VALUES (7, 7, 18, 1, 'Better price found', 'opened');
INSERT INTO return_items VALUES (8, 8, 30, 1, 'Order cancelled', 'opened');

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

INSERT INTO discount_codes VALUES (1, 'WELCOME10', 'Welcome discount for new customers', 'percentage', 10.0, 25.0, 500, 142, '2024-01-01', '2025-12-31', 1, 'admin');
INSERT INTO discount_codes VALUES (2, 'FALL10', 'Fall season $10 off', 'fixed', 10.0, 50.0, 200, 88, '2024-09-01', '2024-11-30', 0, 'admin');
INSERT INTO discount_codes VALUES (3, 'HOLIDAY25', 'Holiday season 25% off', 'percentage', 25.0, 100.0, 300, 156, '2024-11-25', '2024-12-31', 0, 'admin');
INSERT INTO discount_codes VALUES (4, 'SPRING5', 'Spring $5 off any order', 'fixed', 5.0, 20.0, 1000, 23, '2025-03-01', '2025-05-31', 1, 'admin');
INSERT INTO discount_codes VALUES (5, 'VIP50', 'VIP customer $50 off', 'fixed', 50.0, 200.0, 50, 12, '2024-01-01', '2025-12-31', 1, 'admin');
INSERT INTO discount_codes VALUES (6, 'FREESHIP', 'Free shipping on orders over $75', 'free_shipping', 0.0, 75.0, 999, 210, '2024-06-01', '2025-06-30', 1, 'admin');

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

INSERT INTO discount_redemptions VALUES (1, 2, 4, 1004, 10.0, '2024-10-10 11:40:00', '192.168.1.104', 'Mozilla/5.0 Chrome/120', 'sess_dave_1004', 0);
INSERT INTO discount_redemptions VALUES (2, 5, 7, 1007, 50.0, '2024-11-15 10:50:00', '192.168.1.107', 'Mozilla/5.0 Safari/17', 'sess_grace_1007', 0);
INSERT INTO discount_redemptions VALUES (3, 3, 11, 1011, 25.0, '2024-12-20 17:18:00', '192.168.1.111', 'Mozilla/5.0 Chrome/121', 'sess_kate_1011', 1);
INSERT INTO discount_redemptions VALUES (4, 4, 9, 1019, 5.0, '2025-03-15 14:20:00', '192.168.1.109', 'Mozilla/5.0 Firefox/123', 'sess_ivy_1019', 0);
INSERT INTO discount_redemptions VALUES (5, 1, 11, 1011, 0.0, '2024-12-20 17:15:00', '192.168.1.111', 'Mozilla/5.0 Chrome/121', 'sess_kate_1011', 1);
INSERT INTO discount_redemptions VALUES (6, 6, 1, 1001, 0.0, '2024-09-15 10:20:00', '192.168.1.101', 'Mozilla/5.0 Chrome/119', 'sess_alice_1001', 0);
INSERT INTO discount_redemptions VALUES (7, 6, 5, 1005, 0.0, '2024-10-18 16:25:00', '192.168.1.105', 'Mozilla/5.0 Safari/17', 'sess_eve_1005', 0);
INSERT INTO discount_redemptions VALUES (8, 6, 6, 1006, 0.0, '2024-11-02 13:15:00', '192.168.1.106', 'Mozilla/5.0 Chrome/120', 'sess_frank_1006', 0);
INSERT INTO discount_redemptions VALUES (9, 6, 1, 1012, 0.0, '2025-01-05 09:25:00', '192.168.1.101', 'Mozilla/5.0 Chrome/121', 'sess_alice_1012', 0);
INSERT INTO discount_redemptions VALUES (10, 1, 12, 1013, 0.0, '2025-01-15 14:10:00', '192.168.1.112', 'Mozilla/5.0 Firefox/122', 'sess_leo_1013', 1);

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

INSERT INTO marketing_campaigns VALUES (1, 'Fall Sale 2024', 'Annual fall clearance sale', 'seasonal', '2024-09-01', '2024-11-30', 5000.0, 4850.0, 'completed', 'all_customers', 'admin');
INSERT INTO marketing_campaigns VALUES (2, 'Holiday Blitz 2024', 'Black Friday through New Year promotions', 'holiday', '2024-11-25', '2024-12-31', 10000.0, 9200.0, 'completed', 'all_customers', 'admin');
INSERT INTO marketing_campaigns VALUES (3, 'New Year Clearance', 'Post-holiday inventory clearance', 'clearance', '2025-01-02', '2025-01-31', 3000.0, 2100.0, 'completed', 'bargain_hunters', 'admin');
INSERT INTO marketing_campaigns VALUES (4, 'Spring Collection Launch', 'Promote new spring clothing line', 'launch', '2025-03-01', '2025-04-30', 7500.0, 1800.0, 'active', 'fashion_enthusiasts', 'admin');
INSERT INTO marketing_campaigns VALUES (5, 'Tech Upgrade Month', 'Electronics trade-in and upgrade deals', 'promotional', '2025-04-01', '2025-04-30', 8000.0, 0.0, 'scheduled', 'tech_buyers', 'admin');

CREATE TABLE campaign_discount_links (
    id INTEGER PRIMARY KEY,
    campaign_id INTEGER NOT NULL REFERENCES marketing_campaigns(id),
    discount_code_id INTEGER NOT NULL REFERENCES discount_codes(id),
    created_at TEXT NOT NULL
);

INSERT INTO campaign_discount_links VALUES (1, 1, 2, '2024-09-01');
INSERT INTO campaign_discount_links VALUES (2, 1, 5, '2024-09-01');
INSERT INTO campaign_discount_links VALUES (3, 2, 3, '2024-11-25');
INSERT INTO campaign_discount_links VALUES (4, 4, 4, '2025-03-01');
INSERT INTO campaign_discount_links VALUES (5, 2, 1, '2024-11-25');
INSERT INTO campaign_discount_links VALUES (6, 1, 6, '2024-09-01');
INSERT INTO campaign_discount_links VALUES (7, 3, 6, '2025-01-02');
INSERT INTO campaign_discount_links VALUES (8, 3, 1, '2025-01-02');

CREATE TABLE saved_lists (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    name TEXT NOT NULL DEFAULT 'My Wishlist',
    is_public INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    updated_at TEXT
);

INSERT INTO saved_lists VALUES (1, 1, 'My Wishlist', 0, '2024-11-01', '2024-11-01');
INSERT INTO saved_lists VALUES (2, 2, 'My Wishlist', 1, '2024-10-15', '2024-10-15');
INSERT INTO saved_lists VALUES (3, 3, 'My Wishlist', 1, '2024-12-01', '2024-12-01');
INSERT INTO saved_lists VALUES (4, 4, 'My Wishlist', 0, '2025-01-10', '2025-01-10');
INSERT INTO saved_lists VALUES (5, 5, 'My Wishlist', 0, '2025-01-20', '2025-01-20');
INSERT INTO saved_lists VALUES (6, 6, 'My Wishlist', 1, '2024-12-15', '2024-12-15');
INSERT INTO saved_lists VALUES (7, 7, 'My Wishlist', 0, '2025-02-01', '2025-02-01');
INSERT INTO saved_lists VALUES (8, 8, 'My Wishlist', 1, '2025-02-10', '2025-02-10');
INSERT INTO saved_lists VALUES (9, 9, 'My Wishlist', 0, '2025-02-15', '2025-02-15');
INSERT INTO saved_lists VALUES (10, 10, 'My Wishlist', 1, '2025-03-01', '2025-03-01');
INSERT INTO saved_lists VALUES (11, 11, 'My Wishlist', 0, '2025-03-05', '2025-03-05');
INSERT INTO saved_lists VALUES (12, 12, 'My Wishlist', 0, '2025-03-10', '2025-03-10');

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

INSERT INTO saved_list_items VALUES (1, 1, 2, '2024-11-01', 'medium', 'Want for birthday', 899.99, 1);
INSERT INTO saved_list_items VALUES (2, 2, 1, '2024-10-15', 'high', 'For work upgrade', 1299.99, 1);
INSERT INTO saved_list_items VALUES (3, 3, 11, '2024-12-01', 'medium', 'Holiday gift idea', 249.99, 1);
INSERT INTO saved_list_items VALUES (4, 4, 4, '2025-01-10', 'low', NULL, 199.99, 1);
INSERT INTO saved_list_items VALUES (5, 5, 8, '2025-01-20', 'medium', 'Need for hiking trip', 149.99, 0);
INSERT INTO saved_list_items VALUES (6, 6, 10, '2024-12-15', 'low', NULL, 79.99, 1);
INSERT INTO saved_list_items VALUES (7, 7, 13, '2025-02-01', 'low', 'Want to learn SQL', 39.99, 0);
INSERT INTO saved_list_items VALUES (8, 8, 9, '2025-02-10', 'medium', 'Kitchen upgrade', 89.99, 1);
INSERT INTO saved_list_items VALUES (9, 9, 12, '2025-02-15', 'high', 'For travel', 59.99, 1);
INSERT INTO saved_list_items VALUES (10, 10, 3, '2025-03-01', 'medium', NULL, 549.99, 1);
INSERT INTO saved_list_items VALUES (11, 11, 7, '2025-03-05', 'low', 'Running shoes', 119.99, 1);
INSERT INTO saved_list_items VALUES (12, 12, 14, '2025-03-10', 'low', NULL, 49.99, 0);

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

INSERT INTO newsletter_subscribers VALUES (1, 'alice@email.com', 1, '2021-01-10', 'active', 'signup', 'deals,new_arrivals', '2025-03-20', 0.72, 0);
INSERT INTO newsletter_subscribers VALUES (2, 'bob@email.com', 2, '2021-03-05', 'active', 'signup', 'deals', '2025-03-20', 0.45, 0);
INSERT INTO newsletter_subscribers VALUES (3, 'carol@email.com', 3, '2021-06-18', 'active', 'signup', 'deals,new_arrivals,blog', '2025-03-20', 0.68, 0);
INSERT INTO newsletter_subscribers VALUES (4, 'dave@email.com', 4, '2022-01-12', 'unsubscribed', 'signup', 'deals', '2024-08-15', 0.2, 0);
INSERT INTO newsletter_subscribers VALUES (5, 'eve@email.com', 5, '2022-04-20', 'active', 'checkout', 'deals,new_arrivals', '2025-03-20', 0.55, 0);
INSERT INTO newsletter_subscribers VALUES (6, 'frank@email.com', 6, '2022-07-01', 'active', 'checkout', 'deals', '2025-03-20', 0.38, 1);
INSERT INTO newsletter_subscribers VALUES (7, 'grace@email.com', 7, '2022-09-14', 'active', 'signup', 'new_arrivals,blog', '2025-03-20', 0.8, 0);
INSERT INTO newsletter_subscribers VALUES (8, 'newsletter_fan@gmail.com', NULL, '2024-05-10', 'active', 'footer_form', 'deals,blog', '2025-03-20', 0.6, 0);
INSERT INTO newsletter_subscribers VALUES (9, 'techdeals@outlook.com', NULL, '2024-08-22', 'active', 'popup', 'deals', '2025-03-20', 0.35, 2);
INSERT INTO newsletter_subscribers VALUES (10, 'leo@email.com', 12, '2024-04-28', 'active', 'signup', 'deals,new_arrivals', '2025-03-20', 0.5, 0);

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

INSERT INTO support_agents VALUES (1, 'Sarah Wilson', 'agent_sarah@shoplocal.com', '555-6001', 'support', 'senior_agent', 1, '2020-03-15', 'returns,billing,escalations', 4.7);
INSERT INTO support_agents VALUES (2, 'Mike Johnson', 'agent_mike@shoplocal.com', '555-6002', 'support', 'agent', 1, '2021-08-01', 'shipping,tracking,general', 4.5);
INSERT INTO support_agents VALUES (3, 'Jenny Lee', 'agent_jenny@shoplocal.com', '555-6003', 'support', 'agent', 1, '2022-05-20', 'products,returns,technical', 4.3);
INSERT INTO support_agents VALUES (4, 'Tom Bradley', 'agent_tom@shoplocal.com', '555-6004', 'support', 'team_lead', 1, '2019-01-10', 'all,management,training', 4.8);

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

INSERT INTO support_tickets VALUES (1, 3, 1, 'Damaged mugs in order 1003', 'high', 'closed', 'email', '2024-10-12', '2024-10-18', '2024-10-18', 4);
INSERT INTO support_tickets VALUES (2, 4, 2, 'Wrong mug color in order 1004', 'normal', 'closed', 'chat', '2024-10-18', '2024-10-22', '2024-10-22', 5);
INSERT INTO support_tickets VALUES (3, 6, 1, 'T-shirt size issue order 1006', 'normal', 'closed', 'email', '2024-11-10', '2024-11-18', '2024-11-18', 4);
INSERT INTO support_tickets VALUES (4, 8, 3, 'USB-C hub missing ports', 'high', 'open', 'email', '2024-12-08', '2025-01-05', NULL, NULL);
INSERT INTO support_tickets VALUES (5, 1, 2, 'Tracking not updating for order 1012', 'low', 'closed', 'chat', '2025-01-07', '2025-01-08', '2025-01-08', 5);
INSERT INTO support_tickets VALUES (6, 12, 3, 'Sneakers too narrow order 1013', 'normal', 'open', 'email', '2025-01-28', '2025-02-05', NULL, NULL);
INSERT INTO support_tickets VALUES (7, 5, 1, 'When will order 1016 ship?', 'low', 'open', 'chat', '2025-03-01', '2025-03-05', NULL, NULL);
INSERT INTO support_tickets VALUES (8, 2, 2, 'Order 1014 delivery estimate', 'normal', 'open', 'phone', '2025-02-05', '2025-02-10', NULL, NULL);
INSERT INTO support_tickets VALUES (9, 11, 3, 'Return request for USB-C hub', 'normal', 'open', 'email', '2025-01-05', '2025-01-10', NULL, NULL);
INSERT INTO support_tickets VALUES (10, 9, 2, 'Return window question', 'low', 'closed', 'chat', '2024-12-20', '2024-12-22', '2024-12-22', 2);

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

INSERT INTO ticket_messages VALUES (1, 1, 'customer', 3, 'Hi, I received my order 1003 but both mugs have cracks. Can I get a replacement or refund?', 0, 'crack_photo.jpg', '2024-10-12 09:00:00', '2024-10-12 09:30:00', 0);
INSERT INTO ticket_messages VALUES (2, 1, 'agent', 1, 'Sorry about that! We will issue a store credit for the damaged mugs right away.', 0, NULL, '2024-10-12 10:15:00', '2024-10-12 11:00:00', 0);
INSERT INTO ticket_messages VALUES (3, 2, 'customer', 4, 'I ordered a teal mug but received charcoal. Order 1004.', 0, NULL, '2024-10-18 14:00:00', '2024-10-18 14:10:00', 0);
INSERT INTO ticket_messages VALUES (4, 2, 'agent', 2, 'Apologies for the mix-up. Refund has been processed to your original payment method.', 0, NULL, '2024-10-18 14:30:00', '2024-10-18 15:00:00', 0);
INSERT INTO ticket_messages VALUES (5, 3, 'customer', 6, 'The Classic Cotton Tee size S is way too small. I usually wear S in other brands.', 0, NULL, '2024-11-10 11:00:00', '2024-11-10 13:00:00', 0);
INSERT INTO ticket_messages VALUES (6, 3, 'agent', 1, 'We understand. Our sizing runs small. We have initiated a return and refund for you.', 0, NULL, '2024-11-10 14:00:00', '2024-11-10 16:00:00', 0);
INSERT INTO ticket_messages VALUES (7, 4, 'customer', 8, 'The USB-C hub says 7-in-1 but only has 5 ports. Missing the SD card reader and HDMI.', 0, 'hub_photo.jpg', '2024-12-08 10:00:00', '2024-12-08 11:00:00', 0);
INSERT INTO ticket_messages VALUES (8, 4, 'agent', 3, 'Thank you for the photos. We are investigating this with our supplier.', 0, NULL, '2024-12-08 14:00:00', '2024-12-09 09:00:00', 0);
INSERT INTO ticket_messages VALUES (9, 4, 'agent', 3, 'Internal: flagged batch issue with SL-CHARGER-014 from GlobalTech. Check other orders.', 1, NULL, '2024-12-09 10:00:00', NULL, 0);
INSERT INTO ticket_messages VALUES (10, 5, 'customer', 1, 'My tracking number FS-100006-US has not updated in 2 days. Is everything OK?', 0, NULL, '2025-01-07 16:00:00', '2025-01-07 16:30:00', 0);
INSERT INTO ticket_messages VALUES (11, 5, 'agent', 2, 'The carrier had a scanning delay. Your package is on its way and should arrive tomorrow.', 0, NULL, '2025-01-07 17:00:00', '2025-01-07 18:00:00', 0);
INSERT INTO ticket_messages VALUES (12, 6, 'customer', 12, 'The RunFlex sneakers in US10 are too narrow for me. Can I return them?', 0, NULL, '2025-01-28 10:00:00', '2025-01-28 11:00:00', 0);
INSERT INTO ticket_messages VALUES (13, 6, 'agent', 3, 'You are within the return window. I have started a return for you. Please ship back within 14 days.', 0, NULL, '2025-01-28 13:00:00', '2025-01-29 09:00:00', 0);
INSERT INTO ticket_messages VALUES (14, 7, 'customer', 5, 'I placed order 1016 on Feb 20. It still says processing. When will it ship?', 0, NULL, '2025-03-01 12:00:00', '2025-03-01 14:00:00', 0);
INSERT INTO ticket_messages VALUES (15, 10, 'customer', 9, 'How long is the return window? I might want to return an item from order 1009.', 0, NULL, '2024-12-20 15:00:00', '2024-12-20 15:30:00', 0);

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

INSERT INTO product_reviews VALUES (1, 1, 1, 5, 'Amazing laptop!', 'Fast, lightweight, and the battery lasts all day. Perfect for work and streaming.', 1, 1, 12, 0, '2024-09-25');
INSERT INTO product_reviews VALUES (2, 2, 2, 4, 'Great phone, pricey though', 'Excellent camera and display. A bit expensive but worth it for the features.', 1, 1, 8, 0, '2024-10-05');
INSERT INTO product_reviews VALUES (3, 4, 3, 5, 'Best noise cancelling', 'These headphones block out everything. Sound quality is superb. Highly recommend.', 1, 1, 15, 0, '2024-10-10');
INSERT INTO product_reviews VALUES (4, 5, 4, 3, 'Runs small', 'Nice fabric quality but runs at least one size smaller than expected. Order up.', 1, 1, 20, 0, '2024-10-20');
INSERT INTO product_reviews VALUES (5, 3, 5, 4, 'Great for reading and drawing', 'The stylus support is fantastic. Screen could be a bit brighter outdoors.', 1, 1, 6, 0, '2024-10-28');
INSERT INTO product_reviews VALUES (6, 6, 6, 4, 'Comfortable everyday jeans', 'Good stretch and fit. Held up well after multiple washes.', 1, 1, 4, 0, '2024-11-15');
INSERT INTO product_reviews VALUES (7, 2, 7, 5, 'Love this phone', 'Switched from another brand and could not be happier. Fast, beautiful screen.', 1, 1, 10, 0, '2024-11-25');
INSERT INTO product_reviews VALUES (8, 7, 8, 4, 'Lightweight runners', 'Very comfortable for running. The memory foam insole is great.', 1, 1, 7, 0, '2024-12-10');
INSERT INTO product_reviews VALUES (9, 11, 9, 5, 'Feature-packed smartwatch', 'Tracks everything accurately. Battery lasts 4 days. Love the sleep tracking.', 1, 1, 9, 0, '2024-12-15');
INSERT INTO product_reviews VALUES (10, 13, 10, 5, 'Must-have SQL reference', 'Clear explanations with practical examples. Helped me pass my certification.', 1, 1, 18, 0, '2024-12-22');
INSERT INTO product_reviews VALUES (11, 11, 11, 4, 'Beautiful rose gold version', 'Looks elegant. Wish the band was slightly wider though.', 1, 1, 5, 0, '2024-12-28');
INSERT INTO product_reviews VALUES (12, 14, 8, 2, 'Missing ports', 'Advertised as 7-in-1 but mine only has 5 ports. Disappointed.', 1, 1, 22, 0, '2024-12-12');
INSERT INTO product_reviews VALUES (13, 9, 1, 4, 'Powerful blender', 'Makes smoothies in seconds. A bit loud but that is expected for the power.', 1, 1, 3, 0, '2025-01-15');
INSERT INTO product_reviews VALUES (14, 7, 12, 2, 'Too narrow', 'If you have wide feet, skip these. Very uncomfortable after 30 minutes.', 1, 1, 11, 0, '2025-01-25');
INSERT INTO product_reviews VALUES (15, 15, 4, 1, 'Arrived broken', 'Both mugs arrived with cracks. Packaging was terrible. Disappointed.', 0, 1, 14, 1, '2024-10-22');

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

INSERT INTO content_pages VALUES (1, 'About Us', 'about-us', 'ShopLocal is a small e-commerce company dedicated to bringing quality products at fair prices. Founded in 2020, we serve customers nationwide with fast shipping and great support.', 'published', NULL, 'About ShopLocal', 'Learn about our mission and values', '2021-01-01', '2024-06-15', 1);
INSERT INTO content_pages VALUES (2, 'Return Policy', 'return-policy', 'Items may be returned within 30 days of delivery. Items must be in original condition with tags attached. Refunds are processed within 5-7 business days.', 'published', NULL, 'Return Policy', 'Our hassle-free return policy', '2021-01-01', '2025-01-10', 1);
INSERT INTO content_pages VALUES (3, 'Shipping Information', 'shipping-info', 'We ship to all 50 US states. Standard shipping takes 3-7 business days. Express shipping takes 1-3 business days. Free shipping on orders over $75.', 'published', NULL, 'Shipping Info', 'Shipping rates and delivery times', '2021-01-01', '2025-02-20', 1);
INSERT INTO content_pages VALUES (4, 'Privacy Policy', 'privacy-policy', 'We take your privacy seriously. We collect only the data necessary to process your orders and improve your shopping experience. We never sell your data to third parties.', 'published', NULL, 'Privacy Policy', 'How we protect your data', '2021-01-01', '2024-12-01', 1);
INSERT INTO content_pages VALUES (5, 'Spring 2025 Lookbook', 'spring-2025-lookbook', 'Check out our curated spring collection featuring the latest trends in fashion and accessories.', 'draft', NULL, 'Spring 2025 Lookbook', 'Spring fashion trends and picks', '2025-02-15', '2025-03-01', 0);

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

INSERT INTO promotional_banners VALUES (1, 'Spring Sale - Up to 30% Off', '/img/banners/spring-sale.jpg', '/sale/spring-2025', 'hero', '2025-03-01', '2025-04-30', 1, 1245, 28500, 'admin');
INSERT INTO promotional_banners VALUES (2, 'New Tech Arrivals', '/img/banners/tech-arrivals.jpg', '/category/electronics', 'hero', '2025-02-15', '2025-03-31', 1, 890, 22000, 'admin');
INSERT INTO promotional_banners VALUES (3, 'Free Shipping Over $75', '/img/banners/free-shipping.jpg', '/shipping-info', 'sidebar', '2024-06-01', '2025-06-30', 1, 3200, 95000, 'admin');
INSERT INTO promotional_banners VALUES (4, 'Holiday Deals - Ended', '/img/banners/holiday-deals.jpg', '/sale/holiday-2024', 'hero', '2024-11-25', '2024-12-31', 0, 5400, 120000, 'admin');
INSERT INTO promotional_banners VALUES (5, 'Download Our App', '/img/banners/app-download.jpg', '/app', 'footer', '2024-01-01', '2025-12-31', 1, 780, 45000, 'admin');
INSERT INTO promotional_banners VALUES (6, 'Join Loyalty Program', '/img/banners/loyalty.jpg', '/loyalty', 'sidebar', '2025-01-15', '2025-12-31', 1, 450, 18000, 'admin');

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

INSERT INTO tax_rules VALUES (1, 'CA', 9.0, 'California Sales Tax', 'sales', 1, '2024-01-01', NULL, 'all', '2024-01-01');
INSERT INTO tax_rules VALUES (2, 'TX', 8.25, 'Texas Sales Tax', 'sales', 1, '2024-01-01', NULL, 'all', '2024-01-01');
INSERT INTO tax_rules VALUES (3, 'WA', 10.0, 'Washington Sales Tax', 'sales', 1, '2024-01-01', NULL, 'all', '2024-01-01');
INSERT INTO tax_rules VALUES (4, 'FL', 7.0, 'Florida Sales Tax', 'sales', 1, '2024-01-01', NULL, 'all', '2024-01-01');
INSERT INTO tax_rules VALUES (5, 'OR', 0.0, 'Oregon No Sales Tax', 'sales', 1, '2024-01-01', NULL, 'all', '2024-01-01');
INSERT INTO tax_rules VALUES (6, 'IL', 10.25, 'Illinois Sales Tax', 'sales', 1, '2024-01-01', NULL, 'all', '2024-01-01');

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

INSERT INTO product_performance VALUES (1, 1, 2, 2599.98, 5.0, 1, 1, 0, NULL);
INSERT INTO product_performance VALUES (2, 2, 3, 2699.97, 4.5, 2, 1, 0, NULL);
INSERT INTO product_performance VALUES (3, 3, 1, 549.99, 4.0, 1, 1, 0, NULL);
INSERT INTO product_performance VALUES (4, 4, 2, 399.98, 5.0, 1, 1, 0, NULL);
INSERT INTO product_performance VALUES (5, 5, 5, 149.95, 3.0, 1, 0, 0, NULL);
INSERT INTO product_performance VALUES (6, 6, 3, 209.97, 4.0, 1, 0, 0, NULL);
INSERT INTO product_performance VALUES (7, 7, 2, 239.98, 3.0, 2, 1, 0, NULL);
INSERT INTO product_performance VALUES (8, 8, 2, 299.98, NULL, 0, 1, 0, NULL);
INSERT INTO product_performance VALUES (9, 9, 1, 89.99, 4.0, 1, 1, 0, NULL);
INSERT INTO product_performance VALUES (10, 10, 1, 79.99, NULL, 0, 1, 0, NULL);
INSERT INTO product_performance VALUES (11, 11, 3, 749.97, 4.5, 2, 1, 0, NULL);
INSERT INTO product_performance VALUES (12, 12, 2, 119.98, NULL, 0, 1, 0, NULL);
INSERT INTO product_performance VALUES (13, 13, 1, 39.99, 5.0, 1, 1, 0, NULL);
INSERT INTO product_performance VALUES (14, 14, 4, 199.96, 2.0, 1, 1, 0, NULL);
INSERT INTO product_performance VALUES (15, 15, 5, 99.95, 1.0, 1, 0, 0, NULL);

CREATE TABLE category_performance (
    id INTEGER PRIMARY KEY,
    category_id INTEGER NOT NULL UNIQUE REFERENCES categories(id),
    product_count INTEGER NOT NULL DEFAULT 0,
    total_revenue REAL NOT NULL DEFAULT 0.0,
    average_product_rating REAL,
    top_product_id INTEGER REFERENCES products(id)
);

INSERT INTO category_performance VALUES (1, 1, 3, 1149.93, 3.67, 3);
INSERT INTO category_performance VALUES (2, 2, 1, 2599.98, 5.0, 1);
INSERT INTO category_performance VALUES (3, 3, 1, 2699.97, 4.5, 2);
INSERT INTO category_performance VALUES (4, 4, 3, 659.9, 3.5, 8);
INSERT INTO category_performance VALUES (5, 5, 1, 239.98, 3.0, 7);
INSERT INTO category_performance VALUES (6, 6, 3, 269.93, 2.5, 15);
INSERT INTO category_performance VALUES (7, 7, 2, 869.95, 4.5, 11);
INSERT INTO category_performance VALUES (8, 8, 1, 39.99, 5.0, 13);

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

INSERT INTO daily_revenue_summary VALUES (1, '2024-09-15', 1, 1403.99, 104.0, 0.0, 0.0, 1403.99);
INSERT INTO daily_revenue_summary VALUES (2, '2024-09-20', 1, 1014.37, 74.4, 9.99, 0.0, 1014.37);
INSERT INTO daily_revenue_summary VALUES (3, '2024-10-01', 1, 225.98, 20.0, 5.99, 0.0, 225.98);
INSERT INTO daily_revenue_summary VALUES (4, '2024-10-10', 1, 93.17, 7.2, 5.99, 10.0, 93.17);
INSERT INTO daily_revenue_summary VALUES (5, '2024-10-18', 1, 588.49, 38.5, 0.0, 0.0, 588.49);
INSERT INTO daily_revenue_summary VALUES (6, '2024-11-02', 1, 351.98, 32.0, 0.0, 0.0, 351.98);
INSERT INTO daily_revenue_summary VALUES (7, '2024-11-15', 1, 930.99, 81.0, 0.0, 50.0, 930.99);
INSERT INTO daily_revenue_summary VALUES (8, '2024-11-28', 1, 186.6, 10.63, 5.99, 0.0, 186.6);
INSERT INTO daily_revenue_summary VALUES (9, '2024-12-05', 1, 303.5, 23.52, 0.0, 0.0, 303.5);
INSERT INTO daily_revenue_summary VALUES (10, '2024-12-12', 1, 49.68, 3.7, 5.99, 0.0, 49.68);
INSERT INTO daily_revenue_summary VALUES (11, '2024-12-20', 1, 514.97, 40.0, 0.0, 25.0, 514.97);
INSERT INTO daily_revenue_summary VALUES (12, '2025-01-05', 1, 269.99, 20.0, 0.0, 0.0, 269.99);
INSERT INTO daily_revenue_summary VALUES (13, '2025-01-15', 1, 136.78, 10.8, 5.99, 0.0, 136.78);
INSERT INTO daily_revenue_summary VALUES (14, '2025-01-28', 1, 168.36, 12.38, 5.99, 0.0, 168.36);
INSERT INTO daily_revenue_summary VALUES (15, '2025-02-10', 1, 82.98, 7.0, 5.99, 0.0, 82.98);
INSERT INTO daily_revenue_summary VALUES (16, '2025-02-20', 1, 1444.48, 94.5, 0.0, 0.0, 1444.48);
INSERT INTO daily_revenue_summary VALUES (17, '2025-03-01', 1, 71.38, 5.4, 5.99, 0.0, 71.38);
INSERT INTO daily_revenue_summary VALUES (18, '2025-03-10', 1, 90.98, 5.0, 5.99, 0.0, 90.98);
INSERT INTO daily_revenue_summary VALUES (19, '2025-03-15', 1, 55.18, 4.2, 5.99, 5.0, 55.18);
INSERT INTO daily_revenue_summary VALUES (20, '2025-03-22', 1, 962.99, 63.0, 0.0, 0.0, 962.99);

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
INSERT INTO user_cohort_analysis VALUES (3, '2024-03', 4, 4, 2, 2470.33, 1711.97, 0.5);
INSERT INTO user_cohort_analysis VALUES (4, '2024-04', 0, 0, 0, 0.0, 0.0, 0.0);
