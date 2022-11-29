#Variable Global de Instrucciones en formato STRIPS
global Intrucciones
Instrucciones = []

def Apilar(x,y): #Apilar un bloque sobre otro
    global Intrucciones
    Instrucciones.append("Apilar("+ x +"," + y + ")")
    Instrucciones.append("\tPRECOND: Libre(" + y + "), Sujetar(" + x + ")")
    Instrucciones.append("\tEFECTO: Brazo_Libre, Sobre(" + x + "," + y +"), Libre("+ x +")")

def Desapilar(x,y):#Quitar un bloque que estaba sobre otro
    global Intrucciones
    Instrucciones.append("Desapilar("+ x +"," + y + ")")
    Instrucciones.append("\tPRECOND: Sobre(" + x + "," + y + ") , Libre(" + x + "), Brazo_Libre")
    Instrucciones.append("\tEFECTO: Sujetar (" + x + "), Libre (" + y + ")")

def Sujetar(x): #Sujetar un bloque de la Mesa
    global Intrucciones
    Instrucciones.append("Sujetar(" + x + ")")
    Instrucciones.append("\tPRECOND: Libre("+ x + ") , En_Mesa(" + x + "), Brazo_Libre")
    Instrucciones.append("\tEFECTO: Sujetar (" + x + ")")

def Soltar(x): #Soltar un bloque en la Mesa
    global Intrucciones
    Instrucciones.append("Soltar(" + x + ")")
    Instrucciones.append("\tPRECOND: Sujetar(" + x + ")")
    Instrucciones.append("\tEFECTO: En_Mesa (" + x + "), Brazo_Libre, Libre(" + x + ")")

def Solucion(Posicion_Inicial, Posicion_Final):
    Orden = [Posicion_Inicial[0]]
    Plan = []
    global Intrucciones
    
    #Añadir las Condiciones del Problema
    inicio = ""
    objetivo =  ""
    for i  in range(len(Posicion_Inicial)-1):
        #Anadir Condiciones Iniciales
        inicio +="(" + Posicion_Inicial[i+1] + " sobre " + Posicion_Inicial[i] + "), "
        #Anadir el Objetivo del problema
        objetivo += "(" + Posicion_Final[i+1] + " sobre " + Posicion_Final[i] + "), "
    Instrucciones.append("Inicio: " + inicio)
    Instrucciones.append("Objetivo: " + objetivo + "\n")

    for i in range(len(Posicion_Inicial)-1):
        mover_pieza = Posicion_Inicial[len(Posicion_Inicial)-1-i]
        pieza_apoyada = Posicion_Inicial[len(Posicion_Inicial)-2-i]
        Desapilar(mover_pieza, pieza_apoyada)
        Soltar(mover_pieza)
        Plan.append("Poner " + mover_pieza + " sobre la Mesa ")
        Orden.append(mover_pieza)

    #Buscamos la base de la nueva pila
    pie = Orden.index(Posicion_Final[0])
    i=0
    j=1
    flag = True
    while(flag):
        if(i == len(Posicion_Final)-1):
            flag=False
        
        if(Orden[i] == Posicion_Final[j] ):
            Plan.append("Poner " + Orden[i] + " sobre " + Posicion_Final[j-1])
            Sujetar(Orden[i])
            Apilar(Orden[i], Posicion_Final[j-1])
            i=0
            j+=1
        
        i+=1
    
    #Mostrar Solucionn para el Usuario
    print("\nSolucion para el Usuario\n")    
    for i  in range(len(Plan)):
        print(Plan[i])
    
    #Mostrar Solucion en lenguaje STRIPS
    print("\nInstrucciones en formato Strips\n")
    for i  in range(len(Instrucciones)):
        print(Instrucciones[i])
    

def Mostrar_Apilado(Apilado):
    for i in range(len(Apilado)):
        print("-------------------------")
        print("|\t", Apilado[len(Apilado)-1-i]," \t|")
    print("=========================\n")


if __name__ == '__main__':
    print('--------------------Lenguaje STRIPS--------------------')
  
    #Extraemos los datos del txt que contiene el orden de apilamiento con vision artificial
    with open("datos.txt") as archivo:
        for linea in archivo:
            Posicion_Inicial = linea.split(",")
            Posicion_Inicial.pop()
    print("\nApilamiento ascendente Inicial: ", Posicion_Inicial)

    
    flag = True
    while(flag):
        print("\nIngrese la nueva secuencia de apilamiento, comenzando por la base")
        for i in range(len(Posicion_Inicial)):
            print(str(i) + " - " + Posicion_Inicial[i])
        nuevo_objetivo = input("Separado por una coma(,): ")
        secuencia_objetivo = nuevo_objetivo.split(",")
        

        #Validamos los datos ingresados
        #Convertimos la lista en un ser donde no toma elementos repetidos
        if(len(Posicion_Inicial) == len(set(secuencia_objetivo))):
            #La secuencia tiene la misma cantidad de componentes de la posicion inicial y no se repite ninguna
            flag = False
        else:
            print("Error - Intente de nuevo ingresar una secuencia valida\n")
    
    #Conociendo el orden del nuevo apilamiento, hacemos la asignacion de la nueva posicion final
    Posicion_Final = []
    for i in range(len(secuencia_objetivo)):
        Posicion_Final.append(Posicion_Inicial[int(secuencia_objetivo[i])])
    
    print("\nApilamiento ascendente Objetivo: ", Posicion_Final)
   
    #Posicion_Inicial = ['R1','R2','R3','R4','R5']
    #Posicion_Final = ['R3','R1','R4','R5','R2']
    #print("Posicion Inicial ", Posicion_Inicial)
    #print("Posicion Final ", Posicion_Final)

    #Ejecutar la funcion para obtener la solucion
    Solucion(Posicion_Inicial, Posicion_Final)

    print("\nRepresentación Gráfica de la Posición Inicial de Apilado")
    Mostrar_Apilado(Posicion_Inicial)

    print("\nRepresentación Gráfica de la Posición Final de Apilado")
    Mostrar_Apilado(Posicion_Final)

    print("\nFin de la Ejecución")