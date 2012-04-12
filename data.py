#!/usr/bin/python -u
# ~!~ encoding: utf-8 ~!~
import os
import sqlite3

class User:
	def __init__(self,uid,age,sex,occupation,zipcode,ratings):
		self.uid = uid
		self.age = age
		self.sex = sex
		self.occupation = occupation
		self.zipcode = zipcode
		self.ratings = ratings
		self.similarUsers = {}

	def getRatings(self):
		return self.ratings
	def Rate(self,movie,rating):
		self.ratings[movie] = float(rating)
	def getInfo(self):
		return {'uid':self.uid,'age':self.age,'sex':self.sex,'occupation':self.occupation,'zipcode':self.zipcode}
	
	# Notkun: m = u.buildCorrelations(users, algorithm)
	# Fyrir:  u er User object, algorithm er vísir á fylgni (correlation) reiknirit sem ber saman 2 notendur
	# Eftir:  m er listi yfir kvikmyndir (mid) sem við getum gefið einkunn fyrir, handa notanda u
	def buildCorrelations(self,users,alg):
		for uid in users.keys():
			if uid == self.uid: continue # skip if it's ourselves!
			# overkill
			#prefs = dict([(item,self.ratings[item]) for item in self.ratings.keys() if users[uid].ratings.has_key(item)])
			prefs = {self.uid: self.ratings, uid: users[uid].ratings}
			corr = alg(prefs,self.uid, uid)
			if corr <= 0: continue #skip this user if no correlation or negative correlation
			try:
				self.similarUsers[uid]['correlation'] = corr
			except:
				self.similarUsers[uid] = {'correlation': corr}

		# now we have a list of users which are similar, let's try and see if they have seen movies we should also see!
		m = []
		for uid in self.similarUsers.keys():
			user = users[uid]
			unseen_movies = {}
			for mid in user.ratings.keys():
				if mid in self.ratings.keys(): continue
				if mid not in m:
					# óséð movie id!
					m.append(mid)
				unseen_movies[mid] = {}
				unseen_movies[mid]['einkunn'] = user.ratings[mid]
				unseen_movies[mid]['sx-einkunn'] = user.ratings[mid] * self.similarUsers[uid]['correlation']
			self.similarUsers[uid]['unseen_movies'] = unseen_movies
		return m

	def weightedRating(self, mid):
		sumeinkunn = 0
		sumcorr = 0
		for uid in self.similarUsers:
			user = self.similarUsers[uid]
			if (mid in user['unseen_movies']):
				sumcorr += user['correlation']
				sumeinkunn += user['unseen_movies'][mid]['sx-einkunn']
		if (sumeinkunn == 0 or sumcorr == 0):
			raise Exception("No data available to give a weighted rating!?")
		return sumeinkunn/sumcorr

class Movie:
	def __init__(self,mid,name,genres,ratings=None):
		self.ratings = ratings
		self.mid = mid
		self.name = name
		self.genres = genres
	def getRators(self):
		return self.ratings.keys() # the key to a rating is a user id (uid) !
	def getRatings(self):
		return self.ratings
	def loadGenres(self,cursor):
		genres = cursor.execute("select name from genre left join movie_genre where genre.id=movie_genre.genreid and movieid=%d"%self.mid).fetchall()
		self.genres = genres
	def Rate(self,uid,rating):
		self.ratings[uid] = float(rating)

class data:
	def __init__(self, dbname='modmeup.db'):
		self.users = {}
		self.movies = {}
		assert(os.path.exists(dbname))
		self.db = sqlite3.connect(dbname)
		self.db.text_factory = str # our dataset is not utf-8
		self.c = self.db.cursor()

	def addUser(self, uid, age='N/A', sex='N/A', occupation='N/A', zipcode='N/A', ratings={}):
		# XXX: ADD TO DB!
		if self.users.has_key(uid):
			raise Exception("User ID already exists")
		self.users[uid] = User(uid,age,sex,occupation,zipcode,ratings)
		return self.users[uid]

	def addMovie(self,mid,name,release=0,vrelease=0,imdburl='N/A',genres=[],ratings={}):
		# XXX: ADD TO DB!
		if self.movies.has_key(mid):
			raise Exception("Movie ID already exists")
		self.movies[mid] = Movie(mid,name,genres,{})
		return self.movies[mid]

	def addRating(self,uid,mid,rating,timestamp=0):
		# XXX: ADD TO DB!
		if not self.users.has_key(uid):
			raise Exception("No such User ID !")

		if not self.movies.has_key(mid):
			raise Exception("No such Movie ID !")

		self.users[uid].Rate(mid, rating)
		self.movies[mid].Rate(uid, rating)


	def loadUsers(self):
		users = self.c.execute("SELECT * FROM user").fetchall()
		for u in users:
			(id,age,sex,occupation,zipcode) = u
			self.addUser(id,age,sex,occupation,zipcode,{})

	def loadMovies(self):
		movies = self.c.execute("SELECT * FROM movie").fetchall()
		for m in movies:
			(mid,name,release,imdburl) = m
			movie = self.addMovie(mid,name,[],{})
			#print "Loading genres for: %s"%name
			movie.loadGenres(self.c)

	def loadRatings(self):
		ratings = self.c.execute("SELECT * FROM user_ratings")
		for r in ratings:
			(rid,uid,mid,rating,timestamp) = r
			self.addRating(uid,mid,rating,timestamp)
