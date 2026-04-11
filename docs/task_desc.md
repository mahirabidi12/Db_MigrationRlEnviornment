# Task Descriptions

Database migration is one of the most common yet error-prone tasks in software engineering. Every company acquisition, platform consolidation, or system modernisation eventually comes down to the same problem: take the old database, understand it, and transform it into the new one without losing a single row. It happens in healthcare when clinics get acquired by hospital chains. It happens in social media when platforms consolidate. It happens in e-commerce when scrappy startups get absorbed by enterprise retailers. Our three tasks are modelled directly after these real-world scenarios.

Every task operates in **narrative mode**. The agent never sees the target schema as structured data. Instead, it receives a detailed natural-language specification — pages of prose describing what each target table should look like, where the data comes from, and how references should be resolved. The agent must read, comprehend, plan, and execute. This is closer to how a real engineer works: they read a migration spec document, not a diff tool.

---

## Task 1: Hospital Migration (Easy)

**Task ID:** `easy_hospital_migration`

### The Scenario

Picture a small neighbourhood clinic — HealthFirst Community Clinic. For years it ran on paper charts and phone calls. Five years ago they finally went digital, hiring a single developer who built their system over a summer. It worked. Patients got registered, appointments got booked, reports got tracked. But the developer made the choices a solo developer makes under time pressure: patient email addresses as the universal join key instead of proper foreign keys, one monolithic `hc_reports` table that stored X-rays, lab results, and MRI scans all in the same table (with a `rpt_type` column to tell them apart), and abbreviated column names like `pt_fname` and `doc_email`.

Now MedCore Enterprise Hospital System has acquired HealthFirst. MedCore's platform team has sent over their enterprise schema specification — 8 tables, properly normalised, with foreign keys and constraints. The clinic's data needs to move, and it needs to move correctly.

### What Makes It Realistic

The centrepiece challenge is the **report table split**. HealthFirst stored every diagnostic report in one monolithic `hc_reports` table — X-rays alongside lab results alongside MRI scans. MedCore's schema has three separate, specialised report tables (`xray_reports`, `lab_results`, `mri_reports`). The agent must read the `rpt_type` column, filter rows by type, renumber IDs, and route them to the correct target table.

Beyond that, the agent must extract embedded address fields from the patient table into a separate `patient_addresses` table, resolve every email-based reference into integer foreign keys, and compute `patient_stats` using LEFT JOINs across appointments and all three report tables — handling patients with zero reports correctly.

### Scale

| Metric | Value |
|--------|-------|
| Initial tables | 4 (`hc_*` prefix) |
| Target tables | 8 (no prefix) |
| Data | 30 → 35 rows |
| Foreign keys | 10 |
| **Total grader checks** | **194** |

### Initial Schema Overview

- `hc_patients` (5 rows) — email refs, embedded address fields
- `hc_doctors` (3 rows) — basic staff records
- `hc_appointments` (8 rows) — patient/doctor by email
- `hc_reports` (9 rows) — monolithic: 3 xray + 3 lab + 3 mri

### Target Schema Overview

- `patients`, `patient_addresses` — split from hc_patients
- `doctors` — from hc_doctors with email→FK
- `appointments` — email refs → integer FKs via JOINs
- `xray_reports`, `lab_results`, `mri_reports` — split from hc_reports by rpt_type
- `patient_stats` — computed from appointments + all 3 report tables using LEFT JOINs

### Key Challenges

1. **Report splitting** — One source table → three target tables, filtered by report type, IDs renumbered
2. **Address extraction** — Embedded columns in patients → separate address table with FK
3. **Email → FK resolution** — All email cross-references resolved via JOINs
4. **Computed statistics** — patient_stats requires LEFT JOINs across 4 tables with zero-handling

---

## Task 2: Social Media Migration (Medium)

**Task ID:** `medium_instagram_migration`

### The Scenario

Meta is doing what big tech companies periodically do — consolidating platforms. The decision has been made: Facebook's legacy database needs to be restructured into a unified Instagram-style schema. This isn't a simple rename. Facebook's data model was built for a social network centred on text posts, group discussions, and polymorphic likes. Instagram's model is built for media-first content with proper normalisation.

