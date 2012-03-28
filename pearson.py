import math	
class Algorithm:
	def mean(self,prefs,v,u): 
		Ii = len(v)
		sum1 = sum([prefs[u][k] for k in v])
		a = sum1/Ii
		#print a
		return  a #sum1 / Ii
			
	def Correlation(self, prefs, u1, u2):
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
		if (sum2 == 0):
			return 0
		return sum1/sum2
