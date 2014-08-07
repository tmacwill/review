CREATE TABLE upload_files (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    upload_id BIGINT UNSIGNED NOT NULL,
    filename VARCHAR(255) NOT NULL,
    contents MEDIUMTEXT,
    PRIMARY KEY(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE upload_files ADD INDEX upload_id (upload_id);
