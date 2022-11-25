if __name__ == '__main__':
    print('--------------------Lenguaje STRIPS--------------------')
    Posicion_Inicial = ['R1','R2','R3','R4']
    Posicion_Final = ['R3','R1','R4','R2']
    Soportes = ['A', 'B', 'C']
    #print("Posicion Inicial ", Posicion_Inicial)
    #print("Posicion Final ", Posicion_Final)

    Disposicion = [Posicion_Inicial,[],[]]

    #Desarmar la pila
    for i in range(len(Soportes)-1):
        mover_pieza = Posicion_Inicial[len(Posicion_Inicial)-1]
        Disposicion[len(Soportes)-1-i].append(mover_pieza)

        print("Mover la caja", mover_pieza, " a ", Soportes[len(Soportes)-1-i])        
        Posicion_Inicial.pop()

    
    print(Disposicion)
    #Determinar donde esta la base de la posicion final
    for i in range(len(Disposicion)):
        if Posicion_Final[0] in Disposicion[i]:
            pie = Disposicion[i].index(Posicion_Final[0])
            rama = Soportes[i]

    #print(pieza1, rama)    



    
   






