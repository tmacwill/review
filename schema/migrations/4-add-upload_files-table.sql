CREATE TABLE upload_files (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    upload_id BIGINT UNSIGNED NOT NULL,
    filename VARCHAR(255) NOT NULL,
    contents MEDIUMTEXT,
    creation_time BIGINT UNSIGNED NOT NULL,
    PRIMARY KEY(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE uploads ADD INDEX upload_id (upload_id);
