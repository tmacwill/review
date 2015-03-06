CREATE TABLE uploads (
    id CHAR(64) NOT NULL,
    user_id CHAR(64) NOT NULL,
    name VARCHAR(255) NOT NULL,
    slug CHAR(64) NOT NULL,
    description TEXT NOT NULL,
    creation_time BIGINT UNSIGNED NOT NULL,
    PRIMARY KEY(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- used to get all the uploads by a user
ALTER TABLE uploads ADD INDEX user_id (user_id);
