"""
GUI: Graphical User Interface
Hacemos uso de Gradio: pip3 install gradio
"""

import gradio as gr
from Apilamiento import Solucion

def main(Caja_1, Caja_2, Caja_3, Caja_4):
    return Solucion(Posicion_Inicial,Caja_1, Caja_2, Caja_3, Caja_4)

# Gradio Format
title = "Apilamiento 🚀"
description = 'Input: Orden de Apilamiento Objetivo. <br> Output: Propiedades del Problema, Secuencia en Lenguaje STRIPS , Cantidad de Movimientos'
article="**Mario Bustillo 2022** | [Github](https://github.com/mabustillo14) | [Linkedin](https://www.linkedin.com/in/mario-bustillo/) 🤗"
enable_queue=False

#Salida de datos
text1 = gr.Textbox(label="Objetos")
text2 = gr.Textbox(label="Estado Inicial")
text3 = gr.Textbox(label="Estado Objetivo")
text4 = gr.Textbox(label="Secuencia Solución")
text5 = gr.Textbox(label="Costo total del camino")

#Extraer los objetos 
with open("datos.txt") as archivo:
        for linea in archivo:
            Posicion_Inicial = linea.split(",")
            Posicion_Inicial.pop()
        print("\nApilamiento ascendente Inicial: ", Posicion_Inicial)

inputs =  []
for i in range(4):
    titulo = "Caja " +  str(4-i)
    inputs.append(gr.Radio(Posicion_Inicial, label=titulo))

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
