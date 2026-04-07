# Task Descriptions

This document describes the three migration tasks in the DB Migration RL Environment. Each task models a realistic company acquisition scenario where a legacy database must be restructured into a modern enterprise schema. All tasks operate in **narrative mode** — the agent cannot see the target schema and must derive the migration plan entirely from a natural-language specification.

---

## Task 1: Hospital Migration (Easy)

**Task ID:** `easy_hospital_migration`
**Difficulty:** Easy
**Timeout:** 3,600 seconds

### Story

HealthFirst Community Clinic, a small neighbourhood clinic, was recently acquired by MedCore Enterprise Hospital System. Five years ago HealthFirst hired a local developer who built a basic digital system — 31 tables with an `hc_` prefix, patient email addresses used as cross-references instead of foreign keys, a single monolithic `hc_reports` table for every type of diagnostic report, zero indexes, and abbreviated column names like `pt_fname` and `ins_copay`.

MedCore requires a complete migration into their 41-table enterprise schema with proper foreign keys, NOT NULL constraints, DEFAULT values, indexes on lookup columns, and full data preservation.

### Scale

| Metric | Value |
|--------|-------|
| Initial tables | 31 (`hc_*` prefix) |
| Initial rows | 355 |
| Target tables | 41 (no prefix) |
| Target rows | 405 |
| Target columns | 381 |
| Foreign keys | 63 |
| NOT NULL constraints | 227 |
| DEFAULT values | 65 |
| Indexes | 48 |
| **Total grader checks** | **1,635** |

### Initial Schema (31 `hc_*` tables)

The legacy database covers a full clinic operation:

- **Patient identity:** `hc_patients` (embedded address fields), `hc_patient_contacts`, `hc_insurance`, `hc_allergies`, `hc_immunizations`, `hc_medical_history`
- **Staff:** `hc_doctors`, `hc_nurses`, `hc_departments`, `hc_shifts`
- **Clinical operations:** `hc_appointments`, `hc_clinic_notes`, `hc_vitals`, `hc_diagnoses`, `hc_procedures`, `hc_surgeries`, `hc_prescriptions`, `hc_medications`, `hc_referrals`, `hc_follow_ups`, `hc_consent_forms`
- **Diagnostics:** `hc_reports` (one monolithic table for ALL report types — lab, X-ray, MRI, CT, pathology, ultrasound), `hc_lab_orders`
- **Billing & admin:** `hc_billing`, `hc_payments`, `hc_pharmacy_inventory`, `hc_equipment`, `hc_rooms`, `hc_ward_beds`, `hc_waiting_list`, `hc_audit_log`

All cross-references use patient email addresses (e.g., `hc_appointments.apt_patient_email`) rather than integer foreign keys. Column names are abbreviated (e.g., `pt_fname`, `doc_specialty`, `ins_copay`).

### Target Schema (41 tables)

The target enterprise schema introduces:

- **Address normalisation:** Patient addresses extracted from `hc_patients` into a separate `patient_addresses` table
- **Report splitting:** The monolithic `hc_reports` table (which stored lab results, X-rays, MRIs, CT scans, pathology, and ultrasound reports in one table with a `rpt_type` column) must be split into six dedicated tables: `lab_results`, `xray_reports`, `mri_reports`, `ct_scan_reports`, `pathology_reports`, `ultrasound_reports`
- **New derived tables:** `patient_stats` (computed from appointments, prescriptions, and billing), `department_stats` (computed from doctors and appointments), `department_heads` (derived from doctor seniority)
- **Structural additions:** `wards` table (new), `beds` table (restructured from `hc_ward_beds`)
- **Full FK resolution:** Every email-based reference replaced with integer foreign keys
- **48 indexes** on frequently queried columns

### Key Migration Challenges

