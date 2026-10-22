import matplotlib.pyplot as plt
import streamlit as st

import modelo  # nuestro backend

st.set_page_config(page_title="El que aprende a intentos", layout="wide")
st.title("🧭 El que aprende a intentos")
st.caption("Equipo 3 · Aprendizaje por refuerzo · Q-Learning en un laberinto")
def dibujar_laberinto(Q=None, camino=None):
    lab = modelo.LABERINTO
    fig, ax = plt.subplots(figsize=(6, 6))

    # Pintar cada casilla
    for f in range(8):
        for c in range(8):
            celda = lab[f][c]
            color = {"#": "#2b2b2b", "S": "#7ccf7c", "M": "#f5c542"}.get(celda, "white")
            ax.add_patch(plt.Rectangle((c, f), 1, 1, facecolor=color, edgecolor="#cccccc"))
            if celda in "SM":
                ax.text(c + 0.5, f + 0.5, celda, ha="center", va="center", fontsize=16, weight="bold")

    # Camino del agente en rojo
    if camino:
        ax.plot([c + 0.5 for _, c in camino], [f + 0.5 for f, _ in camino],
                color="red", linewidth=4, alpha=0.35)

    # Una flecha por casilla (la politica)
    if Q is not None:
        for (f, c), accion in modelo.politica(Q).items():
            if lab[f][c] != "S":
                ax.text(c + 0.5, f + 0.5, modelo.FLECHAS[accion],
                        ha="center", va="center", fontsize=18, color="#1f4e9c")

    ax.set_xlim(0, 8)
    ax.set_ylim(8, 0)  # invertido para que la fila 0 quede arriba
    ax.set_aspect("equal")
    ax.axis("off")
    return fig


def grafica_exito(curvas):
    fig, ax = plt.subplots(figsize=(7, 4))
    for nombre, tasa in curvas.items():
        ax.plot(range(1, len(tasa) + 1), tasa, label=nombre, linewidth=2)
    ax.set_xlabel("Episodio")
    ax.set_ylabel("% de exito (ultimos 20)")
    ax.set_ylim(-5, 105)
    ax.grid(alpha=0.3)
    ax.legend()
    return fig

st.sidebar.header("Parámetros")
episodios = st.sidebar.slider("Episodios (intentos)", 10, 1000, 300, step=10)
alpha = st.sidebar.slider("alpha · tasa de aprendizaje", 0.01, 1.0, 0.1)
gamma = st.sidebar.slider("gamma · importancia del futuro", 0.1, 0.99, 0.9)
epsilon = st.sidebar.slider("epsilon · exploración", 0.0, 1.0, 0.1)

if st.sidebar.button("🚀 Entrenar", type="primary"):
    st.session_state["Q"], st.session_state["exitos"] = modelo.entrenar(episodios, alpha, gamma, epsilon)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Laberinto y política aprendida")
    if "Q" not in st.session_state:
        st.pyplot(dibujar_laberinto())
        st.info("Ajusta los parámetros y aprieta **Entrenar**.")
    else:
        camino, llego = modelo.recorrer(st.session_state["Q"])
        st.pyplot(dibujar_laberinto(st.session_state["Q"], camino))
        if llego:
            st.success(f"✅ El agente llega a la meta en {len(camino) - 1} pasos sin chocar.")
        else:
            st.error("❌ Todavía no sabe llegar. Prueba con más episodios.")

with col2:
    st.subheader("¿Cómo mejora con los episodios?")
    if "exitos" in st.session_state:
        exitos = st.session_state["exitos"]
        st.metric("Veces que llegó a la meta", f"{sum(exitos)} de {len(exitos)}")
        st.pyplot(grafica_exito({f"epsilon = {epsilon}": modelo.tasa_exito(exitos)}))

 st.divider()
st.subheader("🔬 Experimento: ¿qué pasa si cambio epsilon?")

if st.button("Correr experimento"):
    curvas = {}
    for eps in [0.0, 0.1, 0.3, 0.6]:
        Q, exitos = modelo.entrenar(episodios, alpha, gamma, eps)
        curvas[f"epsilon = {eps}"] = modelo.tasa_exito(exitos)
        st.write(f"epsilon {eps}: llegó {sum(exitos)} de {len(exitos)} veces")
    st.pyplot(grafica_exito(curvas))
    st.caption("Epsilon alto = explora mucho al azar, tarda más en aprender. "
               "Epsilon bajo = aprovecha lo que sabe y sube más rápido.")