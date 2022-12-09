from matplotlib import pyplot as plt

plt.rcParams['image.cmap'] = 'gray'  # Si no le pusiera esto me quedaria fondo amarillo y lineas violeta

import numpy as np
import cv2
from skimage import color, img_as_float
from PIL import Image

# Imagen a analizar
prueba = './ejemplos/tornillo_prueba.jpg'

###################################################################
## Descomposicion de una imagen en una tupla de valores R, G y B ##
###################################################################

# Cargar imagen
tornillo = cv2.imread(prueba)

# Redimensionamiento de la imagen de entrada
fixed_size = tuple((500, 400))
tornillo = cv2.resize(tornillo, fixed_size)

# Descomposicion de la imagen en matrices correspondientes a las 3 capas RGB previamente mencionadas.
R_tornillo = tornillo[:, :, 0]
G_tornillo = tornillo[:, :, 1]
B_tornillo = tornillo[:, :, 2]

f, axes = plt.subplots(1, 4, figsize=(16, 5))

for ax in axes:
    ax.axis('off')

(ax_color, ax_B, ax_G, ax_R) = axes

ax_color.imshow(np.stack([R_tornillo, G_tornillo, B_tornillo], axis=2))
ax_color.set_title('Las 3 capas Superpuestas')

ax_B.imshow(B_tornillo)
ax_B.set_title('Capa Azul')

ax_R.imshow(R_tornillo)
ax_R.set_title('Capa Roja')

ax_G.imshow(G_tornillo)
ax_G.set_title('Capa Verde')

# Guardar resultados
plt.savefig("./pruebas/0_preprocesamiento/descomposion_rgb.jpg")

################################################################
## Conversion de RGB a escalas de grises utilizando librerías ##
################################################################
# https://pythoneyes.wordpress.com/2017/05/22/conversion-de-imagenes-rgb-a-escala-de-grises/

# Cargar imagen
tornillo = cv2.imread(prueba)

# Redimensionamiento de la imagen de entrada
fixed_size = tuple((500, 400))
tornillo = cv2.resize(tornillo, fixed_size)

# Conversion a escalas de grises haciendo uso del modulo de skimage
tornillo_float = img_as_float(tornillo)
sk_gray = color.rgb2gray(tornillo_float)

"""
También se puede modificar manualmente los pesos de cada color en vez de utilizar los propuestos por la libreria
Acá se colocan el mismo peso para los tres [1/3 1/3 1/3]
"""
f, (ax1, ax0) = plt.subplots(1, 2, figsize=(16, 5))

ax1.imshow(tornillo)
ax1.set_title('Original')

ax0.imshow(sk_gray)
# Nota: WG, WB y WR son los coeficientes que definen la transformacion
ax0.set_title('WG, WB y WR por skimage')

# Guardar resultados
plt.savefig("./pruebas/0_preprocesamiento/descomposion_rgb_con_libreria.jpg")

###########################################################################################################
## Conversion de RGB a escalas de grises utilizando pesos WG, WR y WB arbitrarios ingresados manualmente ##
###########################################################################################################
# https://pythoneyes.wordpress.com/2017/05/22/conversion-de-imagenes-rgb-a-escala-de-grises/

# Cargar imagen
foto = Image.open(prueba)
datos = foto.getdata()

# Para el calculo del promedio se utilizara la division entera con el operador de division doble "//" para evitar decimales
promedio = [(datos[x][0] + datos[x][1] + datos[x][2]) // 3 for x in range(len(datos))]

imagen_gris = Image.new('L', foto.size)
imagen_gris.putdata(promedio)

# Guardar resultados
imagen_gris.save("./pruebas/0_preprocesamiento/descomposion_rgb_promediados.jpg")
