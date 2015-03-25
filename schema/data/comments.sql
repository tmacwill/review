INSERT INTO comments
    (id, user_id, file_id, line, contents, creation_time)
VALUES
    ('e3cd9a427e0f4b7bb7bf236f88e35f2', '57f64113e5b64610bc8a5d0809ad027', '1cc34f0add5347efb228a045e86a16b', 1, 'nice header comment!', 1407385226975),
    ('4e398e765b6b448998016a8f78d747b4', '57f64113e5b64610bc8a5d0809ad027', '1cc34f0add5347efb228a045e86a16b', 1, 'this comment overlaps!', 1407385226975),
    ('705f19d4b46b447faa7d59c84ff4627b', '57f64113e5b64610bc8a5d0809ad027', '1cc34f0add5347efb228a045e86a16b', 1, 'what are we going to do with all these overlapping comments', 1407385226975),
    ('ac0f8cb4443d404dbe29496643bc963', '57f64113e5b64610bc8a5d0809ad027', '8f0068feefbd405d89fc8b27f0a951f', 4, 'do we really need this import?', 1407385248975),
    ('0e8eae9f7c504dc4991c1359e8e704f', '9a60b32175c74392bcee166548d27a1', '8f0068feefbd405d89fc8b27f0a951f', 9, 'good idea to use a define macro here, this will make your code much easier to read in the future', 1407385248975)
;
