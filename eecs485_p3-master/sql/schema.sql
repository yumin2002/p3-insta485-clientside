CREATE TABLE users(
  username VARCHAR(20) NOT NULL,
  fullname VARCHAR(40) NOT NULL,
  email VARCHAR(40) NOT NULL,
  filename VARCHAR(64) NOT NULL,
  password VARCHAR(256) NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (username)
);
CREATE TABLE posts(
  postid INTEGER NOT NULL,
  filename VARCHAR(64) NOT NULL,
  owner VARCHAR(20) NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (postid),
  CONSTRAINT postsOwener_usersUsername
    FOREIGN KEY (owner) REFERENCES users(username) 
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE following(
  username1 VARCHAR(20) NOT NULL,
  username2 VARCHAR(20) NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (username1, username2),
  CONSTRAINT followingUsername1_usersUsername
    FOREIGN KEY (username1) REFERENCES users(username) 
    ON DELETE CASCADE
    ON UPDATE CASCADE
  CONSTRAINT followingUsername2_usersUsername
    FOREIGN KEY (username2) REFERENCES users(username) 
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE comments(
  commentid INTEGER NOT NULL,
  owner VARCHAR(20) NOT NULL,
  postid INTEGER NOT NULL,
  text VARCHAR(1024) NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (commentid),
  CONSTRAINT commentsOwner_usersUsername
    FOREIGN KEY (owner) REFERENCES users(username) 
    ON DELETE CASCADE
    ON UPDATE CASCADE
  CONSTRAINT commentsPostid_postsPostid
    FOREIGN KEY (postid) REFERENCES posts(postid) 
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE likes(
  owner VARCHAR(20) NOT NULL,
  postid INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (owner, postid),
  CONSTRAINT likesOwner_usersUsername
    FOREIGN KEY (owner) REFERENCES users(username) 
    ON DELETE CASCADE
    ON UPDATE CASCADE
  CONSTRAINT likesPostid_postsPostid
    FOREIGN KEY (postid) REFERENCES posts(postid) 
    ON DELETE CASCADE
    ON UPDATE CASCADE
);









