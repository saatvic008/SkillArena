-- ============================================================
-- SkillArena — Database Schema (PostgreSQL 15)
-- BCNF normalized, indexed, range-partitioned
-- ============================================================

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
-- CREATE EXTENSION IF NOT EXISTS "pg_cron";

-- ============================================================
-- 1. PLAYERS
-- ============================================================
CREATE TABLE players (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username      VARCHAR(50)  NOT NULL UNIQUE,
    email         VARCHAR(255) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    elo_rating    INT          NOT NULL DEFAULT 1200,
    created_at    TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_players_username ON players (username);
CREATE INDEX idx_players_email    ON players (email);
-- Use-case: fast lookup during login (by username or email)

-- ============================================================
-- 2. MATCHES (partitioned by played_at — monthly)
-- ============================================================
CREATE TABLE matches (
    id                UUID         NOT NULL DEFAULT gen_random_uuid(),
    player_id         UUID         NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    source            VARCHAR(20)  NOT NULL CHECK (source IN ('lichess', 'chesscom', 'upload')),
    opponent_username VARCHAR(100),
    result            VARCHAR(10)  NOT NULL CHECK (result IN ('win', 'loss', 'draw')),
    opening_name      VARCHAR(200),
    opening_eco       VARCHAR(10),
    time_control      VARCHAR(30),
    played_at         TIMESTAMPTZ  NOT NULL,
    pgn_raw           TEXT,
    metadata          JSONB        DEFAULT '{}',
    PRIMARY KEY (id, played_at)
) PARTITION BY RANGE (played_at);

CREATE INDEX idx_matches_player_id   ON matches (player_id);
CREATE INDEX idx_matches_played_at   ON matches (played_at);
CREATE INDEX idx_matches_opening_eco ON matches (opening_eco);
-- Use-case: idx_matches_player_id — list all matches for a player
-- Use-case: idx_matches_played_at — filter/sort matches by date
-- Use-case: idx_matches_opening_eco — aggregate stats by opening

-- Monthly partitions 2024-01 through 2026-12
DO $$
DECLARE
    start_date DATE := '2024-01-01';
    end_date   DATE;
    part_name  TEXT;
BEGIN
    FOR i IN 0..35 LOOP
        end_date := start_date + INTERVAL '1 month';
        part_name := 'matches_' || TO_CHAR(start_date, 'YYYY_MM');
        EXECUTE FORMAT(
            'CREATE TABLE IF NOT EXISTS %I PARTITION OF matches
             FOR VALUES FROM (%L) TO (%L)',
            part_name, start_date, end_date
        );
        start_date := end_date;
    END LOOP;
END $$;

-- ============================================================
-- 3. MOVES (partitioned by created_at — monthly)
-- ============================================================
CREATE TABLE moves (
    id            UUID         NOT NULL DEFAULT gen_random_uuid(),
    match_id      UUID         NOT NULL,
    move_number   INT          NOT NULL,
    color         CHAR(1)      NOT NULL CHECK (color IN ('w', 'b')),
    san           VARCHAR(10)  NOT NULL,
    uci           VARCHAR(10)  NOT NULL,
    fen_before    TEXT         NOT NULL,
    fen_after     TEXT         NOT NULL,
    eval_score    FLOAT,
    move_time_ms  INT,
    is_blunder    BOOLEAN      NOT NULL DEFAULT FALSE,
    is_mistake    BOOLEAN      NOT NULL DEFAULT FALSE,
    created_at    TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    PRIMARY KEY (id, created_at)
) PARTITION BY RANGE (created_at);

CREATE INDEX idx_moves_match_id   ON moves (match_id);
CREATE INDEX idx_moves_is_blunder ON moves (is_blunder) WHERE is_blunder = TRUE;
CREATE INDEX idx_moves_eval_score ON moves (eval_score);
-- Use-case: idx_moves_match_id — fetch all moves for a match replay
-- Use-case: idx_moves_is_blunder — partial index for fast blunder queries
-- Use-case: idx_moves_eval_score — range scans for eval distribution analysis

-- Monthly partitions 2024-01 through 2026-12
DO $$
DECLARE
    start_date DATE := '2024-01-01';
    end_date   DATE;
    part_name  TEXT;
BEGIN
    FOR i IN 0..35 LOOP
        end_date := start_date + INTERVAL '1 month';
        part_name := 'moves_' || TO_CHAR(start_date, 'YYYY_MM');
        EXECUTE FORMAT(
            'CREATE TABLE IF NOT EXISTS %I PARTITION OF moves
             FOR VALUES FROM (%L) TO (%L)',
            part_name, start_date, end_date
        );
        start_date := end_date;
    END LOOP;
END $$;

-- ============================================================
-- 4. MOVE ANNOTATIONS
-- ============================================================
CREATE TABLE move_annotations (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    move_id          UUID         NOT NULL,
    annotation_type  VARCHAR(20)  NOT NULL CHECK (
        annotation_type IN ('blunder', 'inaccuracy', 'best_move', 'brilliant')
    ),
    engine_best_move VARCHAR(10),
    eval_delta       FLOAT,
    annotation_text  TEXT
);

CREATE INDEX idx_move_annotations_move_id ON move_annotations (move_id);
-- Use-case: join with moves table to display annotations on board

-- ============================================================
-- 5. WEAKNESS REPORTS
-- ============================================================
CREATE TABLE weakness_reports (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    player_id        UUID         NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    report_date      DATE         NOT NULL DEFAULT CURRENT_DATE,
    blunder_rate     FLOAT,
    avg_accuracy     FLOAT,
    weak_openings    JSONB        DEFAULT '[]',
    weak_endgames    JSONB        DEFAULT '[]',
    tactical_patterns JSONB       DEFAULT '[]',
    generated_at     TIMESTAMPTZ
);

CREATE INDEX idx_weakness_reports_player_id ON weakness_reports (player_id);
-- Use-case: fetch latest report for a player's dashboard

-- ============================================================
-- 6. DRILLS
-- ============================================================
CREATE TABLE drills (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title         VARCHAR(200) NOT NULL,
    description   TEXT,
    difficulty    INT          NOT NULL CHECK (difficulty BETWEEN 1 AND 5),
    category      VARCHAR(20)  NOT NULL CHECK (
        category IN ('tactic', 'endgame', 'opening')
    ),
    fen_position  TEXT         NOT NULL,
    correct_move  VARCHAR(10)  NOT NULL,
    explanation   TEXT
);

-- ============================================================
-- 7. DRILL ATTEMPTS
-- ============================================================
CREATE TABLE drill_attempts (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    player_id     UUID         NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    drill_id      UUID         NOT NULL REFERENCES drills(id) ON DELETE CASCADE,
    player_move   VARCHAR(10)  NOT NULL,
    is_correct    BOOLEAN      NOT NULL,
    time_taken_ms INT,
    attempted_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_drill_attempts_player_id ON drill_attempts (player_id);
CREATE INDEX idx_drill_attempts_drill_id  ON drill_attempts (drill_id);
-- Use-case: idx_drill_attempts_player_id — drill history for a player
-- Use-case: idx_drill_attempts_drill_id — drill success rate analytics

-- ============================================================
-- 8. RECOMMENDATIONS
-- ============================================================
CREATE TABLE recommendations (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    player_id     UUID         NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    report_id     UUID         NOT NULL REFERENCES weakness_reports(id) ON DELETE CASCADE,
    drill_id      UUID         NOT NULL REFERENCES drills(id) ON DELETE CASCADE,
    priority      INT          NOT NULL DEFAULT 0,
    reason        TEXT,
    created_at    TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_recommendations_player_id ON recommendations (player_id);
-- Use-case: fetch top-priority drills recommended for a player

-- ============================================================
-- MATERIALIZED VIEW: player_stats_mv
-- ============================================================
CREATE MATERIALIZED VIEW player_stats_mv AS
SELECT
    p.id                                         AS player_id,
    p.username,
    p.elo_rating,
    COUNT(m.id)                                  AS games_played,
    ROUND(AVG(CASE WHEN wr.avg_accuracy IS NOT NULL THEN wr.avg_accuracy END)::NUMERIC, 2) AS avg_accuracy,
    ROUND(
        COUNT(CASE WHEN m.result = 'win' THEN 1 END)::NUMERIC
        / NULLIF(COUNT(m.id), 0) * 100, 2
    )                                            AS win_rate,
    COUNT(CASE WHEN m.result = 'win'  THEN 1 END) AS wins,
    COUNT(CASE WHEN m.result = 'loss' THEN 1 END) AS losses,
    COUNT(CASE WHEN m.result = 'draw' THEN 1 END) AS draws
FROM players p
LEFT JOIN matches m ON m.player_id = p.id
LEFT JOIN weakness_reports wr ON wr.player_id = p.id
GROUP BY p.id, p.username, p.elo_rating;

CREATE UNIQUE INDEX idx_player_stats_mv_player_id ON player_stats_mv (player_id);
-- Allows REFRESH CONCURRENTLY

-- Schedule hourly refresh via pg_cron
-- SELECT cron.schedule(
--     'refresh_player_stats_mv',
--     '0 * * * *',
--     'REFRESH MATERIALIZED VIEW CONCURRENTLY player_stats_mv'
-- );

-- ============================================================
-- TRIGGER: Auto-create pending weakness_report on match insert
-- ============================================================
CREATE OR REPLACE FUNCTION fn_create_pending_report()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO weakness_reports (player_id, report_date)
    VALUES (NEW.player_id, CURRENT_DATE)
    ON CONFLICT DO NOTHING;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_match_insert_report
    AFTER INSERT ON matches
    FOR EACH ROW
    EXECUTE FUNCTION fn_create_pending_report();
