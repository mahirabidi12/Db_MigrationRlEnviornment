TASK_ID = "easy_hospital_migration"
DIFFICULTY = "easy"
TIMEOUT_SECONDS = 86400
MAX_STEPS = 12

TASK_DESCRIPTION = """
HealthFirst Clinic → MedCore Enterprise Hospital Migration
============================================================

HealthFirst Community Clinic has 4 legacy tables (hc_ prefix, email refs, zero FKs).
Migrate into 6 enterprise tables. Split hc_reports into xray_reports and lab_results.
Drop all 4 legacy tables after migration.

────────────────────────────────────────────────────────────────
 Table 1 / 6 : patients
────────────────────────────────────────────────────────────────
3 rows from hc_patients. id INTEGER PRIMARY KEY from pid, first_name TEXT NOT NULL from pt_fname, last_name TEXT NOT NULL from pt_lname, email TEXT NOT NULL UNIQUE from pt_email, date_of_birth TEXT NOT NULL from pt_dob, is_active INTEGER NOT NULL DEFAULT 1 from pt_is_active.

────────────────────────────────────────────────────────────────
 Table 2 / 6 : patient_addresses
────────────────────────────────────────────────────────────────
3 rows extracted from hc_patients. id INTEGER PRIMARY KEY, patient_id INTEGER NOT NULL FK→patients(id) (same as pid), address_line TEXT NOT NULL from pt_addr_line, city TEXT NOT NULL from pt_addr_city, state TEXT NOT NULL from pt_addr_state.

────────────────────────────────────────────────────────────────
 Table 3 / 6 : doctors
────────────────────────────────────────────────────────────────
2 rows from hc_doctors. id INTEGER PRIMARY KEY from did, first_name TEXT NOT NULL from doc_fname, last_name TEXT NOT NULL from doc_lname, email TEXT NOT NULL UNIQUE from doc_email, is_active INTEGER NOT NULL DEFAULT 1 from doc_is_active.

────────────────────────────────────────────────────────────────
 Table 4 / 6 : appointments
────────────────────────────────────────────────────────────────
4 rows from hc_appointments. id INTEGER PRIMARY KEY from aid, patient_id INTEGER NOT NULL FK→patients(id) resolved by joining appt_patient_email against patients.email, doctor_id INTEGER NOT NULL FK→doctors(id) resolved by joining appt_doctor_email against doctors.email, appointment_date TEXT NOT NULL from appt_date, status TEXT NOT NULL DEFAULT 'scheduled' from appt_status.

────────────────────────────────────────────────────────────────
 Table 5 / 6 : xray_reports
────────────────────────────────────────────────────────────────
2 rows from hc_reports WHERE rpt_type = 'xray'. id INTEGER PRIMARY KEY (renumbered 1-2), patient_id INTEGER NOT NULL FK→patients(id) via rpt_patient_email, doctor_id INTEGER NOT NULL FK→doctors(id) via rpt_doctor_email, title TEXT NOT NULL from rpt_title, report_date TEXT NOT NULL from rpt_date, severity TEXT NOT NULL DEFAULT 'normal' from rpt_severity.

────────────────────────────────────────────────────────────────
 Table 6 / 6 : lab_results
────────────────────────────────────────────────────────────────
2 rows from hc_reports WHERE rpt_type = 'lab'. Same structure as xray_reports: id INTEGER PRIMARY KEY (renumbered 1-2), patient_id INTEGER NOT NULL FK→patients(id) via rpt_patient_email, doctor_id INTEGER NOT NULL FK→doctors(id) via rpt_doctor_email, title TEXT NOT NULL, report_date TEXT NOT NULL, severity TEXT NOT NULL DEFAULT 'normal'.

────────────────────────────────────────────────────────────────
 DROP ALL LEGACY TABLES: hc_patients, hc_doctors, hc_appointments, hc_reports.
"""

