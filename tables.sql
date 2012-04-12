-- file: u.user
create table user
(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	age INTEGER,
	gender VARCHAR(1),
	occupation VARCHAR(32),
	zipcode INTEGER
);

-- file: u.item
create table movie
(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT,
	releasedate DATE,
	url TEXT
);

-- genres:
-- unknown, action, adventure, animation, childrens, comedy, crime, documentary, darama, fantasy, film-noir, horror, musical, mystery, romance, sci-fi, thriller, war, western
create table genre
(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(32)
);

-- many-to-many based on file: u.item "bitfield" at the end!
create table movie_genre
(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	movieid INTEGER,
	genreid INTEGER,
	FOREIGN KEY (movieid) REFERENCES movie(id),
	FOREIGN KEY (genreid) REFERENCES genre(id)
);

-- u.data
create table user_ratings
(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	uid INTEGER,
	mid INTEGER,
	rating FLOAT,
	timestamp TIMESTAMP,
	FOREIGN KEY (uid) REFERENCES user,
	FOREIGN KEY (mid) REFERENCES movie
);


-- index for movie_genre
create unique index idx_moviegenre on movie_genre (genreid,movieid);
