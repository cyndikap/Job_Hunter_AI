-- Schema PostgreSQL pour Job Hunter AI

CREATE TABLE candidate_profile (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    target_contract VARCHAR(50) NOT NULL,
    preferred_country VARCHAR(100) NOT NULL,
    preferred_location VARCHAR(255) NOT NULL,
    remote_preference VARCHAR(50) NOT NULL,
    cv_text TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE skill_catalog (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    category VARCHAR(100) NOT NULL,
    weight NUMERIC(5,2) DEFAULT 1.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE job_source (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    url VARCHAR(500),
    source_type VARCHAR(100) NOT NULL,
    active BOOLEAN DEFAULT TRUE,
    reliability_score NUMERIC(5,2) DEFAULT 0.0
);

CREATE TABLE job_offer (
    id SERIAL PRIMARY KEY,
    source_id INT REFERENCES job_source(id),
    external_id VARCHAR(255),
    title VARCHAR(255) NOT NULL,
    company VARCHAR(255),
    location VARCHAR(255),
    employment_type VARCHAR(100),
    remote_mode VARCHAR(50),
    salary VARCHAR(255),
    description TEXT,
    url TEXT,
    published_at TIMESTAMP,
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'new',
    UNIQUE (source_id, external_id)
);

CREATE TABLE job_skill (
    id SERIAL PRIMARY KEY,
    job_offer_id INT REFERENCES job_offer(id) ON DELETE CASCADE,
    skill_name VARCHAR(255) NOT NULL,
    confidence NUMERIC(5,2) DEFAULT 0.0,
    detected_by VARCHAR(50) DEFAULT 'heuristic'
);

CREATE TABLE matching_result (
    id SERIAL PRIMARY KEY,
    job_offer_id INT REFERENCES job_offer(id) ON DELETE CASCADE,
    profile_id INT REFERENCES candidate_profile(id),
    overall_score NUMERIC(5,2) NOT NULL,
    title_match NUMERIC(5,2) DEFAULT 0,
    skills_match NUMERIC(5,2) DEFAULT 0,
    experience_match NUMERIC(5,2) DEFAULT 0,
    location_match NUMERIC(5,2) DEFAULT 0,
    company_priority NUMERIC(5,2) DEFAULT 0,
    classification VARCHAR(50) NOT NULL,
    summary TEXT,
    strengths TEXT,
    missing_skills TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE alert_event (
    id SERIAL PRIMARY KEY,
    job_offer_id INT REFERENCES job_offer(id),
    matching_result_id INT REFERENCES matching_result(id),
    channel VARCHAR(50) NOT NULL,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'queued',
    payload JSONB
);

CREATE TABLE application_track (
    id SERIAL PRIMARY KEY,
    job_offer_id INT REFERENCES job_offer(id),
    company VARCHAR(255),
    status VARCHAR(50) DEFAULT 'new',
    score NUMERIC(5,2),
    date_applied TIMESTAMP,
    contact_name VARCHAR(255),
    recruiter_message TEXT,
    email_body TEXT,
    linkedin_message TEXT,
    cover_letter TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE notification_channel (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    config JSONB,
    active BOOLEAN DEFAULT TRUE
);

CREATE INDEX idx_job_offer_status ON job_offer(status);
CREATE INDEX idx_matching_score ON matching_result(overall_score);
CREATE INDEX idx_job_offer_company ON job_offer(company);
CREATE INDEX idx_job_offer_published_at ON job_offer(published_at);
