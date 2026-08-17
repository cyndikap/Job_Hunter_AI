CREATE TABLE IF NOT EXISTS candidate_profile (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    target_title VARCHAR(255) NOT NULL,
    location_preference VARCHAR(255) DEFAULT 'Île-de-France',
    remote_preference VARCHAR(50) DEFAULT 'hybrid',
    contract_type VARCHAR(50) DEFAULT 'CDI',
    country VARCHAR(100) DEFAULT 'France',
    cv_summary TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS job_source (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    base_url TEXT,
    active BOOLEAN DEFAULT TRUE,
    priority_level INT DEFAULT 1
);

CREATE TABLE IF NOT EXISTS job_offer (
    id SERIAL PRIMARY KEY,
    source_id INT REFERENCES job_source(id),
    external_id VARCHAR(255),
    title VARCHAR(255) NOT NULL,
    company VARCHAR(255),
    location VARCHAR(255),
    contract_type VARCHAR(50),
    remote_mode VARCHAR(50),
    url TEXT,
    description TEXT,
    published_at TIMESTAMP,
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fingerprint VARCHAR(255),
    UNIQUE (source_id, external_id)
);

CREATE TABLE IF NOT EXISTS job_skill (
    id SERIAL PRIMARY KEY,
    job_offer_id INT REFERENCES job_offer(id) ON DELETE CASCADE,
    skill_name VARCHAR(255) NOT NULL,
    confidence NUMERIC(5,2) DEFAULT 0.0
);

CREATE TABLE IF NOT EXISTS job_match (
    id SERIAL PRIMARY KEY,
    job_offer_id INT REFERENCES job_offer(id) ON DELETE CASCADE,
    candidate_id INT REFERENCES candidate_profile(id),
    match_score INT NOT NULL,
    classification VARCHAR(50),
    summary TEXT,
    strengths TEXT,
    missing_skills TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    email_sent BOOLEAN DEFAULT FALSE,
    linkedin_sent BOOLEAN DEFAULT FALSE,
    url TEXT
);

CREATE TABLE IF NOT EXISTS email_log (
    id SERIAL PRIMARY KEY,
    job_offer_id INT REFERENCES job_offer(id),
    to_email VARCHAR(255) NOT NULL,
    subject VARCHAR(255),
    payload TEXT,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'sent'
);

CREATE TABLE IF NOT EXISTS application_tracking (
    id SERIAL PRIMARY KEY,
    job_offer_id INT REFERENCES job_offer(id),
    company VARCHAR(255),
    status VARCHAR(50) DEFAULT 'new',
    match_score INT,
    date_applied TIMESTAMP,
    contact_email VARCHAR(255),
    email_body TEXT,
    linkedin_message TEXT,
    cover_letter TEXT,
    notes TEXT
);

INSERT INTO candidate_profile (full_name, target_title, location_preference, remote_preference, contract_type, country)
VALUES ('Cynthia Sileu Kapnang', 'AI & Data Engineer', 'Île-de-France', 'partial_or_full_remote', 'CDI', 'France');

INSERT INTO job_source (name, base_url, active, priority_level)
VALUES
    ('LinkedIn Jobs', 'https://www.linkedin.com/jobs', TRUE, 1),
    ('Welcome to the Jungle', 'https://www.welcometothejungle.com', TRUE, 1),
    ('APEC', 'https://www.apec.fr', TRUE, 2),
    ('HelloWork', 'https://fr.hellowork.com', TRUE, 2),
    ('Indeed', 'https://fr.indeed.com', TRUE, 2),
    ('France Travail', 'https://www.francetravail.fr', TRUE, 2);
