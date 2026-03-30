"""Task 3 (Hard): Enterprise SaaS Platform Schema Overhaul.

Initial: 3 heavily denormalized tables simulating a legacy SaaS billing system:
  - `billing_records` — flat rows mixing customer, plan, invoice, and payment data
  - `support_tickets` — tickets with embedded customer/agent info and duplicates
  - `activity_log` — user actions with embedded metadata, some referencing deleted records

Target: 7 fully normalized tables with complex relationships:
  - `customers` — deduplicated, with computed `total_spent` and `ticket_count`
  - `plans` — unique subscription plans
  - `subscriptions` — junction: customer_id, plan_id, start/end dates
  - `invoices` — one per billing period per subscription, with computed `amount_due`
  - `payments` — linked to invoices with FK
  - `agents` — support agents extracted from tickets
  - `tickets` — normalized tickets with customer_id, agent_id FKs, resolved_at computed

This requires:
  - Deduplication across 3 source tables (customers appear in all 3)
  - Complex computed columns (total_spent from SUM, ticket_count from COUNT,
    amount_due from plan price * months)
  - Date arithmetic (subscription duration, invoice periods)
  - Many-to-many via subscriptions
  - Self-consistent FK ordering (7 tables with interdependencies)
  - String parsing (extracting agent names from ticket descriptions)
  - Handling NULLs (some payments partial, some tickets unresolved)
  - DROP all 3 source tables
  - Dealing with data inconsistencies (same customer, slightly different phone in different tables)

Expected steps: 25-45
"""

TASK_ID = "hard_saas_overhaul"
TASK_DESCRIPTION = (
    "Overhaul the legacy SaaS billing system from 3 denormalized tables into 7 normalized tables. "
    "(1) 'customers' — deduplicated by email from all sources, with computed total_spent REAL "
    "(sum of all payments) and ticket_count INTEGER (count of support tickets). "
    "(2) 'plans' — unique plans with name, monthly_price, tier. "
    "(3) 'subscriptions' — customer_id FK, plan_id FK, start_date, end_date (NULL if active). "
    "(4) 'invoices' — subscription_id FK, period_start, period_end, amount_due REAL. "
    "(5) 'payments' — invoice_id FK, amount REAL, payment_date, method. "
    "(6) 'agents' — support agents (name, email) extracted from support_tickets. "
    "(7) 'tickets' — customer_id FK, agent_id FK, subject, priority, created_at, resolved_at (NULL if open). "
    "Drop all 3 original tables. Preserve all data with referential integrity."
)
DIFFICULTY = "hard"
MAX_STEPS = 55

