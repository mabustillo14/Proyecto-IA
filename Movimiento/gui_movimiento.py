"""
GUI: Graphical User Interface
Hacemos uso de Gradio: pip3 install gradio
"""

import gradio as gr
from A_estrella import solucion, MostrarMapa
import Laberinto as Lab

# Obtener caracteristicas del Laberinto
maze = Lab.Mapa()
val_y=len(maze) -1      # Alto de laberinto
val_x=len(maze[0]) -1   # Ancho del laberinto

# Mostar el Mapa por pantalla
MostrarMapa('mapa.png','Mapa', maze)

# Descripción del Header
title = "Resolución de Laberinto 🗺️"
description = '**Input:** Ingresar coordenadas de Inicio y Fin.<br>' 
description += '**Output:** Path , Mapa con la solución <br>'
description += '**Características:** El Laberinto tiene dimensiones: ' + str(val_x)+ 'x' + str(val_y)+ ', siendo la esquina superior izquierda la coordenada (0,0)'

# Descripción del Footer
article = '**Desafío:** Una vez apiladas las cajas en la nueva configuración, el robot deberá transportarlas desde un punto A a un punto B a través de un laberinto predefinido, utilizando el algoritmo A* para encontrar el camino más corto con Heurística de distancia de Manhattan.<br> '
article += '**Mario Bustillo 2023 🚀** | [Github](https://github.com/mabustillo14) | [Linkedin](https://www.linkedin.com/in/mario-bustillo/) 🤗 '
enable_queue=False

# Entrada de datos
text1 = gr.Textbox(label="Coordena X - Punto Inicio") #Ax
text2 = gr.Textbox(label="Coordena Y - Punto Inicio") #Ay
text3 = gr.Textbox(label="Coordena X - Punto Final") #Bx
text4 = gr.Textbox(label="Coordena Y - Punto Final") #By

# Salida de datos
text5 = gr.Textbox(label="Secuencia Solución")
image1 = gr.Image(shape=(224, 224), label="Mapa Solución")

# Ejemplos
examples = [[2,2,9,9]]

# Planteamiento de la Interfaz
demo = gr.Interface(
    fn=solucion, 
    inputs=[text1, text2, text3, text4], 
    outputs=[text5,image1],
    title=title,
    description=description,
    article=article, 
    examples = examples
    )
demo.launch(enable_queue=enable_queue,debug=True)

