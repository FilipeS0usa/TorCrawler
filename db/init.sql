CREATE EXTENSION IF NOT EXISTS dblink;

-- Create the database (no IF NOT EXISTS for databases in PostgreSQL)
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'crawler_db') THEN
        PERFORM dblink_exec('dbname=postgres', 'CREATE DATABASE crawler_db');
    END IF;
END $$;

-- Switch to the new database (PostgreSQL doesn't use `USE`, you need to connect manually)
\connect crawler_db

-- Create tables
CREATE TABLE IF NOT EXISTS hash (
    id SERIAL PRIMARY KEY,
    hash VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS domain (
    id SERIAL PRIMARY KEY,
    domain TEXT NOT NULL,
    date_last_scan TIMESTAMP
);

CREATE TABLE IF NOT EXISTS link (
    id SERIAL PRIMARY KEY,
    link TEXT NOT NULL,
    date_last_scan TIMESTAMP,
    date_discovery TIMESTAMP NOT NULL,
    disabled BOOLEAN NOT NULL,
    tries INT NOT NULL,
    large BOOLEAN NOT NULL,
    idDomain INT NOT NULL,
    FOREIGN KEY (idDomain)
    REFERENCES domain (id)
    ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS file (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    original_name TEXT NOT NULL,
    type_of_file VARCHAR(50) NOT NULL,
    date_of_discovery TIMESTAMP NOT NULL,
    link TEXT NOT NULL,
    idDomain INT NOT NULL,
    FOREIGN KEY (idDomain)
    REFERENCES domain (id)
    ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS large_link (
    id SERIAL PRIMARY KEY,
    link TEXT NOT NULL,
    header TEXT NOT NULL,
    idDomain INT NOT NULL,
    FOREIGN KEY (idDomain)
    REFERENCES domain (id)
    ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS link_hash (
    id SERIAL PRIMARY KEY,
    date TIMESTAMP NOT NULL,
    idLink INT NOT NULL,
    idHash INT NOT NULL,
    FOREIGN KEY (idLink)
    REFERENCES link (id)
    ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (idHash)
    REFERENCES hash (id)
    ON UPDATE CASCADE ON DELETE CASCADE
);
