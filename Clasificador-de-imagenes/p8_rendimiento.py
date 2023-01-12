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
datos = []
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

    """
    REDIMENSIONAMIENTO DE LA IMAGEN
    Convertir la imagen de 1220x1080 a 500x400
    """
    image = cv2.resize(image, (500, 400))

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


def generar_base_datos():
    print("\n--------------------------------------------------------------------")
    print("Comienza carga de Data Base")
    print("--------------------------------------------------------------------\n")
    global fig
    global ax
    global datos
    datos = []

    # Elemento de ferreteria
    class Elemento:
        def __init__(self):
            self.pieza = None
            self.image = None
            self.caracteristica = []
            self.distancia = 0

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

    i = 0
    # Analisis de tornillos
    iter = 0
    for objeto in tornillo:
        datos.append(Elemento())
        datos[i].pieza = 'Tornillo'
        datos[i].image, datos[i].caracteristica = extraccion(objeto)
        ax.scatter(datos[i].caracteristica[0], datos[i].caracteristica[1], datos[i].caracteristica[2], c='y',
                   marker='o')
        i += 1
        iter += 1
    print("Tornillos OK")

    # Analisis de tuercas
    iter = 0
    for objeto in tuerca:
        datos.append(Elemento())
        datos[i].pieza = 'Tuerca'
        datos[i].image, datos[i].caracteristica = extraccion(objeto)
        ax.scatter(datos[i].caracteristica[0], datos[i].caracteristica[1], datos[i].caracteristica[2], c='r',
                   marker='o')
        i += 1
        iter += 1
    print("Tuercas OK")

    # Analisis de arandelas
    iter = 0
    for objeto in arandela:
        datos.append(Elemento())
        datos[i].pieza = 'Arandela'
        datos[i].image, datos[i].caracteristica = extraccion(objeto)
        ax.scatter(datos[i].caracteristica[0], datos[i].caracteristica[1], datos[i].caracteristica[2], c='b',
                   marker='o')
        i += 1
        iter += 1
    print("Arandelas OK")

    # Analisis de clavos
    iter = 0
    for objeto in clavo:
        datos.append(Elemento())
        datos[i].pieza = 'Clavo'
        datos[i].image, datos[i].caracteristica = extraccion(objeto)
        ax.scatter(datos[i].caracteristica[0], datos[i].caracteristica[1], datos[i].caracteristica[2], c='g',
                   marker='o')
        i += 1
        iter += 1
    print("Clavos OK")

    print("Analisis completo de la base de datos de Train")
    print("Cantidad de imagenes analizadas: ", len(datos))

    # Elemento a evaluar
    test = Elemento()

    print("--------------------------------------------------------------------\n")
    return test


