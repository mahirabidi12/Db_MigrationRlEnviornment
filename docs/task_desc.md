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

## Task 4: Hospital Migration Expanded (Easy 2)

**Task ID:** `easy_hospital_migration_2`

### The Scenario

The same HealthFirst Community Clinic acquisition, but expanded to the full operational scale. HealthFirst's 5-year-old digital system grew from a basic patient-appointment tracker into a 31-table monster covering patient identity, insurance, allergies, immunizations, medical history, clinical operations, diagnostics, staff scheduling, billing, pharmacy, equipment, ward/bed management, and audit logs. Every table uses the `hc_` prefix, every cross-reference is an email string, and every diagnostic report — X-ray, CT scan, MRI, lab result, pathology finding, ultrasound — is thrown into the same monolithic `hc_reports` table distinguished only by a `rpt_type` column.

MedCore Enterprise Hospital System requires the full migration into their 41-table enterprise schema. This is what the acquisition actually looks like in practice — not a clean 4-table teaching example.

### What Makes This Task Interesting

The centrepiece challenge is the **six-way report table split**. HealthFirst stored every diagnostic report in one monolithic `hc_reports` table. MedCore's schema has six separate, specialised report tables (`lab_results`, `xray_reports`, `mri_reports`, `ct_scan_reports`, `pathology_reports`, `ultrasound_reports`), each with columns specific to that report type. The agent must read the `rpt_type` column, filter rows by type, and route them to the correct target table with the correct column mappings.

Beyond that, the agent must extract embedded address fields from the patient table into a separate `patient_addresses` table, resolve every email-based reference across 31 tables into integer foreign keys, compute patient statistics (total appointments, total billed, prescriptions count) from scattered source tables, and create 48 indexes on lookup columns.

### Scale

| Metric | Value |
|--------|-------|
| Initial tables | 31 (`hc_*` prefix) |
| Target tables | 41 (no prefix) |
| Data | 355 → 405 rows |
| Foreign keys | 63 |
| Indexes | 48 |
| **Total grader checks** | **1,635** |

### Initial Schema Overview

The legacy schema spans the full clinic operation across 31 `hc_*` tables:

- **Patient identity:** `hc_patients` (with address columns embedded), `hc_patient_contacts`, `hc_insurance`, `hc_allergies`, `hc_immunizations`, `hc_medical_history`
- **Staff:** `hc_doctors`, `hc_nurses`, `hc_departments`, `hc_shifts`
- **Clinical operations:** `hc_appointments`, `hc_clinic_notes`, `hc_vitals`, `hc_diagnoses`, `hc_procedures`, `hc_surgeries`, `hc_prescriptions`, `hc_medications`, `hc_referrals`, `hc_follow_ups`, `hc_consent_forms`
- **Diagnostics:** `hc_reports` (ALL report types in one table), `hc_lab_orders`
- **Billing & admin:** `hc_billing`, `hc_payments`, `hc_pharmacy_inventory`, `hc_equipment`, `hc_rooms`, `hc_ward_beds`, `hc_waiting_list`, `hc_audit_log`

### Target Schema Overview

The 41-table enterprise schema reorganises everything with proper normalisation:

- Patient addresses extracted into their own table
- The monolithic reports table split into 6 specialised tables
- 3 computed summary tables (`patient_stats`, `department_stats`, `department_heads`)
- Ward/bed structure normalised into `wards` + `beds`
- 63 foreign key constraints and 48 indexes throughout

### Key Challenges

1. **Report splitting** — One source table → six target tables, filtered by report type
2. **Address extraction** — Embedded columns in patients → separate address table with FK
3. **Email → FK resolution** — 31 tables worth of email cross-references to resolve via JOINs
4. **Computed statistics** — Patient and department stats aggregated across multiple tables
5. **Heavy indexing** — 48 indexes that must match exact column specifications

---

## Task 5: Social Media Migration Expanded (Medium 2)

**Task ID:** `medium_instagram_migration_2`

### The Scenario

The same Facebook → Instagram consolidation, but at full platform scale. Facebook's entire 25-table legacy database spans users, profiles, friendships, posts, comments, likes (polymorphic), photos, albums, groups, pages, conversations, messages, events, notifications, activity logs, reports, privacy settings, blocked users, saved items, and hashtags — all prefixed with `fb_` and connected through email addresses, usernames, and text names.

