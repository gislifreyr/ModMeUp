class User:
	def __init__(self,uid,age,sex,occupation,zipcode,ratings):
		self.uid = uid
		self.age = age
		self.sex = sex
		self.occupation = occupation
		self.zipcode = zipcode
		self.ratings = ratings

	def getRatings(self):
		return self.ratings
	def Rate(self,movie,rating):
		self.ratings[movie] = rating
	def getInfo(self):
		return {'uid':self.uid,'age':self.age,'sex':self.sex,'occupation':self.occupation,'zipcode':self.zipcode}

class Movie:
	def __init__(self,mid,name,genres,ratings=None):
		self.ratings = ratings
		self.mid = mid
		self.genres = genres
	def getRators(self):
		return self.ratings.keys() # the key to a rating is a user id (uid) !
	def getRatings(self):
		return self.ratings
	def Rate(self,uid,rating)
		self.ratings[uid] = rating

class data:
	def __init__(self):
		self.users = {}
		self.movies = {}
	def loadUsers(self):
		f = file("data/u.user")
		for l in f.readlines():
			list(id,age,sex,occupation,zipcode) = l.split('|')
			self.users[id] = User(id,age,sex,occupation,{})
		f.close()

	def loadMovies(self):
		f = file("data/u.item")
		for l in f.readlines():
			# 118|Twister (1996)|10-May-1996||http://us.imdb.com/M/title-exact?Twister%20(1996)|0|1|1|0|0|0|0|0|0|0|0|0|0|0|0|0|1|0|0
			arr = l.split('|')
			list(id,name,release,vrelease,imdburl) = arr[0:5]
			genres = self.translateGenre(arr[5:])
			self.movies[id] = Movie(id,name,genres,{})

	def loadRatings(self):
		f = file("data/u.data")
		for l in f.readlines():
			list(uid,mid,rating,timestamp) = l.split("\t")
			self.users[uid].Rate(mid, rating)
			self.movies[mid].Rate(uid, rating)

	def translateGenre(self,garr):
		genres = ['unknown', 'Action' 'Adventure', 'Animation', 'Children\'s', 'Comedy', 'Crime' 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western' ]
		r = []
		i = 0
		for n in garr:
			if (n == 1):
				r.append(genres[i])
			i += 1
		return r

