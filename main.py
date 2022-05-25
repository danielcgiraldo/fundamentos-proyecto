import random
from tkinter import *
import time


# ================================================== FUNCIONES ============================================ #

# ========================= ALEATORIO ============================= #

def mostrar_cartas(lista):
    p=lista[random.randint(0,2)]
    return p


def niveles(nivel):
    global desplazamiento
    global tiempo
    global tiempo_espera
    if nivel<5:
        desplazamiento=10*nivel
        tiempo = 0.05
        tiempo_espera = 0.5
    else:
        desplazamiento = 50
        tiempo = 0.05 - 0.005 * (nivel - 5)
        tiempo_espera = 0.5 - 0.1 * (nivel - 5)
        tiempo_espera = max(0, tiempo_espera)

def cambios(nivel):
    lista_general=["1 2","2 3","1 3"]
    lista_cambios=[]
    for i in range(nivel+4):
        p=lista_general[random.randint(0,2)]
        lista_cambios.append(p)
    return lista_cambios


# ====================================== TKINTER ===================================== #
# ==== MOSTRAR IMAGEN ===== #

def mostrar_carta(carta):
    ancho_carta = q.width()
    altura_carta = q.height()
    canva = Canvas(width=ancho_carta + 70, height=altura_carta + 20)
    canva.pack()
    x = (ancho_carta)/2.0
    y = (altura_carta)/2.0
    if(carta == "Q"):
        carta = canva.create_image(x + 30, y, image=q)
    elif(carta == "K"):
        carta = canva.create_image(x + 30, y, image=k)
    elif(carta == "J"):
        carta = canva.create_image(x + 30, y, image=j)
    root.after(5000, lambda: root.destroy())

def mostrar_game_over():
    ancho_carta = game_over.width()
    altura_carta = game_over.height()
    canva = Canvas(width=ancho_carta + 70, height=altura_carta + 20)
    canva.pack()
    x = (ancho_carta)/2.0
    y = (altura_carta)/2.0
    canva.create_image(x + 30, y, image=game_over)
    root.after(5000, lambda: root.destroy())

# ===== MOVIMIENTO ===== #

def uno_dos(uno, dos, desplazamiento, tiempo):
    canva.move(uno, desplazamiento, 0)
    canva.move(dos, -desplazamiento, 0)
    root.update()
    time.sleep(tiempo)
    if(canva.coords(uno)[0] < 3*longitud_carta + 15):
        uno_dos(uno, dos, desplazamiento, tiempo)
    if(canva.coords(dos)[0] > longitud_carta + 30):
        uno_dos(uno, dos, desplazamiento, tiempo)


def dos_tres(dos, tres, desplazamiento, tiempo):
    canva.move(dos, desplazamiento, 0)
    canva.move(tres, -desplazamiento, 0)
    root.update()
    time.sleep(tiempo)
    if(canva.coords(dos)[0] < 5*longitud_carta + 30):
        dos_tres(dos, tres, desplazamiento, tiempo)
    if(canva.coords(tres)[0] < 3*longitud_carta + 15):
        dos_tres(dos, tres, desplazamiento, tiempo)


def uno_tres(uno, tres, desplazamiento, tiempo):
    canva.move(uno, desplazamiento, 0)
    canva.move(tres, -desplazamiento, 0)
    root.update()
    time.sleep(tiempo)
    if(canva.coords(uno)[0] < 5*longitud_carta + 30):
        uno_tres(uno, tres, desplazamiento, tiempo)
    if(canva.coords(tres)[0] > longitud_carta + 30):
        uno_tres(uno, tres, desplazamiento, tiempo)


def mover(movements, posicion, desplazamiento, tiempo, tiempo_espera):
    if(movements == "1 2"):
        uno_dos(posicion[0][1], posicion[1][1], desplazamiento, tiempo)

        # actualizar posicion e item
        ans_pos = posicion[0]
        posicion[0] = posicion[1]
        posicion[1] = ans_pos
    elif(movements == "2 3"):
        dos_tres(posicion[1][1], posicion[2][1], desplazamiento, tiempo)

        # actualizar posicion e item
        ans_pos = posicion[1]
        posicion[1] = posicion[2]
        posicion[2] = ans_pos
    elif(movements == "1 3"):
        uno_tres(posicion[0][1], posicion[2][1], desplazamiento, tiempo)

        # actualizar posicion e item
        ans_pos = posicion[0]
        posicion[0] = posicion[2]
        posicion[2] = ans_pos
    time.sleep(tiempo_espera)
    #print(posicion[0][0], posicion[1][0], posicion[2][0])
    return posicion

    

# ===== GENERADORES ===== #

def generar_cartas_visibles():
   
    ancho_carta = q.width()
    altura_carta = q.height()
    canva = Canvas(width=ancho_carta*3 + 70, height=altura_carta + 20)
    canva.pack()
    longitud_carta = (ancho_carta)/2.0
    y = (altura_carta)/2.0
    cards = [["Q", q], ["K", k],["J", j]]
    random.shuffle(cards)
    canva.create_image(longitud_carta + 30, y, image=cards[0][1])
    canva.create_image(3*longitud_carta + 30, y, image=cards[1][1])
    canva.create_image(5*longitud_carta + 30, y, image=cards[2][1])
    root.after(3000, lambda: root.destroy())
    return [[cards[0][0]], [cards[1][0]], [cards[2][0]]]

