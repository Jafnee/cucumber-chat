CREATE KEYSPACE cucumber_chat
WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };

USE cucumber_chat;

CREATE TABLE messages (
id timeuuid,
username text,
message text,
PRIMARY KEY((username), id)
) WITH CLUSTERING ORDER BY (id ASC);
