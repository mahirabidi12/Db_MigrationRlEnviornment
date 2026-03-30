"""Task 2 (Medium): Multi-Table School Database Normalization.

Initial: Two denormalized tables — `student_courses` (flat enrollment records)
         and `student_contacts` (contact info with duplicates).
Target:  Fully normalized schema with 5 tables:
         - `students` (deduplicated, with computed GPA)
         - `courses` (deduplicated)
         - `enrollments` (junction table, student_id + course_id FK)
         - `contacts` (one-to-one with students)
         - `course_stats` (aggregated: enrollment_count, avg_grade per course)

Skills tested:
  - Multi-table deduplication with different keys
  - Junction table creation (many-to-many)
  - Computed/aggregated data (GPA calculation, enrollment counts)
  - Data reconciliation between two source tables
  - Handling NULL grades (some students enrolled but not yet graded)
  - DROP TABLE cleanup

Expected steps: 15-25
"""

TASK_ID = "medium_school_normalize"
TASK_DESCRIPTION = (
    "Normalize the school database from 2 denormalized tables into 5 normalized tables: "
    "(1) 'students' — deduplicated from student_courses, with computed 'gpa' REAL "
    "(average of non-NULL grades, NULL if no grades). "
    "(2) 'courses' — unique courses with name, credits, department. "
    "(3) 'enrollments' — junction table (student_id, course_id, grade) with FKs. "
    "(4) 'contacts' — from student_contacts, deduplicated by student email, FK to students. "
    "(5) 'course_stats' — one row per course: enrollment_count INTEGER, avg_grade REAL. "
    "Drop both original tables when done. All data must be preserved."
)
DIFFICULTY = "medium"
MAX_STEPS = 40

INITIAL_SQL = """
CREATE TABLE student_courses (
    id INTEGER PRIMARY KEY,
    student_name TEXT NOT NULL,
    student_email TEXT NOT NULL,
    student_year INTEGER NOT NULL,
    course_name TEXT NOT NULL,
    course_credits INTEGER NOT NULL,
    course_department TEXT NOT NULL,
    grade REAL
);

INSERT INTO student_courses VALUES (1,  'Alice Wang',    'alice@uni.edu',   2, 'Calculus I',       4, 'Mathematics',      3.7);
INSERT INTO student_courses VALUES (2,  'Alice Wang',    'alice@uni.edu',   2, 'Physics I',        4, 'Physics',          3.5);
INSERT INTO student_courses VALUES (3,  'Alice Wang',    'alice@uni.edu',   2, 'English Comp',     3, 'English',          3.9);
INSERT INTO student_courses VALUES (4,  'Bob Patel',     'bob@uni.edu',     3, 'Calculus I',       4, 'Mathematics',      2.8);
INSERT INTO student_courses VALUES (5,  'Bob Patel',     'bob@uni.edu',     3, 'Data Structures',  3, 'Computer Science', 3.2);
INSERT INTO student_courses VALUES (6,  'Carol Lopez',   'carol@uni.edu',   1, 'English Comp',     3, 'English',          NULL);
INSERT INTO student_courses VALUES (7,  'Carol Lopez',   'carol@uni.edu',   1, 'Calculus I',       4, 'Mathematics',      NULL);
INSERT INTO student_courses VALUES (8,  'Dave Kim',      'dave@uni.edu',    4, 'Data Structures',  3, 'Computer Science', 3.9);
INSERT INTO student_courses VALUES (9,  'Dave Kim',      'dave@uni.edu',    4, 'Physics I',        4, 'Physics',          3.6);
INSERT INTO student_courses VALUES (10, 'Dave Kim',      'dave@uni.edu',    4, 'Algorithms',       3, 'Computer Science', 3.8);
INSERT INTO student_courses VALUES (11, 'Eve Tanaka',    'eve@uni.edu',     2, 'Calculus I',       4, 'Mathematics',      3.0);
INSERT INTO student_courses VALUES (12, 'Eve Tanaka',    'eve@uni.edu',     2, 'English Comp',     3, 'English',          3.4);
INSERT INTO student_courses VALUES (13, 'Frank Russo',   'frank@uni.edu',   3, 'Algorithms',       3, 'Computer Science', 2.5);
INSERT INTO student_courses VALUES (14, 'Frank Russo',   'frank@uni.edu',   3, 'Physics I',        4, 'Physics',          2.9);
INSERT INTO student_courses VALUES (15, 'Frank Russo',   'frank@uni.edu',   3, 'Calculus I',       4, 'Mathematics',      2.7);

CREATE TABLE student_contacts (
    id INTEGER PRIMARY KEY,
    student_email TEXT NOT NULL,
    phone TEXT,
    address TEXT,
    emergency_contact TEXT
);

INSERT INTO student_contacts VALUES (1, 'alice@uni.edu',  '555-1001', '100 Elm St, Boston',     'Mary Wang 555-1002');
INSERT INTO student_contacts VALUES (2, 'bob@uni.edu',    '555-2001', '200 Oak Ave, Cambridge', 'Raj Patel 555-2002');
INSERT INTO student_contacts VALUES (3, 'carol@uni.edu',  '555-3001', '300 Pine Rd, Somerville','Ana Lopez 555-3002');
INSERT INTO student_contacts VALUES (4, 'dave@uni.edu',   '555-4001', '400 Maple Dr, Brookline','Jun Kim 555-4002');
INSERT INTO student_contacts VALUES (5, 'eve@uni.edu',    '555-5001', '500 Cedar Ln, Newton',   'Yuki Tanaka 555-5002');
INSERT INTO student_contacts VALUES (6, 'frank@uni.edu',  '555-6001', '600 Birch Ct, Medford',  'Gina Russo 555-6002');
INSERT INTO student_contacts VALUES (7, 'alice@uni.edu',  '555-1001', '100 Elm St, Boston',     'Mary Wang 555-1002');
"""

