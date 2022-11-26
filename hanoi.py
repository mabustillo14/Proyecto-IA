if __name__ == '__main__':
    print('--------------------Lenguaje STRIPS--------------------')
    Posicion_Inicial = ['R1','R2','R3','R4']
    Posicion_Final = ['R3','R1','R4','R2']
    Soportes = ['A', 'B', 'C']
    #print("Posicion Inicial ", Posicion_Inicial)
    print("Posicion Final ", Posicion_Final)

    Disposicion = [Posicion_Inicial,[],[]]

    #Desarmar la pila
    for i in range(len(Soportes)-1):
        mover_pieza = Posicion_Inicial[len(Posicion_Inicial)-1]
        Disposicion[len(Soportes)-1-i].append(mover_pieza)

        print("Mover la caja", mover_pieza, " a ", Soportes[len(Soportes)-1-i])        
        Posicion_Inicial.pop()

    
    print(Disposicion)
    #Determinar donde esta la base de la posicion final
    raiz = -1
    for i in range(len(Soportes)-1):
        if Disposicion[i][0] == Posicion_Final[0]: 
            raiz = i
    
    #Significa que esta apilada sobre la primer pieza de A
    if(raiz ==-1):
        Disposicion[2].append(Disposicion[1][0])
        print("Mover la caja", Disposicion[1][0], " a ", Soportes[len(Soportes)-1])
        Disposicion[1].pop()

        Disposicion[1].append(Disposicion[0][1])
        print("Mover la caja", Disposicion[0][1], " a ", Soportes[len(Soportes)-2])
        Disposicion[0].pop()
        raiz = 0
    #Ya tendremos la raiz a nivel 0

    rodilla = -1
    for i in range(len(Soportes)-1):
        if Disposicion[i][0] == Posicion_Final[1]: 
            rodilla = i
            print("Mover la caja", Posicion_Final[1], " a ", Soportes[raiz])
    
    
    
    
    print (rodilla)



    print(Disposicion) 
        


    #print(pieza1, rama)    



    
   











