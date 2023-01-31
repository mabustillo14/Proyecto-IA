"""
GUI: Graphical User Interface
Hacemos uso de Gradio: pip3 install gradio
"""

import gradio as gr
from Apilamiento import Solucion

cant_cajas = 4

# Función del Gradio
def main(Caja_1, Caja_2, Caja_3, Caja_4):
    return Solucion(Posicion_Inicial,Caja_1, Caja_2, Caja_3, Caja_4)

# Indicaciones del Orden de Apilamiento
def InstruccionesApilamiento():
    InstruccionesApilamiento_text = ""
    for i in range(cant_cajas - 1):
        InstruccionesApilamiento_text += "Sobre(Caja " + str(cant_cajas - i) + ",Caja " + str(cant_cajas - 1 - i) + "), "
    InstruccionesApilamiento_text += "Sobre(Caja 1, Mesa)"
    return "**Orden de apilamiento:** " + InstruccionesApilamiento_text # Orden descendente

# Extraer los objetos del txt
with open("datos.txt") as archivo:
        for linea in archivo:
            Posicion_Inicial = linea.split(",")
            Posicion_Inicial.pop()
        print("\nApilamiento ascendente Inicial: ", Posicion_Inicial)

# Determinar si hay piezas repetidas - Para las situaciones donde hay elementos repetidos
repetidos = []
for i in range(len(Posicion_Inicial)):
    repetidos.append(0)
    for j in range(len(Posicion_Inicial)):
        if(Posicion_Inicial[i]==Posicion_Inicial[j]):
            repetidos[i] += 1
it = 0
for i in range(len(repetidos)):
    if(repetidos[i]>1):
        it +=1
        Posicion_Inicial[i] += " "+ str(it)

# Generar las opciones para los inputs
inputs =  []
for i in range(cant_cajas):
    titulo = "Caja " +  str(cant_cajas-i)
    inputs.append(gr.Radio(Posicion_Inicial, label=titulo))  

# Obtener el orden de apilamiento inicial - Orden ascendente
ApiladoInicial = "Sobre(" +Posicion_Inicial[0] + ",mesa A), "
for i  in range(cant_cajas-1):
    #Anadir Condiciones Iniciales
    ApiladoInicial += "Sobre(" + Posicion_Inicial[i+1] + "," + Posicion_Inicial[i] + "), "

# Descripción del Header
title = "Apilamiento 📦"
description = '**Input:** Orden de Apilamiento Objetivo. <br>'
description += '**Output:** Propiedades del Problema, Secuencia en Lenguaje STRIPS , Cantidad de Movimientos <br>' 
description += InstruccionesApilamiento()

# Descripción del Footer
article = '**Desafío:** Al reconocer el orden de apilamiento de las cajas, mediante lenguaje STRIPS se debe encontrar los pasos que debe realizar el brazo robótico para alcanzar un nuevo orden de apilado de cajas.<br> '
article += '**Apilamiento Inicial:** ' + ApiladoInicial + '<br>'
article += ' **Mario Bustillo 2023 🚀** | [Github](https://github.com/mabustillo14) | [Linkedin](https://www.linkedin.com/in/mario-bustillo/) 🤗 '
enable_queue=False

# Salida de datos
text1 = gr.Textbox(label="Objetos")
text2 = gr.Textbox(label="Estado Inicial")
text3 = gr.Textbox(label="Estado Objetivo")
text4 = gr.Textbox(label="Secuencia Solución")
text5 = gr.Textbox(label="Costo total del camino")



# Planteamiento de la Interfaz
#demo = gr.Interface(fn=main, inputs=[text1, text2, text3, text4], outputs=[text5,image1],title=title,description=description,article=article, css="body {background-image: url('file=mapa.png')}")
demo = gr.Interface(
    main,
    inputs,
    outputs=[text1, text2, text3, text4, text5],
    title=title,
    description=description,
    article=article
)

demo.launch(enable_queue=enable_queue,debug=True)
