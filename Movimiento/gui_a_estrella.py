"""
GUI: Graphical User Interface
Hacemos uso de Gradio: pip3 install gradio
"""

import gradio as gr
from A_estrella import main

# Gradio Format
title = "Resolución de Laberinto 🚀"
description = 'Input: Definir coordenadas. <br> Output: Path , Mapa'
article="**Mario Bustillo 2022** | [Github](https://github.com/mabustillo14) | [Linkedin](https://www.linkedin.com/in/mario-bustillo/) 🤗"
enable_queue=False

demo = gr.Interface(fn=main, inputs=["text", "text", "text", "text"], outputs=["text","image"],title=title,description=description,article=article)

demo.launch(enable_queue=enable_queue,debug=True)
