import matplotlib.patches as mpatches
from matplotlib import pyplot as plt

plt.rcParams['image.cmap'] = 'gray'

import numpy as np
from skimage import io, filters
from skimage.feature import hog
import cv2
import os


################################################
## Reduccion de dimensionalidad para Hu y HOG ##
################################################
def escala_grises(image):
    gris = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gris


def normalizacion(image):
    image = cv2.resize(image, (500, 400))
    return image


def gaussian(image):
    image = cv2.GaussianBlur(image, (3, 3), 0)
    return image


def sobel(image):
    image = filters.sobel(image)
    return image


# HOG: Histograma de gradientes orientados
def histograma_hog(image):
    caracteristica = hog(image, block_norm='L2-Hys').ravel()
    return caracteristica


# Momentos de Hu
def hu(image):
    caracteristica = cv2.HuMoments(cv2.moments(image)).flatten()
    return caracteristica


# Cargar path de las imagenes
tornillo_path = './ejemplos/cortadas/Tornillos/'
tuerca_path = './ejemplos/cortadas/Tuercas/'
arandela_path = './ejemplos/cortadas/Arandelas/'
clavo_path = './ejemplos/cortadas/Clavos/'

# Cargar todas las imagenes dentro de una carpeta
tornillo = []
for image_path in os.listdir(tornillo_path):
    img = cv2.imread(tornillo_path + image_path)
    tornillo.append(img)

tuerca = []
for image_path in os.listdir(tuerca_path):
    img = cv2.imread(tuerca_path + image_path)
    tuerca.append(img)

arandela = []
for image_path in os.listdir(arandela_path):
    img = cv2.imread(arandela_path + image_path)
    arandela.append(img)

clavo = []
for image_path in os.listdir(clavo_path):
    img = cv2.imread(clavo_path + image_path)
    clavo.append(img)

# Set listas para guardar cada proceso asignado a cada imagen
tornillo_gray = []
tornillo_n = []
tornillo_edge = []

tuerca_gray = []
tuerca_n = []
tuerca_edge = []

arandela_gray = []
arandela_n = []
arandela_edge = []

clavo_gray = []
clavo_n = []
clavo_edge = []

i = 0
for i in range(0, len(tornillo)):
    aux = normalizacion(tornillo[i])
    # aux = gaussian(aux)
    tornillo_n.append(aux)
    tornillo_gray.append(escala_grises(tornillo_n[i]))
    tornillo_edge.append(sobel(tornillo_gray[i]))

i = 0
for i in range(0, len(tuerca)):
    aux = normalizacion(tuerca[i])
    # aux = gaussian(aux)
    tuerca_n.append(aux)
    tuerca_gray.append(escala_grises(tuerca_n[i]))
    tuerca_edge.append(sobel(tuerca_gray[i]))

i = 0
for i in range(0, len(arandela)):
    aux = normalizacion(arandela[i])
    # aux = gaussian(aux)
    arandela_n.append(aux)
    arandela_gray.append(escala_grises(arandela_n[i]))
    arandela_edge.append(sobel(arandela_gray[i]))

i = 0
for i in range(0, len(clavo)):
    aux = normalizacion(clavo[i])
    # aux = gaussian(aux)
    clavo_n.append(aux)
    clavo_gray.append(escala_grises(clavo_n[i]))
    clavo_edge.append(sobel(clavo_gray[i]))

"""
Estadisticas
Analizar la frecuencia de aparicion para cada pieza.
Hacemos uso de la media aritmetica y la desviacion estandar
"""


def estadistica(array):
    sum = 0
    for value in array:
        sum += value
    media = sum / len(array)
    sum = 0
    for value in array:
        sum += np.power((value - media), 2)
    desviacion = np.sqrt(sum / (len(array) - 1))

    return media, desviacion


##############################################
## HOG: Histograma de gradientes orientados ##
##############################################
grafico_hog, ax = plt.subplots()

for objeto in tornillo_gray:
    tornillo_fhog = histograma_hog(objeto)
    media, desviacion = estadistica(tornillo_fhog)
    ax.plot(media, desviacion, 'o', color='yellow')

for objeto in tuerca_gray:
    tuerca_fhog = histograma_hog(objeto)
    media, desviacion = estadistica(tuerca_fhog)
    ax.plot(media, desviacion, 'o', color='red')

for objeto in arandela_gray:
    arandela_fhog = histograma_hog(objeto)
    media, desviacion = estadistica(arandela_fhog)
    ax.plot(media, desviacion, 'o', color='blue')

for objeto in clavo_gray:
    clavo_fhog = histograma_hog(objeto)
    media, desviacion = estadistica(clavo_fhog)
    ax.plot(media, desviacion, 'o', color='green')

ax.grid(True)
ax.set_title("Reduccion de dimensionalidad para HOG")

yellow_patch = mpatches.Patch(color='yellow', label='Tornillo')
red_patch = mpatches.Patch(color='red', label='Tuerca')
blue_patch = mpatches.Patch(color='blue', label='Arandela')
green_patch = mpatches.Patch(color='green', label='Clavo')

plt.legend(handles=[yellow_patch, red_patch, blue_patch, green_patch])

plt.ylabel('Desviacion estandar')
plt.xlabel('Media aritmetica')

# Guardar resultados
plt.savefig("./pruebas/5_reduccion/reduccion_dimensionalidad_hog.jpg")

####################
## Momentos de Hu ##
####################
grafico_hu, ax = plt.subplots()

for objeto in tornillo_edge:
    tornillo_fhm = hu(objeto)
    media, desviacion = estadistica(tornillo_fhm)
    ax.plot(media, desviacion, 'o', color='yellow')

for objeto in tuerca_edge:
    tuerca_fhm = hu(objeto)
    media, desviacion = estadistica(tuerca_fhm)
    ax.plot(media, desviacion, 'o', color='red')

for objeto in arandela_edge:
    arandela_fhm = hu(objeto)
    media, desviacion = estadistica(arandela_fhm)
    ax.plot(media, desviacion, 'o', color='blue')

for objeto in clavo_edge:
    clavo_fhm = hu(objeto)
    media, desviacion = estadistica(clavo_fhm)
    ax.plot(media, desviacion, 'o', color='green')

ax.grid(True)
ax.set_title("Reduccion de Dimensionalidad para Hu")

yellow_patch = mpatches.Patch(color='yellow', label='Tornillo')
red_patch = mpatches.Patch(color='red', label='Tuerca')
blue_patch = mpatches.Patch(color='blue', label='Arandela')
green_patch = mpatches.Patch(color='green', label='Clavo')
plt.legend(handles=[yellow_patch, red_patch, blue_patch, green_patch])

plt.ylabel('Desviacion estandar')
plt.xlabel('Media aritmetica')

# Guardar resultados
plt.savefig("./pruebas/5_reduccion/reduccion_dimensionalidad_hu.jpg")
