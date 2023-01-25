from matplotlib import pyplot as plt
import matplotlib.patches as mpatches

plt.rcParams['image.cmap'] = 'gray'

from skimage import io, filters, img_as_ubyte
import numpy as np
import cv2
import os
from datetime import datetime
import random
from skimage.measure import regionprops
from skimage.feature import hog


# Determinar propiedades a una imagen recortada: Eje Menor, Eje Mayor, Momento de Hu 1, Excentricidad
def extraccion(image):

    """
    PRE PROCESAMIENTO
    """
    aux = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convertir a escala de grises

    """
    FILTRACION
    """
    aux = cv2.GaussianBlur(aux, (3, 3), 0)  # Aplicar filtro gaussiano
    aux = filters.sobel(aux)  # Aplicar filtro Sobel o Laplaciano

    """
    SEGMENTACION
    """
    ret, th = cv2.threshold(img_as_ubyte(aux), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    """
    EXTRACCION DE CARACTERISTICAS / PROPIEDADES
    """
    regions = regionprops(th.astype(int))

    # Propiedades
    eje_mayor = regions[0].major_axis_length
    eje_menor = regions[0].minor_axis_length
    excentricidad = regions[0].eccentricity
    hu = regions[0].moments_hu

    return [eje_menor, eje_mayor, hu[0], excentricidad]


"""
Estadisticas
Analizar la frecuencia de aparicion para cada pieza.
Hacemos uso de la media aritmetica y la desviacion estandar
"""

def estadistica(caracteristica):
    sum = 0
    for value in caracteristica:
        sum += value
    media = sum / len(caracteristica)
    sum = 0
    for value in caracteristica:
        sum += np.power((value - media),2)
    desviacion = np.power((sum/(len(caracteristica))),0.5)
    return media, desviacion


def estadisticaHOG(array): #Es una muestra, por eso N-1
    sum = 0
    for value in array:
        sum += value
    media = sum / len(array)
    sum = 0
    for value in array:
        sum += np.power((value - media), 2)
    desviacion = np.sqrt(sum / (len(array) - 1))
    return media, desviacion


"""
Reducción #1:
Eje Menor, Eje Mayor, Momento de Hu, Excentricidad
"""

# Cargar path de las imagenes
tornillo_path = './dataset/transformado/train/Tornillos/'
tuerca_path = './dataset/transformado/train/Tuercas/'
arandela_path = './dataset/transformado/train/Arandelas/'
clavo_path = './dataset/transformado/train/Clavos/'

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



###############
## Eje Menor ##
###############
grafico_ejeMenor, ax = plt.subplots()

ejeMenor = []
for objeto in tornillo:
    tornillo_fhm = extraccion(objeto)
    ejeMenor.append(tornillo_fhm[0])
    media, desviacion = estadistica(ejeMenor)
    ax.plot(media, desviacion, 'o', color='yellow')

ejeMenor = []
for objeto in tuerca:
    tuerca_fhog = extraccion(objeto)
    ejeMenor.append(tuerca_fhog[0])
    media, desviacion = estadistica(ejeMenor)
    ax.plot(media, desviacion, 'o', color='red')

ejeMenor = []
for objeto in arandela:
    arandela_fhog = extraccion(objeto)
    ejeMenor.append(arandela_fhog[0])
    media, desviacion = estadistica(ejeMenor)
    ax.plot(media, desviacion, 'o', color='blue')

ejeMenor = []
for objeto in clavo:
    clavo_fhog = extraccion(objeto)
    ejeMenor.append(clavo_fhog[0])
    media, desviacion = estadistica(ejeMenor)
    ax.plot(media, desviacion, 'o', color='green')

ax.grid(True)
ax.set_title("Reducción de Dimensionalidad para Eje Menor")

yellow_patch = mpatches.Patch(color='yellow', label='Tornillo')
red_patch = mpatches.Patch(color='red', label='Tuerca')
blue_patch = mpatches.Patch(color='blue', label='Arandela')
green_patch = mpatches.Patch(color='green', label='Clavo')
plt.legend(handles=[yellow_patch, red_patch, blue_patch, green_patch])

plt.ylabel('Desviación estandar')
plt.xlabel('Media aritmética')

# Guardar resultados
plt.savefig("./pruebas/6_reduccion/reduccion_dimensionalidad_ejeMenor.jpg")



###############
## Eje Mayor ##
###############
grafico_ejeMayor, ax = plt.subplots()

ejeMayor = []
for objeto in tornillo:
    tornillo_fhm = extraccion(objeto)
    ejeMayor.append(tornillo_fhm[1])
    media, desviacion = estadistica(ejeMayor)
    ax.plot(media, desviacion, 'o', color='yellow')

ejeMayor = []
for objeto in tuerca:
    tuerca_fhog = extraccion(objeto)
    ejeMayor.append(tuerca_fhog[1])
    media, desviacion = estadistica(ejeMayor)
    ax.plot(media, desviacion, 'o', color='red')

ejeMayor = []
for objeto in arandela:
    arandela_fhog = extraccion(objeto)
    ejeMayor.append(arandela_fhog[1])
    media, desviacion = estadistica(ejeMayor)
    ax.plot(media, desviacion, 'o', color='blue')

ejeMayor = []
for objeto in clavo:
    clavo_fhog = extraccion(objeto)
    ejeMayor.append(clavo_fhog[1])
    media, desviacion = estadistica(ejeMayor)
    ax.plot(media, desviacion, 'o', color='green')

ax.grid(True)
ax.set_title("Reducción de Dimensionalidad para Eje Mayor")

yellow_patch = mpatches.Patch(color='yellow', label='Tornillo')
red_patch = mpatches.Patch(color='red', label='Tuerca')
blue_patch = mpatches.Patch(color='blue', label='Arandela')
green_patch = mpatches.Patch(color='green', label='Clavo')
plt.legend(handles=[yellow_patch, red_patch, blue_patch, green_patch])

plt.ylabel('Desviación estandar')
plt.xlabel('Media aritmética')

# Guardar resultados
plt.savefig("./pruebas/6_reduccion/reduccion_dimensionalidad_ejeMayor.jpg")



####################
## Momentos de Hu ##
####################
grafico_hu, ax = plt.subplots()

Hu = []
for objeto in tornillo:
    tornillo_fhm = extraccion(objeto)
    Hu.append(tornillo_fhm[2])
    media, desviacion = estadistica(Hu)
    ax.plot(media, desviacion, 'o', color='yellow')

Hu = []
for objeto in tuerca:
    tuerca_fhog = extraccion(objeto)
    Hu.append(tuerca_fhog[2])
    media, desviacion = estadistica(Hu)
    ax.plot(media, desviacion, 'o', color='red')

Hu = []
for objeto in arandela:
    arandela_fhog = extraccion(objeto)
    Hu.append(arandela_fhog[2])
    media, desviacion = estadistica(Hu)
    ax.plot(media, desviacion, 'o', color='blue')

Hu = []
for objeto in clavo:
    clavo_fhog = extraccion(objeto)
    Hu.append(clavo_fhog[2])
    media, desviacion = estadistica(Hu)
    ax.plot(media, desviacion, 'o', color='green')

ax.grid(True)
ax.set_title("Reducción de Dimensionalidad para Hu 1")

yellow_patch = mpatches.Patch(color='yellow', label='Tornillo')
red_patch = mpatches.Patch(color='red', label='Tuerca')
blue_patch = mpatches.Patch(color='blue', label='Arandela')
green_patch = mpatches.Patch(color='green', label='Clavo')
plt.legend(handles=[yellow_patch, red_patch, blue_patch, green_patch])

plt.ylabel('Desviación estandar')
plt.xlabel('Media aritmética')

# Guardar resultados
plt.savefig("./pruebas/6_reduccion/reduccion_dimensionalidad_hu1.jpg")



####################
## Excentricidad ##
####################
grafico_excentricidad, ax = plt.subplots()

Exce = []
for objeto in tornillo:
    tornillo_fhm = extraccion(objeto)
    Exce.append(tornillo_fhm[3])
    media, desviacion = estadistica(Exce)
    ax.plot(media, desviacion, 'o', color='yellow')

Exce = []
for objeto in tuerca:
    tuerca_fhog = extraccion(objeto)
    Exce.append(tuerca_fhog[3])
    media, desviacion = estadistica(Exce)
    ax.plot(media, desviacion, 'o', color='red')

Exce = []
for objeto in arandela:
    arandela_fhog = extraccion(objeto)
    Exce.append(arandela_fhog[3])
    media, desviacion = estadistica(Exce)
    ax.plot(media, desviacion, 'o', color='blue')

Exce = []
for objeto in clavo:
    clavo_fhog = extraccion(objeto)
    Exce.append(clavo_fhog[3])
    media, desviacion = estadistica(Exce)
    ax.plot(media, desviacion, 'o', color='green')

ax.grid(True)
ax.set_title("Reducción de Dimensionalidad para Excentricidad")

yellow_patch = mpatches.Patch(color='yellow', label='Tornillo')
red_patch = mpatches.Patch(color='red', label='Tuerca')
blue_patch = mpatches.Patch(color='blue', label='Arandela')
green_patch = mpatches.Patch(color='green', label='Clavo')
plt.legend(handles=[yellow_patch, red_patch, blue_patch, green_patch])

plt.ylabel('Desviación estandar')
plt.xlabel('Media aritmética')

# Guardar resultados
plt.savefig("./pruebas/6_reduccion/reduccion_dimensionalidad_excentricidad.jpg")



"""
Reducción #2:
HOG
"""

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


##############################################
## HOG: Histograma de gradientes orientados ##
##############################################
grafico_hog, ax = plt.subplots()

for objeto in tornillo_gray:
    tornillo_fhog = histograma_hog(objeto)
    media, desviacion = estadisticaHOG(tornillo_fhog)
    ax.plot(media, desviacion, 'o', color='yellow')

for objeto in tuerca_gray:
    tuerca_fhog = histograma_hog(objeto)
    media, desviacion = estadisticaHOG(tuerca_fhog)
    ax.plot(media, desviacion, 'o', color='red')

for objeto in arandela_gray:
    arandela_fhog = histograma_hog(objeto)
    media, desviacion = estadisticaHOG(arandela_fhog)
    ax.plot(media, desviacion, 'o', color='blue')

for objeto in clavo_gray:
    clavo_fhog = histograma_hog(objeto)
    media, desviacion = estadisticaHOG(clavo_fhog)
    ax.plot(media, desviacion, 'o', color='green')

ax.grid(True)
ax.set_title("Reducción de dimensionalidad para HOG")

yellow_patch = mpatches.Patch(color='yellow', label='Tornillo')
red_patch = mpatches.Patch(color='red', label='Tuerca')
blue_patch = mpatches.Patch(color='blue', label='Arandela')
green_patch = mpatches.Patch(color='green', label='Clavo')

plt.legend(handles=[yellow_patch, red_patch, blue_patch, green_patch])

plt.ylabel('Desviación estandar')
plt.xlabel('Media aritmética')

# Guardar resultados
plt.savefig("./pruebas/6_reduccion/reduccion_dimensionalidad_hog.jpg")