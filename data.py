#!/usr/bin/python -u
# ~!~ encoding: utf-8 ~!~

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
		try:
			for uid in self.similarUsers:
				user = self.similarUsers[uid]
				if (mid in user['unseen_movies']):
					sumcorr += user['correlation']
					sumeinkunn += user['unseen_movies'][mid]['sx-einkunn']
			return sumeinkunn/sumcorr
		except:
			print "Argh, eitthvað fucked"

class Movie:
	def __init__(self,mid,name,genres,ratings=None):
		self.ratings = ratings
		self.mid = mid
		self.genres = genres
	def getRators(self):
		return self.ratings.keys() # the key to a rating is a user id (uid) !
	def getRatings(self):
		return self.ratings
	def Rate(self,uid,rating):
		self.ratings[uid] = float(rating)

class data:
	def __init__(self):
		self.users = {}
		self.movies = {}

	def addUser(self, uid, age='N/A', sex='N/A', occupation='N/A', zipcode='N/A', ratings={}):
		if self.users.has_key(uid):
			raise Exception("User ID already exists")
		self.users[uid] = User(uid,age,sex,occupation,zipcode,ratings)

	def addMovie(self,mid,name,release=0,vrelease=0,imdburl='N/A',genres=[],ratings={}):
		if self.movies.has_key(mid):
			raise Exception("Movie ID already exists")
		self.movies[mid] = Movie(mid,name,genres,{})

	def addRating(self,uid,mid,rating,timestamp=0):
		if not self.users.has_key(uid):
			raise Exception("No such User ID !")

		if not self.movies.has_key(mid):
			raise Exception("No such Movie ID !")

		self.users[uid].Rate(mid, rating)
		self.movies[mid].Rate(uid, rating)


	def loadUsers(self):
		f = file("data/u.user")
		for l in f.readlines():
			(id,age,sex,occupation,zipcode) = l.split('|')
			self.addUser(id,age,sex,occupation,zipcode,{})
		f.close()

	def loadMovies(self):
		f = file("data/u.item")
		for l in f.readlines():
			# 118|Twister (1996)|10-May-1996||http://us.imdb.com/M/title-exact?Twister%20(1996)|0|1|1|0|0|0|0|0|0|0|0|0|0|0|0|0|1|0|0
			arr = l.split('|')
			(mid,name,release,vrelease,imdburl) = arr[0:5]
			genres = self.translateGenre(arr[5:])
			self.addMovie(mid,name,genres,{})

	def loadRatings(self):
		f = file("data/u.data")
		for l in f.readlines():
			(uid,mid,rating,timestamp) = l.split("\t")
			self.addRating(uid,mid,rating,timestamp)

	def translateGenre(self,garr):
		genres = ['unknown', 'Action' 'Adventure', 'Animation', 'Children\'s', 'Comedy', 'Crime' 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western' ]
		r = []
		i = 0
		for n in garr:
			if (n == 1):
				r.append(genres[i])
			i += 1
		return r

