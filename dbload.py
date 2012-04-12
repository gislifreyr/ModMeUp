#!/usr/bin/python -u
# ~!~ encoding: utf-8 ~!~
import sys
import os
import sqlite3

default_datadir = "./data"
genres = ['unknown', 'Action', 'Adventure', 'Animation', 'Children\'s', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western' ]

def insert_user(cursor, rec):
	return cursor.execute("INSERT INTO user (id,age,gender,occupation,zipcode) VALUES (?, ?, ?, ?, ?)", rec[:5])

def insert_movie(cursor, rec):
	return cursor.execute("INSERT INTO movie (id,name,releasedate,url) VALUES (?, ?, ?, ?)", (rec[0], rec[1], rec[2], rec[4]))

def insert_genre(cursor, rec):
	return cursor.execute("INSERT INTO genre (name) VALUES (?)", rec[:1])

def insert_movie_genre(cursor, rec):
	return cursor.execute("INSERT INTO movie_genre (movieid,genreid) VALUES (?, ?)", rec[:2])

def insert_user_rating(cursor, rec):
	return cursor.execute("INSERT INTO user_ratings (uid,mid,rating,timestamp) VALUES (?,?,?,?)", rec[:4])

def loadGenres(cursor):
	cursor.execute("SELECT * FROM genre")
	gm = {}
	for row in cursor.fetchall():
		gm[row[1]] = row[0]
	return gm

def setGenres(cursor, rec):
	mid = rec[0]
	garr = rec[5:]
	genre_map = loadGenres(cursor)
	r = []
	i = 0
	for n in garr:
		if (int(n) == 1):
			gid = genre_map[genres[i]]
			insert_movie_genre(cursor, list([mid, gid]))
		i += 1

def main():
	if (len(sys.argv) < 2):
		print "Usage: %s <database> [datadir]"%sys.argv[0]
		print "datadir is optional, defaults to \"data\""
		sys.exit(1)
	sys.argv.reverse()
	sys.argv.pop() # get rid of ourselves
	
	database = sys.argv.pop()
	try:
		datadir = sys.argv.pop()
		if not datadir: datadir = default_datadir
	except:
		datadir = default_datadir
	# here below we could use assert(), but that would be wrong
	if not os.path.exists(datadir):
		print "oops! the datadir: %s does not exist, can't continue with that!"%datadir
		sys.exit(1)

	if not os.path.exists(database):
		print "oops! the database you specified (%s) does not exist, please read the README file!"%database
		sys.exit(1)

	print "Opening database: %s"%database
	db = sqlite3.connect(database)
	db.text_factory = str
	c = db.cursor()
	# special handling for genres!
	print "Loading genres.."
	for g in genres:
		if not insert_genre(c, list([g])):
			print "Failed to insert: %s"%g

	db.commit()

	data = [ { 'name': 'user',
		   'insert':insert_user,
	  	   'file':'u.user',
		   'sep':'|'
		 },
		 { 'name': 'movie',
		   'insert':insert_movie,
	 	   'file':'u.item',
		   'sep':'|',
		   'post_proc':setGenres
		 },
		 { 'name': 'user_rating',
		   'insert': insert_user_rating,
		   'file':'u.data',
		   'sep':"\t"
                 }
		]

	for dsn in data:
		print "Loading %s"%dsn['name']
		for line in open(datadir + "/" + dsn['file']).readlines():
			rec = line.strip().split(dsn['sep'])
			if (not dsn['insert'](c, list(rec))):
				print "failed to insert:"
				print rec
			if dsn.has_key('post_proc'):
				dsn['post_proc'](c, list(rec))

	db.commit()
		
if __name__ == '__main__':
	main()