1. **Report table splitting** — The agent must read the `hc_reports.rpt_type` column to determine which rows go to which specialised table. Each target report table has different columns appropriate to that report type.
2. **Address extraction** — Patient addresses are embedded as columns in `hc_patients` (`pt_addr_line`, `pt_addr_city`, etc.) and must be split into a separate `patient_addresses` table with a foreign key back to `patients`.
3. **Email → FK resolution** — All 31 legacy tables use email addresses for cross-references. The agent must write JOINs like `JOIN patients ON hc_appointments.apt_patient_email = patients.email` to resolve these to integer IDs.
4. **Computed statistics** — `patient_stats` requires COUNT/SUM aggregations across appointments, prescriptions, and billing tables. `department_stats` requires similar aggregations across doctors and appointments.
5. **48 indexes** — The target schema requires indexes on nearly every foreign key column and commonly queried fields.

---

## Task 2: Social Media Migration (Medium)

**Task ID:** `medium_instagram_migration`
**Difficulty:** Medium
**Timeout:** 3,600 seconds

### Story

Meta is consolidating its social platforms. Facebook's entire legacy database must be migrated into a new unified Instagram-style schema. All Facebook users, their content, interactions, relationships, and activity history need to move to a normalized schema designed for a media-centric platform. The legacy system stores everything using email addresses and text references — the new system requires proper integer foreign keys throughout.

### Scale

| Metric | Value |
|--------|-------|
| Initial tables | 25 (`fb_*` prefix) |
| Initial rows | 324 |
| Target tables | 44 (no prefix) |
| Target rows | 479 |
| Target columns | 282 |
| Foreign keys | 58 |
| NOT NULL constraints | 186 |
| DEFAULT values | 68 |
| **Total grader checks** | **1,468** |

### Initial Schema (25 `fb_*` tables)

The Facebook legacy database spans the full social platform:

- **Users & identity (3 tables):** `fb_users` (10 users with email, username, name, city, country), `fb_profiles` (bio, avatar, occupation, referenced by email), `fb_friendships` (bidirectional, email-based)
- **Content (5 tables):** `fb_posts` (text/photo/video/link types), `fb_comments` (with self-referential parent for replies), `fb_likes` (polymorphic — targets both posts and comments via `like_target_type`), `fb_photos` (album-based, referenced by album name), `fb_albums`
- **Groups (3 tables):** `fb_groups`, `fb_group_members` (referenced by group name), `fb_group_posts` (referenced by group name)
- **Pages (2 tables):** `fb_pages` (business pages), `fb_page_followers` (referenced by page name)
- **Messaging (2 tables):** `fb_conversations`, `fb_messages` (sender referenced by email)
- **Events (2 tables):** `fb_events`, `fb_event_rsvps` (referenced by event name)
- **Activity (3 tables):** `fb_notifications`, `fb_activity_log`, `fb_reports`
- **Settings (5 tables):** `fb_privacy_settings`, `fb_blocked_users`, `fb_saved_items`, `fb_hashtags`, `fb_post_hashtags`

### Target Schema (44 tables, 11 domain groups)

The Instagram-style target schema reorganises everything:

| Domain | Tables | Key transformations |
|--------|--------|-------------------|
| **Accounts & Identity** (6) | `accounts`, `profiles`, `account_settings`, `follow_relationships`, `blocked_accounts`, `account_verifications` | Bidirectional friendships → directional follows; privacy settings → account_settings; new verification table |
| **Content & Media** (8) | `media_posts`, `post_comments`, `post_likes`, `comment_likes`, `saved_posts`, `media_albums`, `album_media`, `hashtags` | Polymorphic likes split into `post_likes` + `comment_likes`; new `album_media` junction table |
| **Content Relationships** (3) | `post_hashtags`, `post_mentions`, `post_shares` | Hashtag text references → FK IDs; new mentions and shares tables |
| **Stories** (3) | `stories`, `story_views`, `story_highlights` | Entirely new tables derived from recent photo posts |
| **Communities** (4) | `communities`, `community_members`, `community_posts`, `community_rules` | Groups renamed to communities; group name references → FK IDs; new rules table |
| **Business & Creator** (3) | `creator_accounts`, `creator_followers`, `creator_insights` | Pages → creator accounts; computed insights table |
| **Direct Messages** (3) | `dm_threads`, `dm_participants`, `dm_messages` | Conversations split into threads + participants; email refs → FK IDs |
| **Events** (3) | `events`, `event_attendees`, `event_posts` | Event name references → FK IDs; new event_posts table |
| **Moderation** (3) | `content_reports`, `moderation_actions`, `activity_log` | New moderation_actions table (one per report) |
| **Notifications** (2) | `notification_preferences`, `notifications` | Privacy settings → notification_preferences; notification type → title mapping |
| **Analytics** (6) | `account_stats`, `post_analytics`, `engagement_daily`, `hashtag_trends`, `community_stats`, `migration_log` | All computed from migrated data using COUNT/SUM/AVG |

