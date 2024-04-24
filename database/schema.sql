-- This file contains table definitions for the database.


DROP TABLE website CASCADE;
DROP TABLE platform CASCADE;
DROP TABLE subscriber CASCADE;
DROP TABLE tag CASCADE;
DROP TABLE subscriber_tag_subscription CASCADE;
DROP TABLE game CASCADE;
DROP TABLE platform_assignment CASCADE;
DROP TABLE game_tag_matching CASCADE;




CREATE TABLE website (
    website_id INT GENERATED ALWAYS AS IDENTITY,
    website_name VARCHAR(20) UNIQUE NOT NULL,
    PRIMARY KEY (website_id)
);



CREATE TABLE platform (
    platform_id INT GENERATED ALWAYS AS IDENTITY,
    platform_name VARCHAR(30) UNIQUE NOT NULL,
    PRIMARY KEY (platform_id)
);

CREATE TABLE subscriber (
    subscriber_id INT GENERATED ALWAYS AS IDENTITY,
    first_name VARCHAR(15) NOT NULL,
    last_name VARCHAR(15) NOT NULL,
    email VARCHAR(100) NOT NULL,
    PRIMARY KEY (subscriber_id)
);


CREATE TABLE tag (
    tag_id INT GENERATED ALWAYS AS IDENTITY,
    tag_name VARCHAR(30) UNIQUE NOT NULL,
    PRIMARY KEY (tag_id)
);


CREATE TABLE subscriber_tag_subscription (
    subscription_id INT GENERATED ALWAYS AS IDENTITY,
    subscriber_id INT NOT NULL,
    tag_id INT NOT NULL,
    PRIMARY KEY (subscription_id),
    FOREIGN KEY(subscriber_id) REFERENCES subscriber(subscriber_id),
    FOREIGN KEY(tag_id) REFERENCES tag(tag_id)
);

CREATE TABLE game (
    game_id INT GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price FLOAT NOT NULL,
    developer VARCHAR(40) NOT NULL,
    publisher VARCHAR(40),
    release_date DATE NOT NULL,
    rating SMALLINT,
    website_id INT NOT NULL,
    PRIMARY KEY (game_id),
    FOREIGN KEY(website_id) REFERENCES website(website_id)
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


INSERT INTO subscriber (first_name, last_name, email)
VALUES ('Annalise', 'Verzijl', 'trainee.annalise.verzijl@sigmalabs.co.uk');

INSERT INTO website (website_name)
VALUES ('Steam'),('GOG'),('Epic');

