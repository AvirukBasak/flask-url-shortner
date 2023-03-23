CREATE TABLE urldb (
    id INTEGER PRIMARY KEY,
    username VARCHAR(9) NOT NULL,
    original_url TEXT NOT NULL UNIQUE,
    short_key TEXT NOT NULL UNIQUE
);
