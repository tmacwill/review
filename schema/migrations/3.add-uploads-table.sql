CREATE TABLE uploads (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    user_id BIGINT UNSIGNED NOT NULL,
    name VARCHAR(255) NOT NULL,
    slug CHAR(64) NOT NULL,
    creation_time BIGINT UNSIGNED NOT NULL,
    PRIMARY KEY(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- used to get all the uploads by a user
ALTER TABLE uploads ADD INDEX user_id (user_id);
