from matplotlib import pyplot as plt
plt.rcParams['image.cmap'] = 'gray'

from skimage import io
import cv2
import numpy as np

###########################
## Quitar linea de fondo ##
###########################
path = "ejemplos/arandela_original.jpg"
imagen = cv2.imread(path)

# Determinar dimensiones de la imagen
height, width, channels = imagen.shape

# x marca hasta donde cortar (osea corta del pixel 0 hasta 700)
x = 700
crop_img = imagen[0:height, x:width]

# Guardar resultados
cv2.imwrite("./pruebas/0_transformacion/quitar_pared_caja.jpg", crop_img)

################################################################
## Quitar fondo: convertir el fondo a fondo totalmente blanco ##
################################################################

# Determinar dimensiones de la imagen
height, width, channels = crop_img.shape

# Crear una mascara
mask = np.zeros(crop_img.shape[:2], np.uint8)

# Grabar el corte del objeto
bgdModel = np.zeros((1, 65), np.float64)
fgdModel = np.zeros((1, 65), np.float64)

# Hard Coding the Rect The object must lie within this rect.
rect = (1079, 1079, width - 1, height - 1)
cv2.grabCut(crop_img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
mask = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
img1 = crop_img * mask[:, :, np.newaxis]

# Obtener el fondo
background = crop_img - img1

"""
Cambiar todos los pixeles en el fondo que no sean de negro a blanco
[100,100,100] color de fondo (de la mascara) de la caja donde tome las fotos
"""
background[np.where((background > [100, 100, 100]).all(axis=2))] = [255, 255, 255]

# Agregar el fondo y la imagen
resized_image_sin_fondo = background + img1

# Guardar resultados
cv2.imwrite("./pruebas/0_transformacion/quitar_pared_caja_sin_fondo.jpg", resized_image_sin_fondo)

##############################
## Redimension de la imagen ##
##############################

# Redimensionamiento de la imagen de entrada
fixed_size = tuple((500, 400))
resized_image = cv2.resize(resized_image_sin_fondo, fixed_size)

# Guardar resultados
cv2.imwrite("./pruebas/0_transformacion/quitar_pared_caja_sin_fondo_redimensionada.jpg", resized_image)
