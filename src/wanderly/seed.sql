-- --------------------------
-- Trips
-- --------------------------
INSERT INTO trips(destination, depart_date, return_date, user_id) VALUES
('Iceland 2026', '2026-02-15', '2026-03-10', 1),
('Japan 2025', '2025-11-01', '2025-11-15', 1),
('Italy 2025', '2025-06-10', '2025-06-25', 1),
('Canada 2025', '2025-07-05', '2025-07-20', 1),
('Australia 2026', '2026-01-10', '2026-01-25', 1),
('France 2025', '2025-09-12', '2025-09-20', 1),
('Thailand 2025', '2025-12-01', '2025-12-15', 1),
('Greece 2026', '2026-04-05', '2026-04-20', 1),
('Peru 2025', '2025-08-01', '2025-08-15', 1),
('Spain 2026', '2026-05-10', '2026-05-25', 1);

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

-- --------------------------
-- Plans for Trip 3: Italy 2025 (4 rows)
-- --------------------------
INSERT INTO plans(at_date, at_time, activity, note, cost, trip_id) VALUES
('2025-06-10', '09:00AM', 'Arrive in Rome', NULL, 0, 3),
('2025-06-11', '10:00AM', 'Colosseum Tour', NULL, 25, 3),
('2025-06-12', '11:30AM', 'Lunch', 'Trattoria Roma', 35, 3),
('2025-06-15', '09:00AM', 'Vatican Museum', NULL, 30, 3);

-- --------------------------
-- Plans for Trip 4: Canada 2025 (5 rows)
-- --------------------------
INSERT INTO plans(at_date, at_time, activity, note, cost, trip_id) VALUES
('2025-07-05', '10:00AM', 'Arrive in Toronto', NULL, 0, 4),
('2025-07-06', '09:00AM', 'CN Tower Visit', NULL, 35, 4),
('2025-07-06', '01:00PM', 'Lunch', 'Downtown Bistro', 40, 4),
('2025-07-08', '08:00AM', 'Niagara Falls Tour', NULL, 60, 4),
('2025-07-09', '11:00AM', 'Visit Royal Ontario Museum', NULL, 20, 4);

-- --------------------------
-- Plans for Trip 5: Australia 2026 (7 rows)
-- --------------------------
INSERT INTO plans(at_date, at_time, activity, note, cost, trip_id) VALUES
('2026-01-10', '09:00AM', 'Arrive in Sydney', NULL, 0, 5),
('2026-01-11', '10:00AM', 'Sydney Opera House', NULL, 50, 5),
('2026-01-11', '01:00PM', 'Lunch', 'Harbour Cafe', 35, 5),
('2026-01-12', '09:00AM', 'Bondi Beach', NULL, 0, 5),
('2026-01-13', '08:30AM', 'Blue Mountains Tour', NULL, 70, 5),
('2026-01-14', '12:00PM', 'Lunch', 'Mountain View Restaurant', 40, 5),
('2026-01-15', '10:00AM', 'Wildlife Sanctuary', NULL, 20, 5);

-- --------------------------
-- Plans for Trip 6: France 2025 (3 rows)
-- --------------------------
INSERT INTO plans(at_date, at_time, activity, note, cost, trip_id) VALUES
('2025-09-12', '09:00AM', 'Arrive in Paris', NULL, 0, 6),
('2025-09-13', '10:00AM', 'Louvre Museum', NULL, 25, 6),
('2025-09-14', '01:00PM', 'Lunch', 'Cafe de Paris', 30, 6);

-- --------------------------
-- Plans for Trip 7: Thailand 2025 (10 rows)
-- --------------------------
INSERT INTO plans(at_date, at_time, activity, note, cost, trip_id) VALUES
('2025-12-01', '08:00AM', 'Arrive in Bangkok', NULL, 0, 7),
('2025-12-02', '09:00AM', 'Grand Palace', NULL, 20, 7),
('2025-12-02', '12:00PM', 'Lunch', 'Riverside Cafe', 15, 7),
('2025-12-03', '10:00AM', 'Floating Market', NULL, 25, 7),
('2025-12-04', '09:00AM', 'Ayutthaya Day Trip', NULL, 50, 7),
('2025-12-05', '11:00AM', 'Thai Cooking Class', NULL, 40, 7),
('2025-12-06', '08:00AM', 'Temple Tour', NULL, 20, 7),
('2025-12-07', '12:00PM', 'Lunch', 'Local Street Food', 10, 7),
('2025-12-08', '10:00AM', 'Beach Day', NULL, 0, 7),
('2025-12-09', '08:00AM', 'Massage & Spa', NULL, 60, 7);

-- --------------------------
-- Plans for Trip 8: Greece 2026 (3 rows)
-- --------------------------
INSERT INTO plans(at_date, at_time, activity, note, cost, trip_id) VALUES
('2026-04-05', '09:00AM', 'Arrive in Athens', NULL, 0, 8),
('2026-04-06', '10:00AM', 'Acropolis Tour', NULL, 30, 8),
('2026-04-07', '01:00PM', 'Lunch', 'Greek Tavern', 25, 8);

-- --------------------------
-- Plans for Trip 9: Peru 2025 (15 rows)
-- --------------------------
INSERT INTO plans(at_date, at_time, activity, note, cost, trip_id) VALUES
('2025-08-01', '09:00AM', 'Arrive in Lima', NULL, 0, 9),
('2025-08-02', '10:00AM', 'City Tour', NULL, 20, 9),
('2025-08-03', '08:00AM', 'Flight to Cusco', NULL, 50, 9),
('2025-08-04', '09:00AM', 'Machu Picchu Tour', NULL, 100, 9),
('2025-08-05', '10:00AM', 'Sacred Valley Tour', NULL, 80, 9),
('2025-08-06', '11:00AM', 'Free Day', NULL, 0, 9),
('2025-08-06', '01:00PM', 'Lunch', 'Local Cafe', 15, 9),
('2025-08-07', '09:00AM', 'Hike Rainbow Mountain', NULL, 50, 9),
('2025-08-08', '10:00AM', 'Market Visit', NULL, 20, 9),
('2025-08-09', '11:00AM', 'Flight to Lima', NULL, 50, 9),
('2025-08-10', '09:00AM', 'Beach Day', NULL, 0, 9),
('2025-08-11', '12:00PM', 'Lunch', 'Seafood Spot', 30, 9);