INITIAL_SQL = """
CREATE TABLE hc_patients (
    pid INTEGER PRIMARY KEY,
    pt_fname TEXT NOT NULL,
    pt_lname TEXT NOT NULL,
    pt_email TEXT NOT NULL,
    pt_dob TEXT,
    pt_addr_line TEXT,
    pt_addr_city TEXT,
    pt_addr_state TEXT,
    pt_is_active INTEGER DEFAULT 1
);

INSERT INTO hc_patients VALUES (1, 'Alice', 'Chen', 'alice@email.com', '1990-03-15', '123 Maple St', 'Portland', 'OR', 1);
INSERT INTO hc_patients VALUES (2, 'Bob', 'Rivera', 'bob@email.com', '1985-07-22', '456 Oak Ave', 'Austin', 'TX', 1);
INSERT INTO hc_patients VALUES (3, 'Carol', 'Zhang', 'carol@email.com', '1992-11-08', '789 Pine Rd', 'Seattle', 'WA', 1);

CREATE TABLE hc_doctors (
    did INTEGER PRIMARY KEY,
    doc_fname TEXT NOT NULL,
    doc_lname TEXT NOT NULL,
    doc_email TEXT NOT NULL,
    doc_is_active INTEGER DEFAULT 1
);

INSERT INTO hc_doctors VALUES (1, 'Sarah', 'Williams', 'dr.williams@hf.com', 1);
INSERT INTO hc_doctors VALUES (2, 'Michael', 'Lee', 'dr.lee@hf.com', 1);

CREATE TABLE hc_appointments (
    aid INTEGER PRIMARY KEY,
    appt_patient_email TEXT NOT NULL,
    appt_doctor_email TEXT NOT NULL,
    appt_date TEXT NOT NULL,
    appt_status TEXT DEFAULT 'scheduled'
);

INSERT INTO hc_appointments VALUES (1, 'alice@email.com', 'dr.williams@hf.com', '2024-01-15', 'completed');
INSERT INTO hc_appointments VALUES (2, 'bob@email.com', 'dr.lee@hf.com', '2024-01-20', 'completed');
INSERT INTO hc_appointments VALUES (3, 'carol@email.com', 'dr.williams@hf.com', '2024-02-05', 'completed');
INSERT INTO hc_appointments VALUES (4, 'alice@email.com', 'dr.lee@hf.com', '2024-03-10', 'scheduled');

CREATE TABLE hc_reports (
    rid INTEGER PRIMARY KEY,
    rpt_patient_email TEXT NOT NULL,
    rpt_doctor_email TEXT NOT NULL,
    rpt_type TEXT NOT NULL,
    rpt_title TEXT NOT NULL,
    rpt_date TEXT NOT NULL,
    rpt_severity TEXT DEFAULT 'normal'
);

INSERT INTO hc_reports VALUES (1, 'alice@email.com', 'dr.lee@hf.com', 'xray', 'Chest X-Ray', '2024-01-15', 'normal');
INSERT INTO hc_reports VALUES (2, 'bob@email.com', 'dr.lee@hf.com', 'xray', 'Knee X-Ray', '2024-01-20', 'mild');
INSERT INTO hc_reports VALUES (3, 'alice@email.com', 'dr.williams@hf.com', 'lab', 'Blood Count', '2024-01-15', 'normal');
INSERT INTO hc_reports VALUES (4, 'carol@email.com', 'dr.williams@hf.com', 'lab', 'Lipid Panel', '2024-02-05', 'moderate');
"""

TARGET_SQL = """
CREATE TABLE patients (
    id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    date_of_birth TEXT NOT NULL,
    is_active INTEGER NOT NULL DEFAULT 1
);

INSERT INTO patients VALUES (1, 'Alice', 'Chen', 'alice@email.com', '1990-03-15', 1);
INSERT INTO patients VALUES (2, 'Bob', 'Rivera', 'bob@email.com', '1985-07-22', 1);
INSERT INTO patients VALUES (3, 'Carol', 'Zhang', 'carol@email.com', '1992-11-08', 1);

CREATE TABLE patient_addresses (
    id INTEGER PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id),
    address_line TEXT NOT NULL,
    city TEXT NOT NULL,
    state TEXT NOT NULL
);

INSERT INTO patient_addresses VALUES (1, 1, '123 Maple St', 'Portland', 'OR');
INSERT INTO patient_addresses VALUES (2, 2, '456 Oak Ave', 'Austin', 'TX');
INSERT INTO patient_addresses VALUES (3, 3, '789 Pine Rd', 'Seattle', 'WA');

CREATE TABLE doctors (
    id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    is_active INTEGER NOT NULL DEFAULT 1
);

INSERT INTO doctors VALUES (1, 'Sarah', 'Williams', 'dr.williams@hf.com', 1);
INSERT INTO doctors VALUES (2, 'Michael', 'Lee', 'dr.lee@hf.com', 1);

CREATE TABLE appointments (
    id INTEGER PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id),
    doctor_id INTEGER NOT NULL REFERENCES doctors(id),
    appointment_date TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'scheduled'
);

INSERT INTO appointments VALUES (1, 1, 1, '2024-01-15', 'completed');
INSERT INTO appointments VALUES (2, 2, 2, '2024-01-20', 'completed');
INSERT INTO appointments VALUES (3, 3, 1, '2024-02-05', 'completed');
INSERT INTO appointments VALUES (4, 1, 2, '2024-03-10', 'scheduled');

CREATE TABLE xray_reports (
    id INTEGER PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id),
    doctor_id INTEGER NOT NULL REFERENCES doctors(id),
    title TEXT NOT NULL,
    report_date TEXT NOT NULL,
    severity TEXT NOT NULL DEFAULT 'normal'
);

INSERT INTO xray_reports VALUES (1, 1, 2, 'Chest X-Ray', '2024-01-15', 'normal');
INSERT INTO xray_reports VALUES (2, 2, 2, 'Knee X-Ray', '2024-01-20', 'mild');

CREATE TABLE lab_results (
    id INTEGER PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id),
    doctor_id INTEGER NOT NULL REFERENCES doctors(id),
    title TEXT NOT NULL,
    report_date TEXT NOT NULL,
    severity TEXT NOT NULL DEFAULT 'normal'
);

INSERT INTO lab_results VALUES (1, 1, 1, 'Blood Count', '2024-01-15', 'normal');
INSERT INTO lab_results VALUES (2, 3, 1, 'Lipid Panel', '2024-02-05', 'moderate');
"""
