import cv2

################################################
## Algoritmo de Canny para detectar contornos ##
################################################
# NOTA: Consideramos que cada contorno encontrado, equivale a un objeto dentro de la imagen.

# Cargar imagen
imagen = cv2.imread('ejemplos/arandela_internet.jpg')
grises = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

"""
Los umbrales 10 y 140 se determinaron arbitrariamente para esta imagen.
Si cambiamos el tipo de imagen deberíamos ajustarlos nuevamente
"""
bordes = cv2.Canny(grises, 10, 140)

# Detectar bordes
ctns, _ = cv2.findContours(bordes, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
print('Número de contornos encontrados: ', len(ctns))

# Dibujar y escribir en la imagen de input, los contornos detectados
cv2.drawContours(imagen, ctns, -1, (0, 0, 255), 2)
texto = 'Contornos encontrados: ' + str(len(ctns))
cv2.putText(imagen, texto, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
            (255, 0, 0), 1)

# Guardar resultados
path = "./Figuras_test/"
fileb = "Figura_adaptacion_0.png"
cv2.imwrite(path + fileb, imagen)

#################################################
## Uso de Thresholding para detectar contornos ##
#################################################
# NOTA: A veces funciona mejor el algoritmo Canny en vez de Thresholding -> depende mucho de las características de la imagen de entrada

# Cargar imagen
imagen = cv2.imread('ejemplos/arandela_internet.jpg')

"""
Los umbrales 190 y 255 se determinaron arbitrariamente para esta imagen.
Si cambiamos el tipo de imagen deberíamos ajustarlos nuevamente
"""
grises = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
_, th = cv2.threshold(grises, 190, 255, cv2.THRESH_BINARY_INV)

# Detectar bordes
cnts, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
print('Número de contornos encontrados: ', len(ctns))

# Dibujar y escribir en la imagen de input, los contornos detectados
cv2.drawContours(imagen, cnts, -1, (255, 0, 0), 2)

font = cv2.FONT_HERSHEY_SIMPLEX
i = 0
for c in cnts:
    # Determinar los momentos
    M = cv2.moments(c)
    if M["m00"] == 0:
        M["m00"] = 1

    x = int(M["m10"] / M["m00"])
    y = int(M['m01'] / M['m00'])

    mensaje = 'Num :' + str(i + 1)
    cv2.putText(imagen, mensaje, (x - 40, y), font, 0.75,
                (255, 0, 0), 2, cv2.LINE_AA)
    cv2.drawContours(imagen, [c], 0, (255, 0, 0), 2)
    i = i + 1

# Guardar resultados
path = "./Figuras_test/"
fileb = "Figura_adaptacion_1.png"
cv2.imwrite(path + fileb, imagen)

####################################################
## Recortar imagen a partir de Algoritmo de Canny ##
####################################################
# NOTA: Consideramos que este programa solo es capaz de analizar un objeto dentro de la imagen

# Cargar imagen
imagen = cv2.imread('ejemplos/arandela_internet.jpg')
grises = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

"""
Los umbrales 100 y 200 se determinaron arbitrariamente para esta imagen.
Si cambiamos el tipo de imagen deberíamos ajustarlos nuevamente
"""
bordes = cv2.Canny(grises, 100, 200)

# Detectar bordes
ctns, _ = cv2.findContours(bordes, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
print('Número de contornos encontrados: ', len(ctns))

# Determinar coordenadas del rectángulo que encierra al objeto
x, y, w, h = cv2.boundingRect(ctns[0])  # x,y: coordenada de la parte izquierda de arriba. w: ancho y h:alto
crop_img = imagen[y:y + h, x:x + w]

path = "./Figuras_test/"
fileb = "Figura_adaptacion_2.png"
cv2.imwrite(path + fileb, crop_img)