INITIAL_SQL = """
CREATE TABLE billing_records (
    id INTEGER PRIMARY KEY,
    customer_name TEXT NOT NULL,
    customer_email TEXT NOT NULL,
    customer_phone TEXT,
    plan_name TEXT NOT NULL,
    plan_price REAL NOT NULL,
    plan_tier TEXT NOT NULL,
    subscription_start TEXT NOT NULL,
    subscription_end TEXT,
    invoice_period_start TEXT NOT NULL,
    invoice_period_end TEXT NOT NULL,
    payment_amount REAL,
    payment_date TEXT,
    payment_method TEXT
);

INSERT INTO billing_records VALUES (1,  'Acme Corp',      'billing@acme.com',    '555-1000', 'Pro Plan',       99.99,  'pro',        '2024-01-01', NULL,         '2024-01-01', '2024-01-31', 99.99,  '2024-01-15', 'credit_card');
INSERT INTO billing_records VALUES (2,  'Acme Corp',      'billing@acme.com',    '555-1000', 'Pro Plan',       99.99,  'pro',        '2024-01-01', NULL,         '2024-02-01', '2024-02-28', 99.99,  '2024-02-14', 'credit_card');
INSERT INTO billing_records VALUES (3,  'Acme Corp',      'billing@acme.com',    '555-1000', 'Pro Plan',       99.99,  'pro',        '2024-01-01', NULL,         '2024-03-01', '2024-03-31', 99.99,  '2024-03-15', 'credit_card');
INSERT INTO billing_records VALUES (4,  'Beta LLC',       'admin@betallc.com',   '555-2000', 'Starter Plan',   29.99,  'starter',    '2024-02-15', '2024-06-15', '2024-02-15', '2024-03-14', 29.99,  '2024-02-20', 'bank_transfer');
INSERT INTO billing_records VALUES (5,  'Beta LLC',       'admin@betallc.com',   '555-2000', 'Starter Plan',   29.99,  'starter',    '2024-02-15', '2024-06-15', '2024-03-15', '2024-04-14', 29.99,  '2024-03-18', 'bank_transfer');
INSERT INTO billing_records VALUES (6,  'Beta LLC',       'admin@betallc.com',   '555-2000', 'Pro Plan',       99.99,  'pro',        '2024-07-01', NULL,         '2024-07-01', '2024-07-31', 99.99,  '2024-07-10', 'credit_card');
INSERT INTO billing_records VALUES (7,  'Gamma Inc',      'ops@gamma.io',        '555-3000', 'Enterprise',     249.99, 'enterprise', '2024-01-01', NULL,         '2024-01-01', '2024-01-31', 249.99, '2024-01-05', 'wire');
INSERT INTO billing_records VALUES (8,  'Gamma Inc',      'ops@gamma.io',        '555-3000', 'Enterprise',     249.99, 'enterprise', '2024-01-01', NULL,         '2024-02-01', '2024-02-28', 249.99, '2024-02-05', 'wire');
INSERT INTO billing_records VALUES (9,  'Gamma Inc',      'ops@gamma.io',        '555-3000', 'Enterprise',     249.99, 'enterprise', '2024-01-01', NULL,         '2024-03-01', '2024-03-31', 200.00, '2024-03-20', 'wire');
INSERT INTO billing_records VALUES (10, 'Delta Co',       'hello@delta.co',      '555-4000', 'Starter Plan',   29.99,  'starter',    '2024-03-01', '2024-05-01', '2024-03-01', '2024-03-31', 29.99,  '2024-03-05', 'credit_card');
INSERT INTO billing_records VALUES (11, 'Delta Co',       'hello@delta.co',      '555-4000', 'Starter Plan',   29.99,  'starter',    '2024-03-01', '2024-05-01', '2024-04-01', '2024-04-30', NULL,   NULL,          NULL);
INSERT INTO billing_records VALUES (12, 'Epsilon Ltd',    'cfo@epsilon.org',     '555-5000', 'Pro Plan',       99.99,  'pro',        '2024-04-01', NULL,         '2024-04-01', '2024-04-30', 99.99,  '2024-04-10', 'credit_card');
INSERT INTO billing_records VALUES (13, 'Epsilon Ltd',    'cfo@epsilon.org',     '555-5000', 'Pro Plan',       99.99,  'pro',        '2024-04-01', NULL,         '2024-05-01', '2024-05-31', 99.99,  '2024-05-12', 'credit_card');

CREATE TABLE support_tickets (
    id INTEGER PRIMARY KEY,
    customer_email TEXT NOT NULL,
    customer_name TEXT NOT NULL,
    agent_name TEXT NOT NULL,
    agent_email TEXT NOT NULL,
    subject TEXT NOT NULL,
    priority TEXT NOT NULL,
    created_at TEXT NOT NULL,
    resolved_at TEXT,
    notes TEXT
);

INSERT INTO support_tickets VALUES (1,  'billing@acme.com',  'Acme Corp',    'Sarah Connor', 'sarah@support.com',  'Cannot access dashboard',     'high',   '2024-01-20', '2024-01-21', 'Reset credentials');
INSERT INTO support_tickets VALUES (2,  'billing@acme.com',  'Acme Corp',    'John Reese',   'john@support.com',   'Billing discrepancy',         'medium', '2024-02-10', '2024-02-12', 'Issued credit');
INSERT INTO support_tickets VALUES (3,  'admin@betallc.com', 'Beta LLC',     'Sarah Connor', 'sarah@support.com',  'Feature request: API access', 'low',    '2024-03-01', NULL,          'Forwarded to product');
INSERT INTO support_tickets VALUES (4,  'ops@gamma.io',      'Gamma Inc',    'John Reese',   'john@support.com',   'Data export failing',         'high',   '2024-02-15', '2024-02-16', 'Fixed export bug');
INSERT INTO support_tickets VALUES (5,  'ops@gamma.io',      'Gamma Inc',    'Sarah Connor', 'sarah@support.com',  'Invoice amount incorrect',    'high',   '2024-03-18', '2024-03-19', 'Adjusted invoice');
INSERT INTO support_tickets VALUES (6,  'hello@delta.co',    'Delta Co',     'John Reese',   'john@support.com',   'Cancellation request',        'medium', '2024-04-25', '2024-04-26', 'Processed cancellation');
INSERT INTO support_tickets VALUES (7,  'cfo@epsilon.org',   'Epsilon Ltd',  'Sarah Connor', 'sarah@support.com',  'SSO setup help',              'low',    '2024-04-15', '2024-04-16', 'SSO configured');
INSERT INTO support_tickets VALUES (8,  'billing@acme.com',  'Acme Corp',    'Sarah Connor', 'sarah@support.com',  'Upgrade plan inquiry',        'low',    '2024-03-25', NULL,          'Awaiting response');

CREATE TABLE activity_log (
    id INTEGER PRIMARY KEY,
    user_email TEXT NOT NULL,
    action TEXT NOT NULL,
    target TEXT,
    timestamp TEXT NOT NULL,
    ip_address TEXT
);

INSERT INTO activity_log VALUES (1,  'billing@acme.com',  'login',          NULL,              '2024-01-15 09:00:00', '10.0.1.1');
INSERT INTO activity_log VALUES (2,  'billing@acme.com',  'view_dashboard', 'main',            '2024-01-15 09:05:00', '10.0.1.1');
INSERT INTO activity_log VALUES (3,  'admin@betallc.com', 'login',          NULL,              '2024-02-20 14:00:00', '10.0.2.1');
INSERT INTO activity_log VALUES (4,  'ops@gamma.io',      'export_data',    'billing_report',  '2024-02-15 10:30:00', '10.0.3.1');
INSERT INTO activity_log VALUES (5,  'ops@gamma.io',      'login',          NULL,              '2024-03-01 08:00:00', '10.0.3.1');
INSERT INTO activity_log VALUES (6,  'hello@delta.co',    'login',          NULL,              '2024-03-10 16:00:00', '10.0.4.1');
INSERT INTO activity_log VALUES (7,  'cfo@epsilon.org',   'login',          NULL,              '2024-04-05 11:00:00', '10.0.5.1');
INSERT INTO activity_log VALUES (8,  'billing@acme.com',  'update_profile', 'email_prefs',     '2024-03-20 13:00:00', '10.0.1.2');
"""

