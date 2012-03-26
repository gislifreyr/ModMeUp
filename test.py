#!/usr/bin/python
import data
import pearson
from pprint import pprint

d = data.data()
print "Loading users"
d.loadUsers()
print "Loading movies"
d.loadMovies()
print "Loading ratings"
d.loadRatings()

a = pearson.Algorithm()

notandi = d.users['TB']

myndir = notandi.buildCorrelations(d.users, a.Correlation2)
pprint(notandi.similarUsers)

for m in myndir:
	r = notandi.weightedRating(m)
	print m + " = " + str(r)

