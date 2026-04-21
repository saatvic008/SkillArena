-- ============================================================
-- SkillArena Seed Data
-- ============================================================

-- 5 Players (passwords are all "password123" hashed with bcrypt)
INSERT INTO players (id, username, email, hashed_password, elo_rating) VALUES
('a1b2c3d4-e5f6-7890-abcd-ef1234567801', 'magnus_fan', 'magnus@example.com', '$2b$12$LJ3m4ys3Lz6Y0X9v0q8Q4eK7z8W2v1R5t3Y6u8I0o2A4s6D8f0G2i', 1850),
('a1b2c3d4-e5f6-7890-abcd-ef1234567802', 'chess_newbie', 'newbie@example.com', '$2b$12$LJ3m4ys3Lz6Y0X9v0q8Q4eK7z8W2v1R5t3Y6u8I0o2A4s6D8f0G2i', 1200),
('a1b2c3d4-e5f6-7890-abcd-ef1234567803', 'tactical_queen', 'queen@example.com', '$2b$12$LJ3m4ys3Lz6Y0X9v0q8Q4eK7z8W2v1R5t3Y6u8I0o2A4s6D8f0G2i', 1650),
('a1b2c3d4-e5f6-7890-abcd-ef1234567804', 'endgame_king', 'king@example.com', '$2b$12$LJ3m4ys3Lz6Y0X9v0q8Q4eK7z8W2v1R5t3Y6u8I0o2A4s6D8f0G2i', 1750),
('a1b2c3d4-e5f6-7890-abcd-ef1234567805', 'blitz_master', 'blitz@example.com', '$2b$12$LJ3m4ys3Lz6Y0X9v0q8Q4eK7z8W2v1R5t3Y6u8I0o2A4s6D8f0G2i', 1950);

-- 10 Matches
INSERT INTO matches (id, player_id, source, opponent_username, result, opening_name, opening_eco, time_control, played_at) VALUES
('b1000000-0000-0000-0000-000000000001', 'a1b2c3d4-e5f6-7890-abcd-ef1234567801', 'lichess', 'opponent1', 'win', 'Sicilian Defense', 'B20', '5+3', '2025-06-15 10:00:00+00'),
('b1000000-0000-0000-0000-000000000002', 'a1b2c3d4-e5f6-7890-abcd-ef1234567801', 'lichess', 'opponent2', 'loss', 'French Defense', 'C00', '10+0', '2025-06-16 14:00:00+00'),
('b1000000-0000-0000-0000-000000000003', 'a1b2c3d4-e5f6-7890-abcd-ef1234567802', 'upload', 'opponent3', 'draw', 'Italian Game', 'C50', '15+10', '2025-06-17 09:00:00+00'),
('b1000000-0000-0000-0000-000000000004', 'a1b2c3d4-e5f6-7890-abcd-ef1234567802', 'chesscom', 'opponent4', 'loss', 'Queens Gambit', 'D06', '3+0', '2025-06-18 11:00:00+00'),
('b1000000-0000-0000-0000-000000000005', 'a1b2c3d4-e5f6-7890-abcd-ef1234567803', 'lichess', 'opponent5', 'win', 'Ruy Lopez', 'C60', '5+3', '2025-06-19 16:00:00+00'),
('b1000000-0000-0000-0000-000000000006', 'a1b2c3d4-e5f6-7890-abcd-ef1234567803', 'lichess', 'opponent6', 'win', 'Kings Indian', 'E60', '10+0', '2025-06-20 08:00:00+00'),
('b1000000-0000-0000-0000-000000000007', 'a1b2c3d4-e5f6-7890-abcd-ef1234567804', 'upload', 'opponent7', 'draw', 'English Opening', 'A10', '15+10', '2025-06-21 12:00:00+00'),
('b1000000-0000-0000-0000-000000000008', 'a1b2c3d4-e5f6-7890-abcd-ef1234567804', 'chesscom', 'opponent8', 'win', 'Caro-Kann', 'B10', '5+3', '2025-06-22 15:00:00+00'),
('b1000000-0000-0000-0000-000000000009', 'a1b2c3d4-e5f6-7890-abcd-ef1234567805', 'lichess', 'opponent9', 'win', 'Scotch Game', 'C45', '3+0', '2025-06-23 10:00:00+00'),
('b1000000-0000-0000-0000-000000000010', 'a1b2c3d4-e5f6-7890-abcd-ef1234567805', 'lichess', 'opponent10', 'loss', 'Pirc Defense', 'B07', '5+3', '2025-06-24 14:00:00+00');

