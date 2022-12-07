def Apilar(x,y): #Apilar un bloque sobre otro
    print("\tApilar("+ x +"," + y + ")")
    print("\t\tPRECOND: Libre(" + y + "), Sujetar(" + x + "), Caja("+ x + "), Caja(" + y + ") (" + x + " ≠ " + y +")")
    print("\t\tEFECTO: Libre(Brazo), Sobre(" + x + "," + y +"), Libre("+ x +"), ~Libre("+ y +")")

def Desapilar(x,y):#Quitar un bloque que estaba sobre otro
    print("\tDesapilar("+ x +"," + y + ")")
    print("\t\tPRECOND: Sobre(" + x + "," + y + ") , Caja("+ x + "), Caja(" + y + "), Libre(" + x + "), Libre(Brazo), (" + x + " ≠ " + y +")")
    print("\t\tEFECTO: Sujetar (" + x + "), Libre (" + y + "), ~Sobre(" + x + "," + y + ") ~Libre(Brazo)" )

def Sujetar(x): #Sujetar un bloque de la Mesa
    print("\tSujetar(" + x + ")")
    print("\t\tPRECOND: Libre("+ x + "), Libre(Brazo), Caja("+ x + ")")
    print("\t\tEFECTO: Sujetar (" + x + "), ~Libre(Brazo)")

def Soltar(x,mesa): #Soltar un bloque en la Mesa
    print("\tSoltar(" + x + ","+ mesa +")")
    print("\t\tPRECOND: Sujetar(" + x + "), ~Libre(Brazo), Caja("+ x + ")")
    print("\t\tEFECTO: En_Mesa (" + x + ","+ mesa +"), ~Sujetar(" + x + "), Libre(" + x + "), Libre(Brazo)" )    

def Mostrar_Apilado(Apilado):
    print("Representación Simbolica del Resultado de la secuencia:")
    for i in range(len(Apilado)):
        print("\t-------------------------")
        print("\t|\t", Apilado[len(Apilado)-1-i]," \t|")
    print("\t=========================\n")


def Solucion(Posicion_Inicial,Caja_1,Caja_2,Caja_3,Caja_4): #Secuencia de pasos a seguir
    secuencia_objetivo = [Caja_4,Caja_3,Caja_2,Caja_1] #Posicion Final
    mesas = ["mesa A","mesa B", "mesa C", "mesa D"]

    #Validamos los datos ingresados
    #Convertimos la lista en un ser donde no toma elementos repetidos
    if(len(secuencia_objetivo) == len(set(secuencia_objetivo))):#La secuencia tiene la misma cantidad de componentes de la posicion inicial y no se repite ninguna
       
        #Auxiliares
        Orden = [] #Como estan apoyadas en la mesa
        pie = Posicion_Inicial.index(Caja_4)#La mesa sobre donde esta el inicio de la nueva torre

        #Añadir las Condiciones del Problema
        inicio = "Sobre(" +Posicion_Inicial[0] + "," +  mesas[0]+"), "
        objetivo = "Sobre(" +secuencia_objetivo[0] + "," +  mesas[pie]+"), "
        objetos = "Caja("+Posicion_Inicial[0] +"), "
        superficies = mesas[0] +", "

        #Salida: Secuencia Solución y Costo 
        secuencia = ""
        costo = 0
        
        for i  in range(len(Posicion_Inicial)-1):
            #Anadir Condiciones Iniciales
            #inicio +="(" + Posicion_Inicial[i+1] + " sobre " + Posicion_Inicial[i] + "), "
            inicio += "Sobre(" + Posicion_Inicial[i+1] + "," + Posicion_Inicial[i] + "), "
            #Anadir el Objetivo del problema
            objetivo += "Sobre(" + secuencia_objetivo[i+1] + "," + secuencia_objetivo[i] + "), "
            objetos += "Caja("+Posicion_Inicial[i+1] +"), "
            superficies += mesas[i+1] + ", "
        objetos += superficies + " Brazo"
        inicio += "Libre(" + secuencia_objetivo[len(secuencia_objetivo)-1] + "), Libre(Brazo)"

        #Mostrar por pantalla Condiciones Iniciales
        print("\n--------------------------------------------------------------------")
        print("PROPIEDADES:")
        print("\tObjetos: " + objetos )
        print("\tInicio: " + inicio)
        print("\tObjetivo: " + objetivo)

        #Mostrar las Funciones disponibles
        print("\n--------------------------------------------------------------------")
        print("ACCIONES:")
        Desapilar("x","y")
        Sujetar("x")
        Soltar("x", "mesa")
        Apilar("x", "y")

        #Poner todas las cajas sobre la mesa
        for i in range(len(Posicion_Inicial)-1):
            mover_pieza = Posicion_Inicial[len(Posicion_Inicial)-1-i]
            pieza_apoyada = Posicion_Inicial[len(Posicion_Inicial)-2-i]
            secuencia += "Desapilar(" + mover_pieza + "," + pieza_apoyada+"), "
            costo +=1
            #Desapilar(mover_pieza, pieza_apoyada)
            secuencia += "Sujetar(" + mover_pieza + "), "
            costo +=1
            secuencia += "Soltar(" + mover_pieza + ","+ mesas[len(mesas)-i-1]+"), "
            costo +=1
            Orden.append(Posicion_Inicial[i])
            
        #Secuencia de Apilamiento para obtener la posicion final
        flag = True
        i=1 #Porque la base del nuevo apilado esta sobre la mesa
        while (flag):
            if(i == len(secuencia_objetivo)-1):
                flag = False

            for j in range(len(Orden)):
                if(secuencia_objetivo[i]==Orden[j]):
                    secuencia += "Sujetar(" + Orden[j] + "), "
                    costo +=1
                    #Sujetar(Orden[j])
                    
                    secuencia += "Apilar(" + Orden[j] + "," + secuencia_objetivo[i-1] + "), "
                    costo +=1
                    #Apilar(Orden[j], Posicion_Final[i-1])
                    ##Plan.append("Poner " + Orden[j] + " sobre " + Posicion_Final[i-1])
            i+=1

        print("\n--------------------------------------------------------------------")
        print("OUTPUTS: ")
        print("Secuencia Solución: ")
        print(secuencia)
        print("\tCantidad de Movimientos: " + str(costo) + " Movimientos"  )
        
        print("\n--------------------------------------------------------------------")
        Mostrar_Apilado(secuencia_objetivo)
           
        return objetos, inicio, objetivo, secuencia, str(costo) + " Movimientos"
    else:
        return ("Error - Intente de nuevo ingresar un orden de apilamiento valido\n"), None, None, None, None



if __name__ == '__main__': #Para que se pueda usar sin interfaz
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
   
    #Ejecutar la funcion para obtener la solucion
    Solucion(Posicion_Inicial, Posicion_Final[3],Posicion_Final[2],Posicion_Final[1], Posicion_Final[0])

    print("\nFin de la Ejecución")



