CREATE TABLE IF NOT EXISTS users (
  id integer PRIMARY KEY autoincrement,
  login varchar(50) NOT NULL,
  password varchar(100) NOT NULL,
  firstName varchar(80) NOT NULL,
  lastName varchar(20) NOT NULL,
  status integer NOT NULL DEFAULT 1,
  userType integer NOT NULL DEFAULT 0,
  created TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '-3 hours')),
  modified TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '-3 hours'))
);

CREATE TABLE IF NOT EXISTS musics (
  id integer PRIMARY KEY autoincrement,
  title varchar(50) NOT NULL,
  artist varchar(50) NOT NULL,
  genre varchar(50) NOT NULL,
  created TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '-3 hours')),
  modified TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '-3 hours'))
);

INSERT INTO musics (title, artist, genre, created, modified) VALUES
('The Trooper', 'Iron Maiden', 'Heavy Metal', '2024-09-20 20:16:31', '2024-10-27 13:19:19'),
('Fear of the Dark', 'Iron Maiden', 'Heavy Metal', '2024-09-20 20:46:01', '2024-10-11 19:58:08'),
('The Number of the Beast', 'Iron Maiden', 'Heavy Metal', '2024-09-21 22:36:19', '2024-09-21 22:37:13'),
('Hallowed Be Thy Name', 'Iron Maiden', 'Heavy Metal', '2024-09-21 22:39:24', '2024-09-21 22:39:24'),
('Aces High', 'Iron Maiden', 'Heavy Metal', '2024-09-22 00:15:33', '2024-09-22 00:15:43'),
('Run to the Hills', 'Iron Maiden', 'Heavy Metal', '2024-10-26 15:42:01', '2024-10-28 19:04:57');

INSERT INTO users (login, password, firstName, lastName, status, userType, created, modified) VALUES
('nicolascontegt@gmail.com', '$2b$12$JLmtyCC4Szh9o.cbPqAfT..GxVRB.QhMHWhOG5DLUzv5dTL3X8BKq', 'Nicolas Gustavo', 'Conte', 1, 1, '2024-09-20 20:16:31', '2024-10-27 13:19:19'),
('nathan@gmail.com', '$2b$12$yu42uc88fp.E.a0CIq2.wu6z35waqKtG5hNRa2xdAajJtIz6eJzn2', 'Nathan', 'Cielusinski', 1, 0, '2024-09-20 20:46:01', '2024-10-11 19:58:08'),
('HigorAzevedo@hotmail.com', '$2b$12$HZFY/Y4XFBMiL2JlODuWGuRR76ASJ1j2ABuzdeginNwSBXOjuXxFa', 'Higor', 'Azevedo', 0, 0, '2024-09-21 22:36:19', '2024-09-21 22:37:13'),
('Martim@diertelle.com', '$2b$12$GYMHyFdNELaCsjDOnen4wODSH.x3VgtoqVogOd1yITg0wXUCrk81S', 'Martim', 'Diertelle', 1, 0, '2024-09-21 22:39:24', '2024-09-21 22:39:24'),
('Renan@outlook.com', '$2b$12$ilVAXeIV.Kezw1KoCLGHVeBR9tUMixEWQS.0YHbptb5mTvx8H3DNO', 'Renan', 'Calheiros', 0, 0, '2024-09-22 00:15:33', '2024-09-22 00:15:43'),
('nicolasgustavogt@gmail.com', '$2b$12$ULCsh6hVcEUysYSFtK0ZzeyxZ9wmKcu6ud6pbv8FBcoZBqYRng48m', 'Nicolas Gustavo', 'Conte', 2, 0, '2024-10-26 15:42:01', '2024-10-28 19:04:57');