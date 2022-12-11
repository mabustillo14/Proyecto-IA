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

    # Determinar dimensiones de la imagen
    height, width, channels = imagen.shape

    # x marca hasta donde cortar (osea corta del pixel 0 hasta 700)
    x = 50
    crop_img = imagen[0:height, x:width]

    # Guardar resultados
    #cv2.imwrite("./pruebas/0_transformacion/quitar_pared_caja.jpg", crop_img)
    #cv2.imwrite(output_path, crop_img)


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
    #cv2.imwrite("./pruebas/0_transformacion/quitar_pared_caja_sin_fondo.jpg", resized_image_sin_fondo)
    
    ##############################
    ## Redimension de la imagen ##
    ##############################

    # Redimensionamiento de la imagen de entrada
    fixed_size = tuple((500, 400))
    resized_image = cv2.resize(resized_image_sin_fondo, fixed_size)

    # Guardar resultados
    #cv2.imwrite("./pruebas/0_transformacion/quitar_pared_caja_sin_fondo_redimensionada.jpg", resized_image)
    cv2.imwrite(output_path + nombre, resized_image)


    imagen = cv2.imread(output_path + nombre)

    # Determinar dimensiones de la imagen
    height, width, channels = imagen.shape

    # x marca hasta donde cortar (osea corta del pixel 0 hasta 700)
    y = 70
    crop_img = imagen[0:height-y, 0:width]
    cv2.imwrite(output_path + nombre, crop_img)



from rembg import remove
from PIL import Image
global contador
contador = 0
def sinFondo(nombre,input_path, output_path):

    global contador
    
    input_path += nombre
    output_path += "photo" + str(contador)+ ".png"
    contador += 1
    input = Image.open(input_path)
    output = remove(input)
    output.save(output_path)

    imagen = cv2.imread(output_path)
    # Redimensionamiento de la imagen de entrada
    fixed_size = tuple((500, 400))
    resized_image = cv2.resize(imagen, fixed_size)
    cv2.imwrite(output_path, resized_image)



if __name__ == '__main__':  # Para que se pueda usar sin interfaz
    input_path="./dataset/original/train/"
    carpetas = os.listdir( input_path )
    
    # This would print all the files and directories
    #for i in range(len(carpetas)):
    print(carpetas)
    input_path = "./dataset/original/train/" + carpetas[2] +"/"
    output_path = "./dataset/transformado/train/" + carpetas[2] +"/"
    dirs = os.listdir(input_path )
    for file in dirs:
            Transformacion(file, input_path, output_path)
            print(file)
    print(carpetas[1], " Transformada")    