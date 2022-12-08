from matplotlib import pyplot as plt
plt.rcParams['image.cmap'] = 'gray'

from skimage import color, filters
import cv2
from skimage.filters import try_all_threshold

# Imagen a analizar
prueba = './ejemplos/tornillo_prueba.jpg'

##############################
## Thresholding supervisado ##
##############################

# Cargar imagen
imagen = cv2.imread(prueba)
imagen = color.rgb2gray(imagen)
imagen = cv2.resize(imagen, (500,400))

# Aplicar filtros
gaussiano = filters.gaussian(imagen, sigma=1)
sobel = filters.sobel(imagen)

fig, (ax0, ax1, ax2 , ax3, ax4) = plt.subplots(1, 5, figsize=(16, 15))
ax0.imshow(sobel < 0.01)
ax0.set_title('th=0.01')

ax1.imshow(sobel < 0.02)
ax1.set_title('th=0.02')

ax2.imshow(sobel < 0.05)
ax2.set_title('th=0.05')

ax3.imshow(sobel < 0.07)
ax3.set_title('th=0.07')

ax4.imshow(sobel < 0.1)
ax4.set_title('th=0.1')

# Guardar resultados
plt.savefig("./pruebas/3_segmentacion/threshold_supervisado.jpg")

#################################
## Thresholding NO supervisado ##
#################################
# https://scikit-image.org/docs/dev/api/skimage.filters.html#skimage.filters.sobel_v

fig, ax = try_all_threshold(sobel, figsize=(10, 10), verbose=False)

# Guardar resultados
plt.savefig("./pruebas/3_segmentacion/threshold_no_supervisado.jpg")
