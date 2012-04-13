#!/usr/bin/python -u

import data
import pearson
import traceback
import sys
from pprint import pprint

print "ModMeUp ... loading data please wait"

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
			(age,gender,occupation,zipcode) = inp.strip().split(',')
			try:
				user = d.addUser('',age,gender,occupation,zipcode)
				print "You have added a user:\nage:%s, gender:%s, occupation:%s, zipcode:%s" % (age,gender,occupation,zipcode)
				print "Your new user has the user id:%d"%user.uid
				raw_input("Press enter to continue")
				collected = 1
			except Exception as e:
				print str(e)
				traceback.print_exc(file=sys.stdout)


		except Exception as e:
			print "oops: " + str(e)

def collectMovie():
	collected = 0
	while (not collected):
		try:
			inp = raw_input(prompt)
			(name) = inp.strip()
			try:
				movie = d.addMovie('',name)
				print "You have added a movie:\nname:%s id:%d" % (name,movie.mid)
				raw_input("Press enter to continue")
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
			uid = int(uid)
			mid = int(mid)
			rating = float(rating)
			try:
				d.addRating(uid,mid,rating)
				print "You have given %s (%s) a rating of %s" % (d.movies[mid].name,mid,rating)
				raw_input("Press enter to continue")
				collected = 1
			except Exception as e:
				traceback.print_exc(file=sys.stdout)

		except Exception as e:
			print "whoooopsadaisy: " + str(e)

def collectUserId():
	userid = False
	user = None
	while (not userid):
		try:
			inp = raw_input(prompt)
			uid = int(inp.strip())
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
		maxn = len(similar)
		if (maxn > 20):
			maxn = 20
		print "Your %d most similar users are:"%maxn
		for item in similar[:maxn]:
			print str(item[0]) + " : %.2f%% match!"%(item[1]['correlation']*100)
		raw_input("Press enter to continue")

def showRecommendations():
	# 1. get a user ID
	userid = collectUserId()
	user = d.users[userid]
	pprint(user.ratings)
	print "Building correlations... This may take a moment"
	rmovies = user.buildCorrelations(d.users, a.Correlation) # a is a global !
	if (len(user.similarUsers.keys()) < 1):
		print "We are sorry, you have no positive correlation with any of our users so we can't give you any recommendations :-("
	elif (len(rmovies) < 1):
		print "We are sorry, we got no movies to recommend to you :-("
	else:
		# now we loop through the recommended movies and get their ratings!
		recommendations = {}
		for m in rmovies:
			recommendations[user.weightedRating(m)] = m
		rk = recommendations.keys()
		rk.sort()
		rk.reverse()
		print "Your recommended movies:"
		for k in rk:
			print "%s (%s) (your weighted recommendation score: %f)"%(d.movies[recommendations[k]].name, recommendations[k], k)
		raw_input("Press enter to continue")

prompt = '>> '

print "Done!\n"
print "What do you want to do?"

while (1):
	print "\n========================="
	print " [1] create a user\n [2] add a movie.\n [3] add a rating.\n [4] find similar users\n [5] get recommendations\n [6] QUIT"  
	print "========================="
	n = raw_input(prompt)
	try:
		n = int(n)
		if n < 0 or n > 6:
			raise Exception ("Not a valid choice!")
		elif n == 1:	
			print "To create a user type your information as such 'age,gender,occupation,zipcode'"
			collectUser()
		elif n == 2:
			print "To add a movie type your information as such 'movietitle,releasedate,imdburl'"
			collectMovie()
		elif n == 3:
			print "To add a rating type your information as such 'uid,mid,rating"
			collectRating()
		elif n == 4:
			print "To see similar users, enter a valid user ID, such as: %s"%(', '.join([str(z) for z in d.users.keys()[:min(5,len(d.users.keys()))]]))
			showSimilarUsers()
		elif n == 5:
			print "To get recommendations for a user, enter a valid user ID, such as: %s"%(', '.join([str(z) for z in d.users.keys()[:min(5,len(d.users.keys()))]]))
			showRecommendations()
		elif n == 6:
			print "Thank you, come again!"
			sys.exit(0)

	except Exception as e:
		print "Some kind of exception!"
		traceback.print_exc(file=sys.stdout)

