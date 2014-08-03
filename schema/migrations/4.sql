CREATE TABLE submission_files (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    submission_id BIGINT UNSIGNED NOT NULL,
    filename VARCHAR(255) NOT NULL,
    contents MEDIUMTEXT,
    creation_time BIGINT UNSIGNED NOT NULL,
    PRIMARY KEY(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE submission_files ADD INDEX submission_id (submission_id);
