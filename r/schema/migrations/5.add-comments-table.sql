CREATE TABLE comments (
    id CHAR(12) NOT NULL,
    user_id CHAR(12) NOT NULL,
    file_id CHAR(12) NOT NULL,
    line MEDIUMINT UNSIGNED NOT NULL,
    contents TEXT,
    creation_time BIGINT UNSIGNED NOT NULL,
    PRIMARY KEY(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- used to get all of the comments for a file (where files have an upload_id)
ALTER TABLE comments ADD INDEX file_id (file_id);

-- used to get all of the comments by a user
ALTER TABLE comments ADD INDEX user_id (user_id, creation_time);
