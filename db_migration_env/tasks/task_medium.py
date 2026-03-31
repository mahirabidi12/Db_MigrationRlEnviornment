"""Task 2 (Medium): Legacy University LMS Acquisition — Full Schema Migration.

A university ran a custom LMS with 15 tables using legacy_ prefixed names,
abbreviated column names, and email-based cross-references. EduCloud acquired
them and needs a full migration to their standard schema with proper integer
FK IDs, normalized tables, and new derived/lookup tables.

ZERO table name overlap between initial and target schemas.

Initial: 15 legacy_ tables, ~161 rows total, email-based references, abbreviated cols
Target:  21 EduCloud standard tables, proper integer FKs, NOT NULL/UNIQUE/DEFAULT
         constraints, 6 brand-new tables (student_addresses, course_stats, semesters,
         majors, student_activities, faculty_departments, grade_history)

Skills tested:
  - Full table rename + column rename (legacy_ prefix removal, abbreviation expansion)
  - Replacing email-based references with integer FK IDs across many tables
  - Splitting tables (legacy_students -> students + student_addresses)
  - Creating computed aggregate tables (course_stats from enrollments)
  - Creating lookup tables (semesters, majors) and back-filling FKs
  - Adding NOT NULL, UNIQUE, DEFAULT constraints throughout
  - Multi-table JOINs to resolve email -> id mappings
  - SQLite ALTER TABLE recreate pattern (no DROP COLUMN in SQLite)
  - Data preservation across complex restructuring
  - Handling legacy grade_changes -> grade_history with enrollment_id resolution

Expected steps: 50-100
"""

TASK_ID = "medium_lms_acquisition"
TASK_DESCRIPTION = (
    "Migrate the legacy university LMS database to EduCloud standard schema: "
    "(1) Rename ALL 15 legacy_ tables to EduCloud standard names with expanded column names. "
    "(2) Replace ALL email-based references with proper integer FK columns "
    "by JOINing on legacy_students/legacy_profs tables. "
    "(3) Split legacy_students into 'students' + 'student_addresses'. "
    "(4) Create 'semesters' lookup table and replace semester/year text pairs with semester_id FK. "
    "(5) Create 'majors' lookup table and replace s_major text with major_id FK. "
    "(6) Create 'course_stats' aggregate table from enrollment data. "
    "(7) Create 'student_activities' table with one migration entry per student. "
    "(8) Create 'faculty_departments' junction table from faculty department assignments. "
    "(9) Create 'grade_history' table from legacy_grade_changes with enrollment_id resolution. "
    "(10) Add NOT NULL, UNIQUE, and DEFAULT constraints on all appropriate columns. "
    "Preserve all data with referential integrity."
)
DIFFICULTY = "medium"
TIMEOUT_SECONDS = 1800  # 30 minutes

