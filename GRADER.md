# Grader — Complete Reference

## What Is the Grader?

The grader runs at the **end** of an episode (when the agent says `mark_done` or hits max steps). It compares the final schema against the target schema and produces a score from 0.0 to 1.0.

The grader is a **flat checklist**. Every item has **equal weight**. Score = `items_passed / total_items`.

---

## What All Things Are We Checking?

We check **everything** about the schema. If the target says it should be there, we check it's there. If the target says it should be gone, we check it's gone.

1. All the **tables** that should be present in the final schema
2. All the **tables** that should have been dropped
3. All the **columns** that should exist (new ones added + existing ones kept)
4. All the **column types** are correct (INT, VARCHAR(100), FLOAT, etc.)
5. All the **column nullable flags** are correct (nullable=True or False)
6. All the **primary keys** are set correctly
7. All the **unique constraints** are set correctly
8. All the **columns** that should have been removed (dropped or renamed away)
9. All the **foreign keys** that should exist (new ones added + existing ones kept)
10. All the **foreign keys** that should have been removed
11. All the **indexes** that should exist
12. All the **indexes** that should have been removed

That's it. A database schema is ONLY made of tables, columns (with type/nullable/PK/unique), foreign keys, and indexes. There is nothing else. Our 12 checks cover every single property.

---

## How the Flow Works

```
Step 1: reset() is called with a task_id
        ↓
Step 2: We load the current_schema and target_schema for that task
        ↓
Step 3: We compare current vs target and build the checklist:
        - For every table in target       → add "table_exists" check
        - For every table NOT in target    → add "table_removed" check
        - For every column in target       → add "column_exists" check
        - For every column in target       → add "column_type_correct" check
        - For every nullable in target     → add "column_nullable_correct" check
        - For every PK in target           → add "column_primary_key_correct" check
        - For every unique in target       → add "column_unique_correct" check
        - For every column NOT in target   → add "column_removed" check
        - For every FK in target           → add "fk_exists" check
        - For every FK NOT in target       → add "fk_removed" check
        - For every index in target        → add "index_exists" check
        - For every index NOT in target    → add "index_removed" check
        ↓
Step 4: Checklist is ready. Say it has 42 items.
        We evaluate it against current_schema → initial score (e.g. 30/42 = 0.714)
        ↓
Step 5: Agent takes an action (e.g. add_column)
        Environment mutates the schema dict
        ↓
Step 6: We re-evaluate the SAME checklist against the UPDATED schema
        Some items flip from ❌ → ✅ (or ✅ → ❌ if agent broke something)
        New score = 33/42 = 0.786
        Reward = 0.786 - 0.714 = +0.071
        ↓
Step 7: Repeat steps 5-6 for every action the agent takes
        ↓
Step 8: Agent says mark_done (or hits max steps)
        Final score = checklist_items_passed / total_items
        This is the GRADE that gets submitted
```

---

## How the Checklist Is Built

At `reset()`, we compare the current schema and target schema to generate every check. The checklist is built once and evaluated after every step.

---

## All 12 Check Types

### SHOULD EXIST (from target schema)

#### 1. `table_exists`
For every table in the target schema, does it exist?

```
Target has: users, orders, products, categories, order_items

Checks generated:
  ✅ table "users" exists
  ✅ table "orders" exists
  ❌ table "products" exists
  ❌ table "categories" exists
  ❌ table "order_items" exists

Count: 1 check per table in target
```

#### 2. `column_exists`
For every column in every table in the target schema, does it exist?

```
Target says users should have: id, name, email, phone
Current users has: id, name, email

Checks generated:
  ✅ users.id exists
  ✅ users.name exists
  ✅ users.email exists
  ❌ users.phone exists

Count: 1 check per column in every target table
```

#### 3. `column_type_correct`
For every column in the target, is the data type correct?

This is SEPARATE from column_exists — a column can exist but have the wrong type. That gives partial credit (passes check 2, fails check 3).

```
Target says: users.age should be INT
Current has: users.age as VARCHAR(10)

Checks generated:
  ❌ users.age type is INT    (currently VARCHAR(10))

Count: 1 check per column in every target table
```

#### 4. `column_nullable_correct`
For every column that has a nullable constraint in the target, is the flag correct?

```
Target says: users.email nullable=False
Current has: users.email nullable=True

Checks generated:
  ❌ users.email nullable is False

Count: 1 check per column that has nullable defined in target
```

#### 5. `column_primary_key_correct`
For every column that should be a primary key, is the flag set?

