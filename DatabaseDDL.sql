-- Operational Store
CREATE DATABASE faceit_analytics_operations;

CREATE TABLE clients
(
    client_id INT GENERATED ALWAYS AS IDENTITY UNIQUE,
    CONSTRAINT clients_pk PRIMARY KEY (client_id),
    player_id INT NOT NULL,
    faceit_url VARCHAR(200),
    nickname VARCHAR(500),
    country VARCHAR(500)
);

CREATE TABLE download_types
(
    download_type_id INT GENERATED ALWAYS AS IDENTITY UNIQUE,
    name VARCHAR(200) NOT NULL,
    date_added DATE DEFAULT current_date
);

CREATE TABLE client_downloads
(
    client_download_id INT GENERATED ALWAYS AS IDENTITY UNIQUE,
    client_id INT,
    CONSTRAINT client_downloads_client_id_fkey FOREIGN KEY (client_id) REFERENCES clients (client_id),
    download_type_id INT REFERENCES download_types(download_type_id), -- trying out PostgreSQL Automatic Foreign key naming
    download_start_dt TIMESTAMP,
    download_end_dt TIMESTAMP,
    is_download_successful BOOLEAN
);
