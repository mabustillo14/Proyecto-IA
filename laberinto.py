import matplotlib.pyplot as plt

class nodoo():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0
    def __eq__(self, other):
        return self.position == other.position

def astar(maze, start, end):
    start_node = nodoo(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = nodoo(None, end)
    end_node.g = end_node.h = end_node.f = 0

    open_list = []
    closed_list = []

    open_list.append(start_node)

    while len(open_list) > 0:

        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        open_list.pop(current_index)
        closed_list.append(current_node)

        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] 

        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: 
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            if maze[node_position[0]][node_position[1]] != 0:
                continue

            new_node = nodoo(current_node, node_position)

            children.append(new_node)

        for child in children:
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue
            open_list.append(child)

def Mapa():
    #Definir el mapa del problema
    #Los 0 es por donde se puede pasar y los 1 por donde no se puede cruzar
    maze = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    return maze

def MostrarMapa(NombreMapa, titulo, maze):
    #Generar Figura
    plt.matshow(maze)
    #Agregar nombre a los ejes
    plt.xlabel("Coordenada X", size = 16,)
    plt.ylabel("Coordenada Y", size = 16)
    #Agregar el titulo
    plt.title(titulo, 
          fontdict={'family': 'fantasy', 
                    'color' : 'black',
                    
                    'size': 16},
          loc='center')

    #Guardar figura
    plt.savefig(NombreMapa)
    
    #Generar Ventana emergente
    plt.show()    

def main(Ax, Ay, Bx, By):
    
    #Obtener el Mapa
    maze = Mapa()

    #Establecer los puntos de comienzo y fin
    #PuntoStart = (int(Ax), int(Ay)) # 0,0
    #PuntoEnd = (int(Bx), int(By)) #7,7
    PuntoStart = (0,0) # 0,0
    PuntoEnd = (7,7) #7,7

    print('\nLa trayectoria solución que se debe seguir es:')
    #Pasamos los parametros del mapa, el punto A y B y devuelve el string solucion
    path = astar(maze, PuntoStart, PuntoEnd) 
    print(path)

    #Agregar al Mapa la secuencia de la solucion
    lista = []
    for i in range(len(path)):
        num1 = path[i][0] #Coordenada X
        num2 = path[i][1] #Coordenada Y
        lista.append(num1)
        lista.append(num2)
    
    #Colorear los puntos solucion
    for i in range(0,len(lista),2):
        maze[lista[i]][lista[i+1]] = 5 
    #Puntos A y B de distinto Color
    maze[lista[0]][lista[1]] = 7 
    maze[lista[len(lista)-2]][lista[len(lista)-1]] = 7 
    #Mostrar el Mapa con la solucion
    MostrarMapa('mapa_solucion.png','Mapa Solución', maze)


    

if __name__ == '__main__':
    print('--------------------Método A*--------------------')
    print('Llegar del punto A al punto B con el método A*')
    print('La esquina superior izquierda es la coordenada (0,0)')
    maze = Mapa()
    MostrarMapa('mapa.png','Mapa', maze)


    print('\nIngrese la coordenada del punto A')
    """
    Ax = input ('Coordenada X: ')
    Ay = input ('Coordenada Y: ')
    print('\nIngrese la coordenada del punto B')
    Bx = input ('Coordenada X: ')
    By = input ('Coordenada Y: ')
    """
    Ax= 0
    Bx= 0
    Ay= 7
    By= 7 
    main(Ax, Ay, Bx, By)





    