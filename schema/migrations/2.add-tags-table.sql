CREATE TABLE tags (
    id CHAR(64) NOT NULL,
    name VARCHAR(255) NOT NULL,
    creation_time BIGINT UNSIGNED NOT NULL,
    PRIMARY KEY(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- used to search tags
ALTER TABLE tags ADD INDEX name (name);
