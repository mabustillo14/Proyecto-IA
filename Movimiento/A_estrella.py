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
    open_list = [] 
    closed_list = []

    #Agregue el cuadrado inicial (o nodo) a la lista abierta.
    open_list.append(start_node)
    
    # Loop until you find the end
    while len(open_list) > 0:
        
        #Busque el cuadrado de costo F más bajo en la lista abierta. Nos referimos a esto como el cuadrado actual
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index
        
        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)
        
        # Encontrar el objetivo
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] 
        
        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: #Solo me puedo mover vertical y horizontalmente
            
            # Obtener la posicion del nodo
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
            
            # Asegurarme que el nodo este dentro de las dimensiones del mapa
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue
            # Asegurarme que estoy en una casilla sin obstaculo
            if maze[node_position[0]][node_position[1]] != 0:
                continue
             
            # Crear un nuevo nodo
            new_node = nodoo(current_node, node_position)
            
            # Agregar el nuevo nodo
            children.append(new_node)
        
        # Loop through children
        for child in children:
             # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

             # Create the f, g, and h values
            child.g = current_node.g + 1 #distancia entre el nodo actual y el nodo inicial
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2) #Distancia Manhattan
            child.f = child.g + child.h #Costo Total

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue
            # Add the child to the open list
            open_list.append(child)

def MostrarMapa(NombreMapa, titulo, maze):
    # Generar Figura
    plt.matshow(maze)
    # Agregar nombre a los ejes
    plt.xlabel("Coordenada X", size = 16,)
    plt.ylabel("Coordenada Y", size = 16)
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
        for i in range(len(path)):
            num1 = path[i][0] # Coordenada X
            num2 = path[i][1] # Coordenada Y
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
