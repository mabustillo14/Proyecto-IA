#Variable Global de Instrucciones en formato STRIPS
global Intrucciones
Instrucciones = []

def Apilar(x,y): #Apilar un bloque sobre otro
    #print("Apilar(", x,",", y, ")")
    #print("\tPRECOND: Libre(",y,"), Sujetar(",x,")")
    #print("\tEFECTO: Brazo_Libre, Sobre(", x ,",", y ,"), Libre(", x ,")")
    global Intrucciones
    Instrucciones.append("Apilar("+ x +"," + y + ")")
    Instrucciones.append("\tPRECOND: Libre(" + y + "), Sujetar(" + x + ")")
    Instrucciones.append("\tEFECTO: Brazo_Libre, Sobre(" + x + "," + y +"), Libre("+ x +")")

def Desapilar(x,y):#Quitar un bloque que estaba sobre otro
    #print("Desapilar(", x,",", y, ")")
    #print("\tPRECOND: Sobre(",x,",",y,") , Libre(",x,"), Brazo_Libre")
    #print("\tEFECTO: Sujetar (", x ,"), Libre (", y ,")")

    global Intrucciones
    Instrucciones.append("Desapilar("+ x +"," + y + ")")
    Instrucciones.append("\tPRECOND: Sobre(" + x + "," + y + ") , Libre(" + x + "), Brazo_Libre")
    Instrucciones.append("\tEFECTO: Sujetar (" + x + "), Libre (" + y + ")")

def Sujetar(x): #Sujetar un bloque de la Mesa
    #print("Sujetar(",x,")")
    #print("\tPRECOND: Libre(",x,") , En_Mesa(",x,"), Brazo_Libre")
    #print("\tEFECTO: Sujetar (", x ,")")

    global Intrucciones
    Instrucciones.append("Sujetar(" + x + ")")
    Instrucciones.append("\tPRECOND: Libre("+ x + ") , En_Mesa(" + x + "), Brazo_Libre")
    Instrucciones.append("\tEFECTO: Sujetar (" + x + ")")

def Soltar(x): #Soltar un bloque en la Mesa
    #print("Soltar(",x,")")
    #print("\tPRECOND: Sujetar(",x,")")
    #print("\tEFECTO: En_Mesa (", x ,"), Brazo_Libre, Libre(",x,")")
    
    global Intrucciones
    Instrucciones.append("Soltar(" + x + ")")
    Instrucciones.append("\tPRECOND: Sujetar(" + x + ")")
    Instrucciones.append("\tEFECTO: En_Mesa (" + x + "), Brazo_Libre, Libre(" + x + ")")




if __name__ == '__main__':
    print('--------------------Lenguaje STRIPS--------------------')
    Posicion_Inicial = ['R1','R2','R3','R4']
    Posicion_Final = ['R3','R1','R4','R2']
    print("Posicion Inicial ", Posicion_Inicial)
    print("Posicion Final ", Posicion_Final)
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
    
    print("\nSolucion para el Usuario\n")
    
    for i  in range(len(Plan)):
        print(Plan[i])
    


    print("\nInstrucciones en formato Strips\n")
    
    for i  in range(len(Instrucciones)):
        print(Instrucciones[i])
    
    print("\nFin de la Ejecución")


