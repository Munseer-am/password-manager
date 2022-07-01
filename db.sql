.open db.sqlite3

CREATE TABLE IF NOT EXISTS PASSWORDS (
	Application VARCHAR(100),
	Username VARCHAR(100),
	Email VARCHAR(100),
	Password VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS LOG (
	Application VARCHAR(100),
	Time VARCHAR(100),
	Script VARCHAR(200)
);

CREATE TABLE IF NOT EXISTS Key (
	Key VARCHAR(100)
);

