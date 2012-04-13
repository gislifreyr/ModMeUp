#!/usr/bin/python
import data
import pearson
from pprint import pprint

d = data.data('test.db')
print "Loading users"
d.loadUsers()
print "Loading movies"
d.loadMovies()
print "Loading ratings"
d.loadRatings()

a = pearson.Algorithm()

#pprint(notandi.similarUsers)

tests = 7
ntests = 0
fails = 0

#Users
#CP => 1 GS => 2 JM => 3 LR => 4 MLS => 5 MP => 6 TB => 7

#Movies
#LW => 1 SP => 2 JML => 3 SR => 4 YMD => 5 NL => 6

notandi = d.users[7] #TB
myndir = notandi.buildCorrelations(d.users, a.Correlation)

test_output = { 6: 3.34778952671, # NL
		1: 2.83254991826, # LW
		3: 2.53098070377 } # JML
ntests += 1
if len(myndir) != 3:
	print "Test %d failed: too many results"%ntests
	fails += 1
else:
	print "Test %d (result number) successful"%ntests

for m in test_output.keys():
	ntests += 1
	if m not in myndir:
		print "Test %d failed: %s not found"%(ntests,m)
		fails += 1
	else:
		print "Test %d (%s found) successful"%(ntests,m)


for m in test_output.keys():
	ntests += 1
	try:
		if "%f"%test_output[m] != "%f"%notandi.weightedRating(m):
			print "Test %d failed: %s rating incorrect (%f/%f)"%(ntests,m,test_output[m],notandi.weightedRating(m))
			fails += 1
		else:
			print "Test %d (rating %s: %f==%f) successful"%(ntests,m,test_output[m],notandi.weightedRating(m))
	except:
		fails += 1
		print "Test %d failed: %s not found"%(ntests,m)

print "%d/%d tests performed with %d failures"%(tests,ntests,fails)
if fails == 0:
	print "Congratulations"
else:
	print "Oops! Check your code"
