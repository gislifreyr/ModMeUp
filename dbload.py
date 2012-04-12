#!/usr/bin/python -u
# ~!~ encoding: utf-8 ~!~
import sys
import os
import sqlite3

default_datadir = "./data"

def insert_user(cursor, rec):
	return cursor.execute("INSERT INTO user (id,age,gender,occupation,zipcode) VALUES (?, ?, ?, ?, ?)", rec)

def insert_movie(cursor, rec):
	return cursor.execute("INSERT INTO movie (id,name,releasedate,url) VALUES (?, ?, ?, ?)", rec)

def insert_genre(cursor, rec):
	return cursor.execute("INSERT INTO genre (name) VALUES (?)", rec)

def insert_movie_genre(cursor, rec):
	return cursor.execute("INSERT INTO movie_genre (id,movieid,genreid) VALUES (?, ?, ?)", rec)

def insert_user_rating(cursor, rec):
	return cursor.execute("INSERT INTO user_ratings (id,uid,mid,rating,timestamp) VALUES (?,?,?,?,?)", rec)


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
	c = db.cursor()
	# special handling for genres!
	genres = ['unknown', 'Action' 'Adventure', 'Animation', 'Children\'s', 'Comedy', 'Crime' 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western' ]
	print "Loading genres.."
	for g in genres:
		if not insert_genre(c, list([g])):
			print "Failed to insert: %s"%g

	#db.commit()
		
if __name__ == '__main__':
	main()

