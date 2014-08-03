CREATE TABLE review_files (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    review_id BIGINT UNSIGNED NOT NULL,
    contents MEDIUMTEXT,
    creation_time BIGINT UNSIGNED NOT NULL,
    PRIMARY KEY(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE review_files ADD INDEX review_id (review_id);