### Key Migration Challenges

1. **Friendship → Follow conversion** — Facebook friendships are bidirectional (`f_user1_email`, `f_user2_email`). Instagram follows are directional. Each friendship becomes one follow relationship (user1 follows user2).
2. **Polymorphic like splitting** — `fb_likes` has a `like_target_type` column ('post' or 'comment') and a `like_target_id`. These must be split into two separate tables: `post_likes` (FK → `media_posts`) and `comment_likes` (FK → `post_comments`).
3. **Self-referential comments** — `fb_comments.cmt_parent_id` creates a comment reply tree. The target `post_comments.parent_comment_id` is a self-referential FK that must be preserved.
4. **Group name → community ID resolution** — `fb_group_members` and `fb_group_posts` reference groups by name string. The agent must JOIN against `communities.name` to get integer IDs.
5. **Notification title mapping** — The `notifications.title` column must be derived from `notif_type` using specific rules: `'like'` → `'New Like'`, `'comment'` → `'New Comment'`, `'friend_request'` → `'Follow Request'`, etc.
6. **6 computed analytics tables** — `account_stats` (post count, follower count, following count, likes received), `post_analytics` (like/comment/share/save counts, view_count formula), `engagement_daily` (monthly aggregations), `hashtag_trends`, `community_stats`, `migration_log`. Each requires specific COUNT/SUM/JOIN logic.
7. **19 new or derived tables** — Nearly half the target tables don't map directly from a single source table. Tables like `stories`, `story_views`, `post_mentions`, `community_rules`, `moderation_actions`, and `account_verifications` must be created from scratch or derived from indirect sources.

---

## Task 3: E-Commerce Platform Overhaul (Hard)

**Task ID:** `hard_shoplocal_formulas`
**Difficulty:** Hard
**Timeout:** 3,600 seconds

### Story

ShopLocal, a scrappy artisan e-commerce platform built by a team of three over five years, has been acquired by NexGenMart, a major enterprise retail company. ShopLocal's database was built quick and dirty — email references instead of foreign keys, no indexes, no constraints, denormalized tables, and inconsistent naming throughout. NexGenMart's platform team requires a complete schema migration to their enterprise standard before any data can flow into production systems.

### Scale

| Metric | Value |
|--------|-------|
| Initial tables | 35 (`sl_*` prefix) |
| Initial rows | 404 |
| Target tables | 55 (no prefix) |
| Target rows | 701 |
| Target columns | 504 |
| Foreign keys | 72 |
| NOT NULL constraints | 312 |
| DEFAULT values | 98 |
| **Total grader checks** | **2,336** |

### Initial Schema (35 `sl_*` tables)

The ShopLocal legacy database covers the full e-commerce stack:

