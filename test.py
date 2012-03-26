#!/usr/bin/python
import data
import pearson

d = data.data()
print "Loading users"
d.loadUsers()
print "Loading movies"
d.loadMovies()
print "Loading ratings"
d.loadRatings()

prefs = {}
for user in d.users.keys():
	prefs[user] = d.users[user].ratings

a = pearson.Algorithm()

print a.Correlation2(prefs, 'TB', 'JM')
