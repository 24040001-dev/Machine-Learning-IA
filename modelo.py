import numpy as np

#significa
# '#' = pared   '.' = libre   'S' = inicio   'M' = meta
LABERINTO = [
    "S..#....",
    ".#.#.##.",
    ".#...#..",
    ".####.#.",
    "......#.",
    "#.###.#.",
    "..#...#.",
    "#...#..M",
]



ACCIONES = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # arriba, abajo, izquierda, derecha
FLECHAS = ["↑", "↓", "←", "→"]

# Premios y castigos
PREMIO_META = 100
CASTIGO_CHOQUE = -10
PREMIO_ACERCARSE = 1      # gana 1 punto si se acerca a la meta
CASTIGO_ALEJARSE = -2     # pierde el doble si se aleja
MAX_PASOS = 40  # si no llega en 40 pasos, el intento falla

def buscar(laberinto, letra):
    for f, renglon in enumerate(laberinto):
        for c, celda in enumerate(renglon):
            if celda == letra:
                return (f, c)


def es_pared(laberinto, f, c):
    filas, cols = len(laberinto), len(laberinto[0])
    if f < 0 or f >= filas or c < 0 or c >= cols:
        return True  # salirse del mapa cuenta como pared
    return laberinto[f][c] == "#"


def distancia(a, b):
    # cuantas filas + cuantas columnas faltan para llegar
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def paso(laberinto, estado, accion):
    df, dc = ACCIONES[accion]
    nf, nc = estado[0] + df, estado[1] + dc

    if es_pared(laberinto, nf, nc):
        return estado, CASTIGO_CHOQUE, False, True   
    if laberinto[nf][nc] == "M":
        return (nf, nc), PREMIO_META, True, False   

    #gana si se acerca a la meta, pierde el doble si se aleja
    meta = buscar(laberinto, "M")
    if distancia((nf, nc), meta) < distancia(estado, meta):
        return (nf, nc), PREMIO_ACERCARSE, False, False
    return (nf, nc), CASTIGO_ALEJARSE, False, False

def elegir_accion(Q, estado, epsilon, rng):
    if rng.random() < epsilon:
        return int(rng.integers(4))           
    valores = Q[estado[0], estado[1]]
    mejores = np.flatnonzero(valores == valores.max())
    return int(rng.choice(mejores))           


def entrenar(episodios=300, alpha=0.1, gamma=0.9, epsilon=0.1, semilla=0):
    rng = np.random.default_rng(semilla)
    Q = np.zeros((8, 8, 4))                   
    inicio = buscar(LABERINTO, "S")
    exitos = []
    puntos = []                              

    for _ in range(episodios):
        estado = inicio
        llego = False
        total = 0
        for _ in range(MAX_PASOS):
            accion = elegir_accion(Q, estado, epsilon, rng)
            nuevo, r, termino, choco = paso(LABERINTO, estado, accion)
            total += r

            # FORMULA DE Q-LEARNING
            futuro = 0 if termino else Q[nuevo[0], nuevo[1]].max()
            Q[estado[0], estado[1], accion] += alpha * (r + gamma * futuro - Q[estado[0], estado[1], accion])

            estado = nuevo
            if termino:
                llego = True
                break
        exitos.append(int(llego))
        puntos.append(total)

    return Q, exitos, puntos

def tasa_exito(exitos, ventana=20):
    tasa = []
    for i in range(len(exitos)):
        ultimos = exitos[max(0, i - ventana + 1): i + 1]
        tasa.append(sum(ultimos) / len(ultimos) * 100)
    return tasa


def politica(Q):
    flechas = {}
    for f, renglon in enumerate(LABERINTO):
        for c, celda in enumerate(renglon):
            if celda in ".S":
                flechas[(f, c)] = int(np.argmax(Q[f, c]))
    return flechas


def recorrer(Q):
    estado = buscar(LABERINTO, "S")
    camino = [estado]
    for _ in range(MAX_PASOS):
        accion = int(np.argmax(Q[estado[0], estado[1]]))
        estado, _, termino, choco = paso(LABERINTO, estado, accion)
        camino.append(estado)
        if termino:
            return camino, True
        if choco:
            return camino, False
    return camino, False


if __name__ == "__main__":
    Q, exitos, puntos = entrenar()
    camino, llego = recorrer(Q)
    print("Llego a la meta", sum(exitos), "de", len(exitos), "veces")
    print("Puntos en el ultimo episodio:", puntos[-1])
    print("Exito ultimos 20:", tasa_exito(exitos)[-1], "%")
    print("Agente entrenado llega:", llego, "en", len(camino) - 1, "pasos")