import Persona
import Articulo

articulos = {}
i = 0
j = 0
CPs = {}
es_fin = False
presidente_elegido = False
lista_aceptados = []
lista_empatados = []
n = 3


def agregarArticulo():
    global presidente_elegido, articulos, j
    resumen = []
    topicos = []
    articulo = Articulo.Articulo("titulo", ["pal1"], [], []) 
    while(True):
        try:
            print "Ingrese el titulo:",
            titulo = raw_input()
            articulo.setTitulo(titulo)
            break
        except:
            continue
        
    while(True):
        try:
            resumen.append(raw_input("Ingrese una palabra resumen: "))
            if raw_input("Desea agregar otra palabra?(Presione 1 si es afirmativo): ") != "1":
                articulo.setResumen(resumen)
                break
            continue
        except ValueError:
            print "Caracter no valido. Intente de nuevo."
            continue
        
    while(True):
        try:
            topicos.append(raw_input("Ingrese el topico del articulo: "))
            if raw_input("Desea agregar otro topico?(Presione 1 si es afirmativo): ") != "1":
                articulo.setTopicos(topicos)
                break
            continue
        except:
            print "Caracter no valido. Intente de nuevo."
            continue
        
    articulos[j]= articulo 
    j = j + 1  

def agregarCP():
    global presidente_elegido, CPs, i
    topicos = []
    miembroCP = Persona.CP("nombre", "apellido", "inst", "pais", [], False) 
    print "Ingrese el nombre: ",
    while(True):
        try:
            nombre = raw_input()
            miembroCP.setNombre(nombre)
            break
        except:
            continue
    print "Ingrese el apellido: ",
    while(True):
        try:
            apellido = raw_input()
            miembroCP.setApellido(apellido)
            break
        except:
            continue
    print "Ingrese la institucion donde trabaja: ",
    while(True):
        try:
            institucion = raw_input()
            miembroCP.setInstitucion(institucion)
            break
        except:
            continue
    print "Ingrese el pais de origen: ",
    while(True):
        try:
            pais = raw_input()
            miembroCP.setPais(pais)
            break
        except:
            continue
    while(True):
        try:
            topicos.append(raw_input("Ingrese el topico que domina el CP: "))
            if raw_input("Desea agregar otro topico?(Presione 1 si es afirmativo): ") != "1":
                miembroCP.setTopicos(topicos)
                break
            continue
        except:
            print "Caracter no valido. Intente de nuevo."
            continue
        
    if not presidente_elegido:
        while(True):
            try:
                p = input("Es el presidente(1 si, 0 no)?")
                if p == 1:
                    miembroCP.setEsPresidente(True) 
                    presidente_elegido = True
                    break
                if p == 0:
                    break
                else:
                    continue
            except:
                    continue
                
        
        
    CPs[i]= miembroCP 
    i = i + 1  
    
def agregarPuntuacion():
    if len(CPs) == 0 :
        print "No hay CP's"
        return
    if len(articulos) == 0 :
        print "No hay articulos que evaluar"
        return
    
    while True:
        print "Elija el arbitro: "
        for cp in CPs:
            print "%s.- %s" % (cp, CPs[cp])
        print "Presione %s para salir" % len(CPs)
        try:
            choice = input()
            if choice == len(CPs):
                return
            CP_elegido = CPs[choice]
            break
        except:
            print "Valor Erroneo. Intente de nuevo"
            continue
        
   
    while True:
        ya_hay_evaluacion = False
        print "Elija el articulo a evaluar"
        for ar in articulos:
            print "%s.- %s" % (ar, articulos[ar])
        print "Presione %s para salir" % len(articulos)
        try:
            choice = input()
            if choice == len(articulos):
                return
            articulo_elegido = articulos[choice]
        except:
            print "Valor Erroneo. Intente de nuevo"
            continue
        
        # Verificamos que el CP no haya evaluado ya el articulos
        for evaluacion in articulo_elegido.getPuntuaciones():
            if(evaluacion[0] == CP_elegido):
                ya_hay_evaluacion = True
                
        if ya_hay_evaluacion == True:
            print "Ya existe una evaluacion del arbitro hacia este articulo"
            continue 
                                            
    
        if len([x for x in articulo_elegido.getTopicos() if x in CP_elegido.getTopicos()]) != 0:
            while True:
                try:
                    articulos[choice].agregarPuntuacion((CP_elegido, input("Elija la nota(1..5): ")))
                    break
                except ValueError:
                    print "Se espera una nota entre 1 y 5"
                    continue
            break
        else:
            print "El CP no es experto en el topico del articulo. Intente de nuevo"
            continue
            
    return
    
        
def generarAceptadosEmpatados():
    global lista_aceptados, lista_empatados, n
    lista_aceptables = [art for art in list(articulos.values()) if art.es_aceptable()]
    if len(lista_aceptables) <= n:
        lista_aceptados = lista_aceptables
        lista_empatados = []
    else:
        lista_aceptables = sorted(lista_aceptables,
                                   key = lambda x: x.calcularPromedio(),
                                   reverse = True)
        primeros_n = lista_aceptables[0:n]
        min_promedio = min([ar.calcularPromedio() for ar in primeros_n])
        print "minpromedio: ", min_promedio
        empatados = [ar for ar in lista_aceptables if ar.calcularPromedio() == min_promedio]
        print "cantidad de empatados: ", len(empatados)
        if len(empatados) > 1:
            lista_empatados = empatados
            lista_aceptados = [ar for ar in primeros_n if ar.calcularPromedio() > min_promedio]
        else:
            lista_aceptados = primeros_n
            lista_empatados = [] 
            
def mostrarAceptados():           
    generarAceptadosEmpatados()
    if len(lista_aceptados) == 0:
        print "No hay articulos aceptados que mostrar"
    else:
        print "########  LISTA DE ARTICULOS ACEPTADOS ########"
        for art in lista_aceptados:
            print "%s. Promedio: %s" % (art, art.calcularPromedio())   
            
    raw_input("Presione cualquier tecla para volver al menu")      
   

def mostrarEmpatados():
    generarAceptadosEmpatados()
    if len(lista_empatados) == 0:
        print "No hay articulos empatados que mostrar"
    else:
        print "########  LISTA DE ARTICULOS EMPATADOS ########"
        for art in lista_empatados:
            print "%s. Promedio: %s" % (art, art.calcularPromedio())    
            
    for art in articulos:   
            print articulos[art], articulos[art].getPuntuaciones()         
    raw_input("Presione cualquier tecla para volver al menu")
    
    
def salir():
    global es_fin
    es_fin = True

if __name__ == "__main__":
  
    comandos = {1 : agregarArticulo, 2 : agregarCP, 3 : agregarPuntuacion, 
                4 : mostrarAceptados, 5 : mostrarEmpatados, 6 : salir}
    while(not es_fin ):
        print "######  CLEI  ######\n"
        print "1.- Agregar Articulo"
        print "2.- Agregar CP"
        print "3.- Agregar puntuacion"
        print "4.- Chequear lista de ACEPTADOS"
        print "5.- Chequear lista de EMPATADOS"
        print "6.- Salir"
        print "Ingrese un entero:"
        try:
            choice = input(">>")
        except :
            continue
        if choice not in range(1,7):
            continue
        comandos[choice]() 
        
        