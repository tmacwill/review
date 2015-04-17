CREATE TABLE notifications (
    id CHAR(12) NOT NULL,
    user_id CHAR(12) NOT NULL,
    from_user_id CHAR(12) NOT NULL,
    notification_type INT UNSIGNED NOT NULL,
    is_read SMALLINT UNSIGNED NOT NULL DEFAULT 0,
    metadata TINYTEXT NOT NULL,
    creation_time BIGINT UNSIGNED NOT NULL,
    PRIMARY KEY(id)
) ENGINE InnoDB DEFAULT CHARSET=utf8;

-- used to get notifications for a user
ALTER TABLE notifications ADD INDEX user_id (user_id, creation_time);

-- used to query notifications between users
ALTER TABLE notifications ADD INDEX user_id_from_user_id (user_id, from_user_id, notification_type, creation_time);