```
Target says: users.id primary_key=True, orders.id primary_key=True

Checks generated:
  ✅ users.id is primary key
  ✅ orders.id is primary key

Count: 1 check per primary key column in target
```

#### 6. `column_unique_correct`
For every column that should have a unique constraint, is it set?

```
Target says: users.email unique=True

Checks generated:
  ✅ users.email is unique

Count: 1 check per unique column in target
```

#### 7. `fk_exists`
For every foreign key in the target, does it exist? Must match all 3 parts: column, referenced table, referenced column.

```
Target says:
  orders.user_id FK → users.id
  order_items.product_id FK → products.id
  order_items.order_id FK → orders.id

Checks generated:
  ✅ FK orders.user_id → users.id exists
  ❌ FK order_items.product_id → products.id exists
  ❌ FK order_items.order_id → orders.id exists

Count: 1 check per FK in target
```

#### 8. `index_exists`
For every index in the target, does it exist? Must match column name and unique flag.

```
Target says:
  index on users.email (unique=True)
  index on orders.created_at (unique=False)

Checks generated:
  ✅ index on users.email exists (unique=True)
  ❌ index on orders.created_at exists (unique=False)

Count: 1 check per index in target
```

---

### SHOULD BE GONE (in current but not in target)

#### 9. `table_removed`
For every table that exists in current but NOT in target, it should be gone.

```
Current has: users, orders, legacy_cache, temp_logs
Target has: users, orders, products

Checks generated:
  ❌ table "legacy_cache" removed    (still exists)
  ❌ table "temp_logs" removed       (still exists)

Count: 1 check per table in current but NOT in target
```

#### 10. `column_removed`
For every column that exists in current but NOT in the target (within tables that still exist), it should be gone.

```
Current orders has: id, user_id, total, legacy_field
Target orders has: id, user_id, amount, status

Checks generated:
  ❌ orders.total removed         (still exists, should have been renamed to "amount")
  ❌ orders.legacy_field removed  (still exists, should have been dropped)

Count: 1 check per column in current but NOT in target (for surviving tables)
```

#### 11. `fk_removed`
For every FK that exists in current but NOT in target, it should be gone.

```
Current has: orders.old_cat_id FK → old_categories.id
Target has: no such FK

Checks generated:
  ❌ FK orders.old_cat_id → old_categories.id removed

Count: 1 check per FK in current but NOT in target
```

#### 12. `index_removed`
For every index that exists in current but NOT in target, it should be gone.

```
Current has: index on users.legacy_score
Target has: no such index

Checks generated:
  ❌ index on users.legacy_score removed

Count: 1 check per index in current but NOT in target
```

---

## Summary Table

| # | Check Type | What It Verifies | Passes When | Count Source |
|---|---|---|---|---|
| 1 | `table_exists` | Target table is present | Table name found in schema | 1 per table in target |
| 2 | `column_exists` | Target column is present | Column found in the table | 1 per column in target |
| 3 | `column_type_correct` | Column has correct type | Type matches exactly | 1 per column in target |
| 4 | `column_nullable_correct` | Nullable flag is correct | Nullable matches expected | 1 per column with nullable |
| 5 | `column_primary_key_correct` | PK flag is correct | primary_key is True | 1 per PK in target |
| 6 | `column_unique_correct` | Unique constraint is correct | unique is True | 1 per unique in target |
| 7 | `fk_exists` | Target FK is present | col + ref_table + ref_col match | 1 per FK in target |
| 8 | `index_exists` | Target index is present | col + unique flag match | 1 per index in target |
| 9 | `table_removed` | Old table is gone | Table NOT in schema | 1 per table to drop |
| 10 | `column_removed` | Old column is gone | Column NOT in table | 1 per column to drop |
| 11 | `fk_removed` | Old FK is gone | FK no longer exists | 1 per FK to drop |
| 12 | `index_removed` | Old index is gone | Index no longer exists | 1 per index to drop |

---

## Example — Medium Task Checklist Count

```
SHOULD EXIST:
  Tables:            8 checks
  Columns:          35 checks
  Column types:     35 checks
  Column nullable:  20 checks
  Column PK:         8 checks
  Column unique:     3 checks
  Foreign keys:      6 checks
  Indexes:           3 checks

SHOULD BE GONE:
  Tables removed:    1 check
  Columns removed:   4 checks
  FKs removed:       1 check
  Indexes removed:   1 check

TOTAL = 125 checks
Each check = 1/125 = 0.008 of the score
```

---

## Score Formula

```
score = checks_that_pass / total_checks
```

That's it. No weights, no categories, no complexity. Every check is binary (pass/fail). Every check has equal weight.
