import numpy as numpy  # Utilizamos numpy para facilitar la creación de la matriz tablero
import random  # Para generar valores random

# --------------------------------------------LÓGICA NECESARIA-----------------------------------------------------------#
# Crear el tablero (tamaño ajustable)
tamano = 5
# esto genera una matriz de tamaño tamano x tamano llena de ceros, donde cada elemento es de tipo entero.
tablero = numpy.zeros((tamano, tamano), dtype=int)

# Calculamos la distancia absoluta "abs()" (distancia directa entre las dos posiciones)
def distancia(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

while True:

    # Definimos posiciones iniciales
    """estas coordenadas representan el lugar x,y de forma aleatoria en la que se va a almacenar la posicion inicial del personaje
    a lo largo del tamaño del tablero, desde el numero 0, hasta el último numero del tamaño del tablero (x*y = posicion)"""

    posicion_raton = (random.randint(0, tamano - 1), random.randint(0, tamano - 1))
    posicion_gato = (random.randint(0, tamano - 1), random.randint(0, tamano - 1))

    # Verificamos la distancia inicial mínima de 3 cuadros para mejor función del programa
    # como minimo 3 cuadrillas alejados alrededor de cada uno o mayor
    if distancia(posicion_raton, posicion_gato) >= 3:
        break #Si la distancia es mayor o igual a 3, se rompe el bucle (break), lo que significa que se han encontrado posiciones válidas para el ratón y el gato.

# Representación de personajes en el tablero
tablero[posicion_gato] = 1  # 1 representa el gato
tablero[posicion_raton] = 2  # 2 representa el ratón

def movimientos_validos(posicion):
    y, x = posicion  # Posición del elemento (se desempaqueta la tupa que está compuesta por 2 elementos y son los argumentos que recibe la función)
    movimientos = []
    if y > 0:  # Si hay espacio arriba
        movimientos.append((y - 1, x))  # Mover arriba ^
    if y < tamano - 1:  # Si hay espacio abajo
        movimientos.append((y + 1, x))  # Mover abajo v
    if x > 0:  # Si hay espacio a la izquierda
        movimientos.append((y, x - 1))  # Mover izquierda <
    if x < tamano - 1:  # Si hay espacio a la derecha
        movimientos.append((y, x + 1))  # Mover derecha >
    return movimientos  # Retornamos los movimientos que el personaje PUEDE realizar

def minimax(posicion_gato, posicion_raton, depth, maximizando, alpha=float('-inf'), beta=float('inf')):
    # Si la profundidad del programa llega a cero o si el gato encuentra al ratón
    if depth == 0: # si la profundidad llega a 0, significa que se ha alcanzado el límite de la búsqueda y no se evaluarán más movimientos futuros
        return distancia(posicion_gato, posicion_raton), None #Si la profundidad es 0, se retorna la distancia actual entre el gato y el ratón, junto con None para indicar que no se realizarán más movimientos.
    elif posicion_gato == posicion_raton:
        return distancia(posicion_gato, posicion_raton), None  #Si el gato está en la misma posición que el ratón, se retorna la distancia (que en este caso será 0 porque están en la misma posición) junto con None para indicar que el juego ha terminado.

    # Cuando el algoritmo esté en MAX (ratón)
    if maximizando:
        # Iniciamos con la menor evaluación posible para buscar un valor mayor y maximizar
        max_eval = float('-inf')
        mejor_movimiento = None  # Declaramos la variable que adoptará el mejor movimiento

        # Evaluamos cada posibilidad con cada movimiento posible (ratón)
        for mov in movimientos_validos(posicion_raton):
            # Ignoramos mejor_movimiento para priorizar eval utilizando ( _ )
            # Valor de evaluación del posible movimiento actual (ratón) contra el mejor próximo movimiento del gato
            eval, _ = minimax(posicion_gato, mov, depth - 1, False, alpha, beta) # se llama recursivamente a la función minimax para evaluar el valor de una posición después de que el ratón hace un movimiento posible (mov).
            # Si la evaluación actual es mayor (mejor) a nuestra max evaluación anterior la reemplazamos
            if eval > max_eval:
                max_eval = eval
                mejor_movimiento = mov
            # Guarda el mayor valor entre sí y eval
            alpha = max(alpha, eval)
            # Si el ratón ya tiene una mejor jugada garantizada anterior podamos las evaluaciones (Optimización)
            if beta <= alpha:
                break
        return max_eval, mejor_movimiento  # Retornamos mejor jugada para el ratón

    else:
        # Iniciamos con la mayor evaluación posible para buscar un valor mayor y maximizar
        min_eval = float('inf')
        mejor_movimiento = None  # Declaramos de nuevo

        # Evaluamos cada posibilidad con cada movimiento posible (gato)
        for mov in movimientos_validos(posicion_gato):
            # Ignoramos mejor_movimiento para priorizar eval
            # Valor de evaluación del posible movimiento actual (ratón) contra el mejor próximo movimiento del gato
            eval, _ = minimax(mov, posicion_raton, depth - 1, True, alpha, beta)
            if eval < min_eval:
                min_eval = eval
                mejor_movimiento = mov
            # Mejor valor para el gato
            # Guarda el menor valor entre sí y eval
            beta = min(beta, eval)
            # " " " " Se podan las evaluaciones (Optimización)
            if beta <= alpha:
                break
        return min_eval, mejor_movimiento  # Retornamos mejor jugada para el gato

# --------------------------------------------CUERPO PRINCIPAL-----------------------------------------------------------#
# Función para dibujar el tablero
def dibujar_tablero():

    print("\n*********tablero actual*********\n")

    for row in range(tamano):
        for col in range(tamano):
            print(tablero[row][col], end=' ')
        print()

# Función principal para ejecutar el juego hasta que la profundidad llegue a 0
def ejecutar_juego(posicion_gato, posicion_raton, depth):

    print('''El juego del gato y del ratón:
- El ratón (2) escapa y el gato(1) persigue''')

    turno_raton = True  # Empieza el ratón
    juego_terminado = False  # Estado del juego

    while not juego_terminado:  # Mientras juego_terminado != True

        # Mientras la profundidad del programa no sea 0 y el gato no atrapó al ratón
        if depth > 0 and posicion_gato != posicion_raton:

            # Dependiendo del turno llamamos a la función minimax con True o False para especificar el gato o el ratón
            if turno_raton:
                # Mostramos el tablero actual
                dibujar_tablero()
                print("Turno del ratón. Movimientos válidos: arriba (w), abajo (s), izquierda (a), derecha (d)")
                movimiento_valido = False
                while not movimiento_valido:
                    direccion = input("Elija dirección de movimiento para el ratón: ").lower()
                    if direccion == 'w':
                        nuevo_movimiento = (posicion_raton[0] - 1, posicion_raton[1])
                    elif direccion == 's':
                        nuevo_movimiento = (posicion_raton[0] + 1, posicion_raton[1])
                    elif direccion == 'a':
                        nuevo_movimiento = (posicion_raton[0], posicion_raton[1] - 1)
                    elif direccion == 'd':
                        nuevo_movimiento = (posicion_raton[0], posicion_raton[1] + 1)
                    else:
                        print("Dirección no válida. Intente de nuevo.")
                        continue

                    if nuevo_movimiento in movimientos_validos(posicion_raton):
                        movimiento_valido = True
                        posicion_raton = nuevo_movimiento
                        tablero.fill(0)
                        tablero[posicion_gato] = 1
                        tablero[posicion_raton] = 2
                    else:
                        print("Movimiento no válido. Intente de nuevo.")
                # Refrescamos el tablero
                dibujar_tablero()

            else:
                _, mejor_mov = minimax(posicion_gato, posicion_raton, depth, False)
                if mejor_mov:
                    posicion_gato = mejor_mov

            # Alternamos el turno
            turno_raton = not turno_raton
            depth = depth - 1

        # Si es que depth == 0 o el gato atrapó al ratón
        else:
            juego_terminado = True  # Avisamos que el juego se terminó
            # Determinamos la causa de la finalización
            if depth == 0:
                print("Se han acabado los turnos; ¡El ratón gana!")
            elif posicion_gato == posicion_raton:
                print("El gato atrapó al ratón; ¡El gato gana!")

# Ejecutamos el juego y definimos su profundidad (Profundidad máxima posible: 23)
ejecutar_juego(posicion_gato, posicion_raton, 15)
