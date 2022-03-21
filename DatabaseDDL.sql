-- Operational Store
-- CREATE DATABASE faceit_analytics_operations;

CREATE TABLE countries
(
    country_id INT GENERATED ALWAYS AS IDENTITY UNIQUE,
    CONSTRAINT countries_pk PRIMARY KEY (country_id),
    name       VARCHAR(500) NOT NULL,
    code       VARCHAR(50)  NOT NULL,
    date_added DATE DEFAULT CURRENT_DATE
);

CREATE TABLE regions
(
    region_id  INT GENERATED ALWAYS AS IDENTITY UNIQUE,
    CONSTRAINT regions_pk PRIMARY KEY (region_id),
    name       VARCHAR(500) NOT NULL UNIQUE,
    date_added DATE DEFAULT CURRENT_DATE
);

CREATE UNIQUE INDEX countries_name_key ON countries (name);

CREATE TABLE games
(
    game_id    INT GENERATED ALWAYS AS IDENTITY UNIQUE,
    CONSTRAINT games_pk PRIMARY KEY (game_id),
    name       VARCHAR(500) NOT NULL,
    date_added DATE DEFAULT CURRENT_DATE
);

CREATE UNIQUE INDEX games_name_key ON games (name);

CREATE TABLE clients
(
    client_id    INT GENERATED ALWAYS AS IDENTITY UNIQUE,
    CONSTRAINT clients_pk PRIMARY KEY (client_id),
    player_id    INT          NOT NULL,
    country_id   INT,
    CONSTRAINT clients_country_id_fkey FOREIGN KEY (country_id) REFERENCES countries (country_id),
    faceit_url   VARCHAR(200) NOT NULL,
    nickname     VARCHAR(500) NOT NULL,
    date_added   DATE DEFAULT CURRENT_DATE,
    date_deleted DATE
);

CREATE UNIQUE INDEX clients_player_id_key ON clients (player_id);

CREATE TABLE client_game_region
(
    client_game_region_id INT GENERATED ALWAYS AS IDENTITY UNIQUE,
    CONSTRAINT client_game_region_pk PRIMARY KEY (client_game_region_id),
    client_id             INT     NOT NULL,
    CONSTRAINT client_game_region_client_id_fkey FOREIGN KEY (client_id) REFERENCES clients (client_id),
    game_id               INT     NOT NULL,
    CONSTRAINT client_game_region_game_id_fkey FOREIGN KEY (game_id) REFERENCES games (game_id),
    region_id             INT,
    CONSTRAINT client_game_region_region_id_fkey FOREIGN KEY (region_id) REFERENCES regions (region_id),
    download_flag         BOOLEAN NOT NULL DEFAULT true
);

CREATE UNIQUE INDEX client_game_region_client_id_game_id_region_id_key ON client_game_region (client_id, game_id, region_id);

CREATE TABLE download_types
(
    download_type_id INT GENERATED ALWAYS AS IDENTITY UNIQUE,
    name             VARCHAR(200) NOT NULL,
    date_added       DATE DEFAULT current_date
);

CREATE UNIQUE INDEX download_types_name_key ON download_types (name);

CREATE TABLE client_downloads
(
    client_download_id     INT GENERATED ALWAYS AS IDENTITY UNIQUE,
    client_id              INT,
    CONSTRAINT client_downloads_client_id_fkey FOREIGN KEY (client_id) REFERENCES clients (client_id),
    game_id                INT,
    CONSTRAINT client_downloads_game_id_fkey FOREIGN KEY (game_id) REFERENCES games (game_id),
    download_type_id       INT REFERENCES download_types (download_type_id), -- trying out PostgreSQL Automatic Foreign key naming
    download_start_dt      TIMESTAMP,
    download_end_dt        TIMESTAMP,
    is_download_successful BOOLEAN
);

-- Insert myself for testing
INSERT INTO countries (name, code)
VALUES ('Kyrgyzstan', 'kg');

INSERT INTO regions (name)
VALUES ('EU');

INSERT INTO games(name)
VALUES ('csgo');

INSERT INTO download_types(name)
VALUES ('matches');

-- INSERT INTO clients(player_id, country_id, faceit_url, nickname)
-- VALUES ({insert_player_id}, 1, 'https://www.faceit.com/{lang}/players/{insert_nickname}', '{insert_nickname}');

INSERT INTO client_game_region(client_id, game_id, region_id) VALUES (1,1,1)