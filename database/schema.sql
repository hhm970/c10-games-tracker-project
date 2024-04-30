-- This file contains table definitions for the database.


DROP TABLE website CASCADE;
DROP TABLE publisher CASCADE;
DROP TABLE developer CASCADE;
DROP TABLE platform CASCADE;
DROP TABLE tag CASCADE;
DROP TABLE game CASCADE;
DROP TABLE platform_assignment CASCADE;
DROP TABLE game_tag_matching CASCADE;
DROP TABLE subscriber




CREATE TABLE subscriber (
    subscriber_id INT GENERATED ALWAYS AS IDENTITY,
    first_name VARCHAR(20) UNIQUE NOT NULL,
    last_name VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    PRIMARY KEY (subscriber_id)
);

CREATE TABLE website (
    website_id INT GENERATED ALWAYS AS IDENTITY,
    website_name VARCHAR(20) UNIQUE NOT NULL,
    PRIMARY KEY (website_id)
);


CREATE TABLE publisher (
    publisher_id INT GENERATED ALWAYS AS IDENTITY,
    publisher_name TEXT NOT NULL,
    PRIMARY KEY (publisher_id)
);


CREATE TABLE developer (
    developer_id INT GENERATED ALWAYS AS IDENTITY,
    developer_name TEXT NOT NULL,
    PRIMARY KEY (developer_id)
);



CREATE TABLE platform (
    platform_id INT GENERATED ALWAYS AS IDENTITY,
    platform_name VARCHAR(30) UNIQUE NOT NULL,
    PRIMARY KEY (platform_id)
);


CREATE TABLE tag (
    tag_id INT GENERATED ALWAYS AS IDENTITY,
    tag_name VARCHAR(30) UNIQUE NOT NULL,
    PRIMARY KEY (tag_id)
);



CREATE TABLE game (
    game_id INT GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price FLOAT NOT NULL,
    developer_id INT,
    publisher_id INT,
    release_date DATE NOT NULL,
    rating FLOAT,
    website_id INT NOT NULL,
    PRIMARY KEY (game_id),
    FOREIGN KEY(website_id) REFERENCES website(website_id),
    FOREIGN KEY(developer_id) REFERENCES developer(developer_id),
    FOREIGN KEY(publisher_id) REFERENCES publisher(publisher_id)
);

CREATE TABLE platform_assignment (
    assignment_id INT GENERATED ALWAYS AS IDENTITY,
    platform_id INT NOT NULL,
    game_id INT NOT NULL,
    PRIMARY KEY (assignment_id),
    FOREIGN KEY(platform_id) REFERENCES platform(platform_id),
    FOREIGN KEY(game_id) REFERENCES game(game_id)
);

CREATE TABLE game_tag_matching (
    matching_id INT GENERATED ALWAYS AS IDENTITY,
    game_id INT NOT NULL,
    tag_id INT NOT NULL,
    PRIMARY KEY (matching_id),
    FOREIGN KEY(game_id) REFERENCES game(game_id),
    FOREIGN KEY(tag_id) REFERENCES tag(tag_id)
);



INSERT INTO website (website_name)
VALUES ('Steam'),('GOG'),('Epic');

INSERT INTO platform (platform_name)
VALUES ('Windows'),('macOS'),('Linux');

INSERT INTO subscriber (first_name, last_name, email)
VALUES ('Shindy', 'Manic', 'trainee.setinder.manic@sigmalabs.co.uk');

