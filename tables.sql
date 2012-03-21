
# file: u.user
create table user
(
	id
	age
	gender
	occupation
	zipcode
);

# file: u.item
create table movie
(
	id
	name
	release-date
	url
);

# genres:
# unknown, action, adventure, animation, childrens, comedy, crime, documentary, darama, fantasy, film-noir, horror, musical, mystery, romance, sci-fi, thriller, war, western
create table genre
(
	id
	name
);

# many-to-many based on file: u.item "bitfield" at the end!
create table movie_genre
(
	id
	movieid
	genreid
)

# u.data
create table user_ratings
(
	user id,
	movie id
	rating
	timestamp
);

