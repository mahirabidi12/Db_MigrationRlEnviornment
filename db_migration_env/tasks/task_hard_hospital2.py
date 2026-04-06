"""Task (Hard): HealthFirst Clinic → MedCore Enterprise — Narrative Mode.

Same migration as task_hard_hospital, but the task description is a detailed narrative
instead of showing the target SQL. The agent must parse natural language to understand
what tables, columns, FKs, constraints, indexes, and data mappings to create.

Target schema is HIDDEN — the agent only sees the initial hc_ tables and the narrative.

Initial: 31 tables (hc_ prefix), ~350 rows
Target:  41 tables (no prefix), ~400 rows, 63 FKs, 48 indexes
"""

from db_migration_env.tasks.task_hard_hospital import INITIAL_SQL, TARGET_SQL

TASK_ID = "hard_hospital_narrative"

TASK_DESCRIPTION = """
HealthFirst Clinic → MedCore Enterprise Hospital Migration Specification
=========================================================================

HealthFirst Community Clinic, a small neighbourhood clinic that ran mostly on pen-and-paper,
was recently acquired by MedCore Enterprise Hospital System. Five years ago HealthFirst hired
a local developer who built a basic 31-table digital system — all prefixed with hc_, using
patient email addresses as references instead of foreign keys, a single monolithic hc_reports
table for every type of diagnostic report, zero indexes, and abbreviated column names.

MedCore requires a complete migration into their 41-table enterprise schema. Every legacy
table must be dropped. Every email reference must be resolved to a proper integer foreign key.
The monolithic hc_reports table must be split into six specialised report tables. All target
tables must have proper NOT NULL constraints, DEFAULT values, UNIQUE constraints where noted,
and indexes on lookup columns.

Below is the detailed specification for each of the 41 target tables.

────────────────────────────────────────────────────────────────
 Table  1 / 41 : patients
────────────────────────────────────────────────────────────────
The patients table replaces hc_patients as the core identity table, carrying 12 rows. Each row has an id INTEGER PRIMARY KEY mapped directly from hc_patients.pid. The first_name TEXT NOT NULL comes from pt_fname, last_name TEXT NOT NULL from pt_lname, email TEXT NOT NULL UNIQUE from pt_email, and phone TEXT (nullable) from pt_phone. The date_of_birth TEXT NOT NULL is mapped from pt_dob, gender TEXT NOT NULL from pt_gender, and blood_type TEXT (nullable) from pt_blood_type. The registered_at TEXT NOT NULL comes from pt_registered, and is_active INTEGER NOT NULL DEFAULT 1 from pt_is_active. Two indexes must be created: idx_patients_email on email, and idx_patients_name on (last_name, first_name).

────────────────────────────────────────────────────────────────
 Table  2 / 41 : patient_addresses
────────────────────────────────────────────────────────────────
The patient_addresses table extracts the address fields that were embedded directly in hc_patients into a separate normalised table with 12 rows — one per patient. Each row has an id INTEGER PRIMARY KEY and a patient_id INTEGER NOT NULL that references patients(id) as a foreign key, resolved by matching hc_patients.pid. The address_line TEXT NOT NULL comes from pt_addr_line, city TEXT NOT NULL from pt_addr_city, state TEXT NOT NULL from pt_addr_state, zip_code TEXT NOT NULL from pt_addr_zip. Every row gets address_type TEXT NOT NULL DEFAULT 'home' set to 'home'. Create index idx_patient_addresses_patient on patient_id.

────────────────────────────────────────────────────────────────
 Table  3 / 41 : emergency_contacts
────────────────────────────────────────────────────────────────
The emergency_contacts table migrates 8 rows from hc_patient_contacts. Each has id INTEGER PRIMARY KEY from pc_id, patient_id INTEGER NOT NULL FK→patients(id) resolved by joining pc_patient_email against patients.email, contact_name TEXT NOT NULL from pc_contact_name, relationship TEXT (nullable) from pc_relationship, phone TEXT NOT NULL from pc_phone, email TEXT (nullable) from pc_email, and is_primary INTEGER NOT NULL DEFAULT 1 from pc_is_primary. Create index idx_emergency_contacts_patient on patient_id.

────────────────────────────────────────────────────────────────
 Table  4 / 41 : insurance_policies
────────────────────────────────────────────────────────────────
The insurance_policies table migrates 12 rows from hc_insurance. Each has id INTEGER PRIMARY KEY from ins_id, patient_id INTEGER NOT NULL FK→patients(id) resolved by joining ins_patient_email against patients.email, provider TEXT NOT NULL from ins_provider, plan_name TEXT (nullable) from ins_plan, policy_number TEXT NOT NULL from ins_policy_no, group_number TEXT (nullable) from ins_group_no, start_date TEXT NOT NULL from ins_start_date, end_date TEXT (nullable) from ins_end_date, copay REAL NOT NULL DEFAULT 0.0 from ins_copay, and is_primary INTEGER NOT NULL DEFAULT 1 from ins_is_primary. Create index idx_insurance_patient on patient_id.

────────────────────────────────────────────────────────────────
 Table  5 / 41 : departments
────────────────────────────────────────────────────────────────
The departments table migrates 8 rows from hc_departments. Each has id INTEGER PRIMARY KEY from dept_id, name TEXT NOT NULL UNIQUE from dept_name, floor INTEGER NOT NULL from dept_floor, phone TEXT (nullable) from dept_phone, and created_at TEXT NOT NULL from dept_created. Note: the dept_head_email column from hc_departments is NOT migrated here — it moves to the separate department_heads junction table instead.

────────────────────────────────────────────────────────────────
 Table  6 / 41 : doctors
────────────────────────────────────────────────────────────────
The doctors table migrates 8 rows from hc_doctors. Each has id INTEGER PRIMARY KEY from did, first_name TEXT NOT NULL from doc_fname, last_name TEXT NOT NULL from doc_lname, email TEXT NOT NULL UNIQUE from doc_email, phone TEXT (nullable) from doc_phone, specialty TEXT NOT NULL from doc_specialty, license_number TEXT NOT NULL UNIQUE from doc_license_no, department_id INTEGER NOT NULL FK→departments(id) resolved by joining doc_dept_name against departments.name, hire_date TEXT NOT NULL from doc_hire_date, and is_active INTEGER NOT NULL DEFAULT 1 from doc_is_active. Create indexes: idx_doctors_email on email, idx_doctors_dept on department_id.

────────────────────────────────────────────────────────────────
 Table  7 / 41 : department_heads
────────────────────────────────────────────────────────────────
The department_heads table is a NEW junction table with 8 rows — one per department. Each has id INTEGER PRIMARY KEY, department_id INTEGER NOT NULL FK→departments(id), doctor_id INTEGER NOT NULL FK→doctors(id) resolved by joining hc_departments.dept_head_email against doctors.email, and appointed_date TEXT NOT NULL set to the doctor's hire_date. This table captures which doctor leads which department.

────────────────────────────────────────────────────────────────
 Table  8 / 41 : nurses
────────────────────────────────────────────────────────────────
The nurses table migrates 10 rows from hc_nurses. Each has id INTEGER PRIMARY KEY from nid, first_name TEXT NOT NULL from nur_fname, last_name TEXT NOT NULL from nur_lname, email TEXT NOT NULL UNIQUE from nur_email, phone TEXT (nullable) from nur_phone, department_id INTEGER NOT NULL FK→departments(id) resolved by joining nur_dept_name against departments.name, shift TEXT NOT NULL from nur_shift, certification TEXT NOT NULL from nur_certification, hire_date TEXT NOT NULL from nur_hire_date, and is_active INTEGER NOT NULL DEFAULT 1 from nur_is_active. Note: nurses 9 (Iris Carter) and 10 (Jake Davis) have nur_dept_name='Emergency' which does not exist in the departments table — these must map to department_id 8 (Internal Medicine) in the target. Create indexes: idx_nurses_email on email, idx_nurses_dept on department_id.

────────────────────────────────────────────────────────────────
 Table  9 / 41 : appointments
────────────────────────────────────────────────────────────────
The appointments table migrates 20 rows from hc_appointments. Each has id INTEGER PRIMARY KEY from aid, patient_id INTEGER NOT NULL FK→patients(id) resolved by joining appt_patient_email against patients.email, doctor_id INTEGER NOT NULL FK→doctors(id) resolved by joining appt_doctor_email against doctors.email, appointment_date TEXT NOT NULL from appt_date, appointment_time TEXT (nullable) from appt_time, appointment_type TEXT NOT NULL from appt_type, status TEXT NOT NULL DEFAULT 'scheduled' from appt_status, notes TEXT (nullable) from appt_notes, room TEXT (nullable) from appt_room, and created_at TEXT NOT NULL from appt_created. Create indexes: idx_appointments_patient on patient_id, idx_appointments_doctor on doctor_id, idx_appointments_date on appointment_date.

────────────────────────────────────────────────────────────────
 Table 10 / 41 : diagnoses
────────────────────────────────────────────────────────────────
The diagnoses table migrates 16 rows from hc_diagnoses. Each has id INTEGER PRIMARY KEY from diag_id, patient_id INTEGER NOT NULL FK→patients(id) resolved by joining diag_patient_email against patients.email, doctor_id INTEGER NOT NULL FK→doctors(id) resolved by joining diag_doctor_email against doctors.email, icd_code TEXT NOT NULL from diag_icd_code, name TEXT NOT NULL from diag_name, diagnosis_type TEXT NOT NULL DEFAULT 'primary' from diag_type, diagnosed_date TEXT NOT NULL from diag_date, status TEXT NOT NULL DEFAULT 'active' from diag_status, and notes TEXT (nullable) from diag_notes. Create indexes: idx_diagnoses_patient on patient_id, idx_diagnoses_icd on icd_code.

────────────────────────────────────────────────────────────────
 Table 11 / 41 : vital_signs
────────────────────────────────────────────────────────────────
The vital_signs table migrates 20 rows from hc_vitals. Each has id INTEGER PRIMARY KEY from vid, patient_id INTEGER NOT NULL FK→patients(id) resolved by joining vt_patient_email against patients.email, nurse_id INTEGER FK→nurses(id) (nullable) resolved by joining vt_nurse_email against nurses.email, recorded_date TEXT NOT NULL from vt_date, bp_systolic INTEGER (nullable) from vt_bp_systolic, bp_diastolic INTEGER (nullable) from vt_bp_diastolic, heart_rate INTEGER (nullable) from vt_heart_rate, temperature REAL (nullable) from vt_temperature, respiratory_rate INTEGER (nullable) from vt_respiratory_rate, o2_saturation REAL (nullable) from vt_o2_saturation, weight_kg REAL (nullable) from vt_weight_kg, height_cm REAL (nullable) from vt_height_cm, and notes TEXT (nullable) from vt_notes. Create indexes: idx_vitals_patient on patient_id, idx_vitals_date on recorded_date.

────────────────────────────────────────────────────────────────
 Table 12 / 41 : clinical_notes
────────────────────────────────────────────────────────────────
The clinical_notes table migrates 10 rows from hc_clinic_notes. Each has id INTEGER PRIMARY KEY from cn_id, patient_id INTEGER NOT NULL FK→patients(id) resolved by joining cn_patient_email against patients.email, doctor_id INTEGER NOT NULL FK→doctors(id) resolved by joining cn_doctor_email against doctors.email, note_date TEXT NOT NULL from cn_date, note_type TEXT NOT NULL DEFAULT 'progress' from cn_type, subjective TEXT (nullable) from cn_subjective, objective TEXT (nullable) from cn_objective, assessment TEXT (nullable) from cn_assessment, plan TEXT (nullable) from cn_plan, and is_signed INTEGER NOT NULL DEFAULT 0 from cn_is_signed. Create index idx_clinical_notes_patient on patient_id.

────────────────────────────────────────────────────────────────
 Table 13 / 41 : xray_reports
────────────────────────────────────────────────────────────────
The xray_reports table is one of six tables split from the monolithic hc_reports. It contains exactly 4 rows — only those from hc_reports WHERE rpt_type = 'xray'. Each row has id INTEGER PRIMARY KEY (renumbered 1-4), patient_id INTEGER NOT NULL FK→patients(id) resolved by joining rpt_patient_email against patients.email, doctor_id INTEGER NOT NULL FK→doctors(id) resolved by joining rpt_doctor_email against doctors.email, title TEXT NOT NULL from rpt_title, body_region TEXT NOT NULL from rpt_body_region, findings TEXT (nullable) from rpt_findings, conclusion TEXT (nullable) from rpt_conclusion, severity TEXT NOT NULL DEFAULT 'normal' from rpt_severity, file_url TEXT (nullable) from rpt_file_url, report_date TEXT NOT NULL from rpt_date, status TEXT NOT NULL DEFAULT 'final' from rpt_status, and notes TEXT (nullable) from rpt_notes. Create index idx_xray_patient on patient_id.

────────────────────────────────────────────────────────────────
 Table 14 / 41 : ct_scan_reports
────────────────────────────────────────────────────────────────
The ct_scan_reports table contains exactly 4 rows from hc_reports WHERE rpt_type = 'ct_scan'. Same column structure as xray_reports: id INTEGER PRIMARY KEY (renumbered 1-4), patient_id INTEGER NOT NULL FK→patients(id) via rpt_patient_email, doctor_id INTEGER NOT NULL FK→doctors(id) via rpt_doctor_email, title TEXT NOT NULL, body_region TEXT NOT NULL, findings TEXT, conclusion TEXT, severity TEXT NOT NULL DEFAULT 'normal', file_url TEXT, report_date TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'final', notes TEXT. Create index idx_ct_patient on patient_id.

────────────────────────────────────────────────────────────────
 Table 15 / 41 : mri_reports
────────────────────────────────────────────────────────────────
The mri_reports table contains exactly 4 rows from hc_reports WHERE rpt_type = 'mri'. Same column structure as xray_reports: id INTEGER PRIMARY KEY (renumbered 1-4), patient_id INTEGER NOT NULL FK→patients(id) via rpt_patient_email, doctor_id INTEGER NOT NULL FK→doctors(id) via rpt_doctor_email, title TEXT NOT NULL, body_region TEXT NOT NULL, findings TEXT, conclusion TEXT, severity TEXT NOT NULL DEFAULT 'normal', file_url TEXT, report_date TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'final', notes TEXT. Create index idx_mri_patient on patient_id.

────────────────────────────────────────────────────────────────
 Table 16 / 41 : lab_results
────────────────────────────────────────────────────────────────
The lab_results table contains exactly 4 rows from hc_reports WHERE rpt_type = 'lab'. Each has id INTEGER PRIMARY KEY (renumbered 1-4), patient_id INTEGER NOT NULL FK→patients(id) via rpt_patient_email, doctor_id INTEGER NOT NULL FK→doctors(id) via rpt_doctor_email, title TEXT NOT NULL, body_region TEXT NOT NULL DEFAULT 'blood' from rpt_body_region, findings TEXT, conclusion TEXT, severity TEXT NOT NULL DEFAULT 'normal', report_date TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'final', notes TEXT. Note: lab_results does NOT have a file_url column (unlike imaging reports). Create index idx_lab_patient on patient_id.

────────────────────────────────────────────────────────────────
 Table 17 / 41 : ultrasound_reports
────────────────────────────────────────────────────────────────
The ultrasound_reports table contains exactly 4 rows from hc_reports WHERE rpt_type = 'ultrasound'. Same column structure as xray_reports: id INTEGER PRIMARY KEY (renumbered 1-4), patient_id INTEGER NOT NULL FK→patients(id) via rpt_patient_email, doctor_id INTEGER NOT NULL FK→doctors(id) via rpt_doctor_email, title TEXT NOT NULL, body_region TEXT NOT NULL, findings TEXT, conclusion TEXT, severity TEXT NOT NULL DEFAULT 'normal', file_url TEXT, report_date TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'final', notes TEXT. Create index idx_ultrasound_patient on patient_id.

────────────────────────────────────────────────────────────────
 Table 18 / 41 : pathology_reports
────────────────────────────────────────────────────────────────
The pathology_reports table contains exactly 4 rows from hc_reports WHERE rpt_type = 'pathology'. Each has id INTEGER PRIMARY KEY (renumbered 1-4), patient_id INTEGER NOT NULL FK→patients(id) via rpt_patient_email, doctor_id INTEGER NOT NULL FK→doctors(id) via rpt_doctor_email, title TEXT NOT NULL, body_region TEXT NOT NULL, findings TEXT, conclusion TEXT, severity TEXT NOT NULL DEFAULT 'normal', report_date TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'final', notes TEXT. Note: pathology_reports does NOT have a file_url column. Create index idx_pathology_patient on patient_id.

────────────────────────────────────────────────────────────────
 Table 19 / 41 : medications
────────────────────────────────────────────────────────────────
The medications table migrates 10 rows from hc_medications PLUS 5 new rows for medications referenced in hc_prescriptions but missing from the catalog, totaling 15 rows. The original 10 rows: id INTEGER PRIMARY KEY from med_id, name TEXT NOT NULL UNIQUE from med_name, generic_name TEXT (nullable) from med_generic_name, category TEXT NOT NULL from med_category, form TEXT NOT NULL from med_form, manufacturer TEXT (nullable) from med_manufacturer, requires_prescription INTEGER NOT NULL DEFAULT 1 from med_requires_rx, is_controlled INTEGER NOT NULL DEFAULT 0 from med_is_controlled, and schedule TEXT (nullable) from med_schedule. The 5 additional medications that must be created (they appear in hc_prescriptions but not in hc_medications): id=11 'Vitamin D3' (generic 'Cholecalciferol', category 'Supplement', form 'Tablet', manufacturer 'Nature Made', requires_prescription=0, is_controlled=0), id=12 'Acetaminophen' (generic 'Acetaminophen', category 'Analgesic', form 'Tablet', manufacturer 'Tylenol', requires_prescription=0, is_controlled=0), id=13 'Naproxen' (generic 'Naproxen', category 'NSAID', form 'Tablet', manufacturer 'Aleve', requires_prescription=0, is_controlled=0), id=14 'Topiramate' (generic 'Topiramate', category 'Anticonvulsant', form 'Tablet', manufacturer 'Janssen', requires_prescription=1, is_controlled=0), id=15 'Glucosamine' (generic 'Glucosamine', category 'Supplement', form 'Tablet', manufacturer 'Schiff', requires_prescription=0, is_controlled=0).

────────────────────────────────────────────────────────────────
 Table 20 / 41 : prescriptions
────────────────────────────────────────────────────────────────
The prescriptions table migrates 15 rows from hc_prescriptions. Each has id INTEGER PRIMARY KEY from prid, patient_id INTEGER NOT NULL FK→patients(id) resolved by joining rx_patient_email against patients.email, doctor_id INTEGER NOT NULL FK→doctors(id) resolved by joining rx_doctor_email against doctors.email, medication_id INTEGER NOT NULL FK→medications(id) resolved by matching rx_medication against medications.name, dosage TEXT NOT NULL from rx_dosage, frequency TEXT (nullable) from rx_frequency, start_date TEXT NOT NULL from rx_start_date, end_date TEXT (nullable) from rx_end_date, refills INTEGER NOT NULL DEFAULT 0 from rx_refills, status TEXT NOT NULL DEFAULT 'active' from rx_status, pharmacy TEXT (nullable) from rx_pharmacy, and notes TEXT (nullable) from rx_notes. Important medication mappings: 'Vitamin D3'→medication_id 11, 'Acetaminophen'→12, 'Naproxen'→13, 'Topiramate'→14, 'Glucosamine'→15, and 'Hydrocortisone Cream' in the source matches 'Hydrocortisone' (medication_id 5) in the medications table. Create indexes: idx_prescriptions_patient on patient_id, idx_prescriptions_medication on medication_id.

────────────────────────────────────────────────────────────────
 Table 21 / 41 : surgeries
────────────────────────────────────────────────────────────────
The surgeries table migrates 6 rows from hc_surgeries. Each has id INTEGER PRIMARY KEY from surg_id, patient_id INTEGER NOT NULL FK→patients(id) resolved by joining surg_patient_email against patients.email, doctor_id INTEGER NOT NULL FK→doctors(id) resolved by joining surg_doctor_email against doctors.email, nurse_id INTEGER FK→nurses(id) (nullable) resolved by joining surg_nurse_email against nurses.email, surgery_type TEXT NOT NULL from surg_type, description TEXT (nullable) from surg_description, room TEXT (nullable) from surg_room, surgery_date TEXT NOT NULL from surg_date, start_time TEXT (nullable) from surg_start_time, end_time TEXT (nullable) from surg_end_time, outcome TEXT NOT NULL DEFAULT 'successful' from surg_outcome, complications TEXT (nullable) from surg_complications, and notes TEXT (nullable) from surg_notes. Create indexes: idx_surgeries_patient on patient_id, idx_surgeries_doctor on doctor_id.

────────────────────────────────────────────────────────────────
 Table 22 / 41 : procedures
────────────────────────────────────────────────────────────────
The procedures table migrates 8 rows from hc_procedures. Each has id INTEGER PRIMARY KEY from proc_id, patient_id INTEGER NOT NULL FK→patients(id) resolved by joining proc_patient_email against patients.email, doctor_id INTEGER NOT NULL FK→doctors(id) resolved by joining proc_doctor_email against doctors.email, nurse_id INTEGER FK→nurses(id) (nullable) resolved by joining proc_nurse_email against nurses.email, procedure_name TEXT NOT NULL from proc_name, procedure_type TEXT (nullable) from proc_type, room TEXT (nullable) from proc_room, procedure_date TEXT NOT NULL from proc_date, duration_minutes INTEGER (nullable) from proc_duration_min, outcome TEXT NOT NULL DEFAULT 'completed' from proc_outcome, and notes TEXT (nullable) from proc_notes. Create index idx_procedures_patient on patient_id.

────────────────────────────────────────────────────────────────
 Table 23 / 41 : allergies
────────────────────────────────────────────────────────────────
The allergies table migrates 10 rows from hc_allergies. Each has id INTEGER PRIMARY KEY from allergy_id, patient_id INTEGER NOT NULL FK→patients(id) resolved by joining alg_patient_email against patients.email, allergen TEXT NOT NULL from alg_allergen, reaction TEXT (nullable) from alg_reaction, severity TEXT NOT NULL DEFAULT 'moderate' from alg_severity, discovered_date TEXT (nullable) from alg_discovered_date, and notes TEXT (nullable) from alg_notes. Create index idx_allergies_patient on patient_id.

────────────────────────────────────────────────────────────────
 Table 24 / 41 : medical_history
────────────────────────────────────────────────────────────────
The medical_history table migrates 14 rows from hc_medical_history. Each has id INTEGER PRIMARY KEY from mh_id, patient_id INTEGER NOT NULL FK→patients(id) resolved by joining mh_patient_email against patients.email, condition TEXT NOT NULL from mh_condition, onset_date TEXT (nullable) from mh_onset_date, resolved_date TEXT (nullable) from mh_resolved_date, is_chronic INTEGER NOT NULL DEFAULT 0 from mh_is_chronic, and notes TEXT (nullable) from mh_notes. Create index idx_medical_history_patient on patient_id.

────────────────────────────────────────────────────────────────
 Table 25 / 41 : immunizations
────────────────────────────────────────────────────────────────
The immunizations table migrates 12 rows from hc_immunizations. Each has id INTEGER PRIMARY KEY from imm_id, patient_id INTEGER NOT NULL FK→patients(id) resolved by joining imm_patient_email against patients.email, vaccine TEXT NOT NULL from imm_vaccine, dose_number INTEGER NOT NULL DEFAULT 1 from imm_dose_number, administered_date TEXT NOT NULL from imm_date, administered_by_id INTEGER FK→nurses(id) (nullable) resolved by joining imm_administered_by against nurses.email, lot_number TEXT (nullable) from imm_lot_number, site TEXT (nullable) from imm_site, and notes TEXT (nullable) from imm_notes. Create index idx_immunizations_patient on patient_id.

────────────────────────────────────────────────────────────────
 Table 26 / 41 : lab_orders
────────────────────────────────────────────────────────────────
The lab_orders table migrates 12 rows from hc_lab_orders. Each has id INTEGER PRIMARY KEY from lo_id, patient_id INTEGER NOT NULL FK→patients(id) resolved by joining lo_patient_email against patients.email, doctor_id INTEGER NOT NULL FK→doctors(id) resolved by joining lo_doctor_email against doctors.email, test_name TEXT NOT NULL from lo_test_name, test_code TEXT (nullable) from lo_test_code, priority TEXT NOT NULL DEFAULT 'routine' from lo_priority, order_date TEXT NOT NULL from lo_order_date, status TEXT NOT NULL DEFAULT 'ordered' from lo_status, and notes TEXT (nullable) from lo_notes. Create index idx_lab_orders_patient on patient_id.

────────────────────────────────────────────────────────────────
 Table 27 / 41 : referrals
────────────────────────────────────────────────────────────────
The referrals table migrates 8 rows from hc_referrals. Each has id INTEGER PRIMARY KEY from ref_id, patient_id INTEGER NOT NULL FK→patients(id) resolved by joining ref_patient_email against patients.email, from_doctor_id INTEGER NOT NULL FK→doctors(id) resolved by joining ref_from_doctor_email against doctors.email, to_doctor_id INTEGER NOT NULL FK→doctors(id) resolved by joining ref_to_doctor_email against doctors.email, reason TEXT NOT NULL from ref_reason, priority TEXT NOT NULL DEFAULT 'routine' from ref_priority, referral_date TEXT NOT NULL from ref_date, status TEXT NOT NULL DEFAULT 'pending' from ref_status, and notes TEXT (nullable) from ref_notes. Create index idx_referrals_patient on patient_id.

────────────────────────────────────────────────────────────────
 Table 28 / 41 : billing
────────────────────────────────────────────────────────────────
The billing table migrates 18 rows from hc_billing. Each has id INTEGER PRIMARY KEY from bill_id, patient_id INTEGER NOT NULL FK→patients(id) resolved by joining bill_patient_email against patients.email, doctor_id INTEGER FK→doctors(id) (nullable) resolved by joining bill_doctor_email against doctors.email, service_description TEXT NOT NULL from bill_service, total_amount REAL NOT NULL from bill_amount, insurance_covered REAL NOT NULL DEFAULT 0.0 from bill_insurance_covered, patient_responsibility REAL NOT NULL from bill_patient_owes, billing_date TEXT NOT NULL from bill_date, due_date TEXT (nullable) from bill_due_date, status TEXT NOT NULL DEFAULT 'pending' from bill_status, and notes TEXT (nullable) from bill_notes. Create indexes: idx_billing_patient on patient_id, idx_billing_status on status.

────────────────────────────────────────────────────────────────
 Table 29 / 41 : payments
────────────────────────────────────────────────────────────────
The payments table migrates 12 rows from hc_payments. Each has id INTEGER PRIMARY KEY from pay_id, patient_id INTEGER NOT NULL FK→patients(id) resolved by joining pay_patient_email against patients.email, billing_id INTEGER NOT NULL FK→billing(id) from pay_bill_id, amount REAL NOT NULL from pay_amount, payment_method TEXT NOT NULL DEFAULT 'insurance' from pay_method, payment_date TEXT NOT NULL from pay_date, reference_number TEXT (nullable) from pay_reference, status TEXT NOT NULL DEFAULT 'completed' from pay_status, and notes TEXT (nullable) from pay_notes. Create indexes: idx_payments_patient on patient_id, idx_payments_billing on billing_id.

────────────────────────────────────────────────────────────────
 Table 30 / 41 : rooms
────────────────────────────────────────────────────────────────
The rooms table migrates 10 rows from hc_rooms. Each has id INTEGER PRIMARY KEY from room_id, room_number TEXT NOT NULL UNIQUE from room_number, floor INTEGER NOT NULL from room_floor, room_type TEXT NOT NULL from room_type, department_id INTEGER NOT NULL FK→departments(id) resolved by joining room_dept_name against departments.name, capacity INTEGER NOT NULL DEFAULT 1 from room_capacity, equipment TEXT (nullable) from room_equipment, and is_active INTEGER NOT NULL DEFAULT 1 from room_is_active. Create index idx_rooms_dept on department_id.

────────────────────────────────────────────────────────────────
 Table 31 / 41 : wards
────────────────────────────────────────────────────────────────
The wards table is a NEW normalised table with 5 rows, derived from the DISTINCT ward names in hc_ward_beds. Each has id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE from bed_ward, floor INTEGER NOT NULL from bed_floor (use the floor of the first bed in each ward), ward_type TEXT NOT NULL mapped from the ward name ('General Ward'→'general', 'ICU'→'icu', 'Maternity'→'maternity', 'Surgical'→'post-op', 'Pediatric'→'pediatric'), and total_beds INTEGER NOT NULL DEFAULT 0 set to the count of beds in hc_ward_beds for that ward.

────────────────────────────────────────────────────────────────
 Table 32 / 41 : beds
────────────────────────────────────────────────────────────────
The beds table migrates 10 rows from hc_ward_beds. Each has id INTEGER PRIMARY KEY from bed_id, ward_id INTEGER NOT NULL FK→wards(id) resolved by joining bed_ward against wards.name, bed_number TEXT NOT NULL from bed_number, bed_type TEXT NOT NULL DEFAULT 'standard' from bed_type, is_occupied INTEGER NOT NULL DEFAULT 0 from bed_is_occupied, patient_id INTEGER FK→patients(id) (nullable) resolved by joining bed_patient_email against patients.email (NULL if bed is unoccupied), admit_date TEXT (nullable) from bed_admit_date, and notes TEXT (nullable) from bed_notes. Create indexes: idx_beds_ward on ward_id, idx_beds_patient on patient_id.

────────────────────────────────────────────────────────────────
 Table 33 / 41 : equipment
────────────────────────────────────────────────────────────────
The equipment table migrates 8 rows from hc_equipment. Each has id INTEGER PRIMARY KEY from eq_id, name TEXT NOT NULL from eq_name, equipment_type TEXT NOT NULL from eq_type, serial_number TEXT UNIQUE (nullable) from eq_serial_no, department_id INTEGER NOT NULL FK→departments(id) resolved by joining eq_dept_name against departments.name, room TEXT (nullable) from eq_room, purchase_date TEXT (nullable) from eq_purchase_date, last_service_date TEXT (nullable) from eq_last_service, next_service_date TEXT (nullable) from eq_next_service, status TEXT NOT NULL DEFAULT 'operational' from eq_status, and notes TEXT (nullable) from eq_notes. Create index idx_equipment_dept on department_id.

────────────────────────────────────────────────────────────────
 Table 34 / 41 : pharmacy_inventory
────────────────────────────────────────────────────────────────
The pharmacy_inventory table migrates 10 rows from hc_pharmacy_inventory. Each has id INTEGER PRIMARY KEY from inv_id, medication_id INTEGER NOT NULL FK→medications(id) resolved by matching inv_medication_name against medications.name, dosage TEXT NOT NULL from inv_dosage, form TEXT NOT NULL from inv_form, quantity INTEGER NOT NULL from inv_quantity, unit TEXT NOT NULL DEFAULT 'tablets' from inv_unit, batch_number TEXT (nullable) from inv_batch_no, expiry_date TEXT NOT NULL from inv_expiry_date, reorder_level INTEGER NOT NULL DEFAULT 50 from inv_reorder_level, supplier TEXT (nullable) from inv_supplier, and last_restocked TEXT (nullable) from inv_last_restocked. Create index idx_pharmacy_medication on medication_id.

────────────────────────────────────────────────────────────────
 Table 35 / 41 : staff_shifts
────────────────────────────────────────────────────────────────
The staff_shifts table migrates 10 rows from hc_shifts. Each has id INTEGER PRIMARY KEY from shift_id, staff_email TEXT NOT NULL from shft_staff_email, staff_role TEXT NOT NULL from shft_staff_role, department_id INTEGER NOT NULL FK→departments(id) resolved by joining shft_dept_name against departments.name, shift_date TEXT NOT NULL from shft_date, start_time TEXT NOT NULL from shft_start, end_time TEXT NOT NULL from shft_end, shift_type TEXT NOT NULL DEFAULT 'regular' from shft_type, and notes TEXT (nullable) from shft_notes. Note: row 8 has shft_dept_name='Emergency' which does not exist in departments — map it to department_id 8 (Internal Medicine), same as the nurses mapping. Create index idx_shifts_date on shift_date.

────────────────────────────────────────────────────────────────
 Table 36 / 41 : consent_forms
────────────────────────────────────────────────────────────────
The consent_forms table migrates 8 rows from hc_consent_forms. Each has id INTEGER PRIMARY KEY from cf_id, patient_id INTEGER NOT NULL FK→patients(id) resolved by joining cf_patient_email against patients.email, procedure_name TEXT NOT NULL from cf_procedure, doctor_id INTEGER NOT NULL FK→doctors(id) resolved by joining cf_doctor_email against doctors.email, signed_date TEXT NOT NULL from cf_signed_date, witness TEXT (nullable) from cf_witness, form_type TEXT NOT NULL DEFAULT 'procedure' from cf_form_type, status TEXT NOT NULL DEFAULT 'signed' from cf_status, and notes TEXT (nullable) from cf_notes. Create index idx_consent_patient on patient_id.

────────────────────────────────────────────────────────────────
 Table 37 / 41 : follow_ups
────────────────────────────────────────────────────────────────
The follow_ups table migrates 10 rows from hc_follow_ups. Each has id INTEGER PRIMARY KEY from fu_id, patient_id INTEGER NOT NULL FK→patients(id) resolved by joining fu_patient_email against patients.email, doctor_id INTEGER NOT NULL FK→doctors(id) resolved by joining fu_doctor_email against doctors.email, original_visit_date TEXT (nullable) from fu_original_visit_date, scheduled_date TEXT NOT NULL from fu_scheduled_date, reason TEXT (nullable) from fu_reason, status TEXT NOT NULL DEFAULT 'scheduled' from fu_status, and notes TEXT (nullable) from fu_notes. Create index idx_followups_patient on patient_id.

────────────────────────────────────────────────────────────────
 Table 38 / 41 : waiting_list
────────────────────────────────────────────────────────────────
The waiting_list table migrates 6 rows from hc_waiting_list. Each has id INTEGER PRIMARY KEY from wl_id, patient_id INTEGER NOT NULL FK→patients(id) resolved by joining wl_patient_email against patients.email, doctor_id INTEGER NOT NULL FK→doctors(id) resolved by joining wl_doctor_email against doctors.email, procedure_name TEXT NOT NULL from wl_procedure, priority TEXT NOT NULL DEFAULT 'routine' from wl_priority, added_date TEXT NOT NULL from wl_added_date, target_date TEXT (nullable) from wl_target_date, status TEXT NOT NULL DEFAULT 'waiting' from wl_status, and notes TEXT (nullable) from wl_notes. Create index idx_waiting_patient on patient_id.

────────────────────────────────────────────────────────────────
 Table 39 / 41 : audit_log
────────────────────────────────────────────────────────────────
The audit_log table migrates 10 rows from hc_audit_log. Each has id INTEGER PRIMARY KEY from log_id, user_email TEXT NOT NULL from log_user_email, action TEXT NOT NULL from log_action, table_name TEXT (nullable) from log_table_name — but NOTE: the table_name values must be updated to reflect the NEW target table names: 'hc_prescriptions'→'prescriptions', 'hc_vitals'→'vital_signs', 'hc_surgeries'→'surgeries', 'hc_patients'→'patients', 'hc_diagnoses'→'diagnoses'. For 'hc_reports' entries: look up the original hc_reports.rid by the log_record_id to determine the rpt_type, then map to the correct specialised table name ('xray_reports', 'mri_reports', 'pathology_reports', etc.). The record_id INTEGER (nullable) must also be updated for split report tables — since the specialised tables renumber their IDs starting from 1, the record_id must point to the new row number within that specialised table (e.g., hc_reports rid=9 was the 1st MRI report, so record_id becomes 1 in mri_reports; hc_reports rid=22 was the 2nd pathology report, so record_id becomes 2). The timestamp TEXT NOT NULL from log_timestamp, ip_address TEXT (nullable) from log_ip_address, and details TEXT (nullable) from log_details. Create index idx_audit_timestamp on timestamp.

────────────────────────────────────────────────────────────────
 Table 40 / 41 : patient_stats
────────────────────────────────────────────────────────────────
The patient_stats table is a COMPUTED summary table with 12 rows — one per patient. Each has id INTEGER PRIMARY KEY, patient_id INTEGER NOT NULL UNIQUE FK→patients(id), total_appointments INTEGER NOT NULL DEFAULT 0 computed as COUNT of ALL appointments for this patient (including cancelled and scheduled, not just completed), total_diagnoses INTEGER NOT NULL DEFAULT 0 computed as COUNT of diagnoses for this patient, total_prescriptions INTEGER NOT NULL DEFAULT 0 computed as COUNT of prescriptions for this patient, total_billing REAL NOT NULL DEFAULT 0.0 computed as SUM of billing.total_amount for ALL billing records for this patient (regardless of billing status — include pending, paid, all), total_paid REAL NOT NULL DEFAULT 0.0 computed as SUM of payments.amount for this patient, and last_visit_date TEXT (nullable) set to the MAX appointment_date from appointments WHERE status IN ('completed', 'scheduled') for this patient (i.e., the latest appointment date regardless of status, but NULL if patient has no appointments). Create index idx_patient_stats_patient on patient_id.

────────────────────────────────────────────────────────────────
 Table 41 / 41 : department_stats
────────────────────────────────────────────────────────────────
The department_stats table is a COMPUTED summary table with 8 rows — one per department. Each has id INTEGER PRIMARY KEY, department_id INTEGER NOT NULL UNIQUE FK→departments(id), total_doctors INTEGER NOT NULL DEFAULT 0 computed as COUNT of doctors in this department, total_nurses INTEGER NOT NULL DEFAULT 0 computed as COUNT of nurses in this department, total_appointments INTEGER NOT NULL DEFAULT 0 computed as COUNT of appointments where the doctor belongs to this department, and total_revenue REAL NOT NULL DEFAULT 0.0 computed as SUM of billing.total_amount where the billing's doctor belongs to this department.

────────────────────────────────────────────────────────────────
 FINAL STEP: DROP ALL LEGACY TABLES
────────────────────────────────────────────────────────────────
After all 41 target tables are fully populated with correct data, every one of the 31 original hc_ tables must be dropped: hc_patients, hc_doctors, hc_nurses, hc_departments, hc_appointments, hc_reports, hc_prescriptions, hc_diagnoses, hc_vitals, hc_insurance, hc_billing, hc_rooms, hc_surgeries, hc_allergies, hc_lab_orders, hc_referrals, hc_medications, hc_patient_contacts, hc_medical_history, hc_immunizations, hc_ward_beds, hc_shifts, hc_consent_forms, hc_follow_ups, hc_clinic_notes, hc_procedures, hc_equipment, hc_pharmacy_inventory, hc_audit_log, hc_waiting_list, hc_payments.
"""

DIFFICULTY = "hard"
TIMEOUT_SECONDS = 1800  # 30 minutes
