"""
Operadores
"""
def Apilar(x,y): #Apilar un bloque sobre otro
    text_Apilar = "\tApilar("+ x +"," + y + ") \n"
    text_Apilar += "\t\tPRECOND: Libre(" + y + "), Sujetar(" + x + "), Caja("+ x + "), Caja(" + y + ") (" + x + " ≠ " + y +") \n"
    text_Apilar += "\t\tEFECTO: Libre(Brazo), Sobre(" + x + "," + y +"), Libre("+ x +"), ~Libre("+ y +")\n"
    text_Apilar += "\t\tCosto del Camino: 1 movimiento"
    print(text_Apilar)

def Desapilar(x,y):#Quitar un bloque que estaba sobre otro
    text_Desapilar = "\tDesapilar("+ x +"," + y + ") \n"
    text_Desapilar += "\t\tPRECOND: Sobre(" + x + "," + y + ") , Caja("+ x + "), Caja(" + y + "), Libre(" + x + "), Libre(Brazo), (" + x + " ≠ " + y +") \n"
    text_Desapilar += "\t\tEFECTO: Sujetar (" + x + "), Libre (" + y + "), ~Sobre(" + x + "," + y + ") ~Libre(Brazo) \n"
    text_Desapilar += "\t\tCosto del Camino: 0 movimiento"
    print(text_Desapilar)

def Sujetar(x): #Sujetar un bloque de la Mesa
    text_Sujetar = "\tSujetar(" + x + ") \n"
    text_Sujetar += "\t\tPRECOND: Libre("+ x + "), Libre(Brazo), Caja("+ x + ") \n"
    text_Sujetar += "\t\tEFECTO: Sujetar (" + x + "), ~Libre(Brazo) \n" 
    text_Sujetar +="\t\tCosto del Camino: 0 movimiento"
    print(text_Sujetar)

def Soltar(x,mesa): #Soltar un bloque en la Mesa
    text_Soltar = "\tSoltar(" + x + ","+ mesa +") \n"
    text_Soltar += "\t\tPRECOND: Sujetar(" + x + "), ~Libre(Brazo), Caja("+ x + ") \n"
    text_Soltar += "\t\tEFECTO: En_Mesa (" + x + ","+ mesa +"), ~Sujetar(" + x + "), Libre(" + x + "), Libre(Brazo) \n"
    text_Soltar +="\t\tCosto del Camino: 1 movimiento"
    print(text_Soltar)    


"""
Representación por Consola
"""
def Mostrar_Apilado(Apilado):
    print("Representación Simbolica del Resultado de la secuencia:")
    for i in range(len(Apilado)):
        print("\t-------------------------")
        print("\t|\t", Apilado[len(Apilado)-1-i]," \t|")
    print("\t=========================\n")


"""
Mostrar Propiedades por Pantalla
"""
def mostrar_Propiedades(Posicion_Inicial, secuencia_objetivo,mesas):
    #Auxiliares
    pie = Posicion_Inicial.index(secuencia_objetivo[0])#La mesa sobre donde esta el inicio de la nueva torre

    #Añadir las Condiciones del Problema
    inicio = "Sobre(" +Posicion_Inicial[0] + "," +  mesas[0]+"), "
    objetivo = "Sobre(" +secuencia_objetivo[0] + "," +  mesas[pie]+"), "
    objetos = "Caja("+Posicion_Inicial[0] +"), "
    superficies = mesas[0] +","

    for i  in range(len(Posicion_Inicial)-1):
        #Anadir Condiciones Iniciales
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
    print("OPERADORES:")
    Desapilar("x","y")
    Sujetar("x")
    Soltar("x", "mesa")
    Apilar("x", "y")

    return [objetos, inicio, objetivo]




