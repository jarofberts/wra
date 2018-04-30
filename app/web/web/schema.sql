create table if not exists people (
  id integer primary key autoincrement,
  first_name text NOT NULL,
  middle_name text,
  last_name text NOT NULL,
  street_address text NOT NULL,
  city text NOT NULL,
  state text NOT NULL,
  zip_code text NOT NULL,
  phone text,
  voicemail_ok integer,
  email text,
  contact_preference integer,
  birthday_month integer,
  birthday_day_of_month integer,
  emergency_contact_name text NOT NULL,
  emergency_contact_phone text NOT NULL,
  emergency_contact_relationship text,
  highest_education text,
  currently_attending_school integer,
  user_id integer
);

create table if not exists languages (
  id integer primary key autoincrement,
  name text NOT NULL
);

create table if not exists languages_known (
  person_id integer not null,
  language_id integer not null,
  primary key(person_id, language_id)
);

create table if not exists users (
  id integer primary key autoincrement,
  user_name text NOT NULL UNIQUE,
  password text NOT NULL
);

create table if not exists volunteers (
  id integer NOT NULL UNIQUE,
  currently_employed integer not null,
  has_resume integer not null,
  medical_insurance_provider text NOT NULL,
  health_factors text NOT NULL,
  inventory integer NOT null,
  research integer not null,
  outreach integer not null,
  marketing integer not null,
  reception_scheduling integer not null,
  speakers integer not null,
  maintenance integer not null,
  other_details text,
  advocate integer not null,
  computer integer not null,
  resumes_mock_interview integer not null,
  image_consultant integer not null,
  dbase integer not null,
  felon integer not null,
  felon_incident_date text,
  felon_file_date text,
  felon_nature text,
  felon_incident_loc text,
  felon_file_lo text,
  felon_dispos text,
  emp_term integer not null,
  emp_term_incident_date text,
  emp_term_file_date text,
  emp_term_nature text,
  emp_term_incident_loc text,
  emp_term_file_loc text,
  emp_term_dispos text,
  emp_term_employer text,
  emp_term_city text,
  emp_term_state text,
  name_appl_decl_auth_release text,
  date_appl_decl_auth_release text,
  name_confidentiality_agree text,
  date_confidentiality_agree text,
  name_informed_consent text,
  date_informed_consent text
);

create table if not exists time_slots (
  id integer NOT NULL UNIQUE,
  day_of_week text NOT NULL,
  start_time text NOT NULL,
  end_time text NOT NULL
);

create table if not exists volunteer_availability (
  volunteer_id integer NOT NULL,
  time_slot_id integer NOT NULL,
  primary key(volunteer_id, time_slot_id)
)