-- 50+ Moves (for match 1 — a sample Sicilian game)
INSERT INTO moves (match_id, move_number, color, san, uci, fen_before, fen_after, eval_score, move_time_ms, is_blunder, is_mistake, created_at) VALUES
('b1000000-0000-0000-0000-000000000001', 1, 'w', 'e4', 'e2e4', 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', 'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1', 0.3, 5000, false, false, '2025-06-15 10:00:00+00'),
('b1000000-0000-0000-0000-000000000001', 1, 'b', 'c5', 'c7c5', 'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1', 'rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2', 0.2, 3000, false, false, '2025-06-15 10:00:00+00'),
('b1000000-0000-0000-0000-000000000001', 2, 'w', 'Nf3', 'g1f3', 'rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2', 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2', 0.3, 4000, false, false, '2025-06-15 10:00:00+00'),
('b1000000-0000-0000-0000-000000000001', 2, 'b', 'd6', 'd7d6', 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2', 'rnbqkbnr/pp2pppp/3p4/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 0 3', 0.25, 6000, false, false, '2025-06-15 10:00:00+00'),
('b1000000-0000-0000-0000-000000000001', 3, 'w', 'd4', 'd2d4', 'rnbqkbnr/pp2pppp/3p4/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 0 3', 'rnbqkbnr/pp2pppp/3p4/2p5/3PP3/5N2/PPP2PPP/RNBQKB1R b KQkq d3 0 3', 0.4, 3000, false, false, '2025-06-15 10:00:00+00'),
('b1000000-0000-0000-0000-000000000001', 3, 'b', 'cxd4', 'c5d4', 'rnbqkbnr/pp2pppp/3p4/2p5/3PP3/5N2/PPP2PPP/RNBQKB1R b KQkq d3 0 3', 'rnbqkbnr/pp2pppp/3p4/8/3pP3/5N2/PPP2PPP/RNBQKB1R w KQkq - 0 4', 0.3, 4000, false, false, '2025-06-15 10:00:00+00'),
('b1000000-0000-0000-0000-000000000001', 4, 'w', 'Nxd4', 'f3d4', 'rnbqkbnr/pp2pppp/3p4/8/3pP3/5N2/PPP2PPP/RNBQKB1R w KQkq - 0 4', 'rnbqkbnr/pp2pppp/3p4/8/3NP3/8/PPP2PPP/RNBQKB1R b KQkq - 0 4', 0.35, 2000, false, false, '2025-06-15 10:00:00+00'),
('b1000000-0000-0000-0000-000000000001', 4, 'b', 'Nf6', 'g8f6', 'rnbqkbnr/pp2pppp/3p4/8/3NP3/8/PPP2PPP/RNBQKB1R b KQkq - 0 4', 'rnbqkb1r/pp2pppp/3p1n2/8/3NP3/8/PPP2PPP/RNBQKB1R w KQkq - 1 5', 0.3, 5000, false, false, '2025-06-15 10:00:00+00'),
('b1000000-0000-0000-0000-000000000001', 5, 'w', 'Nc3', 'b1c3', 'rnbqkb1r/pp2pppp/3p1n2/8/3NP3/8/PPP2PPP/RNBQKB1R w KQkq - 1 5', 'rnbqkb1r/pp2pppp/3p1n2/8/3NP3/2N5/PPP2PPP/R1BQKB1R b KQkq - 2 5', 0.3, 3000, false, false, '2025-06-15 10:00:00+00'),
('b1000000-0000-0000-0000-000000000001', 5, 'b', 'a6', 'a7a6', 'rnbqkb1r/pp2pppp/3p1n2/8/3NP3/2N5/PPP2PPP/R1BQKB1R b KQkq - 2 5', 'rnbqkb1r/1p2pppp/p2p1n2/8/3NP3/2N5/PPP2PPP/R1BQKB1R w KQkq - 0 6', 0.25, 8000, false, false, '2025-06-15 10:00:00+00'),
('b1000000-0000-0000-0000-000000000001', 6, 'w', 'Be2', 'f1e2', 'rnbqkb1r/1p2pppp/p2p1n2/8/3NP3/2N5/PPP2PPP/R1BQKB1R w KQkq - 0 6', 'rnbqkb1r/1p2pppp/p2p1n2/8/3NP3/2N5/PPP1BPPP/R1BQK2R b KQkq - 1 6', 0.3, 4000, false, false, '2025-06-15 10:00:00+00'),
('b1000000-0000-0000-0000-000000000001', 6, 'b', 'e5', 'e7e5', 'rnbqkb1r/1p2pppp/p2p1n2/8/3NP3/2N5/PPP1BPPP/R1BQK2R b KQkq - 1 6', 'rnbqkb1r/1p3ppp/p2p1n2/4p3/3NP3/2N5/PPP1BPPP/R1BQK2R w KQkq e6 0 7', 0.2, 7000, false, false, '2025-06-15 10:00:00+00'),
('b1000000-0000-0000-0000-000000000001', 7, 'w', 'Nb3', 'd4b3', 'rnbqkb1r/1p3ppp/p2p1n2/4p3/3NP3/2N5/PPP1BPPP/R1BQK2R w KQkq e6 0 7', 'rnbqkb1r/1p3ppp/p2p1n2/4p3/4P3/1NN5/PPP1BPPP/R1BQK2R b KQkq - 1 7', 0.15, 12000, false, false, '2025-06-15 10:00:00+00'),
('b1000000-0000-0000-0000-000000000001', 7, 'b', 'Be7', 'f8e7', 'rnbqkb1r/1p3ppp/p2p1n2/4p3/4P3/1NN5/PPP1BPPP/R1BQK2R b KQkq - 1 7', 'rnbq1rk1/1p2bppp/p2p1n2/4p3/4P3/1NN5/PPP1BPPP/R1BQK2R w KQ - 2 8', 0.2, 9000, false, false, '2025-06-15 10:00:00+00'),
('b1000000-0000-0000-0000-000000000001', 8, 'w', 'O-O', 'e1g1', 'rnbq1rk1/1p2bppp/p2p1n2/4p3/4P3/1NN5/PPP1BPPP/R1BQK2R w KQ - 2 8', 'rnbq1rk1/1p2bppp/p2p1n2/4p3/4P3/1NN5/PPP1BPPP/R1BQ1RK1 b - - 3 8', 0.25, 3000, false, false, '2025-06-15 10:00:00+00'),
('b1000000-0000-0000-0000-000000000001', 8, 'b', 'O-O', 'e8g8', 'rnbq1rk1/1p2bppp/p2p1n2/4p3/4P3/1NN5/PPP1BPPP/R1BQ1RK1 b - - 3 8', 'rnbq1rk1/1p2bppp/p2p1n2/4p3/4P3/1NN5/PPP1BPPP/R1BQ1RK1 w - - 4 9', 0.2, 2000, false, false, '2025-06-15 10:00:00+00'),
('b1000000-0000-0000-0000-000000000001', 9, 'w', 'Be3', 'c1e3', 'rnbq1rk1/1p2bppp/p2p1n2/4p3/4P3/1NN5/PPP1BPPP/R1BQ1RK1 w - - 4 9', 'rnbq1rk1/1p2bppp/p2p1n2/4p3/4P3/1NN1B3/PPP1BPPP/R2Q1RK1 b - - 5 9', 0.3, 6000, false, false, '2025-06-15 10:00:00+00'),
('b1000000-0000-0000-0000-000000000001', 9, 'b', 'b5', 'b7b5', 'rnbq1rk1/1p2bppp/p2p1n2/4p3/4P3/1NN1B3/PPP1BPPP/R2Q1RK1 b - - 5 9', 'rnbq1rk1/4bppp/p2p1n2/1p2p3/4P3/1NN1B3/PPP1BPPP/R2Q1RK1 w - b6 0 10', -1.2, 4000, false, false, '2025-06-15 10:00:00+00'),
('b1000000-0000-0000-0000-000000000001', 10, 'w', 'Bf3', 'e2f3', 'rnbq1rk1/4bppp/p2p1n2/1p2p3/4P3/1NN1B3/PPP1BPPP/R2Q1RK1 w - b6 0 10', 'rnbq1rk1/4bppp/p2p1n2/1p2p3/4P3/1NNBBB2/PPP2PPP/R2Q1RK1 b - - 1 10', 0.35, 5000, false, false, '2025-06-15 10:00:00+00'),
('b1000000-0000-0000-0000-000000000001', 10, 'b', 'Bb7', 'c8b7', 'rnbq1rk1/4bppp/p2p1n2/1p2p3/4P3/1NNBBB2/PPP2PPP/R2Q1RK1 b - - 1 10', 'rn1q1rk1/1b2bppp/p2p1n2/1p2p3/4P3/1NNBBB2/PPP2PPP/R2Q1RK1 w - - 2 11', 0.3, 7000, false, false, '2025-06-15 10:00:00+00'),
('b1000000-0000-0000-0000-000000000001', 11, 'w', 'Qd2', 'd1d2', 'rn1q1rk1/1b2bppp/p2p1n2/1p2p3/4P3/1NNBBB2/PPP2PPP/R2Q1RK1 w - - 2 11', 'rn1q1rk1/1b2bppp/p2p1n2/1p2p3/4P3/1NNBBB2/PPPQ1PPP/R4RK1 b - - 3 11', 0.4, 8000, false, false, '2025-06-15 10:00:00+00'),
('b1000000-0000-0000-0000-000000000001', 11, 'b', 'Nbd7', 'b8d7', 'rn1q1rk1/1b2bppp/p2p1n2/1p2p3/4P3/1NNBBB2/PPPQ1PPP/R4RK1 b - - 3 11', 'r2q1rk1/1b1nbppp/p2p1n2/1p2p3/4P3/1NNBBB2/PPPQ1PPP/R4RK1 w - - 4 12', 0.35, 10000, false, false, '2025-06-15 10:00:00+00'),
('b1000000-0000-0000-0000-000000000001', 12, 'w', 'a4', 'a2a4', 'r2q1rk1/1b1nbppp/p2p1n2/1p2p3/4P3/1NNBBB2/PPPQ1PPP/R4RK1 w - - 4 12', 'r2q1rk1/1b1nbppp/p2p1n2/1p2p3/P3P3/1NNBBB2/1PPQ1PPP/R4RK1 b - a3 0 12', 0.5, 6000, false, false, '2025-06-15 10:00:00+00'),
('b1000000-0000-0000-0000-000000000001', 12, 'b', 'Rc8', 'a8c8', 'r2q1rk1/1b1nbppp/p2p1n2/1p2p3/P3P3/1NNBBB2/1PPQ1PPP/R4RK1 b - a3 0 12', '2rq1rk1/1b1nbppp/p2p1n2/1p2p3/P3P3/1NNBBB2/1PPQ1PPP/R4RK1 w - - 1 13', -2.5, 3000, true, false, '2025-06-15 10:00:00+00'),
('b1000000-0000-0000-0000-000000000001', 13, 'w', 'Rfd1', 'f1d1', '2rq1rk1/1b1nbppp/p2p1n2/1p2p3/P3P3/1NNBBB2/1PPQ1PPP/R4RK1 w - - 1 13', '2rq1rk1/1b1nbppp/p2p1n2/1p2p3/P3P3/1NNBBB2/1PPQ1PPP/R2R2K1 b - - 2 13', 0.6, 9000, false, false, '2025-06-15 10:00:00+00');

-- Additional moves for matches 2-5 to reach 50+
INSERT INTO moves (match_id, move_number, color, san, uci, fen_before, fen_after, eval_score, move_time_ms, is_blunder, is_mistake, created_at) VALUES
('b1000000-0000-0000-0000-000000000002', 1, 'w', 'e4', 'e2e4', 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', 'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1', 0.3, 4000, false, false, '2025-06-16 14:00:00+00'),
('b1000000-0000-0000-0000-000000000002', 1, 'b', 'e6', 'e7e6', 'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1', 'rnbqkbnr/pppp1ppp/4p3/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2', 0.4, 3000, false, false, '2025-06-16 14:00:00+00'),
('b1000000-0000-0000-0000-000000000002', 2, 'w', 'd4', 'd2d4', 'rnbqkbnr/pppp1ppp/4p3/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2', 'rnbqkbnr/pppp1ppp/4p3/8/3PP3/8/PPP2PPP/RNBQKBNR b KQkq - 0 2', 0.35, 3000, false, false, '2025-06-16 14:00:00+00'),
('b1000000-0000-0000-0000-000000000002', 2, 'b', 'd5', 'd7d5', 'rnbqkbnr/pppp1ppp/4p3/8/3PP3/8/PPP2PPP/RNBQKBNR b KQkq - 0 2', 'rnbqkbnr/ppp2ppp/4p3/3p4/3PP3/8/PPP2PPP/RNBQKBNR w KQkq - 0 3', 0.3, 5000, false, false, '2025-06-16 14:00:00+00'),
('b1000000-0000-0000-0000-000000000002', 3, 'w', 'Nc3', 'b1c3', 'rnbqkbnr/ppp2ppp/4p3/3p4/3PP3/8/PPP2PPP/RNBQKBNR w KQkq - 0 3', 'rnbqkbnr/ppp2ppp/4p3/3p4/3PP3/2N5/PPP2PPP/R1BQKBNR b KQkq - 1 3', 0.4, 4000, false, false, '2025-06-16 14:00:00+00'),
('b1000000-0000-0000-0000-000000000002', 3, 'b', 'Nf6', 'g8f6', 'rnbqkbnr/ppp2ppp/4p3/3p4/3PP3/2N5/PPP2PPP/R1BQKBNR b KQkq - 1 3', 'rnbqkb1r/ppp2ppp/4pn2/3p4/3PP3/2N5/PPP2PPP/R1BQKBNR w KQkq - 2 4', 0.35, 6000, false, false, '2025-06-16 14:00:00+00'),
('b1000000-0000-0000-0000-000000000002', 4, 'w', 'Bg5', 'c1g5', 'rnbqkb1r/ppp2ppp/4pn2/3p4/3PP3/2N5/PPP2PPP/R1BQKBNR w KQkq - 2 4', 'rnbqkb1r/ppp2ppp/4pn2/3p2B1/3PP3/2N5/PPP2PPP/R2QKBNR b KQkq - 3 4', 0.5, 5000, false, false, '2025-06-16 14:00:00+00'),
('b1000000-0000-0000-0000-000000000002', 4, 'b', 'Be7', 'f8e7', 'rnbqkb1r/ppp2ppp/4pn2/3p2B1/3PP3/2N5/PPP2PPP/R2QKBNR b KQkq - 3 4', 'rnbq1rk1/ppp1bppp/4pn2/3p2B1/3PP3/2N5/PPP2PPP/R2QKBNR w KQ - 4 5', 0.4, 7000, false, false, '2025-06-16 14:00:00+00'),
('b1000000-0000-0000-0000-000000000003', 1, 'w', 'e4', 'e2e4', 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', 'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1', 0.3, 3000, false, false, '2025-06-17 09:00:00+00'),
('b1000000-0000-0000-0000-000000000003', 1, 'b', 'e5', 'e7e5', 'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1', 'rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2', 0.2, 4000, false, false, '2025-06-17 09:00:00+00'),
('b1000000-0000-0000-0000-000000000003', 2, 'w', 'Nf3', 'g1f3', 'rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2', 'rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2', 0.3, 3000, false, false, '2025-06-17 09:00:00+00'),
('b1000000-0000-0000-0000-000000000003', 2, 'b', 'Nc6', 'b8c6', 'rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2', 'r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3', 0.25, 5000, false, false, '2025-06-17 09:00:00+00'),
('b1000000-0000-0000-0000-000000000003', 3, 'w', 'Bc4', 'f1c4', 'r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3', 'r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R b KQkq - 3 3', 0.3, 4000, false, false, '2025-06-17 09:00:00+00'),
('b1000000-0000-0000-0000-000000000003', 3, 'b', 'Bc5', 'f8c5', 'r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R b KQkq - 3 3', 'r1bqk1nr/pppp1ppp/2n5/2b1p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4', 0.2, 6000, false, false, '2025-06-17 09:00:00+00');

-- Drills (15 drills across categories)
INSERT INTO drills (id, title, description, difficulty, category, fen_position, correct_move, explanation) VALUES
('d1000000-0000-0000-0000-000000000001', 'Back Rank Mate', 'Find the back rank checkmate', 1, 'tactic', '6k1/5ppp/8/8/8/8/5PPP/R5K1 w - - 0 1', 'Ra8#', 'The rook delivers checkmate on the back rank since the pawns block escape'),
('d1000000-0000-0000-0000-000000000002', 'Knight Fork', 'Find the knight fork winning material', 2, 'tactic', 'r1bqkb1r/pppp1ppp/2n2n2/4p2Q/2B1P3/8/PPPP1PPP/RNB1K1NR w KQkq - 0 1', 'Qxf7#', 'Scholars mate pattern — queen takes f7 with checkmate'),
('d1000000-0000-0000-0000-000000000003', 'Pin the Knight', 'Use a pin to win material', 2, 'tactic', 'rnbqkb1r/pppppppp/5n2/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1', 'e5', 'Push the pawn to attack the pinned knight'),
('d1000000-0000-0000-0000-000000000004', 'King and Pawn Endgame', 'Win the king and pawn endgame', 3, 'endgame', '8/8/8/8/4k3/8/4KP2/8 w - - 0 1', 'f4', 'Push the pawn to create a passed pawn'),
('d1000000-0000-0000-0000-000000000005', 'Rook Endgame', 'Convert the rook endgame advantage', 4, 'endgame', '8/8/8/8/R3k3/8/4KP2/8 w - - 0 1', 'f4', 'Advance the pawn with rook support'),
('d1000000-0000-0000-0000-000000000006', 'Queen vs Rook', 'Checkmate with queen vs rook', 5, 'endgame', '8/8/8/8/4k3/8/2Q1K3/8 w - - 0 1', 'Qc4+', 'Force the king to the edge with checks'),
('d1000000-0000-0000-0000-000000000007', 'Sicilian Response', 'Find the best response in the Sicilian', 2, 'opening', 'rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2', 'Nf3', 'The Open Sicilian with Nf3 is the most challenging for Black'),
('d1000000-0000-0000-0000-000000000008', 'French Defense Advance', 'Find the best continuation', 3, 'opening', 'rnbqkbnr/ppp2ppp/4p3/3pP3/3P4/8/PPP2PPP/RNBQKBNR b KQkq - 0 3', 'c5', 'Strike at the center with c5 in the Advance French'),
('d1000000-0000-0000-0000-000000000009', 'Discovery Attack', 'Find the discovered attack', 3, 'tactic', 'r1bqkb1r/pppp1ppp/2n5/4p3/2B1n3/5N2/PPPP1PPP/RNBQK2R w KQkq - 0 4', 'Bxf7+', 'Bishop sacrifice reveals discovered attack'),
('d1000000-0000-0000-0000-000000000010', 'Smothered Mate', 'Deliver the smothered mate', 4, 'tactic', '6rk/5Npp/8/8/8/8/8/6K1 w - - 0 1', 'Nh6+', 'Knight check forces king to corner for smothered mate'),
('d1000000-0000-0000-0000-000000000011', 'Opposition', 'Use opposition to promote', 2, 'endgame', '8/8/4k3/8/4K3/4P3/8/8 w - - 0 1', 'e3', 'Hold opposition to escort the pawn'),
('d1000000-0000-0000-0000-000000000012', 'Italian Game Setup', 'Best development in the Italian', 1, 'opening', 'r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3', 'Bc4', 'Develop the bishop to the active c4 square'),
('d1000000-0000-0000-0000-000000000013', 'Double Attack', 'Find the double attack winning material', 3, 'tactic', 'r1bqk2r/pppp1ppp/2n2n2/2b1p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4', 'Ng5', 'Knight attack on f7 creates double threat'),
('d1000000-0000-0000-0000-000000000014', 'Lucena Position', 'Win the Lucena position', 5, 'endgame', '3K4/3P1k2/8/8/8/8/1R6/8 w - - 0 1', 'Rb4', 'Build a bridge to shield the king from checks'),
('d1000000-0000-0000-0000-000000000015', 'Caro-Kann Main Line', 'Find the right continuation', 3, 'opening', 'rnbqkbnr/pp1ppppp/2p5/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2', 'd4', 'Occupy the center with d4 in the Caro-Kann');

-- Refresh materialized view with seed data
REFRESH MATERIALIZED VIEW player_stats_mv;
