CREATE TABLE IF NOT EXISTS users (
  id integer PRIMARY KEY autoincrement,
  login varchar(50) NOT NULL,
  password varchar(30) NOT NULL,
  firstName varchar(80) NOT NULL,
  lastName varchar(20) NOT NULL,
  status integer NOT NULL DEFAULT 1,
  created TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '-3 hours')),
  modified TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '-3 hours'))
);