"""Task (Hard): HealthFirst Clinic → MedCore Enterprise Hospital System.

HealthFirst Community Clinic was a small neighbourhood clinic that ran on pen-and-paper
for decades. Five years ago they hired a local developer to put together a basic digital
system. The result: 30 tables with an hc_ prefix, patient references by email everywhere,
a single monolithic 'hc_reports' table that lumps X-rays, CT scans, MRIs, lab results,
ultrasounds, and pathology into one giant pile, zero foreign keys, zero indexes, and
abbreviated column names that only the original developer understood.

MedCore Enterprise Hospital System has acquired HealthFirst and needs every record
migrated into their 50-table enterprise schema — proper integer FKs, NOT NULL and
DEFAULT constraints on every column that needs them, UNIQUE where appropriate,
indexes on all lookup columns, and the monolithic reports table split into six
specialised tables (xray_reports, ct_scan_reports, mri_reports, lab_results,
ultrasound_reports, pathology_reports).

Initial: 30 tables (hc_ prefix), ~350 rows, 0 FKs, 0 indexes, email-based refs
Target:  50 tables (no prefix), ~550 rows, 60+ FKs, enterprise constraints + indexes

ZERO table name overlap between initial and target schemas.
"""

TASK_ID = "hard_hospital_acquisition"
TASK_DESCRIPTION = (
    "HealthFirst Community Clinic acquired by MedCore Enterprise Hospital System. "
    "Migrate 30 legacy hc_* tables (~350 rows, zero FKs, email/name text references, "
    "monolithic hc_reports table) into 50 enterprise-grade tables (~550 rows, 60+ foreign keys, "
    "NOT NULL/UNIQUE/DEFAULT constraints, indexes). Split hc_reports into xray_reports, "
    "ct_scan_reports, mri_reports, lab_results, ultrasound_reports, pathology_reports. "
    "Resolve all email references to integer FK IDs. Drop all 30 original hc_ tables. "
    "Zero table name overlap between source and target."
)
DIFFICULTY = "hard"
TIMEOUT_SECONDS = 1800  # 30 minutes

# =====================================================================
# INITIAL SCHEMA — HealthFirst Community Clinic (30 tables, hc_ prefix)
# =====================================================================

