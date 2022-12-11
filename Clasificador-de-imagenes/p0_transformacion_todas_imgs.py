import cv2
import numpy as np
import os


def transformacion(image):
    """
    QUITAR PARED DE LA CAJA EN LA IMAGEN
    """
    # Determinar dimensiones de la imagen
    height, width, channels = image.shape

    # x marca hasta donde cortar (osea corta del pixel 0 hasta 700)
    x = 700
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

    return image_sin_fondo

"""
TRANSFORMACION DE TODAS LAS IMAGENES
"""

input_path = "./dataset/original/"
output_path = "./dataset/transformado/"
opciones = ["test/", "train/"]
elementos = ["Arandelas", "Clavos", "Tornillos", "Tuercas"]

for opcion in opciones:
    folder_path = input_path + opcion

    for elemento in elementos:
        path_a_analizar = folder_path + elemento

        # Listar todos los archivos en esta carpeta
        files = os.listdir(path_a_analizar)

        # Listar todas las imagenes y transformarlas
        for file in files:
            # Transformar imagen
            img = cv2.imread(path_a_analizar + file)
            img_transformada = transformacion(img)

            # Guardar imagen transformada en la nueva carpeta
            cv2.imwrite(output_path + opcion + elemento + file, img_transformada)