def generar_cartas_escondidas(posicion):
    global canva
    global longitud_carta
    ancho_carta = carta_escondida.width()
    altura_carta = carta_escondida.height()
    canva = Canvas(width=ancho_carta*3 + 70, height=altura_carta + 20)
    canva.pack()
    longitud_carta = (ancho_carta)/2.0
    y = (altura_carta)/2.0
    item1 = canva.create_image(longitud_carta + 30, y, image=carta_escondida)
    item2 = canva.create_image(3*longitud_carta + 30, y, image=carta_escondida)
    item3 = canva.create_image(5*longitud_carta + 30, y, image=carta_escondida)
    posicion[0].append(item1)
    posicion[1].append(item2)
    posicion[2].append(item3)
    return posicion

# ===== MOVER ===== #

def mover_cartas(posicion, movimientos, desplazamiento, tiempo, carta, tiempo_espera):
    global resultado
    for mov in movimientos:
        posicion = mover(mov, posicion, desplazamiento, tiempo, tiempo_espera)
    root.after(1000, lambda: root.destroy())
    if(posicion[0][0] == carta):
        resultado = "I"
    elif(posicion[1][0] == carta):
        resultado = "M"
    else:
        resultado = "D"



# ============================================================== EJECUCION PRINCIPAL ==========================================================






print(f"\nAdivina donde está la carta ♥\n")
print(f"Hola 👋, bienvenido a nuestro juego... olvidé tu nombre, ¿podrías recordarlmelo?")
player= input("Ingrese el nombre del Jugador: ")
player=player.capitalize()
print(f'\nHola {player}, ahora si te doy la bienvenida formal a "Adivina dónde esta la carta" \nElige una de las siguientes opciones: \n')

while 6>5:
    option = input("Seleccione: [ J ] Jugar, [ T ] Tabla de Posiciones, [ I ] Instrucciones, [ S ] Salir: ")
    if(option == "S"):
        break
    elif option =="J":
        # ============================================= Jugar ============================================= #
        nivel=1
        puntos_finales = 0
        while 5<6:
            carticas = ['Q', 'K', 'P']
            carta_interes=mostrar_cartas(carticas) 
            if(carta_interes == 'Q'):
                print('La carta que debes seguir es la reina de corazones:')
            elif(carta_interes == 'J'):
                print("La carta que debes seguir es el jack de corazones:")
            else:
                print("La carta que debes seguir es el rey de corazones:")
            time.sleep(1)
            
    
            root = Tk() 
    
            q = PhotoImage(file="./resources/images/q.png")
            k = PhotoImage(file="./resources/images/k.png")
            j = PhotoImage(file="./resources/images/j.png") 
    
            mostrar_carta(carta_interes)
            root.mainloop() 

            print(f"¡{player} mantén los ojos abiertos mientras las cartas se mueven!")
            input("Presiona ENTER cuando estés listo(a):")

            desplazamiento = 0
            tiempo = 0
            tiempo_espera = 0
            niveles(nivel)

            root = Tk()

            q = PhotoImage(file="./resources/images/q.png")
            k = PhotoImage(file="./resources/images/k.png")
            j = PhotoImage(file="./resources/images/j.png")

            posicion = generar_cartas_visibles()

            root.mainloop()

            root = Tk()

            carta_escondida = PhotoImage(file="./resources/images/card.png")

            canva = ""
            longitud_carta = 0

            posicion = generar_cartas_escondidas(posicion)

            resultado = ""

            root.after(1000, lambda: mover_cartas(posicion,cambios(nivel), desplazamiento, tiempo, carta_interes, tiempo_espera))

            root.mainloop()

            if(carta_interes == 'Q'):
                print("¿En cuál de las cartas está la reina de corazones?")
            elif(carta_interes == 'J'):
                print("¿En cuál de las cartas está el jack de corazones?")
            else:
                print("¿En cuál de las cartas está el rey de corazones?")
            carta_seleccionada=str(input("Inserta [ D ] para la derecha, [ M ] para el medio ó [ I ] para la izquierda: "))
            if resultado==carta_seleccionada:
                nivel=nivel+1
                niveles(nivel)
                cambios(nivel)
                puntos_finales += 5
                print("\n ¡Ganaste 5 puntos, pasas al siguiente nivel! \n")
            else:
                root = Tk()

                game_over = PhotoImage(file="./resources/images/game_over.png")

                mostrar_game_over()

                root.mainloop()
                break
    elif option == "I":
        # ============================================= Instrucciones ============================================= #
        print(f"\nLas instrucciones del juego son simples:\n\n1. Sale la carta que debes buscar.")
        print(f"2. Se te muestran tres cartas, una de ellas es la que se te indico en el paso (1), rapidamente debes memorizar sus pocisiones.\n3. Se van a voltear e intercambiarse entre ellas.\n(Como eres un principiante se comenzaran a realizar los intercambios lentamente);\n4. Finalizados los intercambios debes escoger una de las cartas;\n5. Si aciertas con la carta indicada, ganas y avanzas al siguiente nivel.\n(Los niveles aumentan de dificultad cada vez que los superas, cada nivel superado son 5 puntos)\n\n¡Mucha Suerte!")
    elif option == "T":
        # ============================================= Tabla de Posiciones ============================================= #
        print(f"No disponible :/, estamos trabajando en ello")  

    

print("\n====== Fin del Programa =========")

    

