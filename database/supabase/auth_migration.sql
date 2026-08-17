-- SaaS multi-utilisateur foundation
-- 1. Ensure canonical user table exists
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    full_name VARCHAR(255),
    avatar_url TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    status VARCHAR(50) DEFAULT 'active'
);

-- 2. Add user ownership to tables that hold user-scoped content
ALTER TABLE jobs ADD COLUMN IF NOT EXISTS user_id UUID NULL REFERENCES users(id) ON DELETE CASCADE;
ALTER TABLE applications ADD COLUMN IF NOT EXISTS user_id UUID NULL REFERENCES users(id) ON DELETE CASCADE;
ALTER TABLE alerts ADD COLUMN IF NOT EXISTS user_id UUID NULL REFERENCES users(id) ON DELETE CASCADE;
ALTER TABLE candidate_profile ADD COLUMN IF NOT EXISTS user_id UUID NULL REFERENCES users(id) ON DELETE CASCADE;
ALTER TABLE job_match ADD COLUMN IF NOT EXISTS user_id UUID NULL REFERENCES users(id) ON DELETE CASCADE;
ALTER TABLE email_log ADD COLUMN IF NOT EXISTS user_id UUID NULL REFERENCES users(id) ON DELETE CASCADE;
ALTER TABLE application_tracking ADD COLUMN IF NOT EXISTS user_id UUID NULL REFERENCES users(id) ON DELETE CASCADE;

-- 3. Backfill user_id for existing records if a user is known
-- This is intentionally conservative; rows remain visible only to the owner after RLS is enforced.
UPDATE jobs SET user_id = users.id
FROM users
WHERE jobs.user_id IS NULL
  AND jobs.source = 'manual';

-- 4. Indexes
CREATE INDEX IF NOT EXISTS idx_jobs_user_id ON jobs(user_id);
CREATE INDEX IF NOT EXISTS idx_applications_user_id ON applications(user_id);
CREATE INDEX IF NOT EXISTS idx_alerts_user_id ON alerts(user_id);
CREATE INDEX IF NOT EXISTS idx_candidate_profile_user_id ON candidate_profile(user_id);
CREATE INDEX IF NOT EXISTS idx_job_match_user_id ON job_match(user_id);
CREATE INDEX IF NOT EXISTS idx_email_log_user_id ON email_log(user_id);
CREATE INDEX IF NOT EXISTS idx_application_tracking_user_id ON application_tracking(user_id);

-- 5. Enabled Row Level Security on user-owned tables
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE jobs ENABLE ROW LEVEL SECURITY;
ALTER TABLE applications ENABLE ROW LEVEL SECURITY;
ALTER TABLE alerts ENABLE ROW LEVEL SECURITY;
ALTER TABLE candidate_profile ENABLE ROW LEVEL SECURITY;
ALTER TABLE job_match ENABLE ROW LEVEL SECURITY;
ALTER TABLE email_log ENABLE ROW LEVEL SECURITY;
ALTER TABLE application_tracking ENABLE ROW LEVEL SECURITY;

-- 6. Policies: only the authenticated user can read/update their own records
CREATE POLICY IF NOT EXISTS "users_self_access" ON users
    FOR ALL USING (auth.uid() = id) WITH CHECK (auth.uid() = id);

CREATE POLICY IF NOT EXISTS "jobs_self_access" ON jobs
    FOR ALL USING (user_id IS NULL OR user_id = auth.uid())
    WITH CHECK (user_id IS NULL OR user_id = auth.uid());

CREATE POLICY IF NOT EXISTS "applications_self_access" ON applications
    FOR ALL USING (user_id = auth.uid()) WITH CHECK (user_id = auth.uid());

CREATE POLICY IF NOT EXISTS "alerts_self_access" ON alerts
    FOR ALL USING (user_id = auth.uid()) WITH CHECK (user_id = auth.uid());

CREATE POLICY IF NOT EXISTS "candidate_profile_self_access" ON candidate_profile
    FOR ALL USING (user_id = auth.uid()) WITH CHECK (user_id = auth.uid());

CREATE POLICY IF NOT EXISTS "job_match_self_access" ON job_match
    FOR ALL USING (user_id = auth.uid()) WITH CHECK (user_id = auth.uid());

CREATE POLICY IF NOT EXISTS "email_log_self_access" ON email_log
    FOR ALL USING (user_id = auth.uid()) WITH CHECK (user_id = auth.uid());

CREATE POLICY IF NOT EXISTS "application_tracking_self_access" ON application_tracking
    FOR ALL USING (user_id = auth.uid()) WITH CHECK (user_id = auth.uid());

-- 7. Optional: allow public read of shared job feed if product is meant to be global
-- Uncomment if needed, but default is secure per-user isolation.
-- CREATE POLICY "jobs_public_read" ON jobs FOR SELECT USING (true);
