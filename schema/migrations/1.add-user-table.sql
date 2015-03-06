CREATE TABLE users (
    id CHAR(64) NOT NULL,
    username VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password CHAR(66) NOT NULL,
    api CHAR(64) NOT NULL,
    photo_url VARCHAR(255) NOT NULL,
    bio TINYTEXT,
    creation_time BIGINT UNSIGNED NOT NULL,
    PRIMARY KEY(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- used to get the user associated with an email
ALTER TABLE users ADD UNIQUE INDEX email (email);

-- used to get the user associated with an email
ALTER TABLE users ADD UNIQUE INDEX username (username);
