#considerar cambiar el nombre de este archivo a fdiff o a cualquiera mas corto
class GridPoint(object):
    def __init__(self, coeff=1, ind=0):
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
    def __init__(self, power=1):
        self.power = power

    def __str__(self):
        return '(dh)^%i' % self.power


class Num(object):
    def __init__(self, exp=None):
        #exp=list of GridPoint elements
        if exp is None:
            self.exp = []
        else:
            self.exp = exp
        self.simplify()

    def __add__(self, num2):
        self.exp.extend(num2.exp)
        self.simplify()

    def simplify(self):
        """
        :rtype: Num
        """
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
    # Type: forward,backward,central
    def __init__(self, method, order, point):
        # point: gridPoint
        self.method = method
        self.order = order
        self.point = point
        self.numer = Num([self.point])  # Posiblemente deberia construirse con num
        if self.method == 'backward':
            self.numer = Num(self.backwardmethod(self.order, self.numer.exp))
        # Must raise an error for undefined method
        # Must return a numerator and one denominator
        self.denom = Den(power=order)

    def backwardmethod(self, order, exp):
        if order > 1:
            return self.backwardmethod(order - 1, self.backwardmethod(1, exp))
        if order == 1:
            temp = []
            for gP in exp:
                temp.extend([GridPoint(coeff=gP.coeff, ind=gP.ind + 1), GridPoint(coeff=-gP.coeff, ind=gP.ind)])
            return temp
        # generalizar mas
