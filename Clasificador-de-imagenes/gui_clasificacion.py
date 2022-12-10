"""
GUI: Graphical User Interface
Hacemos uso de Gradio: pip3 install gradio
"""

import gradio as gr
from p7_clasificacion import main

# Gradio Format
title = "Clasificación 🚀"
description = 'Input: Fotos de las piezas según como estan apiladas. <br> Output: Orden de Apilamiento'
article = "**Mario Bustillo 2022** | [Github](https://github.com/mabustillo14) | [Linkedin](https://www.linkedin.com/in/mario-bustillo/) 🤗"
enable_queue = False

# Entrada de datos
image1 = gr.Image(label="Foto - Caja 1")
image2 = gr.Image(label="Foto - Caja 2")
image3 = gr.Image(label="Foto - Caja 3")
image4 = gr.Image(label="Foto - Caja 4")

# Salida de datos
text1 = gr.Textbox(label="Resultado del Análisis - Caja 1")
text2 = gr.Textbox(label="Resultado del Análisis - Caja 2")
text3 = gr.Textbox(label="Resultado del Análisis - Caja 3")
text4 = gr.Textbox(label="Resultado del Análisis - Caja 4")
text5 = gr.Textbox(label="Orden ascendente de Apilamiento")

# Armar la GUI
demo = gr.Interface(fn=main, inputs=[image4, image3, image2, image1], outputs=[text4, text3, text2, text1, text5],
                    title=title, description=description, article=article)

demo.launch(enable_queue=enable_queue, debug=True)
