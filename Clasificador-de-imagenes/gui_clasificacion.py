"""
GUI: Graphical User Interface
Hacemos uso de Gradio: pip3 install gradio
"""

import gradio as gr
from p7_clasificacion import main

cant_cajas = 4

# Indicaciones del Orden de Apilamiento
def InstruccionesApilamiento():
    InstruccionesApilamiento_text = ""
    for i in range(cant_cajas - 1):
        InstruccionesApilamiento_text += "Sobre(Caja " + str(cant_cajas - i) + ",Caja " + str(cant_cajas - 1 - i) + "), "
    InstruccionesApilamiento_text += "Sobre(Caja 1, Mesa)"
    return "**Orden de apilamiento:** " + InstruccionesApilamiento_text

# Descripción del Header
title = "Clasificación 🔍🚀"
description = '**Input:** Pieza representativa de cada una de las cajas, según el orden en que estan apiladas. <br>'
description += '**Output:** Identificación del contenido de cada una de las cajas y orden de apilamiento ascendente. <br>' 
description += InstruccionesApilamiento()

# Descripción del Footer
article = '**Desafío:** Mediante visión artificial identidficar el contenido de cuatro cajas que se encuentran apiladas. Una caja contiene tornillos, una segunda caja contiene tuercas, una tercera caja contiene clavos y la cuarta caja contiene arandelas; las cuales se encuentran apiladas en un orden aleatorio.<br> '
article += '**Mario Bustillo 2023 🚀** | [Github](https://github.com/mabustillo14) | [Linkedin](https://www.linkedin.com/in/mario-bustillo/) 🤗 '
enable_queue=False

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

# Ejemplos
examples = [["./dataset/evaluacion/photo2.jpg", "./dataset/evaluacion/photo6.jpg", "./dataset/evaluacion/photo12.jpg", "./dataset/evaluacion/photo18.jpg"]]

# Armar la GUI
demo = gr.Interface(
    fn=main, 
    inputs=[image4, image3, image2, image1], 
    outputs=[text4, text3, text2, text1, text5],
    title=title, 
    description=description, 
    article=article,
    examples = examples
    )

demo.launch(enable_queue=enable_queue, debug=True)
