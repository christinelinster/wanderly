
-- Trips

INSERT INTO trips(destination, depart_date, return_date, user_id) VALUES
('Iceland 2026', '2026-02-15', '2026-03-10', 1),
('Japan 2025', '2025-11-01', '2025-11-15', 1);

-- --------------------------
-- Plans for Trip 1: Iceland 2026 (6 rows)
-- --------------------------
INSERT INTO plans(at_date, at_time, activity, note, cost, trip_id) VALUES
('2026-02-15', '08:00AM', 'Arrive in Reykjavik', NULL, 0, 1),
('2026-02-16', '10:00AM', 'Golden Circle Tour', NULL, 150, 1),
('2026-02-16', '06:00PM', 'Dinner', 'Seafood Restaurant', 120, 1),
('2026-02-18', '09:00AM', 'Hike in Landmannalaugar', NULL, 0, 1),
('2026-02-20', '11:00AM', 'Visit Blue Lagoon', NULL, 80, 1),
('2026-02-25', '12:00PM', 'Lunch', 'Meatbowl Restaurant', 30, 1);

-- --------------------------
-- Plans for Trip 2: Japan 2025 (8 rows)
-- --------------------------
INSERT INTO plans(at_date, at_time, activity, note, cost, trip_id) VALUES
('2025-11-01', '09:00AM', 'Arrive in Tokyo', NULL, 0, 2),
('2025-11-02', '10:30AM', 'Visit Senso-ji Temple', NULL, 15, 2),
('2025-11-02', '01:00PM', 'Lunch', 'Sushi Place', 40, 2),
('2025-11-03', '09:00AM', 'Day trip to Nikko', NULL, 50, 2),
('2025-11-05', '07:00PM', 'Dinner', 'Ramen Alley', 25, 2),
('2025-11-07', '11:00AM', 'Shibuya Crossing & Shopping', NULL, 0, 2),
('2025-11-07', '02:00PM', 'Lunch', 'Cafe Tokyo', 20, 2),
('2025-11-10', '08:00AM', 'Bullet Train to Kyoto', NULL, 120, 2);