The target schema has 44 tables with no prefix. Friendships become directional follows. Groups become communities. Pages become creator accounts. The single polymorphic likes table splits into `post_likes` and `comment_likes`. Six analytics tables must be computed from the migrated data. Nineteen of the 44 target tables are either entirely new or derived from indirect sources — the agent can't just rename and reinsert.

### What Makes This Task Interesting

The **conceptual transformation** is what sets this apart from a straightforward rename-and-restructure migration. The agent isn't just changing column names and adding foreign keys — it's changing the *data model*. A bidirectional friendship row becomes a directional follow. A polymorphic likes table gets split by target type. A group with members referenced by group name becomes a community with members referenced by community ID. The agent must understand these semantic shifts from the narrative description alone.

The computed analytics layer adds another dimension. Six tables (`account_stats`, `post_analytics`, `engagement_daily`, `hashtag_trends`, `community_stats`, `migration_log`) must be populated with values derived from the migrated data. The agent has to write GROUP BY queries that COUNT posts per user, SUM likes per post, calculate engagement scores, and track migration progress — all while the source tables use email addresses that need to be resolved to IDs first.

### Scale

| Metric | Value |
|--------|-------|
| Initial tables | 25 (`fb_*` prefix) |
| Target tables | 44 (no prefix) |
| Data | 324 → 479 rows |
| Foreign keys | 58 |
| DEFAULT values | 68 |
| **Total grader checks** | **1,468** |

### Initial Schema Overview

The Facebook legacy database spans the full social platform across 25 `fb_*` tables:

- **Users & identity (3):** `fb_users`, `fb_profiles`, `fb_friendships`
- **Content (5):** `fb_posts`, `fb_comments` (self-referential replies), `fb_likes` (polymorphic), `fb_photos`, `fb_albums`
- **Groups (3):** `fb_groups`, `fb_group_members`, `fb_group_posts`
- **Pages (2):** `fb_pages`, `fb_page_followers`
- **Messaging (2):** `fb_conversations`, `fb_messages`
- **Events (2):** `fb_events`, `fb_event_rsvps`
- **Activity (3):** `fb_notifications`, `fb_activity_log`, `fb_reports`
- **Settings (5):** `fb_privacy_settings`, `fb_blocked_users`, `fb_saved_items`, `fb_hashtags`, `fb_post_hashtags`

### Target Schema Overview (11 domain groups)

| Domain | Tables | Key transformation |
|--------|--------|--------------------|
| **Accounts & Identity** (6) | `accounts`, `profiles`, `account_settings`, `follow_relationships`, `blocked_accounts`, `account_verifications` | Friendships → directional follows |
| **Content & Media** (8) | `media_posts`, `post_comments`, `post_likes`, `comment_likes`, `saved_posts`, `media_albums`, `album_media`, `hashtags` | Polymorphic likes → two tables |
| **Content Relationships** (3) | `post_hashtags`, `post_mentions`, `post_shares` | Text hashtag refs → FK IDs |
| **Stories** (3) | `stories`, `story_views`, `story_highlights` | New concept derived from posts |
| **Communities** (4) | `communities`, `community_members`, `community_posts`, `community_rules` | Groups → communities |
| **Creator** (3) | `creator_accounts`, `creator_followers`, `creator_insights` | Pages → creator accounts |
| **DMs** (3) | `dm_threads`, `dm_participants`, `dm_messages` | Conversations split into threads + participants |
| **Events** (3) | `events`, `event_attendees`, `event_posts` | Name refs → FK IDs |
| **Moderation** (3) | `content_reports`, `moderation_actions`, `activity_log` | New auto-moderation table |
| **Notifications** (2) | `notification_preferences`, `notifications` | Type → title mapping required |
| **Analytics** (6) | `account_stats`, `post_analytics`, `engagement_daily`, `hashtag_trends`, `community_stats`, `migration_log` | All computed from migrated data |

### Key Challenges

1. **Friendship → Follow model** — Bidirectional becomes directional; the agent must understand this conceptual shift
2. **Polymorphic like splitting** — One table filtered by `like_target_type` into two FK-constrained tables
3. **Self-referential comments** — Comment replies create a tree via `parent_comment_id` FK → same table
4. **5 different text reference types** — Email, username, group name, page name, event name — all need resolution
5. **Notification title derivation** — `'like'` → `'New Like'`, `'comment'` → `'New Comment'`, etc.
6. **6 computed analytics tables** — Each with specific COUNT/SUM/formula logic described in prose
7. **19 new or derived tables** — Nearly half the target doesn't map 1:1 from any source

