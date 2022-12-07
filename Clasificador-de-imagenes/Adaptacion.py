import cv2

#Imagen a analizar
#Las fotos de entrada estan en formato png o jpeg
prueba = './ejemplos/arandela_internet.jpg'

#####################################################################################################################################
##Algoritmo de Canny para detectar contornos
#####################################################################################################################################
#NOTA:Consideramos que cada contorno encontrado equivale a un objeto dentro de la imagen

#Aca cargamos la imagen
imagen = cv2.imread(prueba)
#imagen = cv2.imread('Data-Base/YTrain/ZArandelas/photo0.jpg')
#imagen = cv2.imread('ejemplos/arandela_internet.jpg')
#imagen = cv2.imread('ejemplos/arandelas2_internet.png')
#imagen = cv2.imread('ejemplos/tornillo_prueba.jpg')
#imagen = cv2.imread('ejemplos/cartas.png') #Por si quiere evaluar otra imagen
grises = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

#bordes = cv2.Canny(grises, 10, 140) #Para arandela_internet
#bordes = cv2.Canny(grises, 100, 200) #Para arandela_internet
#bordes = cv2.Canny(grises, 10, 800) #Para tornillo_prueba
bordes = cv2.Canny(grises, 10, 1300) #Para arandelas2_internet

#Para OpenCV4
ctns, _ = cv2.findContours(bordes, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

cv2.drawContours(imagen, ctns, -1, (0,0,255), 2)
#Muestra por consola
#print('Numero de contornos encontrados: ', len(ctns))
#Incorpora un texto en la parte superior izquierda a la propia imagen
texto = 'Contornos encontrados: '+ str(len(ctns))

cv2.putText(imagen, texto, (10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
	(255, 0, 0), 1)

path="./Figuras_test/"
fileb="Figura_adaptacion_0.png"
cv2.imwrite(path + fileb, imagen)

#####################################################################################################################################
##Uso de Thresholding para detectar contornos
#####################################################################################################################################
#NOTA: A veces funciona mejor el algoritmo Canny en vez de Thresholding -> depende mucho de las caracteristicas de la imagen de entrada 

#imagen = cv2.imread(prueba)
#imagen = cv2.imread('ejemplos/arandela_internet.jpg')
imagen = cv2.imread('ejemplos/arandelas2_internet.png')
#imagen = cv2.imread('ejemplos/monedas.jpg')
#imagen = cv2.imread('ejemplos/tornillo_prueba.jpg')

grises = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
_,th =  cv2.threshold(grises, 240, 255, cv2.THRESH_BINARY_INV)

#Para OpenCV 4
cnts,_ = cv2.findContours(th, cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)

cv2.drawContours(imagen, cnts, -1, (255,0,0),2)
#print('Contornos: ', len(cnts))

font = cv2.FONT_HERSHEY_SIMPLEX
i=0
for c in cnts:
	M=cv2.moments(c)
	if (M["m00"]==0): M["m00"]=1
	x=int(M["m10"]/M["m00"])
	y=int(M['m01']/M['m00'])

	mensaje = 'Num :' + str(i+1)
	cv2.putText(imagen,mensaje,(x-40,y),font,0.75,
		(255,0,0),2,cv2.LINE_AA)
	cv2.drawContours(imagen, [c], 0, (255,0,0),2)
	i = i+1

path="./Figuras_test/"
fileb="Figura_adaptacion_1.png"
cv2.imwrite(path + fileb, imagen)


#####################################################################################################################################
##Recortar imagen a partir de Algoritmo de Canny
#####################################################################################################################################
#NOTA: Consideramos que este programa solo es capaz de analizar un objeto dentro de la imagen

imagen = cv2.imread(prueba)
grises = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
bordes = cv2.Canny(grises, 100, 200)

#Para OpenCV4
ctns, _ = cv2.findContours(bordes, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

#Determinar coordenadas del rectangulo que encierra al objeto
x,y,w,h = cv2.boundingRect(ctns[0]) #x,y: coordenada de la parte izquierda de arriba. w: ancho y h:alto

crop_img = imagen[y:y+h, x:x+w]

path="./Figuras_test/"
fileb="Figura_adaptacion_2.png"
cv2.imwrite(path + fileb, crop_img)
