--
-- adds two users to the database, one for read-only access and
-- another for read-write access:
--
-- NOTE: do NOT change the user names, and do NOT change the pwds.
-- These need to remain as is for grading purposes.
--
-- ref: https://dev.mysql.com/doc/refman/8.0/en/create-user.html
--

USE photoapp;

DROP USER IF EXISTS 'photoapp-read-only';
DROP USER IF EXISTS 'photoapp-read-write';

CREATE USER 'photoapp-read-only' IDENTIFIED BY 'abc123!!';
CREATE USER 'photoapp-read-write' IDENTIFIED BY 'def456!!';

GRANT SELECT, SHOW VIEW ON photoapp.* 
      TO 'photoapp-read-only';
GRANT SELECT, SHOW VIEW, INSERT, UPDATE, DELETE ON photoapp.* 
      TO 'photoapp-read-write';
      
FLUSH PRIVILEGES;