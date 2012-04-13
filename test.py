#!/usr/bin/python
import data
import pearson
import sys
from pprint import pprint

test_db = "test.db"
if (len(sys.argv) > 1):
	try:
		assert(os.path.exists(sys.argv[1]))
	except:
		print "Oops, if you run %s with arguments, the first argument is expected to be an sqlite database file!"%sys.argv[0]
		print "However %s was not found!"%sys.argv[1]

# correlation tests, performed after loading data, and after closing and reopening database to verify data integrity of addUser/addMovie/addRating
def correlation_tests(d, curtest):
	a = pearson.Algorithm()
	fails = 0
	ntests = curtest
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
	return (ntests,fails)

ratings = {
	4: {1: 2.5, 2: 3.5, 3: 3, 4: 3.5, 5: 2.5, 6: 3.0 },
	2: {1: 3, 2: 3.5, 3: 1.5, 4: 5, 6: 3, 5: 3.5 },
	6: {1: 2.5, 2: 3.0, 4: 3.5, 6: 4 },
	1: {2: 3.5, 3: 3, 6: 4.5, 4: 4.0, 5: 2.5 },
	5: {1: 3, 2: 4, 3: 2, 4: 3, 6: 3, 5: 2 },
	3: {1: 3, 2: 4, 6: 3, 4: 5, 5: 3.5 },
	7: {2: 4.5, 5: 1, 4: 4 }
}

tests = 17
ntests = 0
fails = 0

print "Testing phase 1: loading data via the API"
d = data.data(test_db)
users = []
try:
	ntests += 1
	for i in range(0,7):
		users.append(d.addUser('', 20, 'M', 'programmer', '90210'))
	if (len(users) == 7):
		print "Test %d (adding users) successful"%ntests
	else:
		print "Test %d (adding users) failed: incorrect no. of users: %d"%(ntests, len(users))
		fails +=1
except Exception as e:
	print "Test %d (adding users) failed: exception: %s"%(ntests, str(e))
	fails +=1

movies = []
try:
	ntests += 1
	for movie in ['Lady (1999)','Snakes (2000)','Luck (2001)','Superman (2002)','Dupree (2003)','Night (2004)']:
		movies.append(d.addMovie('', movie))
	if (len(movies) == 6):
		print "Test %d (adding movies) successful"%ntests
	else:
		print "Test %d (adding movies) failed: incorrect no. of movies: %d"%(ntests, len(moviess))
		fails +=1
except Exception as e:
	print "Test %d (adding movies) failed: exception: %s"%(ntests, str(e))
	fails +=1

try:
	ntests += 1
	for uid in ratings.keys():
		for mid in ratings[uid].keys():
			rating = ratings[uid][mid]
			d.addRating(uid,mid,rating)
	cnt = d.c.execute("SELECT COUNT(*) FROM user_ratings").fetchone()[0]
	if (cnt == 35):
		print "Test %d (adding ratings) succesful"%ntests
	else:
		print "Test %d (adding ratings) failed: wrong no. of ratings: %d"%(ntests, cnt)
		fails +=1
except Exception as e:
	print "Test %d (adding ratings) failed: exception: %s"%(ntests, str(e))
	fails +=1


print "\nTesting phase 2: Correlation tests using API loaded data"
(ntests,nfails) = correlation_tests(d, ntests)
fails += nfails

d = None
d = data.data('test.db')
print "\nTesting phase 3: Correlation tests using DB loaded data (did the API loading save?)"
print "Loading users"
d.loadUsers()
print "Loading movies"
d.loadMovies()
print "Loading ratings"
d.loadRatings()
(ntests,nfails) = correlation_tests(d, ntests)
fails += nfails

print "%d/%d tests performed with %d failures"%(ntests,tests,fails)
if fails == 0:
	print "Congratulations"
else:
	print "Oops! Check your code"
