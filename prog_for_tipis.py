import math
import numpy as np
#from matplotlib import pyplot as plt
from draw import draw_func as df

### Параметры в словарях
rocket_dict = {1: 'MH-300', 2: 'MP-12', 3: 'MP20', 4: 'Atea-1', 5: 'Mera', 6: 'KSR III', 7: 'KSR I', 8: 'Teya'}
m_zond_dict = {1: 150, 2: 50, 3: 100, 4: 2, 5: 13.5, 6: 140, 7: 120, 8: 25}
H0_dict = {1: 40000, 2: 40000, 3: 45000, 4: 40000, 5: 40000, 6: 40000, 7: 50000, 8: 55000}
H1_dict = {1: 120000, 2: 100000, 3: 115000, 4: 70000, 5: 85000, 6: 90000, 7: 150000, 8: 110000}
t_treb_dict = {1: 62, 2: 70, 3: 60, 4: 90, 5: 63, 6: 61, 7: 83, 8: 85}
m_start_dict = {1: 1500, 2: 1485, 3: 1620, 4: 60, 5: 58, 6: 6100, 7: 1200, 8: 440}
m_fuel_dict = {1: 1040, 2: 1061, 3: 1213, 4: 40, 5: 39, 6: 2296.67, 7: 800, 8: 294.2}
t_engine_dict = {1: 23, 2: 21, 3: 24, 4: 14.5, 5: 2, 6: 53, 7: 25, 8: 129.6}
w_dict = {1: 45.2, 2: 50.53, 3: 50.53, 4: 2.76, 5: 19.5, 6: 43.33, 7: 32, 8: 2.27}
I_dict = {1: 248, 2: 205, 3: 205, 4: 255, 5: 198, 6: 300, 7: 275, 8: 220}
D_before_dict = {1: 0.445, 2: 0.45, 3: 0.45, 4: 0.15, 5: 0.17, 6: 1, 7: 0.42, 8: 0.3}
D_after_dict = {1: 0.445, 2: 0.45, 3: 0.45, 4: 0.15, 5: 0.065, 6: 1, 7: 0.42, 8: 0.3}
#Cx_dict = {1: 0.2, 2: 0.2, 3: 0.2, 4: 0.2, 5: 0.2, 6: 0.2, 7: 0.2, 8: 0.2}
###

### прочие параметры
h0=0
p0=101325
#p0kg=1
g=9.8
Mmol=0.029
R=8.31
Cx=0.2
#T=273

#Ps=6612
#pkkg=0.9
###
"""
#m=1500
### параметры зонда
m_zond=150
#t_treb_in_mezosphere
###

### параметры ракеты
m_start=1500
m_fuel=1040

t_otdel=23# on zhe t raboti dvigatelya

D_before=0.445
D_after=0.445

Cx=0.2
#Sm=((D/2)**2)*3.14
#print(Sm)

I=248#ud imp
W=I*g
#Ssopla=(((100*D_before)/2)**2)*3.14
#print(Ssopla)

w=45.2#sek rash fuel
###

H0=40000
H1=120000

W=I*g
Ssopla=(((100*D_before)/2)**2)*3.14
print(Ssopla)
"""

resultV = []
resultH = []
resultI = []
resultS = []

def Sm(tx, h, v, D_before, D_after, t_otdel):
	if tx <= t_otdel:
		Sm=((D_before/2)**2)*3.14

	if tx > t_otdel:
		Sm=((D_after/2)**2)*3.14

	if tx > t_otdel:
		if h < 20000:
			if v < 0:
				Sm=(((D_after/2)**2)*3.14)*25

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

def P(h, W, Ssopla, w):
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

def X(v, ro, h, t_tek, D_before, D_after, t_otdel):
	return (Sm(t_tek, h, v, D_before, D_after, t_otdel)*Cx*(ro*v*v)/2)

def ft_func(t_tek, t_otdel, v, ro, h, m, D_before, D_after, W, Ssopla, w):
	if v>=0:
		if t_tek <= t_otdel:
			return ((P(h, W, Ssopla, w)-X(v, ro, h, t_tek, D_before, D_after, t_otdel)-(m*g))/m)
		elif t_tek >= t_otdel:
			return ((-X(v, ro, h, t_tek, D_before, D_after, t_otdel)-(m*g))/m)
	elif v<0:
		return ((X(v, ro, h, t_tek, D_before, D_after, t_otdel)-(m*g))/m)

