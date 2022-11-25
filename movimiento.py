if __name__ == '__main__':
    print('--------------------Lenguaje STRIPS--------------------')
    Posicion_Inicial = ['R1','R2','R3','R4']
    Posicion_Final = ['R3','R1','R4','R2']
    Soportes = ['A', 'B', 'C', 'D']
    print("Posicion Inicial ", Posicion_Inicial)
    print("Posicion Final ", Posicion_Final)
    Orden = [Posicion_Inicial[0]]

    for i in range(len(Soportes)-1):
        mover_pieza = Posicion_Inicial[len(Posicion_Inicial)-1-i]
        print("Poner", mover_pieza, " en ", Soportes[i+1])
        Orden.append(mover_pieza)

    #print(Orden)

    #Buscamos la base de la nueva pila
    pie = Orden.index(Posicion_Final[0])
    i=0
    j=1
    flag = True
    while(flag):
        if(i == len(Posicion_Final)-1):
            flag=False
        
        if(Orden[i] == Posicion_Final[j] ):
            print("Poner", Orden[i], " en ", Soportes[pie], " sobre ", Posicion_Final[j-1])
            i=0
            j+=1
        
        i+=1
    print("Fin de la Ejecución")