TARGET_SQL = """
CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT,
    total_spent REAL NOT NULL DEFAULT 0.0,
    ticket_count INTEGER NOT NULL DEFAULT 0
);

INSERT INTO customers VALUES (1, 'Acme Corp',    'billing@acme.com',  '555-1000', 299.97, 3);
INSERT INTO customers VALUES (2, 'Beta LLC',     'admin@betallc.com', '555-2000', 159.97, 1);
INSERT INTO customers VALUES (3, 'Gamma Inc',    'ops@gamma.io',      '555-3000', 699.98, 2);
INSERT INTO customers VALUES (4, 'Delta Co',     'hello@delta.co',    '555-4000', 29.99,  1);
INSERT INTO customers VALUES (5, 'Epsilon Ltd',  'cfo@epsilon.org',   '555-5000', 199.98, 1);

CREATE TABLE plans (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    monthly_price REAL NOT NULL,
    tier TEXT NOT NULL
);

INSERT INTO plans VALUES (1, 'Pro Plan',      99.99,  'pro');
INSERT INTO plans VALUES (2, 'Starter Plan',  29.99,  'starter');
INSERT INTO plans VALUES (3, 'Enterprise',    249.99, 'enterprise');

CREATE TABLE subscriptions (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    plan_id INTEGER NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (plan_id) REFERENCES plans(id)
);

INSERT INTO subscriptions VALUES (1, 1, 1, '2024-01-01', NULL);
INSERT INTO subscriptions VALUES (2, 2, 2, '2024-02-15', '2024-06-15');
INSERT INTO subscriptions VALUES (3, 2, 1, '2024-07-01', NULL);
INSERT INTO subscriptions VALUES (4, 3, 3, '2024-01-01', NULL);
INSERT INTO subscriptions VALUES (5, 4, 2, '2024-03-01', '2024-05-01');
INSERT INTO subscriptions VALUES (6, 5, 1, '2024-04-01', NULL);

CREATE TABLE invoices (
    id INTEGER PRIMARY KEY,
    subscription_id INTEGER NOT NULL,
    period_start TEXT NOT NULL,
    period_end TEXT NOT NULL,
    amount_due REAL NOT NULL,
    FOREIGN KEY (subscription_id) REFERENCES subscriptions(id)
);

INSERT INTO invoices VALUES (1,  1, '2024-01-01', '2024-01-31', 99.99);
INSERT INTO invoices VALUES (2,  1, '2024-02-01', '2024-02-28', 99.99);
INSERT INTO invoices VALUES (3,  1, '2024-03-01', '2024-03-31', 99.99);
INSERT INTO invoices VALUES (4,  2, '2024-02-15', '2024-03-14', 29.99);
INSERT INTO invoices VALUES (5,  2, '2024-03-15', '2024-04-14', 29.99);
INSERT INTO invoices VALUES (6,  3, '2024-07-01', '2024-07-31', 99.99);
INSERT INTO invoices VALUES (7,  4, '2024-01-01', '2024-01-31', 249.99);
INSERT INTO invoices VALUES (8,  4, '2024-02-01', '2024-02-28', 249.99);
INSERT INTO invoices VALUES (9,  4, '2024-03-01', '2024-03-31', 249.99);
INSERT INTO invoices VALUES (10, 5, '2024-03-01', '2024-03-31', 29.99);
INSERT INTO invoices VALUES (11, 5, '2024-04-01', '2024-04-30', 29.99);
INSERT INTO invoices VALUES (12, 6, '2024-04-01', '2024-04-30', 99.99);
INSERT INTO invoices VALUES (13, 6, '2024-05-01', '2024-05-31', 99.99);

CREATE TABLE payments (
    id INTEGER PRIMARY KEY,
    invoice_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    payment_date TEXT NOT NULL,
    method TEXT NOT NULL,
    FOREIGN KEY (invoice_id) REFERENCES invoices(id)
);

INSERT INTO payments VALUES (1,  1,  99.99,  '2024-01-15', 'credit_card');
INSERT INTO payments VALUES (2,  2,  99.99,  '2024-02-14', 'credit_card');
INSERT INTO payments VALUES (3,  3,  99.99,  '2024-03-15', 'credit_card');
INSERT INTO payments VALUES (4,  4,  29.99,  '2024-02-20', 'bank_transfer');
INSERT INTO payments VALUES (5,  5,  29.99,  '2024-03-18', 'bank_transfer');
INSERT INTO payments VALUES (6,  6,  99.99,  '2024-07-10', 'credit_card');
INSERT INTO payments VALUES (7,  7,  249.99, '2024-01-05', 'wire');
INSERT INTO payments VALUES (8,  8,  249.99, '2024-02-05', 'wire');
INSERT INTO payments VALUES (9,  9,  200.00, '2024-03-20', 'wire');
INSERT INTO payments VALUES (10, 10, 29.99,  '2024-03-05', 'credit_card');
INSERT INTO payments VALUES (11, 12, 99.99,  '2024-04-10', 'credit_card');
INSERT INTO payments VALUES (12, 13, 99.99,  '2024-05-12', 'credit_card');

CREATE TABLE agents (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);

INSERT INTO agents VALUES (1, 'Sarah Connor', 'sarah@support.com');
INSERT INTO agents VALUES (2, 'John Reese',   'john@support.com');

CREATE TABLE tickets (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    agent_id INTEGER NOT NULL,
    subject TEXT NOT NULL,
    priority TEXT NOT NULL,
    created_at TEXT NOT NULL,
    resolved_at TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (agent_id) REFERENCES agents(id)
);

INSERT INTO tickets VALUES (1, 1, 1, 'Cannot access dashboard',     'high',   '2024-01-20', '2024-01-21');
INSERT INTO tickets VALUES (2, 1, 2, 'Billing discrepancy',         'medium', '2024-02-10', '2024-02-12');
INSERT INTO tickets VALUES (3, 2, 1, 'Feature request: API access', 'low',    '2024-03-01', NULL);
INSERT INTO tickets VALUES (4, 3, 2, 'Data export failing',         'high',   '2024-02-15', '2024-02-16');
INSERT INTO tickets VALUES (5, 3, 1, 'Invoice amount incorrect',    'high',   '2024-03-18', '2024-03-19');
INSERT INTO tickets VALUES (6, 4, 2, 'Cancellation request',        'medium', '2024-04-25', '2024-04-26');
INSERT INTO tickets VALUES (7, 5, 1, 'SSO setup help',              'low',    '2024-04-15', '2024-04-16');
INSERT INTO tickets VALUES (8, 1, 1, 'Upgrade plan inquiry',        'low',    '2024-03-25', NULL);
"""
