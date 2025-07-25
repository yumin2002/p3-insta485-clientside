PRAGMA foreign_keys = ON;

CREATE TABLE users(
  username VARCHAR(20) PRIMARY KEY NOT NULL,
  fullname VARCHAR(40) NOT NULL,
  email VARCHAR(40) NOT NULL,
  filename VARCHAR(64) NOT NULL,
  password VARCHAR(256) NOT NULL,
  created DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE posts(
  postid INTEGER PRIMARY KEY AUTOINCREMENT,
  filename VARCHAR(64) NOT NULL,
  owner VARCHAR(20) NOT NULL,
  created DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
  --why is filename and owner blue

  FOREIGN KEY (owner)
  REFERENCES users (username)
  ON DELETE CASCADE

);

CREATE TABLE following(
  username1 VARCHAR(20) NOT NULL,
  username2 VARCHAR(20) NOT NULL,
  --(username1, username2) PRIMARY KEY,
  created DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,


  FOREIGN KEY (username1)
  REFERENCES users (username)
  ON DELETE CASCADE

  FOREIGN KEY (username2)
  REFERENCES users (username)
  ON DELETE CASCADE
  --how to specify relation 
);

CREATE TABLE comments(
  commentid INTEGER PRIMARY KEY AUTOINCREMENT,
  owner VARCHAR(20),
  postid INTEGER,
  text VARCHAR(1024),
  created DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,

  FOREIGN KEY (owner)
  REFERENCES users (username)
  ON DELETE CASCADE

  FOREIGN KEY (postid)
  REFERENCES posts (postid)
  ON DELETE CASCADE
);

CREATE TABLE likes(
  likeid INTEGER PRIMARY KEY AUTOINCREMENT,
  owner VARCHAR(20) NOT NULL,
  postid INTEGER NOT NULL,
  created DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,

  FOREIGN KEY (owner)
  REFERENCES users (username)
  ON DELETE CASCADE
  
  FOREIGN KEY (postid)
  REFERENCES posts (postid)
  ON DELETE CASCADE
);