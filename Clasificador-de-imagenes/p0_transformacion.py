from matplotlib import pyplot as plt
plt.rcParams['image.cmap'] = 'gray'

from skimage import io
import cv2
import numpy as np
import os, sys

def Transformacion(nombre, input_path, output_path):
    ###########################
    ## Quitar linea de fondo ##
    ###########################
    #input_path = "ejemplos/arandela_original.jpg"
    input_path+=nombre
    imagen = cv2.imread(input_path)
    
    # Guardar el registro
    # cv2.imwrite("./pruebas/0_transformacion/foto_original.jpg", imagen)

    # Determinar dimensiones de la imagen
    height, width, channels = imagen.shape

    # x marca hasta donde cortar (osea corta del pixel 0 hasta 700)
    x = 50
    crop_img = imagen[0:height, x:width]

    # Guardar resultados
    # cv2.imwrite("./pruebas/0_transformacion/quitar_pared_caja.jpg", crop_img)

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

    # Codificación rígida del Rect. El objeto debe estar dentro de este rect.
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
    background[np.where((background > [100, 100, 100]).all(axis=2))] = [255, 255, 255] # 255 es blanco

    # Agregar el fondo y la imagen
    resized_image_sin_fondo = background + img1

    # Guardar resultados
    # cv2.imwrite("./pruebas/0_transformacion/quitar_pared_caja_sin_fondo.jpg", resized_image_sin_fondo)
    
    ##############################
    ## Redimension de la imagen ##
    ##############################

    # Redimensionamiento de la imagen de entrada
    fixed_size = tuple((500, 400))
    resized_image = cv2.resize(resized_image_sin_fondo, fixed_size)

    # Guardar resultados
    # cv2.imwrite("./pruebas/0_transformacion/quitar_pared_caja_sin_fondo_redimensionada.jpg", resized_image)
    cv2.imwrite(output_path + nombre, resized_image)

    #################################
    ## Recorte de sombra detectada ##
    #################################

    imagen = cv2.imread(output_path + nombre)

    # Determinar dimensiones de la imagen
    height, width, channels = imagen.shape

    # x marca hasta donde cortar (osea corta del pixel 0 hasta 500)
    # y se corta desde 0 hasta el pixel height-y
    y = 100
    crop_img = imagen[0:height-y, 0:width]
    cv2.imwrite(output_path + nombre, crop_img)
    # cv2.imwrite("./pruebas/0_transformacion/quitar_pared_caja_sin_fondo_redimensionada_recortada.jpg", crop_img)



if __name__ == '__main__':  # Para que se pueda usar sin interfaz
    input_path="./dataset/original/train/"
    carpetas = os.listdir( input_path ) # Obtener el nombre de los archivos en ese path
    #0-Arandelas 1-Clavos 2-Tornillos 3-Tuercas
    #carpetas = ["Arandelas"]
    #carpetas = ["Clavos"]
    #carpetas = ["Tornillos"]
    #carpetas = ["Tuercas"]

    # Para transformar todas las carpetas de fotos
    for i in range(len(carpetas)):
        input_path = "./dataset/original/train/" + carpetas[i] +"/"
        output_path = "./dataset/transformado/train/" + carpetas[i] +"/"
        dirs_input = os.listdir(input_path)
        dirs_output = os.listdir(output_path)
        
        print("Se comenzo la transformación de :", carpetas[i])

        for j in range(len(dirs_output)): # Se revisa si ya hay una imagen en output con el nombre del input, sino lo añade a una lista
            dirs_input = list(filter((dirs_output[j]).__ne__, dirs_input))


        for file in dirs_input:
            Transformacion(file, input_path, output_path)
            print(file) # Muestra el nombre de la imagen que ya se transformo
        
        print(carpetas[i], " Transformada")    
    