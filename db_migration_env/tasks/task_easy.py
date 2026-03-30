"""Task 1 (Easy): Restructure Employee Table + Add Departments.

Initial: A single `employees` table with embedded department info, no constraints.
Target:
  - `departments` table (deduplicated from employees)
  - `employees` table restructured: remove dept columns, add dept FK, add status column,
    add hire_year extracted from hire_date, add an index on email.
  - `audit_log` table with one entry per employee recording the migration.

This is "easy" but still requires:
  - Table creation with FKs
  - INSERT ... SELECT DISTINCT for dedup
  - Table recreation (SQLite no DROP COLUMN) to remove embedded dept columns
  - Data transformation (extract year from date)
  - Index creation

Expected steps for a perfect agent: 8-15
"""

TASK_ID = "easy_restructure_employees"
TASK_DESCRIPTION = (
    "Restructure the employee database: "
    "(1) Extract unique departments into a new 'departments' table with an auto-assigned id. "
    "(2) Restructure 'employees' to remove department_name and department_floor columns, "
    "add a department_id FK, add a 'status' column defaulting to 'active', "
    "and add 'hire_year' INTEGER extracted from hire_date. "
    "(3) Create an 'audit_log' table logging each employee_id with action='migrated'. "
    "(4) Create a UNIQUE index 'idx_employees_email' on employees(email). "
    "Preserve all data."
)
DIFFICULTY = "easy"
MAX_STEPS = 30

INITIAL_SQL = """
CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    hire_date TEXT NOT NULL,
    salary REAL NOT NULL,
    department_name TEXT NOT NULL,
    department_floor INTEGER NOT NULL
);

INSERT INTO employees VALUES (1,  'Alice Johnson',   'alice@corp.com',   '2020-03-15', 85000.0,  'Engineering',  3);
INSERT INTO employees VALUES (2,  'Bob Smith',       'bob@corp.com',     '2019-07-22', 72000.0,  'Marketing',    2);
INSERT INTO employees VALUES (3,  'Charlie Brown',   'charlie@corp.com', '2021-01-10', 91000.0,  'Engineering',  3);
INSERT INTO employees VALUES (4,  'Diana Prince',    'diana@corp.com',   '2018-11-05', 68000.0,  'Sales',        1);
INSERT INTO employees VALUES (5,  'Eve Williams',    'eve@corp.com',     '2022-06-30', 78000.0,  'Marketing',    2);
INSERT INTO employees VALUES (6,  'Frank Castle',    'frank@corp.com',   '2020-09-12', 95000.0,  'Engineering',  3);
INSERT INTO employees VALUES (7,  'Grace Hopper',    'grace@corp.com',   '2017-04-01', 110000.0, 'Engineering',  3);
INSERT INTO employees VALUES (8,  'Hank Pym',        'hank@corp.com',    '2023-02-14', 62000.0,  'Sales',        1);
INSERT INTO employees VALUES (9,  'Ivy Chen',        'ivy@corp.com',     '2021-08-20', 74000.0,  'Marketing',    2);
INSERT INTO employees VALUES (10, 'Jack Ryan',       'jack@corp.com',    '2019-12-01', 88000.0,  'Sales',        1);
"""

TARGET_SQL = """
CREATE TABLE departments (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    floor INTEGER NOT NULL
);

INSERT INTO departments VALUES (1, 'Engineering', 3);
INSERT INTO departments VALUES (2, 'Marketing',   2);
INSERT INTO departments VALUES (3, 'Sales',       1);

CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    hire_date TEXT NOT NULL,
    hire_year INTEGER NOT NULL,
    salary REAL NOT NULL,
    department_id INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'active',
    FOREIGN KEY (department_id) REFERENCES departments(id)
);

INSERT INTO employees VALUES (1,  'Alice Johnson',   'alice@corp.com',   '2020-03-15', 2020, 85000.0,  1, 'active');
INSERT INTO employees VALUES (2,  'Bob Smith',       'bob@corp.com',     '2019-07-22', 2019, 72000.0,  2, 'active');
INSERT INTO employees VALUES (3,  'Charlie Brown',   'charlie@corp.com', '2021-01-10', 2021, 91000.0,  1, 'active');
INSERT INTO employees VALUES (4,  'Diana Prince',    'diana@corp.com',   '2018-11-05', 2018, 68000.0,  3, 'active');
INSERT INTO employees VALUES (5,  'Eve Williams',    'eve@corp.com',     '2022-06-30', 2022, 78000.0,  2, 'active');
INSERT INTO employees VALUES (6,  'Frank Castle',    'frank@corp.com',   '2020-09-12', 2020, 95000.0,  1, 'active');
INSERT INTO employees VALUES (7,  'Grace Hopper',    'grace@corp.com',   '2017-04-01', 2017, 110000.0, 1, 'active');
INSERT INTO employees VALUES (8,  'Hank Pym',        'hank@corp.com',    '2023-02-14', 2023, 62000.0,  3, 'active');
INSERT INTO employees VALUES (9,  'Ivy Chen',        'ivy@corp.com',     '2021-08-20', 2021, 74000.0,  2, 'active');
INSERT INTO employees VALUES (10, 'Jack Ryan',       'jack@corp.com',    '2019-12-01', 2019, 88000.0,  3, 'active');

CREATE TABLE audit_log (
    id INTEGER PRIMARY KEY,
    employee_id INTEGER NOT NULL,
    action TEXT NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES employees(id)
);

INSERT INTO audit_log VALUES (1,  1,  'migrated');
INSERT INTO audit_log VALUES (2,  2,  'migrated');
INSERT INTO audit_log VALUES (3,  3,  'migrated');
INSERT INTO audit_log VALUES (4,  4,  'migrated');
INSERT INTO audit_log VALUES (5,  5,  'migrated');
INSERT INTO audit_log VALUES (6,  6,  'migrated');
INSERT INTO audit_log VALUES (7,  7,  'migrated');
INSERT INTO audit_log VALUES (8,  8,  'migrated');
INSERT INTO audit_log VALUES (9,  9,  'migrated');
INSERT INTO audit_log VALUES (10, 10, 'migrated');
"""
