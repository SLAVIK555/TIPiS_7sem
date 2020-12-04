import math
import numpy as np
from matplotlib import pyplot as plt

### прочие параметры
h0=0
p0=101325
#p0kg=1
g=9.8
Mmol=0.029
R=8.31
#T=273

#Ps=6612
#pkkg=0.9
###

#m=1500
### параметры зонда
m_zond=25
#t_treb_in_mezosphere
###

### параметры ракеты
m_start=440
m_fuel=294.2

t_otdel=129.6# on zhe t raboti dvigatelya

D_before=0.3
D_after=0.3

Cx=0.2
#Sm=((D/2)**2)*3.14
#print(Sm)

I=220#ud imp
W=I*g
Ssopla=(((100*D_before)/2)**2)*3.14
print(Ssopla)

w=2.27#sek rash fuel
###

H0=55000
H1=110000


resultV = []
resultH = []
resultI = []

def Sm(tx, h, v):
	if tx <= t_otdel:
		Sm=((D_before/2)**2)*3.14
	elif tx > t_otdel:
		Sm=((D_after/2)**2)*3.14
	elif tx > t_otdel & h < 5000 & v < 0:
		Sm=(((D_after/2)**2)*3.14)*50

	return Sm



def Mtek(tx, t_otdel, m_zond, m_start, m_fuel):
	if tx <= t_otdel:
		Mt = m_start - m_fuel*(tx/t_otdel)
	else:
		Mt = m_zond
		#Mt = m_start - m_fuel

	return (Mt)


def p(h):
	#pznach = -Mmol*g*(h-h0)/(R*T(h))
	return (p0 * (2.71**(-Mmol*g*(h-h0)/(R*T(h)))))

def P(h):
	return (g*(w/g)*W+Ssopla*((p(h)/98066.5)-(p0/980866.5)))#tyaga v kilogrammah

def T(h):
	if h < 11000:
		Hb = 0
		Tb = 288.15
		Lb = -6.5/1000

	elif 11000 <= h < 20000:
		Hb = 11000
		Tb = 216.65
		Lb = 0.0/1000

	elif 20000 <= h < 32000:
		Hb = 20000
		Tb = 216.65
		Lb = 1.0/1000

	elif 32000 <= h < 47000:
		Hb = 32000
		Tb = 228.65
		Lb = 2.8/1000

	elif 47000 <= h < 51000:
		Hb = 47000
		Tb = 270.65
		Lb = 0.0/1000

	elif 51000 <= h < 71000:
		Hb = 51000
		Tb = 270.65
		Lb = -2.8/1000

	elif 71000 <= h < 84900:
		Hb = 71000
		Tb = 214.65
		Lb = -2.0/1000

	else:
		Hb = 84900
		Tb = 186.87
		Lb = -1.8/1000

	Tm = Tb + Lb*(h-Hb)

	if Tm < 0:
		Tm = 4

	return (Tm)


def ro(h):
	#return ((p(h)*Mmol)/(R*T(h)))
	# kg/m^3
	ro0 = 1.2250# kg/m^3
	k = 1.38 * 10**(-23)
	momv = 4.83 * 10**(-26)#kg
	ro = ro0*(2.71**((-momv*g*(h-h0))/(k*T(h))))

	return ro

def X(v, ro, h, t_tek):
	return (Sm(t_tek, h, v)*Cx*(ro*v*v)/2)

def ft_func(t_tek, t_otdel, v, ro, h, m):
	if v>=0:
		if t_tek <= t_otdel:
			return ((P(h)-X(v, ro, h, t_tek)-(m*g))/m)
		elif t_tek >= t_otdel:
			return ((-X(v, ro, h, t_tek)-(m*g))/m)
	elif v<0:
		return ((X(v, ro, h, t_tek)-(m*g))/m)

def graf_plot(resultV, resultH, resultI):
	tresultV = tuple(resultV)
	tresultH = tuple(resultH)
	tresultI = tuple(resultI)

	#print(tresultV)

	ax = plt.subplot()
	ax.plot(tresultI, tresultV, color="blue", label="V(t)")

	#figh = plt.subplot()
	#figh.plot(tresultI, tresultH, color="red", label="H(t)")

	ax.set_xlabel("t")
	ax.set_ylabel("V(t)")

	#figh.set_xlabel("t")
	#figh.set_ylabel("H(t)")	

	ax.legend()
	#figh.legend()

	plt.show()

def main():
	print("Hello World!")

	t=1000
	dt=0.001

	V=0
	H=0
	M=m_start

	i=0
	ttr=0

	while i < t:
		dv = (ft_func(i, t_otdel, V, ro(H), H, M))*dt
		V = V + dv
		H = H + V*dt
		
		M = Mtek(i, t_otdel, m_zond, m_start, m_fuel)

		if H>=0:
			resultV.append(V)
			resultH.append(H)
			resultI.append(I)

		if H0 < H < H1:
			ttr = ttr + dt

		if type(i) == int:
			print("i:", i, " V: ", V, " H: ", H, " X: ", X(V, ro(H), H, i), " ro: ", ro(H))
			print()

		i = i + dt
		#print (i)
	print (ttr)

	#graf_plot(resultV, resultH, resultI)
 
if __name__== "__main__":
	main()

	
	#plt.

	#pp = ro(500)
	#print (pp)

	#radius = 2
	#print('Площадь окружности с радиусом 2 равна:', math.exp(18) * (radius ** 2))
 
print("Guru99")