The legacy Facebook database has 6 tables, all prefixed with `fb_`. Groups are referenced by name. Likes are polymorphic (one table stores likes for both posts and comments, distinguished by a `like_target_type` column). Comments have self-referential replies. Everything is connected through email addresses.

The target schema has 10 tables with no prefix. Groups become communities. The single likes table splits into `post_likes` and `comment_likes`. An account_stats table must be computed. Notifications and hashtags must be derived from scratch.

### What Makes It Realistic

**Polymorphic data splitting** is a genuine pattern in production systems. Facebook's `fb_likes` table has a `like_target_type` column ('post' or 'comment') — a common anti-pattern that eventually needs normalisation. The agent must filter by type and route to two separate FK-constrained tables.

**Self-referential comment chains** are how every social platform works. Comment replies create a tree via `parent_comment_id` pointing back to the same table. The agent must preserve this tree structure during migration.

**Multiple reference types** add complexity — the agent must resolve emails (for users), usernames (for display names computed as `u_fname || ' ' || u_lname`), and group names (for community membership) using different JOIN strategies. The computed `account_stats` requires LEFT JOINs with COALESCE for zero counts.

### Scale

| Metric | Value |
|--------|-------|
| Initial tables | 6 (`fb_*` prefix) |
| Target tables | 10 (no prefix) |
| Data | 33 → 43 rows |
| Foreign keys | 13 |
| Indexes | 2 |
| **Total grader checks** | **217** |

### Initial Schema Overview

- `fb_users` (5 rows) — email, username, first/last name
- `fb_posts` (6 rows) — author by email
- `fb_comments` (6 rows) — self-referential replies via `cmt_parent_id`
- `fb_likes` (7 rows) — polymorphic: 4 post likes + 3 comment likes
- `fb_groups` (2 rows) — group name as identifier
- `fb_group_members` (4 rows) — referenced by group name + user email

### Target Schema Overview

- `accounts` — from fb_users, with computed `display_name`
- `media_posts` — email → author_id FK
- `post_comments` — self-referential `parent_comment_id` FK preserved
- `post_likes` — from fb_likes WHERE type='post'
- `comment_likes` — from fb_likes WHERE type='comment'
- `communities`, `community_members` — group name refs → integer FKs
- `account_stats` — computed: total_posts + total_likes_received per account
- `notifications` — derived: one welcome notification per account
- `hashtags` — new table with usage counts

### Key Challenges

1. **Polymorphic like splitting** — One table filtered by `like_target_type` into two FK-constrained tables
2. **Self-referential comments** — Comment reply chain via `parent_comment_id` must be preserved
3. **3 text reference types** — Email, username, group name — each needs different JOIN logic
4. **Display name computation** — Concatenation: `u_fname || ' ' || u_lname`
5. **Computed stats with zero-handling** — LEFT JOINs with COALESCE for accounts with no posts/likes
6. **Derived tables** — notifications and hashtags created from scratch or computed

---

## Task 3: E-Commerce Platform Overhaul (Hard)

**Task ID:** `hard_shoplocal_formulas`

### The Scenario

ShopLocal started as a weekend project by three friends who wanted to help local artisans sell online. Over five years it grew into a real business — 8 tables tracking products, orders, customers, reviews, and coupons. But the database grew the way scrappy startups grow: email addresses as the universal join key because "it's simpler," SKU strings as product references because "we'll add proper IDs later," and category parents referenced by name instead of ID.

Later never came. Now NexGenMart, a major enterprise retailer, has acquired ShopLocal. NexGenMart's platform team has handed over their 11-table enterprise specification. Every table must be renamed. Every email, SKU, name, and coupon code text reference must be converted to an integer foreign key. Customer addresses must be extracted. Two analytics tables must be computed from scratch. The entire 8-table legacy database must be dropped after migration.

### What Makes It Realistic

The **depth of the FK dependency chain** is what distinguishes this from the easier tasks. In the hospital task, most tables reference just `patients`. In the Instagram task, most tables reference just `accounts`. Here, `order_items` references `orders` (which references `users`) and `products` (which references `categories`). `discount_usage` references `discount_codes` (by coupon code), `users` (by email), and `orders` (by ID) — a three-way FK resolution in a single INSERT. The agent must figure out the correct creation order from the narrative alone — if it creates `order_items` before `products`, the FK constraint will fail.

