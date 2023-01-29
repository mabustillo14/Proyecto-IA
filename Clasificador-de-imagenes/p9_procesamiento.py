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


"""
VARIABLES GLOBALES
Para almacenar los datos y graficar
"""
global datos, fig, ax
datos = [] # Base de datos
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


def transformacion(image):
    """
    QUITAR PARED DE LA CAJA EN LA IMAGEN
    """
    # Determinar dimensiones de la imagen
    height, width, channels = image.shape

    # x marca hasta donde cortar (osea corta del pixel 0 hasta 700)
    x = 50
    crop_img = image[0:height, x:width]

    """
    QUITAR EL FONDO
    Convertir el fondo a fondo totalmente blanco
    """
    # Determinar nuevamente las dimensiones de la imagen
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
    image_sin_fondo = background + img1


    # Redimensionamiento de la imagen de entrada
    fixed_size = tuple((500, 400))
    resized_image = cv2.resize(image_sin_fondo, fixed_size)

    # Determinar dimensiones de la imagen
    height, width, channels = resized_image.shape

    # x marca hasta donde cortar (osea corta del pixel 0 hasta 700)
    y = 100
    crop_img = resized_image[0:height-y, 0:width]
    
    return crop_img



def extraccion(image, hacer_transformacion=False):
    """
    TRANSFORMACION
    """
    if hacer_transformacion:
        image = transformacion(image)
        cv2.imwrite("./pruebas/9_procesamiento/1_transformacion.jpg", image)

    """
    REDIMENSIONAMIENTO DE LA IMAGEN
    Convertir la imagen de 1220x1080 a 500x400
    """
    image = cv2.resize(image, (500, 400))
    cv2.imwrite("./pruebas/9_procesamiento/2_redimensionada.jpg", image)

    """
    PRE PROCESAMIENTO
    """
    aux = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convertir a escala de grises
    cv2.imwrite("./pruebas/9_procesamiento/3_preprocesamiento.jpg", aux)

    """
    FILTRACION
    """
    aux = cv2.GaussianBlur(aux, (3, 3), 0)  # Aplicar filtro gaussiano
    cv2.imwrite("./pruebas/9_procesamiento/4_filtro_Gauss.jpg", aux)
    aux = filters.sobel(aux)  # Aplicar filtro Sobel o Laplaciano
    cv2.imwrite("./pruebas/9_procesamiento/4_filtro_Sobel.jpg", aux)

    """
    SEGMENTACION
    """
    ret, th = cv2.threshold(img_as_ubyte(aux), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    cv2.imwrite("./pruebas/9_procesamiento/5_segmentacion.jpg", th)

    """
    EXTRACCION DE CARACTERISTICAS / PROPIEDADES
    """
    regions = regionprops(th.astype(int))

    # Propiedades
    #perimetro = regions[0].perimeter
    #excentricidad = regions[0].eccentricity
    #equivalent_diameter = regions[0].equivalent_diameter
    #euler_number = regions[0].euler_number
    #solidity = regions[0].solidity
    #prueba = regions[0].bbox_area
    #area = regions[0].area
    eje_mayor = regions[0].major_axis_length
    eje_menor = regions[0].minor_axis_length
    hu = regions[0].moments_hu

    # RETORNAR VALORES
    # Otras combinaciones - No validas por rendimiento
    #return aux, [hu[0], perimetro, area]
    #return aux, [hu[0], hu[1], hu[3]]
    #return aux, [eje_menor, eje_mayor, hu[3]]
    #return aux, [eje_menor, hu[0], excentricidad ]

    #COMBINACIONES QUE FUNCIONAN CON EFICIENCIA
    #return aux, [eje_menor, eje_mayor, excentricidad]
    return aux, [eje_menor, eje_mayor, hu[0]]

if __name__ == '__main__':  # Para que se pueda usar sin interfaz
    path = nombre = './dataset/evaluacion/photo' + str(16) + '.jpg'
    image = cv2.imread(path)
    cv2.imwrite("./pruebas/9_procesamiento/0_imagen_original.jpg", image)
    imagen, caracteristica = extraccion(image, hacer_transformacion=True)