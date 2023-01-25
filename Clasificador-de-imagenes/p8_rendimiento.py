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


# Llamar las funciones de clasificacion de imagenes desde p7_clasificacion.py
import p7_clasificacion as clasificacion

"""
VARIABLES GLOBALES
Para almacenar los datos y graficar
"""
global datos, fig, ax
datos = []
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


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
        datos[i].image, datos[i].caracteristica = clasificacion.extraccion(objeto)
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
        datos[i].image, datos[i].caracteristica = clasificacion.extraccion(objeto)
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
        datos[i].image, datos[i].caracteristica = clasificacion.extraccion(objeto)
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
        datos[i].image, datos[i].caracteristica = clasificacion.extraccion(objeto)
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


def clasifica(image, test, K):
    
    respuesta = []
    global fig
    global ax
    global datos
    global contador_cajas

    test.image, test.caracteristica =  clasificacion.extraccion(image, hacer_transformacion=True)
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
    KNN para un valor K dado
    """
    vect_contador = [] # Cantidad de veces que se repite una categoria

    # Comienza el analisis para distintos valores de K    
    for i in range(K):
        vect_contador.append(0)   

        for j in range(K):
            if(datos[i].pieza == datos[j].pieza):
                vect_contador[i] +=1

    maxContador = max(vect_contador)
    indice_maxContador = vect_contador.index(maxContador)
    KNN_Multiple = datos[indice_maxContador].pieza

    #print("KNN Multiple (K=9): ", caracteristica)

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

    return KNN, KNN_Multiple, KMEANS

def MostrarResultados(cont_piezas, vect_KNN, cont_KMEANS):
    print("--------------------------------------------------------------------\n")
    print("\nResultados:")
    print("\tSe analizaron " + str(cont_piezas) + " piezas")
    for i in range(len(vect_KNN)-1):
        print("\tSe acertaron: " + str(vect_KNN[i]) + " piezas con KNN con K=" + str(i+1))
    print("\tSe acertaron: " + str(cont_KMEANS) + " piezas con KMEANS")

    print("\nPorcentajes:")

    for i in range(len(vect_KNN)-1):
        print("\tPorcentaje de certeza KNN con K=" + str(i+1) + ": " + str(vect_KNN[i]/cont_piezas*100) + "%")

    print("\tPorcentaje de certeza KMEANS: " + str(cont_KMEANS/cont_piezas*100) + "%")

"""
Calculo de Rendimiento
"""
def rendimiento(val_K):
    K = val_K # Establecer rango de busqueda de O - K
   
    # Nombre de las piezas y carpetas
    piezas = ["Arandela","Clavo", "Tornillo", "Tuerca"]
    carpetas = ["Arandelas", "Clavos", "Tornillos", "Tuercas"]
    
    # Clasificacion
    test = generar_base_datos()

    # Generar el vector contador, vector K
    vect_it=[]

    vect_aciertos_KNN = []
    vect_val_K = []
    vect_eficiencia_KNN = []

    cont_KMEANS = 0
    vect_eficiencia_KMEANS = []
    
    
    for i in range(K): #Consideramos el KNN y KNN Multiple
        vect_aciertos_KNN.append(0) # Lo rellenamos de cero cada componente
        vect_val_K.append(i+1)
    
    cont_piezas = 0

    for j in range(len(carpetas)):
        carpeta = carpetas[j]
        input_path = "./dataset/original/test/" + carpeta +"/"
        dirs_input = os.listdir(input_path)

        for i in range(len(dirs_input)):
            nombre = input_path + dirs_input[i]
            image = io.imread(nombre)
            cont_piezas +=1

            print("Análisis de: ", carpeta +"/"+dirs_input [i])

            # A partir de aca comienza el analisis con distintos valores de K
            for  i in range(K-1): # Para una misma imagen la evaluamos con distintos valores de 
                # Ejecutar clasificacion para un valor de K
                KNN, KNN_Multiple, KMEANS = clasifica(image, test, K)
                
                # Categoria devuelta para un valor de K dado
                KNN_Multiple = KNN_Multiple + 's'
                
                if(carpeta == KNN_Multiple):
                    vect_aciertos_KNN[i+1] +=1
            
            # KNN con K=1
            KNN = KNN + 's'
            if(carpeta == KNN):
                    vect_aciertos_KNN[0] +=1

            # KMEANS
            KMEANS = KMEANS + 's'
            if(carpeta == KMEANS):
                    cont_KMEANS +=1


            vect_it.append(cont_piezas)
            vect_eficiencia_KMEANS.append(cont_KMEANS/cont_piezas*100)

    # Rellenar vector de eficiencia
    for i in range(K):
        vect_eficiencia_KNN.append(vect_aciertos_KNN[i]*100/cont_piezas)

    # Grafico de Aciertos -KNN
    grafico_aciertos_KNN, ax = plt.subplots()
    ax.plot(vect_val_K, vect_aciertos_KNN)
    ax.grid(True)
    ax.set_title("Rendimiento de KNN para distintos K")
    ax.set_xlabel('K Nearest Neighbors')
    ax.set_ylabel('Cantidad de Predicciones Correctas')
    plt.savefig("pruebas/8_rendimiento/rendimiento_valores_K_aciertos" + ".jpg")

    # Grafico de Eficiencia - KNN
    grafico_eficiencia_KNN, ax = plt.subplots()
    ax.plot(vect_val_K, vect_eficiencia_KNN)
    ax.grid(True)
    ax.set_title("Rendimiento de KNN")
    ax.set_xlabel('K Nearest Neighbors')
    ax.set_ylabel('Predicciones Correctas (%)')
    plt.savefig("pruebas/8_rendimiento/rendimiento_valores_K_eficiencia" + ".jpg")

    # Grafico de Eficiencia - KMEANS
    grafico_eficiencia_KNN, ax = plt.subplots()
    ax.plot(vect_it, vect_eficiencia_KMEANS)
    ax.grid(True)
    ax.set_title("Rendimiento de KMeans")
    ax.set_xlabel('Número de Ejecución')
    ax.set_ylabel('Predicciones Correctas (%)')
    plt.savefig("pruebas/8_rendimiento/rendimiento_KMeans_eficiencia" + ".jpg")

    MostrarResultados(cont_piezas, vect_aciertos_KNN, cont_KMEANS)

    

if __name__ == '__main__':  # Para que se pueda usar sin interfaz
    print("--------------------------------------------------------------------")
    print("Rendimiento del Algoritmo de Clasificación de Imágenes")
    print("--------------------------------------------------------------------\n")
    print("Ingrese el valor de K hasta el que desea evaluar el algoritmo de KNN")
    val_K = int(input("Valor de K = "))
    rendimiento(val_K)