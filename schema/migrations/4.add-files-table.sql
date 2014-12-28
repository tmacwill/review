CREATE TABLE files (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    upload_id BIGINT UNSIGNED NOT NULL,
    filename VARCHAR(255) NOT NULL,
    contents MEDIUMTEXT,
    PRIMARY KEY(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- used to get all the files in an upload
ALTER TABLE files ADD INDEX upload_id (upload_id);