INITIAL_SQL = """
-- HealthFirst Community Clinic Legacy Schema
-- No foreign keys, no indexes, email-based patient references everywhere
-- One monolithic hc_reports table for ALL diagnostic reports

-- =============================================
-- hc_patients (12 rows) — core patient records
-- =============================================
CREATE TABLE hc_patients (
    pid INTEGER PRIMARY KEY,
    pt_fname TEXT NOT NULL,
    pt_lname TEXT NOT NULL,
    pt_email TEXT NOT NULL,
    pt_phone TEXT,
    pt_dob TEXT,
    pt_gender TEXT,
    pt_blood_type TEXT,
    pt_addr_line TEXT,
    pt_addr_city TEXT,
    pt_addr_state TEXT,
    pt_addr_zip TEXT,
    pt_emergency_name TEXT,
    pt_emergency_phone TEXT,
    pt_insurance_id TEXT,
    pt_registered TEXT,
    pt_is_active INTEGER DEFAULT 1
);

INSERT INTO hc_patients VALUES (1, 'Alice', 'Chen', 'alice.chen@email.com', '555-0101', '1990-03-15', 'F', 'A+', '123 Maple St', 'Portland', 'OR', '97201', 'Bob Chen', '555-0901', 'INS-1001', '2020-01-10', 1);
INSERT INTO hc_patients VALUES (2, 'Bob', 'Rivera', 'bob.rivera@email.com', '555-0102', '1985-07-22', 'M', 'O+', '456 Oak Ave', 'Austin', 'TX', '78701', 'Maria Rivera', '555-0902', 'INS-1002', '2020-03-05', 1);
INSERT INTO hc_patients VALUES (3, 'Carol', 'Zhang', 'carol.zhang@email.com', '555-0103', '1992-11-08', 'F', 'B+', '789 Pine Rd', 'Seattle', 'WA', '98101', 'Dan Zhang', '555-0903', 'INS-1003', '2020-06-18', 1);
INSERT INTO hc_patients VALUES (4, 'Dave', 'Wilson', 'dave.wilson@email.com', '555-0104', '1978-01-30', 'M', 'AB-', '321 Elm Blvd', 'Denver', 'CO', '80201', 'Sue Wilson', '555-0904', 'INS-1004', '2021-01-12', 1);
INSERT INTO hc_patients VALUES (5, 'Eve', 'Thompson', 'eve.thompson@email.com', '555-0105', '1995-05-12', 'F', 'O-', '654 Birch Ln', 'Miami', 'FL', '33101', 'Tom Thompson', '555-0905', 'INS-1005', '2021-04-20', 1);
INSERT INTO hc_patients VALUES (6, 'Frank', 'Garcia', 'frank.garcia@email.com', '555-0106', '1983-09-25', 'M', 'A-', '987 Cedar Ct', 'Chicago', 'IL', '60601', 'Rosa Garcia', '555-0906', 'INS-1006', '2021-07-01', 1);
INSERT INTO hc_patients VALUES (7, 'Grace', 'Kim', 'grace.kim@email.com', '555-0107', '1991-12-03', 'F', 'B-', '147 Walnut Dr', 'San Francisco', 'CA', '94101', 'James Kim', '555-0907', 'INS-1007', '2022-01-14', 1);
INSERT INTO hc_patients VALUES (8, 'Henry', 'Patel', 'henry.patel@email.com', '555-0108', '1987-04-18', 'M', 'AB+', '258 Spruce Way', 'Boston', 'MA', '02101', 'Priya Patel', '555-0908', 'INS-1008', '2022-05-22', 1);
INSERT INTO hc_patients VALUES (9, 'Ivy', 'Santos', 'ivy.santos@email.com', '555-0109', '1994-08-07', 'F', 'O+', '369 Ash Pl', 'Phoenix', 'AZ', '85001', 'Carlos Santos', '555-0909', 'INS-1009', '2022-09-10', 1);
INSERT INTO hc_patients VALUES (10, 'Jack', 'Murphy', 'jack.murphy@email.com', '555-0110', '1976-02-14', 'M', 'A+', '480 Poplar St', 'Nashville', 'TN', '37201', 'Fiona Murphy', '555-0910', 'INS-1010', '2023-01-03', 1);
INSERT INTO hc_patients VALUES (11, 'Kate', 'Brown', 'kate.brown@email.com', '555-0111', '1989-06-29', 'F', 'B+', '591 Hickory Ave', 'Atlanta', 'GA', '30301', 'Mark Brown', '555-0911', 'INS-1011', '2023-04-15', 1);
INSERT INTO hc_patients VALUES (12, 'Leo', 'Martinez', 'leo.martinez@email.com', '555-0112', '1982-10-11', 'M', 'O-', '702 Sycamore Rd', 'San Diego', 'CA', '92101', 'Ana Martinez', '555-0912', 'INS-1012', '2023-08-28', 0);

-- =============================================
-- hc_doctors (8 rows) — physician records
-- =============================================
CREATE TABLE hc_doctors (
    did INTEGER PRIMARY KEY,
    doc_fname TEXT NOT NULL,
    doc_lname TEXT NOT NULL,
    doc_email TEXT NOT NULL,
    doc_phone TEXT,
    doc_specialty TEXT,
    doc_license_no TEXT,
    doc_dept_name TEXT,
    doc_hire_date TEXT,
    doc_is_active INTEGER DEFAULT 1
);

INSERT INTO hc_doctors VALUES (1, 'Sarah', 'Williams', 'dr.williams@healthfirst.com', '555-0201', 'Cardiology', 'LIC-5001', 'Cardiology', '2018-03-01', 1);
INSERT INTO hc_doctors VALUES (2, 'Michael', 'Lee', 'dr.lee@healthfirst.com', '555-0202', 'Radiology', 'LIC-5002', 'Radiology', '2019-06-15', 1);
INSERT INTO hc_doctors VALUES (3, 'Jennifer', 'Adams', 'dr.adams@healthfirst.com', '555-0203', 'Orthopedics', 'LIC-5003', 'Orthopedics', '2019-09-01', 1);
INSERT INTO hc_doctors VALUES (4, 'Robert', 'Nguyen', 'dr.nguyen@healthfirst.com', '555-0204', 'Neurology', 'LIC-5004', 'Neurology', '2020-01-10', 1);
INSERT INTO hc_doctors VALUES (5, 'Emily', 'Clark', 'dr.clark@healthfirst.com', '555-0205', 'Dermatology', 'LIC-5005', 'Dermatology', '2020-05-20', 1);
INSERT INTO hc_doctors VALUES (6, 'David', 'Brown', 'dr.brown@healthfirst.com', '555-0206', 'General Surgery', 'LIC-5006', 'Surgery', '2021-02-01', 1);
INSERT INTO hc_doctors VALUES (7, 'Lisa', 'Taylor', 'dr.taylor@healthfirst.com', '555-0207', 'Pediatrics', 'LIC-5007', 'Pediatrics', '2021-08-15', 1);
INSERT INTO hc_doctors VALUES (8, 'James', 'White', 'dr.white@healthfirst.com', '555-0208', 'Internal Medicine', 'LIC-5008', 'Internal Medicine', '2022-01-05', 0);

-- =============================================
-- hc_nurses (10 rows) — nursing staff
-- =============================================
CREATE TABLE hc_nurses (
    nid INTEGER PRIMARY KEY,
    nur_fname TEXT NOT NULL,
    nur_lname TEXT NOT NULL,
    nur_email TEXT NOT NULL,
    nur_phone TEXT,
    nur_dept_name TEXT,
    nur_shift TEXT,
    nur_certification TEXT,
    nur_hire_date TEXT,
    nur_is_active INTEGER DEFAULT 1
);

INSERT INTO hc_nurses VALUES (1, 'Anna', 'Scott', 'anna.scott@healthfirst.com', '555-0301', 'Cardiology', 'Day', 'RN', '2019-01-10', 1);
INSERT INTO hc_nurses VALUES (2, 'Brian', 'Hall', 'brian.hall@healthfirst.com', '555-0302', 'Radiology', 'Night', 'RN', '2019-04-15', 1);
INSERT INTO hc_nurses VALUES (3, 'Clara', 'Young', 'clara.young@healthfirst.com', '555-0303', 'Orthopedics', 'Day', 'BSN', '2019-08-01', 1);
INSERT INTO hc_nurses VALUES (4, 'Derek', 'King', 'derek.king@healthfirst.com', '555-0304', 'Neurology', 'Night', 'RN', '2020-02-20', 1);
INSERT INTO hc_nurses VALUES (5, 'Elena', 'Wright', 'elena.wright@healthfirst.com', '555-0305', 'Dermatology', 'Day', 'BSN', '2020-06-10', 1);
INSERT INTO hc_nurses VALUES (6, 'Felix', 'Lopez', 'felix.lopez@healthfirst.com', '555-0306', 'Surgery', 'Night', 'RN', '2021-01-05', 1);
INSERT INTO hc_nurses VALUES (7, 'Gina', 'Allen', 'gina.allen@healthfirst.com', '555-0307', 'Pediatrics', 'Day', 'BSN', '2021-05-15', 1);
INSERT INTO hc_nurses VALUES (8, 'Hugo', 'Baker', 'hugo.baker@healthfirst.com', '555-0308', 'Internal Medicine', 'Day', 'RN', '2021-09-20', 1);
INSERT INTO hc_nurses VALUES (9, 'Iris', 'Carter', 'iris.carter@healthfirst.com', '555-0309', 'Emergency', 'Night', 'BSN', '2022-03-01', 1);
INSERT INTO hc_nurses VALUES (10, 'Jake', 'Davis', 'jake.davis@healthfirst.com', '555-0310', 'Emergency', 'Day', 'RN', '2022-07-10', 0);

-- =============================================
-- hc_departments (8 rows) — clinic departments
-- =============================================
CREATE TABLE hc_departments (
    dept_id INTEGER PRIMARY KEY,
    dept_name TEXT NOT NULL,
    dept_head_email TEXT,
    dept_floor INTEGER,
    dept_phone TEXT,
    dept_created TEXT
);

INSERT INTO hc_departments VALUES (1, 'Cardiology', 'dr.williams@healthfirst.com', 2, '555-1001', '2018-01-01');
INSERT INTO hc_departments VALUES (2, 'Radiology', 'dr.lee@healthfirst.com', 1, '555-1002', '2018-01-01');
INSERT INTO hc_departments VALUES (3, 'Orthopedics', 'dr.adams@healthfirst.com', 3, '555-1003', '2019-01-01');
INSERT INTO hc_departments VALUES (4, 'Neurology', 'dr.nguyen@healthfirst.com', 2, '555-1004', '2020-01-01');
INSERT INTO hc_departments VALUES (5, 'Dermatology', 'dr.clark@healthfirst.com', 1, '555-1005', '2020-01-01');
INSERT INTO hc_departments VALUES (6, 'Surgery', 'dr.brown@healthfirst.com', 3, '555-1006', '2021-01-01');
INSERT INTO hc_departments VALUES (7, 'Pediatrics', 'dr.taylor@healthfirst.com', 1, '555-1007', '2021-01-01');
INSERT INTO hc_departments VALUES (8, 'Internal Medicine', 'dr.white@healthfirst.com', 2, '555-1008', '2022-01-01');

-- =============================================
-- hc_appointments (20 rows) — patient appointments
-- =============================================
CREATE TABLE hc_appointments (
    aid INTEGER PRIMARY KEY,
    appt_patient_email TEXT NOT NULL,
    appt_doctor_email TEXT NOT NULL,
    appt_date TEXT NOT NULL,
    appt_time TEXT,
    appt_type TEXT,
    appt_status TEXT DEFAULT 'scheduled',
    appt_notes TEXT,
    appt_room TEXT,
    appt_created TEXT
);

INSERT INTO hc_appointments VALUES (1, 'alice.chen@email.com', 'dr.williams@healthfirst.com', '2024-01-15', '09:00', 'checkup', 'completed', 'Annual cardiac checkup', 'Room 201', '2024-01-10');
INSERT INTO hc_appointments VALUES (2, 'bob.rivera@email.com', 'dr.lee@healthfirst.com', '2024-01-20', '10:30', 'imaging', 'completed', 'Chest X-ray follow-up', 'Room 102', '2024-01-15');
INSERT INTO hc_appointments VALUES (3, 'carol.zhang@email.com', 'dr.adams@healthfirst.com', '2024-02-05', '14:00', 'consultation', 'completed', 'Knee pain evaluation', 'Room 301', '2024-01-28');
INSERT INTO hc_appointments VALUES (4, 'dave.wilson@email.com', 'dr.nguyen@healthfirst.com', '2024-02-10', '11:00', 'follow-up', 'completed', 'Migraine follow-up', 'Room 205', '2024-02-03');
INSERT INTO hc_appointments VALUES (5, 'eve.thompson@email.com', 'dr.clark@healthfirst.com', '2024-02-15', '09:30', 'checkup', 'completed', 'Skin rash evaluation', 'Room 108', '2024-02-10');
INSERT INTO hc_appointments VALUES (6, 'frank.garcia@email.com', 'dr.brown@healthfirst.com', '2024-03-01', '08:00', 'surgery', 'completed', 'Appendectomy pre-op', 'Room 305', '2024-02-20');
INSERT INTO hc_appointments VALUES (7, 'grace.kim@email.com', 'dr.taylor@healthfirst.com', '2024-03-10', '15:00', 'checkup', 'completed', 'Wellness checkup', 'Room 110', '2024-03-05');
INSERT INTO hc_appointments VALUES (8, 'henry.patel@email.com', 'dr.williams@healthfirst.com', '2024-03-15', '10:00', 'imaging', 'completed', 'Echocardiogram', 'Room 201', '2024-03-10');
INSERT INTO hc_appointments VALUES (9, 'ivy.santos@email.com', 'dr.lee@healthfirst.com', '2024-03-20', '13:00', 'imaging', 'completed', 'MRI brain scan', 'Room 102', '2024-03-15');
INSERT INTO hc_appointments VALUES (10, 'jack.murphy@email.com', 'dr.nguyen@healthfirst.com', '2024-04-01', '11:30', 'consultation', 'completed', 'Numbness in extremities', 'Room 205', '2024-03-25');
INSERT INTO hc_appointments VALUES (11, 'kate.brown@email.com', 'dr.adams@healthfirst.com', '2024-04-10', '09:00', 'follow-up', 'completed', 'Post-surgery knee check', 'Room 301', '2024-04-05');
INSERT INTO hc_appointments VALUES (12, 'alice.chen@email.com', 'dr.lee@healthfirst.com', '2024-04-15', '14:30', 'imaging', 'completed', 'CT scan chest', 'Room 102', '2024-04-10');
INSERT INTO hc_appointments VALUES (13, 'bob.rivera@email.com', 'dr.brown@healthfirst.com', '2024-05-01', '08:30', 'consultation', 'completed', 'Hernia evaluation', 'Room 305', '2024-04-25');
INSERT INTO hc_appointments VALUES (14, 'carol.zhang@email.com', 'dr.williams@healthfirst.com', '2024-05-10', '10:00', 'checkup', 'completed', 'Blood pressure monitoring', 'Room 201', '2024-05-05');
INSERT INTO hc_appointments VALUES (15, 'dave.wilson@email.com', 'dr.lee@healthfirst.com', '2024-05-15', '11:00', 'imaging', 'completed', 'Brain MRI', 'Room 102', '2024-05-10');
INSERT INTO hc_appointments VALUES (16, 'eve.thompson@email.com', 'dr.taylor@healthfirst.com', '2024-06-01', '09:00', 'checkup', 'cancelled', 'Annual physical', 'Room 110', '2024-05-25');
INSERT INTO hc_appointments VALUES (17, 'frank.garcia@email.com', 'dr.brown@healthfirst.com', '2024-06-10', '08:00', 'follow-up', 'completed', 'Post-appendectomy check', 'Room 305', '2024-06-05');
INSERT INTO hc_appointments VALUES (18, 'grace.kim@email.com', 'dr.clark@healthfirst.com', '2024-06-15', '14:00', 'consultation', 'scheduled', 'Mole assessment', 'Room 108', '2024-06-10');
INSERT INTO hc_appointments VALUES (19, 'henry.patel@email.com', 'dr.nguyen@healthfirst.com', '2024-07-01', '10:30', 'follow-up', 'scheduled', 'Nerve conduction test results', 'Room 205', '2024-06-25');
INSERT INTO hc_appointments VALUES (20, 'leo.martinez@email.com', 'dr.williams@healthfirst.com', '2024-07-10', '09:00', 'checkup', 'scheduled', 'Cardiac stress test', 'Room 201', '2024-07-05');

-- =============================================
-- hc_reports (24 rows) — THE MONOLITHIC REPORTS TABLE
-- All types lumped together: xray, ct_scan, mri, lab, ultrasound, pathology
-- =============================================
CREATE TABLE hc_reports (
    rid INTEGER PRIMARY KEY,
    rpt_patient_email TEXT NOT NULL,
    rpt_doctor_email TEXT NOT NULL,
    rpt_type TEXT NOT NULL,
    rpt_title TEXT NOT NULL,
    rpt_body_region TEXT,
    rpt_findings TEXT,
    rpt_conclusion TEXT,
    rpt_severity TEXT DEFAULT 'normal',
    rpt_file_url TEXT,
    rpt_date TEXT NOT NULL,
    rpt_status TEXT DEFAULT 'final',
    rpt_notes TEXT
);

-- X-ray reports (4)
INSERT INTO hc_reports VALUES (1, 'alice.chen@email.com', 'dr.lee@healthfirst.com', 'xray', 'Chest X-Ray', 'chest', 'No acute cardiopulmonary process', 'Normal chest radiograph', 'normal', '/files/xray/001.dcm', '2024-01-15', 'final', 'PA and lateral views');
INSERT INTO hc_reports VALUES (2, 'bob.rivera@email.com', 'dr.lee@healthfirst.com', 'xray', 'Chest X-Ray', 'chest', 'Mild cardiomegaly noted', 'Borderline cardiac enlargement', 'moderate', '/files/xray/002.dcm', '2024-01-20', 'final', 'Comparison with prior study recommended');
INSERT INTO hc_reports VALUES (3, 'carol.zhang@email.com', 'dr.adams@healthfirst.com', 'xray', 'Right Knee X-Ray', 'knee', 'Mild degenerative changes', 'Early osteoarthritis', 'mild', '/files/xray/003.dcm', '2024-02-05', 'final', 'Weight-bearing views');
INSERT INTO hc_reports VALUES (4, 'jack.murphy@email.com', 'dr.adams@healthfirst.com', 'xray', 'Lumbar Spine X-Ray', 'spine', 'Disc space narrowing L4-L5', 'Degenerative disc disease', 'moderate', '/files/xray/004.dcm', '2024-04-01', 'final', 'AP and lateral views');

-- CT scan reports (4)
INSERT INTO hc_reports VALUES (5, 'alice.chen@email.com', 'dr.lee@healthfirst.com', 'ct_scan', 'CT Chest with Contrast', 'chest', 'No pulmonary embolism', 'Negative for PE', 'normal', '/files/ct/001.dcm', '2024-04-15', 'final', 'IV contrast administered');
INSERT INTO hc_reports VALUES (6, 'dave.wilson@email.com', 'dr.nguyen@healthfirst.com', 'ct_scan', 'CT Head without Contrast', 'head', 'No acute intracranial abnormality', 'Normal CT head', 'normal', '/files/ct/002.dcm', '2024-02-10', 'final', 'Non-contrast study');
INSERT INTO hc_reports VALUES (7, 'frank.garcia@email.com', 'dr.brown@healthfirst.com', 'ct_scan', 'CT Abdomen/Pelvis', 'abdomen', 'Acute appendicitis with periappendiceal fat stranding', 'Acute appendicitis confirmed', 'severe', '/files/ct/003.dcm', '2024-03-01', 'final', 'Oral and IV contrast');
INSERT INTO hc_reports VALUES (8, 'henry.patel@email.com', 'dr.lee@healthfirst.com', 'ct_scan', 'CT Chest', 'chest', 'Small ground-glass opacity right lower lobe', 'Follow-up recommended in 3 months', 'mild', '/files/ct/004.dcm', '2024-03-15', 'preliminary', 'Non-contrast study');

-- MRI reports (4)
INSERT INTO hc_reports VALUES (9, 'ivy.santos@email.com', 'dr.lee@healthfirst.com', 'mri', 'MRI Brain with Contrast', 'brain', 'No enhancing lesions, no mass effect', 'Normal brain MRI', 'normal', '/files/mri/001.dcm', '2024-03-20', 'final', 'Gadolinium contrast');
INSERT INTO hc_reports VALUES (10, 'dave.wilson@email.com', 'dr.nguyen@healthfirst.com', 'mri', 'MRI Brain without Contrast', 'brain', 'Mild white matter changes', 'Age-appropriate white matter changes', 'mild', '/files/mri/002.dcm', '2024-05-15', 'final', 'Non-contrast study');
INSERT INTO hc_reports VALUES (11, 'carol.zhang@email.com', 'dr.adams@healthfirst.com', 'mri', 'MRI Right Knee', 'knee', 'Partial tear medial meniscus', 'Meniscal pathology confirmed', 'moderate', '/files/mri/003.dcm', '2024-02-10', 'final', 'Without contrast');
INSERT INTO hc_reports VALUES (12, 'kate.brown@email.com', 'dr.adams@healthfirst.com', 'mri', 'MRI Left Shoulder', 'shoulder', 'Rotator cuff tendinosis without tear', 'No surgical intervention needed', 'mild', '/files/mri/004.dcm', '2024-04-10', 'final', 'Without contrast');

-- Lab results (4)
INSERT INTO hc_reports VALUES (13, 'alice.chen@email.com', 'dr.williams@healthfirst.com', 'lab', 'Complete Blood Count', 'blood', 'WBC 6.8, RBC 4.5, Hgb 13.2, Hct 39.5, Plt 250', 'All values within normal limits', 'normal', NULL, '2024-01-15', 'final', 'Fasting sample');
INSERT INTO hc_reports VALUES (14, 'bob.rivera@email.com', 'dr.williams@healthfirst.com', 'lab', 'Lipid Panel', 'blood', 'Total Chol 245, LDL 160, HDL 42, Trig 215', 'Hyperlipidemia', 'moderate', NULL, '2024-01-20', 'final', 'Fasting 12 hours');
INSERT INTO hc_reports VALUES (15, 'eve.thompson@email.com', 'dr.clark@healthfirst.com', 'lab', 'Comprehensive Metabolic Panel', 'blood', 'Glucose 95, BUN 15, Creatinine 0.9, all electrolytes normal', 'Normal metabolic panel', 'normal', NULL, '2024-02-15', 'final', 'Morning draw');
INSERT INTO hc_reports VALUES (16, 'henry.patel@email.com', 'dr.williams@healthfirst.com', 'lab', 'Thyroid Panel', 'blood', 'TSH 2.5, Free T4 1.1, Free T3 3.2', 'Euthyroid', 'normal', NULL, '2024-03-15', 'final', 'No fasting required');

-- Ultrasound reports (4)
INSERT INTO hc_reports VALUES (17, 'grace.kim@email.com', 'dr.taylor@healthfirst.com', 'ultrasound', 'Abdominal Ultrasound', 'abdomen', 'Normal liver, gallbladder, kidneys', 'No significant findings', 'normal', '/files/us/001.dcm', '2024-03-10', 'final', 'Fasting study');
INSERT INTO hc_reports VALUES (18, 'ivy.santos@email.com', 'dr.williams@healthfirst.com', 'ultrasound', 'Thyroid Ultrasound', 'neck', 'Small benign-appearing nodule right lobe 0.8cm', 'Benign thyroid nodule, follow-up in 12 months', 'mild', '/files/us/002.dcm', '2024-03-25', 'final', 'No prior comparison');
INSERT INTO hc_reports VALUES (19, 'kate.brown@email.com', 'dr.williams@healthfirst.com', 'ultrasound', 'Carotid Doppler', 'neck', 'No hemodynamically significant stenosis', 'Normal carotid arteries', 'normal', '/files/us/003.dcm', '2024-04-12', 'final', 'Bilateral study');
INSERT INTO hc_reports VALUES (20, 'frank.garcia@email.com', 'dr.brown@healthfirst.com', 'ultrasound', 'RUQ Ultrasound', 'abdomen', 'No gallstones, normal bile ducts', 'Normal right upper quadrant', 'normal', '/files/us/004.dcm', '2024-03-02', 'final', 'Fasting study');

-- Pathology reports (4)
INSERT INTO hc_reports VALUES (21, 'frank.garcia@email.com', 'dr.brown@healthfirst.com', 'pathology', 'Appendix Specimen', 'appendix', 'Acute appendicitis with transmural inflammation', 'Acute suppurative appendicitis confirmed', 'severe', NULL, '2024-03-02', 'final', 'Specimen from appendectomy');
INSERT INTO hc_reports VALUES (22, 'eve.thompson@email.com', 'dr.clark@healthfirst.com', 'pathology', 'Skin Biopsy - Left Arm', 'skin', 'Benign intradermal nevus', 'Benign melanocytic nevus', 'normal', NULL, '2024-02-15', 'final', 'Punch biopsy 4mm');
INSERT INTO hc_reports VALUES (23, 'jack.murphy@email.com', 'dr.clark@healthfirst.com', 'pathology', 'Skin Biopsy - Back', 'skin', 'Seborrheic keratosis', 'Benign keratosis', 'normal', NULL, '2024-04-05', 'final', 'Shave biopsy');
INSERT INTO hc_reports VALUES (24, 'grace.kim@email.com', 'dr.clark@healthfirst.com', 'pathology', 'Skin Lesion Excision', 'skin', 'Basal cell carcinoma, margins clear', 'BCC completely excised', 'moderate', NULL, '2024-06-15', 'preliminary', 'Excisional biopsy');

-- =============================================
-- hc_prescriptions (15 rows) — medication prescriptions
-- =============================================
CREATE TABLE hc_prescriptions (
    prid INTEGER PRIMARY KEY,
    rx_patient_email TEXT NOT NULL,
    rx_doctor_email TEXT NOT NULL,
    rx_medication TEXT NOT NULL,
    rx_dosage TEXT NOT NULL,
    rx_frequency TEXT,
    rx_start_date TEXT,
    rx_end_date TEXT,
    rx_refills INTEGER DEFAULT 0,
    rx_status TEXT DEFAULT 'active',
    rx_pharmacy TEXT,
    rx_notes TEXT
);

INSERT INTO hc_prescriptions VALUES (1, 'alice.chen@email.com', 'dr.williams@healthfirst.com', 'Lisinopril', '10mg', 'Once daily', '2024-01-15', '2024-07-15', 3, 'active', 'CVS Pharmacy', 'Monitor blood pressure');
INSERT INTO hc_prescriptions VALUES (2, 'bob.rivera@email.com', 'dr.williams@healthfirst.com', 'Atorvastatin', '20mg', 'Once daily at bedtime', '2024-01-20', '2025-01-20', 6, 'active', 'Walgreens', 'Check lipids in 3 months');
INSERT INTO hc_prescriptions VALUES (3, 'carol.zhang@email.com', 'dr.adams@healthfirst.com', 'Ibuprofen', '400mg', 'Three times daily with food', '2024-02-05', '2024-03-05', 0, 'completed', 'Rite Aid', 'For knee inflammation');
INSERT INTO hc_prescriptions VALUES (4, 'dave.wilson@email.com', 'dr.nguyen@healthfirst.com', 'Sumatriptan', '50mg', 'As needed for migraine', '2024-02-10', '2024-08-10', 2, 'active', 'CVS Pharmacy', 'Max 2 doses per 24 hours');
INSERT INTO hc_prescriptions VALUES (5, 'eve.thompson@email.com', 'dr.clark@healthfirst.com', 'Hydrocortisone Cream', '1%', 'Twice daily to affected area', '2024-02-15', '2024-03-15', 0, 'completed', 'Walgreens', 'Apply thin layer');
INSERT INTO hc_prescriptions VALUES (6, 'frank.garcia@email.com', 'dr.brown@healthfirst.com', 'Amoxicillin', '500mg', 'Three times daily', '2024-03-02', '2024-03-12', 0, 'completed', 'CVS Pharmacy', 'Post-surgery prophylaxis');
INSERT INTO hc_prescriptions VALUES (7, 'grace.kim@email.com', 'dr.taylor@healthfirst.com', 'Vitamin D3', '2000IU', 'Once daily', '2024-03-10', '2024-09-10', 2, 'active', 'Rite Aid', 'Supplement for deficiency');
INSERT INTO hc_prescriptions VALUES (8, 'henry.patel@email.com', 'dr.williams@healthfirst.com', 'Levothyroxine', '50mcg', 'Once daily on empty stomach', '2024-03-15', '2025-03-15', 6, 'active', 'CVS Pharmacy', 'Take 30 min before breakfast');
INSERT INTO hc_prescriptions VALUES (9, 'ivy.santos@email.com', 'dr.lee@healthfirst.com', 'Acetaminophen', '500mg', 'Every 6 hours as needed', '2024-03-20', '2024-04-20', 0, 'completed', 'Walgreens', 'For headache after MRI');
INSERT INTO hc_prescriptions VALUES (10, 'jack.murphy@email.com', 'dr.nguyen@healthfirst.com', 'Gabapentin', '300mg', 'Three times daily', '2024-04-01', '2024-10-01', 3, 'active', 'CVS Pharmacy', 'For neuropathic pain');
INSERT INTO hc_prescriptions VALUES (11, 'kate.brown@email.com', 'dr.adams@healthfirst.com', 'Naproxen', '500mg', 'Twice daily with food', '2024-04-10', '2024-05-10', 1, 'completed', 'Rite Aid', 'For shoulder pain');
INSERT INTO hc_prescriptions VALUES (12, 'alice.chen@email.com', 'dr.williams@healthfirst.com', 'Metoprolol', '25mg', 'Twice daily', '2024-04-15', '2024-10-15', 3, 'active', 'CVS Pharmacy', 'Heart rate control');
INSERT INTO hc_prescriptions VALUES (13, 'bob.rivera@email.com', 'dr.williams@healthfirst.com', 'Aspirin', '81mg', 'Once daily', '2024-01-20', '2025-01-20', 6, 'active', 'Walgreens', 'Low-dose for cardiac protection');
INSERT INTO hc_prescriptions VALUES (14, 'dave.wilson@email.com', 'dr.nguyen@healthfirst.com', 'Topiramate', '25mg', 'Once daily', '2024-05-15', '2024-11-15', 3, 'active', 'CVS Pharmacy', 'Migraine prevention');
INSERT INTO hc_prescriptions VALUES (15, 'carol.zhang@email.com', 'dr.adams@healthfirst.com', 'Glucosamine', '1500mg', 'Once daily', '2024-02-10', '2024-08-10', 2, 'active', 'Rite Aid', 'Joint supplement');

-- =============================================
-- hc_diagnoses (16 rows) — patient diagnoses
-- =============================================
CREATE TABLE hc_diagnoses (
    diag_id INTEGER PRIMARY KEY,
    diag_patient_email TEXT NOT NULL,
    diag_doctor_email TEXT NOT NULL,
    diag_icd_code TEXT NOT NULL,
    diag_name TEXT NOT NULL,
    diag_type TEXT DEFAULT 'primary',
    diag_date TEXT NOT NULL,
    diag_status TEXT DEFAULT 'active',
    diag_notes TEXT
);

INSERT INTO hc_diagnoses VALUES (1, 'alice.chen@email.com', 'dr.williams@healthfirst.com', 'I10', 'Essential Hypertension', 'primary', '2024-01-15', 'active', 'Stage 1, diet and medication');
INSERT INTO hc_diagnoses VALUES (2, 'bob.rivera@email.com', 'dr.williams@healthfirst.com', 'E78.5', 'Hyperlipidemia', 'primary', '2024-01-20', 'active', 'Elevated LDL and triglycerides');
INSERT INTO hc_diagnoses VALUES (3, 'carol.zhang@email.com', 'dr.adams@healthfirst.com', 'M17.11', 'Primary Osteoarthritis Right Knee', 'primary', '2024-02-05', 'active', 'Mild degenerative changes on imaging');
INSERT INTO hc_diagnoses VALUES (4, 'dave.wilson@email.com', 'dr.nguyen@healthfirst.com', 'G43.909', 'Migraine Unspecified', 'primary', '2024-02-10', 'active', 'Chronic migraines with aura');
INSERT INTO hc_diagnoses VALUES (5, 'eve.thompson@email.com', 'dr.clark@healthfirst.com', 'L30.9', 'Dermatitis Unspecified', 'primary', '2024-02-15', 'resolved', 'Contact dermatitis, resolved with treatment');
INSERT INTO hc_diagnoses VALUES (6, 'frank.garcia@email.com', 'dr.brown@healthfirst.com', 'K35.80', 'Acute Appendicitis', 'primary', '2024-03-01', 'resolved', 'Surgically treated');
INSERT INTO hc_diagnoses VALUES (7, 'grace.kim@email.com', 'dr.taylor@healthfirst.com', 'D51.0', 'Vitamin D Deficiency', 'secondary', '2024-03-10', 'active', 'Low vitamin D levels on labs');
INSERT INTO hc_diagnoses VALUES (8, 'henry.patel@email.com', 'dr.williams@healthfirst.com', 'E03.9', 'Hypothyroidism', 'primary', '2024-03-15', 'active', 'Subclinical, started levothyroxine');
INSERT INTO hc_diagnoses VALUES (9, 'ivy.santos@email.com', 'dr.lee@healthfirst.com', 'R51', 'Headache', 'primary', '2024-03-20', 'resolved', 'Tension headache, normal MRI');
INSERT INTO hc_diagnoses VALUES (10, 'jack.murphy@email.com', 'dr.nguyen@healthfirst.com', 'G62.9', 'Polyneuropathy Unspecified', 'primary', '2024-04-01', 'active', 'Peripheral neuropathy, workup ongoing');
INSERT INTO hc_diagnoses VALUES (11, 'kate.brown@email.com', 'dr.adams@healthfirst.com', 'M75.10', 'Rotator Cuff Tendinitis', 'primary', '2024-04-10', 'active', 'Conservative management');
INSERT INTO hc_diagnoses VALUES (12, 'carol.zhang@email.com', 'dr.adams@healthfirst.com', 'M23.21', 'Meniscal Derangement Right Knee', 'secondary', '2024-02-10', 'active', 'Partial tear medial meniscus on MRI');
INSERT INTO hc_diagnoses VALUES (13, 'alice.chen@email.com', 'dr.williams@healthfirst.com', 'I25.10', 'Atherosclerotic Heart Disease', 'secondary', '2024-04-15', 'active', 'CT showed no significant stenosis');
INSERT INTO hc_diagnoses VALUES (14, 'bob.rivera@email.com', 'dr.williams@healthfirst.com', 'I10', 'Essential Hypertension', 'secondary', '2024-01-20', 'active', 'Associated with hyperlipidemia');
INSERT INTO hc_diagnoses VALUES (15, 'grace.kim@email.com', 'dr.clark@healthfirst.com', 'C44.91', 'Basal Cell Carcinoma', 'primary', '2024-06-15', 'active', 'Excised with clear margins');
INSERT INTO hc_diagnoses VALUES (16, 'frank.garcia@email.com', 'dr.brown@healthfirst.com', 'K40.90', 'Inguinal Hernia', 'primary', '2024-05-01', 'active', 'Watchful waiting for now');

-- =============================================
-- hc_vitals (20 rows) — patient vital signs
-- =============================================
CREATE TABLE hc_vitals (
    vid INTEGER PRIMARY KEY,
    vt_patient_email TEXT NOT NULL,
    vt_nurse_email TEXT,
    vt_date TEXT NOT NULL,
    vt_bp_systolic INTEGER,
    vt_bp_diastolic INTEGER,
    vt_heart_rate INTEGER,
    vt_temperature REAL,
    vt_respiratory_rate INTEGER,
    vt_o2_saturation REAL,
    vt_weight_kg REAL,
    vt_height_cm REAL,
    vt_notes TEXT
);

INSERT INTO hc_vitals VALUES (1, 'alice.chen@email.com', 'anna.scott@healthfirst.com', '2024-01-15', 138, 88, 72, 98.6, 16, 98.0, 62.0, 165.0, 'Slightly elevated BP');
INSERT INTO hc_vitals VALUES (2, 'bob.rivera@email.com', 'anna.scott@healthfirst.com', '2024-01-20', 142, 92, 78, 98.4, 18, 97.5, 95.0, 178.0, 'Elevated BP, overweight');
INSERT INTO hc_vitals VALUES (3, 'carol.zhang@email.com', 'clara.young@healthfirst.com', '2024-02-05', 118, 76, 68, 98.6, 14, 99.0, 58.0, 162.0, 'Normal vitals');
INSERT INTO hc_vitals VALUES (4, 'dave.wilson@email.com', 'derek.king@healthfirst.com', '2024-02-10', 125, 82, 70, 98.8, 16, 98.5, 82.0, 175.0, 'Mild headache reported');
INSERT INTO hc_vitals VALUES (5, 'eve.thompson@email.com', 'elena.wright@healthfirst.com', '2024-02-15', 112, 72, 65, 98.6, 14, 99.0, 55.0, 160.0, 'Normal vitals');
INSERT INTO hc_vitals VALUES (6, 'frank.garcia@email.com', 'felix.lopez@healthfirst.com', '2024-03-01', 130, 85, 88, 100.2, 20, 97.0, 78.0, 172.0, 'Fever and elevated HR pre-surgery');
INSERT INTO hc_vitals VALUES (7, 'grace.kim@email.com', 'gina.allen@healthfirst.com', '2024-03-10', 110, 70, 62, 98.4, 14, 99.5, 52.0, 158.0, 'Excellent vitals');
INSERT INTO hc_vitals VALUES (8, 'henry.patel@email.com', 'anna.scott@healthfirst.com', '2024-03-15', 120, 78, 68, 98.6, 16, 98.5, 75.0, 180.0, 'Normal vitals');
INSERT INTO hc_vitals VALUES (9, 'ivy.santos@email.com', 'brian.hall@healthfirst.com', '2024-03-20', 115, 74, 70, 98.4, 15, 99.0, 60.0, 168.0, 'Normal vitals');
INSERT INTO hc_vitals VALUES (10, 'jack.murphy@email.com', 'derek.king@healthfirst.com', '2024-04-01', 135, 86, 74, 98.6, 16, 98.0, 88.0, 182.0, 'Elevated BP');
INSERT INTO hc_vitals VALUES (11, 'kate.brown@email.com', 'clara.young@healthfirst.com', '2024-04-10', 116, 74, 66, 98.6, 14, 99.0, 64.0, 170.0, 'Normal vitals');
INSERT INTO hc_vitals VALUES (12, 'alice.chen@email.com', 'anna.scott@healthfirst.com', '2024-04-15', 132, 84, 70, 98.6, 16, 98.5, 61.5, 165.0, 'BP slightly improved');
INSERT INTO hc_vitals VALUES (13, 'bob.rivera@email.com', 'anna.scott@healthfirst.com', '2024-05-01', 140, 90, 76, 98.4, 18, 97.5, 94.0, 178.0, 'Still elevated BP');
INSERT INTO hc_vitals VALUES (14, 'carol.zhang@email.com', 'clara.young@healthfirst.com', '2024-05-10', 120, 78, 66, 98.6, 14, 99.0, 57.5, 162.0, 'Normal');
INSERT INTO hc_vitals VALUES (15, 'dave.wilson@email.com', 'derek.king@healthfirst.com', '2024-05-15', 122, 80, 68, 98.8, 16, 98.5, 81.0, 175.0, 'Stable');
INSERT INTO hc_vitals VALUES (16, 'frank.garcia@email.com', 'felix.lopez@healthfirst.com', '2024-06-10', 122, 78, 72, 98.6, 16, 98.5, 76.0, 172.0, 'Post-surgery recovery good');
INSERT INTO hc_vitals VALUES (17, 'grace.kim@email.com', 'elena.wright@healthfirst.com', '2024-06-15', 108, 68, 60, 98.4, 14, 99.5, 52.0, 158.0, 'Normal');
INSERT INTO hc_vitals VALUES (18, 'henry.patel@email.com', 'derek.king@healthfirst.com', '2024-07-01', 118, 76, 66, 98.6, 16, 98.5, 74.0, 180.0, 'Stable on medication');
INSERT INTO hc_vitals VALUES (19, 'leo.martinez@email.com', 'anna.scott@healthfirst.com', '2024-07-10', 128, 82, 72, 98.6, 16, 98.0, 80.0, 176.0, 'Normal for age');
INSERT INTO hc_vitals VALUES (20, 'ivy.santos@email.com', 'iris.carter@healthfirst.com', '2024-06-20', 114, 72, 68, 98.4, 15, 99.0, 59.5, 168.0, 'Normal');

-- =============================================
-- hc_insurance (12 rows) — patient insurance info
-- =============================================
CREATE TABLE hc_insurance (
    ins_id INTEGER PRIMARY KEY,
    ins_patient_email TEXT NOT NULL,
    ins_provider TEXT NOT NULL,
    ins_plan TEXT,
    ins_policy_no TEXT,
    ins_group_no TEXT,
    ins_start_date TEXT,
    ins_end_date TEXT,
    ins_copay REAL DEFAULT 0.0,
    ins_is_primary INTEGER DEFAULT 1
);

INSERT INTO hc_insurance VALUES (1, 'alice.chen@email.com', 'BlueCross BlueShield', 'PPO Gold', 'POL-10001', 'GRP-5001', '2024-01-01', '2024-12-31', 25.0, 1);
INSERT INTO hc_insurance VALUES (2, 'bob.rivera@email.com', 'Aetna', 'HMO Standard', 'POL-10002', 'GRP-5002', '2024-01-01', '2024-12-31', 30.0, 1);
INSERT INTO hc_insurance VALUES (3, 'carol.zhang@email.com', 'UnitedHealth', 'PPO Premium', 'POL-10003', 'GRP-5003', '2024-01-01', '2024-12-31', 20.0, 1);
INSERT INTO hc_insurance VALUES (4, 'dave.wilson@email.com', 'Cigna', 'EPO Basic', 'POL-10004', 'GRP-5004', '2024-01-01', '2024-12-31', 35.0, 1);
INSERT INTO hc_insurance VALUES (5, 'eve.thompson@email.com', 'BlueCross BlueShield', 'PPO Silver', 'POL-10005', 'GRP-5001', '2024-01-01', '2024-12-31', 30.0, 1);
INSERT INTO hc_insurance VALUES (6, 'frank.garcia@email.com', 'Aetna', 'HMO Plus', 'POL-10006', 'GRP-5002', '2024-01-01', '2024-12-31', 25.0, 1);
INSERT INTO hc_insurance VALUES (7, 'grace.kim@email.com', 'Kaiser Permanente', 'HMO Standard', 'POL-10007', 'GRP-5005', '2024-01-01', '2024-12-31', 20.0, 1);
INSERT INTO hc_insurance VALUES (8, 'henry.patel@email.com', 'UnitedHealth', 'PPO Gold', 'POL-10008', 'GRP-5003', '2024-01-01', '2024-12-31', 25.0, 1);
INSERT INTO hc_insurance VALUES (9, 'ivy.santos@email.com', 'Cigna', 'EPO Plus', 'POL-10009', 'GRP-5004', '2024-01-01', '2024-12-31', 30.0, 1);
INSERT INTO hc_insurance VALUES (10, 'jack.murphy@email.com', 'BlueCross BlueShield', 'PPO Gold', 'POL-10010', 'GRP-5001', '2024-01-01', '2024-12-31', 25.0, 1);
INSERT INTO hc_insurance VALUES (11, 'kate.brown@email.com', 'Aetna', 'HMO Standard', 'POL-10011', 'GRP-5002', '2024-01-01', '2024-12-31', 30.0, 1);
INSERT INTO hc_insurance VALUES (12, 'leo.martinez@email.com', 'UnitedHealth', 'PPO Silver', 'POL-10012', 'GRP-5003', '2024-01-01', '2024-12-31', 35.0, 1);

-- =============================================
-- hc_billing (18 rows) — billing records
-- =============================================
CREATE TABLE hc_billing (
    bill_id INTEGER PRIMARY KEY,
    bill_patient_email TEXT NOT NULL,
    bill_doctor_email TEXT,
    bill_service TEXT NOT NULL,
    bill_amount REAL NOT NULL,
    bill_insurance_covered REAL DEFAULT 0.0,
    bill_patient_owes REAL,
    bill_date TEXT NOT NULL,
    bill_due_date TEXT,
    bill_status TEXT DEFAULT 'pending',
    bill_notes TEXT
);

INSERT INTO hc_billing VALUES (1, 'alice.chen@email.com', 'dr.williams@healthfirst.com', 'Cardiac Checkup', 250.0, 200.0, 50.0, '2024-01-15', '2024-02-15', 'paid', NULL);
INSERT INTO hc_billing VALUES (2, 'bob.rivera@email.com', 'dr.lee@healthfirst.com', 'Chest X-Ray', 350.0, 280.0, 70.0, '2024-01-20', '2024-02-20', 'paid', NULL);
INSERT INTO hc_billing VALUES (3, 'carol.zhang@email.com', 'dr.adams@healthfirst.com', 'Knee Consultation', 200.0, 160.0, 40.0, '2024-02-05', '2024-03-05', 'paid', NULL);
INSERT INTO hc_billing VALUES (4, 'dave.wilson@email.com', 'dr.nguyen@healthfirst.com', 'Neurology Follow-up', 175.0, 140.0, 35.0, '2024-02-10', '2024-03-10', 'paid', NULL);
INSERT INTO hc_billing VALUES (5, 'eve.thompson@email.com', 'dr.clark@healthfirst.com', 'Dermatology Visit', 150.0, 120.0, 30.0, '2024-02-15', '2024-03-15', 'paid', NULL);
INSERT INTO hc_billing VALUES (6, 'frank.garcia@email.com', 'dr.brown@healthfirst.com', 'Appendectomy', 8500.0, 7650.0, 850.0, '2024-03-01', '2024-04-01', 'paid', 'Surgery + recovery');
INSERT INTO hc_billing VALUES (7, 'grace.kim@email.com', 'dr.taylor@healthfirst.com', 'Wellness Checkup', 150.0, 120.0, 30.0, '2024-03-10', '2024-04-10', 'paid', NULL);
INSERT INTO hc_billing VALUES (8, 'henry.patel@email.com', 'dr.williams@healthfirst.com', 'Echocardiogram', 800.0, 640.0, 160.0, '2024-03-15', '2024-04-15', 'paid', NULL);
INSERT INTO hc_billing VALUES (9, 'ivy.santos@email.com', 'dr.lee@healthfirst.com', 'Brain MRI', 1200.0, 960.0, 240.0, '2024-03-20', '2024-04-20', 'paid', NULL);
INSERT INTO hc_billing VALUES (10, 'jack.murphy@email.com', 'dr.nguyen@healthfirst.com', 'Neurology Consultation', 225.0, 180.0, 45.0, '2024-04-01', '2024-05-01', 'pending', NULL);
INSERT INTO hc_billing VALUES (11, 'kate.brown@email.com', 'dr.adams@healthfirst.com', 'Shoulder Follow-up', 175.0, 140.0, 35.0, '2024-04-10', '2024-05-10', 'paid', NULL);
INSERT INTO hc_billing VALUES (12, 'alice.chen@email.com', 'dr.lee@healthfirst.com', 'CT Chest', 950.0, 760.0, 190.0, '2024-04-15', '2024-05-15', 'paid', NULL);
INSERT INTO hc_billing VALUES (13, 'bob.rivera@email.com', 'dr.brown@healthfirst.com', 'Hernia Consultation', 200.0, 160.0, 40.0, '2024-05-01', '2024-06-01', 'pending', NULL);
INSERT INTO hc_billing VALUES (14, 'carol.zhang@email.com', 'dr.williams@healthfirst.com', 'BP Monitoring', 125.0, 100.0, 25.0, '2024-05-10', '2024-06-10', 'paid', NULL);
INSERT INTO hc_billing VALUES (15, 'dave.wilson@email.com', 'dr.lee@healthfirst.com', 'Brain MRI', 1200.0, 960.0, 240.0, '2024-05-15', '2024-06-15', 'pending', NULL);
INSERT INTO hc_billing VALUES (16, 'frank.garcia@email.com', 'dr.brown@healthfirst.com', 'Post-Op Follow-up', 125.0, 100.0, 25.0, '2024-06-10', '2024-07-10', 'paid', NULL);
INSERT INTO hc_billing VALUES (17, 'grace.kim@email.com', 'dr.clark@healthfirst.com', 'Mole Assessment', 175.0, 140.0, 35.0, '2024-06-15', '2024-07-15', 'pending', NULL);
INSERT INTO hc_billing VALUES (18, 'henry.patel@email.com', 'dr.nguyen@healthfirst.com', 'Nerve Conduction Test', 450.0, 360.0, 90.0, '2024-07-01', '2024-08-01', 'pending', NULL);

-- =============================================
-- hc_rooms (10 rows) — clinic rooms
-- =============================================
CREATE TABLE hc_rooms (
    room_id INTEGER PRIMARY KEY,
    room_number TEXT NOT NULL,
    room_floor INTEGER,
    room_type TEXT,
    room_dept_name TEXT,
    room_capacity INTEGER DEFAULT 1,
    room_equipment TEXT,
    room_is_active INTEGER DEFAULT 1
);

INSERT INTO hc_rooms VALUES (1, 'Room 101', 1, 'examination', 'Radiology', 1, 'X-ray machine', 1);
INSERT INTO hc_rooms VALUES (2, 'Room 102', 1, 'imaging', 'Radiology', 1, 'CT scanner, MRI machine', 1);
INSERT INTO hc_rooms VALUES (3, 'Room 108', 1, 'examination', 'Dermatology', 1, 'Dermatoscope, biopsy tools', 1);
INSERT INTO hc_rooms VALUES (4, 'Room 110', 1, 'examination', 'Pediatrics', 2, 'Pediatric equipment', 1);
INSERT INTO hc_rooms VALUES (5, 'Room 201', 2, 'examination', 'Cardiology', 1, 'ECG machine, echocardiogram', 1);
INSERT INTO hc_rooms VALUES (6, 'Room 205', 2, 'examination', 'Neurology', 1, 'EMG machine, reflex tools', 1);
INSERT INTO hc_rooms VALUES (7, 'Room 301', 3, 'examination', 'Orthopedics', 1, 'Bone density scanner', 1);
INSERT INTO hc_rooms VALUES (8, 'Room 305', 3, 'operating', 'Surgery', 1, 'Full surgical suite', 1);
INSERT INTO hc_rooms VALUES (9, 'Room 210', 2, 'laboratory', 'Internal Medicine', 2, 'Blood draw station', 1);
INSERT INTO hc_rooms VALUES (10, 'Room 115', 1, 'ultrasound', 'Radiology', 1, 'Ultrasound machine', 1);

-- =============================================
-- hc_surgeries (6 rows) — surgical procedures
-- =============================================
CREATE TABLE hc_surgeries (
    surg_id INTEGER PRIMARY KEY,
    surg_patient_email TEXT NOT NULL,
    surg_doctor_email TEXT NOT NULL,
    surg_nurse_email TEXT,
    surg_type TEXT NOT NULL,
    surg_description TEXT,
    surg_room TEXT,
    surg_date TEXT NOT NULL,
    surg_start_time TEXT,
    surg_end_time TEXT,
    surg_outcome TEXT DEFAULT 'successful',
    surg_complications TEXT,
    surg_notes TEXT
);

INSERT INTO hc_surgeries VALUES (1, 'frank.garcia@email.com', 'dr.brown@healthfirst.com', 'felix.lopez@healthfirst.com', 'Appendectomy', 'Laparoscopic appendectomy', 'Room 305', '2024-03-02', '08:00', '09:30', 'successful', 'None', 'Clean procedure');
INSERT INTO hc_surgeries VALUES (2, 'carol.zhang@email.com', 'dr.adams@healthfirst.com', 'clara.young@healthfirst.com', 'Arthroscopy', 'Right knee arthroscopic meniscal repair', 'Room 305', '2024-03-15', '10:00', '11:15', 'successful', 'None', 'Partial meniscectomy');
INSERT INTO hc_surgeries VALUES (3, 'eve.thompson@email.com', 'dr.clark@healthfirst.com', 'elena.wright@healthfirst.com', 'Biopsy', 'Skin punch biopsy left arm', 'Room 108', '2024-02-15', '14:00', '14:30', 'successful', 'None', 'Minimal procedure');
INSERT INTO hc_surgeries VALUES (4, 'jack.murphy@email.com', 'dr.clark@healthfirst.com', 'elena.wright@healthfirst.com', 'Biopsy', 'Skin shave biopsy back', 'Room 108', '2024-04-05', '15:00', '15:20', 'successful', 'None', 'Superficial shave');
INSERT INTO hc_surgeries VALUES (5, 'grace.kim@email.com', 'dr.clark@healthfirst.com', 'elena.wright@healthfirst.com', 'Excision', 'Skin lesion excision right forearm', 'Room 108', '2024-06-15', '13:00', '13:45', 'successful', 'None', 'Clear margins achieved');
INSERT INTO hc_surgeries VALUES (6, 'frank.garcia@email.com', 'dr.brown@healthfirst.com', 'felix.lopez@healthfirst.com', 'Hernia Repair', 'Inguinal hernia repair planned', 'Room 305', '2024-08-01', '08:00', '10:00', 'scheduled', NULL, 'Pre-op clearance obtained');

-- =============================================
-- hc_allergies (10 rows) — patient allergies
-- =============================================
CREATE TABLE hc_allergies (
    allergy_id INTEGER PRIMARY KEY,
    alg_patient_email TEXT NOT NULL,
    alg_allergen TEXT NOT NULL,
    alg_reaction TEXT,
    alg_severity TEXT DEFAULT 'moderate',
    alg_discovered_date TEXT,
    alg_notes TEXT
);

INSERT INTO hc_allergies VALUES (1, 'alice.chen@email.com', 'Penicillin', 'Rash', 'moderate', '2020-05-10', 'Confirmed allergy');
INSERT INTO hc_allergies VALUES (2, 'bob.rivera@email.com', 'Sulfa drugs', 'Hives', 'severe', '2021-02-15', 'Anaphylaxis risk');
INSERT INTO hc_allergies VALUES (3, 'carol.zhang@email.com', 'Latex', 'Skin irritation', 'mild', '2020-08-20', 'Use non-latex gloves');
INSERT INTO hc_allergies VALUES (4, 'dave.wilson@email.com', 'Aspirin', 'GI upset', 'moderate', '2022-03-10', 'Use acetaminophen instead');
INSERT INTO hc_allergies VALUES (5, 'eve.thompson@email.com', 'Shellfish', 'Swelling', 'severe', '2021-06-01', 'Carry EpiPen');
INSERT INTO hc_allergies VALUES (6, 'frank.garcia@email.com', 'Codeine', 'Nausea', 'mild', '2024-03-01', 'Discovered during surgery prep');
INSERT INTO hc_allergies VALUES (7, 'henry.patel@email.com', 'Iodine contrast', 'Hives', 'moderate', '2024-03-15', 'Pre-medicate before contrast CT');
INSERT INTO hc_allergies VALUES (8, 'jack.murphy@email.com', 'NSAIDs', 'GI bleeding', 'severe', '2023-05-20', 'History of GI bleed');
INSERT INTO hc_allergies VALUES (9, 'alice.chen@email.com', 'Bee stings', 'Anaphylaxis', 'severe', '2019-08-15', 'Carry EpiPen');
INSERT INTO hc_allergies VALUES (10, 'grace.kim@email.com', 'Amoxicillin', 'Rash', 'mild', '2022-11-10', 'Mild reaction');

-- =============================================
-- hc_lab_orders (12 rows) — lab test orders
-- =============================================
CREATE TABLE hc_lab_orders (
    lo_id INTEGER PRIMARY KEY,
    lo_patient_email TEXT NOT NULL,
    lo_doctor_email TEXT NOT NULL,
    lo_test_name TEXT NOT NULL,
    lo_test_code TEXT,
    lo_priority TEXT DEFAULT 'routine',
    lo_order_date TEXT NOT NULL,
    lo_status TEXT DEFAULT 'ordered',
    lo_notes TEXT
);

INSERT INTO hc_lab_orders VALUES (1, 'alice.chen@email.com', 'dr.williams@healthfirst.com', 'Complete Blood Count', 'CBC', 'routine', '2024-01-15', 'completed', 'Annual labs');
INSERT INTO hc_lab_orders VALUES (2, 'bob.rivera@email.com', 'dr.williams@healthfirst.com', 'Lipid Panel', 'LIPID', 'routine', '2024-01-20', 'completed', 'Fasting required');
INSERT INTO hc_lab_orders VALUES (3, 'eve.thompson@email.com', 'dr.clark@healthfirst.com', 'Comprehensive Metabolic Panel', 'CMP', 'routine', '2024-02-15', 'completed', 'Annual labs');
INSERT INTO hc_lab_orders VALUES (4, 'henry.patel@email.com', 'dr.williams@healthfirst.com', 'Thyroid Panel', 'THYROID', 'stat', '2024-03-15', 'completed', 'Suspected hypothyroidism');
INSERT INTO hc_lab_orders VALUES (5, 'alice.chen@email.com', 'dr.williams@healthfirst.com', 'Basic Metabolic Panel', 'BMP', 'routine', '2024-04-15', 'completed', 'Renal function check');
INSERT INTO hc_lab_orders VALUES (6, 'bob.rivera@email.com', 'dr.williams@healthfirst.com', 'HbA1c', 'HBA1C', 'routine', '2024-05-01', 'completed', 'Diabetes screening');
INSERT INTO hc_lab_orders VALUES (7, 'carol.zhang@email.com', 'dr.adams@healthfirst.com', 'ESR', 'ESR', 'routine', '2024-02-05', 'completed', 'Inflammation marker');
INSERT INTO hc_lab_orders VALUES (8, 'dave.wilson@email.com', 'dr.nguyen@healthfirst.com', 'Vitamin B12', 'B12', 'routine', '2024-05-15', 'completed', 'Neuropathy workup');
INSERT INTO hc_lab_orders VALUES (9, 'frank.garcia@email.com', 'dr.brown@healthfirst.com', 'CBC with Diff', 'CBCD', 'stat', '2024-03-01', 'completed', 'Pre-surgery');
INSERT INTO hc_lab_orders VALUES (10, 'grace.kim@email.com', 'dr.taylor@healthfirst.com', 'Vitamin D Level', 'VITD', 'routine', '2024-03-10', 'completed', 'Fatigue workup');
INSERT INTO hc_lab_orders VALUES (11, 'jack.murphy@email.com', 'dr.nguyen@healthfirst.com', 'Nerve Conduction Study', 'NCS', 'routine', '2024-04-01', 'pending', 'Peripheral neuropathy');
INSERT INTO hc_lab_orders VALUES (12, 'ivy.santos@email.com', 'dr.lee@healthfirst.com', 'CBC', 'CBC', 'routine', '2024-03-20', 'completed', 'Routine labs');

-- =============================================
-- hc_referrals (8 rows) — inter-department referrals
-- =============================================
CREATE TABLE hc_referrals (
    ref_id INTEGER PRIMARY KEY,
    ref_patient_email TEXT NOT NULL,
    ref_from_doctor_email TEXT NOT NULL,
    ref_to_doctor_email TEXT NOT NULL,
    ref_reason TEXT NOT NULL,
    ref_priority TEXT DEFAULT 'routine',
    ref_date TEXT NOT NULL,
    ref_status TEXT DEFAULT 'pending',
    ref_notes TEXT
);

INSERT INTO hc_referrals VALUES (1, 'alice.chen@email.com', 'dr.williams@healthfirst.com', 'dr.lee@healthfirst.com', 'CT chest for cardiac workup', 'urgent', '2024-04-10', 'completed', 'Rule out PE');
INSERT INTO hc_referrals VALUES (2, 'carol.zhang@email.com', 'dr.adams@healthfirst.com', 'dr.lee@healthfirst.com', 'MRI knee for surgical planning', 'routine', '2024-02-06', 'completed', 'Meniscal evaluation');
INSERT INTO hc_referrals VALUES (3, 'dave.wilson@email.com', 'dr.nguyen@healthfirst.com', 'dr.lee@healthfirst.com', 'Brain MRI for headache workup', 'routine', '2024-05-10', 'completed', 'Rule out structural cause');
INSERT INTO hc_referrals VALUES (4, 'frank.garcia@email.com', 'dr.brown@healthfirst.com', 'dr.lee@healthfirst.com', 'CT abdomen for appendicitis', 'stat', '2024-03-01', 'completed', 'Acute abdomen');
INSERT INTO hc_referrals VALUES (5, 'grace.kim@email.com', 'dr.taylor@healthfirst.com', 'dr.clark@healthfirst.com', 'Dermatology for skin lesion', 'routine', '2024-06-01', 'completed', 'Suspicious mole');
INSERT INTO hc_referrals VALUES (6, 'henry.patel@email.com', 'dr.williams@healthfirst.com', 'dr.nguyen@healthfirst.com', 'Neurology for tingling', 'routine', '2024-06-15', 'pending', 'Peripheral symptoms');
INSERT INTO hc_referrals VALUES (7, 'jack.murphy@email.com', 'dr.nguyen@healthfirst.com', 'dr.adams@healthfirst.com', 'Orthopedics for back pain', 'routine', '2024-04-05', 'completed', 'Spine evaluation');
INSERT INTO hc_referrals VALUES (8, 'bob.rivera@email.com', 'dr.williams@healthfirst.com', 'dr.brown@healthfirst.com', 'Surgery for hernia evaluation', 'routine', '2024-04-25', 'completed', 'Inguinal hernia');

-- =============================================
-- hc_medications (10 rows) — medication catalog
-- =============================================
CREATE TABLE hc_medications (
    med_id INTEGER PRIMARY KEY,
    med_name TEXT NOT NULL,
    med_generic_name TEXT,
    med_category TEXT,
    med_form TEXT,
    med_manufacturer TEXT,
    med_requires_rx INTEGER DEFAULT 1,
    med_is_controlled INTEGER DEFAULT 0,
    med_schedule TEXT
);

INSERT INTO hc_medications VALUES (1, 'Lisinopril', 'Lisinopril', 'ACE Inhibitor', 'Tablet', 'Lupin Pharma', 1, 0, NULL);
INSERT INTO hc_medications VALUES (2, 'Atorvastatin', 'Atorvastatin', 'Statin', 'Tablet', 'Pfizer', 1, 0, NULL);
INSERT INTO hc_medications VALUES (3, 'Ibuprofen', 'Ibuprofen', 'NSAID', 'Tablet', 'Advil', 0, 0, NULL);
INSERT INTO hc_medications VALUES (4, 'Sumatriptan', 'Sumatriptan', 'Triptan', 'Tablet', 'GlaxoSmithKline', 1, 0, NULL);
INSERT INTO hc_medications VALUES (5, 'Hydrocortisone', 'Hydrocortisone', 'Corticosteroid', 'Cream', 'Teva Pharma', 0, 0, NULL);
INSERT INTO hc_medications VALUES (6, 'Amoxicillin', 'Amoxicillin', 'Antibiotic', 'Capsule', 'Sandoz', 1, 0, NULL);
INSERT INTO hc_medications VALUES (7, 'Gabapentin', 'Gabapentin', 'Anticonvulsant', 'Capsule', 'Pfizer', 1, 0, 'Schedule V');
INSERT INTO hc_medications VALUES (8, 'Levothyroxine', 'Levothyroxine', 'Thyroid Hormone', 'Tablet', 'AbbVie', 1, 0, NULL);
INSERT INTO hc_medications VALUES (9, 'Metoprolol', 'Metoprolol', 'Beta Blocker', 'Tablet', 'AstraZeneca', 1, 0, NULL);
INSERT INTO hc_medications VALUES (10, 'Aspirin', 'Acetylsalicylic Acid', 'NSAID', 'Tablet', 'Bayer', 0, 0, NULL);

-- =============================================
-- hc_patient_contacts (8 rows) — emergency contacts
-- =============================================
CREATE TABLE hc_patient_contacts (
    pc_id INTEGER PRIMARY KEY,
    pc_patient_email TEXT NOT NULL,
    pc_contact_name TEXT NOT NULL,
    pc_relationship TEXT,
    pc_phone TEXT NOT NULL,
    pc_email TEXT,
    pc_is_primary INTEGER DEFAULT 1
);

INSERT INTO hc_patient_contacts VALUES (1, 'alice.chen@email.com', 'Bob Chen', 'Spouse', '555-0901', 'bob.chen@email.com', 1);
INSERT INTO hc_patient_contacts VALUES (2, 'bob.rivera@email.com', 'Maria Rivera', 'Wife', '555-0902', 'maria.r@email.com', 1);
INSERT INTO hc_patient_contacts VALUES (3, 'carol.zhang@email.com', 'Dan Zhang', 'Husband', '555-0903', 'dan.z@email.com', 1);
INSERT INTO hc_patient_contacts VALUES (4, 'dave.wilson@email.com', 'Sue Wilson', 'Wife', '555-0904', 'sue.w@email.com', 1);
INSERT INTO hc_patient_contacts VALUES (5, 'eve.thompson@email.com', 'Tom Thompson', 'Father', '555-0905', 'tom.t@email.com', 1);
INSERT INTO hc_patient_contacts VALUES (6, 'frank.garcia@email.com', 'Rosa Garcia', 'Wife', '555-0906', 'rosa.g@email.com', 1);
INSERT INTO hc_patient_contacts VALUES (7, 'grace.kim@email.com', 'James Kim', 'Husband', '555-0907', 'james.k@email.com', 1);
INSERT INTO hc_patient_contacts VALUES (8, 'henry.patel@email.com', 'Priya Patel', 'Wife', '555-0908', 'priya.p@email.com', 1);

-- =============================================
-- hc_medical_history (14 rows) — past medical history
-- =============================================
CREATE TABLE hc_medical_history (
    mh_id INTEGER PRIMARY KEY,
    mh_patient_email TEXT NOT NULL,
    mh_condition TEXT NOT NULL,
    mh_onset_date TEXT,
    mh_resolved_date TEXT,
    mh_is_chronic INTEGER DEFAULT 0,
    mh_notes TEXT
);

INSERT INTO hc_medical_history VALUES (1, 'alice.chen@email.com', 'Childhood asthma', '2000-01-01', '2008-06-15', 0, 'Outgrown');
INSERT INTO hc_medical_history VALUES (2, 'alice.chen@email.com', 'Hypertension', '2024-01-15', NULL, 1, 'Current medication');
INSERT INTO hc_medical_history VALUES (3, 'bob.rivera@email.com', 'Hyperlipidemia', '2024-01-20', NULL, 1, 'On statin therapy');
INSERT INTO hc_medical_history VALUES (4, 'carol.zhang@email.com', 'Broken arm', '2015-07-10', '2015-09-15', 0, 'Left radius fracture');
INSERT INTO hc_medical_history VALUES (5, 'dave.wilson@email.com', 'Migraines', '2020-03-01', NULL, 1, 'Chronic with aura');
INSERT INTO hc_medical_history VALUES (6, 'eve.thompson@email.com', 'Tonsillectomy', '2005-04-20', '2005-05-10', 0, 'Age 10');
INSERT INTO hc_medical_history VALUES (7, 'frank.garcia@email.com', 'Appendicitis', '2024-03-01', '2024-03-15', 0, 'Surgical removal');
INSERT INTO hc_medical_history VALUES (8, 'grace.kim@email.com', 'Vitamin D deficiency', '2024-03-10', NULL, 1, 'On supplements');
INSERT INTO hc_medical_history VALUES (9, 'henry.patel@email.com', 'Hypothyroidism', '2024-03-15', NULL, 1, 'On levothyroxine');
INSERT INTO hc_medical_history VALUES (10, 'jack.murphy@email.com', 'Type 2 Diabetes', '2020-06-01', NULL, 1, 'Diet controlled');
INSERT INTO hc_medical_history VALUES (11, 'jack.murphy@email.com', 'Peripheral neuropathy', '2024-04-01', NULL, 1, 'Under investigation');
INSERT INTO hc_medical_history VALUES (12, 'kate.brown@email.com', 'ACL reconstruction', '2018-09-15', '2019-03-01', 0, 'Right knee, full recovery');
INSERT INTO hc_medical_history VALUES (13, 'bob.rivera@email.com', 'Hypertension', '2024-01-20', NULL, 1, 'Monitoring');
INSERT INTO hc_medical_history VALUES (14, 'leo.martinez@email.com', 'GERD', '2022-05-01', NULL, 1, 'On PPI therapy');

-- =============================================
-- hc_immunizations (12 rows) — vaccination records
-- =============================================
CREATE TABLE hc_immunizations (
    imm_id INTEGER PRIMARY KEY,
    imm_patient_email TEXT NOT NULL,
    imm_vaccine TEXT NOT NULL,
    imm_dose_number INTEGER DEFAULT 1,
    imm_date TEXT NOT NULL,
    imm_administered_by TEXT,
    imm_lot_number TEXT,
    imm_site TEXT,
    imm_notes TEXT
);

INSERT INTO hc_immunizations VALUES (1, 'alice.chen@email.com', 'Influenza', 1, '2024-01-15', 'anna.scott@healthfirst.com', 'LOT-FLU-2401', 'Left deltoid', 'Annual flu shot');
INSERT INTO hc_immunizations VALUES (2, 'bob.rivera@email.com', 'Influenza', 1, '2024-01-20', 'anna.scott@healthfirst.com', 'LOT-FLU-2401', 'Left deltoid', 'Annual flu shot');
INSERT INTO hc_immunizations VALUES (3, 'carol.zhang@email.com', 'Tdap', 1, '2024-02-05', 'clara.young@healthfirst.com', 'LOT-TDAP-2402', 'Right deltoid', '10-year booster');
INSERT INTO hc_immunizations VALUES (4, 'dave.wilson@email.com', 'COVID-19 Booster', 3, '2024-02-10', 'derek.king@healthfirst.com', 'LOT-COV-2403', 'Left deltoid', 'Updated booster');
INSERT INTO hc_immunizations VALUES (5, 'eve.thompson@email.com', 'Influenza', 1, '2024-02-15', 'elena.wright@healthfirst.com', 'LOT-FLU-2401', 'Left deltoid', 'Annual flu shot');
INSERT INTO hc_immunizations VALUES (6, 'frank.garcia@email.com', 'Tetanus', 1, '2024-03-01', 'felix.lopez@healthfirst.com', 'LOT-TET-2404', 'Right deltoid', 'Pre-surgery update');
INSERT INTO hc_immunizations VALUES (7, 'grace.kim@email.com', 'HPV', 2, '2024-03-10', 'gina.allen@healthfirst.com', 'LOT-HPV-2405', 'Left deltoid', 'Second dose');
INSERT INTO hc_immunizations VALUES (8, 'henry.patel@email.com', 'Hepatitis B', 3, '2024-03-15', 'hugo.baker@healthfirst.com', 'LOT-HEPB-2406', 'Right deltoid', 'Third dose series');
INSERT INTO hc_immunizations VALUES (9, 'ivy.santos@email.com', 'Influenza', 1, '2024-03-20', 'iris.carter@healthfirst.com', 'LOT-FLU-2407', 'Left deltoid', 'Annual flu shot');
INSERT INTO hc_immunizations VALUES (10, 'jack.murphy@email.com', 'Pneumococcal', 1, '2024-04-01', 'derek.king@healthfirst.com', 'LOT-PCV-2408', 'Left deltoid', 'Age-related recommendation');
INSERT INTO hc_immunizations VALUES (11, 'kate.brown@email.com', 'Influenza', 1, '2024-04-10', 'clara.young@healthfirst.com', 'LOT-FLU-2409', 'Left deltoid', 'Annual flu shot');
INSERT INTO hc_immunizations VALUES (12, 'leo.martinez@email.com', 'COVID-19 Booster', 4, '2024-07-10', 'anna.scott@healthfirst.com', 'LOT-COV-2410', 'Right deltoid', 'Latest booster');

-- =============================================
-- hc_ward_beds (10 rows) — ward/bed assignments
-- =============================================
CREATE TABLE hc_ward_beds (
    bed_id INTEGER PRIMARY KEY,
    bed_ward TEXT NOT NULL,
    bed_number TEXT NOT NULL,
    bed_floor INTEGER,
    bed_type TEXT DEFAULT 'standard',
    bed_is_occupied INTEGER DEFAULT 0,
    bed_patient_email TEXT,
    bed_admit_date TEXT,
    bed_notes TEXT
);

INSERT INTO hc_ward_beds VALUES (1, 'General Ward', 'GW-101', 1, 'standard', 0, NULL, NULL, NULL);
INSERT INTO hc_ward_beds VALUES (2, 'General Ward', 'GW-102', 1, 'standard', 1, 'frank.garcia@email.com', '2024-03-01', 'Post-appendectomy');
INSERT INTO hc_ward_beds VALUES (3, 'General Ward', 'GW-103', 1, 'standard', 0, NULL, NULL, NULL);
INSERT INTO hc_ward_beds VALUES (4, 'ICU', 'ICU-201', 2, 'icu', 0, NULL, NULL, NULL);
INSERT INTO hc_ward_beds VALUES (5, 'ICU', 'ICU-202', 2, 'icu', 0, NULL, NULL, NULL);
INSERT INTO hc_ward_beds VALUES (6, 'Maternity', 'MAT-301', 3, 'maternity', 0, NULL, NULL, NULL);
INSERT INTO hc_ward_beds VALUES (7, 'Maternity', 'MAT-302', 3, 'maternity', 0, NULL, NULL, NULL);
INSERT INTO hc_ward_beds VALUES (8, 'Surgical', 'SR-401', 4, 'post-op', 0, NULL, NULL, NULL);
INSERT INTO hc_ward_beds VALUES (9, 'Surgical', 'SR-402', 4, 'post-op', 1, 'carol.zhang@email.com', '2024-03-15', 'Post-arthroscopy recovery');
INSERT INTO hc_ward_beds VALUES (10, 'Pediatric', 'PED-501', 5, 'pediatric', 0, NULL, NULL, NULL);

-- =============================================
-- hc_shifts (10 rows) — staff shift schedule
-- =============================================
CREATE TABLE hc_shifts (
    shift_id INTEGER PRIMARY KEY,
    shft_staff_email TEXT NOT NULL,
    shft_staff_role TEXT NOT NULL,
    shft_dept_name TEXT,
    shft_date TEXT NOT NULL,
    shft_start TEXT NOT NULL,
    shft_end TEXT NOT NULL,
    shft_type TEXT DEFAULT 'regular',
    shft_notes TEXT
);

INSERT INTO hc_shifts VALUES (1, 'anna.scott@healthfirst.com', 'Nurse', 'Cardiology', '2024-01-15', '07:00', '15:00', 'day', NULL);
INSERT INTO hc_shifts VALUES (2, 'brian.hall@healthfirst.com', 'Nurse', 'Radiology', '2024-01-15', '23:00', '07:00', 'night', NULL);
INSERT INTO hc_shifts VALUES (3, 'clara.young@healthfirst.com', 'Nurse', 'Orthopedics', '2024-02-05', '07:00', '15:00', 'day', NULL);
INSERT INTO hc_shifts VALUES (4, 'dr.williams@healthfirst.com', 'Doctor', 'Cardiology', '2024-01-15', '08:00', '17:00', 'day', 'Regular clinic');
INSERT INTO hc_shifts VALUES (5, 'dr.lee@healthfirst.com', 'Doctor', 'Radiology', '2024-01-20', '08:00', '17:00', 'day', 'Regular clinic');
INSERT INTO hc_shifts VALUES (6, 'felix.lopez@healthfirst.com', 'Nurse', 'Surgery', '2024-03-02', '06:00', '14:00', 'day', 'Surgery assist');
INSERT INTO hc_shifts VALUES (7, 'dr.brown@healthfirst.com', 'Doctor', 'Surgery', '2024-03-02', '07:00', '16:00', 'day', 'Surgery day');
INSERT INTO hc_shifts VALUES (8, 'iris.carter@healthfirst.com', 'Nurse', 'Emergency', '2024-03-20', '23:00', '07:00', 'night', 'ER coverage');
INSERT INTO hc_shifts VALUES (9, 'gina.allen@healthfirst.com', 'Nurse', 'Pediatrics', '2024-03-10', '07:00', '15:00', 'day', NULL);
INSERT INTO hc_shifts VALUES (10, 'derek.king@healthfirst.com', 'Nurse', 'Neurology', '2024-04-01', '23:00', '07:00', 'night', NULL);

-- =============================================
-- hc_consent_forms (8 rows) — patient consent records
-- =============================================
CREATE TABLE hc_consent_forms (
    cf_id INTEGER PRIMARY KEY,
    cf_patient_email TEXT NOT NULL,
    cf_procedure TEXT NOT NULL,
    cf_doctor_email TEXT NOT NULL,
    cf_signed_date TEXT NOT NULL,
    cf_witness TEXT,
    cf_form_type TEXT DEFAULT 'procedure',
    cf_status TEXT DEFAULT 'signed',
    cf_notes TEXT
);

INSERT INTO hc_consent_forms VALUES (1, 'frank.garcia@email.com', 'Appendectomy', 'dr.brown@healthfirst.com', '2024-03-01', 'Rosa Garcia', 'surgery', 'signed', 'Pre-op consent');
INSERT INTO hc_consent_forms VALUES (2, 'carol.zhang@email.com', 'Knee Arthroscopy', 'dr.adams@healthfirst.com', '2024-03-14', 'Dan Zhang', 'surgery', 'signed', 'Pre-op consent');
INSERT INTO hc_consent_forms VALUES (3, 'eve.thompson@email.com', 'Skin Biopsy', 'dr.clark@healthfirst.com', '2024-02-15', NULL, 'procedure', 'signed', 'Minor procedure');
INSERT INTO hc_consent_forms VALUES (4, 'jack.murphy@email.com', 'Skin Biopsy', 'dr.clark@healthfirst.com', '2024-04-05', NULL, 'procedure', 'signed', 'Minor procedure');
INSERT INTO hc_consent_forms VALUES (5, 'grace.kim@email.com', 'Skin Excision', 'dr.clark@healthfirst.com', '2024-06-15', 'James Kim', 'surgery', 'signed', 'Excisional biopsy');
INSERT INTO hc_consent_forms VALUES (6, 'alice.chen@email.com', 'CT with Contrast', 'dr.lee@healthfirst.com', '2024-04-15', NULL, 'imaging', 'signed', 'Contrast consent');
INSERT INTO hc_consent_forms VALUES (7, 'ivy.santos@email.com', 'MRI with Contrast', 'dr.lee@healthfirst.com', '2024-03-20', NULL, 'imaging', 'signed', 'Gadolinium consent');
INSERT INTO hc_consent_forms VALUES (8, 'frank.garcia@email.com', 'Hernia Repair', 'dr.brown@healthfirst.com', '2024-07-25', 'Rosa Garcia', 'surgery', 'signed', 'Pre-op consent');

-- =============================================
-- hc_follow_ups (10 rows) — follow-up tracking
-- =============================================
CREATE TABLE hc_follow_ups (
    fu_id INTEGER PRIMARY KEY,
    fu_patient_email TEXT NOT NULL,
    fu_doctor_email TEXT NOT NULL,
    fu_original_visit_date TEXT,
    fu_scheduled_date TEXT NOT NULL,
    fu_reason TEXT,
    fu_status TEXT DEFAULT 'scheduled',
    fu_notes TEXT
);

INSERT INTO hc_follow_ups VALUES (1, 'alice.chen@email.com', 'dr.williams@healthfirst.com', '2024-01-15', '2024-04-15', 'BP recheck', 'completed', '3-month follow-up');
INSERT INTO hc_follow_ups VALUES (2, 'bob.rivera@email.com', 'dr.williams@healthfirst.com', '2024-01-20', '2024-04-20', 'Lipid recheck', 'completed', '3-month labs');
INSERT INTO hc_follow_ups VALUES (3, 'carol.zhang@email.com', 'dr.adams@healthfirst.com', '2024-03-15', '2024-06-15', 'Post-surgery knee eval', 'scheduled', '3-month post-op');
INSERT INTO hc_follow_ups VALUES (4, 'dave.wilson@email.com', 'dr.nguyen@healthfirst.com', '2024-02-10', '2024-05-10', 'Migraine management', 'completed', 'Medication review');
INSERT INTO hc_follow_ups VALUES (5, 'frank.garcia@email.com', 'dr.brown@healthfirst.com', '2024-03-02', '2024-06-10', 'Post-appendectomy', 'completed', '3-month check');
INSERT INTO hc_follow_ups VALUES (6, 'henry.patel@email.com', 'dr.williams@healthfirst.com', '2024-03-15', '2024-06-15', 'Thyroid recheck', 'scheduled', 'Repeat TSH');
INSERT INTO hc_follow_ups VALUES (7, 'ivy.santos@email.com', 'dr.lee@healthfirst.com', '2024-03-20', '2024-09-20', 'Brain MRI follow-up', 'scheduled', '6-month recheck');
INSERT INTO hc_follow_ups VALUES (8, 'jack.murphy@email.com', 'dr.nguyen@healthfirst.com', '2024-04-01', '2024-07-01', 'Neuropathy follow-up', 'scheduled', 'NCS results review');
INSERT INTO hc_follow_ups VALUES (9, 'kate.brown@email.com', 'dr.adams@healthfirst.com', '2024-04-10', '2024-07-10', 'Shoulder recheck', 'scheduled', '3-month follow-up');
INSERT INTO hc_follow_ups VALUES (10, 'grace.kim@email.com', 'dr.clark@healthfirst.com', '2024-06-15', '2024-09-15', 'BCC post-excision check', 'scheduled', '3-month surveillance');

-- =============================================
-- hc_clinic_notes (10 rows) — doctor clinical notes
-- =============================================
CREATE TABLE hc_clinic_notes (
    cn_id INTEGER PRIMARY KEY,
    cn_patient_email TEXT NOT NULL,
    cn_doctor_email TEXT NOT NULL,
    cn_date TEXT NOT NULL,
    cn_type TEXT DEFAULT 'progress',
    cn_subjective TEXT,
    cn_objective TEXT,
    cn_assessment TEXT,
    cn_plan TEXT,
    cn_is_signed INTEGER DEFAULT 0
);

INSERT INTO hc_clinic_notes VALUES (1, 'alice.chen@email.com', 'dr.williams@healthfirst.com', '2024-01-15', 'initial', 'Patient reports occasional headaches', 'BP 138/88, HR 72', 'Stage 1 hypertension', 'Start Lisinopril 10mg daily, recheck in 3 months', 1);
INSERT INTO hc_clinic_notes VALUES (2, 'bob.rivera@email.com', 'dr.williams@healthfirst.com', '2024-01-20', 'initial', 'No symptoms, routine screening', 'BP 142/92, Weight 95kg', 'Hyperlipidemia with HTN', 'Start Atorvastatin 20mg, low-sodium diet', 1);
INSERT INTO hc_clinic_notes VALUES (3, 'carol.zhang@email.com', 'dr.adams@healthfirst.com', '2024-02-05', 'initial', 'Right knee pain worsening over 3 months', 'Tenderness medial joint line, McMurray positive', 'OA right knee with possible meniscal tear', 'NSAIDs, physical therapy, MRI ordered', 1);
INSERT INTO hc_clinic_notes VALUES (4, 'dave.wilson@email.com', 'dr.nguyen@healthfirst.com', '2024-02-10', 'follow-up', 'Migraines occurring 3-4 times per month', 'Neuro exam normal', 'Chronic migraine with aura', 'Continue Sumatriptan PRN, add Topiramate prophylaxis', 1);
INSERT INTO hc_clinic_notes VALUES (5, 'frank.garcia@email.com', 'dr.brown@healthfirst.com', '2024-03-01', 'emergency', 'Acute RLQ pain x 12 hours, nausea', 'Tenderness RLQ, rebound positive, fever 100.2F', 'Acute appendicitis', 'Emergent appendectomy, IV antibiotics', 1);
INSERT INTO hc_clinic_notes VALUES (6, 'grace.kim@email.com', 'dr.taylor@healthfirst.com', '2024-03-10', 'wellness', 'Fatigue and low energy for 2 months', 'PE unremarkable', 'Vitamin D deficiency suspected', 'Check vitamin D level, start supplementation', 1);
INSERT INTO hc_clinic_notes VALUES (7, 'henry.patel@email.com', 'dr.williams@healthfirst.com', '2024-03-15', 'initial', 'Weight gain and cold intolerance', 'Thyroid non-tender, no nodules', 'Subclinical hypothyroidism', 'Start Levothyroxine 50mcg, recheck TSH in 6 weeks', 1);
INSERT INTO hc_clinic_notes VALUES (8, 'jack.murphy@email.com', 'dr.nguyen@healthfirst.com', '2024-04-01', 'initial', 'Numbness and tingling in feet bilateral', 'Decreased sensation stocking distribution', 'Peripheral polyneuropathy', 'NCS ordered, Gabapentin started, B12 check', 1);
INSERT INTO hc_clinic_notes VALUES (9, 'kate.brown@email.com', 'dr.adams@healthfirst.com', '2024-04-10', 'follow-up', 'Left shoulder pain with overhead activity', 'Positive impingement signs, MRI shows tendinosis', 'Rotator cuff tendinitis', 'Physical therapy, NSAIDs, avoid overhead lifting', 1);
INSERT INTO hc_clinic_notes VALUES (10, 'frank.garcia@email.com', 'dr.brown@healthfirst.com', '2024-06-10', 'follow-up', 'Doing well post-appendectomy, new inguinal bulge', 'Inguinal hernia palpable on exam', 'Inguinal hernia, post-appendectomy recovery good', 'Schedule hernia repair, continue recovery', 1);

-- =============================================
-- hc_procedures (8 rows) — non-surgical procedure log
-- =============================================
CREATE TABLE hc_procedures (
    proc_id INTEGER PRIMARY KEY,
    proc_patient_email TEXT NOT NULL,
    proc_doctor_email TEXT NOT NULL,
    proc_nurse_email TEXT,
    proc_name TEXT NOT NULL,
    proc_type TEXT,
    proc_room TEXT,
    proc_date TEXT NOT NULL,
    proc_duration_min INTEGER,
    proc_outcome TEXT DEFAULT 'completed',
    proc_notes TEXT
);

INSERT INTO hc_procedures VALUES (1, 'alice.chen@email.com', 'dr.williams@healthfirst.com', 'anna.scott@healthfirst.com', 'ECG', 'diagnostic', 'Room 201', '2024-01-15', 15, 'completed', 'Normal sinus rhythm');
INSERT INTO hc_procedures VALUES (2, 'henry.patel@email.com', 'dr.williams@healthfirst.com', 'anna.scott@healthfirst.com', 'Echocardiogram', 'diagnostic', 'Room 201', '2024-03-15', 45, 'completed', 'Normal EF 60%');
INSERT INTO hc_procedures VALUES (3, 'bob.rivera@email.com', 'dr.lee@healthfirst.com', 'brian.hall@healthfirst.com', 'Chest X-Ray', 'imaging', 'Room 101', '2024-01-20', 10, 'completed', 'Standard PA/LAT');
INSERT INTO hc_procedures VALUES (4, 'alice.chen@email.com', 'dr.lee@healthfirst.com', 'brian.hall@healthfirst.com', 'CT Chest', 'imaging', 'Room 102', '2024-04-15', 30, 'completed', 'With IV contrast');
INSERT INTO hc_procedures VALUES (5, 'ivy.santos@email.com', 'dr.lee@healthfirst.com', 'brian.hall@healthfirst.com', 'Brain MRI', 'imaging', 'Room 102', '2024-03-20', 45, 'completed', 'With gadolinium');
INSERT INTO hc_procedures VALUES (6, 'carol.zhang@email.com', 'dr.williams@healthfirst.com', 'anna.scott@healthfirst.com', 'Blood Pressure Monitoring', 'diagnostic', 'Room 201', '2024-05-10', 20, 'completed', '24-hour ABPM setup');
INSERT INTO hc_procedures VALUES (7, 'grace.kim@email.com', 'dr.taylor@healthfirst.com', 'gina.allen@healthfirst.com', 'Abdominal Ultrasound', 'imaging', 'Room 115', '2024-03-10', 30, 'completed', 'Fasting study');
INSERT INTO hc_procedures VALUES (8, 'jack.murphy@email.com', 'dr.nguyen@healthfirst.com', 'derek.king@healthfirst.com', 'EMG', 'diagnostic', 'Room 205', '2024-04-01', 40, 'completed', 'Upper and lower extremity');

-- =============================================
-- hc_equipment (8 rows) — medical equipment inventory
-- =============================================
CREATE TABLE hc_equipment (
    eq_id INTEGER PRIMARY KEY,
    eq_name TEXT NOT NULL,
    eq_type TEXT,
    eq_serial_no TEXT,
    eq_dept_name TEXT,
    eq_room TEXT,
    eq_purchase_date TEXT,
    eq_last_service TEXT,
    eq_next_service TEXT,
    eq_status TEXT DEFAULT 'operational',
    eq_notes TEXT
);

INSERT INTO hc_equipment VALUES (1, 'GE Optima XR240', 'X-Ray Machine', 'SN-XR-001', 'Radiology', 'Room 101', '2020-06-15', '2024-01-10', '2024-07-10', 'operational', 'Digital radiography');
INSERT INTO hc_equipment VALUES (2, 'Siemens SOMATOM', 'CT Scanner', 'SN-CT-001', 'Radiology', 'Room 102', '2021-03-20', '2024-02-15', '2024-08-15', 'operational', '128-slice CT');
INSERT INTO hc_equipment VALUES (3, 'GE SIGNA Premier', 'MRI Machine', 'SN-MR-001', 'Radiology', 'Room 102', '2021-09-01', '2024-03-01', '2024-09-01', 'operational', '3T MRI');
INSERT INTO hc_equipment VALUES (4, 'Philips EPIQ 7', 'Ultrasound', 'SN-US-001', 'Radiology', 'Room 115', '2022-01-10', '2024-01-15', '2024-07-15', 'operational', 'General purpose');
INSERT INTO hc_equipment VALUES (5, 'GE MAC 5500', 'ECG Machine', 'SN-ECG-001', 'Cardiology', 'Room 201', '2020-03-01', '2024-02-01', '2024-08-01', 'operational', '12-lead ECG');
INSERT INTO hc_equipment VALUES (6, 'Philips EPIQ CVx', 'Echocardiogram', 'SN-ECHO-001', 'Cardiology', 'Room 201', '2021-06-15', '2024-03-15', '2024-09-15', 'operational', 'Cardiac ultrasound');
INSERT INTO hc_equipment VALUES (7, 'Natus Nicolet EDX', 'EMG Machine', 'SN-EMG-001', 'Neurology', 'Room 205', '2022-04-01', '2024-01-20', '2024-07-20', 'operational', 'EMG/NCS system');
INSERT INTO hc_equipment VALUES (8, 'Hologic Horizon', 'Bone Density Scanner', 'SN-DEXA-001', 'Orthopedics', 'Room 301', '2022-08-15', '2024-02-20', '2024-08-20', 'operational', 'DEXA scanner');

-- =============================================
-- hc_pharmacy_inventory (10 rows) — pharmacy stock
-- =============================================
CREATE TABLE hc_pharmacy_inventory (
    inv_id INTEGER PRIMARY KEY,
    inv_medication_name TEXT NOT NULL,
    inv_dosage TEXT,
    inv_form TEXT,
    inv_quantity INTEGER NOT NULL,
    inv_unit TEXT DEFAULT 'tablets',
    inv_batch_no TEXT,
    inv_expiry_date TEXT,
    inv_reorder_level INTEGER DEFAULT 50,
    inv_supplier TEXT,
    inv_last_restocked TEXT
);

INSERT INTO hc_pharmacy_inventory VALUES (1, 'Lisinopril', '10mg', 'Tablet', 500, 'tablets', 'BATCH-LIS-001', '2025-06-30', 100, 'McKesson', '2024-01-05');
INSERT INTO hc_pharmacy_inventory VALUES (2, 'Atorvastatin', '20mg', 'Tablet', 400, 'tablets', 'BATCH-ATV-001', '2025-08-15', 80, 'Cardinal Health', '2024-02-10');
INSERT INTO hc_pharmacy_inventory VALUES (3, 'Amoxicillin', '500mg', 'Capsule', 300, 'capsules', 'BATCH-AMX-001', '2025-03-20', 60, 'McKesson', '2024-01-15');
INSERT INTO hc_pharmacy_inventory VALUES (4, 'Ibuprofen', '400mg', 'Tablet', 1000, 'tablets', 'BATCH-IBU-001', '2025-12-31', 200, 'AmerisourceBergen', '2024-03-01');
INSERT INTO hc_pharmacy_inventory VALUES (5, 'Sumatriptan', '50mg', 'Tablet', 150, 'tablets', 'BATCH-SUM-001', '2025-05-15', 30, 'Cardinal Health', '2024-01-20');
INSERT INTO hc_pharmacy_inventory VALUES (6, 'Gabapentin', '300mg', 'Capsule', 600, 'capsules', 'BATCH-GAB-001', '2025-09-30', 100, 'McKesson', '2024-02-15');
INSERT INTO hc_pharmacy_inventory VALUES (7, 'Levothyroxine', '50mcg', 'Tablet', 350, 'tablets', 'BATCH-LEV-001', '2025-07-20', 70, 'AmerisourceBergen', '2024-03-10');
INSERT INTO hc_pharmacy_inventory VALUES (8, 'Metoprolol', '25mg', 'Tablet', 450, 'tablets', 'BATCH-MET-001', '2025-10-15', 90, 'Cardinal Health', '2024-04-01');
INSERT INTO hc_pharmacy_inventory VALUES (9, 'Aspirin', '81mg', 'Tablet', 2000, 'tablets', 'BATCH-ASP-001', '2026-01-31', 300, 'McKesson', '2024-01-01');
INSERT INTO hc_pharmacy_inventory VALUES (10, 'Hydrocortisone', '1%', 'Cream', 100, 'tubes', 'BATCH-HYD-001', '2025-04-30', 20, 'AmerisourceBergen', '2024-02-01');

-- =============================================
-- hc_audit_log (10 rows) — system audit trail
-- =============================================
CREATE TABLE hc_audit_log (
    log_id INTEGER PRIMARY KEY,
    log_user_email TEXT NOT NULL,
    log_action TEXT NOT NULL,
    log_table_name TEXT,
    log_record_id INTEGER,
    log_timestamp TEXT NOT NULL,
    log_ip_address TEXT,
    log_details TEXT
);

INSERT INTO hc_audit_log VALUES (1, 'dr.williams@healthfirst.com', 'CREATE', 'hc_prescriptions', 1, '2024-01-15 09:30:00', '192.168.1.10', 'New prescription for alice.chen@email.com');
INSERT INTO hc_audit_log VALUES (2, 'anna.scott@healthfirst.com', 'CREATE', 'hc_vitals', 1, '2024-01-15 08:45:00', '192.168.1.20', 'Vitals recorded for alice.chen@email.com');
INSERT INTO hc_audit_log VALUES (3, 'dr.lee@healthfirst.com', 'CREATE', 'hc_reports', 1, '2024-01-15 11:00:00', '192.168.1.11', 'X-ray report created');
INSERT INTO hc_audit_log VALUES (4, 'dr.brown@healthfirst.com', 'CREATE', 'hc_surgeries', 1, '2024-03-02 10:00:00', '192.168.1.15', 'Surgery record for appendectomy');
INSERT INTO hc_audit_log VALUES (5, 'dr.williams@healthfirst.com', 'UPDATE', 'hc_prescriptions', 1, '2024-04-15 10:15:00', '192.168.1.10', 'Refill approved');
INSERT INTO hc_audit_log VALUES (6, 'admin@healthfirst.com', 'CREATE', 'hc_patients', 12, '2023-08-28 14:00:00', '192.168.1.1', 'New patient registered');
INSERT INTO hc_audit_log VALUES (7, 'dr.clark@healthfirst.com', 'CREATE', 'hc_reports', 22, '2024-02-15 15:30:00', '192.168.1.14', 'Pathology report created');
INSERT INTO hc_audit_log VALUES (8, 'dr.nguyen@healthfirst.com', 'UPDATE', 'hc_diagnoses', 4, '2024-05-15 11:30:00', '192.168.1.13', 'Diagnosis updated with new medication');
INSERT INTO hc_audit_log VALUES (9, 'felix.lopez@healthfirst.com', 'CREATE', 'hc_vitals', 6, '2024-03-01 07:30:00', '192.168.1.25', 'Pre-surgery vitals');
INSERT INTO hc_audit_log VALUES (10, 'dr.lee@healthfirst.com', 'CREATE', 'hc_reports', 9, '2024-03-20 14:30:00', '192.168.1.11', 'MRI report created');

-- =============================================
-- hc_waiting_list (6 rows) — procedure waiting list
-- =============================================
CREATE TABLE hc_waiting_list (
    wl_id INTEGER PRIMARY KEY,
    wl_patient_email TEXT NOT NULL,
    wl_doctor_email TEXT NOT NULL,
    wl_procedure TEXT NOT NULL,
    wl_priority TEXT DEFAULT 'routine',
    wl_added_date TEXT NOT NULL,
    wl_target_date TEXT,
    wl_status TEXT DEFAULT 'waiting',
    wl_notes TEXT
);

INSERT INTO hc_waiting_list VALUES (1, 'frank.garcia@email.com', 'dr.brown@healthfirst.com', 'Inguinal Hernia Repair', 'routine', '2024-05-01', '2024-08-01', 'scheduled', 'Surgery date confirmed');
INSERT INTO hc_waiting_list VALUES (2, 'carol.zhang@email.com', 'dr.adams@healthfirst.com', 'Knee Replacement Consultation', 'routine', '2024-06-01', '2024-09-01', 'waiting', 'If conservative treatment fails');
INSERT INTO hc_waiting_list VALUES (3, 'jack.murphy@email.com', 'dr.nguyen@healthfirst.com', 'Nerve Conduction Study', 'urgent', '2024-04-01', '2024-07-01', 'scheduled', 'Neuropathy workup');
INSERT INTO hc_waiting_list VALUES (4, 'henry.patel@email.com', 'dr.nguyen@healthfirst.com', 'Nerve Conduction Test', 'routine', '2024-06-15', '2024-08-15', 'waiting', 'Tingling evaluation');
INSERT INTO hc_waiting_list VALUES (5, 'bob.rivera@email.com', 'dr.brown@healthfirst.com', 'Hernia Evaluation', 'routine', '2024-04-25', '2024-07-25', 'completed', 'Seen and assessed');
INSERT INTO hc_waiting_list VALUES (6, 'kate.brown@email.com', 'dr.adams@healthfirst.com', 'Shoulder MRI', 'routine', '2024-04-15', '2024-05-15', 'completed', 'MRI done 2024-04-10');

-- =============================================
-- hc_payments (12 rows) — payment transactions
-- =============================================
CREATE TABLE hc_payments (
    pay_id INTEGER PRIMARY KEY,
    pay_patient_email TEXT NOT NULL,
    pay_bill_id INTEGER,
    pay_amount REAL NOT NULL,
    pay_method TEXT DEFAULT 'insurance',
    pay_date TEXT NOT NULL,
    pay_reference TEXT,
    pay_status TEXT DEFAULT 'completed',
    pay_notes TEXT
);

INSERT INTO hc_payments VALUES (1, 'alice.chen@email.com', 1, 50.0, 'credit_card', '2024-01-15', 'TXN-PAY-001', 'completed', 'Copay');
INSERT INTO hc_payments VALUES (2, 'bob.rivera@email.com', 2, 70.0, 'debit_card', '2024-01-20', 'TXN-PAY-002', 'completed', 'Copay');
INSERT INTO hc_payments VALUES (3, 'carol.zhang@email.com', 3, 40.0, 'credit_card', '2024-02-05', 'TXN-PAY-003', 'completed', 'Copay');
INSERT INTO hc_payments VALUES (4, 'dave.wilson@email.com', 4, 35.0, 'cash', '2024-02-10', 'TXN-PAY-004', 'completed', 'Copay');
INSERT INTO hc_payments VALUES (5, 'eve.thompson@email.com', 5, 30.0, 'credit_card', '2024-02-15', 'TXN-PAY-005', 'completed', 'Copay');
INSERT INTO hc_payments VALUES (6, 'frank.garcia@email.com', 6, 850.0, 'insurance', '2024-03-15', 'TXN-PAY-006', 'completed', 'Patient responsibility');
INSERT INTO hc_payments VALUES (7, 'grace.kim@email.com', 7, 30.0, 'credit_card', '2024-03-10', 'TXN-PAY-007', 'completed', 'Copay');
INSERT INTO hc_payments VALUES (8, 'henry.patel@email.com', 8, 160.0, 'debit_card', '2024-03-20', 'TXN-PAY-008', 'completed', 'After insurance');
INSERT INTO hc_payments VALUES (9, 'ivy.santos@email.com', 9, 240.0, 'credit_card', '2024-04-01', 'TXN-PAY-009', 'completed', 'After insurance');
INSERT INTO hc_payments VALUES (10, 'kate.brown@email.com', 11, 35.0, 'debit_card', '2024-04-15', 'TXN-PAY-010', 'completed', 'Copay');
INSERT INTO hc_payments VALUES (11, 'alice.chen@email.com', 12, 190.0, 'credit_card', '2024-04-20', 'TXN-PAY-011', 'completed', 'After insurance');
INSERT INTO hc_payments VALUES (12, 'carol.zhang@email.com', 14, 25.0, 'cash', '2024-05-10', 'TXN-PAY-012', 'completed', 'Copay');
"""