---

## Task 6: E-Commerce Platform Overhaul Expanded (Hard 2)

**Task ID:** `hard_shoplocal_formulas_2`

### The Scenario

The same ShopLocal → NexGenMart acquisition, but at full production scale. ShopLocal's database grew from a scrappy weekend project into a 35-table operation tracking products, orders, shipments, payments, returns, support tickets, marketing campaigns, and inventory across multiple warehouses. Every table still uses the `sl_` prefix, every join is by email/SKU/name text, and every cross-reference is an unindexed text comparison.

NexGenMart's platform team has handed over their 55-table enterprise specification spanning 11 business domains. Every table must be renamed. Every email, name, and SKU text reference must be converted to an integer foreign key. Purchase orders must be split into headers and line items. Returns must be split into requests and items. Four analytics tables must be computed from scratch. The entire 35-table legacy database must be dropped after migration.

This is the migration that would take a senior DBA a full sprint to plan and a weekend to execute. The agent gets the full timeout to attempt it.

### What Makes This Task Interesting

The **depth of the FK dependency chain** is what distinguishes this from the easier tasks. In the hospital task, most tables reference just `patients`. In the Instagram task, most tables reference just `accounts`. Here, `order_items` references `orders` (which references `users`), `products` (which references `categories` and `brands`), and optionally `product_variants` (which references `products`). That's four levels of dependency. The agent must figure out the correct creation order from the narrative alone — if it creates `order_items` before `products`, the FK constraint will fail.

The **breadth of text reference types** adds another layer. The hospital task only resolves emails. The Instagram task resolves emails plus a few names. Here, the agent must resolve four different reference types: customer emails (e.g., `ord_cust_email` → `users.email`), supplier/carrier names (e.g., `po_sup_name` → `vendors.name`), product SKUs (e.g., `oi_prod_sku` → `products.sku`), and coupon codes (e.g., `cu_code` → `discount_codes.code`). Each requires a different JOIN strategy.

The **computed analytics** are the hardest in the suite. `user_cohort_analysis` requires segmenting customers by registration month, then counting orders and revenue within 30-day and 60-day windows after registration — date arithmetic that most LLMs struggle with. `product_performance` aggregates data from four different tables (order_items, reviews, wishlists, returns) into a single row per product. `daily_revenue_summary` has 20 rows grouped by order date with multiple SUM columns.

### Scale

| Metric | Value |
|--------|-------|
| Initial tables | 35 (`sl_*` prefix) |
| Target tables | 55 (no prefix) |
| Data | 404 → 701 rows |
| Foreign keys | 72 |
| DEFAULT values | 98 |
| NOT NULL constraints | 312 |
| **Total grader checks** | **2,336** |

### Initial Schema Overview

The ShopLocal legacy database covers the full e-commerce stack across 35 `sl_*` tables:

- **Customers (3):** `sl_customers` (12 users, embedded addresses), `sl_customer_notes`, `sl_email_subs`
- **Catalog (7):** `sl_products`, `sl_product_variants`, `sl_product_images`, `sl_product_tags`, `sl_categories` (self-referential parent by name), `sl_brands`, `sl_tags`
- **Orders (3):** `sl_orders` (20 orders), `sl_order_items` (35 line items), `sl_payments`
- **Inventory (5):** `sl_warehouses`, `sl_inventory`, `sl_suppliers`, `sl_purchase_orders`, `sl_stock_movements`
- **Shipping (4):** `sl_carriers`, `sl_shipping_zones`, `sl_shipments`, `sl_returns`
- **Marketing (4):** `sl_coupons`, `sl_coupon_uses`, `sl_campaigns`, `sl_wishlists`
- **Support (3):** `sl_agents`, `sl_tickets`, `sl_ticket_msgs`
- **Content (4):** `sl_reviews`, `sl_pages`, `sl_banners`, `sl_tax_rates`
- **Finance (2):** `sl_refunds`, `sl_gift_cards`

Zero foreign keys. Zero indexes. Every cross-reference is a text string.

### Target Schema Overview (11 domain groups)

