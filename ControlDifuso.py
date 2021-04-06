from matplotlib import pyplot as plt
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

#Definimos antecedentes y masa del objeto (kg)
m = 1
v0 = ctrl.Antecedent(np.arange(1, 5, 0.1), 'v0')
mew = ctrl.Antecedent(np.arange(0.1, 0.3, 0.01), 'mew')
xf = ctrl.Consequent(np.arange(0, 50, 0.1), 'xf')

#Separamos velocidades iniciales y coeficientes de fricción en 5 categorías
v0.automf(5)
mew.automf(5)
#Separamos manualmente las distancias en 6 categorías
xf['super close'] = fuzz.trimf(xf.universe, [0, 0, 10])
xf['very close'] = fuzz.trimf(xf.universe, [0, 10, 20])
xf['close'] = fuzz.trimf(xf.universe, [10, 20, 30])
xf['far'] = fuzz.trimf(xf.universe, [20, 30, 40])
xf['very far'] = fuzz.trimf(xf.universe, [30, 40, 50])
xf['super far'] = fuzz.trimf(xf.universe, [40, 50, 50])
#Reglas para coeficientes buenos
rule1 = ctrl.Rule(v0['poor'] & mew['good'], xf['super close'])
rule2 = ctrl.Rule(v0['mediocre'] & mew['good'], xf['super close'])
rule3 = ctrl.Rule(v0['average'] & mew['good'], xf['very close'])
rule4 = ctrl.Rule(v0['decent'] & mew['good'], xf['very close'])
rule5 = ctrl.Rule(v0['good'] & mew['good'], xf['close'])
#Reglas para coeficientes decentes
rule6 = ctrl.Rule(v0['poor'] & mew['decent'], xf['super close'])
rule7 = ctrl.Rule(v0['mediocre'] & mew['decent'], xf['super close'])
rule8 = ctrl.Rule(v0['average'] & mew['decent'], xf['very close'])
rule9 = ctrl.Rule(v0['decent'] & mew['decent'], xf['very close'])
rule10= ctrl.Rule(v0['good'] & mew['decent'], xf['close'])
#Reglas para coeficientes promedio
rule11= ctrl.Rule(v0['poor'] & mew['average'], xf['super close'])
rule12= ctrl.Rule(v0['mediocre'] & mew['average'], xf['very close'])
rule13= ctrl.Rule(v0['average'] & mew['average'], xf['close'])
rule14= ctrl.Rule(v0['decent'] & mew['average'], xf['close'])
rule15= ctrl.Rule(v0['good'] & mew['average'], xf['far'])
#Reglas para coeficientes mediocres
rule16= ctrl.Rule(v0['poor'] & mew['mediocre'], xf['super close'])
rule17= ctrl.Rule(v0['mediocre'] & mew['mediocre'], xf['super close'])
rule18= ctrl.Rule(v0['average'] & mew['mediocre'], xf['very close'])
rule19= ctrl.Rule(v0['decent'] & mew['mediocre'], xf['close'])
rule20= ctrl.Rule(v0['good'] & mew['mediocre'], xf['close'])
#Reglas para coeficientes bajos
rule21= ctrl.Rule(v0['poor'] & mew['poor'], xf['very close'])
rule22= ctrl.Rule(v0['mediocre'] & mew['poor'], xf['close'])
rule23= ctrl.Rule(v0['average'] & mew['poor'], xf['far'])
rule24= ctrl.Rule(v0['decent'] & mew['poor'], xf['very far'])
rule25= ctrl.Rule(v0['good'] & mew['poor'], xf['super far'])
#Se juntan las reglas en el sistema y se simula
xf_control= ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule7, rule8,rule9,rule10,rule11,rule12,rule13,rule14,rule15,rule16,rule17,rule18,rule19,rule20,rule21,rule22,rule23,rule24,rule25])
distance = ctrl.ControlSystemSimulation(xf_control)
#Generamos 3 figuras para graficar
fig = plt.figure()
ax1 = fig.add_subplot(131)
ax1.set_ylabel("Posición (μ = 0.1)")
ax1.set_xlabel("Velocidad Inicial")
ax2 = fig.add_subplot(132)
ax2.title.set_text("Posición final esperada (azul) vs Predicción (naranja)")
ax2.set_ylabel("Posición Final (μ = 0.2)")
ax2.set_xlabel("Velocidad Inicial")
ax3 = fig.add_subplot(133)
ax3.set_ylabel("Posición (μ = 0.3)")
ax3.set_xlabel("Velocidad Inicial")

#Comparamos distancias reales con los del sistema con μ = 0.1
v0_in = 1
real = []
difuse = []
mew_in = 0.1
while (v0_in<=5):
    distance.input['v0'] = v0_in
    distance.input['mew'] = mew_in
    distance.compute()
    real.append(v0_in * m / mew_in)
    difuse.append(distance.output['xf'])
    v0_in += 0.1
ax1.plot(real)
ax1.plot(difuse)

#Comparamos distancias reales con los del sistema con μ = 0.2
real.clear()
difuse.clear()
v0_in = 1
mew_in = 0.2
while (v0_in<=5):
    distance.input['v0'] = v0_in
    distance.input['mew'] = mew_in
    distance.compute()
    real.append(v0_in * m / mew_in)
    difuse.append(distance.output['xf'])
    v0_in += 0.1
ax2.plot(real)
ax2.plot(difuse)

#Comparamos distancias reales con los del sistema con μ = 0.3
real.clear()
difuse.clear()
v0_in = 1
mew_in = 0.3
while (v0_in<=5):
    distance.input['v0'] = v0_in
    distance.input['mew'] = mew_in
    distance.compute()
    real.append(v0_in * m / mew_in)
    difuse.append(distance.output['xf'])
    v0_in += 0.1
ax3.plot(real)
ax3.plot(difuse)
#Generamos la gráfica de los resultados
plt.show()