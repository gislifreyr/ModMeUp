import math	
class Algorithm:
	def Correlation(self,prefs,u1,u2):
		# Get the list of mutually rated items
		inCommon = list(set(prefs[u1]) & set(prefs[u2]))
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
		
	def mean(self,prefs,v,u): 
		Ii = len(v)
		sum1 = sum([prefs[u][k] for k in v])
		a = sum1/Ii
		#print a
		return  a #sum1 / Ii
			
	def Correlation2(self, prefs, u1, u2):
		inCommon = list(set(prefs[u1]) & set(prefs[u2]))
		if len(inCommon) == 0: 
			return 0
		v_a = self.mean(prefs,inCommon,u1)
		v_i = self.mean(prefs,inCommon,u2)
		sum1 = 0
		for k in inCommon:
			sum1 += (prefs[u1][k] - v_a) * (prefs[u2][k] - v_i)
		sum2 = 0
		#print sum1
		sum1Sq = 0
		sum2Sq = 0
		for k in inCommon:
			sum1Sq += pow((prefs[u1][k] - v_a),2)
			sum2Sq += pow((prefs[u2][k] - v_i),2)
		sum2 = math.sqrt(sum1Sq*sum2Sq)
		#print sum2
		return sum1/sum2
	
	def Pearson(self,u1,u2):
		corr = self.Correlation2(prefs,u1,u2)
		if corr == 0:
			return 0
