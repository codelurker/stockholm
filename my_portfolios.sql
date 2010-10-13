TRUNCATE TABLE portfolio;
INSERT INTO portfolio VALUES 
(1, 'Avanza', 'SEK'),
(2, 'Avanza IPS', 'SEK'),
(3, 'XO', 'GBP')
;

TRUNCATE TABLE position;
INSERT INTO position VALUES 
-- ('FUNDS',      'SEK', 1, '2000-01-01',         null,      1,    null,   0,    0, 20258.08,     1),
-- ('CASH',       'SEK', 1, '2000-01-01',         null,      1,    null,   0,    0, 22712.88,     1),
('MIC-SDB.ST', 'SEK', 1, '2010-09-09', '2010-09-29', 719.50,   647.0,  99,   99,       30, 1),
('LUPE.ST',    'SEK', 1, '2010-09-28',         null,     55,    null,  99, null,     2400, 1),
('AAPL',       'USD', 1, '2010-07-06',         null, 259.98,    null, 109, null,       15, 1),
('AXIS.ST',    'SEK', 1, '2010-09-22',         null,     92,    null,  99, null,      450, 1),
('BOL.ST',     'SEK', 1, '2010-09-14',         null,     97.5,  null,  99, null,      250, 1)
;
-- ('ERIC-A.ST',     'SEK', 1, '2010-09-14',         null,     97.5,  null,  99, null,      250, 1),
-- ('KARO.ST',     'SEK', 1, '2010-09-14',         null,     97.5,  null,  99, null,      250, 1)
INSERT INTO position VALUES 
-- ( 'FUNDS',      'SEK', 1, '2000-01-01',         null,      1,    null,   0,    0,  2508.50, 2),
-- ('CASH',       'SEK', 1, '2000-01-01',         null,      1,    null,   0,    0, 17747.97, 2),
-- ('HOLM-B.ST',  'SEK', 1, '2010-09-09',         null, 217.00,    null,  99, null,       25, 2),
('HMB.ST',     'SEK', 1, '2010-09-02',         null, 247.10,    null,  99, null,      40,  2),
('LUPE.ST',    'SEK', 1, '2010-07-23',         null,     40,    null,  99, null,      130, 2),
('TLSN.ST',    'SEK', 1, '2010-07-23',         null,  53.65,    null,  99, null,      100, 2),
('TEL2-A.ST',  'SEK', 1, '2010-07-19',         null,  129.0,    null,  99, null,       40, 2)
;
INSERT INTO position VALUES 
('AGLD.L',     'GBP', 1, '2010-09-10',         null,  26.91,    null,  0, null,      20.00, 3),
('AGLD.L',     'GBP', 1, '2010-10-07',         null,  31.50,    null,  5.95, null,   15.68, 3)
-- one day offse
;