# =====================================================================
# TARGET SCHEMA — MedCore Enterprise Hospital System (50 tables)
# =====================================================================

TARGET_SQL = """
-- MedCore Enterprise Hospital System — 50 tables
-- Full enterprise schema with proper FKs, indexes, constraints

-- =============================================
-- CORE ENTITIES
-- =============================================

CREATE TABLE patients (
    id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT,
    date_of_birth TEXT NOT NULL,
    gender TEXT NOT NULL,
    blood_type TEXT,
    registered_at TEXT NOT NULL,
    is_active INTEGER NOT NULL DEFAULT 1
);
CREATE INDEX idx_patients_email ON patients(email);
CREATE INDEX idx_patients_name ON patients(last_name, first_name);

INSERT INTO patients VALUES (1, 'Alice', 'Chen', 'alice.chen@email.com', '555-0101', '1990-03-15', 'F', 'A+', '2020-01-10', 1);
INSERT INTO patients VALUES (2, 'Bob', 'Rivera', 'bob.rivera@email.com', '555-0102', '1985-07-22', 'M', 'O+', '2020-03-05', 1);
INSERT INTO patients VALUES (3, 'Carol', 'Zhang', 'carol.zhang@email.com', '555-0103', '1992-11-08', 'F', 'B+', '2020-06-18', 1);
INSERT INTO patients VALUES (4, 'Dave', 'Wilson', 'dave.wilson@email.com', '555-0104', '1978-01-30', 'M', 'AB-', '2021-01-12', 1);
INSERT INTO patients VALUES (5, 'Eve', 'Thompson', 'eve.thompson@email.com', '555-0105', '1995-05-12', 'F', 'O-', '2021-04-20', 1);
INSERT INTO patients VALUES (6, 'Frank', 'Garcia', 'frank.garcia@email.com', '555-0106', '1983-09-25', 'M', 'A-', '2021-07-01', 1);
INSERT INTO patients VALUES (7, 'Grace', 'Kim', 'grace.kim@email.com', '555-0107', '1991-12-03', 'F', 'B-', '2022-01-14', 1);
INSERT INTO patients VALUES (8, 'Henry', 'Patel', 'henry.patel@email.com', '555-0108', '1987-04-18', 'M', 'AB+', '2022-05-22', 1);
INSERT INTO patients VALUES (9, 'Ivy', 'Santos', 'ivy.santos@email.com', '555-0109', '1994-08-07', 'F', 'O+', '2022-09-10', 1);
INSERT INTO patients VALUES (10, 'Jack', 'Murphy', 'jack.murphy@email.com', '555-0110', '1976-02-14', 'M', 'A+', '2023-01-03', 1);
INSERT INTO patients VALUES (11, 'Kate', 'Brown', 'kate.brown@email.com', '555-0111', '1989-06-29', 'F', 'B+', '2023-04-15', 1);
INSERT INTO patients VALUES (12, 'Leo', 'Martinez', 'leo.martinez@email.com', '555-0112', '1982-10-11', 'M', 'O-', '2023-08-28', 0);

CREATE TABLE patient_addresses (
    id INTEGER PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id),
    address_line TEXT NOT NULL,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    zip_code TEXT NOT NULL,
    address_type TEXT NOT NULL DEFAULT 'home'
);
CREATE INDEX idx_patient_addresses_patient ON patient_addresses(patient_id);

INSERT INTO patient_addresses VALUES (1, 1, '123 Maple St', 'Portland', 'OR', '97201', 'home');
INSERT INTO patient_addresses VALUES (2, 2, '456 Oak Ave', 'Austin', 'TX', '78701', 'home');
INSERT INTO patient_addresses VALUES (3, 3, '789 Pine Rd', 'Seattle', 'WA', '98101', 'home');
INSERT INTO patient_addresses VALUES (4, 4, '321 Elm Blvd', 'Denver', 'CO', '80201', 'home');
INSERT INTO patient_addresses VALUES (5, 5, '654 Birch Ln', 'Miami', 'FL', '33101', 'home');
INSERT INTO patient_addresses VALUES (6, 6, '987 Cedar Ct', 'Chicago', 'IL', '60601', 'home');
INSERT INTO patient_addresses VALUES (7, 7, '147 Walnut Dr', 'San Francisco', 'CA', '94101', 'home');
INSERT INTO patient_addresses VALUES (8, 8, '258 Spruce Way', 'Boston', 'MA', '02101', 'home');
INSERT INTO patient_addresses VALUES (9, 9, '369 Ash Pl', 'Phoenix', 'AZ', '85001', 'home');
INSERT INTO patient_addresses VALUES (10, 10, '480 Poplar St', 'Nashville', 'TN', '37201', 'home');
INSERT INTO patient_addresses VALUES (11, 11, '591 Hickory Ave', 'Atlanta', 'GA', '30301', 'home');
INSERT INTO patient_addresses VALUES (12, 12, '702 Sycamore Rd', 'San Diego', 'CA', '92101', 'home');

CREATE TABLE emergency_contacts (
    id INTEGER PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id),
    contact_name TEXT NOT NULL,
    relationship TEXT,
    phone TEXT NOT NULL,
    email TEXT,
    is_primary INTEGER NOT NULL DEFAULT 1
);
CREATE INDEX idx_emergency_contacts_patient ON emergency_contacts(patient_id);

INSERT INTO emergency_contacts VALUES (1, 1, 'Bob Chen', 'Spouse', '555-0901', 'bob.chen@email.com', 1);
INSERT INTO emergency_contacts VALUES (2, 2, 'Maria Rivera', 'Wife', '555-0902', 'maria.r@email.com', 1);
INSERT INTO emergency_contacts VALUES (3, 3, 'Dan Zhang', 'Husband', '555-0903', 'dan.z@email.com', 1);
INSERT INTO emergency_contacts VALUES (4, 4, 'Sue Wilson', 'Wife', '555-0904', 'sue.w@email.com', 1);
INSERT INTO emergency_contacts VALUES (5, 5, 'Tom Thompson', 'Father', '555-0905', 'tom.t@email.com', 1);
INSERT INTO emergency_contacts VALUES (6, 6, 'Rosa Garcia', 'Wife', '555-0906', 'rosa.g@email.com', 1);
INSERT INTO emergency_contacts VALUES (7, 7, 'James Kim', 'Husband', '555-0907', 'james.k@email.com', 1);
INSERT INTO emergency_contacts VALUES (8, 8, 'Priya Patel', 'Wife', '555-0908', 'priya.p@email.com', 1);

CREATE TABLE insurance_policies (
    id INTEGER PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id),
    provider TEXT NOT NULL,
    plan_name TEXT,
    policy_number TEXT NOT NULL,
    group_number TEXT,
    start_date TEXT NOT NULL,
    end_date TEXT,
    copay REAL NOT NULL DEFAULT 0.0,
    is_primary INTEGER NOT NULL DEFAULT 1
);
CREATE INDEX idx_insurance_patient ON insurance_policies(patient_id);

INSERT INTO insurance_policies VALUES (1, 1, 'BlueCross BlueShield', 'PPO Gold', 'POL-10001', 'GRP-5001', '2024-01-01', '2024-12-31', 25.0, 1);
INSERT INTO insurance_policies VALUES (2, 2, 'Aetna', 'HMO Standard', 'POL-10002', 'GRP-5002', '2024-01-01', '2024-12-31', 30.0, 1);
INSERT INTO insurance_policies VALUES (3, 3, 'UnitedHealth', 'PPO Premium', 'POL-10003', 'GRP-5003', '2024-01-01', '2024-12-31', 20.0, 1);
INSERT INTO insurance_policies VALUES (4, 4, 'Cigna', 'EPO Basic', 'POL-10004', 'GRP-5004', '2024-01-01', '2024-12-31', 35.0, 1);
INSERT INTO insurance_policies VALUES (5, 5, 'BlueCross BlueShield', 'PPO Silver', 'POL-10005', 'GRP-5001', '2024-01-01', '2024-12-31', 30.0, 1);
INSERT INTO insurance_policies VALUES (6, 6, 'Aetna', 'HMO Plus', 'POL-10006', 'GRP-5002', '2024-01-01', '2024-12-31', 25.0, 1);
INSERT INTO insurance_policies VALUES (7, 7, 'Kaiser Permanente', 'HMO Standard', 'POL-10007', 'GRP-5005', '2024-01-01', '2024-12-31', 20.0, 1);
INSERT INTO insurance_policies VALUES (8, 8, 'UnitedHealth', 'PPO Gold', 'POL-10008', 'GRP-5003', '2024-01-01', '2024-12-31', 25.0, 1);
INSERT INTO insurance_policies VALUES (9, 9, 'Cigna', 'EPO Plus', 'POL-10009', 'GRP-5004', '2024-01-01', '2024-12-31', 30.0, 1);
INSERT INTO insurance_policies VALUES (10, 10, 'BlueCross BlueShield', 'PPO Gold', 'POL-10010', 'GRP-5001', '2024-01-01', '2024-12-31', 25.0, 1);
INSERT INTO insurance_policies VALUES (11, 11, 'Aetna', 'HMO Standard', 'POL-10011', 'GRP-5002', '2024-01-01', '2024-12-31', 30.0, 1);
INSERT INTO insurance_policies VALUES (12, 12, 'UnitedHealth', 'PPO Silver', 'POL-10012', 'GRP-5003', '2024-01-01', '2024-12-31', 35.0, 1);

-- =============================================
-- STAFF
-- =============================================

CREATE TABLE departments (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    floor INTEGER NOT NULL,
    phone TEXT,
    created_at TEXT NOT NULL
);

INSERT INTO departments VALUES (1, 'Cardiology', 2, '555-1001', '2018-01-01');
INSERT INTO departments VALUES (2, 'Radiology', 1, '555-1002', '2018-01-01');
INSERT INTO departments VALUES (3, 'Orthopedics', 3, '555-1003', '2019-01-01');
INSERT INTO departments VALUES (4, 'Neurology', 2, '555-1004', '2020-01-01');
INSERT INTO departments VALUES (5, 'Dermatology', 1, '555-1005', '2020-01-01');
INSERT INTO departments VALUES (6, 'Surgery', 3, '555-1006', '2021-01-01');
INSERT INTO departments VALUES (7, 'Pediatrics', 1, '555-1007', '2021-01-01');
INSERT INTO departments VALUES (8, 'Internal Medicine', 2, '555-1008', '2022-01-01');

CREATE TABLE doctors (
    id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT,
    specialty TEXT NOT NULL,
    license_number TEXT NOT NULL UNIQUE,
    department_id INTEGER NOT NULL REFERENCES departments(id),
    hire_date TEXT NOT NULL,
    is_active INTEGER NOT NULL DEFAULT 1
);
CREATE INDEX idx_doctors_email ON doctors(email);
CREATE INDEX idx_doctors_dept ON doctors(department_id);

INSERT INTO doctors VALUES (1, 'Sarah', 'Williams', 'dr.williams@healthfirst.com', '555-0201', 'Cardiology', 'LIC-5001', 1, '2018-03-01', 1);
INSERT INTO doctors VALUES (2, 'Michael', 'Lee', 'dr.lee@healthfirst.com', '555-0202', 'Radiology', 'LIC-5002', 2, '2019-06-15', 1);
INSERT INTO doctors VALUES (3, 'Jennifer', 'Adams', 'dr.adams@healthfirst.com', '555-0203', 'Orthopedics', 'LIC-5003', 3, '2019-09-01', 1);
INSERT INTO doctors VALUES (4, 'Robert', 'Nguyen', 'dr.nguyen@healthfirst.com', '555-0204', 'Neurology', 'LIC-5004', 4, '2020-01-10', 1);
INSERT INTO doctors VALUES (5, 'Emily', 'Clark', 'dr.clark@healthfirst.com', '555-0205', 'Dermatology', 'LIC-5005', 5, '2020-05-20', 1);
INSERT INTO doctors VALUES (6, 'David', 'Brown', 'dr.brown@healthfirst.com', '555-0206', 'General Surgery', 'LIC-5006', 6, '2021-02-01', 1);
INSERT INTO doctors VALUES (7, 'Lisa', 'Taylor', 'dr.taylor@healthfirst.com', '555-0207', 'Pediatrics', 'LIC-5007', 7, '2021-08-15', 1);
INSERT INTO doctors VALUES (8, 'James', 'White', 'dr.white@healthfirst.com', '555-0208', 'Internal Medicine', 'LIC-5008', 8, '2022-01-05', 0);

CREATE TABLE department_heads (
    id INTEGER PRIMARY KEY,
    department_id INTEGER NOT NULL REFERENCES departments(id),
    doctor_id INTEGER NOT NULL REFERENCES doctors(id),
    appointed_date TEXT NOT NULL
);

INSERT INTO department_heads VALUES (1, 1, 1, '2018-03-01');
INSERT INTO department_heads VALUES (2, 2, 2, '2019-06-15');
INSERT INTO department_heads VALUES (3, 3, 3, '2019-09-01');
INSERT INTO department_heads VALUES (4, 4, 4, '2020-01-10');
INSERT INTO department_heads VALUES (5, 5, 5, '2020-05-20');
INSERT INTO department_heads VALUES (6, 6, 6, '2021-02-01');
INSERT INTO department_heads VALUES (7, 7, 7, '2021-08-15');
INSERT INTO department_heads VALUES (8, 8, 8, '2022-01-05');

CREATE TABLE nurses (
    id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT,
    department_id INTEGER NOT NULL REFERENCES departments(id),
    shift TEXT NOT NULL,
    certification TEXT NOT NULL,
    hire_date TEXT NOT NULL,
    is_active INTEGER NOT NULL DEFAULT 1
);
CREATE INDEX idx_nurses_email ON nurses(email);
CREATE INDEX idx_nurses_dept ON nurses(department_id);

INSERT INTO nurses VALUES (1, 'Anna', 'Scott', 'anna.scott@healthfirst.com', '555-0301', 1, 'Day', 'RN', '2019-01-10', 1);
INSERT INTO nurses VALUES (2, 'Brian', 'Hall', 'brian.hall@healthfirst.com', '555-0302', 2, 'Night', 'RN', '2019-04-15', 1);
INSERT INTO nurses VALUES (3, 'Clara', 'Young', 'clara.young@healthfirst.com', '555-0303', 3, 'Day', 'BSN', '2019-08-01', 1);
INSERT INTO nurses VALUES (4, 'Derek', 'King', 'derek.king@healthfirst.com', '555-0304', 4, 'Night', 'RN', '2020-02-20', 1);
INSERT INTO nurses VALUES (5, 'Elena', 'Wright', 'elena.wright@healthfirst.com', '555-0305', 5, 'Day', 'BSN', '2020-06-10', 1);
INSERT INTO nurses VALUES (6, 'Felix', 'Lopez', 'felix.lopez@healthfirst.com', '555-0306', 6, 'Night', 'RN', '2021-01-05', 1);
INSERT INTO nurses VALUES (7, 'Gina', 'Allen', 'gina.allen@healthfirst.com', '555-0307', 7, 'Day', 'BSN', '2021-05-15', 1);
INSERT INTO nurses VALUES (8, 'Hugo', 'Baker', 'hugo.baker@healthfirst.com', '555-0308', 8, 'Day', 'RN', '2021-09-20', 1);
INSERT INTO nurses VALUES (9, 'Iris', 'Carter', 'iris.carter@healthfirst.com', '555-0309', 8, 'Night', 'BSN', '2022-03-01', 1);
INSERT INTO nurses VALUES (10, 'Jake', 'Davis', 'jake.davis@healthfirst.com', '555-0310', 8, 'Day', 'RN', '2022-07-10', 0);

-- =============================================
-- APPOINTMENTS & CLINICAL
-- =============================================

CREATE TABLE appointments (
    id INTEGER PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id),
    doctor_id INTEGER NOT NULL REFERENCES doctors(id),
    appointment_date TEXT NOT NULL,
    appointment_time TEXT,
    appointment_type TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'scheduled',
    notes TEXT,
    room TEXT,
    created_at TEXT NOT NULL
);
CREATE INDEX idx_appointments_patient ON appointments(patient_id);
CREATE INDEX idx_appointments_doctor ON appointments(doctor_id);
CREATE INDEX idx_appointments_date ON appointments(appointment_date);

INSERT INTO appointments VALUES (1, 1, 1, '2024-01-15', '09:00', 'checkup', 'completed', 'Annual cardiac checkup', 'Room 201', '2024-01-10');
INSERT INTO appointments VALUES (2, 2, 2, '2024-01-20', '10:30', 'imaging', 'completed', 'Chest X-ray follow-up', 'Room 102', '2024-01-15');
INSERT INTO appointments VALUES (3, 3, 3, '2024-02-05', '14:00', 'consultation', 'completed', 'Knee pain evaluation', 'Room 301', '2024-01-28');
INSERT INTO appointments VALUES (4, 4, 4, '2024-02-10', '11:00', 'follow-up', 'completed', 'Migraine follow-up', 'Room 205', '2024-02-03');
INSERT INTO appointments VALUES (5, 5, 5, '2024-02-15', '09:30', 'checkup', 'completed', 'Skin rash evaluation', 'Room 108', '2024-02-10');
INSERT INTO appointments VALUES (6, 6, 6, '2024-03-01', '08:00', 'surgery', 'completed', 'Appendectomy pre-op', 'Room 305', '2024-02-20');
INSERT INTO appointments VALUES (7, 7, 7, '2024-03-10', '15:00', 'checkup', 'completed', 'Wellness checkup', 'Room 110', '2024-03-05');
INSERT INTO appointments VALUES (8, 8, 1, '2024-03-15', '10:00', 'imaging', 'completed', 'Echocardiogram', 'Room 201', '2024-03-10');
INSERT INTO appointments VALUES (9, 9, 2, '2024-03-20', '13:00', 'imaging', 'completed', 'MRI brain scan', 'Room 102', '2024-03-15');
INSERT INTO appointments VALUES (10, 10, 4, '2024-04-01', '11:30', 'consultation', 'completed', 'Numbness in extremities', 'Room 205', '2024-03-25');
INSERT INTO appointments VALUES (11, 11, 3, '2024-04-10', '09:00', 'follow-up', 'completed', 'Post-surgery knee check', 'Room 301', '2024-04-05');
INSERT INTO appointments VALUES (12, 1, 2, '2024-04-15', '14:30', 'imaging', 'completed', 'CT scan chest', 'Room 102', '2024-04-10');
INSERT INTO appointments VALUES (13, 2, 6, '2024-05-01', '08:30', 'consultation', 'completed', 'Hernia evaluation', 'Room 305', '2024-04-25');
INSERT INTO appointments VALUES (14, 3, 1, '2024-05-10', '10:00', 'checkup', 'completed', 'Blood pressure monitoring', 'Room 201', '2024-05-05');
INSERT INTO appointments VALUES (15, 4, 2, '2024-05-15', '11:00', 'imaging', 'completed', 'Brain MRI', 'Room 102', '2024-05-10');
INSERT INTO appointments VALUES (16, 5, 7, '2024-06-01', '09:00', 'checkup', 'cancelled', 'Annual physical', 'Room 110', '2024-05-25');
INSERT INTO appointments VALUES (17, 6, 6, '2024-06-10', '08:00', 'follow-up', 'completed', 'Post-appendectomy check', 'Room 305', '2024-06-05');
INSERT INTO appointments VALUES (18, 7, 5, '2024-06-15', '14:00', 'consultation', 'scheduled', 'Mole assessment', 'Room 108', '2024-06-10');
INSERT INTO appointments VALUES (19, 8, 4, '2024-07-01', '10:30', 'follow-up', 'scheduled', 'Nerve conduction test results', 'Room 205', '2024-06-25');
INSERT INTO appointments VALUES (20, 12, 1, '2024-07-10', '09:00', 'checkup', 'scheduled', 'Cardiac stress test', 'Room 201', '2024-07-05');

CREATE TABLE diagnoses (
    id INTEGER PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id),
    doctor_id INTEGER NOT NULL REFERENCES doctors(id),
    icd_code TEXT NOT NULL,
    name TEXT NOT NULL,
    diagnosis_type TEXT NOT NULL DEFAULT 'primary',
    diagnosed_date TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'active',
    notes TEXT
);
CREATE INDEX idx_diagnoses_patient ON diagnoses(patient_id);
CREATE INDEX idx_diagnoses_icd ON diagnoses(icd_code);

INSERT INTO diagnoses VALUES (1, 1, 1, 'I10', 'Essential Hypertension', 'primary', '2024-01-15', 'active', 'Stage 1, diet and medication');
INSERT INTO diagnoses VALUES (2, 2, 1, 'E78.5', 'Hyperlipidemia', 'primary', '2024-01-20', 'active', 'Elevated LDL and triglycerides');
INSERT INTO diagnoses VALUES (3, 3, 3, 'M17.11', 'Primary Osteoarthritis Right Knee', 'primary', '2024-02-05', 'active', 'Mild degenerative changes on imaging');
INSERT INTO diagnoses VALUES (4, 4, 4, 'G43.909', 'Migraine Unspecified', 'primary', '2024-02-10', 'active', 'Chronic migraines with aura');
INSERT INTO diagnoses VALUES (5, 5, 5, 'L30.9', 'Dermatitis Unspecified', 'primary', '2024-02-15', 'resolved', 'Contact dermatitis, resolved with treatment');
INSERT INTO diagnoses VALUES (6, 6, 6, 'K35.80', 'Acute Appendicitis', 'primary', '2024-03-01', 'resolved', 'Surgically treated');
INSERT INTO diagnoses VALUES (7, 7, 7, 'D51.0', 'Vitamin D Deficiency', 'secondary', '2024-03-10', 'active', 'Low vitamin D levels on labs');
INSERT INTO diagnoses VALUES (8, 8, 1, 'E03.9', 'Hypothyroidism', 'primary', '2024-03-15', 'active', 'Subclinical, started levothyroxine');
INSERT INTO diagnoses VALUES (9, 9, 2, 'R51', 'Headache', 'primary', '2024-03-20', 'resolved', 'Tension headache, normal MRI');
INSERT INTO diagnoses VALUES (10, 10, 4, 'G62.9', 'Polyneuropathy Unspecified', 'primary', '2024-04-01', 'active', 'Peripheral neuropathy, workup ongoing');
INSERT INTO diagnoses VALUES (11, 11, 3, 'M75.10', 'Rotator Cuff Tendinitis', 'primary', '2024-04-10', 'active', 'Conservative management');
INSERT INTO diagnoses VALUES (12, 3, 3, 'M23.21', 'Meniscal Derangement Right Knee', 'secondary', '2024-02-10', 'active', 'Partial tear medial meniscus on MRI');
INSERT INTO diagnoses VALUES (13, 1, 1, 'I25.10', 'Atherosclerotic Heart Disease', 'secondary', '2024-04-15', 'active', 'CT showed no significant stenosis');
INSERT INTO diagnoses VALUES (14, 2, 1, 'I10', 'Essential Hypertension', 'secondary', '2024-01-20', 'active', 'Associated with hyperlipidemia');
INSERT INTO diagnoses VALUES (15, 7, 5, 'C44.91', 'Basal Cell Carcinoma', 'primary', '2024-06-15', 'active', 'Excised with clear margins');
INSERT INTO diagnoses VALUES (16, 6, 6, 'K40.90', 'Inguinal Hernia', 'primary', '2024-05-01', 'active', 'Watchful waiting for now');

CREATE TABLE vital_signs (
    id INTEGER PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id),
    nurse_id INTEGER REFERENCES nurses(id),
    recorded_date TEXT NOT NULL,
    bp_systolic INTEGER,
    bp_diastolic INTEGER,
    heart_rate INTEGER,
    temperature REAL,
    respiratory_rate INTEGER,
    o2_saturation REAL,
    weight_kg REAL,
    height_cm REAL,
    notes TEXT
);
CREATE INDEX idx_vitals_patient ON vital_signs(patient_id);
CREATE INDEX idx_vitals_date ON vital_signs(recorded_date);

INSERT INTO vital_signs VALUES (1, 1, 1, '2024-01-15', 138, 88, 72, 98.6, 16, 98.0, 62.0, 165.0, 'Slightly elevated BP');
INSERT INTO vital_signs VALUES (2, 2, 1, '2024-01-20', 142, 92, 78, 98.4, 18, 97.5, 95.0, 178.0, 'Elevated BP, overweight');
INSERT INTO vital_signs VALUES (3, 3, 3, '2024-02-05', 118, 76, 68, 98.6, 14, 99.0, 58.0, 162.0, 'Normal vitals');
INSERT INTO vital_signs VALUES (4, 4, 4, '2024-02-10', 125, 82, 70, 98.8, 16, 98.5, 82.0, 175.0, 'Mild headache reported');
INSERT INTO vital_signs VALUES (5, 5, 5, '2024-02-15', 112, 72, 65, 98.6, 14, 99.0, 55.0, 160.0, 'Normal vitals');
INSERT INTO vital_signs VALUES (6, 6, 6, '2024-03-01', 130, 85, 88, 100.2, 20, 97.0, 78.0, 172.0, 'Fever and elevated HR pre-surgery');
INSERT INTO vital_signs VALUES (7, 7, 7, '2024-03-10', 110, 70, 62, 98.4, 14, 99.5, 52.0, 158.0, 'Excellent vitals');
INSERT INTO vital_signs VALUES (8, 8, 1, '2024-03-15', 120, 78, 68, 98.6, 16, 98.5, 75.0, 180.0, 'Normal vitals');
INSERT INTO vital_signs VALUES (9, 9, 2, '2024-03-20', 115, 74, 70, 98.4, 15, 99.0, 60.0, 168.0, 'Normal vitals');
INSERT INTO vital_signs VALUES (10, 10, 4, '2024-04-01', 135, 86, 74, 98.6, 16, 98.0, 88.0, 182.0, 'Elevated BP');
INSERT INTO vital_signs VALUES (11, 11, 3, '2024-04-10', 116, 74, 66, 98.6, 14, 99.0, 64.0, 170.0, 'Normal vitals');
INSERT INTO vital_signs VALUES (12, 1, 1, '2024-04-15', 132, 84, 70, 98.6, 16, 98.5, 61.5, 165.0, 'BP slightly improved');
INSERT INTO vital_signs VALUES (13, 2, 1, '2024-05-01', 140, 90, 76, 98.4, 18, 97.5, 94.0, 178.0, 'Still elevated BP');
INSERT INTO vital_signs VALUES (14, 3, 3, '2024-05-10', 120, 78, 66, 98.6, 14, 99.0, 57.5, 162.0, 'Normal');
INSERT INTO vital_signs VALUES (15, 4, 4, '2024-05-15', 122, 80, 68, 98.8, 16, 98.5, 81.0, 175.0, 'Stable');
INSERT INTO vital_signs VALUES (16, 6, 6, '2024-06-10', 122, 78, 72, 98.6, 16, 98.5, 76.0, 172.0, 'Post-surgery recovery good');
INSERT INTO vital_signs VALUES (17, 7, 5, '2024-06-15', 108, 68, 60, 98.4, 14, 99.5, 52.0, 158.0, 'Normal');
INSERT INTO vital_signs VALUES (18, 8, 4, '2024-07-01', 118, 76, 66, 98.6, 16, 98.5, 74.0, 180.0, 'Stable on medication');
INSERT INTO vital_signs VALUES (19, 12, 1, '2024-07-10', 128, 82, 72, 98.6, 16, 98.0, 80.0, 176.0, 'Normal for age');
INSERT INTO vital_signs VALUES (20, 9, 9, '2024-06-20', 114, 72, 68, 98.4, 15, 99.0, 59.5, 168.0, 'Normal');

CREATE TABLE clinical_notes (
    id INTEGER PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id),
    doctor_id INTEGER NOT NULL REFERENCES doctors(id),
    note_date TEXT NOT NULL,
    note_type TEXT NOT NULL DEFAULT 'progress',
    subjective TEXT,
    objective TEXT,
    assessment TEXT,
    plan TEXT,
    is_signed INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX idx_clinical_notes_patient ON clinical_notes(patient_id);

INSERT INTO clinical_notes VALUES (1, 1, 1, '2024-01-15', 'initial', 'Patient reports occasional headaches', 'BP 138/88, HR 72', 'Stage 1 hypertension', 'Start Lisinopril 10mg daily, recheck in 3 months', 1);
INSERT INTO clinical_notes VALUES (2, 2, 1, '2024-01-20', 'initial', 'No symptoms, routine screening', 'BP 142/92, Weight 95kg', 'Hyperlipidemia with HTN', 'Start Atorvastatin 20mg, low-sodium diet', 1);
INSERT INTO clinical_notes VALUES (3, 3, 3, '2024-02-05', 'initial', 'Right knee pain worsening over 3 months', 'Tenderness medial joint line, McMurray positive', 'OA right knee with possible meniscal tear', 'NSAIDs, physical therapy, MRI ordered', 1);
INSERT INTO clinical_notes VALUES (4, 4, 4, '2024-02-10', 'follow-up', 'Migraines occurring 3-4 times per month', 'Neuro exam normal', 'Chronic migraine with aura', 'Continue Sumatriptan PRN, add Topiramate prophylaxis', 1);
INSERT INTO clinical_notes VALUES (5, 6, 6, '2024-03-01', 'emergency', 'Acute RLQ pain x 12 hours, nausea', 'Tenderness RLQ, rebound positive, fever 100.2F', 'Acute appendicitis', 'Emergent appendectomy, IV antibiotics', 1);
INSERT INTO clinical_notes VALUES (6, 7, 7, '2024-03-10', 'wellness', 'Fatigue and low energy for 2 months', 'PE unremarkable', 'Vitamin D deficiency suspected', 'Check vitamin D level, start supplementation', 1);
INSERT INTO clinical_notes VALUES (7, 8, 1, '2024-03-15', 'initial', 'Weight gain and cold intolerance', 'Thyroid non-tender, no nodules', 'Subclinical hypothyroidism', 'Start Levothyroxine 50mcg, recheck TSH in 6 weeks', 1);
INSERT INTO clinical_notes VALUES (8, 10, 4, '2024-04-01', 'initial', 'Numbness and tingling in feet bilateral', 'Decreased sensation stocking distribution', 'Peripheral polyneuropathy', 'NCS ordered, Gabapentin started, B12 check', 1);
INSERT INTO clinical_notes VALUES (9, 11, 3, '2024-04-10', 'follow-up', 'Left shoulder pain with overhead activity', 'Positive impingement signs, MRI shows tendinosis', 'Rotator cuff tendinitis', 'Physical therapy, NSAIDs, avoid overhead lifting', 1);
INSERT INTO clinical_notes VALUES (10, 6, 6, '2024-06-10', 'follow-up', 'Doing well post-appendectomy, new inguinal bulge', 'Inguinal hernia palpable on exam', 'Inguinal hernia, post-appendectomy recovery good', 'Schedule hernia repair, continue recovery', 1);

-- =============================================
-- REPORTS — split from monolithic hc_reports
-- =============================================

CREATE TABLE xray_reports (
    id INTEGER PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id),
    doctor_id INTEGER NOT NULL REFERENCES doctors(id),
    title TEXT NOT NULL,
    body_region TEXT NOT NULL,
    findings TEXT,
    conclusion TEXT,
    severity TEXT NOT NULL DEFAULT 'normal',
    file_url TEXT,
    report_date TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'final',
    notes TEXT
);
CREATE INDEX idx_xray_patient ON xray_reports(patient_id);

INSERT INTO xray_reports VALUES (1, 1, 2, 'Chest X-Ray', 'chest', 'No acute cardiopulmonary process', 'Normal chest radiograph', 'normal', '/files/xray/001.dcm', '2024-01-15', 'final', 'PA and lateral views');
INSERT INTO xray_reports VALUES (2, 2, 2, 'Chest X-Ray', 'chest', 'Mild cardiomegaly noted', 'Borderline cardiac enlargement', 'moderate', '/files/xray/002.dcm', '2024-01-20', 'final', 'Comparison with prior study recommended');
INSERT INTO xray_reports VALUES (3, 3, 3, 'Right Knee X-Ray', 'knee', 'Mild degenerative changes', 'Early osteoarthritis', 'mild', '/files/xray/003.dcm', '2024-02-05', 'final', 'Weight-bearing views');
INSERT INTO xray_reports VALUES (4, 10, 3, 'Lumbar Spine X-Ray', 'spine', 'Disc space narrowing L4-L5', 'Degenerative disc disease', 'moderate', '/files/xray/004.dcm', '2024-04-01', 'final', 'AP and lateral views');

CREATE TABLE ct_scan_reports (
    id INTEGER PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id),
    doctor_id INTEGER NOT NULL REFERENCES doctors(id),
    title TEXT NOT NULL,
    body_region TEXT NOT NULL,
    findings TEXT,
    conclusion TEXT,
    severity TEXT NOT NULL DEFAULT 'normal',
    file_url TEXT,
    report_date TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'final',
    notes TEXT
);
CREATE INDEX idx_ct_patient ON ct_scan_reports(patient_id);

INSERT INTO ct_scan_reports VALUES (1, 1, 2, 'CT Chest with Contrast', 'chest', 'No pulmonary embolism', 'Negative for PE', 'normal', '/files/ct/001.dcm', '2024-04-15', 'final', 'IV contrast administered');
INSERT INTO ct_scan_reports VALUES (2, 4, 4, 'CT Head without Contrast', 'head', 'No acute intracranial abnormality', 'Normal CT head', 'normal', '/files/ct/002.dcm', '2024-02-10', 'final', 'Non-contrast study');
INSERT INTO ct_scan_reports VALUES (3, 6, 6, 'CT Abdomen/Pelvis', 'abdomen', 'Acute appendicitis with periappendiceal fat stranding', 'Acute appendicitis confirmed', 'severe', '/files/ct/003.dcm', '2024-03-01', 'final', 'Oral and IV contrast');
INSERT INTO ct_scan_reports VALUES (4, 8, 2, 'CT Chest', 'chest', 'Small ground-glass opacity right lower lobe', 'Follow-up recommended in 3 months', 'mild', '/files/ct/004.dcm', '2024-03-15', 'preliminary', 'Non-contrast study');

CREATE TABLE mri_reports (
    id INTEGER PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id),
    doctor_id INTEGER NOT NULL REFERENCES doctors(id),
    title TEXT NOT NULL,
    body_region TEXT NOT NULL,
    findings TEXT,
    conclusion TEXT,
    severity TEXT NOT NULL DEFAULT 'normal',
    file_url TEXT,
    report_date TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'final',
    notes TEXT
);
CREATE INDEX idx_mri_patient ON mri_reports(patient_id);

INSERT INTO mri_reports VALUES (1, 9, 2, 'MRI Brain with Contrast', 'brain', 'No enhancing lesions, no mass effect', 'Normal brain MRI', 'normal', '/files/mri/001.dcm', '2024-03-20', 'final', 'Gadolinium contrast');
INSERT INTO mri_reports VALUES (2, 4, 4, 'MRI Brain without Contrast', 'brain', 'Mild white matter changes', 'Age-appropriate white matter changes', 'mild', '/files/mri/002.dcm', '2024-05-15', 'final', 'Non-contrast study');
INSERT INTO mri_reports VALUES (3, 3, 3, 'MRI Right Knee', 'knee', 'Partial tear medial meniscus', 'Meniscal pathology confirmed', 'moderate', '/files/mri/003.dcm', '2024-02-10', 'final', 'Without contrast');
INSERT INTO mri_reports VALUES (4, 11, 3, 'MRI Left Shoulder', 'shoulder', 'Rotator cuff tendinosis without tear', 'No surgical intervention needed', 'mild', '/files/mri/004.dcm', '2024-04-10', 'final', 'Without contrast');

CREATE TABLE lab_results (
    id INTEGER PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id),
    doctor_id INTEGER NOT NULL REFERENCES doctors(id),
    title TEXT NOT NULL,
    body_region TEXT NOT NULL DEFAULT 'blood',
    findings TEXT,
    conclusion TEXT,
    severity TEXT NOT NULL DEFAULT 'normal',
    report_date TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'final',
    notes TEXT
);
CREATE INDEX idx_lab_patient ON lab_results(patient_id);

INSERT INTO lab_results VALUES (1, 1, 1, 'Complete Blood Count', 'blood', 'WBC 6.8, RBC 4.5, Hgb 13.2, Hct 39.5, Plt 250', 'All values within normal limits', 'normal', '2024-01-15', 'final', 'Fasting sample');
INSERT INTO lab_results VALUES (2, 2, 1, 'Lipid Panel', 'blood', 'Total Chol 245, LDL 160, HDL 42, Trig 215', 'Hyperlipidemia', 'moderate', '2024-01-20', 'final', 'Fasting 12 hours');
INSERT INTO lab_results VALUES (3, 5, 5, 'Comprehensive Metabolic Panel', 'blood', 'Glucose 95, BUN 15, Creatinine 0.9, all electrolytes normal', 'Normal metabolic panel', 'normal', '2024-02-15', 'final', 'Morning draw');
INSERT INTO lab_results VALUES (4, 8, 1, 'Thyroid Panel', 'blood', 'TSH 2.5, Free T4 1.1, Free T3 3.2', 'Euthyroid', 'normal', '2024-03-15', 'final', 'No fasting required');

CREATE TABLE ultrasound_reports (
    id INTEGER PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id),
    doctor_id INTEGER NOT NULL REFERENCES doctors(id),
    title TEXT NOT NULL,
    body_region TEXT NOT NULL,
    findings TEXT,
    conclusion TEXT,
    severity TEXT NOT NULL DEFAULT 'normal',
    file_url TEXT,
    report_date TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'final',
    notes TEXT
);
CREATE INDEX idx_ultrasound_patient ON ultrasound_reports(patient_id);

INSERT INTO ultrasound_reports VALUES (1, 7, 7, 'Abdominal Ultrasound', 'abdomen', 'Normal liver, gallbladder, kidneys', 'No significant findings', 'normal', '/files/us/001.dcm', '2024-03-10', 'final', 'Fasting study');
INSERT INTO ultrasound_reports VALUES (2, 9, 1, 'Thyroid Ultrasound', 'neck', 'Small benign-appearing nodule right lobe 0.8cm', 'Benign thyroid nodule, follow-up in 12 months', 'mild', '/files/us/002.dcm', '2024-03-25', 'final', 'No prior comparison');
INSERT INTO ultrasound_reports VALUES (3, 11, 1, 'Carotid Doppler', 'neck', 'No hemodynamically significant stenosis', 'Normal carotid arteries', 'normal', '/files/us/003.dcm', '2024-04-12', 'final', 'Bilateral study');
INSERT INTO ultrasound_reports VALUES (4, 6, 6, 'RUQ Ultrasound', 'abdomen', 'No gallstones, normal bile ducts', 'Normal right upper quadrant', 'normal', '/files/us/004.dcm', '2024-03-02', 'final', 'Fasting study');

CREATE TABLE pathology_reports (
    id INTEGER PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id),
    doctor_id INTEGER NOT NULL REFERENCES doctors(id),
    title TEXT NOT NULL,
    body_region TEXT NOT NULL,
    findings TEXT,
    conclusion TEXT,
    severity TEXT NOT NULL DEFAULT 'normal',
    report_date TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'final',
    notes TEXT
);
CREATE INDEX idx_pathology_patient ON pathology_reports(patient_id);

INSERT INTO pathology_reports VALUES (1, 6, 6, 'Appendix Specimen', 'appendix', 'Acute appendicitis with transmural inflammation', 'Acute suppurative appendicitis confirmed', 'severe', '2024-03-02', 'final', 'Specimen from appendectomy');
INSERT INTO pathology_reports VALUES (2, 5, 5, 'Skin Biopsy - Left Arm', 'skin', 'Benign intradermal nevus', 'Benign melanocytic nevus', 'normal', '2024-02-15', 'final', 'Punch biopsy 4mm');
INSERT INTO pathology_reports VALUES (3, 10, 5, 'Skin Biopsy - Back', 'skin', 'Seborrheic keratosis', 'Benign keratosis', 'normal', '2024-04-05', 'final', 'Shave biopsy');
INSERT INTO pathology_reports VALUES (4, 7, 5, 'Skin Lesion Excision', 'skin', 'Basal cell carcinoma, margins clear', 'BCC completely excised', 'moderate', '2024-06-15', 'preliminary', 'Excisional biopsy');

-- =============================================
-- MEDICATIONS & PRESCRIPTIONS
-- =============================================

CREATE TABLE medications (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    generic_name TEXT,
    category TEXT NOT NULL,
    form TEXT NOT NULL,
    manufacturer TEXT,
    requires_prescription INTEGER NOT NULL DEFAULT 1,
    is_controlled INTEGER NOT NULL DEFAULT 0,
    schedule TEXT
);

INSERT INTO medications VALUES (1, 'Lisinopril', 'Lisinopril', 'ACE Inhibitor', 'Tablet', 'Lupin Pharma', 1, 0, NULL);
INSERT INTO medications VALUES (2, 'Atorvastatin', 'Atorvastatin', 'Statin', 'Tablet', 'Pfizer', 1, 0, NULL);
INSERT INTO medications VALUES (3, 'Ibuprofen', 'Ibuprofen', 'NSAID', 'Tablet', 'Advil', 0, 0, NULL);
INSERT INTO medications VALUES (4, 'Sumatriptan', 'Sumatriptan', 'Triptan', 'Tablet', 'GlaxoSmithKline', 1, 0, NULL);
INSERT INTO medications VALUES (5, 'Hydrocortisone', 'Hydrocortisone', 'Corticosteroid', 'Cream', 'Teva Pharma', 0, 0, NULL);
INSERT INTO medications VALUES (6, 'Amoxicillin', 'Amoxicillin', 'Antibiotic', 'Capsule', 'Sandoz', 1, 0, NULL);
INSERT INTO medications VALUES (7, 'Gabapentin', 'Gabapentin', 'Anticonvulsant', 'Capsule', 'Pfizer', 1, 0, 'Schedule V');
INSERT INTO medications VALUES (8, 'Levothyroxine', 'Levothyroxine', 'Thyroid Hormone', 'Tablet', 'AbbVie', 1, 0, NULL);
INSERT INTO medications VALUES (9, 'Metoprolol', 'Metoprolol', 'Beta Blocker', 'Tablet', 'AstraZeneca', 1, 0, NULL);
INSERT INTO medications VALUES (10, 'Aspirin', 'Acetylsalicylic Acid', 'NSAID', 'Tablet', 'Bayer', 0, 0, NULL);

CREATE TABLE prescriptions (
    id INTEGER PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id),
    doctor_id INTEGER NOT NULL REFERENCES doctors(id),
    medication_id INTEGER NOT NULL REFERENCES medications(id),
    dosage TEXT NOT NULL,
    frequency TEXT,
    start_date TEXT NOT NULL,
    end_date TEXT,
    refills INTEGER NOT NULL DEFAULT 0,
    status TEXT NOT NULL DEFAULT 'active',
    pharmacy TEXT,
    notes TEXT
);
CREATE INDEX idx_prescriptions_patient ON prescriptions(patient_id);
CREATE INDEX idx_prescriptions_medication ON prescriptions(medication_id);

INSERT INTO prescriptions VALUES (1, 1, 1, 1, '10mg', 'Once daily', '2024-01-15', '2024-07-15', 3, 'active', 'CVS Pharmacy', 'Monitor blood pressure');
INSERT INTO prescriptions VALUES (2, 2, 1, 2, '20mg', 'Once daily at bedtime', '2024-01-20', '2025-01-20', 6, 'active', 'Walgreens', 'Check lipids in 3 months');
INSERT INTO prescriptions VALUES (3, 3, 3, 3, '400mg', 'Three times daily with food', '2024-02-05', '2024-03-05', 0, 'completed', 'Rite Aid', 'For knee inflammation');
INSERT INTO prescriptions VALUES (4, 4, 4, 4, '50mg', 'As needed for migraine', '2024-02-10', '2024-08-10', 2, 'active', 'CVS Pharmacy', 'Max 2 doses per 24 hours');
INSERT INTO prescriptions VALUES (5, 5, 5, 5, '1%', 'Twice daily to affected area', '2024-02-15', '2024-03-15', 0, 'completed', 'Walgreens', 'Apply thin layer');
INSERT INTO prescriptions VALUES (6, 6, 6, 6, '500mg', 'Three times daily', '2024-03-02', '2024-03-12', 0, 'completed', 'CVS Pharmacy', 'Post-surgery prophylaxis');
INSERT INTO prescriptions VALUES (7, 7, 7, 3, '2000IU', 'Once daily', '2024-03-10', '2024-09-10', 2, 'active', 'Rite Aid', 'Supplement for deficiency');
INSERT INTO prescriptions VALUES (8, 8, 1, 8, '50mcg', 'Once daily on empty stomach', '2024-03-15', '2025-03-15', 6, 'active', 'CVS Pharmacy', 'Take 30 min before breakfast');
INSERT INTO prescriptions VALUES (9, 9, 2, 3, '500mg', 'Every 6 hours as needed', '2024-03-20', '2024-04-20', 0, 'completed', 'Walgreens', 'For headache after MRI');
INSERT INTO prescriptions VALUES (10, 10, 4, 7, '300mg', 'Three times daily', '2024-04-01', '2024-10-01', 3, 'active', 'CVS Pharmacy', 'For neuropathic pain');
INSERT INTO prescriptions VALUES (11, 11, 3, 3, '500mg', 'Twice daily with food', '2024-04-10', '2024-05-10', 1, 'completed', 'Rite Aid', 'For shoulder pain');
INSERT INTO prescriptions VALUES (12, 1, 1, 9, '25mg', 'Twice daily', '2024-04-15', '2024-10-15', 3, 'active', 'CVS Pharmacy', 'Heart rate control');
INSERT INTO prescriptions VALUES (13, 2, 1, 10, '81mg', 'Once daily', '2024-01-20', '2025-01-20', 6, 'active', 'Walgreens', 'Low-dose for cardiac protection');
INSERT INTO prescriptions VALUES (14, 4, 4, 3, '25mg', 'Once daily', '2024-05-15', '2024-11-15', 3, 'active', 'CVS Pharmacy', 'Migraine prevention');
INSERT INTO prescriptions VALUES (15, 3, 3, 3, '1500mg', 'Once daily', '2024-02-10', '2024-08-10', 2, 'active', 'Rite Aid', 'Joint supplement');

-- =============================================
-- SURGICAL & PROCEDURES
-- =============================================

CREATE TABLE surgeries (
    id INTEGER PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id),
    doctor_id INTEGER NOT NULL REFERENCES doctors(id),
    nurse_id INTEGER REFERENCES nurses(id),
    surgery_type TEXT NOT NULL,
    description TEXT,
    room TEXT,
    surgery_date TEXT NOT NULL,
    start_time TEXT,
    end_time TEXT,
    outcome TEXT NOT NULL DEFAULT 'successful',
    complications TEXT,
    notes TEXT
);
CREATE INDEX idx_surgeries_patient ON surgeries(patient_id);
CREATE INDEX idx_surgeries_doctor ON surgeries(doctor_id);

INSERT INTO surgeries VALUES (1, 6, 6, 6, 'Appendectomy', 'Laparoscopic appendectomy', 'Room 305', '2024-03-02', '08:00', '09:30', 'successful', 'None', 'Clean procedure');
INSERT INTO surgeries VALUES (2, 3, 3, 3, 'Arthroscopy', 'Right knee arthroscopic meniscal repair', 'Room 305', '2024-03-15', '10:00', '11:15', 'successful', 'None', 'Partial meniscectomy');
INSERT INTO surgeries VALUES (3, 5, 5, 5, 'Biopsy', 'Skin punch biopsy left arm', 'Room 108', '2024-02-15', '14:00', '14:30', 'successful', 'None', 'Minimal procedure');
INSERT INTO surgeries VALUES (4, 10, 5, 5, 'Biopsy', 'Skin shave biopsy back', 'Room 108', '2024-04-05', '15:00', '15:20', 'successful', 'None', 'Superficial shave');
INSERT INTO surgeries VALUES (5, 7, 5, 5, 'Excision', 'Skin lesion excision right forearm', 'Room 108', '2024-06-15', '13:00', '13:45', 'successful', 'None', 'Clear margins achieved');
INSERT INTO surgeries VALUES (6, 6, 6, 6, 'Hernia Repair', 'Inguinal hernia repair planned', 'Room 305', '2024-08-01', '08:00', '10:00', 'scheduled', NULL, 'Pre-op clearance obtained');

CREATE TABLE procedures (
    id INTEGER PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id),
    doctor_id INTEGER NOT NULL REFERENCES doctors(id),
    nurse_id INTEGER REFERENCES nurses(id),
    procedure_name TEXT NOT NULL,
    procedure_type TEXT,
    room TEXT,
    procedure_date TEXT NOT NULL,
    duration_minutes INTEGER,
    outcome TEXT NOT NULL DEFAULT 'completed',
    notes TEXT
);
CREATE INDEX idx_procedures_patient ON procedures(patient_id);

INSERT INTO procedures VALUES (1, 1, 1, 1, 'ECG', 'diagnostic', 'Room 201', '2024-01-15', 15, 'completed', 'Normal sinus rhythm');
INSERT INTO procedures VALUES (2, 8, 1, 1, 'Echocardiogram', 'diagnostic', 'Room 201', '2024-03-15', 45, 'completed', 'Normal EF 60%');
INSERT INTO procedures VALUES (3, 2, 2, 2, 'Chest X-Ray', 'imaging', 'Room 101', '2024-01-20', 10, 'completed', 'Standard PA/LAT');
INSERT INTO procedures VALUES (4, 1, 2, 2, 'CT Chest', 'imaging', 'Room 102', '2024-04-15', 30, 'completed', 'With IV contrast');
INSERT INTO procedures VALUES (5, 9, 2, 2, 'Brain MRI', 'imaging', 'Room 102', '2024-03-20', 45, 'completed', 'With gadolinium');
INSERT INTO procedures VALUES (6, 3, 1, 1, 'Blood Pressure Monitoring', 'diagnostic', 'Room 201', '2024-05-10', 20, 'completed', '24-hour ABPM setup');
INSERT INTO procedures VALUES (7, 7, 7, 7, 'Abdominal Ultrasound', 'imaging', 'Room 115', '2024-03-10', 30, 'completed', 'Fasting study');
INSERT INTO procedures VALUES (8, 10, 4, 4, 'EMG', 'diagnostic', 'Room 205', '2024-04-01', 40, 'completed', 'Upper and lower extremity');

-- =============================================
-- ALLERGY, HISTORY, IMMUNIZATIONS
-- =============================================

CREATE TABLE allergies (
    id INTEGER PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id),
    allergen TEXT NOT NULL,
    reaction TEXT,
    severity TEXT NOT NULL DEFAULT 'moderate',
    discovered_date TEXT,
    notes TEXT
);
CREATE INDEX idx_allergies_patient ON allergies(patient_id);

INSERT INTO allergies VALUES (1, 1, 'Penicillin', 'Rash', 'moderate', '2020-05-10', 'Confirmed allergy');
INSERT INTO allergies VALUES (2, 2, 'Sulfa drugs', 'Hives', 'severe', '2021-02-15', 'Anaphylaxis risk');
INSERT INTO allergies VALUES (3, 3, 'Latex', 'Skin irritation', 'mild', '2020-08-20', 'Use non-latex gloves');
INSERT INTO allergies VALUES (4, 4, 'Aspirin', 'GI upset', 'moderate', '2022-03-10', 'Use acetaminophen instead');
INSERT INTO allergies VALUES (5, 5, 'Shellfish', 'Swelling', 'severe', '2021-06-01', 'Carry EpiPen');
INSERT INTO allergies VALUES (6, 6, 'Codeine', 'Nausea', 'mild', '2024-03-01', 'Discovered during surgery prep');
INSERT INTO allergies VALUES (7, 8, 'Iodine contrast', 'Hives', 'moderate', '2024-03-15', 'Pre-medicate before contrast CT');
INSERT INTO allergies VALUES (8, 10, 'NSAIDs', 'GI bleeding', 'severe', '2023-05-20', 'History of GI bleed');
INSERT INTO allergies VALUES (9, 1, 'Bee stings', 'Anaphylaxis', 'severe', '2019-08-15', 'Carry EpiPen');
INSERT INTO allergies VALUES (10, 7, 'Amoxicillin', 'Rash', 'mild', '2022-11-10', 'Mild reaction');

CREATE TABLE medical_history (
    id INTEGER PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id),
    condition TEXT NOT NULL,
    onset_date TEXT,
    resolved_date TEXT,
    is_chronic INTEGER NOT NULL DEFAULT 0,
    notes TEXT
);
CREATE INDEX idx_medical_history_patient ON medical_history(patient_id);

INSERT INTO medical_history VALUES (1, 1, 'Childhood asthma', '2000-01-01', '2008-06-15', 0, 'Outgrown');
INSERT INTO medical_history VALUES (2, 1, 'Hypertension', '2024-01-15', NULL, 1, 'Current medication');
INSERT INTO medical_history VALUES (3, 2, 'Hyperlipidemia', '2024-01-20', NULL, 1, 'On statin therapy');
INSERT INTO medical_history VALUES (4, 3, 'Broken arm', '2015-07-10', '2015-09-15', 0, 'Left radius fracture');
INSERT INTO medical_history VALUES (5, 4, 'Migraines', '2020-03-01', NULL, 1, 'Chronic with aura');
INSERT INTO medical_history VALUES (6, 5, 'Tonsillectomy', '2005-04-20', '2005-05-10', 0, 'Age 10');
INSERT INTO medical_history VALUES (7, 6, 'Appendicitis', '2024-03-01', '2024-03-15', 0, 'Surgical removal');
INSERT INTO medical_history VALUES (8, 7, 'Vitamin D deficiency', '2024-03-10', NULL, 1, 'On supplements');
INSERT INTO medical_history VALUES (9, 8, 'Hypothyroidism', '2024-03-15', NULL, 1, 'On levothyroxine');
INSERT INTO medical_history VALUES (10, 10, 'Type 2 Diabetes', '2020-06-01', NULL, 1, 'Diet controlled');
INSERT INTO medical_history VALUES (11, 10, 'Peripheral neuropathy', '2024-04-01', NULL, 1, 'Under investigation');
INSERT INTO medical_history VALUES (12, 11, 'ACL reconstruction', '2018-09-15', '2019-03-01', 0, 'Right knee, full recovery');
INSERT INTO medical_history VALUES (13, 2, 'Hypertension', '2024-01-20', NULL, 1, 'Monitoring');
INSERT INTO medical_history VALUES (14, 12, 'GERD', '2022-05-01', NULL, 1, 'On PPI therapy');

CREATE TABLE immunizations (
    id INTEGER PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id),
    vaccine TEXT NOT NULL,
    dose_number INTEGER NOT NULL DEFAULT 1,
    administered_date TEXT NOT NULL,
    administered_by_id INTEGER REFERENCES nurses(id),
    lot_number TEXT,
    site TEXT,
    notes TEXT
);
CREATE INDEX idx_immunizations_patient ON immunizations(patient_id);

INSERT INTO immunizations VALUES (1, 1, 'Influenza', 1, '2024-01-15', 1, 'LOT-FLU-2401', 'Left deltoid', 'Annual flu shot');
INSERT INTO immunizations VALUES (2, 2, 'Influenza', 1, '2024-01-20', 1, 'LOT-FLU-2401', 'Left deltoid', 'Annual flu shot');
INSERT INTO immunizations VALUES (3, 3, 'Tdap', 1, '2024-02-05', 3, 'LOT-TDAP-2402', 'Right deltoid', '10-year booster');
INSERT INTO immunizations VALUES (4, 4, 'COVID-19 Booster', 3, '2024-02-10', 4, 'LOT-COV-2403', 'Left deltoid', 'Updated booster');
INSERT INTO immunizations VALUES (5, 5, 'Influenza', 1, '2024-02-15', 5, 'LOT-FLU-2401', 'Left deltoid', 'Annual flu shot');
INSERT INTO immunizations VALUES (6, 6, 'Tetanus', 1, '2024-03-01', 6, 'LOT-TET-2404', 'Right deltoid', 'Pre-surgery update');
INSERT INTO immunizations VALUES (7, 7, 'HPV', 2, '2024-03-10', 7, 'LOT-HPV-2405', 'Left deltoid', 'Second dose');
INSERT INTO immunizations VALUES (8, 8, 'Hepatitis B', 3, '2024-03-15', 8, 'LOT-HEPB-2406', 'Right deltoid', 'Third dose series');
INSERT INTO immunizations VALUES (9, 9, 'Influenza', 1, '2024-03-20', 9, 'LOT-FLU-2407', 'Left deltoid', 'Annual flu shot');
INSERT INTO immunizations VALUES (10, 10, 'Pneumococcal', 1, '2024-04-01', 4, 'LOT-PCV-2408', 'Left deltoid', 'Age-related recommendation');
INSERT INTO immunizations VALUES (11, 11, 'Influenza', 1, '2024-04-10', 3, 'LOT-FLU-2409', 'Left deltoid', 'Annual flu shot');
INSERT INTO immunizations VALUES (12, 12, 'COVID-19 Booster', 4, '2024-07-10', 1, 'LOT-COV-2410', 'Right deltoid', 'Latest booster');

-- =============================================
-- LAB & REFERRALS
-- =============================================

CREATE TABLE lab_orders (
    id INTEGER PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id),
    doctor_id INTEGER NOT NULL REFERENCES doctors(id),
    test_name TEXT NOT NULL,
    test_code TEXT,
    priority TEXT NOT NULL DEFAULT 'routine',
    order_date TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'ordered',
    notes TEXT
);
CREATE INDEX idx_lab_orders_patient ON lab_orders(patient_id);

INSERT INTO lab_orders VALUES (1, 1, 1, 'Complete Blood Count', 'CBC', 'routine', '2024-01-15', 'completed', 'Annual labs');
INSERT INTO lab_orders VALUES (2, 2, 1, 'Lipid Panel', 'LIPID', 'routine', '2024-01-20', 'completed', 'Fasting required');
INSERT INTO lab_orders VALUES (3, 5, 5, 'Comprehensive Metabolic Panel', 'CMP', 'routine', '2024-02-15', 'completed', 'Annual labs');
INSERT INTO lab_orders VALUES (4, 8, 1, 'Thyroid Panel', 'THYROID', 'stat', '2024-03-15', 'completed', 'Suspected hypothyroidism');
INSERT INTO lab_orders VALUES (5, 1, 1, 'Basic Metabolic Panel', 'BMP', 'routine', '2024-04-15', 'completed', 'Renal function check');
INSERT INTO lab_orders VALUES (6, 2, 1, 'HbA1c', 'HBA1C', 'routine', '2024-05-01', 'completed', 'Diabetes screening');
INSERT INTO lab_orders VALUES (7, 3, 3, 'ESR', 'ESR', 'routine', '2024-02-05', 'completed', 'Inflammation marker');
INSERT INTO lab_orders VALUES (8, 4, 4, 'Vitamin B12', 'B12', 'routine', '2024-05-15', 'completed', 'Neuropathy workup');
INSERT INTO lab_orders VALUES (9, 6, 6, 'CBC with Diff', 'CBCD', 'stat', '2024-03-01', 'completed', 'Pre-surgery');
INSERT INTO lab_orders VALUES (10, 7, 7, 'Vitamin D Level', 'VITD', 'routine', '2024-03-10', 'completed', 'Fatigue workup');
INSERT INTO lab_orders VALUES (11, 10, 4, 'Nerve Conduction Study', 'NCS', 'routine', '2024-04-01', 'pending', 'Peripheral neuropathy');
INSERT INTO lab_orders VALUES (12, 9, 2, 'CBC', 'CBC', 'routine', '2024-03-20', 'completed', 'Routine labs');

CREATE TABLE referrals (
    id INTEGER PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id),
    from_doctor_id INTEGER NOT NULL REFERENCES doctors(id),
    to_doctor_id INTEGER NOT NULL REFERENCES doctors(id),
    reason TEXT NOT NULL,
    priority TEXT NOT NULL DEFAULT 'routine',
    referral_date TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    notes TEXT
);
CREATE INDEX idx_referrals_patient ON referrals(patient_id);

INSERT INTO referrals VALUES (1, 1, 1, 2, 'CT chest for cardiac workup', 'urgent', '2024-04-10', 'completed', 'Rule out PE');
INSERT INTO referrals VALUES (2, 3, 3, 2, 'MRI knee for surgical planning', 'routine', '2024-02-06', 'completed', 'Meniscal evaluation');
INSERT INTO referrals VALUES (3, 4, 4, 2, 'Brain MRI for headache workup', 'routine', '2024-05-10', 'completed', 'Rule out structural cause');
INSERT INTO referrals VALUES (4, 6, 6, 2, 'CT abdomen for appendicitis', 'stat', '2024-03-01', 'completed', 'Acute abdomen');
INSERT INTO referrals VALUES (5, 7, 7, 5, 'Dermatology for skin lesion', 'routine', '2024-06-01', 'completed', 'Suspicious mole');
INSERT INTO referrals VALUES (6, 8, 1, 4, 'Neurology for tingling', 'routine', '2024-06-15', 'pending', 'Peripheral symptoms');
INSERT INTO referrals VALUES (7, 10, 4, 3, 'Orthopedics for back pain', 'routine', '2024-04-05', 'completed', 'Spine evaluation');
INSERT INTO referrals VALUES (8, 2, 1, 6, 'Surgery for hernia evaluation', 'routine', '2024-04-25', 'completed', 'Inguinal hernia');

-- =============================================
-- BILLING & PAYMENTS
-- =============================================

CREATE TABLE billing (
    id INTEGER PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id),
    doctor_id INTEGER REFERENCES doctors(id),
    service_description TEXT NOT NULL,
    total_amount REAL NOT NULL,
    insurance_covered REAL NOT NULL DEFAULT 0.0,
    patient_responsibility REAL NOT NULL,
    billing_date TEXT NOT NULL,
    due_date TEXT,
    status TEXT NOT NULL DEFAULT 'pending',
    notes TEXT
);
CREATE INDEX idx_billing_patient ON billing(patient_id);
CREATE INDEX idx_billing_status ON billing(status);

INSERT INTO billing VALUES (1, 1, 1, 'Cardiac Checkup', 250.0, 200.0, 50.0, '2024-01-15', '2024-02-15', 'paid', NULL);
INSERT INTO billing VALUES (2, 2, 2, 'Chest X-Ray', 350.0, 280.0, 70.0, '2024-01-20', '2024-02-20', 'paid', NULL);
INSERT INTO billing VALUES (3, 3, 3, 'Knee Consultation', 200.0, 160.0, 40.0, '2024-02-05', '2024-03-05', 'paid', NULL);
INSERT INTO billing VALUES (4, 4, 4, 'Neurology Follow-up', 175.0, 140.0, 35.0, '2024-02-10', '2024-03-10', 'paid', NULL);
INSERT INTO billing VALUES (5, 5, 5, 'Dermatology Visit', 150.0, 120.0, 30.0, '2024-02-15', '2024-03-15', 'paid', NULL);
INSERT INTO billing VALUES (6, 6, 6, 'Appendectomy', 8500.0, 7650.0, 850.0, '2024-03-01', '2024-04-01', 'paid', 'Surgery + recovery');
INSERT INTO billing VALUES (7, 7, 7, 'Wellness Checkup', 150.0, 120.0, 30.0, '2024-03-10', '2024-04-10', 'paid', NULL);
INSERT INTO billing VALUES (8, 8, 1, 'Echocardiogram', 800.0, 640.0, 160.0, '2024-03-15', '2024-04-15', 'paid', NULL);
INSERT INTO billing VALUES (9, 9, 2, 'Brain MRI', 1200.0, 960.0, 240.0, '2024-03-20', '2024-04-20', 'paid', NULL);
INSERT INTO billing VALUES (10, 10, 4, 'Neurology Consultation', 225.0, 180.0, 45.0, '2024-04-01', '2024-05-01', 'pending', NULL);
INSERT INTO billing VALUES (11, 11, 3, 'Shoulder Follow-up', 175.0, 140.0, 35.0, '2024-04-10', '2024-05-10', 'paid', NULL);
INSERT INTO billing VALUES (12, 1, 2, 'CT Chest', 950.0, 760.0, 190.0, '2024-04-15', '2024-05-15', 'paid', NULL);
INSERT INTO billing VALUES (13, 2, 6, 'Hernia Consultation', 200.0, 160.0, 40.0, '2024-05-01', '2024-06-01', 'pending', NULL);
INSERT INTO billing VALUES (14, 3, 1, 'BP Monitoring', 125.0, 100.0, 25.0, '2024-05-10', '2024-06-10', 'paid', NULL);
INSERT INTO billing VALUES (15, 4, 2, 'Brain MRI', 1200.0, 960.0, 240.0, '2024-05-15', '2024-06-15', 'pending', NULL);
INSERT INTO billing VALUES (16, 6, 6, 'Post-Op Follow-up', 125.0, 100.0, 25.0, '2024-06-10', '2024-07-10', 'paid', NULL);
INSERT INTO billing VALUES (17, 7, 5, 'Mole Assessment', 175.0, 140.0, 35.0, '2024-06-15', '2024-07-15', 'pending', NULL);
INSERT INTO billing VALUES (18, 8, 4, 'Nerve Conduction Test', 450.0, 360.0, 90.0, '2024-07-01', '2024-08-01', 'pending', NULL);

CREATE TABLE payments (
    id INTEGER PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id),
    billing_id INTEGER NOT NULL REFERENCES billing(id),
    amount REAL NOT NULL,
    payment_method TEXT NOT NULL DEFAULT 'insurance',
    payment_date TEXT NOT NULL,
    reference_number TEXT,
    status TEXT NOT NULL DEFAULT 'completed',
    notes TEXT
);
CREATE INDEX idx_payments_patient ON payments(patient_id);
CREATE INDEX idx_payments_billing ON payments(billing_id);

INSERT INTO payments VALUES (1, 1, 1, 50.0, 'credit_card', '2024-01-15', 'TXN-PAY-001', 'completed', 'Copay');
INSERT INTO payments VALUES (2, 2, 2, 70.0, 'debit_card', '2024-01-20', 'TXN-PAY-002', 'completed', 'Copay');
INSERT INTO payments VALUES (3, 3, 3, 40.0, 'credit_card', '2024-02-05', 'TXN-PAY-003', 'completed', 'Copay');
INSERT INTO payments VALUES (4, 4, 4, 35.0, 'cash', '2024-02-10', 'TXN-PAY-004', 'completed', 'Copay');
INSERT INTO payments VALUES (5, 5, 5, 30.0, 'credit_card', '2024-02-15', 'TXN-PAY-005', 'completed', 'Copay');
INSERT INTO payments VALUES (6, 6, 6, 850.0, 'insurance', '2024-03-15', 'TXN-PAY-006', 'completed', 'Patient responsibility');
INSERT INTO payments VALUES (7, 7, 7, 30.0, 'credit_card', '2024-03-10', 'TXN-PAY-007', 'completed', 'Copay');
INSERT INTO payments VALUES (8, 8, 8, 160.0, 'debit_card', '2024-03-20', 'TXN-PAY-008', 'completed', 'After insurance');
INSERT INTO payments VALUES (9, 9, 9, 240.0, 'credit_card', '2024-04-01', 'TXN-PAY-009', 'completed', 'After insurance');
INSERT INTO payments VALUES (10, 11, 11, 35.0, 'debit_card', '2024-04-15', 'TXN-PAY-010', 'completed', 'Copay');
INSERT INTO payments VALUES (11, 1, 12, 190.0, 'credit_card', '2024-04-20', 'TXN-PAY-011', 'completed', 'After insurance');
INSERT INTO payments VALUES (12, 3, 14, 25.0, 'cash', '2024-05-10', 'TXN-PAY-012', 'completed', 'Copay');

-- =============================================
-- FACILITY & OPERATIONS
-- =============================================

CREATE TABLE rooms (
    id INTEGER PRIMARY KEY,
    room_number TEXT NOT NULL UNIQUE,
    floor INTEGER NOT NULL,
    room_type TEXT NOT NULL,
    department_id INTEGER NOT NULL REFERENCES departments(id),
    capacity INTEGER NOT NULL DEFAULT 1,
    equipment TEXT,
    is_active INTEGER NOT NULL DEFAULT 1
);
CREATE INDEX idx_rooms_dept ON rooms(department_id);

INSERT INTO rooms VALUES (1, 'Room 101', 1, 'examination', 2, 1, 'X-ray machine', 1);
INSERT INTO rooms VALUES (2, 'Room 102', 1, 'imaging', 2, 1, 'CT scanner, MRI machine', 1);
INSERT INTO rooms VALUES (3, 'Room 108', 1, 'examination', 5, 1, 'Dermatoscope, biopsy tools', 1);
INSERT INTO rooms VALUES (4, 'Room 110', 1, 'examination', 7, 2, 'Pediatric equipment', 1);
INSERT INTO rooms VALUES (5, 'Room 201', 2, 'examination', 1, 1, 'ECG machine, echocardiogram', 1);
INSERT INTO rooms VALUES (6, 'Room 205', 2, 'examination', 4, 1, 'EMG machine, reflex tools', 1);
INSERT INTO rooms VALUES (7, 'Room 301', 3, 'examination', 3, 1, 'Bone density scanner', 1);
INSERT INTO rooms VALUES (8, 'Room 305', 3, 'operating', 6, 1, 'Full surgical suite', 1);
INSERT INTO rooms VALUES (9, 'Room 210', 2, 'laboratory', 8, 2, 'Blood draw station', 1);
INSERT INTO rooms VALUES (10, 'Room 115', 1, 'ultrasound', 2, 1, 'Ultrasound machine', 1);

CREATE TABLE wards (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    floor INTEGER NOT NULL,
    ward_type TEXT NOT NULL,
    total_beds INTEGER NOT NULL DEFAULT 0
);

INSERT INTO wards VALUES (1, 'General Ward', 1, 'general', 3);
INSERT INTO wards VALUES (2, 'ICU', 2, 'icu', 2);
INSERT INTO wards VALUES (3, 'Maternity', 3, 'maternity', 2);
INSERT INTO wards VALUES (4, 'Surgical', 4, 'post-op', 2);
INSERT INTO wards VALUES (5, 'Pediatric', 5, 'pediatric', 1);

CREATE TABLE beds (
    id INTEGER PRIMARY KEY,
    ward_id INTEGER NOT NULL REFERENCES wards(id),
    bed_number TEXT NOT NULL,
    bed_type TEXT NOT NULL DEFAULT 'standard',
    is_occupied INTEGER NOT NULL DEFAULT 0,
    patient_id INTEGER REFERENCES patients(id),
    admit_date TEXT,
    notes TEXT
);
CREATE INDEX idx_beds_ward ON beds(ward_id);
CREATE INDEX idx_beds_patient ON beds(patient_id);

INSERT INTO beds VALUES (1, 1, 'GW-101', 'standard', 0, NULL, NULL, NULL);
INSERT INTO beds VALUES (2, 1, 'GW-102', 'standard', 1, 6, '2024-03-01', 'Post-appendectomy');
INSERT INTO beds VALUES (3, 1, 'GW-103', 'standard', 0, NULL, NULL, NULL);
INSERT INTO beds VALUES (4, 2, 'ICU-201', 'icu', 0, NULL, NULL, NULL);
INSERT INTO beds VALUES (5, 2, 'ICU-202', 'icu', 0, NULL, NULL, NULL);
INSERT INTO beds VALUES (6, 3, 'MAT-301', 'maternity', 0, NULL, NULL, NULL);
INSERT INTO beds VALUES (7, 3, 'MAT-302', 'maternity', 0, NULL, NULL, NULL);
INSERT INTO beds VALUES (8, 4, 'SR-401', 'post-op', 0, NULL, NULL, NULL);
INSERT INTO beds VALUES (9, 4, 'SR-402', 'post-op', 1, 3, '2024-03-15', 'Post-arthroscopy recovery');
INSERT INTO beds VALUES (10, 5, 'PED-501', 'pediatric', 0, NULL, NULL, NULL);

CREATE TABLE equipment (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    equipment_type TEXT NOT NULL,
    serial_number TEXT UNIQUE,
    department_id INTEGER NOT NULL REFERENCES departments(id),
    room TEXT,
    purchase_date TEXT,
    last_service_date TEXT,
    next_service_date TEXT,
    status TEXT NOT NULL DEFAULT 'operational',
    notes TEXT
);
CREATE INDEX idx_equipment_dept ON equipment(department_id);

INSERT INTO equipment VALUES (1, 'GE Optima XR240', 'X-Ray Machine', 'SN-XR-001', 2, 'Room 101', '2020-06-15', '2024-01-10', '2024-07-10', 'operational', 'Digital radiography');
INSERT INTO equipment VALUES (2, 'Siemens SOMATOM', 'CT Scanner', 'SN-CT-001', 2, 'Room 102', '2021-03-20', '2024-02-15', '2024-08-15', 'operational', '128-slice CT');
INSERT INTO equipment VALUES (3, 'GE SIGNA Premier', 'MRI Machine', 'SN-MR-001', 2, 'Room 102', '2021-09-01', '2024-03-01', '2024-09-01', 'operational', '3T MRI');
INSERT INTO equipment VALUES (4, 'Philips EPIQ 7', 'Ultrasound', 'SN-US-001', 2, 'Room 115', '2022-01-10', '2024-01-15', '2024-07-15', 'operational', 'General purpose');
INSERT INTO equipment VALUES (5, 'GE MAC 5500', 'ECG Machine', 'SN-ECG-001', 1, 'Room 201', '2020-03-01', '2024-02-01', '2024-08-01', 'operational', '12-lead ECG');
INSERT INTO equipment VALUES (6, 'Philips EPIQ CVx', 'Echocardiogram', 'SN-ECHO-001', 1, 'Room 201', '2021-06-15', '2024-03-15', '2024-09-15', 'operational', 'Cardiac ultrasound');
INSERT INTO equipment VALUES (7, 'Natus Nicolet EDX', 'EMG Machine', 'SN-EMG-001', 4, 'Room 205', '2022-04-01', '2024-01-20', '2024-07-20', 'operational', 'EMG/NCS system');
INSERT INTO equipment VALUES (8, 'Hologic Horizon', 'Bone Density Scanner', 'SN-DEXA-001', 3, 'Room 301', '2022-08-15', '2024-02-20', '2024-08-20', 'operational', 'DEXA scanner');

CREATE TABLE pharmacy_inventory (
    id INTEGER PRIMARY KEY,
    medication_id INTEGER NOT NULL REFERENCES medications(id),
    dosage TEXT NOT NULL,
    form TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    unit TEXT NOT NULL DEFAULT 'tablets',
    batch_number TEXT,
    expiry_date TEXT NOT NULL,
    reorder_level INTEGER NOT NULL DEFAULT 50,
    supplier TEXT,
    last_restocked TEXT
);
CREATE INDEX idx_pharmacy_medication ON pharmacy_inventory(medication_id);

INSERT INTO pharmacy_inventory VALUES (1, 1, '10mg', 'Tablet', 500, 'tablets', 'BATCH-LIS-001', '2025-06-30', 100, 'McKesson', '2024-01-05');
INSERT INTO pharmacy_inventory VALUES (2, 2, '20mg', 'Tablet', 400, 'tablets', 'BATCH-ATV-001', '2025-08-15', 80, 'Cardinal Health', '2024-02-10');
INSERT INTO pharmacy_inventory VALUES (3, 6, '500mg', 'Capsule', 300, 'capsules', 'BATCH-AMX-001', '2025-03-20', 60, 'McKesson', '2024-01-15');
INSERT INTO pharmacy_inventory VALUES (4, 3, '400mg', 'Tablet', 1000, 'tablets', 'BATCH-IBU-001', '2025-12-31', 200, 'AmerisourceBergen', '2024-03-01');
INSERT INTO pharmacy_inventory VALUES (5, 4, '50mg', 'Tablet', 150, 'tablets', 'BATCH-SUM-001', '2025-05-15', 30, 'Cardinal Health', '2024-01-20');
INSERT INTO pharmacy_inventory VALUES (6, 7, '300mg', 'Capsule', 600, 'capsules', 'BATCH-GAB-001', '2025-09-30', 100, 'McKesson', '2024-02-15');
INSERT INTO pharmacy_inventory VALUES (7, 8, '50mcg', 'Tablet', 350, 'tablets', 'BATCH-LEV-001', '2025-07-20', 70, 'AmerisourceBergen', '2024-03-10');
INSERT INTO pharmacy_inventory VALUES (8, 9, '25mg', 'Tablet', 450, 'tablets', 'BATCH-MET-001', '2025-10-15', 90, 'Cardinal Health', '2024-04-01');
INSERT INTO pharmacy_inventory VALUES (9, 10, '81mg', 'Tablet', 2000, 'tablets', 'BATCH-ASP-001', '2026-01-31', 300, 'McKesson', '2024-01-01');
INSERT INTO pharmacy_inventory VALUES (10, 5, '1%', 'Cream', 100, 'tubes', 'BATCH-HYD-001', '2025-04-30', 20, 'AmerisourceBergen', '2024-02-01');

-- =============================================
-- SCHEDULING & ADMIN
-- =============================================

CREATE TABLE staff_shifts (
    id INTEGER PRIMARY KEY,
    staff_email TEXT NOT NULL,
    staff_role TEXT NOT NULL,
    department_id INTEGER NOT NULL REFERENCES departments(id),
    shift_date TEXT NOT NULL,
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    shift_type TEXT NOT NULL DEFAULT 'regular',
    notes TEXT
);
CREATE INDEX idx_shifts_date ON staff_shifts(shift_date);

INSERT INTO staff_shifts VALUES (1, 'anna.scott@healthfirst.com', 'Nurse', 1, '2024-01-15', '07:00', '15:00', 'day', NULL);
INSERT INTO staff_shifts VALUES (2, 'brian.hall@healthfirst.com', 'Nurse', 2, '2024-01-15', '23:00', '07:00', 'night', NULL);
INSERT INTO staff_shifts VALUES (3, 'clara.young@healthfirst.com', 'Nurse', 3, '2024-02-05', '07:00', '15:00', 'day', NULL);
INSERT INTO staff_shifts VALUES (4, 'dr.williams@healthfirst.com', 'Doctor', 1, '2024-01-15', '08:00', '17:00', 'day', 'Regular clinic');
INSERT INTO staff_shifts VALUES (5, 'dr.lee@healthfirst.com', 'Doctor', 2, '2024-01-20', '08:00', '17:00', 'day', 'Regular clinic');
INSERT INTO staff_shifts VALUES (6, 'felix.lopez@healthfirst.com', 'Nurse', 6, '2024-03-02', '06:00', '14:00', 'day', 'Surgery assist');
INSERT INTO staff_shifts VALUES (7, 'dr.brown@healthfirst.com', 'Doctor', 6, '2024-03-02', '07:00', '16:00', 'day', 'Surgery day');
INSERT INTO staff_shifts VALUES (8, 'iris.carter@healthfirst.com', 'Nurse', 8, '2024-03-20', '23:00', '07:00', 'night', 'ER coverage');
INSERT INTO staff_shifts VALUES (9, 'gina.allen@healthfirst.com', 'Nurse', 7, '2024-03-10', '07:00', '15:00', 'day', NULL);
INSERT INTO staff_shifts VALUES (10, 'derek.king@healthfirst.com', 'Nurse', 4, '2024-04-01', '23:00', '07:00', 'night', NULL);

CREATE TABLE consent_forms (
    id INTEGER PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id),
    procedure_name TEXT NOT NULL,
    doctor_id INTEGER NOT NULL REFERENCES doctors(id),
    signed_date TEXT NOT NULL,
    witness TEXT,
    form_type TEXT NOT NULL DEFAULT 'procedure',
    status TEXT NOT NULL DEFAULT 'signed',
    notes TEXT
);
CREATE INDEX idx_consent_patient ON consent_forms(patient_id);

INSERT INTO consent_forms VALUES (1, 6, 'Appendectomy', 6, '2024-03-01', 'Rosa Garcia', 'surgery', 'signed', 'Pre-op consent');
INSERT INTO consent_forms VALUES (2, 3, 'Knee Arthroscopy', 3, '2024-03-14', 'Dan Zhang', 'surgery', 'signed', 'Pre-op consent');
INSERT INTO consent_forms VALUES (3, 5, 'Skin Biopsy', 5, '2024-02-15', NULL, 'procedure', 'signed', 'Minor procedure');
INSERT INTO consent_forms VALUES (4, 10, 'Skin Biopsy', 5, '2024-04-05', NULL, 'procedure', 'signed', 'Minor procedure');
INSERT INTO consent_forms VALUES (5, 7, 'Skin Excision', 5, '2024-06-15', 'James Kim', 'surgery', 'signed', 'Excisional biopsy');
INSERT INTO consent_forms VALUES (6, 1, 'CT with Contrast', 2, '2024-04-15', NULL, 'imaging', 'signed', 'Contrast consent');
INSERT INTO consent_forms VALUES (7, 9, 'MRI with Contrast', 2, '2024-03-20', NULL, 'imaging', 'signed', 'Gadolinium consent');
INSERT INTO consent_forms VALUES (8, 6, 'Hernia Repair', 6, '2024-07-25', 'Rosa Garcia', 'surgery', 'signed', 'Pre-op consent');

CREATE TABLE follow_ups (
    id INTEGER PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id),
    doctor_id INTEGER NOT NULL REFERENCES doctors(id),
    original_visit_date TEXT,
    scheduled_date TEXT NOT NULL,
    reason TEXT,
    status TEXT NOT NULL DEFAULT 'scheduled',
    notes TEXT
);
CREATE INDEX idx_followups_patient ON follow_ups(patient_id);

INSERT INTO follow_ups VALUES (1, 1, 1, '2024-01-15', '2024-04-15', 'BP recheck', 'completed', '3-month follow-up');
INSERT INTO follow_ups VALUES (2, 2, 1, '2024-01-20', '2024-04-20', 'Lipid recheck', 'completed', '3-month labs');
INSERT INTO follow_ups VALUES (3, 3, 3, '2024-03-15', '2024-06-15', 'Post-surgery knee eval', 'scheduled', '3-month post-op');
INSERT INTO follow_ups VALUES (4, 4, 4, '2024-02-10', '2024-05-10', 'Migraine management', 'completed', 'Medication review');
INSERT INTO follow_ups VALUES (5, 6, 6, '2024-03-02', '2024-06-10', 'Post-appendectomy', 'completed', '3-month check');
INSERT INTO follow_ups VALUES (6, 8, 1, '2024-03-15', '2024-06-15', 'Thyroid recheck', 'scheduled', 'Repeat TSH');
INSERT INTO follow_ups VALUES (7, 9, 2, '2024-03-20', '2024-09-20', 'Brain MRI follow-up', 'scheduled', '6-month recheck');
INSERT INTO follow_ups VALUES (8, 10, 4, '2024-04-01', '2024-07-01', 'Neuropathy follow-up', 'scheduled', 'NCS results review');
INSERT INTO follow_ups VALUES (9, 11, 3, '2024-04-10', '2024-07-10', 'Shoulder recheck', 'scheduled', '3-month follow-up');
INSERT INTO follow_ups VALUES (10, 7, 5, '2024-06-15', '2024-09-15', 'BCC post-excision check', 'scheduled', '3-month surveillance');

CREATE TABLE waiting_list (
    id INTEGER PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id),
    doctor_id INTEGER NOT NULL REFERENCES doctors(id),
    procedure_name TEXT NOT NULL,
    priority TEXT NOT NULL DEFAULT 'routine',
    added_date TEXT NOT NULL,
    target_date TEXT,
    status TEXT NOT NULL DEFAULT 'waiting',
    notes TEXT
);
CREATE INDEX idx_waiting_patient ON waiting_list(patient_id);

INSERT INTO waiting_list VALUES (1, 6, 6, 'Inguinal Hernia Repair', 'routine', '2024-05-01', '2024-08-01', 'scheduled', 'Surgery date confirmed');
INSERT INTO waiting_list VALUES (2, 3, 3, 'Knee Replacement Consultation', 'routine', '2024-06-01', '2024-09-01', 'waiting', 'If conservative treatment fails');
INSERT INTO waiting_list VALUES (3, 10, 4, 'Nerve Conduction Study', 'urgent', '2024-04-01', '2024-07-01', 'scheduled', 'Neuropathy workup');
INSERT INTO waiting_list VALUES (4, 8, 4, 'Nerve Conduction Test', 'routine', '2024-06-15', '2024-08-15', 'waiting', 'Tingling evaluation');
INSERT INTO waiting_list VALUES (5, 2, 6, 'Hernia Evaluation', 'routine', '2024-04-25', '2024-07-25', 'completed', 'Seen and assessed');
INSERT INTO waiting_list VALUES (6, 11, 3, 'Shoulder MRI', 'routine', '2024-04-15', '2024-05-15', 'completed', 'MRI done 2024-04-10');

CREATE TABLE audit_log (
    id INTEGER PRIMARY KEY,
    user_email TEXT NOT NULL,
    action TEXT NOT NULL,
    table_name TEXT,
    record_id INTEGER,
    timestamp TEXT NOT NULL,
    ip_address TEXT,
    details TEXT
);
CREATE INDEX idx_audit_timestamp ON audit_log(timestamp);

INSERT INTO audit_log VALUES (1, 'dr.williams@healthfirst.com', 'CREATE', 'prescriptions', 1, '2024-01-15 09:30:00', '192.168.1.10', 'New prescription for alice.chen@email.com');
INSERT INTO audit_log VALUES (2, 'anna.scott@healthfirst.com', 'CREATE', 'vital_signs', 1, '2024-01-15 08:45:00', '192.168.1.20', 'Vitals recorded for alice.chen@email.com');
INSERT INTO audit_log VALUES (3, 'dr.lee@healthfirst.com', 'CREATE', 'xray_reports', 1, '2024-01-15 11:00:00', '192.168.1.11', 'X-ray report created');
INSERT INTO audit_log VALUES (4, 'dr.brown@healthfirst.com', 'CREATE', 'surgeries', 1, '2024-03-02 10:00:00', '192.168.1.15', 'Surgery record for appendectomy');
INSERT INTO audit_log VALUES (5, 'dr.williams@healthfirst.com', 'UPDATE', 'prescriptions', 1, '2024-04-15 10:15:00', '192.168.1.10', 'Refill approved');
INSERT INTO audit_log VALUES (6, 'admin@healthfirst.com', 'CREATE', 'patients', 12, '2023-08-28 14:00:00', '192.168.1.1', 'New patient registered');
INSERT INTO audit_log VALUES (7, 'dr.clark@healthfirst.com', 'CREATE', 'pathology_reports', 2, '2024-02-15 15:30:00', '192.168.1.14', 'Pathology report created');
INSERT INTO audit_log VALUES (8, 'dr.nguyen@healthfirst.com', 'UPDATE', 'diagnoses', 4, '2024-05-15 11:30:00', '192.168.1.13', 'Diagnosis updated with new medication');
INSERT INTO audit_log VALUES (9, 'felix.lopez@healthfirst.com', 'CREATE', 'vital_signs', 6, '2024-03-01 07:30:00', '192.168.1.25', 'Pre-surgery vitals');
INSERT INTO audit_log VALUES (10, 'dr.lee@healthfirst.com', 'CREATE', 'mri_reports', 1, '2024-03-20 14:30:00', '192.168.1.11', 'MRI report created');

-- =============================================
-- COMPUTED / STATS TABLES
-- =============================================

CREATE TABLE patient_stats (
    id INTEGER PRIMARY KEY,
    patient_id INTEGER NOT NULL UNIQUE REFERENCES patients(id),
    total_appointments INTEGER NOT NULL DEFAULT 0,
    total_diagnoses INTEGER NOT NULL DEFAULT 0,
    total_prescriptions INTEGER NOT NULL DEFAULT 0,
    total_billing REAL NOT NULL DEFAULT 0.0,
    total_paid REAL NOT NULL DEFAULT 0.0,
    last_visit_date TEXT
);
CREATE INDEX idx_patient_stats_patient ON patient_stats(patient_id);

INSERT INTO patient_stats VALUES (1, 1, 3, 2, 2, 1200.0, 240.0, '2024-04-15');
INSERT INTO patient_stats VALUES (2, 2, 3, 2, 2, 550.0, 70.0, '2024-05-01');
INSERT INTO patient_stats VALUES (3, 3, 3, 2, 2, 325.0, 65.0, '2024-05-10');
INSERT INTO patient_stats VALUES (4, 4, 3, 1, 2, 1375.0, 35.0, '2024-05-15');
INSERT INTO patient_stats VALUES (5, 5, 2, 1, 1, 150.0, 30.0, '2024-02-15');
INSERT INTO patient_stats VALUES (6, 6, 3, 2, 1, 8625.0, 850.0, '2024-06-10');
INSERT INTO patient_stats VALUES (7, 7, 2, 2, 1, 150.0, 30.0, '2024-03-10');
INSERT INTO patient_stats VALUES (8, 8, 3, 1, 1, 1250.0, 160.0, '2024-07-01');
INSERT INTO patient_stats VALUES (9, 9, 1, 1, 1, 1200.0, 240.0, '2024-03-20');
INSERT INTO patient_stats VALUES (10, 10, 1, 1, 1, 225.0, 0.0, '2024-04-01');
INSERT INTO patient_stats VALUES (11, 11, 1, 1, 1, 175.0, 35.0, '2024-04-10');
INSERT INTO patient_stats VALUES (12, 12, 1, 0, 0, 0.0, 0.0, '2024-07-10');

CREATE TABLE department_stats (
    id INTEGER PRIMARY KEY,
    department_id INTEGER NOT NULL UNIQUE REFERENCES departments(id),
    total_doctors INTEGER NOT NULL DEFAULT 0,
    total_nurses INTEGER NOT NULL DEFAULT 0,
    total_appointments INTEGER NOT NULL DEFAULT 0,
    total_revenue REAL NOT NULL DEFAULT 0.0
);

INSERT INTO department_stats VALUES (1, 1, 1, 1, 5, 1425.0);
INSERT INTO department_stats VALUES (2, 2, 1, 1, 5, 3700.0);
INSERT INTO department_stats VALUES (3, 3, 1, 1, 3, 375.0);
INSERT INTO department_stats VALUES (4, 4, 1, 1, 4, 850.0);
INSERT INTO department_stats VALUES (5, 5, 1, 1, 2, 325.0);
INSERT INTO department_stats VALUES (6, 6, 1, 1, 4, 8825.0);
INSERT INTO department_stats VALUES (7, 7, 1, 1, 2, 150.0);
INSERT INTO department_stats VALUES (8, 8, 1, 3, 0, 0.0);
"""
