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
#pprint(notandi.similarUsers)

tests = 7
ntests = 0
fails = 0

test_output = { 'NL': 3.34778952671,
		'LW': 2.83254991826,
		'JML': 2.53098070377 }
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
