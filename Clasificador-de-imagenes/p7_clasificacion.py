from matplotlib import pyplot as plt
import matplotlib.patches as mpatches

plt.rcParams['image.cmap'] = 'gray'

from skimage import io, filters
import numpy as np
import cv2
import os
from datetime import datetime
import random

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

    """
    REDIMENSIONAMIENTO DE LA IMAGEN
    Convertir la imagen de 1220x1080 a 500x400
    """
    resized_image = cv2.resize(image_sin_fondo, (500, 400))

    return resized_image


def extraccion(image, hacer_transformacion=False):
    """
    TRANSFORMACION
    """
    if hacer_transformacion:
        image = transformacion(image)

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
    Solo funciona para imagenes cortadas -> porque sino el fondo afecta mucho al objeto dentro de la imagen
    """
    # ret, th = cv2.threshold(aux, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    # aux= th

    """
    EXTRACCION DE RASGOS
    Para momentos de Hu
    """
    hu = cv2.HuMoments(cv2.moments(aux)).flatten()

    return aux, [hu[0], hu[1], hu[3]]


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

    ax.grid(True)
    ax.set_title("Analisis completo de carpeta Train")

    yellow_patch = mpatches.Patch(color='yellow', label='Tornillo')
    red_patch = mpatches.Patch(color='red', label='Tuerca')
    blue_patch = mpatches.Patch(color='blue', label='Arandela')
    green_patch = mpatches.Patch(color='green', label='Clavo')
    plt.legend(handles=[yellow_patch, red_patch, blue_patch, green_patch])

    ax.set_xlabel('componente 1')
    ax.set_ylabel('componente 2')
    ax.set_zlabel('componente 4')

    plt.savefig("pruebas/7_clasificacion/grafico_base_de_datos.jpg")
    # plt.show()

    print("Analisis completo de la base de datos de Train")
    print("Cantidad de imagenes analizadas: ", len(datos))

    # Elemento a evaluar
    test = Elemento()

    print("--------------------------------------------------------------------\n")
    return test


def clasifica(image, test, numero_caja):
    print("\n--------------------------------------------------------------------")
    print("Comienza Análisis de la Caja #", numero_caja)
    print("--------------------------------------------------------------------\n")

    respuesta = []
    global fig
    global ax
    global datos
    global contador_cajas

    test.image, test.caracteristica = extraccion(image, hacer_transformacion=True)
    test.pieza = 'Arandela'  # label inicial

    ax.scatter(test.caracteristica[0], test.caracteristica[1], test.caracteristica[2], c='k', marker='o')
    fig

    """
    KNN: K Nearest Neighbors
    """
    print("\nInicializacion KNN")
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

    print("Prediccion para KNN con K=1: ", test.pieza)
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
    print("\nPredicciones para KNN con K=9: ")
    k = 9
    for i in range(k):
        print(datos[i].pieza)

    """
    K MEANS
    """
    print("\nInicializacion KMeans")

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

    fig_means = plt.figure()
    ax = fig_means.add_subplot(111, projection='3d')

    # fig_means, ax = plt.subplots()
    ax.scatter(tornillo_mean[0], tornillo_mean[1], tornillo_mean[2], c='y', marker='o')
    ax.scatter(tuerca_mean[0], tuerca_mean[1], tuerca_mean[2], c='r', marker='o')
    ax.scatter(arandela_mean[0], arandela_mean[1], arandela_mean[2], c='b', marker='o')
    ax.scatter(clavo_mean[0], clavo_mean[1], clavo_mean[2], c='g', marker='o')

    ax.grid(True)
    ax.set_title("Means")

    yellow_patch = mpatches.Patch(color='yellow', label='Tornillo')
    red_patch = mpatches.Patch(color='red', label='Tuerca')
    blue_patch = mpatches.Patch(color='blue', label='Arandela')
    green_patch = mpatches.Patch(color='green', label='Clavo')
    plt.legend(handles=[yellow_patch, red_patch, blue_patch, green_patch])

    ax.set_xlabel('componente 1')
    ax.set_ylabel('componente 2')
    ax.set_zlabel('componente 4')

    plt.savefig("pruebas/7_clasificacion/means_de_caja_" + str(numero_caja) + ".jpg")

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

    # Ubicacion de los means finales
    ax.scatter(tornillo_mean[0], tornillo_mean[1], tornillo_mean[2], c='k', marker='o')
    ax.scatter(tuerca_mean[0], tuerca_mean[1], tuerca_mean[2], c='k', marker='o')
    ax.scatter(arandela_mean[0], arandela_mean[1], arandela_mean[2], c='k', marker='o')
    ax.scatter(clavo_mean[0], clavo_mean[1], clavo_mean[2], c='k', marker='o')

    print("Ubicacion de los means finales")
    print("Tornillo  Tuerca  Arandela  Clavo")
    print(len(tornillo_data), len(tuerca_data), len(arandela_data), len(clavo_data))
    fig_means

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

    print("\nMean mas cercano")
    print("Tornillo  Tuerca  Arandela  Clavo")
    print(dist_tornillo, dist_tuerca, dist_arandela, dist_clavo)

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

    print("\nPrediccion para KMeans: ", test.pieza)
    KMEANS = test.pieza

    # confidendes = {"KNN": KNN, "KMEANS": KMEANS}
    respuesta.append("KNN: " + KNN)
    respuesta.append("KMEANS: " + KMEANS)
    return respuesta


def generar_archivo(orden):
    # Generar un txt con el orden de apilamiento
    file = open("../Apilamiento/datos.txt", "w")
    ahora = datetime.now()
    fecha = ahora.strftime("%Y-%m-%d %H:%M:%S")
    file.write("Fecha y Hora de determinación de secuencia de Apilamiento: " + fecha)
    file.write("\n")
    for i in range(len(orden)):
        file.write(orden[i])
        file.write(",")
    file.close()


def mostrar_apilado(orden_apilado):
    print("\n\nRepresentación Simbolica del Resultado de la secuencia:")
    for i in range(len(orden_apilado)):
        print("\t-------------------------")
        print("\t|\t", orden_apilado[len(orden_apilado) - 1 - i], " \t|")
    print("\t=========================\n")


def main(foto4, foto3, foto2, foto1):
    orden = []

    test = generar_base_datos()
    resultado1 = clasifica(foto1, test, 1)
    resultado2 = clasifica(foto2, test, 2)
    resultado3 = clasifica(foto3, test, 3)
    resultado4 = clasifica(foto4, test, 4)

    """
    Devolver orden de Apilamiento
    La prioridad es el metodo KNN por todas las pruebas hechas en eficiencia
    """
    aux = resultado1[0].split(":")  # Le quitamos el "KNN:", para ello lo separamos por :
    orden.append(aux[1])  # Tomamos el segundo termino de la separacion
    aux = resultado2[0].split(":")
    orden.append(aux[1])
    aux = resultado3[0].split(":")
    orden.append(aux[1])
    aux = resultado4[0].split(":")
    orden.append(aux[1])

    # Archivo con el orden de apilamiento
    generar_archivo(orden)

    print("\n--------------------------------------------------------------------")
    print("Conclusiones")
    print("--------------------------------------------------------------------\n")
    print("Resultados:")
    print("Caja 4:", resultado4)
    print("Caja 3:", resultado3)
    print("Caja 2:", resultado2)
    print("Caja 1:", resultado1)

    print("\nLa secuencia de apilamiento ascendente es:", orden)

    mostrar_apilado(orden)

    return resultado4, resultado3, resultado2, resultado1, orden


if __name__ == '__main__':  # Para que se pueda usar sin interfaz
    orden = []
    flag = True
    cant_cajas = 4
    fotos_cajas = []    # lista con los valores de las fotos a evaluar
    inicio = ""
    print("\n--------------------------------------------------------------------")
    print("Clasificación de Objetos")
    print("--------------------------------------------------------------------\n")

    for i in range(cant_cajas - 1):
        # Anadir Condiciones Iniciales
        inicio += "Sobre(Caja " + str(cant_cajas - i) + ",Caja " + str(cant_cajas - 1 - i) + "), "
    inicio += "Sobre(Caja 1, Mesa)"
    print("Orden de apilamiento:", inicio, "\n")

    # Pedir todos los numeros de las fotos a evaluar
    for i in range(cant_cajas):
        text = "Introduce numero de la foto de la Caja #" + str(cant_cajas - i) + ": "
        numero = input(text)
        fotos_cajas.append(numero)

    test = generar_base_datos()
    resultado = []
    for i in range(cant_cajas):
        nombre = './dataset/evaluacion/photo' + str(fotos_cajas[cant_cajas - i - 1]) + '.jpg'
        image = io.imread(nombre)
        resultado.append(clasifica(image, test, i + 1))

    print("\n--------------------------------------------------------------------")
    print("Conclusiones")
    print("--------------------------------------------------------------------\n")
    print("Resultados:")
    for i in range(cant_cajas):
        print("Caja ", cant_cajas - i, ":", resultado[cant_cajas - i - 1])

    # Devolver orden de Apilamiento
    # La prioridad es el metodo KNN por todas las pruebas hechas en eficiencia
    aux = resultado[0][0].split(":")    # Le quitamos el "KNN:", para ello lo separamos por :
    orden.append(aux[1])                # Tomamos el segundo termino de la separacion
    aux = resultado[1][0].split(":")
    orden.append(aux[1])
    aux = resultado[2][0].split(":")
    orden.append(aux[1])
    aux = resultado[3][0].split(":")
    orden.append(aux[1])

    generar_archivo(orden)

    print("\nLa secuencia de apilamiento ascendente es:", orden)

    mostrar_apilado(orden)
    print("\nFin de la Ejecución")