def clasifica(image, test):
    
    respuesta = []
    global fig
    global ax
    global datos
    global contador_cajas

    test.image, test.caracteristica = extraccion(image, hacer_transformacion=True)
    test.pieza = 'Arandela'  # label inicial

    """
    KNN: K Nearest Neighbors
    """
    #print("\nInicializacion KNN")
    i = 0
    sum = 0
    for ft in datos[0].caracteristica:
        sum = sum + np.power(np.abs(test.caracteristica[i] - ft), 2)
        i += 1
    d = np.sqrt(sum)

    for element in datos:
        sum = 0
        i = 0
        for ft in element.caracteristica:
            sum = sum + np.power(np.abs((test.caracteristica[i]) - ft), 2)
            i += 1

        element.distancia = np.sqrt(sum)

        if sum < d:
            d = sum
            test.pieza = element.pieza

    #print("Prediccion para KNN con K=1: ", test.pieza)
    KNN = test.pieza

    """
    BUBBLE SORT: Algoritmo de ordenamiento de burbuja
    Lo elegi porque es bastante estable
    """
    swap = True
    while swap:
        swap = False
        for i in range(1, len(datos) - 1):
            if datos[i - 1].distancia > datos[i].distancia:
                aux = datos[i]
                datos[i] = datos[i - 1]
                datos[i - 1] = aux
                swap = True

    """
    K MEANS
    """
    #print("\nInicializacion KMeans")

    tornillo_data = []
    tuerca_data = []
    arandela_data = []
    clavo_data = []

    for element in datos:
        if element.pieza == 'Tornillo':
            tornillo_data.append(element)
        if element.pieza == 'Tuerca':
            tuerca_data.append(element)
        if element.pieza == 'Arandela':
            arandela_data.append(element)
        if element.pieza == 'Clavo':
            clavo_data.append(element)

    tornillo_mean = list(random.choice(tornillo_data).caracteristica)
    tuerca_mean = list(random.choice(tuerca_data).caracteristica)
    arandela_mean = list(random.choice(arandela_data).caracteristica)
    clavo_mean = list(random.choice(clavo_data).caracteristica)

    # Asignacion, Actualizacion y Convergencia
    tornillo_len = [0, 0, 0]
    tuerca_len = [0, 0, 0]
    arandela_len = [0, 0, 0]
    clavo_len = [0, 0, 0]

    iter = 0
    while iter < 20:

        tornillo_data = []
        tuerca_data = []
        arandela_data = []
        clavo_data = []

        # Asignacion
        for element in datos:
            sum_tornillo = 0
            sum_tuerca = 0
            sum_arandela = 0
            sum_clavo = 0

            for i in range(0, len(element.caracteristica) - 1):
                sum_tornillo += np.power(np.abs(tornillo_mean[i] - element.caracteristica[i]), 2)
                sum_tuerca += np.power(np.abs(tuerca_mean[i] - element.caracteristica[i]), 2)
                sum_arandela += np.power(np.abs(arandela_mean[i] - element.caracteristica[i]), 2)
                sum_clavo += np.power(np.abs(clavo_mean[i] - element.caracteristica[i]), 2)

            dist_tornillo = np.sqrt(sum_tornillo)
            dist_tuerca = np.sqrt(sum_tuerca)
            dist_arandela = np.sqrt(sum_arandela)
            dist_clavo = np.sqrt(sum_clavo)

            aux = dist_tornillo
            if dist_tuerca < aux:
                aux = dist_tuerca
            if dist_arandela < aux:
                aux = dist_arandela
            if dist_clavo < aux:
                aux = dist_clavo

            if aux == dist_tornillo:
                tornillo_data.append(element.caracteristica)
            elif aux == dist_tuerca:
                tuerca_data.append(element.caracteristica)
            elif aux == dist_arandela:
                arandela_data.append(element.caracteristica)
            elif aux == dist_clavo:
                clavo_data.append(element.caracteristica)

        # Actualizacion
        sum_tornillo = [0, 0, 0]
        for b in tornillo_data:
            sum_tornillo[0] += b[0]
            sum_tornillo[1] += b[1]
            sum_tornillo[2] += b[2]

        sum_tuerca = [0, 0, 0]
        for o in tuerca_data:
            sum_tuerca[0] += o[0]
            sum_tuerca[1] += o[1]
            sum_tuerca[2] += o[2]

        sum_arandela = [0, 0, 0]
        for l in arandela_data:
            sum_arandela[0] += l[0]
            sum_arandela[1] += l[1]
            sum_arandela[2] += l[2]

        sum_clavo = [0, 0, 0]
        for p in clavo_data:
            sum_clavo[0] += p[0]
            sum_clavo[1] += p[1]
            sum_clavo[2] += p[2]

        tornillo_mean[0] = sum_tornillo[0] / len(tornillo_data)
        tornillo_mean[1] = sum_tornillo[1] / len(tornillo_data)
        tornillo_mean[2] = sum_tornillo[2] / len(tornillo_data)

        tuerca_mean[0] = sum_tuerca[0] / len(tuerca_data)
        tuerca_mean[1] = sum_tuerca[1] / len(tuerca_data)
        tuerca_mean[2] = sum_tuerca[2] / len(tuerca_data)

        arandela_mean[0] = sum_arandela[0] / len(arandela_data)
        arandela_mean[1] = sum_arandela[1] / len(arandela_data)
        arandela_mean[2] = sum_arandela[1] / len(arandela_data)

        clavo_mean[0] = sum_clavo[0] / len(clavo_data)
        clavo_mean[1] = sum_clavo[1] / len(clavo_data)
        clavo_mean[2] = sum_clavo[1] / len(clavo_data)

        # print("Tornillo  Tuerca  Arandela  Clavo")
        # print(len(tornillo_data), len(tuerca_data), len(arandela_data), len(clavo_data))

        # CONVERGENCIA Y CONDICION DE SALIDA
        if not tornillo_mean == tornillo_len:
            tornillo_len = tornillo_mean

        if not tuerca_mean == tuerca_len:
            tuerca_len = tuerca_mean

        if not arandela_mean == arandela_len:
            arandela_len = arandela_mean

        if not clavo_mean == clavo_len:
            clavo_len = clavo_mean

        iter += 1

    # Mean mas cercano
    sum_tornillo = 0
    sum_tuerca = 0
    sum_arandela = 0
    sum_clavo = 0

    for i in range(0, len(test.caracteristica) - 1):
        sum_tornillo += np.power(np.abs(test.caracteristica[i] - tornillo_mean[i]), 2)
        sum_tuerca += np.power(np.abs(test.caracteristica[i] - tuerca_mean[i]), 2)
        sum_arandela += np.power(np.abs(test.caracteristica[i] - arandela_mean[i]), 2)
        sum_clavo += np.power(np.abs(test.caracteristica[i] - clavo_mean[i]), 2)

    dist_tornillo = np.sqrt(sum_tornillo)
    dist_tuerca = np.sqrt(sum_tuerca)
    dist_arandela = np.sqrt(sum_arandela)
    dist_clavo = np.sqrt(sum_clavo)

    #print("\nMean mas cercano")
    #print("Tornillo  Tuerca  Arandela  Clavo")
    #print(dist_tornillo, dist_tuerca, dist_arandela, dist_clavo)

    aux = dist_tornillo
    if dist_tuerca < aux:
        aux = dist_tuerca
    if dist_arandela < aux:
        aux = dist_arandela
    if dist_clavo < aux:
        aux = dist_clavo

    if aux == dist_tornillo:
        test.pieza = 'Tornillo'
    elif aux == dist_tuerca:
        test.pieza = 'Tuerca'
    elif aux == dist_arandela:
        test.pieza = 'Arandela'
    elif aux == dist_clavo:
        test.pieza = 'Clavo'

    #print("\nPrediccion para KMeans: ", test.pieza)
    KMEANS = test.pieza

    return KNN, KMEANS


