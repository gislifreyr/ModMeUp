import math
prefs = {
	'1':{'lotr':1, 'starwars':5, 'indianajones':4, 'notebook':5},
	'2':{'lotr':1,'starwars':5, 'indianajones':5, 'notebook':5}
}

def pearson(prefs,u1,u2):
	# Get the list of mutually rated items
	inCommon = list(set(prefs[u1]) & set(prefs[u2]))
	print inCommon
	# if they are no ratings in common, return 0
	if len(inCommon)==0:
		return 
	# Sum calculations
	n=len(inCommon)
	# Sums of all the preferences
	sum1=sum([prefs[u1][k] for k in inCommon])
	sum2=sum([prefs[u2][k] for k in inCommon])
	# Sums of the squares
	sum1Sq=sum([pow(prefs[u1][k],2) for k in inCommon])
	sum2Sq=sum([pow(prefs[u2][k],2) for k in inCommon])	
	# Sum of the products
	pSum=sum([prefs[u1][k]*prefs[u2][k] for k in inCommon])
	# Calculate r (Pearson score)
	num=pSum-(sum1*sum2/n)
	den=math.sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
	if den==0: return 0
	r=num/den
	return r

print pearson(prefs, '1','2')
