"""
	Classes for generating finite difference expressions for derivatives.

	Classes:
    --------

	GridPoint: Expression that represents function evaluation at a certain point.
	Num: Numerator of a finite difference expression.
	Den: Denominator of a finite difference expression.
	FinDiff: Finite difference expression of a derivative.
"""

class GridPoint(object):
	"""
		 Evaluation of a function at a certain point: coeff*f(i+ind)

	Examples:
	--------

		>>> import finiteDifference as fd		
		>>> a=fd.GridPoint()
		>>> print(a)
  			1.0*f(i)
		>>> b=fd.GridPoint(coeff=2,ind=3)
		>>> print(b)
  			2.0*f(i+3)
	"""
	def __init__(self, coeff = 1, ind = 0):

		self.ind = ind
		self.coeff = coeff
		if ind < 0:
			self.sign = '-'
		else:
			self.sign = '+'

	def __str__(self):
		if self.ind == 0:
			return '%5.1f*f(i)' % self.coeff
		else:
			return '%5.1f*f(i%s%i)' % (self.coeff, self.sign, abs(self.ind))


class Den(object):
	"""
		Denominator of a finite difference approximation.

	Examples:
	--------

	>>> import finiteDifference as fd		
	>>> a=fd.Den()
	>>> print(a)
		(dh)^1
	>>> b=fd.Den(power=2)
	>>> print(b)
		(dh)^2
	"""
	def __init__(self, power = 1):
		self.power = power

	def __str__(self):
		return '(dh)^%i' % self.power


class Num(object):
	"""
		Numerator of a finite difference approximation. Created from a list of grid points.
		It simplifies similar terms at the moment it is created.

	Examples:
	--------

	>>> import finiteDifference as fd		
	>>> a=fd.Num([fd.GridPoint(coeff=2.0,ind=2),fd.GridPoint(coeff=-1,ind=2),fd.GridPoint()])
	>>> print(a)
  		1.0*f(i+2)+  1.0*f(i)

	Numerators can be added can also be added.

	>>> a=fd.Num([fd.GridPoint(ind=2)])
	>>> b=fd.Num([fd.GridPoint(ind=1)])
	>>> c=a+b
	>>> print(a)
  		1.0*f(i+2)
	>>> print(b)
	  	1.0*f(i+1)
	>>> print(c)
  		1.0*f(i+2)+  1.0*f(i+1)

	"""
	def __init__(self, exp = None):
		if exp is None:
			self.exp = []
		else:
			self.exp = exp
			self.simplify()

	def __add__(self, num2):
		return Num(exp=self.exp+num2.exp)

	def simplify(self):
		temp = [self.exp[0]]
		for gP in self.exp[1:]:
			for i, gPtemp in enumerate(temp):
				if gP.ind == gPtemp.ind:
					temp[i] = GridPoint(coeff=gP.coeff + gPtemp.coeff, ind=gP.ind)
					break
			else:
				temp.append(gP)
		self.exp = temp

	def __str__(self):
		temps = str(self.exp[0])
		for gP in self.exp[1:]:
			if gP.coeff<0:
				temps += str(gP)
			else:
				temps += '+'+str(gP)
		return temps


class FinDiff(object):
	"""
		Finite difference approximation around a specified grid point.
		The approximation is computed using one of the following methods:
		'backward', 'forward', 'central'
	
	Contains the following attributes:

	numer: Instance of finiteDifference.Num class.
	denom: Instance of finiteDifference.Den class.

	Examples:
	--------

	>>> import finiteDifference as fd
	>>> a=fd.FinDiff()
	>>> print(a.numer)
	  	0.5*f(i+1)+  0.0*f(i) -0.5*f(i-1)
	>>> print(a.denom)
		(dh)^1
	"""
	def __init__(self, method = 'central', order = 1, point = GridPoint()):
		self.method = method
		self.order = order
		self.point = point
		self.numer = Num([self.point])
		if self.method == 'backward':
			self.numer = Num(self.backwardMethod(self.order, self.numer.exp))
		elif self.method == 'forward':
			self.numer = Num(self.forwardMethod(self.order, self.numer.exp))
		elif self.method == 'central':
			if order%2==0:
				gPTemp1=GridPoint(coeff=0.5*self.point.coeff,ind=self.point.ind-0.5*order)
				gPTemp2=GridPoint(coeff=0.5*self.point.coeff,ind=self.point.ind+0.5*order)
				self.numer = Num(self.forwardMethod(self.order,[gPTemp1]))+Num(self.backwardMethod(self.order,[gPTemp2]))
			else:
				gPTemp1=GridPoint(coeff=0.5*self.point.coeff,ind=self.point.ind-0.5*(order-1))
				gPTemp2=GridPoint(coeff=0.5*self.point.coeff,ind=self.point.ind+0.5*(order-1))				
				self.numer = Num(self.forwardMethod(self.order,[gPTemp1]))+Num(self.backwardMethod(self.order,[gPTemp2]))
		else:
			print('Invalid method')
			self.numer=Num()      
		self.denom = Den(power=order)

	def backwardMethod(self, order, exp):
		if order > 1:
			return self.backwardMethod(order - 1, self.backwardMethod(1, exp))
		if order == 1:
			temp = []
			for gP in exp:
				temp.extend([GridPoint(coeff=gP.coeff, ind=gP.ind), GridPoint(coeff=-gP.coeff, ind=gP.ind - 1)])
			return temp
	def forwardMethod(self, order, exp):
		if order > 1:
			return self.forwardMethod(order - 1, self.forwardMethod(1, exp))
		if order == 1:
			temp = []
			for gP in exp:
				temp.extend([GridPoint(coeff=gP.coeff, ind=gP.ind+1),GridPoint(coeff=-gP.coeff, ind=gP.ind)])
			return temp

