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
	def getInfo(self):
		return {'uid':self.uid,'age':self.age,'sex':self.sex,'occupation':self.occupation,'zipcode':self.zipcode}

class Movie:
	def __init__(self,mid,name,genre,ratings=None):
		self.ratings = ratings
	def getRators(self):
		return self.ratings.keys() # the key to a rating is a user id (uid) !
	def getRatings(self):
		return self.ratings
	def setRatings(self, ratings):
		self.ratings = ratings

class data:
	def __init__(self):
		self.users = {}
		self.movies = {}
	def loadUsers(self):
		f = file("data/u.user")
		for l in f.readlines():
			list(id,age,sex,occupation,zipcode) = l.split('|')
			self.users[id] = User(id,age,sex,occupation,{})

	def loadMovies(self):
		f = file("data/u.item")
		for l in f.readlines():

	def translateGenre(self,garr):
		genres = ['unknown', 'Action' 'Adventure', 'Animation', 'Children\'s', 'Comedy', 'Crime' 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western' ]
		r = []
		i = 0
		for n in garr:
			if (n == 1):
				r.append(genres[i])
			i += 1
		return r