def Solucion(Posicion_Inicial,Caja_1,Caja_2,Caja_3,Caja_4): #Secuencia de pasos a seguir
    # Elementos Iniciales
    secuencia_objetivo = [Caja_4,Caja_3,Caja_2,Caja_1] #Posicion Final - orden ascendente
    mesas = ["mesa A","mesa B", "mesa C", "mesa D"]

    if(Caja_1 != None) and (Caja_2 != None) and (Caja_3 != None) and (Caja_4 != None): # Cada opcion tiene una selección

        #Validamos los datos ingresados
        #Convertimos la lista en un ser donde no toma elementos repetidos
        if(len(secuencia_objetivo) == len(set(secuencia_objetivo))):#La secuencia tiene la misma cantidad de componentes de la posicion inicial y no se repite ninguna
        
            Propiedades = mostrar_Propiedades(Posicion_Inicial, secuencia_objetivo,mesas)

            #Salida: Secuencia Solución y Costo 
            Orden = [Posicion_Inicial[0]]

            secuencia = ""
            costo = 0
            poner_en_mesa = True
            cant_cajas = len(Posicion_Inicial)
            

            """
            Caso 1: El apilamiento inicial es el mismo del apilamiento final 
            """
            # Verificar si el apilamiento inicial es igual al final
            if(Posicion_Inicial == secuencia_objetivo):
                return Propiedades[0], Propiedades[1], Propiedades[2], "No hay movimientos", str(0) + " Movimientos"

            
            """
            Caso 2: El apilamiento inicial es la inversa del apilamiento final 
            """
            # Comprobar si secuencia objetivo es la inversa de posicion inicial
            if(Posicion_Inicial== list(reversed(secuencia_objetivo))):
                print ("Es la inversa")
                poner_en_mesa = False
                Orden = Posicion_Inicial

                mover_pieza = Posicion_Inicial[cant_cajas-1]
                pieza_apoyada = Posicion_Inicial[cant_cajas-2]
                secuencia += "Desapilar(" + mover_pieza + "," + pieza_apoyada+") \n"
                secuencia += "Soltar(" + mover_pieza + ","+ mesas[1]+") \n"
                costo +=1
                
            """
            Caso 3: No hay relación directa entre apilamiento inicial y apilamiento final
            """
            if(poner_en_mesa):
            #Poner todas las cajas sobre la mesa
                for i in range(cant_cajas-1):
                    mover_pieza = Posicion_Inicial[cant_cajas-1-i]
                    pieza_apoyada = Posicion_Inicial[cant_cajas-2-i]
                    secuencia += "Desapilar(" + mover_pieza + "," + pieza_apoyada+") \n"
                    secuencia += "Soltar(" + mover_pieza + ","+ mesas[i+1]+") \n"
                    costo +=1
                    Orden.append(Posicion_Inicial[cant_cajas-1-i])
            print(Orden) #orden sobre la mesa de derecha a izquierda



            #Secuencia de Apilamiento para obtener la posicion final
            flag = True
            i=1 #Porque la base del nuevo apilado esta sobre la mesa
            while (flag):
                if(i == cant_cajas-1):
                    flag = False

                for j in range(len(Orden)):
                    if(secuencia_objetivo[i]==Orden[j]):
                        
                        if(poner_en_mesa == False) and j!=0: # Si esta caja sobre otra caja
                            secuencia += "Desapilar(" + Orden[j] + "," + Orden[j-1]+") \n"
                        else: # Si esta caja sobre la mesa
                            secuencia += "Sujetar(" + Orden[j] + ") \n"
                        
                        secuencia += "Apilar(" + Orden[j] + "," + secuencia_objetivo[i-1] + ") \n"
                        costo +=1
                
                i+=1
        
            print("\n--------------------------------------------------------------------")
            print("OUTPUTS: ")
            print("Secuencia Solución en lenguaje STRIPS: ")
            print(secuencia)
            print("\tCantidad de Movimientos: " + str(costo) + " Movimientos"  )
            
            print("\n--------------------------------------------------------------------")
            Mostrar_Apilado(secuencia_objetivo)
            
            return Propiedades[0], Propiedades[1], Propiedades[2], secuencia, str(costo) + " Movimientos"
        else:
            return ("Error - Intente de nuevo ingresar un orden de apilamiento válido\n"), None, None, None, None
    else:
        return ("Error - Rellene todos los campos\n"), None, None, None, None


"""
Ejecución por Consola
"""
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