- **Customers (3 tables):** `sl_customers` (12 users with embedded address fields), `sl_customer_notes`, `sl_email_subs`
- **Catalog (7 tables):** `sl_products` (15 products, SKU/name/category/brand as text), `sl_product_variants`, `sl_product_images`, `sl_product_tags`, `sl_categories` (with self-referential parent by name), `sl_brands`, `sl_tags`
- **Orders (3 tables):** `sl_orders` (20 orders, customer referenced by email), `sl_order_items` (35 line items, product referenced by SKU), `sl_payments`
- **Inventory (5 tables):** `sl_warehouses`, `sl_inventory` (product by SKU, warehouse by name), `sl_suppliers`, `sl_purchase_orders` (supplier by name, product by SKU, warehouse by name), `sl_stock_movements`
- **Shipping (4 tables):** `sl_carriers`, `sl_shipping_zones` (carrier by name), `sl_shipments` (carrier by name), `sl_returns` (customer by email)
- **Marketing (4 tables):** `sl_coupons`, `sl_coupon_uses` (coupon by code, customer by email), `sl_campaigns`, `sl_wishlists` (product by SKU, customer by email)
- **Support (3 tables):** `sl_agents`, `sl_tickets` (customer by email, agent by name), `sl_ticket_msgs`
- **Content (4 tables):** `sl_reviews` (product by SKU, customer by email), `sl_pages` (author by email), `sl_banners`, `sl_tax_rates`
- **Finance (2 tables):** `sl_refunds`, `sl_gift_cards` (customer by email)

Every cross-reference is text-based — emails, names, SKU codes. Zero foreign keys. Zero indexes.

### Target Schema (55 tables, 11 domain groups)

NexGenMart's enterprise schema organises data into 11 clean domains:

| Domain | Tables | Description |
|--------|--------|-------------|
| **Customer** (5) | `users`, `user_addresses`, `user_preferences`, `user_stats`, `user_notes` | Split monolithic `sl_customers` into identity + addresses + preferences; computed user stats |
| **Catalog** (8) | `categories`, `brands`, `products`, `product_variants`, `product_images`, `tags`, `product_tags`, `product_attributes`, `product_price_history` | Self-referential category FK; new attributes and price history tables |
| **Orders** (3) | `orders`, `order_items`, `order_status_history` | Customer email → user_id FK; product SKU → product_id FK; new status history (66 rows derived from order lifecycle) |
| **Payments** (4) | `payments`, `refunds`, `gift_cards`, `gift_card_transactions` | Multi-FK resolution (order, user, payment); new gift card transaction log |
| **Inventory** (7) | `warehouses`, `inventory_levels`, `vendors`, `vendor_products`, `purchase_orders`, `purchase_order_lines`, `inventory_movements` | Supplier name → vendor_id FK; SKU → product_id; warehouse name → warehouse_id; PO split into header + lines |
| **Shipping** (7) | `shipping_carriers`, `delivery_zones`, `zone_carrier_rates`, `shipments`, `shipment_items`, `return_requests`, `return_items` | Carrier name → carrier_id FK; new zone-carrier junction table; returns split into header + items |
| **Marketing** (7) | `discount_codes`, `discount_redemptions`, `marketing_campaigns`, `campaign_discount_links`, `saved_lists`, `saved_list_items`, `newsletter_subscribers` | Coupon code → discount_code_id FK; wishlist restructured into list + items; campaign-discount junction table |
| **Support** (3) | `support_agents`, `support_tickets`, `ticket_messages` | Agent name → agent_id FK; customer email → user_id FK |
| **Content** (4) | `product_reviews`, `review_responses`, `content_pages`, `promotional_banners` | Product SKU → product_id FK; customer email → user_id FK; new review responses |
| **Finance** (2) | `tax_rules`, `tax_rate_history` | New tax rate history table |
| **Analytics** (4) | `product_performance`, `category_performance`, `daily_revenue_summary`, `user_cohort_analysis` | All computed from migrated data |

### Key Migration Challenges

