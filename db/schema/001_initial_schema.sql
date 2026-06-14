CREATE TABLE "User" (
    user_id BIGINT GENERATED ALWAYS AS IDENTITY,
    username TEXT NOT NULL,
    email TEXT,
    lc_username TEXT,
    cf_username TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_synced_at TIMESTAMPTZ,
    PRIMARY KEY (user_id),
    UNIQUE (username),
    UNIQUE (email)
);
CREATE TABLE "Problems" (
    problem_id BIGINT GENERATED ALWAYS AS IDENTITY,
    platform TEXT NOT NULL,
    platform_problem_id TEXT NOT NULL,
    title TEXT NOT NULL,
    platform_difficulty TEXT,
    cf_rating INT,
    url TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (problem_id),
    UNIQUE (platform, platform_problem_id),
    CHECK (
        platform IN ('codeforces', 'leetcode')
    ),
    CHECK (
        cf_rating IS NULL
        OR cf_rating > 0
    )
);
CREATE TABLE "Tags" (
    tag_id BIGINT GENERATED ALWAYS AS IDENTITY,
    name TEXT NOT NULL,
    PRIMARY KEY (tag_id),
    UNIQUE (name)
);
CREATE TABLE "ProblemTags" (
    problem_id BIGINT NOT NULL,
    tag_id BIGINT NOT NULL,
    PRIMARY KEY (problem_id, tag_id),
    FOREIGN KEY (problem_id) REFERENCES "Problems"(problem_id),
    FOREIGN KEY (tag_id) REFERENCES "Tags"(tag_id)
);
CREATE TABLE "UserSessions" (
    session_id BIGINT GENERATED ALWAYS AS IDENTITY,
    user_id BIGINT NOT NULL,
    started_at TIMESTAMPTZ NOT NULL,
    ended_at TIMESTAMPTZ NOT NULL,
    PRIMARY KEY (session_id),
    FOREIGN KEY (user_id) REFERENCES "User"(user_id),
    CHECK (ended_at > started_at)
);
CREATE TABLE "ContestParticipation" (
    participation_id BIGINT GENERATED ALWAYS AS IDENTITY,
    user_id BIGINT NOT NULL,
    platform TEXT NOT NULL,
    contest_id TEXT NOT NULL,
    contest_name TEXT NOT NULL,
    rank INT,
    old_rating INT,
    new_rating INT,
    participated_at TIMESTAMPTZ NOT NULL,
    PRIMARY KEY (participation_id),
    FOREIGN KEY (user_id) REFERENCES "User"(user_id),
    UNIQUE (user_id, platform, contest_id)
);
CREATE TABLE "Submissions" (
    submission_id BIGINT GENERATED ALWAYS AS IDENTITY,
    user_id BIGINT NOT NULL,
    session_id BIGINT,
    problem_id BIGINT NOT NULL,
    platform TEXT NOT NULL,
    platform_submission_id TEXT NOT NULL,
    verdict TEXT NOT NULL,
    language TEXT NOT NULL,
    submitted_at TIMESTAMPTZ NOT NULL,
    attempt_number INT NOT NULL,
    PRIMARY KEY (submission_id),
    FOREIGN KEY (user_id) REFERENCES "User"(user_id),
    FOREIGN KEY (session_id) REFERENCES "UserSessions"(session_id),
    FOREIGN KEY (problem_id) REFERENCES "Problems"(problem_id),
    UNIQUE (platform, platform_submission_id),
    CHECK (attempt_number > 0)
);
-- Foreign Key Indexes
CREATE INDEX idx_usersessions_user_id ON "UserSessions"(user_id);
CREATE INDEX idx_submissions_user_id ON "Submissions"(user_id);
CREATE INDEX idx_submissions_problem_id ON "Submissions"(problem_id);
CREATE INDEX idx_submissions_session_id ON "Submissions"(session_id);
CREATE INDEX idx_submissions_submitted_at ON "Submissions"(submitted_at);
CREATE INDEX idx_submissions_user_problem ON "Submissions"(user_id, problem_id);
CREATE INDEX idx_contestparticipation_user_id ON "ContestParticipation"(user_id);
CREATE INDEX idx_contestparticipation_user_date ON "ContestParticipation"(user_id, participated_at);
CREATE INDEX idx_problemtags_problem_id ON "ProblemTags"(problem_id);
CREATE INDEX idx_problemtags_tag_id ON "ProblemTags"(tag_id);
CREATE INDEX idx_problems_platform ON "Problems"(platform);
