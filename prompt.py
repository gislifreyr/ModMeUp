import data
import pearson
from pprint import pprint

d = data.data()
d.loadUsers()
d.loadMovies()
d.loadRatings()

a = pearson.Algorithm()

def collectUser():
	collected = 0
	while (not collected):
		try:
			inp = raw_input(prompt)
			(uid,age,sex,occupation,zipcode) = inp.strip().split(',')
			try:
				d.addUser(uid,age,sex,occupation,zipcode)
				print "You have added a user.\n uid:%s, age:%s, sex:%s, occupation:%s, zipcode:%s" % (uid,age,sex,occupation,zipcode)
				collected = 1
			except Exception as e:
				print str(e)

		except Exception as e:
			print "oops: " + str(e)

def collectMovie():
	collected = 0
	while (not collected):
		try:
			inp = raw_input(prompt)
			(mid,name) = inp.strip().split(',')
			try:
				d.addMovie(mid,name)
				print "You have added %s with the mid %s" % (name,mid)
				collected = 1
			except Exception as e:
				print str(e)

		except Exception as e:
			print "oopsadaisy: " + str(e)
	
def collectRating():
	collected = 0
	while (not collected):
		try:
			inp = raw_input(prompt)
			(uid,mid,rating) = inp.strip().split(',')
			try:
				d.addRating(uid,mid,rating)
				print "You have given %s a rating of %s" % (mid,rating)
				collected = 1
			except Exception as e:
				print str(e)

		except Exception as e:
			print "whoooopsadaisy: " + str(e)

prompt = '>> '

print "ModMeUp"
print "What do you want to do?"
#print "To create a user press [1].\nTo add a movie press [2].\nTo add a rating press [3]."  

while (1):
	print "To create a user press [1].\nTo add a movie press [2].\nTo add a rating press [3]."  
	n = raw_input(prompt)
	try:
		n = int(n)
		if n < 0 or n > 3:
			raise Exception ("Not a valid choice!")
		elif n == 1:	
			print "To create a user type your information as such 'initials,age,sex,occupation,zipcode'"
			collectUser()
		elif n == 2:
			print "To add a movie type your information as such 'movieid,movietitle'"
			collectMovie()
		elif n == 3:
			print "To add a rating type your information as such 'uid,mid,rating"
			collectRating()

	except Exception as e:
		print "HEYRRU! " + str(e)