| Domain | Tables | Key transformation |
|--------|--------|--------------------|
| **Customer** (5) | `users`, `user_addresses`, `user_preferences`, `user_stats`, `user_notes` | Monolithic customer → identity + address + preferences + stats |
| **Catalog** (9) | `categories`, `brands`, `products`, `product_variants`, `product_images`, `tags`, `product_tags`, `product_attributes`, `product_price_history` | Self-referential category FK; 2 new history tables |
| **Orders** (3) | `orders`, `order_items`, `order_status_history` | Email/SKU refs → FK IDs; 66-row status history derived from order lifecycle |
| **Payments** (4) | `payments`, `refunds`, `gift_cards`, `gift_card_transactions` | Multi-FK resolution; new transaction log |
| **Inventory** (7) | `warehouses`, `inventory_levels`, `vendors`, `vendor_products`, `purchase_orders`, `purchase_order_lines`, `inventory_movements` | PO split into header + lines; name → FK resolution |
| **Shipping** (7) | `shipping_carriers`, `delivery_zones`, `zone_carrier_rates`, `shipments`, `shipment_items`, `return_requests`, `return_items` | Returns split into requests + items; new junction table |
| **Marketing** (7) | `discount_codes`, `discount_redemptions`, `marketing_campaigns`, `campaign_discount_links`, `saved_lists`, `saved_list_items`, `newsletter_subscribers` | Wishlists → lists + items; campaign-discount junction |
| **Support** (3) | `support_agents`, `support_tickets`, `ticket_messages` | Name/email → FK resolution |
| **Content** (4) | `product_reviews`, `review_responses`, `content_pages`, `promotional_banners` | SKU/email → FK; new review responses |
| **Finance** (2) | `tax_rules`, `tax_rate_history` | New rate history |
| **Analytics** (4) | `product_performance`, `category_performance`, `daily_revenue_summary`, `user_cohort_analysis` | Complex aggregations with date windowing |

### Key Challenges

1. **Deep FK dependency chains** — Up to 4 levels deep; strict creation order required
2. **4 text reference types** — Email, name, SKU, coupon code — each with different JOIN logic
3. **Table splitting** — Purchase orders → header + lines; returns → requests + items
4. **Self-referential FK** — `categories.parent_id` → `categories(id)`
5. **66-row status history** — Generated from order lifecycle, not directly from any source table
6. **Cohort analysis with date arithmetic** — 30-day and 60-day windows from registration date
7. **98 DEFAULT values** — State columns, numeric defaults, country defaults, booleans — all must match exactly
8. **2,336 grader checks** — The most comprehensive test in the suite

---

## Difficulty Progression

### Compact (Easy / Medium / Hard)

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

### Expanded (Easy 2 / Medium 2 / Hard 2)

| Aspect | Easy 2 (Hospital) | Medium 2 (Instagram) | Hard 2 (E-Commerce) |
|--------|----------------|-------------------|-------------------|
| Initial → Target tables | 31 → 41 | 25 → 44 | 35 → 55 |
| Total data rows | 405 | 479 | 701 |
| Foreign keys | 63 | 58 | 72 |
| Grader checks | 1,635 | 1,468 | 2,336 |
| Text reference types | Email only | Email + username + group/page/event names | Email + name + SKU + code |
| Computed tables | 3 | 6 | 4 (but more complex) |
| Tables not mapping 1:1 | 6 | 19 | 20 |
| Hardest single challenge | Report table split (1→6) | Conceptual model change (friendship→follow) | Cohort analysis with date windowing |

**Easy → Medium**: The leap is conceptual complexity. The hospital migration is mostly filter-split-and-restructure. The Instagram migration requires the agent to understand that polymorphic data must be split by type, comments reference themselves, display names must be concatenated, and groups become communities referenced by name.

**Medium → Hard**: The leap is dependency depth and computation. The e-commerce task has 4 different text reference types (vs 1 for easy, 3 for medium), self-referential categories that require ordered insertion, 3-way FK resolution in a single table, and aggregation queries with NULL handling and GROUP BY.

**Compact → Expanded (×2)**: The leap is scale. Each expanded task covers the *full production operation* with 25–35 initial tables instead of 4–8, and 41–55 target tables instead of 8–11. Grader checks grow from ~200 per task to 1,400–2,300+, meaning the agent has very little room to cut corners — every column type, every NOT NULL, every DEFAULT, every single data row is individually verified across the entire enterprise schema.
