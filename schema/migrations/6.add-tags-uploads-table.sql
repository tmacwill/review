CREATE TABLE tags_uploads (
    id CHAR(64) NOT NULL,
    tag_id CHAR(64) NOT NULL,
    upload_id CHAR(64) NOT NULL,
    creation_time BIGINT UNSIGNED NOT NULL,
    PRIMARY KEY(id)
) ENGINE InnoDB DEFAULT CHARSET=utf8;

-- used to get uploads with a tag
ALTER TABLE tags_uploads ADD INDEX tag_id (tag_id, creation_time);

-- used to get tags on an upload
ALTER TABLE tags_uploads ADD INDEX upload_id (upload_id);
