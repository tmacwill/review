CREATE TABLE files (
    id CHAR(64) NOT NULL,
    upload_id CHAR(64) NOT NULL,
    filename VARCHAR(255) NOT NULL,
    contents MEDIUMTEXT,
    line_count INT UNSIGNED NOT NULL,
    creation_time BIGINT UNSIGNED NOT NULL,
    PRIMARY KEY(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- used to get all the files in an upload
ALTER TABLE files ADD INDEX upload_id (upload_id);
