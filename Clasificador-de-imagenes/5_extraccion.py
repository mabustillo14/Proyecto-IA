from matplotlib import pyplot as plt
plt.rcParams['image.cmap'] = 'gray'

import os
from skimage import filters
import cv2
from skimage.feature import hog


####################################################################
## Representacion de Histograma de color para una imagen filtrada ##
####################################################################

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


img = cv2.imread('./ejemplos/arandela_internet.jpg')
tornillo = escala_grises(img)
tornillo = normalizacion(tornillo)

bg = gaussian(tornillo)
bc = sobel(bg)

fig, (ax2, ax1, ax0) = plt.subplots(1, 3, figsize=(16, 5))
ax0.imshow(bc)
ax0.hlines(bc.shape[0] // 2, 0, bc.shape[1], color='C3')
ax0.set_title('Filtro Gauss + Sobel')
ax1.plot(bc[bc.shape[0] // 2, :], color='C3')
ax1.set_title('Linea divisoria central')

ax2.hist(bc.ravel(), bins=32, range=[0, 256], color='C3')
ax2.set_xlim(0, 256)
ax2.set_title('Histograma de color para imagen filtrada')

# Guardar resultados
plt.savefig("./pruebas/5_extraccion/histograma_color.jpg")

###############################################################################################
## Comparacion de caracteristicas HOG y HU para las distintas piezas de ferreteria ##
###############################################################################################

# Cargar path de las imagenes
tornillo_path = './ejemplos/no_cortadas/Tornillos/'
tuerca_path = './ejemplos/no_cortadas/Tuercas/'
arandela_path = './ejemplos/no_cortadas/Arandelas/'
clavo_path = './ejemplos/no_cortadas/Clavos/'

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


def histograma_hog(image):
    caracteristica = hog(image, block_norm='L2-Hys').ravel()
    return caracteristica


# Entre 5 arandelas distintos
print("\nHOG: Entre 5 arandelas distintos")
for j in range(5):
    print(histograma_hog(arandela_gray[j]))

# Entre 5 clavos distintos
print("\nHOG: Entre 5 clavos distintos")
for j in range(5):
    print(histograma_hog(clavo_gray[j]))

# Entre 5 tornillos distintos
print("\nHOG: Entre 5 tornillos distintos")
for j in range(5):
    print(histograma_hog(tornillo_gray[j]))

# Entre 5 tuercas distintos
print("\nHOG: Entre 5 tuercas distintos")
for j in range(5):
    print(histograma_hog(tuerca_gray[j]))

# Entre tornillo, tuerca, arandela y clavo
print("\nHOG: Entre tornillo, clavo, tuerca y arandela")
print(histograma_hog(tornillo_gray[0]))
print(histograma_hog(clavo_gray[0]))
print(histograma_hog(tuerca_gray[0]))
print(histograma_hog(arandela_gray[0]))

####################
## Momentos de Hu ##
####################


def hu(image):
    caracteristica = cv2.HuMoments(cv2.moments(image)).flatten()
    return caracteristica


# Entre 5 arandelas distintos
print("\nHU: Entre 5 arandelas distintos")
print(hu(arandela_edge[0]))
print(hu(arandela_edge[1]))
print(hu(arandela_edge[2]))
print(hu(arandela_edge[3]))
print(hu(arandela_edge[4]))

# Entre 5 clavos distintos
print("\nHU: Entre 5 clavos distintos")
print(hu(clavo_edge[0]))
print(hu(clavo_edge[1]))
print(hu(clavo_edge[2]))
print(hu(clavo_edge[3]))
print(hu(clavo_edge[4]))

# Entre 5 tornillos distintos
print("\nHU: Entre 5 tornillos distintos")
print(hu(tornillo_edge[0]))
print(hu(tornillo_edge[1]))
print(hu(tornillo_edge[2]))
print(hu(tornillo_edge[3]))
print(hu(tornillo_edge[4]))

# Entre 5 tuercas distintos
print("\nHU: Entre 5 tuercas distintos")
print(hu(tuerca_edge[0]))
print(hu(tuerca_edge[1]))
print(hu(tuerca_edge[2]))
print(hu(tuerca_edge[3]))
print(hu(tuerca_edge[4]))

# Entre tornillo, tuerca, arandela y clavo
print("\nHU: Entre tornillo, tuerca, arandela y clavo")
print(hu(tornillo_edge[0]))
print(hu(tuerca_edge[0]))
print(hu(arandela_edge[0]))
print(hu(clavo_edge[0]))