INITIAL_SQL = """
CREATE TABLE legacy_students (
    sid INTEGER PRIMARY KEY,
    s_fname TEXT,
    s_lname TEXT,
    s_email TEXT,
    s_phone TEXT,
    s_dob TEXT,
    s_enrolled TEXT,
    s_major TEXT,
    s_advisor TEXT,
    s_gpa REAL,
    s_status TEXT,
    s_addr TEXT,
    s_city TEXT,
    s_state TEXT,
    s_zip TEXT
);
INSERT INTO legacy_students VALUES (1, 'Alice', 'Wang', 'alice.w@olduni.edu', '555-1001', '2002-03-15', '2022-08-20', 'Computer Science', 'dr.smith@olduni.edu', 3.7, 'active', '100 Elm St', 'Boston', 'MA', '02101');
INSERT INTO legacy_students VALUES (2, 'Bob', 'Patel', 'bob.p@olduni.edu', '555-1002', '2001-07-22', '2021-08-18', 'Mathematics', 'dr.jones@olduni.edu', 3.0, 'active', '200 Oak Ave', 'Cambridge', 'MA', '02139');
INSERT INTO legacy_students VALUES (3, 'Carol', 'Lopez', 'carol.l@olduni.edu', '555-1003', '2003-11-05', '2023-08-21', 'English', 'dr.williams@olduni.edu', 3.4, 'active', '300 Pine Rd', 'Somerville', 'MA', '02143');
INSERT INTO legacy_students VALUES (4, 'Dave', 'Kim', 'dave.k@olduni.edu', '555-1004', '2000-01-30', '2020-08-17', 'Computer Science', 'dr.smith@olduni.edu', 3.8, 'active', '400 Maple Dr', 'Brookline', 'MA', '02445');
INSERT INTO legacy_students VALUES (5, 'Eve', 'Tanaka', 'eve.t@olduni.edu', '555-1005', '2002-09-12', '2022-08-20', 'Physics', 'dr.garcia@olduni.edu', 3.2, 'active', '500 Cedar Ln', 'Newton', 'MA', '02458');
INSERT INTO legacy_students VALUES (6, 'Frank', 'Russo', 'frank.r@olduni.edu', '555-1006', '2001-04-18', '2021-08-18', 'Mathematics', 'dr.jones@olduni.edu', 2.7, 'probation', '600 Birch Ct', 'Medford', 'MA', '02155');
INSERT INTO legacy_students VALUES (7, 'Grace', 'Huang', 'grace.h@olduni.edu', '555-1007', '2003-06-25', '2023-08-21', 'Physics', 'dr.garcia@olduni.edu', 3.5, 'active', '700 Walnut St', 'Arlington', 'MA', '02474');
INSERT INTO legacy_students VALUES (8, 'Henry', 'Morgan', 'henry.m@olduni.edu', '555-1008', '2002-12-01', '2022-08-20', 'English', 'dr.williams@olduni.edu', 2.9, 'active', '800 Spruce Ave', 'Belmont', 'MA', '02478');

CREATE TABLE legacy_profs (
    pid INTEGER PRIMARY KEY,
    p_fname TEXT,
    p_lname TEXT,
    p_email TEXT,
    p_phone TEXT,
    p_hired TEXT,
    p_dept TEXT,
    p_title TEXT,
    p_room TEXT,
    p_building TEXT,
    p_salary REAL,
    p_tenure TEXT
);
INSERT INTO legacy_profs VALUES (1, 'John', 'Smith', 'dr.smith@olduni.edu', '555-2001', '2010-08-15', 'Computer Science', 'Professor', '301', 'Science Hall', 120000.00, 'tenured');
INSERT INTO legacy_profs VALUES (2, 'Margaret', 'Jones', 'dr.jones@olduni.edu', '555-2002', '2012-01-10', 'Mathematics', 'Associate Professor', '205', 'Math Building', 105000.00, 'tenured');
INSERT INTO legacy_profs VALUES (3, 'Robert', 'Williams', 'dr.williams@olduni.edu', '555-2003', '2015-08-20', 'English', 'Assistant Professor', '110', 'Humanities Hall', 85000.00, 'tenure-track');
INSERT INTO legacy_profs VALUES (4, 'Elena', 'Garcia', 'dr.garcia@olduni.edu', '555-2004', '2008-01-05', 'Physics', 'Professor', '402', 'Science Hall', 125000.00, 'tenured');
INSERT INTO legacy_profs VALUES (5, 'Wei', 'Chen', 'dr.chen@olduni.edu', '555-2005', '2018-08-15', 'Computer Science', 'Lecturer', '303', 'Science Hall', 72000.00, 'non-tenure');
INSERT INTO legacy_profs VALUES (6, 'James', 'Taylor', 'dr.taylor@olduni.edu', '555-2006', '2020-01-10', 'Mathematics', 'Lecturer', '207', 'Math Building', 68000.00, 'non-tenure');

CREATE TABLE legacy_depts (
    did INTEGER PRIMARY KEY,
    d_name TEXT,
    d_code TEXT,
    d_building TEXT,
    d_floor INTEGER,
    d_phone TEXT,
    d_head_email TEXT,
    d_budget REAL,
    d_founded INTEGER,
    d_desc TEXT
);
INSERT INTO legacy_depts VALUES (1, 'Computer Science', 'CS', 'Science Hall', 3, '555-3001', 'dr.smith@olduni.edu', 2500000.00, 1985, 'Department of Computer Science and Engineering');
INSERT INTO legacy_depts VALUES (2, 'Mathematics', 'MATH', 'Math Building', 2, '555-3002', 'dr.jones@olduni.edu', 1800000.00, 1920, 'Department of Mathematics and Applied Mathematics');
INSERT INTO legacy_depts VALUES (3, 'English', 'ENG', 'Humanities Hall', 1, '555-3003', 'dr.williams@olduni.edu', 1200000.00, 1900, 'Department of English Language and Literature');
INSERT INTO legacy_depts VALUES (4, 'Physics', 'PHYS', 'Science Hall', 4, '555-3004', 'dr.garcia@olduni.edu', 2200000.00, 1935, 'Department of Physics and Astronomy');

CREATE TABLE legacy_classes (
    cid INTEGER PRIMARY KEY,
    c_code TEXT,
    c_name TEXT,
    c_desc TEXT,
    c_credits INTEGER,
    c_dept_name TEXT,
    c_prof_email TEXT,
    c_capacity INTEGER,
    c_enrolled INTEGER,
    c_semester TEXT,
    c_year INTEGER,
    c_room TEXT
);
INSERT INTO legacy_classes VALUES (1, 'CS101', 'Intro to Programming', 'Learn basic programming concepts', 4, 'Computer Science', 'dr.smith@olduni.edu', 40, 30, 'Fall', 2025, 'SH-101');
INSERT INTO legacy_classes VALUES (2, 'CS201', 'Data Structures', 'Advanced data structures and algorithms', 4, 'Computer Science', 'dr.smith@olduni.edu', 35, 25, 'Fall', 2025, 'SH-102');
INSERT INTO legacy_classes VALUES (3, 'MATH101', 'Calculus I', 'Introduction to differential calculus', 4, 'Mathematics', 'dr.jones@olduni.edu', 45, 35, 'Fall', 2025, 'MB-201');
INSERT INTO legacy_classes VALUES (4, 'MATH201', 'Linear Algebra', 'Vectors, matrices, and linear transformations', 3, 'Mathematics', 'dr.jones@olduni.edu', 40, 28, 'Fall', 2025, 'MB-202');
INSERT INTO legacy_classes VALUES (5, 'ENG101', 'English Composition', 'Academic writing fundamentals', 3, 'English', 'dr.williams@olduni.edu', 30, 25, 'Fall', 2025, 'HH-101');
INSERT INTO legacy_classes VALUES (6, 'ENG201', 'American Literature', 'Survey of American literary works', 3, 'English', 'dr.williams@olduni.edu', 30, 20, 'Fall', 2025, 'HH-102');
INSERT INTO legacy_classes VALUES (7, 'PHYS101', 'Physics I', 'Mechanics and thermodynamics', 4, 'Physics', 'dr.garcia@olduni.edu', 40, 32, 'Fall', 2025, 'SH-201');
INSERT INTO legacy_classes VALUES (8, 'PHYS201', 'Physics II', 'Electricity and magnetism', 4, 'Physics', 'dr.garcia@olduni.edu', 35, 22, 'Fall', 2025, 'SH-202');
INSERT INTO legacy_classes VALUES (9, 'CS301', 'Database Systems', 'Relational databases and SQL', 3, 'Computer Science', 'dr.chen@olduni.edu', 30, 20, 'Fall', 2025, 'SH-103');
INSERT INTO legacy_classes VALUES (10, 'MATH301', 'Probability and Stats', 'Intro to probability and statistics', 3, 'Mathematics', 'dr.taylor@olduni.edu', 35, 30, 'Fall', 2025, 'MB-301');

CREATE TABLE legacy_registrations (
    rid INTEGER PRIMARY KEY,
    r_student_email TEXT,
    r_class_code TEXT,
    r_grade TEXT,
    r_gpa_pts REAL,
    r_reg_date TEXT,
    r_status TEXT,
    r_midterm REAL,
    r_final REAL,
    r_attend_pct REAL,
    r_notes TEXT
);
INSERT INTO legacy_registrations VALUES (1, 'alice.w@olduni.edu', 'CS101', 'A', 4.0, '2025-08-25', 'completed', 92.0, 95.0, 96.0, 'Excellent work');
INSERT INTO legacy_registrations VALUES (2, 'alice.w@olduni.edu', 'MATH101', 'A-', 3.7, '2025-08-25', 'completed', 88.0, 91.0, 94.0, NULL);
INSERT INTO legacy_registrations VALUES (3, 'alice.w@olduni.edu', 'ENG101', 'A', 4.0, '2025-08-25', 'completed', 95.0, 93.0, 98.0, 'Strong writer');
INSERT INTO legacy_registrations VALUES (4, 'bob.p@olduni.edu', 'MATH101', 'B', 3.0, '2025-08-25', 'completed', 78.0, 82.0, 88.0, NULL);
INSERT INTO legacy_registrations VALUES (5, 'bob.p@olduni.edu', 'MATH201', 'B+', 3.3, '2025-08-25', 'completed', 80.0, 85.0, 90.0, NULL);
INSERT INTO legacy_registrations VALUES (6, 'bob.p@olduni.edu', 'CS201', 'B-', 2.7, '2025-08-25', 'completed', 75.0, 78.0, 85.0, 'Needs improvement in recursion');
INSERT INTO legacy_registrations VALUES (7, 'carol.l@olduni.edu', 'ENG101', 'A-', 3.7, '2025-08-25', 'completed', 90.0, 88.0, 95.0, NULL);
INSERT INTO legacy_registrations VALUES (8, 'carol.l@olduni.edu', 'ENG201', NULL, NULL, '2025-08-25', 'enrolled', NULL, NULL, 80.0, 'In progress');
INSERT INTO legacy_registrations VALUES (9, 'carol.l@olduni.edu', 'PHYS101', 'B+', 3.3, '2025-08-25', 'completed', 82.0, 86.0, 91.0, NULL);
INSERT INTO legacy_registrations VALUES (10, 'dave.k@olduni.edu', 'CS101', 'A', 4.0, '2025-08-25', 'completed', 96.0, 98.0, 99.0, 'Top student');
INSERT INTO legacy_registrations VALUES (11, 'dave.k@olduni.edu', 'CS201', 'A', 4.0, '2025-08-25', 'completed', 94.0, 96.0, 97.0, NULL);
INSERT INTO legacy_registrations VALUES (12, 'dave.k@olduni.edu', 'CS301', 'A-', 3.7, '2025-08-25', 'completed', 90.0, 92.0, 95.0, NULL);
INSERT INTO legacy_registrations VALUES (13, 'eve.t@olduni.edu', 'PHYS101', 'B+', 3.3, '2025-08-25', 'completed', 84.0, 87.0, 92.0, NULL);
INSERT INTO legacy_registrations VALUES (14, 'eve.t@olduni.edu', 'PHYS201', 'B', 3.0, '2025-08-25', 'completed', 79.0, 81.0, 88.0, NULL);
INSERT INTO legacy_registrations VALUES (15, 'eve.t@olduni.edu', 'MATH101', 'B+', 3.3, '2025-08-25', 'completed', 83.0, 86.0, 90.0, NULL);
INSERT INTO legacy_registrations VALUES (16, 'frank.r@olduni.edu', 'MATH101', 'C+', 2.3, '2025-08-25', 'completed', 68.0, 72.0, 75.0, 'Attendance issues');
INSERT INTO legacy_registrations VALUES (17, 'frank.r@olduni.edu', 'MATH201', 'C', 2.0, '2025-08-25', 'completed', 65.0, 70.0, 72.0, NULL);
INSERT INTO legacy_registrations VALUES (18, 'grace.h@olduni.edu', 'PHYS101', NULL, NULL, '2025-08-25', 'enrolled', NULL, NULL, 85.0, 'In progress');
INSERT INTO legacy_registrations VALUES (19, 'grace.h@olduni.edu', 'MATH101', 'B', 3.0, '2025-08-25', 'completed', 80.0, 83.0, 89.0, NULL);
INSERT INTO legacy_registrations VALUES (20, 'henry.m@olduni.edu', 'ENG101', 'B-', 2.7, '2025-08-25', 'completed', 74.0, 77.0, 82.0, NULL);

CREATE TABLE legacy_homework (
    hid INTEGER PRIMARY KEY,
    h_class_code TEXT,
    h_title TEXT,
    h_desc TEXT,
    h_due TEXT,
    h_max_pts REAL,
    h_weight REAL,
    h_type TEXT,
    h_published INTEGER,
    h_creator_email TEXT,
    h_created TEXT
);
INSERT INTO legacy_homework VALUES (1, 'CS101', 'Hello World Program', 'Write your first program in Python', '2025-09-15', 100.0, 5.0, 'homework', 1, 'dr.smith@olduni.edu', '2025-08-25');
INSERT INTO legacy_homework VALUES (2, 'CS101', 'Midterm Exam', 'Covers chapters 1-6', '2025-10-15', 200.0, 25.0, 'exam', 1, 'dr.smith@olduni.edu', '2025-08-25');
INSERT INTO legacy_homework VALUES (3, 'CS201', 'Linked List Implementation', 'Implement singly and doubly linked lists', '2025-09-20', 100.0, 10.0, 'homework', 1, 'dr.smith@olduni.edu', '2025-08-26');
INSERT INTO legacy_homework VALUES (4, 'MATH101', 'Problem Set 1', 'Limits and continuity exercises', '2025-09-10', 50.0, 5.0, 'homework', 1, 'dr.jones@olduni.edu', '2025-08-25');
INSERT INTO legacy_homework VALUES (5, 'MATH101', 'Midterm Exam', 'Chapters 1-4', '2025-10-12', 100.0, 30.0, 'exam', 1, 'dr.jones@olduni.edu', '2025-08-25');
INSERT INTO legacy_homework VALUES (6, 'ENG101', 'Personal Essay', 'Write a 5-page personal narrative', '2025-09-18', 100.0, 15.0, 'essay', 1, 'dr.williams@olduni.edu', '2025-08-25');
INSERT INTO legacy_homework VALUES (7, 'ENG101', 'Research Paper Draft', 'First draft of research paper', '2025-10-20', 100.0, 10.0, 'essay', 1, 'dr.williams@olduni.edu', '2025-08-26');
INSERT INTO legacy_homework VALUES (8, 'PHYS101', 'Lab Report 1', 'Kinematics experiment report', '2025-09-12', 50.0, 5.0, 'lab', 1, 'dr.garcia@olduni.edu', '2025-08-25');
INSERT INTO legacy_homework VALUES (9, 'PHYS101', 'Midterm Exam', 'Mechanics chapters 1-5', '2025-10-14', 150.0, 25.0, 'exam', 1, 'dr.garcia@olduni.edu', '2025-08-25');
INSERT INTO legacy_homework VALUES (10, 'CS301', 'SQL Exercises', 'Practice SELECT, JOIN, and subqueries', '2025-09-22', 80.0, 8.0, 'homework', 1, 'dr.chen@olduni.edu', '2025-08-27');
INSERT INTO legacy_homework VALUES (11, 'MATH201', 'Matrix Operations', 'Solve systems of linear equations', '2025-09-16', 60.0, 8.0, 'homework', 1, 'dr.jones@olduni.edu', '2025-08-26');
INSERT INTO legacy_homework VALUES (12, 'PHYS201', 'Coulombs Law Problems', 'Electric force calculations', '2025-09-19', 70.0, 7.0, 'homework', 1, 'dr.garcia@olduni.edu', '2025-08-26');

CREATE TABLE legacy_turnins (
    tid INTEGER PRIMARY KEY,
    t_hw_id INTEGER,
    t_student_email TEXT,
    t_submitted TEXT,
    t_file TEXT,
    t_score REAL,
    t_feedback TEXT,
    t_late INTEGER,
    t_grader_email TEXT,
    t_graded_at TEXT,
    t_status TEXT
);
INSERT INTO legacy_turnins VALUES (1, 1, 'alice.w@olduni.edu', '2025-09-14 23:30:00', '/files/alice_hw1.py', 95.0, 'Great job!', 0, 'dr.smith@olduni.edu', '2025-09-16', 'graded');
INSERT INTO legacy_turnins VALUES (2, 1, 'dave.k@olduni.edu', '2025-09-14 20:00:00', '/files/dave_hw1.py', 100.0, 'Perfect', 0, 'dr.smith@olduni.edu', '2025-09-16', 'graded');
INSERT INTO legacy_turnins VALUES (3, 2, 'alice.w@olduni.edu', '2025-10-15 10:00:00', '/files/alice_midterm.pdf', 92.0, NULL, 0, 'dr.smith@olduni.edu', '2025-10-18', 'graded');
INSERT INTO legacy_turnins VALUES (4, 2, 'dave.k@olduni.edu', '2025-10-15 10:00:00', '/files/dave_midterm.pdf', 96.0, 'Excellent', 0, 'dr.smith@olduni.edu', '2025-10-18', 'graded');
INSERT INTO legacy_turnins VALUES (5, 3, 'bob.p@olduni.edu', '2025-09-21 08:00:00', '/files/bob_ll.zip', 72.0, 'Missing edge cases', 1, 'dr.smith@olduni.edu', '2025-09-23', 'graded');
INSERT INTO legacy_turnins VALUES (6, 3, 'dave.k@olduni.edu', '2025-09-19 18:00:00', '/files/dave_ll.zip', 98.0, 'Excellent implementation', 0, 'dr.smith@olduni.edu', '2025-09-23', 'graded');
INSERT INTO legacy_turnins VALUES (7, 4, 'alice.w@olduni.edu', '2025-09-09 22:00:00', '/files/alice_ps1.pdf', 45.0, NULL, 0, 'dr.jones@olduni.edu', '2025-09-12', 'graded');
INSERT INTO legacy_turnins VALUES (8, 4, 'bob.p@olduni.edu', '2025-09-10 01:00:00', '/files/bob_ps1.pdf', 38.0, 'Review limits section', 1, 'dr.jones@olduni.edu', '2025-09-12', 'graded');
INSERT INTO legacy_turnins VALUES (9, 4, 'eve.t@olduni.edu', '2025-09-09 20:00:00', '/files/eve_ps1.pdf', 42.0, NULL, 0, 'dr.jones@olduni.edu', '2025-09-12', 'graded');
INSERT INTO legacy_turnins VALUES (10, 6, 'alice.w@olduni.edu', '2025-09-17 15:00:00', '/files/alice_essay.docx', 93.0, 'Beautiful prose', 0, 'dr.williams@olduni.edu', '2025-09-20', 'graded');
INSERT INTO legacy_turnins VALUES (11, 6, 'carol.l@olduni.edu', '2025-09-18 09:00:00', '/files/carol_essay.docx', 90.0, 'Strong voice', 0, 'dr.williams@olduni.edu', '2025-09-20', 'graded');
INSERT INTO legacy_turnins VALUES (12, 6, 'henry.m@olduni.edu', '2025-09-19 11:00:00', '/files/henry_essay.docx', 74.0, 'Needs more detail', 1, 'dr.williams@olduni.edu', '2025-09-20', 'graded');
INSERT INTO legacy_turnins VALUES (13, 8, 'eve.t@olduni.edu', '2025-09-12 14:00:00', '/files/eve_lab1.pdf', 44.0, NULL, 0, 'dr.garcia@olduni.edu', '2025-09-15', 'graded');
INSERT INTO legacy_turnins VALUES (14, 8, 'carol.l@olduni.edu', '2025-09-12 16:00:00', '/files/carol_lab1.pdf', 46.0, 'Good analysis', 0, 'dr.garcia@olduni.edu', '2025-09-15', 'graded');
INSERT INTO legacy_turnins VALUES (15, 10, 'dave.k@olduni.edu', '2025-09-21 22:00:00', '/files/dave_sql.sql', 78.0, 'Good joins', 0, 'dr.chen@olduni.edu', '2025-09-24', 'graded');

CREATE TABLE legacy_notices (
    nid INTEGER PRIMARY KEY,
    n_class_code TEXT,
    n_author_email TEXT,
    n_title TEXT,
    n_body TEXT,
    n_priority TEXT,
    n_pinned INTEGER,
    n_created TEXT,
    n_updated TEXT,
    n_expires TEXT
);
INSERT INTO legacy_notices VALUES (1, 'CS101', 'dr.smith@olduni.edu', 'Welcome to CS101', 'Please review the syllabus before first class.', 'high', 1, '2025-08-20', '2025-08-20', '2025-09-01');
INSERT INTO legacy_notices VALUES (2, 'CS101', 'dr.smith@olduni.edu', 'Office Hours Change', 'Office hours moved to Thursdays 2-4pm.', 'normal', 0, '2025-09-05', '2025-09-05', '2025-12-15');
INSERT INTO legacy_notices VALUES (3, 'MATH101', 'dr.jones@olduni.edu', 'Textbook Required', 'Please purchase Stewart Calculus 9th edition.', 'high', 1, '2025-08-21', '2025-08-21', '2025-09-10');
INSERT INTO legacy_notices VALUES (4, 'ENG101', 'dr.williams@olduni.edu', 'Essay Guidelines', 'All essays must follow MLA format.', 'normal', 1, '2025-08-22', '2025-08-22', '2025-12-15');
INSERT INTO legacy_notices VALUES (5, 'PHYS101', 'dr.garcia@olduni.edu', 'Lab Safety Training', 'Mandatory safety training on Sept 5.', 'high', 0, '2025-08-28', '2025-08-28', '2025-09-05');
INSERT INTO legacy_notices VALUES (6, 'CS201', 'dr.smith@olduni.edu', 'Prerequisites Reminder', 'CS101 is a prerequisite for this course.', 'normal', 0, '2025-08-20', '2025-08-20', '2025-09-01');
INSERT INTO legacy_notices VALUES (7, 'CS301', 'dr.chen@olduni.edu', 'Software Installation', 'Install PostgreSQL and SQLite before Week 2.', 'high', 1, '2025-08-25', '2025-08-25', '2025-09-08');
INSERT INTO legacy_notices VALUES (8, 'MATH201', 'dr.jones@olduni.edu', 'Study Group Formation', 'Form study groups of 3-4 students.', 'normal', 0, '2025-09-01', '2025-09-01', '2025-12-15');

CREATE TABLE legacy_rollcall (
    rcid INTEGER PRIMARY KEY,
    rc_class_code TEXT,
    rc_student_email TEXT,
    rc_date TEXT,
    rc_status TEXT,
    rc_checkin TEXT,
    rc_checkout TEXT,
    rc_duration INTEGER,
    rc_notes TEXT,
    rc_by_email TEXT
);
INSERT INTO legacy_rollcall VALUES (1, 'CS101', 'alice.w@olduni.edu', '2025-09-02', 'present', '09:00', '10:15', 75, NULL, 'dr.smith@olduni.edu');
INSERT INTO legacy_rollcall VALUES (2, 'CS101', 'dave.k@olduni.edu', '2025-09-02', 'present', '08:58', '10:15', 77, NULL, 'dr.smith@olduni.edu');
INSERT INTO legacy_rollcall VALUES (3, 'CS101', 'alice.w@olduni.edu', '2025-09-04', 'present', '09:02', '10:15', 73, NULL, 'dr.smith@olduni.edu');
INSERT INTO legacy_rollcall VALUES (4, 'CS101', 'dave.k@olduni.edu', '2025-09-04', 'late', '09:20', '10:15', 55, 'Arrived 20 min late', 'dr.smith@olduni.edu');
INSERT INTO legacy_rollcall VALUES (5, 'MATH101', 'alice.w@olduni.edu', '2025-09-03', 'present', '10:00', '11:15', 75, NULL, 'dr.jones@olduni.edu');
INSERT INTO legacy_rollcall VALUES (6, 'MATH101', 'bob.p@olduni.edu', '2025-09-03', 'present', '10:05', '11:15', 70, NULL, 'dr.jones@olduni.edu');
INSERT INTO legacy_rollcall VALUES (7, 'MATH101', 'eve.t@olduni.edu', '2025-09-03', 'present', '10:00', '11:15', 75, NULL, 'dr.jones@olduni.edu');
INSERT INTO legacy_rollcall VALUES (8, 'MATH101', 'frank.r@olduni.edu', '2025-09-03', 'absent', NULL, NULL, 0, 'No show', 'dr.jones@olduni.edu');
INSERT INTO legacy_rollcall VALUES (9, 'ENG101', 'alice.w@olduni.edu', '2025-09-02', 'present', '13:00', '14:15', 75, NULL, 'dr.williams@olduni.edu');
INSERT INTO legacy_rollcall VALUES (10, 'ENG101', 'carol.l@olduni.edu', '2025-09-02', 'present', '13:00', '14:15', 75, NULL, 'dr.williams@olduni.edu');
INSERT INTO legacy_rollcall VALUES (11, 'ENG101', 'henry.m@olduni.edu', '2025-09-02', 'late', '13:15', '14:15', 60, 'Arrived late', 'dr.williams@olduni.edu');
INSERT INTO legacy_rollcall VALUES (12, 'PHYS101', 'eve.t@olduni.edu', '2025-09-03', 'present', '14:00', '15:30', 90, NULL, 'dr.garcia@olduni.edu');
INSERT INTO legacy_rollcall VALUES (13, 'PHYS101', 'carol.l@olduni.edu', '2025-09-03', 'present', '14:00', '15:30', 90, NULL, 'dr.garcia@olduni.edu');
INSERT INTO legacy_rollcall VALUES (14, 'PHYS101', 'grace.h@olduni.edu', '2025-09-03', 'present', '14:02', '15:30', 88, NULL, 'dr.garcia@olduni.edu');
INSERT INTO legacy_rollcall VALUES (15, 'CS201', 'bob.p@olduni.edu', '2025-09-02', 'present', '11:00', '12:15', 75, NULL, 'dr.smith@olduni.edu');
INSERT INTO legacy_rollcall VALUES (16, 'CS201', 'dave.k@olduni.edu', '2025-09-02', 'present', '11:00', '12:15', 75, NULL, 'dr.smith@olduni.edu');
INSERT INTO legacy_rollcall VALUES (17, 'CS301', 'dave.k@olduni.edu', '2025-09-04', 'present', '15:00', '16:15', 75, NULL, 'dr.chen@olduni.edu');
INSERT INTO legacy_rollcall VALUES (18, 'MATH201', 'bob.p@olduni.edu', '2025-09-04', 'present', '10:00', '11:15', 75, NULL, 'dr.jones@olduni.edu');

CREATE TABLE legacy_grade_changes (
    gcid INTEGER PRIMARY KEY,
    gc_student_email TEXT,
    gc_class_code TEXT,
    gc_old TEXT,
    gc_new TEXT,
    gc_by_email TEXT,
    gc_reason TEXT,
    gc_at TEXT,
    gc_semester TEXT,
    gc_year INTEGER,
    gc_final INTEGER
);
INSERT INTO legacy_grade_changes VALUES (1, 'alice.w@olduni.edu', 'CS101', 'A-', 'A', 'dr.smith@olduni.edu', 'Adjusted after extra credit', '2025-12-10', 'Fall', 2025, 1);
INSERT INTO legacy_grade_changes VALUES (2, 'bob.p@olduni.edu', 'MATH101', 'B-', 'B', 'dr.jones@olduni.edu', 'Regrade request approved', '2025-12-08', 'Fall', 2025, 1);
INSERT INTO legacy_grade_changes VALUES (3, 'dave.k@olduni.edu', 'CS201', 'A-', 'A', 'dr.smith@olduni.edu', 'Curve applied', '2025-12-12', 'Fall', 2025, 1);
INSERT INTO legacy_grade_changes VALUES (4, 'eve.t@olduni.edu', 'PHYS101', 'B', 'B+', 'dr.garcia@olduni.edu', 'Lab grade correction', '2025-12-09', 'Fall', 2025, 1);
INSERT INTO legacy_grade_changes VALUES (5, 'frank.r@olduni.edu', 'MATH101', 'C', 'C+', 'dr.jones@olduni.edu', 'Homework resubmission', '2025-12-11', 'Fall', 2025, 1);
INSERT INTO legacy_grade_changes VALUES (6, 'carol.l@olduni.edu', 'ENG101', 'B+', 'A-', 'dr.williams@olduni.edu', 'Final essay regraded', '2025-12-13', 'Fall', 2025, 1);
INSERT INTO legacy_grade_changes VALUES (7, 'henry.m@olduni.edu', 'ENG101', 'C+', 'B-', 'dr.williams@olduni.edu', 'Participation grade updated', '2025-12-14', 'Fall', 2025, 1);
INSERT INTO legacy_grade_changes VALUES (8, 'alice.w@olduni.edu', 'MATH101', 'B+', 'A-', 'dr.jones@olduni.edu', 'Final exam curve', '2025-12-10', 'Fall', 2025, 1);
INSERT INTO legacy_grade_changes VALUES (9, 'grace.h@olduni.edu', 'MATH101', 'B-', 'B', 'dr.jones@olduni.edu', 'Attendance bonus', '2025-12-15', 'Fall', 2025, 1);
INSERT INTO legacy_grade_changes VALUES (10, 'bob.p@olduni.edu', 'CS201', 'C+', 'B-', 'dr.smith@olduni.edu', 'Project resubmission', '2025-12-14', 'Fall', 2025, 1);

CREATE TABLE legacy_materials (
    mid INTEGER PRIMARY KEY,
    m_class_code TEXT,
    m_title TEXT,
    m_file TEXT,
    m_type TEXT,
    m_size INTEGER,
    m_uploader_email TEXT,
    m_desc TEXT,
    m_downloads INTEGER,
    m_visible INTEGER,
    m_uploaded TEXT
);
INSERT INTO legacy_materials VALUES (1, 'CS101', 'Syllabus', '/materials/cs101_syllabus.pdf', 'pdf', 245000, 'dr.smith@olduni.edu', 'Course syllabus and schedule', 45, 1, '2025-08-15');
INSERT INTO legacy_materials VALUES (2, 'CS101', 'Lecture 1 Slides', '/materials/cs101_lec1.pptx', 'pptx', 1200000, 'dr.smith@olduni.edu', 'Introduction to programming', 38, 1, '2025-09-01');
INSERT INTO legacy_materials VALUES (3, 'MATH101', 'Formula Sheet', '/materials/math101_formulas.pdf', 'pdf', 120000, 'dr.jones@olduni.edu', 'Key formulas for calculus', 52, 1, '2025-08-20');
INSERT INTO legacy_materials VALUES (4, 'MATH101', 'Practice Problems', '/materials/math101_practice.pdf', 'pdf', 350000, 'dr.jones@olduni.edu', 'Extra practice for midterm', 30, 1, '2025-10-01');
INSERT INTO legacy_materials VALUES (5, 'ENG101', 'Style Guide', '/materials/eng101_style.pdf', 'pdf', 180000, 'dr.williams@olduni.edu', 'MLA formatting guide', 40, 1, '2025-08-18');
INSERT INTO legacy_materials VALUES (6, 'ENG101', 'Essay Rubric', '/materials/eng101_rubric.pdf', 'pdf', 95000, 'dr.williams@olduni.edu', 'Grading criteria for essays', 35, 1, '2025-08-18');
INSERT INTO legacy_materials VALUES (7, 'PHYS101', 'Lab Manual', '/materials/phys101_lab.pdf', 'pdf', 2500000, 'dr.garcia@olduni.edu', 'Complete lab manual', 48, 1, '2025-08-16');
INSERT INTO legacy_materials VALUES (8, 'CS201', 'Big-O Cheatsheet', '/materials/cs201_bigo.pdf', 'pdf', 85000, 'dr.smith@olduni.edu', 'Time complexity reference', 28, 1, '2025-09-05');
INSERT INTO legacy_materials VALUES (9, 'CS301', 'SQL Reference', '/materials/cs301_sql.pdf', 'pdf', 310000, 'dr.chen@olduni.edu', 'SQL syntax quick reference', 22, 1, '2025-08-28');
INSERT INTO legacy_materials VALUES (10, 'PHYS201', 'Maxwells Equations', '/materials/phys201_maxwell.pdf', 'pdf', 200000, 'dr.garcia@olduni.edu', 'Summary of electromagnetic theory', 18, 1, '2025-08-22');

CREATE TABLE legacy_forums (
    fid INTEGER PRIMARY KEY,
    f_class_code TEXT,
    f_author_email TEXT,
    f_title TEXT,
    f_body TEXT,
    f_parent INTEGER,
    f_likes INTEGER,
    f_pinned INTEGER,
    f_anon INTEGER,
    f_created TEXT,
    f_updated TEXT
);
INSERT INTO legacy_forums VALUES (1, 'CS101', 'alice.w@olduni.edu', 'Help with HW1', 'I am stuck on the loop exercise. Any tips?', NULL, 3, 0, 0, '2025-09-10', '2025-09-10');
INSERT INTO legacy_forums VALUES (2, 'CS101', 'dave.k@olduni.edu', 'Re: Help with HW1', 'Try using a while loop instead of for.', 1, 5, 0, 0, '2025-09-10', '2025-09-10');
INSERT INTO legacy_forums VALUES (3, 'CS101', 'dr.smith@olduni.edu', 'Re: Help with HW1', 'Good suggestion Dave. Also review chapter 3.', 1, 2, 0, 0, '2025-09-11', '2025-09-11');
INSERT INTO legacy_forums VALUES (4, 'MATH101', 'bob.p@olduni.edu', 'Limit Problem Clarification', 'Can someone explain L Hopitals rule with an example?', NULL, 4, 0, 0, '2025-09-15', '2025-09-15');
INSERT INTO legacy_forums VALUES (5, 'MATH101', 'dr.jones@olduni.edu', 'Re: Limit Problem', 'See the attached example from lecture 5.', 4, 6, 0, 0, '2025-09-15', '2025-09-15');
INSERT INTO legacy_forums VALUES (6, 'ENG101', 'carol.l@olduni.edu', 'MLA Citation Question', 'How do I cite an online article in MLA?', NULL, 2, 0, 0, '2025-09-12', '2025-09-12');
INSERT INTO legacy_forums VALUES (7, 'ENG101', 'dr.williams@olduni.edu', 'Re: MLA Citation', 'Use the format: Author. Title. Website, Date, URL.', 6, 4, 0, 0, '2025-09-12', '2025-09-12');
INSERT INTO legacy_forums VALUES (8, 'PHYS101', 'eve.t@olduni.edu', 'Lab Partner Needed', 'Looking for a lab partner for Thursday sessions.', NULL, 1, 0, 0, '2025-09-08', '2025-09-08');
INSERT INTO legacy_forums VALUES (9, 'PHYS101', 'grace.h@olduni.edu', 'Re: Lab Partner', 'I am available! Send me an email.', 8, 1, 0, 0, '2025-09-08', '2025-09-08');
INSERT INTO legacy_forums VALUES (10, 'CS301', 'dave.k@olduni.edu', 'JOIN vs Subquery', 'When should I prefer JOIN over subquery?', NULL, 7, 0, 0, '2025-09-20', '2025-09-20');

CREATE TABLE legacy_office_hrs (
    ohid INTEGER PRIMARY KEY,
    oh_prof_email TEXT,
    oh_day TEXT,
    oh_start TEXT,
    oh_end TEXT,
    oh_location TEXT,
    oh_virtual INTEGER,
    oh_url TEXT,
    oh_max INTEGER,
    oh_semester TEXT,
    oh_year INTEGER
);
INSERT INTO legacy_office_hrs VALUES (1, 'dr.smith@olduni.edu', 'Tuesday', '14:00', '16:00', 'SH-301', 0, NULL, 5, 'Fall', 2025);
INSERT INTO legacy_office_hrs VALUES (2, 'dr.smith@olduni.edu', 'Thursday', '14:00', '16:00', 'SH-301', 0, NULL, 5, 'Fall', 2025);
INSERT INTO legacy_office_hrs VALUES (3, 'dr.jones@olduni.edu', 'Monday', '10:00', '12:00', 'MB-205', 0, NULL, 4, 'Fall', 2025);
INSERT INTO legacy_office_hrs VALUES (4, 'dr.jones@olduni.edu', 'Wednesday', '10:00', '12:00', NULL, 1, 'https://zoom.us/jones123', 6, 'Fall', 2025);
INSERT INTO legacy_office_hrs VALUES (5, 'dr.williams@olduni.edu', 'Tuesday', '11:00', '12:30', 'HH-110', 0, NULL, 3, 'Fall', 2025);
INSERT INTO legacy_office_hrs VALUES (6, 'dr.garcia@olduni.edu', 'Friday', '13:00', '15:00', 'SH-402', 0, NULL, 4, 'Fall', 2025);
INSERT INTO legacy_office_hrs VALUES (7, 'dr.chen@olduni.edu', 'Wednesday', '15:00', '17:00', NULL, 1, 'https://zoom.us/chen456', 5, 'Fall', 2025);
INSERT INTO legacy_office_hrs VALUES (8, 'dr.taylor@olduni.edu', 'Thursday', '09:00', '11:00', 'MB-207', 0, NULL, 4, 'Fall', 2025);

CREATE TABLE legacy_clubs (
    clid INTEGER PRIMARY KEY,
    cl_name TEXT,
    cl_desc TEXT,
    cl_advisor_email TEXT,
    cl_president_email TEXT,
    cl_founded TEXT,
    cl_day TEXT,
    cl_room TEXT,
    cl_budget REAL,
    cl_active INTEGER,
    cl_members INTEGER
);
INSERT INTO legacy_clubs VALUES (1, 'Coding Club', 'Learn programming and compete in hackathons', 'dr.smith@olduni.edu', 'dave.k@olduni.edu', '2018-09-01', 'Friday', 'SH-105', 3000.00, 1, 25);
INSERT INTO legacy_clubs VALUES (2, 'Math Society', 'Explore mathematics beyond the classroom', 'dr.jones@olduni.edu', 'alice.w@olduni.edu', '2015-09-01', 'Wednesday', 'MB-101', 1500.00, 1, 15);
INSERT INTO legacy_clubs VALUES (3, 'Literary Circle', 'Book club and creative writing group', 'dr.williams@olduni.edu', 'carol.l@olduni.edu', '2010-09-01', 'Tuesday', 'HH-105', 1000.00, 1, 12);
INSERT INTO legacy_clubs VALUES (4, 'Physics Society', 'Demos experiments and physics outreach', 'dr.garcia@olduni.edu', 'eve.t@olduni.edu', '2012-09-01', 'Thursday', 'SH-210', 2000.00, 1, 18);
INSERT INTO legacy_clubs VALUES (5, 'Debate Team', 'Competitive debate and public speaking', 'dr.williams@olduni.edu', 'bob.p@olduni.edu', '2005-09-01', 'Monday', 'HH-201', 2500.00, 1, 20);

CREATE TABLE legacy_book_loans (
    blid INTEGER PRIMARY KEY,
    bl_student_email TEXT,
    bl_title TEXT,
    bl_isbn TEXT,
    bl_loaned TEXT,
    bl_due TEXT,
    bl_returned TEXT,
    bl_fine REAL,
    bl_status TEXT,
    bl_branch TEXT,
    bl_staff TEXT
);
INSERT INTO legacy_book_loans VALUES (1, 'alice.w@olduni.edu', 'Introduction to Algorithms', '978-0262033848', '2025-09-01', '2025-09-29', '2025-09-28', 0.00, 'returned', 'Main Library', 'Librarian Jones');
INSERT INTO legacy_book_loans VALUES (2, 'alice.w@olduni.edu', 'Clean Code', '978-0132350884', '2025-09-15', '2025-10-13', '2025-10-10', 0.00, 'returned', 'Main Library', 'Librarian Smith');
INSERT INTO legacy_book_loans VALUES (3, 'bob.p@olduni.edu', 'Stewart Calculus', '978-1285740621', '2025-09-02', '2025-09-30', '2025-10-05', 2.50, 'returned', 'Main Library', 'Librarian Jones');
INSERT INTO legacy_book_loans VALUES (4, 'bob.p@olduni.edu', 'Linear Algebra Done Right', '978-3319110790', '2025-09-10', '2025-10-08', NULL, 5.00, 'overdue', 'Science Branch', 'Librarian Davis');
INSERT INTO legacy_book_loans VALUES (5, 'carol.l@olduni.edu', 'The Elements of Style', '978-0205309023', '2025-09-05', '2025-10-03', '2025-09-30', 0.00, 'returned', 'Humanities Branch', 'Librarian Wilson');
INSERT INTO legacy_book_loans VALUES (6, 'dave.k@olduni.edu', 'Database System Concepts', '978-0078022159', '2025-09-08', '2025-10-06', '2025-10-01', 0.00, 'returned', 'Science Branch', 'Librarian Davis');
INSERT INTO legacy_book_loans VALUES (7, 'dave.k@olduni.edu', 'The Art of Computer Programming', '978-0201896831', '2025-10-01', '2025-10-29', NULL, 0.00, 'active', 'Main Library', 'Librarian Jones');
INSERT INTO legacy_book_loans VALUES (8, 'eve.t@olduni.edu', 'University Physics', '978-0133969290', '2025-09-03', '2025-10-01', '2025-09-29', 0.00, 'returned', 'Science Branch', 'Librarian Davis');
INSERT INTO legacy_book_loans VALUES (9, 'frank.r@olduni.edu', 'Principles of Mathematical Analysis', '978-0070856134', '2025-09-12', '2025-10-10', NULL, 3.00, 'overdue', 'Main Library', 'Librarian Smith');
INSERT INTO legacy_book_loans VALUES (10, 'grace.h@olduni.edu', 'Feynman Lectures on Physics', '978-0465023820', '2025-09-15', '2025-10-13', '2025-10-12', 0.00, 'returned', 'Science Branch', 'Librarian Davis');
INSERT INTO legacy_book_loans VALUES (11, 'henry.m@olduni.edu', 'On Writing Well', '978-0060891541', '2025-09-08', '2025-10-06', '2025-10-06', 0.00, 'returned', 'Humanities Branch', 'Librarian Wilson');
INSERT INTO legacy_book_loans VALUES (12, 'grace.h@olduni.edu', 'Classical Mechanics', '978-1891389221', '2025-10-05', '2025-11-02', NULL, 0.00, 'active', 'Science Branch', 'Librarian Davis');
""";