TARGET_SQL = """
CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    year INTEGER NOT NULL,
    gpa REAL
);

INSERT INTO students VALUES (1, 'Alice Wang',   'alice@uni.edu',  2, 3.7);
INSERT INTO students VALUES (2, 'Bob Patel',    'bob@uni.edu',    3, 3.0);
INSERT INTO students VALUES (3, 'Carol Lopez',  'carol@uni.edu',  1, NULL);
INSERT INTO students VALUES (4, 'Dave Kim',     'dave@uni.edu',   4, 3.77);
INSERT INTO students VALUES (5, 'Eve Tanaka',   'eve@uni.edu',    2, 3.2);
INSERT INTO students VALUES (6, 'Frank Russo',  'frank@uni.edu',  3, 2.7);

CREATE TABLE courses (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    credits INTEGER NOT NULL,
    department TEXT NOT NULL
);

INSERT INTO courses VALUES (1, 'Calculus I',      4, 'Mathematics');
INSERT INTO courses VALUES (2, 'Physics I',       4, 'Physics');
INSERT INTO courses VALUES (3, 'English Comp',    3, 'English');
INSERT INTO courses VALUES (4, 'Data Structures', 3, 'Computer Science');
INSERT INTO courses VALUES (5, 'Algorithms',      3, 'Computer Science');

CREATE TABLE enrollments (
    id INTEGER PRIMARY KEY,
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    grade REAL,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (course_id) REFERENCES courses(id)
);

INSERT INTO enrollments VALUES (1,  1, 1, 3.7);
INSERT INTO enrollments VALUES (2,  1, 2, 3.5);
INSERT INTO enrollments VALUES (3,  1, 3, 3.9);
INSERT INTO enrollments VALUES (4,  2, 1, 2.8);
INSERT INTO enrollments VALUES (5,  2, 4, 3.2);
INSERT INTO enrollments VALUES (6,  3, 3, NULL);
INSERT INTO enrollments VALUES (7,  3, 1, NULL);
INSERT INTO enrollments VALUES (8,  4, 4, 3.9);
INSERT INTO enrollments VALUES (9,  4, 2, 3.6);
INSERT INTO enrollments VALUES (10, 4, 5, 3.8);
INSERT INTO enrollments VALUES (11, 5, 1, 3.0);
INSERT INTO enrollments VALUES (12, 5, 3, 3.4);
INSERT INTO enrollments VALUES (13, 6, 5, 2.5);
INSERT INTO enrollments VALUES (14, 6, 2, 2.9);
INSERT INTO enrollments VALUES (15, 6, 1, 2.7);

CREATE TABLE contacts (
    id INTEGER PRIMARY KEY,
    student_id INTEGER NOT NULL UNIQUE,
    phone TEXT,
    address TEXT,
    emergency_contact TEXT,
    FOREIGN KEY (student_id) REFERENCES students(id)
);

INSERT INTO contacts VALUES (1, 1, '555-1001', '100 Elm St, Boston',     'Mary Wang 555-1002');
INSERT INTO contacts VALUES (2, 2, '555-2001', '200 Oak Ave, Cambridge', 'Raj Patel 555-2002');
INSERT INTO contacts VALUES (3, 3, '555-3001', '300 Pine Rd, Somerville','Ana Lopez 555-3002');
INSERT INTO contacts VALUES (4, 4, '555-4001', '400 Maple Dr, Brookline','Jun Kim 555-4002');
INSERT INTO contacts VALUES (5, 5, '555-5001', '500 Cedar Ln, Newton',   'Yuki Tanaka 555-5002');
INSERT INTO contacts VALUES (6, 6, '555-6001', '600 Birch Ct, Medford',  'Gina Russo 555-6002');

CREATE TABLE course_stats (
    id INTEGER PRIMARY KEY,
    course_id INTEGER NOT NULL UNIQUE,
    enrollment_count INTEGER NOT NULL,
    avg_grade REAL,
    FOREIGN KEY (course_id) REFERENCES courses(id)
);

INSERT INTO course_stats VALUES (1, 1, 5, 3.04);
INSERT INTO course_stats VALUES (2, 2, 3, 3.33);
INSERT INTO course_stats VALUES (3, 3, 3, 3.65);
INSERT INTO course_stats VALUES (4, 4, 2, 3.55);
INSERT INTO course_stats VALUES (5, 5, 2, 3.15);
"""
