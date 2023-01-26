import matplotlib.pyplot as plt
import Laberinto as Lab
from PIL import Image

class nodoo(): #A cada punto del mapa le calcula los valores de g, h y f
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0 # G es la distancia entre el nodo actual y el nodo inicial
        self.h = 0 # H es la heurística: distancia estimada desde el nodo actual hasta el nodo final
        self.f = 0 # F es el costo total del nodo.
    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end):
    #Definimos los nodos inicial y final
    start_node = nodoo(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = nodoo(None, end)
    end_node.g = end_node.h = end_node.f = 0

    #Creamos la lista abierta y cerrada para nodos
    lista_abierta = [] 
    lista_cerrada = []

    #Agregue el cuadrado inicial (o nodo) a la lista abierta.
    lista_abierta.append(start_node)
    
    cont_it = 0
    max_iterations = (len(maze) // 2)  * 100

    # Loop hasta encontrar el nodo final
    while len(lista_abierta) > 0:
        

        cont_it += 1
        # si llegamos a este punto, devolvemos el camino, ya que puede que no haya solución o
        # el costo de computación es demasiado alto
        if cont_it > max_iterations:
            print ("Demasiadas iteraciones")
            path = []
            current = nodo_Actual
            while current is not None:
                path.append(current.position)

                # Actualizo el actual por el padre del mismo
                current = current.parent
            return path[::-1]


        #Busque el cuadrado de costo F más bajo en la lista abierta. Nos referimos a esto como el cuadrado actual
        nodo_Actual = lista_abierta[0]
        current_index = 0
        for index, item in enumerate(lista_abierta):
            if item.f < nodo_Actual.f: # Buscar la celda de menor F
                nodo_Actual = item
                current_index = index
        
        

        # ELiminar la celda actual de la lista abierta, agregar a la lista cerrada
        lista_abierta.pop(current_index)
        lista_cerrada.append(nodo_Actual)
        
        # Condicional de llegar al objetivo
        if nodo_Actual == end_node:
            path = []
            current = nodo_Actual
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] 
        
        # Generar hijos para la siguiente lista abierta
        children = [] # Generamos maximo 4 hijos
        for new_position in [(-1, 0), (1, 0), (0, -1), (0, 1)]: #Solo me puedo mover vertical y horizontalmente
            # Prioridades: Arriba, Abajo, Izquierda, Derecha
            # Obtener la posicion del nodo
            posicion_nodo = (nodo_Actual.position[0] + new_position[0], nodo_Actual.position[1] + new_position[1])
            
            # Asegurarme que el nodo este dentro de las dimensiones del mapa
            if posicion_nodo[0] > (len(maze) - 1) or posicion_nodo[0] < 0 or posicion_nodo[1] > (len(maze[len(maze)-1]) -1) or posicion_nodo[1] < 0:
                continue
            # Asegurarme que estoy en una casilla sin obstaculo
            if maze[posicion_nodo[0]][posicion_nodo[1]] != 0:
                continue
             
            # Crear un nuevo nodo- un hijo
            nuevo_node = nodoo(nodo_Actual, posicion_nodo)
            
            # Si pasa todas las pruebas, agregar el nuevo nodo
            children.append(nuevo_node)
        

        # Para cada elemento de la lista children se verifica si ya se analizo antes
        for nodo_children in children:

             # Child is on the closed list
            for nodo_lista_cerrada in lista_cerrada:
                if nodo_children == nodo_lista_cerrada: # Si ya pertenece a la lista cerrada, no se continua analizando lo de abajo
                    continue
                
            #En caso de que no perteneza a la lista cerrada, sucede lo siguiente

            # Calcular f,g,h
            nodo_children.g = nodo_Actual.g + 1 #distancia entre el nodo actual y el nodo inicial
            nodo_children.h = ((nodo_children.position[0] - end_node.position[0]) ** 2) + ((nodo_children.position[1] - end_node.position[1]) ** 2) #Distancia Manhattan
            nodo_children.f = nodo_children.g + nodo_children.h #Costo Total

            # Verificar que no vuelve a una casilla donde ya estuvo
            for nodo_lista_abierta in lista_abierta:

                
                if nodo_children == nodo_lista_abierta and nodo_children.g > nodo_lista_abierta.g: 
                    continue
            
            # Añadir el nodo_children a la lista abierta si paso todas las pruebas
            lista_abierta.append(nodo_children)
    


def MostrarMapa(NombreMapa, titulo, maze):
    # Generar Figura
    plt.matshow(maze)
    # Agregar nombre a los ejes
    # Los ejes estan invertidos
    plt.xlabel("Coordenada Y", size = 16,)
    plt.ylabel("Coordenada X", size = 16)
    
    # Agregar el titulo
    plt.title(
        titulo, 
        fontdict={'color':'black', 'size':16},
        loc='center')
    
    # Guardar figura
    plt.savefig(NombreMapa)   

def validacion_coordenadas(Ax, Ay, Bx, By, maze):
    # Saber el tamaño de la matriz del laberinto
    val_y=len(maze) -1      # Alto de laberinto
    val_x=len(maze[0]) -1   # Ancho del laberinto

    # Validamos que este dentro del mapa
    if (0<=Ax<=val_x) and (0<=Ay<=val_y) and (0<=Bx<=val_x) and (0<=By<=val_y):
        return True
    else:
        return False


def solucion(Ax, Ay, Bx, By):
    # Cast: Conversión string a int
    Ax, Ay, Bx, By = int(Ax), int(Ay), int(Bx), int(By)
    
    # Obtener el Mapa
    maze = Lab.Mapa()

    # Validar que el input sea el correcto (== True), sino resaltar el error
    if validacion_coordenadas(Ax, Ay, Bx, By, maze):
    
        # Establecer los puntos de comienzo y fin
        # El programa lee las coordenadas como (x,y)
        PuntoStart = (Ax, Ay) # 0,0
        PuntoEnd = (Bx, By) #7,7
        
        # PuntoStart = (2,2) # 0,0
        # PuntoEnd = (16,16) # 7,7

        print('\nLa trayectoria solución que se debe seguir es:')
        # Pasamos los parametros del mapa, el punto A y B y devuelve el string solucion
        path = astar(maze, PuntoStart, PuntoEnd) 
        print(path) 

        # Agregar al Mapa la secuencia de la solucion
        lista = []
        for i in range(len(path)): # El sistema de referencia esta invertido
            num1 = path[i][0] # Coordenada Y
            num2 = path[i][1] # Coordenada X

            # Pasamos las coordenadas a graficar como (y,x)
            # Los ejes estan invertidos
            lista.append(num1)
            lista.append(num2)

        # Colorear los puntos solucion
        for i in range(0,len(lista),2):
            maze[lista[i]][lista[i+1]] = 5 
        # Puntos A y B de distinto Color
        maze[lista[0]][lista[1]] = 7 
        maze[lista[len(lista)-2]][lista[len(lista)-1]] = 7 
        # Mostrar el Mapa con la solucion
        MostrarMapa('mapa_solucion.png','Mapa Solución', maze)

        # Output para interfaz gráfica
        imagen_output = Image.open('mapa_solucion.png')

        return path, imagen_output
    
    else:
        print("ERROR: Coordenada fuera del Laberinto")
        return "ERROR: Coordenada fuera del Laberinto", None
    

if __name__ == '__main__': #Para que se pueda usar sin interfaz grafica
    
    print('--------------------Método A*--------------------')
    print('Llegar del punto A al punto B con el método A*')
    print('La esquina superior izquierda es la coordenada (0,0)')
    maze = Lab.Mapa()
    MostrarMapa('mapa.png','Mapa', maze)

    #Saber el tamaño de la matriz del laberinto
    val_y=len(maze) -1 #Alto de laberinto
    val_x=len(maze[0]) -1 #Ancho del laberinto

    #Validar datos para una solución valida
    flag = True
    while(flag):
        #Solicitamos Coordenadas
        print('\nIngrese la coordenada del punto A')
        Ax = int(input ('Coordenada X: '))
        Ay = int(input ('Coordenada Y: '))

        #Validamos que este dentro del mapa
        if(0<=Ax<=val_x) and (0<=Ay<=val_y):
            flag = False
        else:
            print("Error - Coordenada fuera del Laberinto")
            print("Ingrese una Coordenada valida")

    flag = True
    while(flag):
        #Solicitamos Coordenadas
        print('\nIngrese la coordenada del punto B')
        Bx = int(input ('Coordenada X: '))
        By = int(input ('Coordenada Y: '))

        #Validamos que este dentro del mapa
        if(0<=Bx<=val_x) and (0<=By<=val_y):
            flag = False
        else:
            print("Error - Coordenada fuera del Laberinto")
            print("Ingrese una Coordenada valida")

    solucion(Ax, Ay, Bx, By)