1. **Massive scale** — 35 → 55 tables, 404 → 701 rows, 2,336 individual grader checks. The agent must maintain consistency across the entire migration.
2. **Deep FK chains** — Some tables are 3-4 levels deep in FK dependencies. `order_items` references both `orders` (which references `users`) and `products` (which references `categories` and `brands`). Tables must be created and populated in correct dependency order.
3. **Self-referential FK** — `categories.parent_id` references `categories(id)`. The agent must first create the table, then populate it carefully so parent categories exist before child categories reference them.
4. **Purchase order splitting** — `sl_purchase_orders` is one table that must be split into `purchase_orders` (header) and `purchase_order_lines` (line items), each with their own FKs.
5. **Multi-source text resolution** — A single INSERT may require JOINs across 3+ source tables. For example, populating `order_items` requires joining `sl_order_items.oi_prod_sku` → `products.sku` for product_id, `sl_order_items.oi_variant_sku` → `product_variants.variant_sku` for variant_id, plus the order_id from the parent order.
6. **Computed analytics** — 4 tables require complex aggregations:
   - `product_performance`: units sold, revenue, avg rating, review count, wishlist count, return count — each from a different source table
   - `category_performance`: product count, total revenue, average rating, top product by revenue — requires subqueries
   - `daily_revenue_summary`: 20 rows grouped by order date — COUNT, SUM across multiple financial columns
   - `user_cohort_analysis`: 4 rows segmented by registration month — requires date arithmetic for month-1 and month-2 order windows
7. **Order status history** — `order_status_history` has 66 rows, the largest derived table. Each order gets multiple status entries (placed → processing → shipped → delivered) that must be generated from the order lifecycle dates in `sl_orders`.
8. **98 DEFAULT values** — The target schema has DEFAULT values on nearly every table, including state columns (`DEFAULT 'active'`), numeric defaults (`DEFAULT 0`, `DEFAULT 0.0`), country defaults (`DEFAULT 'US'`), and boolean defaults (`DEFAULT 1`). The agent must match each one exactly.

---

## Difficulty Comparison

| Aspect | Easy (Hospital) | Medium (Instagram) | Hard (E-Commerce) |
|--------|----------------|-------------------|-------------------|
| Initial tables | 31 | 25 | 35 |
| Target tables | 41 | 44 | 55 |
| Total rows | 405 | 479 | 701 |
| Foreign keys | 63 | 58 | 72 |
| Grader checks | 1,635 | 1,468 | 2,336 |
| Indexes required | 48 | 0 | 0 |
| Computed tables | 3 | 6 | 4 |
| Table splitting | 1 (reports → 6) | 1 (likes → 2) | 2 (POs, returns) |
| Self-referential FK | No | Yes (comments) | Yes (categories) |
| New derived tables | 6 | 19 | 20 |
| Text ref types | Email only | Email + username + group name + page name + event name | Email + name + SKU + code |

### What Makes Each Level Harder

**Easy → Medium:** The medium task introduces polymorphic data splitting (likes by target type), bidirectional-to-directional relationship conversion (friendships → follows), and significantly more computed tables (6 vs 3). The social media domain also has more indirect references (group names, page names, event names) compared to the hospital's email-only references.

**Medium → Hard:** The hard task has the most tables (55), the most rows (701), and the most grader checks (2,336). It requires resolving references across 4 different text types (email, name, SKU, code) instead of just email. The FK dependency chains are deeper (3-4 levels), the computed analytics are more complex (cohort analysis with date windowing), and there are more tables that must be split from single sources (purchase orders → header + lines, returns → requests + items).

### Narrative Mode

All three tasks operate in **narrative mode** — the agent's observation contains an empty `target_schema` and empty `schema_diff`. The only guide is the `task_description`: a detailed natural-language specification (30-38K characters) that describes each target table in prose, including column definitions, source mappings, FK relationships, and computation logic.

The agent must:
1. Parse the narrative to understand the target schema
2. Determine the correct table creation order (FK dependencies)
3. Write SQL to create tables with proper constraints
4. Write INSERT...SELECT statements with JOINs to resolve text references
5. Compute aggregated/derived data using GROUP BY, COUNT, SUM, AVG
6. Drop all legacy tables after migration

This is intentionally harder than traditional environments where the agent can see the target state directly and compute a diff.
