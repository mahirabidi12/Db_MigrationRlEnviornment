"""Task 2 (Medium): University LMS Database — Normalize FK References & Restructure.

A university Learning Management System with 15 tables where cross-table
relationships are stored as email addresses and names instead of proper
integer FK IDs. The agent must replace all text-based references with
proper integer FKs, split student addresses into a separate table,
create a course_stats aggregate table, drop the redundant grades_log
table, and add appropriate constraints.

Initial: 15 tables, ~151 rows total, email-based references everywhere
Target:  16 tables (14 restructured + 1 new student_addresses + 1 new course_stats
         - 1 dropped grades_log)

Skills tested:
  - Replacing email/name references with integer FK IDs across many tables
  - Splitting a table (students -> students + student_addresses)
  - Creating computed aggregate tables (course_stats)
  - Adding NOT NULL, UNIQUE, DEFAULT constraints
  - Dropping redundant tables
  - Multi-table JOINs to resolve email -> id mappings
  - SQLite ALTER TABLE recreate pattern (no DROP COLUMN in SQLite)
  - Data preservation across complex restructuring

Expected steps: 40-80
"""

TASK_ID = "medium_university_lms"
TASK_DESCRIPTION = (
    "Normalize the university LMS database: "
    "(1) Replace ALL email/name-based references with proper integer FK columns "
    "across all tables by JOINing on students/faculty tables. "
    "(2) Split student addresses into a new 'student_addresses' table. "
    "(3) In 'departments', replace head_faculty_email with head_faculty_id FK. "
    "(4) In 'students', replace major_name with department_id FK and advisor_name with advisor_id FK to faculty. "
    "(5) Create a 'course_stats' table with enrollment_count, avg_grade, avg_attendance per course. "
    "(6) Drop the 'grades_log' table (redundant). "
    "(7) Add NOT NULL and UNIQUE constraints on key columns. "
    "Preserve all data with referential integrity."
)
DIFFICULTY = "medium"
MAX_STEPS = 120