The **self-referential category FK** adds a subtle trap. Categories have parent categories (Electronics → Phones, Electronics → Laptops). The `parent_id` FK points back to `categories(id)`, resolved by joining `cat_parent_name` against `categories.name`. Parent rows must be inserted before child rows.

The **computed analytics** are the hardest in the suite. `product_performance` aggregates data from order_items and reviews into a single row per product — COUNT(DISTINCT order_id) for total_orders, SUM(subtotal) for revenue, and ROUND(AVG(rating), 2) with NULL handling for products with no reviews. `daily_revenue` requires GROUP BY on order dates with COUNT + SUM.

### Scale

| Metric | Value |
|--------|-------|
| Initial tables | 8 (`sl_*` prefix) |
| Target tables | 11 (no prefix) |
| Data | 36 → 42 rows |
| Foreign keys | 12 |
| Indexes | 2 |
| **Total grader checks** | **249** |

### Initial Schema Overview

- `sl_customers` (4 rows) — email refs, embedded addresses
- `sl_categories` (4 rows) — self-referential parent by name
- `sl_products` (4 rows) — category by name, SKU as identifier
- `sl_orders` (4 rows) — customer by email
- `sl_order_items` (6 rows) — product by SKU
- `sl_reviews` (3 rows) — customer by email, product by SKU
- `sl_coupons` (2 rows) — code as identifier
- `sl_coupon_uses` (3 rows) — coupon by code, customer by email

Zero foreign keys. Zero indexes. Every cross-reference is a text string.

### Target Schema Overview

- `users`, `user_addresses` — split from sl_customers
- `categories` — self-referential `parent_id` FK resolved by name
- `products` — category name → FK via JOIN
- `orders` — email → user_id FK via JOIN
- `order_items` — SKU → product_id FK, computed subtotal
- `product_reviews` — dual FK: email → user, SKU → product
- `discount_codes` — from sl_coupons
- `discount_usage` — 3-way FK: code → discount_id, email → user_id, order_id direct
- `product_performance` — computed: total_orders, total_revenue, avg_rating with NULL
- `daily_revenue` — computed: GROUP BY order_date with COUNT + SUM

### Key Challenges

1. **Self-referential FK** — `categories.parent_id` → `categories(id)`, resolved by name; insertion order matters
2. **4 text reference types** — Email, SKU, category name, coupon code — each with different JOIN logic
3. **3-way FK resolution** — `discount_usage` requires resolving code, email, and order_id in one INSERT
4. **Computed subtotal** — `order_items.subtotal = quantity * unit_price`
5. **Aggregation with NULL handling** — avg_rating is NULL for products with no reviews
6. **Daily revenue grouping** — GROUP BY on dates with COUNT + SUM
7. **Deep FK chains** — order_items → orders → users; order_items → products → categories

---

## Difficulty Progression

| Aspect | Easy (Hospital) | Medium (Instagram) | Hard (E-Commerce) |
|--------|----------------|-------------------|-------------------|
| Initial → Target tables | 4 → 8 | 6 → 10 | 8 → 11 |
| Total data rows | 35 | 43 | 42 |
| Grader checks | 194 | 217 | 249 |
| Text reference types | Email only | Email + username + group name | Email + SKU + category name + coupon code |
| Table splitting | 1 → 3 (reports by type) | 1 → 2 (likes by target type) | 1 → 2 (customers → users + addresses) |
| Self-referential FK | No | Yes (comment replies) | Yes (category parents) |
| Computed tables | 1 (patient_stats) | 1 (account_stats) + 2 derived | 2 (product_performance + daily_revenue) |
| Hardest single operation | Report split with renumbered IDs | Polymorphic like split | 3-way FK resolution in discount_usage |

**Easy → Medium**: The leap is conceptual complexity. The hospital migration is mostly filter-split-and-restructure. The Instagram migration requires the agent to understand that polymorphic data must be split by type, comments reference themselves, display names must be concatenated, and groups become communities referenced by name.

**Medium → Hard**: The leap is dependency depth and computation. The e-commerce task has 4 different text reference types (vs 1 for easy, 3 for medium), self-referential categories that require ordered insertion, 3-way FK resolution in a single table, and aggregation queries with NULL handling and GROUP BY.
