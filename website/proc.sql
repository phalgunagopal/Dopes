DELIMITER $$
CREATE PROCEDURE commitsmade(IN id INT)
BEGIN
SELECT repo_id, filename, timestamp from  commit WHERE commit.user_id = id;
END $$
DELIMITER;