def main():
    cont_KNN = 0
    cont_KMEANS = 0
    cont_piezas = 0
    estado_KNN = ""
    estado_KMEANS = ""
    piezas = ["Arandela","Clavo", "Tornillo", "Tuerca"]
    carpetas = ["Arandelas", "Clavos", "Tornillos", "Tuercas"]
    
    # Clasificacion
    test = generar_base_datos()
    for j in range(len(carpetas)):
        carpeta = carpetas[j]
        input_path = "./dataset/original/test/" + carpeta +"/"
        dirs_input = os.listdir(input_path)

        for i in range(len(dirs_input)):
            nombre = input_path + dirs_input[i]
            image = io.imread(nombre)
            cont_piezas +=1
            KNN, KMEANS = clasifica(image, test)

            KNN = KNN + 's'
            KMEANS = KMEANS + 's'
            if(carpeta == KNN):
                cont_KNN +=1
                estado_KNN = "Acerto KNN"
            else:
                estado_KNN = "NO acerto KNN"
            
            if(carpeta == KMEANS):
                cont_KMEANS +=1
                estado_KMEANS = "Acerto KMEANS"
            else:
                estado_KMEANS = "NO acerto KMEANS"

            #print(KNN, KMEANS)
            resultado = carpeta +"/"+dirs_input [i] + " :" + estado_KNN + " y " + estado_KMEANS 
            print(resultado)
    print("--------------------------------------------------------------------\n")
    print("\nResultados:")
    print("\tSe analizaron ", cont_piezas, " piezas")
    print("\tSe acertaron: ", cont_KNN," piezas con KNN")
    print("\tSe acertaron: ", cont_KMEANS, " piezas con KMEANS")

    print("\nPorcentajes:")
    print("\tPorcentaje de certeza KNN: ", cont_KNN/cont_piezas*100, "%")
    print("\tPorcentaje de certeza KMEANS: ", cont_KMEANS/cont_piezas*100, "%")



if __name__ == '__main__':  # Para que se pueda usar sin interfaz
    main()