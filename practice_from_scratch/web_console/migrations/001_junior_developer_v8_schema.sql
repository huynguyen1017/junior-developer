-- ============================================================================
-- JUNIOR DEVELOPER V8.0 — MULTI-TENANT RELATIONAL SCHEMA & RLS MIGRATION
-- Brand: JUNIOR DEVELOPER ("Learn. Build. Connect.")
-- Compatible with SQLite WAL (Staged/Local Engine) & PostgreSQL / Supabase RLS
-- ============================================================================

PRAGMA foreign_keys = ON;

-- 1. User Profiles & Authenticated Accounts
CREATE TABLE IF NOT EXISTS profiles (
    user_id TEXT PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    password_salt TEXT NOT NULL,
    display_name TEXT NOT NULL,
    handle TEXT UNIQUE NOT NULL,
    role TEXT NOT NULL DEFAULT 'student', -- 'guest', 'student', 'instructor', 'moderator', 'owner_admin'
    avatar_url TEXT DEFAULT '',
    bio TEXT DEFAULT '',
    learning_path TEXT DEFAULT 'beginner_digital_logic',
    declared_topics_json TEXT DEFAULT '["Verilog","ASIC Design","Computer Architecture"]',
    reputation INTEGER NOT NULL DEFAULT 10,
    online_visibility TEXT NOT NULL DEFAULT 'online', -- 'online', 'study_mode', 'Appear_offline'
    allow_message_requests INTEGER NOT NULL DEFAULT 1,
    github_connected_account TEXT DEFAULT '',
    eda_companion_authorized INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

-- 2. Authenticated Sessions (HTTP-Only / Bearer + CSRF Protection)
CREATE TABLE IF NOT EXISTS sessions (
    session_id TEXT PRIMARY KEY,
    token_hash TEXT UNIQUE NOT NULL,
    csrf_token TEXT NOT NULL,
    user_id TEXT NOT NULL REFERENCES profiles(user_id) ON DELETE CASCADE,
    is_guest INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    expires_at TEXT NOT NULL,
    revoked_at TEXT DEFAULT NULL,
    user_agent TEXT DEFAULT '',
    ip_hash TEXT DEFAULT ''
);
CREATE INDEX IF NOT EXISTS idx_sessions_token_hash ON sessions(token_hash);
CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions(user_id);

-- 3. Junior Connect — Reddit-Style Technical Communities
CREATE TABLE IF NOT EXISTS communities (
    id TEXT PRIMARY KEY,
    slug TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    tagline TEXT NOT NULL,
    description TEXT NOT NULL,
    category TEXT NOT NULL,
    visibility TEXT NOT NULL DEFAULT 'public', -- 'public', 'private', 'course_group'
    owner_id TEXT NOT NULL REFERENCES profiles(user_id),
    rules_json TEXT NOT NULL DEFAULT '[]',
    member_count INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS community_members (
    community_id TEXT NOT NULL REFERENCES communities(id) ON DELETE CASCADE,
    user_id TEXT NOT NULL REFERENCES profiles(user_id) ON DELETE CASCADE,
    role TEXT NOT NULL DEFAULT 'member', -- 'member', 'moderator', 'instructor', 'owner'
    joined_at TEXT NOT NULL,
    PRIMARY KEY (community_id, user_id)
);

-- 4. Community Posts (Ask a Question, Help Me Debug, Share a Project, Explain a Concept, Study Group, Solved Problem)
CREATE TABLE IF NOT EXISTS posts (
    id TEXT PRIMARY KEY,
    community_id TEXT NOT NULL REFERENCES communities(id) ON DELETE CASCADE,
    author_id TEXT NOT NULL REFERENCES profiles(user_id) ON DELETE CASCADE,
    post_type TEXT NOT NULL DEFAULT 'Ask a Question',
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    tags_json TEXT NOT NULL DEFAULT '[]',
    code_snippet TEXT DEFAULT '',
    lab_run_id TEXT DEFAULT '',
    shared_artifact_id TEXT DEFAULT '',
    sanitized_verified INTEGER NOT NULL DEFAULT 1,
    vote_score INTEGER NOT NULL DEFAULT 1,
    comment_count INTEGER NOT NULL DEFAULT 0,
    accepted_comment_id TEXT DEFAULT '',
    is_pinned INTEGER NOT NULL DEFAULT 0,
    is_locked INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_posts_community_id ON posts(community_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_posts_author_id ON posts(author_id);

-- 5. Nested Comments & Technical Explanations
CREATE TABLE IF NOT EXISTS comments (
    id TEXT PRIMARY KEY,
    post_id TEXT NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    parent_comment_id TEXT DEFAULT '',
    author_id TEXT NOT NULL REFERENCES profiles(user_id) ON DELETE CASCADE,
    body TEXT NOT NULL,
    code_snippet TEXT DEFAULT '',
    vote_score INTEGER NOT NULL DEFAULT 1,
    is_accepted INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_comments_post_id ON comments(post_id, created_at ASC);

-- 6. Helpful Votes, Saved Posts, Tags & Accepted Answers
CREATE TABLE IF NOT EXISTS votes (
    user_id TEXT NOT NULL REFERENCES profiles(user_id) ON DELETE CASCADE,
    target_type TEXT NOT NULL, -- 'post' or 'comment'
    target_id TEXT NOT NULL,
    value INTEGER NOT NULL,    -- +1 or -1
    created_at TEXT NOT NULL,
    PRIMARY KEY (user_id, target_type, target_id)
);

CREATE TABLE IF NOT EXISTS saved_posts (
    user_id TEXT NOT NULL REFERENCES profiles(user_id) ON DELETE CASCADE,
    post_id TEXT NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    created_at TEXT NOT NULL,
    PRIMARY KEY (user_id, post_id)
);

CREATE TABLE IF NOT EXISTS post_tags (
    post_id TEXT NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    tag TEXT NOT NULL,
    PRIMARY KEY (post_id, tag)
);

CREATE TABLE IF NOT EXISTS accepted_answers (
    post_id TEXT PRIMARY KEY REFERENCES posts(id) ON DELETE CASCADE,
    comment_id TEXT NOT NULL REFERENCES comments(id) ON DELETE CASCADE,
    accepted_by TEXT NOT NULL REFERENCES profiles(user_id) ON DELETE CASCADE,
    accepted_at TEXT NOT NULL
);

-- 7. Junior Messenger — Real-Time Conversations (Direct, Group Study Rooms, Community Rooms)
CREATE TABLE IF NOT EXISTS conversations (
    id TEXT PRIMARY KEY,
    type TEXT NOT NULL DEFAULT 'direct', -- 'direct', 'group_study', 'community_room'
    title TEXT DEFAULT '',
    community_id TEXT DEFAULT '',
    created_by TEXT NOT NULL REFERENCES profiles(user_id) ON DELETE CASCADE,
    request_status TEXT NOT NULL DEFAULT 'active', -- 'active', 'pending_request', 'declined'
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS conversation_members (
    conversation_id TEXT NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    user_id TEXT NOT NULL REFERENCES profiles(user_id) ON DELETE CASCADE,
    role TEXT NOT NULL DEFAULT 'member', -- 'owner', 'moderator', 'member', 'invited'
    joined_at TEXT NOT NULL,
    last_read_at TEXT DEFAULT '',
    typing_until TEXT DEFAULT '',
    PRIMARY KEY (conversation_id, user_id)
);
CREATE INDEX IF NOT EXISTS idx_conv_members_user ON conversation_members(user_id);

CREATE TABLE IF NOT EXISTS messages (
    id TEXT PRIMARY KEY,
    conversation_id TEXT NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    sender_id TEXT NOT NULL REFERENCES profiles(user_id) ON DELETE CASCADE,
    reply_to_id TEXT DEFAULT '',
    body TEXT NOT NULL,
    code_snippet TEXT DEFAULT '',
    attachment_json TEXT DEFAULT '{}',
    reactions_json TEXT DEFAULT '{}',
    delivery_status TEXT NOT NULL DEFAULT 'delivered', -- 'sent', 'delivered', 'read'
    created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_messages_conv_created ON messages(conversation_id, created_at ASC);

CREATE TABLE IF NOT EXISTS message_attachments (
    id TEXT PRIMARY KEY,
    message_id TEXT NOT NULL REFERENCES messages(id) ON DELETE CASCADE,
    storage_object_id TEXT NOT NULL,
    file_name TEXT NOT NULL,
    mime_type TEXT NOT NULL,
    sanitized_verified INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL
);

-- 8. Safety, Blocks, Reports, Moderation & Notifications
CREATE TABLE IF NOT EXISTS notifications (
    id TEXT PRIMARY KEY,
    recipient_id TEXT NOT NULL REFERENCES profiles(user_id) ON DELETE CASCADE,
    actor_id TEXT DEFAULT '',
    event_type TEXT NOT NULL,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    target_url TEXT DEFAULT '',
    read_at TEXT DEFAULT '',
    created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_notifications_recipient ON notifications(recipient_id, created_at DESC);

CREATE TABLE IF NOT EXISTS user_blocks (
    blocker_id TEXT NOT NULL REFERENCES profiles(user_id) ON DELETE CASCADE,
    blocked_id TEXT NOT NULL REFERENCES profiles(user_id) ON DELETE CASCADE,
    reason TEXT DEFAULT '',
    created_at TEXT NOT NULL,
    PRIMARY KEY (blocker_id, blocked_id)
);

CREATE TABLE IF NOT EXISTS reports (
    id TEXT PRIMARY KEY,
    reporter_id TEXT NOT NULL REFERENCES profiles(user_id) ON DELETE CASCADE,
    object_type TEXT NOT NULL, -- 'post', 'comment', 'message', 'user'
    object_id TEXT NOT NULL,
    reason TEXT NOT NULL,
    details TEXT DEFAULT '',
    priority TEXT NOT NULL DEFAULT 'medium',
    status TEXT NOT NULL DEFAULT 'open', -- 'open', 'reviewed', 'resolved', 'dismissed'
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS moderation_actions (
    id TEXT PRIMARY KEY,
    moderator_id TEXT NOT NULL REFERENCES profiles(user_id),
    report_id TEXT DEFAULT '',
    action TEXT NOT NULL,
    notes TEXT DEFAULT '',
    created_at TEXT NOT NULL
);

-- 9. Courses, Lessons, Student Projects, Open-Source EDA Lab Runs & Shared Sanitized Artifacts
CREATE TABLE IF NOT EXISTS courses (
    id TEXT PRIMARY KEY,
    slug TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    discipline TEXT NOT NULL,
    difficulty TEXT NOT NULL,
    summary TEXT NOT NULL,
    lesson_count INTEGER NOT NULL DEFAULT 1,
    has_interactive_lab INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS lessons (
    id TEXT PRIMARY KEY,
    course_id TEXT NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
    lesson_number INTEGER NOT NULL,
    title TEXT NOT NULL,
    content_md TEXT NOT NULL,
    starter_rtl TEXT DEFAULT '',
    starter_tb TEXT DEFAULT '',
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS projects (
    id TEXT PRIMARY KEY,
    owner_id TEXT NOT NULL REFERENCES profiles(user_id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    template_type TEXT NOT NULL DEFAULT 'start_from_zero', -- 'start_from_zero', 'import_existing', 'motion_estimator_reference'
    visibility TEXT NOT NULL DEFAULT 'private', -- 'private', 'community_shared'
    rtl_source TEXT NOT NULL DEFAULT '',
    tb_source TEXT NOT NULL DEFAULT '',
    constraints_sdc TEXT DEFAULT '',
    github_repo TEXT DEFAULT '',
    github_sync_state TEXT NOT NULL DEFAULT 'LOCAL_SAVED', -- 'LOCAL_SAVED', 'LOCAL_COMMITTED', 'PUSH_PENDING', 'PUSH_FAILED', 'REMOTE_CONFIRMED'
    github_last_sha TEXT DEFAULT '',
    learning_progress_pct INTEGER NOT NULL DEFAULT 0,
    execution_count INTEGER NOT NULL DEFAULT 0,
    verified_count INTEGER NOT NULL DEFAULT 0,
    progress_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_projects_owner ON projects(owner_id);

CREATE TABLE IF NOT EXISTS lab_runs (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    owner_id TEXT NOT NULL REFERENCES profiles(user_id) ON DELETE CASCADE,
    engine_type TEXT NOT NULL DEFAULT 'open_source_eda', -- 'open_source_eda', 'authorized_native_verdi'
    tool_chain TEXT NOT NULL DEFAULT 'iverilog+vvp+yosys',
    execution_mode TEXT NOT NULL DEFAULT 'one_line', -- 'full_auto', 'one_line', 'baby_steps'
    state TEXT NOT NULL DEFAULT 'QUEUED', -- 'QUEUED','AUTHORIZING','PREPARING','RUNNING','VERIFYING','PASSED','FAILED','BLOCKED','CANCELLED'
    evidence_class TEXT NOT NULL DEFAULT 'UNVERIFIED', -- 'OPEN_SOURCE_SIMULATION_VERIFIED', 'NATIVE_EXECUTION', 'EDUCATIONAL_SIMULATION', 'FAILED'
    compiler_log TEXT DEFAULT '',
    simulation_log TEXT DEFAULT '',
    synthesis_report TEXT DEFAULT '',
    timing_report TEXT DEFAULT '',
    vcd_path TEXT DEFAULT '',
    waveform_json TEXT DEFAULT '{}',
    verification_json TEXT DEFAULT '{}',
    created_at TEXT NOT NULL,
    finished_at TEXT DEFAULT ''
);
CREATE INDEX IF NOT EXISTS idx_lab_runs_owner ON lab_runs(owner_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_lab_runs_project ON lab_runs(project_id, created_at DESC);

CREATE TABLE IF NOT EXISTS verification_results (
    id TEXT PRIMARY KEY,
    lab_run_id TEXT NOT NULL REFERENCES lab_runs(id) ON DELETE CASCADE,
    owner_id TEXT NOT NULL REFERENCES profiles(user_id) ON DELETE CASCADE,
    layer_fsdb_or_vcd INTEGER NOT NULL DEFAULT 0,
    layer_numerical INTEGER NOT NULL DEFAULT 0,
    layer_synthesis INTEGER NOT NULL DEFAULT 0,
    layer_visual INTEGER NOT NULL DEFAULT 0,
    overall_passed INTEGER NOT NULL DEFAULT 0,
    details_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS shared_artifacts (
    id TEXT PRIMARY KEY,
    lab_run_id TEXT NOT NULL REFERENCES lab_runs(id) ON DELETE CASCADE,
    project_id TEXT NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    shared_by TEXT NOT NULL REFERENCES profiles(user_id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    artifact_type TEXT NOT NULL DEFAULT 'help_me_debug_bundle',
    sanitized_rtl TEXT DEFAULT '',
    sanitized_log TEXT DEFAULT '',
    waveform_summary_json TEXT DEFAULT '{}',
    privacy_scan_passed INTEGER NOT NULL DEFAULT 1,
    redacted_items_count INTEGER NOT NULL DEFAULT 0,
    access_policy TEXT NOT NULL DEFAULT 'community_read', -- 'community_read', 'conversation_members', 'private'
    created_at TEXT NOT NULL
);

-- ============================================================================
-- POSTGRESQL / SUPABASE ROW-LEVEL SECURITY (RLS) REFERENCE POLICIES
-- (Executed when deploying against PostgreSQL / Supabase Auth)
-- ============================================================================
-- ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
-- CREATE POLICY projects_owner_isolation ON projects
--   USING (owner_id = auth.uid()::text OR visibility = 'community_shared')
--   WITH CHECK (owner_id = auth.uid()::text);
--
-- ALTER TABLE lab_runs ENABLE ROW LEVEL SECURITY;
-- CREATE POLICY lab_runs_owner_isolation ON lab_runs
--   USING (owner_id = auth.uid()::text)
--   WITH CHECK (owner_id = auth.uid()::text);
--
-- ALTER TABLE conversations ENABLE ROW LEVEL SECURITY;
-- CREATE POLICY conversations_member_only ON conversations
--   USING (EXISTS (
--     SELECT 1 FROM conversation_members cm
--     WHERE cm.conversation_id = conversations.id AND cm.user_id = auth.uid()::text
--   ));
--
-- ALTER TABLE messages ENABLE ROW LEVEL SECURITY;
-- CREATE POLICY messages_member_only ON messages
--   USING (EXISTS (
--     SELECT 1 FROM conversation_members cm
--     WHERE cm.conversation_id = messages.conversation_id AND cm.user_id = auth.uid()::text
--   ))
--   WITH CHECK (
--     sender_id = auth.uid()::text AND EXISTS (
--       SELECT 1 FROM conversation_members cm
--       WHERE cm.conversation_id = messages.conversation_id AND cm.user_id = auth.uid()::text
--     )
--   );
