"""
GUI: Graphical User Interface
Hacemos uso de Gradio: pip3 install gradio
"""

import gradio as gr
from A_estrella import solucion
import Laberinto as Lab

maze = Lab.Mapa()
val_y=len(maze) -1      # Alto de laberinto
val_x=len(maze[0]) -1   # Ancho del laberinto

# Gradio Format
title = "Resolución de Laberinto 🚀"
description = 'Input: Definir coordenadas. <br> Output: Path , Mapa <br><br> El Laberinto tiene dimensiones: ' + str(val_x)+ 'x' + str(val_y)+ ', siendo la esquina superior izquierda la coordenada (0,0)'
article="**Mario Bustillo 2022** | [Github](https://github.com/mabustillo14) | [Linkedin](https://www.linkedin.com/in/mario-bustillo/) 🤗"
enable_queue=False

#Entrada de datos
text1 = gr.Textbox(label="Coordena X - Punto Inicio")
text2 = gr.Textbox(label="Coordena Y - Punto Inicio")
text3 = gr.Textbox(label="Coordena X - Punto Final")
text4 = gr.Textbox(label="Coordena Y - Punto Final")


#Salida de datos
text5 = gr.Textbox(label="Secuencia Solución")
image1 = gr.Image(shape=(224, 224), label="Mapa Solución")

demo = gr.Interface(fn=solucion, inputs=[text1, text2, text3, text4], outputs=[text5,image1],title=title,description=description,article=article, css="body {background-image: url('file=mapa.png')}")




demo.launch(enable_queue=enable_queue,debug=True)

