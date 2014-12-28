CREATE TABLE comments (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    user_id BIGINT UNSIGNED NOT NULL,
    file_id BIGINT UNSIGNED NOT NULL,
    line MEDIUMINT UNSIGNED NOT NULL,
    contents MEDIUMTEXT,
    PRIMARY KEY(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- used to get all of the comments for a file (where files have an upload_id)
ALTER TABLE comments ADD INDEX file_id (file_id);

-- used to get all of the comments by a user
ALTER TABLE comments ADD INDEX user_id (user_id);