TARGET_SQL = """
CREATE TABLE departments (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    code TEXT NOT NULL UNIQUE,
    building TEXT NOT NULL,
    floor INTEGER NOT NULL,
    phone TEXT NOT NULL,
    head_faculty_id INTEGER,
    budget REAL NOT NULL DEFAULT 0.0,
    founded_year INTEGER NOT NULL,
    description TEXT NOT NULL
);
INSERT INTO departments VALUES (1, 'Computer Science', 'CS', 'Science Hall', 3, '555-3001', 1, 2500000.00, 1985, 'Department of Computer Science and Engineering');
INSERT INTO departments VALUES (2, 'Mathematics', 'MATH', 'Math Building', 2, '555-3002', 2, 1800000.00, 1920, 'Department of Mathematics and Applied Mathematics');
INSERT INTO departments VALUES (3, 'English', 'ENG', 'Humanities Hall', 1, '555-3003', 3, 1200000.00, 1900, 'Department of English Language and Literature');
INSERT INTO departments VALUES (4, 'Physics', 'PHYS', 'Science Hall', 4, '555-3004', 4, 2200000.00, 1935, 'Department of Physics and Astronomy');

CREATE TABLE faculty (
    id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT NOT NULL,
    hire_date TEXT NOT NULL,
    department_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    office_location TEXT NOT NULL,
    salary REAL NOT NULL,
    tenure_status TEXT NOT NULL,
    FOREIGN KEY (department_id) REFERENCES departments(id)
);
INSERT INTO faculty VALUES (1, 'John', 'Smith', 'dr.smith@olduni.edu', '555-2001', '2010-08-15', 1, 'Professor', 'Science Hall 301', 120000.00, 'tenured');
INSERT INTO faculty VALUES (2, 'Margaret', 'Jones', 'dr.jones@olduni.edu', '555-2002', '2012-01-10', 2, 'Associate Professor', 'Math Building 205', 105000.00, 'tenured');
INSERT INTO faculty VALUES (3, 'Robert', 'Williams', 'dr.williams@olduni.edu', '555-2003', '2015-08-20', 3, 'Assistant Professor', 'Humanities Hall 110', 85000.00, 'tenure-track');
INSERT INTO faculty VALUES (4, 'Elena', 'Garcia', 'dr.garcia@olduni.edu', '555-2004', '2008-01-05', 4, 'Professor', 'Science Hall 402', 125000.00, 'tenured');
INSERT INTO faculty VALUES (5, 'Wei', 'Chen', 'dr.chen@olduni.edu', '555-2005', '2018-08-15', 1, 'Lecturer', 'Science Hall 303', 72000.00, 'non-tenure');
INSERT INTO faculty VALUES (6, 'James', 'Taylor', 'dr.taylor@olduni.edu', '555-2006', '2020-01-10', 2, 'Lecturer', 'Math Building 207', 68000.00, 'non-tenure');

CREATE TABLE majors (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    department_id INTEGER NOT NULL,
    required_credits INTEGER NOT NULL,
    description TEXT,
    FOREIGN KEY (department_id) REFERENCES departments(id)
);
INSERT INTO majors VALUES (1, 'Computer Science', 1, 120, 'Study of computation and information');
INSERT INTO majors VALUES (2, 'Mathematics', 2, 110, 'Study of numbers, structure, and space');
INSERT INTO majors VALUES (3, 'English', 3, 105, 'Study of language and literature');
INSERT INTO majors VALUES (4, 'Physics', 4, 115, 'Study of matter and energy');

CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT NOT NULL,
    dob TEXT NOT NULL,
    enrollment_date TEXT NOT NULL,
    major_id INTEGER NOT NULL,
    advisor_id INTEGER NOT NULL,
    gpa REAL,
    status TEXT NOT NULL DEFAULT 'active',
    FOREIGN KEY (major_id) REFERENCES majors(id),
    FOREIGN KEY (advisor_id) REFERENCES faculty(id)
);
INSERT INTO students VALUES (1, 'Alice', 'Wang', 'alice.w@olduni.edu', '555-1001', '2002-03-15', '2022-08-20', 1, 1, 3.7, 'active');
INSERT INTO students VALUES (2, 'Bob', 'Patel', 'bob.p@olduni.edu', '555-1002', '2001-07-22', '2021-08-18', 2, 2, 3.0, 'active');
INSERT INTO students VALUES (3, 'Carol', 'Lopez', 'carol.l@olduni.edu', '555-1003', '2003-11-05', '2023-08-21', 3, 3, 3.4, 'active');
INSERT INTO students VALUES (4, 'Dave', 'Kim', 'dave.k@olduni.edu', '555-1004', '2000-01-30', '2020-08-17', 1, 1, 3.8, 'active');
INSERT INTO students VALUES (5, 'Eve', 'Tanaka', 'eve.t@olduni.edu', '555-1005', '2002-09-12', '2022-08-20', 4, 4, 3.2, 'active');
INSERT INTO students VALUES (6, 'Frank', 'Russo', 'frank.r@olduni.edu', '555-1006', '2001-04-18', '2021-08-18', 2, 2, 2.7, 'probation');
INSERT INTO students VALUES (7, 'Grace', 'Huang', 'grace.h@olduni.edu', '555-1007', '2003-06-25', '2023-08-21', 4, 4, 3.5, 'active');
INSERT INTO students VALUES (8, 'Henry', 'Morgan', 'henry.m@olduni.edu', '555-1008', '2002-12-01', '2022-08-20', 3, 3, 2.9, 'active');

CREATE TABLE student_addresses (
    id INTEGER PRIMARY KEY,
    student_id INTEGER NOT NULL UNIQUE,
    address_line1 TEXT NOT NULL,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    zip TEXT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(id)
);
INSERT INTO student_addresses VALUES (1, 1, '100 Elm St', 'Boston', 'MA', '02101');
INSERT INTO student_addresses VALUES (2, 2, '200 Oak Ave', 'Cambridge', 'MA', '02139');
INSERT INTO student_addresses VALUES (3, 3, '300 Pine Rd', 'Somerville', 'MA', '02143');
INSERT INTO student_addresses VALUES (4, 4, '400 Maple Dr', 'Brookline', 'MA', '02445');
INSERT INTO student_addresses VALUES (5, 5, '500 Cedar Ln', 'Newton', 'MA', '02458');
INSERT INTO student_addresses VALUES (6, 6, '600 Birch Ct', 'Medford', 'MA', '02155');
INSERT INTO student_addresses VALUES (7, 7, '700 Walnut St', 'Arlington', 'MA', '02474');
INSERT INTO student_addresses VALUES (8, 8, '800 Spruce Ave', 'Belmont', 'MA', '02478');

CREATE TABLE semesters (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    year INTEGER NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    is_current INTEGER NOT NULL DEFAULT 0
);
INSERT INTO semesters VALUES (1, 'Fall', 2025, '2025-08-25', '2025-12-15', 1);

CREATE TABLE courses (
    id INTEGER PRIMARY KEY,
    code TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    credits INTEGER NOT NULL,
    department_id INTEGER NOT NULL,
    instructor_id INTEGER NOT NULL,
    max_capacity INTEGER NOT NULL,
    current_enrollment INTEGER NOT NULL DEFAULT 0,
    semester_id INTEGER NOT NULL,
    room_number TEXT NOT NULL,
    FOREIGN KEY (department_id) REFERENCES departments(id),
    FOREIGN KEY (instructor_id) REFERENCES faculty(id),
    FOREIGN KEY (semester_id) REFERENCES semesters(id)
);
INSERT INTO courses VALUES (1, 'CS101', 'Intro to Programming', 'Learn basic programming concepts', 4, 1, 1, 40, 30, 1, 'SH-101');
INSERT INTO courses VALUES (2, 'CS201', 'Data Structures', 'Advanced data structures and algorithms', 4, 1, 1, 35, 25, 1, 'SH-102');
INSERT INTO courses VALUES (3, 'MATH101', 'Calculus I', 'Introduction to differential calculus', 4, 2, 2, 45, 35, 1, 'MB-201');
INSERT INTO courses VALUES (4, 'MATH201', 'Linear Algebra', 'Vectors, matrices, and linear transformations', 3, 2, 2, 40, 28, 1, 'MB-202');
INSERT INTO courses VALUES (5, 'ENG101', 'English Composition', 'Academic writing fundamentals', 3, 3, 3, 30, 25, 1, 'HH-101');
INSERT INTO courses VALUES (6, 'ENG201', 'American Literature', 'Survey of American literary works', 3, 3, 3, 30, 20, 1, 'HH-102');
INSERT INTO courses VALUES (7, 'PHYS101', 'Physics I', 'Mechanics and thermodynamics', 4, 4, 4, 40, 32, 1, 'SH-201');
INSERT INTO courses VALUES (8, 'PHYS201', 'Physics II', 'Electricity and magnetism', 4, 4, 4, 35, 22, 1, 'SH-202');
INSERT INTO courses VALUES (9, 'CS301', 'Database Systems', 'Relational databases and SQL', 3, 1, 5, 30, 20, 1, 'SH-103');
INSERT INTO courses VALUES (10, 'MATH301', 'Probability and Stats', 'Intro to probability and statistics', 3, 2, 6, 35, 30, 1, 'MB-301');

CREATE TABLE enrollments (
    id INTEGER PRIMARY KEY,
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    grade TEXT,
    grade_points REAL,
    enrollment_date TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'enrolled',
    midterm_score REAL,
    final_score REAL,
    attendance_pct REAL,
    notes TEXT,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (course_id) REFERENCES courses(id)
);
INSERT INTO enrollments VALUES (1, 1, 1, 'A', 4.0, '2025-08-25', 'completed', 92.0, 95.0, 96.0, 'Excellent work');
INSERT INTO enrollments VALUES (2, 1, 3, 'A-', 3.7, '2025-08-25', 'completed', 88.0, 91.0, 94.0, NULL);
INSERT INTO enrollments VALUES (3, 1, 5, 'A', 4.0, '2025-08-25', 'completed', 95.0, 93.0, 98.0, 'Strong writer');
INSERT INTO enrollments VALUES (4, 2, 3, 'B', 3.0, '2025-08-25', 'completed', 78.0, 82.0, 88.0, NULL);
INSERT INTO enrollments VALUES (5, 2, 4, 'B+', 3.3, '2025-08-25', 'completed', 80.0, 85.0, 90.0, NULL);
INSERT INTO enrollments VALUES (6, 2, 2, 'B-', 2.7, '2025-08-25', 'completed', 75.0, 78.0, 85.0, 'Needs improvement in recursion');
INSERT INTO enrollments VALUES (7, 3, 5, 'A-', 3.7, '2025-08-25', 'completed', 90.0, 88.0, 95.0, NULL);
INSERT INTO enrollments VALUES (8, 3, 6, NULL, NULL, '2025-08-25', 'enrolled', NULL, NULL, 80.0, 'In progress');
INSERT INTO enrollments VALUES (9, 3, 7, 'B+', 3.3, '2025-08-25', 'completed', 82.0, 86.0, 91.0, NULL);
INSERT INTO enrollments VALUES (10, 4, 1, 'A', 4.0, '2025-08-25', 'completed', 96.0, 98.0, 99.0, 'Top student');
INSERT INTO enrollments VALUES (11, 4, 2, 'A', 4.0, '2025-08-25', 'completed', 94.0, 96.0, 97.0, NULL);
INSERT INTO enrollments VALUES (12, 4, 9, 'A-', 3.7, '2025-08-25', 'completed', 90.0, 92.0, 95.0, NULL);
INSERT INTO enrollments VALUES (13, 5, 7, 'B+', 3.3, '2025-08-25', 'completed', 84.0, 87.0, 92.0, NULL);
INSERT INTO enrollments VALUES (14, 5, 8, 'B', 3.0, '2025-08-25', 'completed', 79.0, 81.0, 88.0, NULL);
INSERT INTO enrollments VALUES (15, 5, 3, 'B+', 3.3, '2025-08-25', 'completed', 83.0, 86.0, 90.0, NULL);
INSERT INTO enrollments VALUES (16, 6, 3, 'C+', 2.3, '2025-08-25', 'completed', 68.0, 72.0, 75.0, 'Attendance issues');
INSERT INTO enrollments VALUES (17, 6, 4, 'C', 2.0, '2025-08-25', 'completed', 65.0, 70.0, 72.0, NULL);
INSERT INTO enrollments VALUES (18, 7, 7, NULL, NULL, '2025-08-25', 'enrolled', NULL, NULL, 85.0, 'In progress');
INSERT INTO enrollments VALUES (19, 7, 3, 'B', 3.0, '2025-08-25', 'completed', 80.0, 83.0, 89.0, NULL);
INSERT INTO enrollments VALUES (20, 8, 5, 'B-', 2.7, '2025-08-25', 'completed', 74.0, 77.0, 82.0, NULL);

CREATE TABLE assignments (
    id INTEGER PRIMARY KEY,
    course_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    due_date TEXT NOT NULL,
    max_points REAL NOT NULL,
    weight_pct REAL NOT NULL,
    assignment_type TEXT NOT NULL,
    is_published INTEGER NOT NULL DEFAULT 1,
    created_by_id INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (course_id) REFERENCES courses(id),
    FOREIGN KEY (created_by_id) REFERENCES faculty(id)
);
INSERT INTO assignments VALUES (1, 1, 'Hello World Program', 'Write your first program in Python', '2025-09-15', 100.0, 5.0, 'homework', 1, 1, '2025-08-25');
INSERT INTO assignments VALUES (2, 1, 'Midterm Exam', 'Covers chapters 1-6', '2025-10-15', 200.0, 25.0, 'exam', 1, 1, '2025-08-25');
INSERT INTO assignments VALUES (3, 2, 'Linked List Implementation', 'Implement singly and doubly linked lists', '2025-09-20', 100.0, 10.0, 'homework', 1, 1, '2025-08-26');
INSERT INTO assignments VALUES (4, 3, 'Problem Set 1', 'Limits and continuity exercises', '2025-09-10', 50.0, 5.0, 'homework', 1, 2, '2025-08-25');
INSERT INTO assignments VALUES (5, 3, 'Midterm Exam', 'Chapters 1-4', '2025-10-12', 100.0, 30.0, 'exam', 1, 2, '2025-08-25');
INSERT INTO assignments VALUES (6, 5, 'Personal Essay', 'Write a 5-page personal narrative', '2025-09-18', 100.0, 15.0, 'essay', 1, 3, '2025-08-25');
INSERT INTO assignments VALUES (7, 5, 'Research Paper Draft', 'First draft of research paper', '2025-10-20', 100.0, 10.0, 'essay', 1, 3, '2025-08-26');
INSERT INTO assignments VALUES (8, 7, 'Lab Report 1', 'Kinematics experiment report', '2025-09-12', 50.0, 5.0, 'lab', 1, 4, '2025-08-25');
INSERT INTO assignments VALUES (9, 7, 'Midterm Exam', 'Mechanics chapters 1-5', '2025-10-14', 150.0, 25.0, 'exam', 1, 4, '2025-08-25');
INSERT INTO assignments VALUES (10, 9, 'SQL Exercises', 'Practice SELECT, JOIN, and subqueries', '2025-09-22', 80.0, 8.0, 'homework', 1, 5, '2025-08-27');
INSERT INTO assignments VALUES (11, 4, 'Matrix Operations', 'Solve systems of linear equations', '2025-09-16', 60.0, 8.0, 'homework', 1, 2, '2025-08-26');
INSERT INTO assignments VALUES (12, 8, 'Coulombs Law Problems', 'Electric force calculations', '2025-09-19', 70.0, 7.0, 'homework', 1, 4, '2025-08-26');

CREATE TABLE submissions (
    id INTEGER PRIMARY KEY,
    assignment_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    submitted_at TEXT NOT NULL,
    file_url TEXT NOT NULL,
    score REAL,
    feedback TEXT,
    is_late INTEGER NOT NULL DEFAULT 0,
    graded_by_id INTEGER,
    graded_at TEXT,
    status TEXT NOT NULL DEFAULT 'submitted',
    FOREIGN KEY (assignment_id) REFERENCES assignments(id),
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (graded_by_id) REFERENCES faculty(id)
);
INSERT INTO submissions VALUES (1, 1, 1, '2025-09-14 23:30:00', '/files/alice_hw1.py', 95.0, 'Great job!', 0, 1, '2025-09-16', 'graded');
INSERT INTO submissions VALUES (2, 1, 4, '2025-09-14 20:00:00', '/files/dave_hw1.py', 100.0, 'Perfect', 0, 1, '2025-09-16', 'graded');
INSERT INTO submissions VALUES (3, 2, 1, '2025-10-15 10:00:00', '/files/alice_midterm.pdf', 92.0, NULL, 0, 1, '2025-10-18', 'graded');
INSERT INTO submissions VALUES (4, 2, 4, '2025-10-15 10:00:00', '/files/dave_midterm.pdf', 96.0, 'Excellent', 0, 1, '2025-10-18', 'graded');
INSERT INTO submissions VALUES (5, 3, 2, '2025-09-21 08:00:00', '/files/bob_ll.zip', 72.0, 'Missing edge cases', 1, 1, '2025-09-23', 'graded');
INSERT INTO submissions VALUES (6, 3, 4, '2025-09-19 18:00:00', '/files/dave_ll.zip', 98.0, 'Excellent implementation', 0, 1, '2025-09-23', 'graded');
INSERT INTO submissions VALUES (7, 4, 1, '2025-09-09 22:00:00', '/files/alice_ps1.pdf', 45.0, NULL, 0, 2, '2025-09-12', 'graded');
INSERT INTO submissions VALUES (8, 4, 2, '2025-09-10 01:00:00', '/files/bob_ps1.pdf', 38.0, 'Review limits section', 1, 2, '2025-09-12', 'graded');
INSERT INTO submissions VALUES (9, 4, 5, '2025-09-09 20:00:00', '/files/eve_ps1.pdf', 42.0, NULL, 0, 2, '2025-09-12', 'graded');
INSERT INTO submissions VALUES (10, 6, 1, '2025-09-17 15:00:00', '/files/alice_essay.docx', 93.0, 'Beautiful prose', 0, 3, '2025-09-20', 'graded');
INSERT INTO submissions VALUES (11, 6, 3, '2025-09-18 09:00:00', '/files/carol_essay.docx', 90.0, 'Strong voice', 0, 3, '2025-09-20', 'graded');
INSERT INTO submissions VALUES (12, 6, 8, '2025-09-19 11:00:00', '/files/henry_essay.docx', 74.0, 'Needs more detail', 1, 3, '2025-09-20', 'graded');
INSERT INTO submissions VALUES (13, 8, 5, '2025-09-12 14:00:00', '/files/eve_lab1.pdf', 44.0, NULL, 0, 4, '2025-09-15', 'graded');
INSERT INTO submissions VALUES (14, 8, 3, '2025-09-12 16:00:00', '/files/carol_lab1.pdf', 46.0, 'Good analysis', 0, 4, '2025-09-15', 'graded');
INSERT INTO submissions VALUES (15, 10, 4, '2025-09-21 22:00:00', '/files/dave_sql.sql', 78.0, 'Good joins', 0, 5, '2025-09-24', 'graded');

CREATE TABLE announcements (
    id INTEGER PRIMARY KEY,
    course_id INTEGER NOT NULL,
    author_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    priority TEXT NOT NULL DEFAULT 'normal',
    is_pinned INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    expiry_date TEXT,
    FOREIGN KEY (course_id) REFERENCES courses(id),
    FOREIGN KEY (author_id) REFERENCES faculty(id)
);
INSERT INTO announcements VALUES (1, 1, 1, 'Welcome to CS101', 'Please review the syllabus before first class.', 'high', 1, '2025-08-20', '2025-08-20', '2025-09-01');
INSERT INTO announcements VALUES (2, 1, 1, 'Office Hours Change', 'Office hours moved to Thursdays 2-4pm.', 'normal', 0, '2025-09-05', '2025-09-05', '2025-12-15');
INSERT INTO announcements VALUES (3, 3, 2, 'Textbook Required', 'Please purchase Stewart Calculus 9th edition.', 'high', 1, '2025-08-21', '2025-08-21', '2025-09-10');
INSERT INTO announcements VALUES (4, 5, 3, 'Essay Guidelines', 'All essays must follow MLA format.', 'normal', 1, '2025-08-22', '2025-08-22', '2025-12-15');
INSERT INTO announcements VALUES (5, 7, 4, 'Lab Safety Training', 'Mandatory safety training on Sept 5.', 'high', 0, '2025-08-28', '2025-08-28', '2025-09-05');
INSERT INTO announcements VALUES (6, 2, 1, 'Prerequisites Reminder', 'CS101 is a prerequisite for this course.', 'normal', 0, '2025-08-20', '2025-08-20', '2025-09-01');
INSERT INTO announcements VALUES (7, 9, 5, 'Software Installation', 'Install PostgreSQL and SQLite before Week 2.', 'high', 1, '2025-08-25', '2025-08-25', '2025-09-08');
INSERT INTO announcements VALUES (8, 4, 2, 'Study Group Formation', 'Form study groups of 3-4 students.', 'normal', 0, '2025-09-01', '2025-09-01', '2025-12-15');

CREATE TABLE attendance (
    id INTEGER PRIMARY KEY,
    course_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    session_date TEXT NOT NULL,
    status TEXT NOT NULL,
    check_in_time TEXT,
    check_out_time TEXT,
    duration_min INTEGER NOT NULL DEFAULT 0,
    notes TEXT,
    recorded_by_id INTEGER NOT NULL,
    FOREIGN KEY (course_id) REFERENCES courses(id),
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (recorded_by_id) REFERENCES faculty(id)
);
INSERT INTO attendance VALUES (1, 1, 1, '2025-09-02', 'present', '09:00', '10:15', 75, NULL, 1);
INSERT INTO attendance VALUES (2, 1, 4, '2025-09-02', 'present', '08:58', '10:15', 77, NULL, 1);
INSERT INTO attendance VALUES (3, 1, 1, '2025-09-04', 'present', '09:02', '10:15', 73, NULL, 1);
INSERT INTO attendance VALUES (4, 1, 4, '2025-09-04', 'late', '09:20', '10:15', 55, 'Arrived 20 min late', 1);
INSERT INTO attendance VALUES (5, 3, 1, '2025-09-03', 'present', '10:00', '11:15', 75, NULL, 2);
INSERT INTO attendance VALUES (6, 3, 2, '2025-09-03', 'present', '10:05', '11:15', 70, NULL, 2);
INSERT INTO attendance VALUES (7, 3, 5, '2025-09-03', 'present', '10:00', '11:15', 75, NULL, 2);
INSERT INTO attendance VALUES (8, 3, 6, '2025-09-03', 'absent', NULL, NULL, 0, 'No show', 2);
INSERT INTO attendance VALUES (9, 5, 1, '2025-09-02', 'present', '13:00', '14:15', 75, NULL, 3);
INSERT INTO attendance VALUES (10, 5, 3, '2025-09-02', 'present', '13:00', '14:15', 75, NULL, 3);
INSERT INTO attendance VALUES (11, 5, 8, '2025-09-02', 'late', '13:15', '14:15', 60, 'Arrived late', 3);
INSERT INTO attendance VALUES (12, 7, 5, '2025-09-03', 'present', '14:00', '15:30', 90, NULL, 4);
INSERT INTO attendance VALUES (13, 7, 3, '2025-09-03', 'present', '14:00', '15:30', 90, NULL, 4);
INSERT INTO attendance VALUES (14, 7, 7, '2025-09-03', 'present', '14:02', '15:30', 88, NULL, 4);
INSERT INTO attendance VALUES (15, 2, 2, '2025-09-02', 'present', '11:00', '12:15', 75, NULL, 1);
INSERT INTO attendance VALUES (16, 2, 4, '2025-09-02', 'present', '11:00', '12:15', 75, NULL, 1);
INSERT INTO attendance VALUES (17, 9, 4, '2025-09-04', 'present', '15:00', '16:15', 75, NULL, 5);
INSERT INTO attendance VALUES (18, 4, 2, '2025-09-04', 'present', '10:00', '11:15', 75, NULL, 2);

CREATE TABLE course_materials (
    id INTEGER PRIMARY KEY,
    course_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    file_url TEXT NOT NULL,
    file_type TEXT NOT NULL,
    file_size INTEGER NOT NULL,
    uploaded_by_id INTEGER NOT NULL,
    description TEXT NOT NULL,
    download_count INTEGER NOT NULL DEFAULT 0,
    is_visible INTEGER NOT NULL DEFAULT 1,
    uploaded_at TEXT NOT NULL,
    FOREIGN KEY (course_id) REFERENCES courses(id),
    FOREIGN KEY (uploaded_by_id) REFERENCES faculty(id)
);
INSERT INTO course_materials VALUES (1, 1, 'Syllabus', '/materials/cs101_syllabus.pdf', 'pdf', 245000, 1, 'Course syllabus and schedule', 45, 1, '2025-08-15');
INSERT INTO course_materials VALUES (2, 1, 'Lecture 1 Slides', '/materials/cs101_lec1.pptx', 'pptx', 1200000, 1, 'Introduction to programming', 38, 1, '2025-09-01');
INSERT INTO course_materials VALUES (3, 3, 'Formula Sheet', '/materials/math101_formulas.pdf', 'pdf', 120000, 2, 'Key formulas for calculus', 52, 1, '2025-08-20');
INSERT INTO course_materials VALUES (4, 3, 'Practice Problems', '/materials/math101_practice.pdf', 'pdf', 350000, 2, 'Extra practice for midterm', 30, 1, '2025-10-01');
INSERT INTO course_materials VALUES (5, 5, 'Style Guide', '/materials/eng101_style.pdf', 'pdf', 180000, 3, 'MLA formatting guide', 40, 1, '2025-08-18');
INSERT INTO course_materials VALUES (6, 5, 'Essay Rubric', '/materials/eng101_rubric.pdf', 'pdf', 95000, 3, 'Grading criteria for essays', 35, 1, '2025-08-18');
INSERT INTO course_materials VALUES (7, 7, 'Lab Manual', '/materials/phys101_lab.pdf', 'pdf', 2500000, 4, 'Complete lab manual', 48, 1, '2025-08-16');
INSERT INTO course_materials VALUES (8, 2, 'Big-O Cheatsheet', '/materials/cs201_bigo.pdf', 'pdf', 85000, 1, 'Time complexity reference', 28, 1, '2025-09-05');
INSERT INTO course_materials VALUES (9, 9, 'SQL Reference', '/materials/cs301_sql.pdf', 'pdf', 310000, 5, 'SQL syntax quick reference', 22, 1, '2025-08-28');
INSERT INTO course_materials VALUES (10, 8, 'Maxwells Equations', '/materials/phys201_maxwell.pdf', 'pdf', 200000, 4, 'Summary of electromagnetic theory', 18, 1, '2025-08-22');

CREATE TABLE discussion_posts (
    id INTEGER PRIMARY KEY,
    course_id INTEGER NOT NULL,
    author_type TEXT NOT NULL,
    author_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    parent_post_id INTEGER,
    likes_count INTEGER NOT NULL DEFAULT 0,
    is_pinned INTEGER NOT NULL DEFAULT 0,
    is_anonymous INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (course_id) REFERENCES courses(id),
    FOREIGN KEY (parent_post_id) REFERENCES discussion_posts(id)
);
INSERT INTO discussion_posts VALUES (1, 1, 'student', 1, 'Help with HW1', 'I am stuck on the loop exercise. Any tips?', NULL, 3, 0, 0, '2025-09-10', '2025-09-10');
INSERT INTO discussion_posts VALUES (2, 1, 'student', 4, 'Re: Help with HW1', 'Try using a while loop instead of for.', 1, 5, 0, 0, '2025-09-10', '2025-09-10');
INSERT INTO discussion_posts VALUES (3, 1, 'faculty', 1, 'Re: Help with HW1', 'Good suggestion Dave. Also review chapter 3.', 1, 2, 0, 0, '2025-09-11', '2025-09-11');
INSERT INTO discussion_posts VALUES (4, 3, 'student', 2, 'Limit Problem Clarification', 'Can someone explain L Hopitals rule with an example?', NULL, 4, 0, 0, '2025-09-15', '2025-09-15');
INSERT INTO discussion_posts VALUES (5, 3, 'faculty', 2, 'Re: Limit Problem', 'See the attached example from lecture 5.', 4, 6, 0, 0, '2025-09-15', '2025-09-15');
INSERT INTO discussion_posts VALUES (6, 5, 'student', 3, 'MLA Citation Question', 'How do I cite an online article in MLA?', NULL, 2, 0, 0, '2025-09-12', '2025-09-12');
INSERT INTO discussion_posts VALUES (7, 5, 'faculty', 3, 'Re: MLA Citation', 'Use the format: Author. Title. Website, Date, URL.', 6, 4, 0, 0, '2025-09-12', '2025-09-12');
INSERT INTO discussion_posts VALUES (8, 7, 'student', 5, 'Lab Partner Needed', 'Looking for a lab partner for Thursday sessions.', NULL, 1, 0, 0, '2025-09-08', '2025-09-08');
INSERT INTO discussion_posts VALUES (9, 7, 'student', 7, 'Re: Lab Partner', 'I am available! Send me an email.', 8, 1, 0, 0, '2025-09-08', '2025-09-08');
INSERT INTO discussion_posts VALUES (10, 9, 'student', 4, 'JOIN vs Subquery', 'When should I prefer JOIN over subquery?', NULL, 7, 0, 0, '2025-09-20', '2025-09-20');

CREATE TABLE office_hours (
    id INTEGER PRIMARY KEY,
    faculty_id INTEGER NOT NULL,
    day_of_week TEXT NOT NULL,
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    location TEXT,
    is_virtual INTEGER NOT NULL DEFAULT 0,
    meeting_url TEXT,
    max_students INTEGER NOT NULL DEFAULT 5,
    semester_id INTEGER NOT NULL,
    FOREIGN KEY (faculty_id) REFERENCES faculty(id),
    FOREIGN KEY (semester_id) REFERENCES semesters(id)
);
INSERT INTO office_hours VALUES (1, 1, 'Tuesday', '14:00', '16:00', 'SH-301', 0, NULL, 5, 1);
INSERT INTO office_hours VALUES (2, 1, 'Thursday', '14:00', '16:00', 'SH-301', 0, NULL, 5, 1);
INSERT INTO office_hours VALUES (3, 2, 'Monday', '10:00', '12:00', 'MB-205', 0, NULL, 4, 1);
INSERT INTO office_hours VALUES (4, 2, 'Wednesday', '10:00', '12:00', NULL, 1, 'https://zoom.us/jones123', 6, 1);
INSERT INTO office_hours VALUES (5, 3, 'Tuesday', '11:00', '12:30', 'HH-110', 0, NULL, 3, 1);
INSERT INTO office_hours VALUES (6, 4, 'Friday', '13:00', '15:00', 'SH-402', 0, NULL, 4, 1);
INSERT INTO office_hours VALUES (7, 5, 'Wednesday', '15:00', '17:00', NULL, 1, 'https://zoom.us/chen456', 5, 1);
INSERT INTO office_hours VALUES (8, 6, 'Thursday', '09:00', '11:00', 'MB-207', 0, NULL, 4, 1);

CREATE TABLE student_clubs (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    description TEXT NOT NULL,
    faculty_advisor_id INTEGER NOT NULL,
    president_id INTEGER NOT NULL,
    founded_date TEXT NOT NULL,
    meeting_day TEXT NOT NULL,
    meeting_room TEXT NOT NULL,
    budget REAL NOT NULL DEFAULT 0.0,
    is_active INTEGER NOT NULL DEFAULT 1,
    member_count INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (faculty_advisor_id) REFERENCES faculty(id),
    FOREIGN KEY (president_id) REFERENCES students(id)
);
INSERT INTO student_clubs VALUES (1, 'Coding Club', 'Learn programming and compete in hackathons', 1, 4, '2018-09-01', 'Friday', 'SH-105', 3000.00, 1, 25);
INSERT INTO student_clubs VALUES (2, 'Math Society', 'Explore mathematics beyond the classroom', 2, 1, '2015-09-01', 'Wednesday', 'MB-101', 1500.00, 1, 15);
INSERT INTO student_clubs VALUES (3, 'Literary Circle', 'Book club and creative writing group', 3, 3, '2010-09-01', 'Tuesday', 'HH-105', 1000.00, 1, 12);
INSERT INTO student_clubs VALUES (4, 'Physics Society', 'Demos experiments and physics outreach', 4, 5, '2012-09-01', 'Thursday', 'SH-210', 2000.00, 1, 18);
INSERT INTO student_clubs VALUES (5, 'Debate Team', 'Competitive debate and public speaking', 3, 2, '2005-09-01', 'Monday', 'HH-201', 2500.00, 1, 20);

CREATE TABLE library_loans (
    id INTEGER PRIMARY KEY,
    student_id INTEGER NOT NULL,
    book_title TEXT NOT NULL,
    isbn TEXT NOT NULL,
    loan_date TEXT NOT NULL,
    due_date TEXT NOT NULL,
    return_date TEXT,
    fine_amount REAL NOT NULL DEFAULT 0.0,
    status TEXT NOT NULL DEFAULT 'active',
    library_branch TEXT NOT NULL,
    processed_by TEXT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(id)
);
INSERT INTO library_loans VALUES (1, 1, 'Introduction to Algorithms', '978-0262033848', '2025-09-01', '2025-09-29', '2025-09-28', 0.00, 'returned', 'Main Library', 'Librarian Jones');
INSERT INTO library_loans VALUES (2, 1, 'Clean Code', '978-0132350884', '2025-09-15', '2025-10-13', '2025-10-10', 0.00, 'returned', 'Main Library', 'Librarian Smith');
INSERT INTO library_loans VALUES (3, 2, 'Stewart Calculus', '978-1285740621', '2025-09-02', '2025-09-30', '2025-10-05', 2.50, 'returned', 'Main Library', 'Librarian Jones');
INSERT INTO library_loans VALUES (4, 2, 'Linear Algebra Done Right', '978-3319110790', '2025-09-10', '2025-10-08', NULL, 5.00, 'overdue', 'Science Branch', 'Librarian Davis');
INSERT INTO library_loans VALUES (5, 3, 'The Elements of Style', '978-0205309023', '2025-09-05', '2025-10-03', '2025-09-30', 0.00, 'returned', 'Humanities Branch', 'Librarian Wilson');
INSERT INTO library_loans VALUES (6, 4, 'Database System Concepts', '978-0078022159', '2025-09-08', '2025-10-06', '2025-10-01', 0.00, 'returned', 'Science Branch', 'Librarian Davis');
INSERT INTO library_loans VALUES (7, 4, 'The Art of Computer Programming', '978-0201896831', '2025-10-01', '2025-10-29', NULL, 0.00, 'active', 'Main Library', 'Librarian Jones');
INSERT INTO library_loans VALUES (8, 5, 'University Physics', '978-0133969290', '2025-09-03', '2025-10-01', '2025-09-29', 0.00, 'returned', 'Science Branch', 'Librarian Davis');
INSERT INTO library_loans VALUES (9, 6, 'Principles of Mathematical Analysis', '978-0070856134', '2025-09-12', '2025-10-10', NULL, 3.00, 'overdue', 'Main Library', 'Librarian Smith');
INSERT INTO library_loans VALUES (10, 7, 'Feynman Lectures on Physics', '978-0465023820', '2025-09-15', '2025-10-13', '2025-10-12', 0.00, 'returned', 'Science Branch', 'Librarian Davis');
INSERT INTO library_loans VALUES (11, 8, 'On Writing Well', '978-0060891541', '2025-09-08', '2025-10-06', '2025-10-06', 0.00, 'returned', 'Humanities Branch', 'Librarian Wilson');
INSERT INTO library_loans VALUES (12, 7, 'Classical Mechanics', '978-1891389221', '2025-10-05', '2025-11-02', NULL, 0.00, 'active', 'Science Branch', 'Librarian Davis');

CREATE TABLE course_stats (
    id INTEGER PRIMARY KEY,
    course_id INTEGER NOT NULL UNIQUE,
    enrollment_count INTEGER NOT NULL,
    avg_grade_points REAL,
    avg_attendance_pct REAL,
    FOREIGN KEY (course_id) REFERENCES courses(id)
);
INSERT INTO course_stats VALUES (1, 1, 2, 4.0, 97.5);
INSERT INTO course_stats VALUES (2, 2, 2, 3.35, 91.0);
INSERT INTO course_stats VALUES (3, 3, 5, 3.06, 87.2);
INSERT INTO course_stats VALUES (4, 4, 2, 2.65, 81.0);
INSERT INTO course_stats VALUES (5, 5, 3, 3.47, 91.67);
INSERT INTO course_stats VALUES (6, 6, 1, NULL, 80.0);
INSERT INTO course_stats VALUES (7, 7, 3, 3.3, 89.33);
INSERT INTO course_stats VALUES (8, 8, 1, 3.0, 88.0);
INSERT INTO course_stats VALUES (9, 9, 1, 3.7, 95.0);
INSERT INTO course_stats VALUES (10, 10, 0, NULL, NULL);

CREATE TABLE student_activities (
    id INTEGER PRIMARY KEY,
    student_id INTEGER NOT NULL,
    activity_type TEXT NOT NULL,
    description TEXT NOT NULL,
    date TEXT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(id)
);
INSERT INTO student_activities VALUES (1, 1, 'migration', 'Account migrated to EduCloud', '2025-08-01');
INSERT INTO student_activities VALUES (2, 2, 'migration', 'Account migrated to EduCloud', '2025-08-01');
INSERT INTO student_activities VALUES (3, 3, 'migration', 'Account migrated to EduCloud', '2025-08-01');
INSERT INTO student_activities VALUES (4, 4, 'migration', 'Account migrated to EduCloud', '2025-08-01');
INSERT INTO student_activities VALUES (5, 5, 'migration', 'Account migrated to EduCloud', '2025-08-01');
INSERT INTO student_activities VALUES (6, 6, 'migration', 'Account migrated to EduCloud', '2025-08-01');
INSERT INTO student_activities VALUES (7, 7, 'migration', 'Account migrated to EduCloud', '2025-08-01');
INSERT INTO student_activities VALUES (8, 8, 'migration', 'Account migrated to EduCloud', '2025-08-01');

CREATE TABLE faculty_departments (
    id INTEGER PRIMARY KEY,
    faculty_id INTEGER NOT NULL,
    department_id INTEGER NOT NULL,
    role TEXT NOT NULL DEFAULT 'member',
    start_date TEXT NOT NULL,
    is_primary INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (faculty_id) REFERENCES faculty(id),
    FOREIGN KEY (department_id) REFERENCES departments(id)
);
INSERT INTO faculty_departments VALUES (1, 1, 1, 'head', '2010-08-15', 1);
INSERT INTO faculty_departments VALUES (2, 2, 2, 'head', '2012-01-10', 1);
INSERT INTO faculty_departments VALUES (3, 3, 3, 'head', '2015-08-20', 1);
INSERT INTO faculty_departments VALUES (4, 4, 4, 'head', '2008-01-05', 1);
INSERT INTO faculty_departments VALUES (5, 5, 1, 'member', '2018-08-15', 1);
INSERT INTO faculty_departments VALUES (6, 6, 2, 'member', '2020-01-10', 1);

CREATE TABLE grade_history (
    id INTEGER PRIMARY KEY,
    enrollment_id INTEGER NOT NULL,
    old_grade TEXT,
    new_grade TEXT NOT NULL,
    changed_by_id INTEGER NOT NULL,
    reason TEXT,
    changed_at TEXT NOT NULL,
    FOREIGN KEY (enrollment_id) REFERENCES enrollments(id),
    FOREIGN KEY (changed_by_id) REFERENCES faculty(id)
);
INSERT INTO grade_history VALUES (1, 1, 'A-', 'A', 1, 'Adjusted after extra credit', '2025-12-10');
INSERT INTO grade_history VALUES (2, 4, 'B-', 'B', 2, 'Regrade request approved', '2025-12-08');
INSERT INTO grade_history VALUES (3, 11, 'A-', 'A', 1, 'Curve applied', '2025-12-12');
INSERT INTO grade_history VALUES (4, 13, 'B', 'B+', 4, 'Lab grade correction', '2025-12-09');
INSERT INTO grade_history VALUES (5, 16, 'C', 'C+', 2, 'Homework resubmission', '2025-12-11');
INSERT INTO grade_history VALUES (6, 7, 'B+', 'A-', 3, 'Final essay regraded', '2025-12-13');
INSERT INTO grade_history VALUES (7, 20, 'C+', 'B-', 3, 'Participation grade updated', '2025-12-14');
INSERT INTO grade_history VALUES (8, 2, 'B+', 'A-', 2, 'Final exam curve', '2025-12-10');
INSERT INTO grade_history VALUES (9, 19, 'B-', 'B', 2, 'Attendance bonus', '2025-12-15');
INSERT INTO grade_history VALUES (10, 6, 'C+', 'B-', 1, 'Project resubmission', '2025-12-14');
""";
