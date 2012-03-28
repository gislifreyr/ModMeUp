import data
import pearson
import traceback
import sys
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
				print "You have given %s (%s) a rating of %s" % (d.movies[mid].name,mid,rating)
				collected = 1
			except Exception as e:
				print str(e)

		except Exception as e:
			print "whoooopsadaisy: " + str(e)

def collectUserId():
	userid = False
	user = None
	while (not userid):
		try:
			inp = raw_input(prompt)
			uid = inp.strip()
			if uid not in d.users.keys():
				raise Exception("No such user ID!")
			if (len(d.users[uid].ratings.keys()) < 2):
				raise Exception("Selected user (%s) does not have enough ratings!"%uid)
			userid = uid
			print "You have chosen user: %s"%uid
		except Exception as e:
			print str(e)
	return userid


def showSimilarUsers():
	# 1. get a user ID
	userid = collectUserId()
	user = d.users[userid]
	pprint(user.ratings)
	print "Building correlations... This may take a moment"
	user.buildCorrelations(d.users, a.Correlation) # a is a global !
	if (len(user.similarUsers.keys()) < 1):
		print "We are sorry, you have no positive correlation with any of our users :-("
	else:
		# now we shall order the users by similarity!
		similar = sorted(user.similarUsers.iteritems(), key=lambda(k,v):(v,k), reverse=True)
		# And show them..
		print "Your most similar users are:"
		for item in similar:
			print item[0] + " : %.2f%% match!"%(item[1]['correlation']*100)
		raw_input("Press enter to continue")

prompt = '>> '

print "ModMeUp"
print "What do you want to do?"
#print "To create a user press [1].\nTo add a movie press [2].\nTo add a rating press [3]."  

while (1):
	print "To create a user press [1].\nTo add a movie press [2].\nTo add a rating press [3].\nTo find similar users press [4]\nTo get recommendations press [5]"  
	n = raw_input(prompt)
	try:
		n = int(n)
		if n < 0 or n > 5:
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
		elif n == 4:
			print "To see similar users, enter a valid user ID, such as: %s"%(', '.join(d.users.keys()[:min(5,len(d.users.keys()))]))
			showSimilarUsers()
		elif n == 5:
			print "To get recommendations for a user, enter a valid user ID, such as: %s"%(', '.join(d.users.keys()[:min(5,len(d.users.keys()))]))
			showRecommendations()

	except Exception as e:
		print "Some kind of exception!"
		traceback.print_exc(file=sys.stdout)