INITIAL_SQL = """
CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    phone TEXT,
    dob TEXT,
    enrollment_date TEXT,
    major_name TEXT,
    advisor_name TEXT,
    gpa REAL,
    status TEXT,
    address_line1 TEXT,
    address_city TEXT,
    address_state TEXT,
    address_zip TEXT
);
INSERT INTO students VALUES (1, 'Alice', 'Wang', 'alice@uni.edu', '555-1001', '2002-03-15', '2022-08-20', 'Computer Science', 'Dr. Roberts', 3.7, 'active', '100 Elm St', 'Boston', 'MA', '02101');
INSERT INTO students VALUES (2, 'Bob', 'Patel', 'bob@uni.edu', '555-1002', '2001-07-22', '2021-08-18', 'Mathematics', 'Dr. Chen', 3.0, 'active', '200 Oak Ave', 'Cambridge', 'MA', '02139');
INSERT INTO students VALUES (3, 'Carol', 'Lopez', 'carol@uni.edu', '555-1003', '2003-11-05', '2023-08-21', 'English', 'Dr. Miller', 3.4, 'active', '300 Pine Rd', 'Somerville', 'MA', '02143');
INSERT INTO students VALUES (4, 'Dave', 'Kim', 'dave@uni.edu', '555-1004', '2000-01-30', '2020-08-17', 'Computer Science', 'Dr. Roberts', 3.8, 'active', '400 Maple Dr', 'Brookline', 'MA', '02445');
INSERT INTO students VALUES (5, 'Eve', 'Tanaka', 'eve@uni.edu', '555-1005', '2002-09-12', '2022-08-20', 'Physics', 'Dr. Adams', 3.2, 'active', '500 Cedar Ln', 'Newton', 'MA', '02458');
INSERT INTO students VALUES (6, 'Frank', 'Russo', 'frank@uni.edu', '555-1006', '2001-04-18', '2021-08-18', 'Mathematics', 'Dr. Chen', 2.7, 'probation', '600 Birch Ct', 'Medford', 'MA', '02155');
INSERT INTO students VALUES (7, 'Grace', 'Okafor', 'grace@uni.edu', '555-1007', '2003-06-25', '2023-08-21', 'Physics', 'Dr. Adams', 3.5, 'active', '700 Walnut St', 'Arlington', 'MA', '02474');
INSERT INTO students VALUES (8, 'Hiro', 'Sato', 'hiro@uni.edu', '555-1008', '2002-12-01', '2022-08-20', 'English', 'Dr. Miller', 2.9, 'active', '800 Spruce Ave', 'Belmont', 'MA', '02478');

CREATE TABLE faculty (
    id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    phone TEXT,
    hire_date TEXT,
    department_name TEXT,
    title TEXT,
    office_room TEXT,
    office_building TEXT,
    salary REAL,
    tenure_status TEXT
);
INSERT INTO faculty VALUES (1, 'James', 'Roberts', 'roberts@uni.edu', '555-2001', '2010-08-15', 'Computer Science', 'Professor', '301', 'Science Hall', 120000.00, 'tenured');
INSERT INTO faculty VALUES (2, 'Li', 'Chen', 'chen@uni.edu', '555-2002', '2012-01-10', 'Mathematics', 'Associate Professor', '205', 'Math Building', 105000.00, 'tenured');
INSERT INTO faculty VALUES (3, 'Sarah', 'Miller', 'miller@uni.edu', '555-2003', '2015-08-20', 'English', 'Assistant Professor', '110', 'Humanities Hall', 85000.00, 'tenure-track');
INSERT INTO faculty VALUES (4, 'Raj', 'Adams', 'adams@uni.edu', '555-2004', '2008-01-05', 'Physics', 'Professor', '402', 'Science Hall', 125000.00, 'tenured');
INSERT INTO faculty VALUES (5, 'Maria', 'Garcia', 'garcia@uni.edu', '555-2005', '2018-08-15', 'Computer Science', 'Lecturer', '303', 'Science Hall', 72000.00, 'non-tenure');
INSERT INTO faculty VALUES (6, 'Tom', 'Wilson', 'wilson@uni.edu', '555-2006', '2020-01-10', 'Mathematics', 'Lecturer', '207', 'Math Building', 68000.00, 'non-tenure');

CREATE TABLE courses (
    id INTEGER PRIMARY KEY,
    code TEXT,
    name TEXT,
    description TEXT,
    credits INTEGER,
    department_name TEXT,
    instructor_email TEXT,
    max_capacity INTEGER,
    current_enrollment INTEGER,
    semester TEXT,
    year INTEGER,
    room_number TEXT
);
INSERT INTO courses VALUES (1, 'CS101', 'Intro to Programming', 'Learn basic programming concepts', 4, 'Computer Science', 'roberts@uni.edu', 40, 30, 'Fall', 2025, 'SH-101');
INSERT INTO courses VALUES (2, 'CS201', 'Data Structures', 'Advanced data structures and algorithms', 4, 'Computer Science', 'roberts@uni.edu', 35, 25, 'Fall', 2025, 'SH-102');
INSERT INTO courses VALUES (3, 'MATH101', 'Calculus I', 'Introduction to differential calculus', 4, 'Mathematics', 'chen@uni.edu', 45, 35, 'Fall', 2025, 'MB-201');
INSERT INTO courses VALUES (4, 'MATH201', 'Linear Algebra', 'Vectors, matrices, and linear transformations', 3, 'Mathematics', 'chen@uni.edu', 40, 28, 'Fall', 2025, 'MB-202');
INSERT INTO courses VALUES (5, 'ENG101', 'English Composition', 'Academic writing fundamentals', 3, 'English', 'miller@uni.edu', 30, 25, 'Fall', 2025, 'HH-101');
INSERT INTO courses VALUES (6, 'ENG201', 'American Literature', 'Survey of American literary works', 3, 'English', 'miller@uni.edu', 30, 20, 'Fall', 2025, 'HH-102');
INSERT INTO courses VALUES (7, 'PHYS101', 'Physics I', 'Mechanics and thermodynamics', 4, 'Physics', 'adams@uni.edu', 40, 32, 'Fall', 2025, 'SH-201');
INSERT INTO courses VALUES (8, 'PHYS201', 'Physics II', 'Electricity and magnetism', 4, 'Physics', 'adams@uni.edu', 35, 22, 'Fall', 2025, 'SH-202');
INSERT INTO courses VALUES (9, 'CS301', 'Database Systems', 'Relational databases and SQL', 3, 'Computer Science', 'garcia@uni.edu', 30, 20, 'Fall', 2025, 'SH-103');
INSERT INTO courses VALUES (10, 'MATH301', 'Probability & Stats', 'Intro to probability and statistics', 3, 'Mathematics', 'wilson@uni.edu', 35, 30, 'Fall', 2025, 'MB-301');

CREATE TABLE enrollments (
    id INTEGER PRIMARY KEY,
    student_email TEXT,
    course_code TEXT,
    grade TEXT,
    grade_points REAL,
    enrollment_date TEXT,
    status TEXT,
    midterm_score REAL,
    final_score REAL,
    attendance_pct REAL,
    notes TEXT
);
INSERT INTO enrollments VALUES (1, 'alice@uni.edu', 'CS101', 'A', 4.0, '2025-08-25', 'completed', 92.0, 95.0, 96.0, 'Excellent work');
INSERT INTO enrollments VALUES (2, 'alice@uni.edu', 'MATH101', 'A-', 3.7, '2025-08-25', 'completed', 88.0, 91.0, 94.0, NULL);
INSERT INTO enrollments VALUES (3, 'alice@uni.edu', 'ENG101', 'A', 4.0, '2025-08-25', 'completed', 95.0, 93.0, 98.0, 'Strong writer');
INSERT INTO enrollments VALUES (4, 'bob@uni.edu', 'MATH101', 'B', 3.0, '2025-08-25', 'completed', 78.0, 82.0, 88.0, NULL);
INSERT INTO enrollments VALUES (5, 'bob@uni.edu', 'MATH201', 'B+', 3.3, '2025-08-25', 'completed', 80.0, 85.0, 90.0, NULL);
INSERT INTO enrollments VALUES (6, 'bob@uni.edu', 'CS201', 'B-', 2.7, '2025-08-25', 'completed', 75.0, 78.0, 85.0, 'Needs improvement in recursion');
INSERT INTO enrollments VALUES (7, 'carol@uni.edu', 'ENG101', 'A-', 3.7, '2025-08-25', 'completed', 90.0, 88.0, 95.0, NULL);
INSERT INTO enrollments VALUES (8, 'carol@uni.edu', 'ENG201', NULL, NULL, '2025-08-25', 'enrolled', NULL, NULL, 80.0, 'In progress');
INSERT INTO enrollments VALUES (9, 'carol@uni.edu', 'PHYS101', 'B+', 3.3, '2025-08-25', 'completed', 82.0, 86.0, 91.0, NULL);
INSERT INTO enrollments VALUES (10, 'dave@uni.edu', 'CS101', 'A', 4.0, '2025-08-25', 'completed', 96.0, 98.0, 99.0, 'Top student');
INSERT INTO enrollments VALUES (11, 'dave@uni.edu', 'CS201', 'A', 4.0, '2025-08-25', 'completed', 94.0, 96.0, 97.0, NULL);
INSERT INTO enrollments VALUES (12, 'dave@uni.edu', 'CS301', 'A-', 3.7, '2025-08-25', 'completed', 90.0, 92.0, 95.0, NULL);
INSERT INTO enrollments VALUES (13, 'eve@uni.edu', 'PHYS101', 'B+', 3.3, '2025-08-25', 'completed', 84.0, 87.0, 92.0, NULL);
INSERT INTO enrollments VALUES (14, 'eve@uni.edu', 'PHYS201', 'B', 3.0, '2025-08-25', 'completed', 79.0, 81.0, 88.0, NULL);
INSERT INTO enrollments VALUES (15, 'eve@uni.edu', 'MATH101', 'B+', 3.3, '2025-08-25', 'completed', 83.0, 86.0, 90.0, NULL);
INSERT INTO enrollments VALUES (16, 'frank@uni.edu', 'MATH101', 'C+', 2.3, '2025-08-25', 'completed', 68.0, 72.0, 75.0, 'Attendance issues');
INSERT INTO enrollments VALUES (17, 'frank@uni.edu', 'MATH201', 'C', 2.0, '2025-08-25', 'completed', 65.0, 70.0, 72.0, NULL);
INSERT INTO enrollments VALUES (18, 'grace@uni.edu', 'PHYS101', NULL, NULL, '2025-08-25', 'enrolled', NULL, NULL, 85.0, 'In progress');
INSERT INTO enrollments VALUES (19, 'grace@uni.edu', 'MATH101', 'B', 3.0, '2025-08-25', 'completed', 80.0, 83.0, 89.0, NULL);
INSERT INTO enrollments VALUES (20, 'hiro@uni.edu', 'ENG101', 'B-', 2.7, '2025-08-25', 'completed', 74.0, 77.0, 82.0, NULL);

CREATE TABLE departments (
    id INTEGER PRIMARY KEY,
    name TEXT,
    code TEXT,
    building TEXT,
    floor INTEGER,
    phone TEXT,
    head_faculty_email TEXT,
    budget REAL,
    founded_year INTEGER,
    description TEXT
);
INSERT INTO departments VALUES (1, 'Computer Science', 'CS', 'Science Hall', 3, '555-3001', 'roberts@uni.edu', 2500000.00, 1985, 'Department of Computer Science and Engineering');
INSERT INTO departments VALUES (2, 'Mathematics', 'MATH', 'Math Building', 2, '555-3002', 'chen@uni.edu', 1800000.00, 1920, 'Department of Mathematics and Applied Mathematics');
INSERT INTO departments VALUES (3, 'English', 'ENG', 'Humanities Hall', 1, '555-3003', 'miller@uni.edu', 1200000.00, 1900, 'Department of English Language and Literature');
INSERT INTO departments VALUES (4, 'Physics', 'PHYS', 'Science Hall', 4, '555-3004', 'adams@uni.edu', 2200000.00, 1935, 'Department of Physics and Astronomy');

CREATE TABLE assignments (
    id INTEGER PRIMARY KEY,
    course_code TEXT,
    title TEXT,
    description TEXT,
    due_date TEXT,
    max_points REAL,
    weight_pct REAL,
    assignment_type TEXT,
    is_published INTEGER,
    created_by_email TEXT,
    created_at TEXT
);
INSERT INTO assignments VALUES (1, 'CS101', 'Hello World Program', 'Write your first program in Python', '2025-09-15', 100.0, 5.0, 'homework', 1, 'roberts@uni.edu', '2025-08-25');
INSERT INTO assignments VALUES (2, 'CS101', 'Midterm Exam', 'Covers chapters 1-6', '2025-10-15', 200.0, 25.0, 'exam', 1, 'roberts@uni.edu', '2025-08-25');
INSERT INTO assignments VALUES (3, 'CS201', 'Linked List Implementation', 'Implement singly and doubly linked lists', '2025-09-20', 100.0, 10.0, 'homework', 1, 'roberts@uni.edu', '2025-08-26');
INSERT INTO assignments VALUES (4, 'MATH101', 'Problem Set 1', 'Limits and continuity exercises', '2025-09-10', 50.0, 5.0, 'homework', 1, 'chen@uni.edu', '2025-08-25');
INSERT INTO assignments VALUES (5, 'MATH101', 'Midterm Exam', 'Chapters 1-4', '2025-10-12', 100.0, 30.0, 'exam', 1, 'chen@uni.edu', '2025-08-25');
INSERT INTO assignments VALUES (6, 'ENG101', 'Personal Essay', 'Write a 5-page personal narrative', '2025-09-18', 100.0, 15.0, 'essay', 1, 'miller@uni.edu', '2025-08-25');
INSERT INTO assignments VALUES (7, 'ENG101', 'Research Paper Draft', 'First draft of research paper', '2025-10-20', 100.0, 10.0, 'essay', 1, 'miller@uni.edu', '2025-08-26');
INSERT INTO assignments VALUES (8, 'PHYS101', 'Lab Report 1', 'Kinematics experiment report', '2025-09-12', 50.0, 5.0, 'lab', 1, 'adams@uni.edu', '2025-08-25');
INSERT INTO assignments VALUES (9, 'PHYS101', 'Midterm Exam', 'Mechanics chapters 1-5', '2025-10-14', 150.0, 25.0, 'exam', 1, 'adams@uni.edu', '2025-08-25');
INSERT INTO assignments VALUES (10, 'CS301', 'SQL Exercises', 'Practice SELECT, JOIN, and subqueries', '2025-09-22', 80.0, 8.0, 'homework', 1, 'garcia@uni.edu', '2025-08-27');
INSERT INTO assignments VALUES (11, 'MATH201', 'Matrix Operations', 'Solve systems of linear equations', '2025-09-16', 60.0, 8.0, 'homework', 1, 'chen@uni.edu', '2025-08-26');
INSERT INTO assignments VALUES (12, 'PHYS201', 'Coulombs Law Problems', 'Electric force calculations', '2025-09-19', 70.0, 7.0, 'homework', 1, 'adams@uni.edu', '2025-08-26');

CREATE TABLE submissions (
    id INTEGER PRIMARY KEY,
    assignment_id INTEGER,
    student_email TEXT,
    submitted_at TEXT,
    file_url TEXT,
    score REAL,
    feedback TEXT,
    is_late INTEGER,
    graded_by_email TEXT,
    graded_at TEXT,
    status TEXT
);
INSERT INTO submissions VALUES (1, 1, 'alice@uni.edu', '2025-09-14 23:30:00', '/files/alice_hw1.py', 95.0, 'Great job!', 0, 'roberts@uni.edu', '2025-09-16', 'graded');
INSERT INTO submissions VALUES (2, 1, 'dave@uni.edu', '2025-09-14 20:00:00', '/files/dave_hw1.py', 100.0, 'Perfect', 0, 'roberts@uni.edu', '2025-09-16', 'graded');
INSERT INTO submissions VALUES (3, 2, 'alice@uni.edu', '2025-10-15 10:00:00', '/files/alice_midterm.pdf', 92.0, NULL, 0, 'roberts@uni.edu', '2025-10-18', 'graded');
INSERT INTO submissions VALUES (4, 2, 'dave@uni.edu', '2025-10-15 10:00:00', '/files/dave_midterm.pdf', 96.0, 'Excellent', 0, 'roberts@uni.edu', '2025-10-18', 'graded');
INSERT INTO submissions VALUES (5, 3, 'bob@uni.edu', '2025-09-21 08:00:00', '/files/bob_ll.zip', 72.0, 'Missing edge cases', 1, 'roberts@uni.edu', '2025-09-23', 'graded');
INSERT INTO submissions VALUES (6, 3, 'dave@uni.edu', '2025-09-19 18:00:00', '/files/dave_ll.zip', 98.0, 'Excellent implementation', 0, 'roberts@uni.edu', '2025-09-23', 'graded');
INSERT INTO submissions VALUES (7, 4, 'alice@uni.edu', '2025-09-09 22:00:00', '/files/alice_ps1.pdf', 45.0, NULL, 0, 'chen@uni.edu', '2025-09-12', 'graded');
INSERT INTO submissions VALUES (8, 4, 'bob@uni.edu', '2025-09-10 01:00:00', '/files/bob_ps1.pdf', 38.0, 'Review limits section', 1, 'chen@uni.edu', '2025-09-12', 'graded');
INSERT INTO submissions VALUES (9, 4, 'eve@uni.edu', '2025-09-09 20:00:00', '/files/eve_ps1.pdf', 42.0, NULL, 0, 'chen@uni.edu', '2025-09-12', 'graded');
INSERT INTO submissions VALUES (10, 6, 'alice@uni.edu', '2025-09-17 15:00:00', '/files/alice_essay.docx', 93.0, 'Beautiful prose', 0, 'miller@uni.edu', '2025-09-20', 'graded');
INSERT INTO submissions VALUES (11, 6, 'carol@uni.edu', '2025-09-18 09:00:00', '/files/carol_essay.docx', 90.0, 'Strong voice', 0, 'miller@uni.edu', '2025-09-20', 'graded');
INSERT INTO submissions VALUES (12, 6, 'hiro@uni.edu', '2025-09-19 11:00:00', '/files/hiro_essay.docx', 74.0, 'Needs more detail', 1, 'miller@uni.edu', '2025-09-20', 'graded');
INSERT INTO submissions VALUES (13, 8, 'eve@uni.edu', '2025-09-12 14:00:00', '/files/eve_lab1.pdf', 44.0, NULL, 0, 'adams@uni.edu', '2025-09-15', 'graded');
INSERT INTO submissions VALUES (14, 8, 'carol@uni.edu', '2025-09-12 16:00:00', '/files/carol_lab1.pdf', 46.0, 'Good analysis', 0, 'adams@uni.edu', '2025-09-15', 'graded');
INSERT INTO submissions VALUES (15, 10, 'dave@uni.edu', '2025-09-21 22:00:00', '/files/dave_sql.sql', 78.0, 'Good joins', 0, 'garcia@uni.edu', '2025-09-24', 'graded');

CREATE TABLE announcements (
    id INTEGER PRIMARY KEY,
    course_code TEXT,
    author_email TEXT,
    title TEXT,
    body TEXT,
    priority TEXT,
    is_pinned INTEGER,
    created_at TEXT,
    updated_at TEXT,
    expiry_date TEXT
);
INSERT INTO announcements VALUES (1, 'CS101', 'roberts@uni.edu', 'Welcome to CS101', 'Please review the syllabus before first class.', 'high', 1, '2025-08-20', '2025-08-20', '2025-09-01');
INSERT INTO announcements VALUES (2, 'CS101', 'roberts@uni.edu', 'Office Hours Change', 'Office hours moved to Thursdays 2-4pm.', 'normal', 0, '2025-09-05', '2025-09-05', '2025-12-15');
INSERT INTO announcements VALUES (3, 'MATH101', 'chen@uni.edu', 'Textbook Required', 'Please purchase Stewart Calculus 9th edition.', 'high', 1, '2025-08-21', '2025-08-21', '2025-09-10');
INSERT INTO announcements VALUES (4, 'ENG101', 'miller@uni.edu', 'Essay Guidelines', 'All essays must follow MLA format.', 'normal', 1, '2025-08-22', '2025-08-22', '2025-12-15');
INSERT INTO announcements VALUES (5, 'PHYS101', 'adams@uni.edu', 'Lab Safety Training', 'Mandatory safety training on Sept 5.', 'high', 0, '2025-08-28', '2025-08-28', '2025-09-05');
INSERT INTO announcements VALUES (6, 'CS201', 'roberts@uni.edu', 'Prerequisites Reminder', 'CS101 is a prerequisite for this course.', 'normal', 0, '2025-08-20', '2025-08-20', '2025-09-01');
INSERT INTO announcements VALUES (7, 'CS301', 'garcia@uni.edu', 'Software Installation', 'Install PostgreSQL and SQLite before Week 2.', 'high', 1, '2025-08-25', '2025-08-25', '2025-09-08');
INSERT INTO announcements VALUES (8, 'MATH201', 'chen@uni.edu', 'Study Group Formation', 'Form study groups of 3-4 students.', 'normal', 0, '2025-09-01', '2025-09-01', '2025-12-15');

CREATE TABLE attendance (
    id INTEGER PRIMARY KEY,
    course_code TEXT,
    student_email TEXT,
    session_date TEXT,
    status TEXT,
    check_in_time TEXT,
    check_out_time TEXT,
    duration_min INTEGER,
    notes TEXT,
    recorded_by_email TEXT
);
INSERT INTO attendance VALUES (1, 'CS101', 'alice@uni.edu', '2025-09-02', 'present', '09:00', '10:15', 75, NULL, 'roberts@uni.edu');
INSERT INTO attendance VALUES (2, 'CS101', 'dave@uni.edu', '2025-09-02', 'present', '08:58', '10:15', 77, NULL, 'roberts@uni.edu');
INSERT INTO attendance VALUES (3, 'CS101', 'alice@uni.edu', '2025-09-04', 'present', '09:02', '10:15', 73, NULL, 'roberts@uni.edu');
INSERT INTO attendance VALUES (4, 'CS101', 'dave@uni.edu', '2025-09-04', 'late', '09:20', '10:15', 55, 'Arrived 20 min late', 'roberts@uni.edu');
INSERT INTO attendance VALUES (5, 'MATH101', 'alice@uni.edu', '2025-09-03', 'present', '10:00', '11:15', 75, NULL, 'chen@uni.edu');
INSERT INTO attendance VALUES (6, 'MATH101', 'bob@uni.edu', '2025-09-03', 'present', '10:05', '11:15', 70, NULL, 'chen@uni.edu');
INSERT INTO attendance VALUES (7, 'MATH101', 'eve@uni.edu', '2025-09-03', 'present', '10:00', '11:15', 75, NULL, 'chen@uni.edu');
INSERT INTO attendance VALUES (8, 'MATH101', 'frank@uni.edu', '2025-09-03', 'absent', NULL, NULL, 0, 'No show', 'chen@uni.edu');
INSERT INTO attendance VALUES (9, 'ENG101', 'alice@uni.edu', '2025-09-02', 'present', '13:00', '14:15', 75, NULL, 'miller@uni.edu');
INSERT INTO attendance VALUES (10, 'ENG101', 'carol@uni.edu', '2025-09-02', 'present', '13:00', '14:15', 75, NULL, 'miller@uni.edu');
INSERT INTO attendance VALUES (11, 'ENG101', 'hiro@uni.edu', '2025-09-02', 'late', '13:15', '14:15', 60, 'Arrived late', 'miller@uni.edu');
INSERT INTO attendance VALUES (12, 'PHYS101', 'eve@uni.edu', '2025-09-03', 'present', '14:00', '15:30', 90, NULL, 'adams@uni.edu');
INSERT INTO attendance VALUES (13, 'PHYS101', 'carol@uni.edu', '2025-09-03', 'present', '14:00', '15:30', 90, NULL, 'adams@uni.edu');
INSERT INTO attendance VALUES (14, 'PHYS101', 'grace@uni.edu', '2025-09-03', 'present', '14:02', '15:30', 88, NULL, 'adams@uni.edu');
INSERT INTO attendance VALUES (15, 'CS201', 'bob@uni.edu', '2025-09-02', 'present', '11:00', '12:15', 75, NULL, 'roberts@uni.edu');
INSERT INTO attendance VALUES (16, 'CS201', 'dave@uni.edu', '2025-09-02', 'present', '11:00', '12:15', 75, NULL, 'roberts@uni.edu');
INSERT INTO attendance VALUES (17, 'CS301', 'dave@uni.edu', '2025-09-04', 'present', '15:00', '16:15', 75, NULL, 'garcia@uni.edu');
INSERT INTO attendance VALUES (18, 'MATH201', 'bob@uni.edu', '2025-09-04', 'present', '10:00', '11:15', 75, NULL, 'chen@uni.edu');

CREATE TABLE grades_log (
    id INTEGER PRIMARY KEY,
    student_email TEXT,
    course_code TEXT,
    old_grade TEXT,
    new_grade TEXT,
    changed_by_email TEXT,
    change_reason TEXT,
    changed_at TEXT,
    semester TEXT,
    year INTEGER,
    is_final INTEGER
);
INSERT INTO grades_log VALUES (1, 'alice@uni.edu', 'CS101', 'A-', 'A', 'roberts@uni.edu', 'Adjusted after extra credit', '2025-12-10', 'Fall', 2025, 1);
INSERT INTO grades_log VALUES (2, 'bob@uni.edu', 'MATH101', 'B-', 'B', 'chen@uni.edu', 'Regrade request approved', '2025-12-08', 'Fall', 2025, 1);
INSERT INTO grades_log VALUES (3, 'dave@uni.edu', 'CS201', 'A-', 'A', 'roberts@uni.edu', 'Curve applied', '2025-12-12', 'Fall', 2025, 1);
INSERT INTO grades_log VALUES (4, 'eve@uni.edu', 'PHYS101', 'B', 'B+', 'adams@uni.edu', 'Lab grade correction', '2025-12-09', 'Fall', 2025, 1);
INSERT INTO grades_log VALUES (5, 'frank@uni.edu', 'MATH101', 'C', 'C+', 'chen@uni.edu', 'Homework resubmission', '2025-12-11', 'Fall', 2025, 1);
INSERT INTO grades_log VALUES (6, 'carol@uni.edu', 'ENG101', 'B+', 'A-', 'miller@uni.edu', 'Final essay regraded', '2025-12-13', 'Fall', 2025, 1);
INSERT INTO grades_log VALUES (7, 'hiro@uni.edu', 'ENG101', 'C+', 'B-', 'miller@uni.edu', 'Participation grade updated', '2025-12-14', 'Fall', 2025, 1);
INSERT INTO grades_log VALUES (8, 'alice@uni.edu', 'MATH101', 'B+', 'A-', 'chen@uni.edu', 'Final exam curve', '2025-12-10', 'Fall', 2025, 1);
INSERT INTO grades_log VALUES (9, 'grace@uni.edu', 'MATH101', 'B-', 'B', 'chen@uni.edu', 'Attendance bonus', '2025-12-15', 'Fall', 2025, 1);
INSERT INTO grades_log VALUES (10, 'bob@uni.edu', 'CS201', 'C+', 'B-', 'roberts@uni.edu', 'Project resubmission', '2025-12-14', 'Fall', 2025, 1);

CREATE TABLE course_materials (
    id INTEGER PRIMARY KEY,
    course_code TEXT,
    title TEXT,
    file_url TEXT,
    file_type TEXT,
    file_size INTEGER,
    uploaded_by_email TEXT,
    description TEXT,
    download_count INTEGER,
    is_visible INTEGER,
    uploaded_at TEXT
);
INSERT INTO course_materials VALUES (1, 'CS101', 'Syllabus', '/materials/cs101_syllabus.pdf', 'pdf', 245000, 'roberts@uni.edu', 'Course syllabus and schedule', 45, 1, '2025-08-15');
INSERT INTO course_materials VALUES (2, 'CS101', 'Lecture 1 Slides', '/materials/cs101_lec1.pptx', 'pptx', 1200000, 'roberts@uni.edu', 'Introduction to programming', 38, 1, '2025-09-01');
INSERT INTO course_materials VALUES (3, 'MATH101', 'Formula Sheet', '/materials/math101_formulas.pdf', 'pdf', 120000, 'chen@uni.edu', 'Key formulas for calculus', 52, 1, '2025-08-20');
INSERT INTO course_materials VALUES (4, 'MATH101', 'Practice Problems', '/materials/math101_practice.pdf', 'pdf', 350000, 'chen@uni.edu', 'Extra practice for midterm', 30, 1, '2025-10-01');
INSERT INTO course_materials VALUES (5, 'ENG101', 'Style Guide', '/materials/eng101_style.pdf', 'pdf', 180000, 'miller@uni.edu', 'MLA formatting guide', 40, 1, '2025-08-18');
INSERT INTO course_materials VALUES (6, 'ENG101', 'Essay Rubric', '/materials/eng101_rubric.pdf', 'pdf', 95000, 'miller@uni.edu', 'Grading criteria for essays', 35, 1, '2025-08-18');
INSERT INTO course_materials VALUES (7, 'PHYS101', 'Lab Manual', '/materials/phys101_lab.pdf', 'pdf', 2500000, 'adams@uni.edu', 'Complete lab manual', 48, 1, '2025-08-16');
INSERT INTO course_materials VALUES (8, 'CS201', 'Big-O Cheatsheet', '/materials/cs201_bigo.pdf', 'pdf', 85000, 'roberts@uni.edu', 'Time complexity reference', 28, 1, '2025-09-05');
INSERT INTO course_materials VALUES (9, 'CS301', 'SQL Reference', '/materials/cs301_sql.pdf', 'pdf', 310000, 'garcia@uni.edu', 'SQL syntax quick reference', 22, 1, '2025-08-28');
INSERT INTO course_materials VALUES (10, 'PHYS201', 'Maxwells Equations', '/materials/phys201_maxwell.pdf', 'pdf', 200000, 'adams@uni.edu', 'Summary of electromagnetic theory', 18, 1, '2025-08-22');

CREATE TABLE discussion_posts (
    id INTEGER PRIMARY KEY,
    course_code TEXT,
    author_email TEXT,
    title TEXT,
    body TEXT,
    parent_post_id INTEGER,
    likes_count INTEGER,
    is_pinned INTEGER,
    is_anonymous INTEGER,
    created_at TEXT,
    updated_at TEXT
);
INSERT INTO discussion_posts VALUES (1, 'CS101', 'alice@uni.edu', 'Help with HW1', 'I am stuck on the loop exercise. Any tips?', NULL, 3, 0, 0, '2025-09-10', '2025-09-10');
INSERT INTO discussion_posts VALUES (2, 'CS101', 'dave@uni.edu', 'Re: Help with HW1', 'Try using a while loop instead of for.', 1, 5, 0, 0, '2025-09-10', '2025-09-10');
INSERT INTO discussion_posts VALUES (3, 'CS101', 'roberts@uni.edu', 'Re: Help with HW1', 'Good suggestion Dave. Also review chapter 3.', 1, 2, 0, 0, '2025-09-11', '2025-09-11');
INSERT INTO discussion_posts VALUES (4, 'MATH101', 'bob@uni.edu', 'Limit Problem Clarification', 'Can someone explain L Hopitals rule with an example?', NULL, 4, 0, 0, '2025-09-15', '2025-09-15');
INSERT INTO discussion_posts VALUES (5, 'MATH101', 'chen@uni.edu', 'Re: Limit Problem', 'See the attached example from lecture 5.', 4, 6, 0, 0, '2025-09-15', '2025-09-15');
INSERT INTO discussion_posts VALUES (6, 'ENG101', 'carol@uni.edu', 'MLA Citation Question', 'How do I cite an online article in MLA?', NULL, 2, 0, 0, '2025-09-12', '2025-09-12');
INSERT INTO discussion_posts VALUES (7, 'ENG101', 'miller@uni.edu', 'Re: MLA Citation', 'Use the format: Author. Title. Website, Date, URL.', 6, 4, 0, 0, '2025-09-12', '2025-09-12');
INSERT INTO discussion_posts VALUES (8, 'PHYS101', 'eve@uni.edu', 'Lab Partner Needed', 'Looking for a lab partner for Thursday sessions.', NULL, 1, 0, 0, '2025-09-08', '2025-09-08');
INSERT INTO discussion_posts VALUES (9, 'PHYS101', 'grace@uni.edu', 'Re: Lab Partner', 'I am available! Send me an email.', 8, 1, 0, 0, '2025-09-08', '2025-09-08');
INSERT INTO discussion_posts VALUES (10, 'CS301', 'dave@uni.edu', 'JOIN vs Subquery', 'When should I prefer JOIN over subquery?', NULL, 7, 0, 0, '2025-09-20', '2025-09-20');

CREATE TABLE office_hours (
    id INTEGER PRIMARY KEY,
    faculty_email TEXT,
    day_of_week TEXT,
    start_time TEXT,
    end_time TEXT,
    location TEXT,
    is_virtual INTEGER,
    meeting_url TEXT,
    max_students INTEGER,
    semester TEXT,
    year INTEGER
);
INSERT INTO office_hours VALUES (1, 'roberts@uni.edu', 'Tuesday', '14:00', '16:00', 'SH-301', 0, NULL, 5, 'Fall', 2025);
INSERT INTO office_hours VALUES (2, 'roberts@uni.edu', 'Thursday', '14:00', '16:00', 'SH-301', 0, NULL, 5, 'Fall', 2025);
INSERT INTO office_hours VALUES (3, 'chen@uni.edu', 'Monday', '10:00', '12:00', 'MB-205', 0, NULL, 4, 'Fall', 2025);
INSERT INTO office_hours VALUES (4, 'chen@uni.edu', 'Wednesday', '10:00', '12:00', NULL, 1, 'https://zoom.us/chen123', 6, 'Fall', 2025);
INSERT INTO office_hours VALUES (5, 'miller@uni.edu', 'Tuesday', '11:00', '12:30', 'HH-110', 0, NULL, 3, 'Fall', 2025);
INSERT INTO office_hours VALUES (6, 'adams@uni.edu', 'Friday', '13:00', '15:00', 'SH-402', 0, NULL, 4, 'Fall', 2025);
INSERT INTO office_hours VALUES (7, 'garcia@uni.edu', 'Wednesday', '15:00', '17:00', NULL, 1, 'https://zoom.us/garcia456', 5, 'Fall', 2025);
INSERT INTO office_hours VALUES (8, 'wilson@uni.edu', 'Thursday', '09:00', '11:00', 'MB-207', 0, NULL, 4, 'Fall', 2025);

CREATE TABLE student_clubs (
    id INTEGER PRIMARY KEY,
    name TEXT,
    description TEXT,
    faculty_advisor_email TEXT,
    president_email TEXT,
    founded_date TEXT,
    meeting_day TEXT,
    meeting_room TEXT,
    budget REAL,
    is_active INTEGER,
    member_count INTEGER
);
INSERT INTO student_clubs VALUES (1, 'Coding Club', 'Learn programming and compete in hackathons', 'roberts@uni.edu', 'dave@uni.edu', '2018-09-01', 'Friday', 'SH-105', 3000.00, 1, 25);
INSERT INTO student_clubs VALUES (2, 'Math Society', 'Explore mathematics beyond the classroom', 'chen@uni.edu', 'alice@uni.edu', '2015-09-01', 'Wednesday', 'MB-101', 1500.00, 1, 15);
INSERT INTO student_clubs VALUES (3, 'Literary Circle', 'Book club and creative writing group', 'miller@uni.edu', 'carol@uni.edu', '2010-09-01', 'Tuesday', 'HH-105', 1000.00, 1, 12);
INSERT INTO student_clubs VALUES (4, 'Physics Society', 'Demos experiments and physics outreach', 'adams@uni.edu', 'eve@uni.edu', '2012-09-01', 'Thursday', 'SH-210', 2000.00, 1, 18);
INSERT INTO student_clubs VALUES (5, 'Debate Team', 'Competitive debate and public speaking', 'miller@uni.edu', 'bob@uni.edu', '2005-09-01', 'Monday', 'HH-201', 2500.00, 1, 20);

CREATE TABLE library_loans (
    id INTEGER PRIMARY KEY,
    student_email TEXT,
    book_title TEXT,
    isbn TEXT,
    loan_date TEXT,
    due_date TEXT,
    return_date TEXT,
    fine_amount REAL,
    status TEXT,
    library_branch TEXT,
    processed_by TEXT
);
INSERT INTO library_loans VALUES (1, 'alice@uni.edu', 'Introduction to Algorithms', '978-0262033848', '2025-09-01', '2025-09-29', '2025-09-28', 0.00, 'returned', 'Main Library', 'Librarian Jones');
INSERT INTO library_loans VALUES (2, 'alice@uni.edu', 'Clean Code', '978-0132350884', '2025-09-15', '2025-10-13', '2025-10-10', 0.00, 'returned', 'Main Library', 'Librarian Smith');
INSERT INTO library_loans VALUES (3, 'bob@uni.edu', 'Stewart Calculus', '978-1285740621', '2025-09-02', '2025-09-30', '2025-10-05', 2.50, 'returned', 'Main Library', 'Librarian Jones');
INSERT INTO library_loans VALUES (4, 'bob@uni.edu', 'Linear Algebra Done Right', '978-3319110790', '2025-09-10', '2025-10-08', NULL, 5.00, 'overdue', 'Science Branch', 'Librarian Davis');
INSERT INTO library_loans VALUES (5, 'carol@uni.edu', 'The Elements of Style', '978-0205309023', '2025-09-05', '2025-10-03', '2025-09-30', 0.00, 'returned', 'Humanities Branch', 'Librarian Wilson');
INSERT INTO library_loans VALUES (6, 'dave@uni.edu', 'Database System Concepts', '978-0078022159', '2025-09-08', '2025-10-06', '2025-10-01', 0.00, 'returned', 'Science Branch', 'Librarian Davis');
INSERT INTO library_loans VALUES (7, 'dave@uni.edu', 'The Art of Computer Programming', '978-0201896831', '2025-10-01', '2025-10-29', NULL, 0.00, 'active', 'Main Library', 'Librarian Jones');
INSERT INTO library_loans VALUES (8, 'eve@uni.edu', 'University Physics', '978-0133969290', '2025-09-03', '2025-10-01', '2025-09-29', 0.00, 'returned', 'Science Branch', 'Librarian Davis');
INSERT INTO library_loans VALUES (9, 'frank@uni.edu', 'Principles of Mathematical Analysis', '978-0070856134', '2025-09-12', '2025-10-10', NULL, 3.00, 'overdue', 'Main Library', 'Librarian Smith');
INSERT INTO library_loans VALUES (10, 'grace@uni.edu', 'Feynman Lectures on Physics', '978-0465023820', '2025-09-15', '2025-10-13', '2025-10-12', 0.00, 'returned', 'Science Branch', 'Librarian Davis');
INSERT INTO library_loans VALUES (11, 'hiro@uni.edu', 'On Writing Well', '978-0060891541', '2025-09-08', '2025-10-06', '2025-10-06', 0.00, 'returned', 'Humanities Branch', 'Librarian Wilson');
INSERT INTO library_loans VALUES (12, 'grace@uni.edu', 'Classical Mechanics', '978-1891389221', '2025-10-05', '2025-11-02', NULL, 0.00, 'active', 'Science Branch', 'Librarian Davis');
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
INSERT INTO faculty VALUES (1, 'James', 'Roberts', 'roberts@uni.edu', '555-2001', '2010-08-15', 1, 'Professor', 'Science Hall 301', 120000.00, 'tenured');
INSERT INTO faculty VALUES (2, 'Li', 'Chen', 'chen@uni.edu', '555-2002', '2012-01-10', 2, 'Associate Professor', 'Math Building 205', 105000.00, 'tenured');
INSERT INTO faculty VALUES (3, 'Sarah', 'Miller', 'miller@uni.edu', '555-2003', '2015-08-20', 3, 'Assistant Professor', 'Humanities Hall 110', 85000.00, 'tenure-track');
INSERT INTO faculty VALUES (4, 'Raj', 'Adams', 'adams@uni.edu', '555-2004', '2008-01-05', 4, 'Professor', 'Science Hall 402', 125000.00, 'tenured');
INSERT INTO faculty VALUES (5, 'Maria', 'Garcia', 'garcia@uni.edu', '555-2005', '2018-08-15', 1, 'Lecturer', 'Science Hall 303', 72000.00, 'non-tenure');
INSERT INTO faculty VALUES (6, 'Tom', 'Wilson', 'wilson@uni.edu', '555-2006', '2020-01-10', 2, 'Lecturer', 'Math Building 207', 68000.00, 'non-tenure');

CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT NOT NULL,
    dob TEXT NOT NULL,
    enrollment_date TEXT NOT NULL,
    department_id INTEGER NOT NULL,
    advisor_id INTEGER NOT NULL,
    gpa REAL,
    status TEXT NOT NULL DEFAULT 'active',
    FOREIGN KEY (department_id) REFERENCES departments(id),
    FOREIGN KEY (advisor_id) REFERENCES faculty(id)
);
INSERT INTO students VALUES (1, 'Alice', 'Wang', 'alice@uni.edu', '555-1001', '2002-03-15', '2022-08-20', 1, 1, 3.7, 'active');
INSERT INTO students VALUES (2, 'Bob', 'Patel', 'bob@uni.edu', '555-1002', '2001-07-22', '2021-08-18', 2, 2, 3.0, 'active');
INSERT INTO students VALUES (3, 'Carol', 'Lopez', 'carol@uni.edu', '555-1003', '2003-11-05', '2023-08-21', 3, 3, 3.4, 'active');
INSERT INTO students VALUES (4, 'Dave', 'Kim', 'dave@uni.edu', '555-1004', '2000-01-30', '2020-08-17', 1, 1, 3.8, 'active');
INSERT INTO students VALUES (5, 'Eve', 'Tanaka', 'eve@uni.edu', '555-1005', '2002-09-12', '2022-08-20', 4, 4, 3.2, 'active');
INSERT INTO students VALUES (6, 'Frank', 'Russo', 'frank@uni.edu', '555-1006', '2001-04-18', '2021-08-18', 2, 2, 2.7, 'probation');
INSERT INTO students VALUES (7, 'Grace', 'Okafor', 'grace@uni.edu', '555-1007', '2003-06-25', '2023-08-21', 4, 4, 3.5, 'active');
INSERT INTO students VALUES (8, 'Hiro', 'Sato', 'hiro@uni.edu', '555-1008', '2002-12-01', '2022-08-20', 3, 3, 2.9, 'active');

CREATE TABLE student_addresses (
    id INTEGER PRIMARY KEY,
    student_id INTEGER NOT NULL UNIQUE,
    address_line1 TEXT NOT NULL,
    address_city TEXT NOT NULL,
    address_state TEXT NOT NULL,
    address_zip TEXT NOT NULL,
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
    semester TEXT NOT NULL,
    year INTEGER NOT NULL,
    room_number TEXT NOT NULL,
    FOREIGN KEY (department_id) REFERENCES departments(id),
    FOREIGN KEY (instructor_id) REFERENCES faculty(id)
);
INSERT INTO courses VALUES (1, 'CS101', 'Intro to Programming', 'Learn basic programming concepts', 4, 1, 1, 40, 30, 'Fall', 2025, 'SH-101');
INSERT INTO courses VALUES (2, 'CS201', 'Data Structures', 'Advanced data structures and algorithms', 4, 1, 1, 35, 25, 'Fall', 2025, 'SH-102');
INSERT INTO courses VALUES (3, 'MATH101', 'Calculus I', 'Introduction to differential calculus', 4, 2, 2, 45, 35, 'Fall', 2025, 'MB-201');
INSERT INTO courses VALUES (4, 'MATH201', 'Linear Algebra', 'Vectors, matrices, and linear transformations', 3, 2, 2, 40, 28, 'Fall', 2025, 'MB-202');
INSERT INTO courses VALUES (5, 'ENG101', 'English Composition', 'Academic writing fundamentals', 3, 3, 3, 30, 25, 'Fall', 2025, 'HH-101');
INSERT INTO courses VALUES (6, 'ENG201', 'American Literature', 'Survey of American literary works', 3, 3, 3, 30, 20, 'Fall', 2025, 'HH-102');
INSERT INTO courses VALUES (7, 'PHYS101', 'Physics I', 'Mechanics and thermodynamics', 4, 4, 4, 40, 32, 'Fall', 2025, 'SH-201');
INSERT INTO courses VALUES (8, 'PHYS201', 'Physics II', 'Electricity and magnetism', 4, 4, 4, 35, 22, 'Fall', 2025, 'SH-202');
INSERT INTO courses VALUES (9, 'CS301', 'Database Systems', 'Relational databases and SQL', 3, 1, 5, 30, 20, 'Fall', 2025, 'SH-103');
INSERT INTO courses VALUES (10, 'MATH301', 'Probability & Stats', 'Intro to probability and statistics', 3, 2, 6, 35, 30, 'Fall', 2025, 'MB-301');

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
INSERT INTO submissions VALUES (12, 6, 8, '2025-09-19 11:00:00', '/files/hiro_essay.docx', 74.0, 'Needs more detail', 1, 3, '2025-09-20', 'graded');
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
    FOREIGN KEY (course_id) REFERENCES courses(id)
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
    semester TEXT NOT NULL,
    year INTEGER NOT NULL,
    FOREIGN KEY (faculty_id) REFERENCES faculty(id)
);
INSERT INTO office_hours VALUES (1, 1, 'Tuesday', '14:00', '16:00', 'SH-301', 0, NULL, 5, 'Fall', 2025);
INSERT INTO office_hours VALUES (2, 1, 'Thursday', '14:00', '16:00', 'SH-301', 0, NULL, 5, 'Fall', 2025);
INSERT INTO office_hours VALUES (3, 2, 'Monday', '10:00', '12:00', 'MB-205', 0, NULL, 4, 'Fall', 2025);
INSERT INTO office_hours VALUES (4, 2, 'Wednesday', '10:00', '12:00', NULL, 1, 'https://zoom.us/chen123', 6, 'Fall', 2025);
INSERT INTO office_hours VALUES (5, 3, 'Tuesday', '11:00', '12:30', 'HH-110', 0, NULL, 3, 'Fall', 2025);
INSERT INTO office_hours VALUES (6, 4, 'Friday', '13:00', '15:00', 'SH-402', 0, NULL, 4, 'Fall', 2025);
INSERT INTO office_hours VALUES (7, 5, 'Wednesday', '15:00', '17:00', NULL, 1, 'https://zoom.us/garcia456', 5, 'Fall', 2025);
INSERT INTO office_hours VALUES (8, 6, 'Thursday', '09:00', '11:00', 'MB-207', 0, NULL, 4, 'Fall', 2025);

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

CREATE TABLE semesters (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    year INTEGER NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    is_current INTEGER NOT NULL DEFAULT 0
);
INSERT INTO semesters VALUES (1, 'Fall', 2024, '2024-08-26', '2024-12-13', 0);
INSERT INTO semesters VALUES (2, 'Spring', 2025, '2025-01-13', '2025-05-09', 1);

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
INSERT INTO majors VALUES (3, 'English Literature', 3, 105, 'Study of written works');
INSERT INTO majors VALUES (4, 'Physics', 4, 115, 'Study of matter and energy');

CREATE TABLE student_activities (
    id INTEGER PRIMARY KEY,
    student_id INTEGER NOT NULL,
    activity_type TEXT NOT NULL,
    description TEXT NOT NULL,
    date TEXT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(id)
);
INSERT INTO student_activities VALUES (1, 1, 'enrollment', 'Enrolled in CS101', '2025-01-15');
INSERT INTO student_activities VALUES (2, 2, 'enrollment', 'Enrolled in MATH201', '2025-01-15');
INSERT INTO student_activities VALUES (3, 3, 'club_join', 'Joined Robotics Club', '2025-01-20');
INSERT INTO student_activities VALUES (4, 4, 'library_loan', 'Borrowed Design Patterns', '2025-02-01');
INSERT INTO student_activities VALUES (5, 5, 'enrollment', 'Enrolled in PHYS101', '2025-01-15');
INSERT INTO student_activities VALUES (6, 6, 'enrollment', 'Enrolled in ENG201', '2025-01-16');
INSERT INTO student_activities VALUES (7, 7, 'office_hours', 'Visited Dr. Smith office hours', '2025-02-10');
INSERT INTO student_activities VALUES (8, 8, 'enrollment', 'Enrolled in CS301', '2025-01-15');

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
INSERT INTO faculty_departments VALUES (1, 1, 1, 'head', '2018-08-15', 1);
INSERT INTO faculty_departments VALUES (2, 2, 2, 'member', '2015-01-10', 1);
INSERT INTO faculty_departments VALUES (3, 3, 3, 'member', '2019-08-20', 1);
INSERT INTO faculty_departments VALUES (4, 4, 4, 'head', '2016-06-01', 1);
INSERT INTO faculty_departments VALUES (5, 5, 1, 'member', '2020-01-15', 1);
INSERT INTO faculty_departments VALUES (6, 6, 2, 'member', '2021-08-20', 1);

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
INSERT INTO grade_history VALUES (1, 1, NULL, 'A', 1, 'Final grade posted', '2025-05-10');
INSERT INTO grade_history VALUES (2, 3, 'B+', 'A-', 2, 'Regrade request approved', '2025-05-12');
INSERT INTO grade_history VALUES (3, 5, NULL, 'B', 3, 'Final grade posted', '2025-05-10');
""";