"""def graf_plot(resultV, resultH, resultI):
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

	plt.show()"""

def main(m_zond, H0, H1, t_treb, m_start, m_fuel, t_engine, I, D_before, D_after, W, Ssopla, w,):
	print("Hello World!")

	t=1000
	dt=0.001

	V=0
	H=0
	M=m_start
	t_otdel=t_engine

	i=0
	ttr=0

	while i < t:
		dv = (ft_func(i, t_otdel, V, ro(H), H, M, D_before, D_after, W, Ssopla, w))*dt
		V = V + dv
		H = H + V*dt
		
		M = Mtek(i, t_otdel, m_zond, m_start, m_fuel)

		if H>=0:
			resultV.append(V)
			resultH.append(H)
			resultI.append(i)
			resultS.append(Sm(i, H, V, D_before, D_after, t_otdel))

		if H0 < H < H1:
			ttr = ttr + dt

		#if type(i) == int:
		#	print("i:", i, " V: ", V, " H: ", H, " X: ", X(V, ro(H), H, i, D_before, D_after, t_otdel), " ro: ", ro(H))
		#	print()

		i = i + dt
		#print (i)
	O_M='ttr: '+str(ttr)+', t_treb: '+str(t_treb)
	print (O_M)

	return ttr

	#graf_plot(resultV, resultH, resultI)

def work():
	i=1
	j=1
	#for i in range(1,8):#for zond
	#for j in range(1,1):#for rocket//8
	#zond Character
	m_zond=m_zond_dict[i]
	H0=H0_dict[i]
	H1=H1_dict[i]
	t_treb=t_treb_dict[i]
	#rocket Character
	m_start=m_start_dict[j]
	m_fuel=m_fuel_dict[j]
	t_engine=t_engine_dict[j]
	w=w_dict[j]
	I=I_dict[j]
	D_before=D_before_dict[j]
	D_after=D_after_dict[j]
	#Cx=Cx_dict[i]

	W=I*g
	Ssopla=(((100*D_before)/2)**2)*3.14
	#print(Ssopla)

	main(m_zond, H0, H1, t_treb, m_start, m_fuel, t_engine, I, D_before, D_after, W, Ssopla, w)
	rocket=rocket_dict[j]

	df(resultI, resultV, 'V for rocket: '+rocket)
	df(resultI, resultH, 'H for rocket: '+rocket)

def cowork():
	f=open('out_m.txt', 'w')
	f.write('1 - pravilo vupolnaetcya, 0 - pravilo ne vupolnaetcya\n')

	for i in range(1,9):#for zond
		for j in range(1,9):#for rocket//8
			#zond Character
			m_zond=m_zond_dict[i]
			H0=H0_dict[i]
			H1=H1_dict[i]
			t_treb=t_treb_dict[i]
			#rocket Character
			m_start=m_start_dict[j]
			m_fuel=m_fuel_dict[j]
			t_engine=t_engine_dict[j]
			w=w_dict[j]
			I=I_dict[j]
			D_before=D_before_dict[j]
			D_after=D_after_dict[j]
			#Cx=Cx_dict[i]

			W=I*g
			Ssopla=(((100*D_before)/2)**2)*3.14
			#print(Ssopla)

			t_z_in_int=main(m_zond, H0, H1, t_treb, m_start, m_fuel, t_engine, I, D_before, D_after, W, Ssopla, w)
			rocket=rocket_dict[j]

			index=0
			if t_z_in_int >= t_treb:
				index=1
			else:
				index=0

			out_message='if meteozond i: '+str(i)+' otpravitcya na rakete j: '+str(j)+' to index: '+str(index)
			print(out_message)
			f.write(out_message + '\n')

			#df(resultI, resultV, 'V for rocket: '+rocket)
			#df(resultI, resultH, 'H for rocket: '+rocket)

 
if __name__== "__main__":
	cowork()
	#main()

	#xx = [0.1, 0.2, 0.4, 0.8]
	#yy = [5, 6, 7, 8]
	#df(resultI, resultV, 'V')
	#df(resultI, resultH, 'H')

	#print(resultV)
	#plt.

	#pp = ro(500)
	#print (pp)

	#radius = 2
	#print('Площадь окружности с радиусом 2 равна:', math.exp(18) * (radius ** 2))
 
print("Guru99")

