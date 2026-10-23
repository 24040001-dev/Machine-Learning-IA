import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import streamlit as st

import modelo 

st.set_page_config(page_title="El que aprende a intentos", layout="wide")
st.title("El que aprende a intentos")
st.caption("Equipo 3 · Aprendizaje por refuerzo · Q-Learning en un laberinto")


COLOR_LIBRE = "#eaf4fa"
COLOR_PARED = "#7d8c5a"
COLOR_INICIO = "#b5c98e"
COLOR_META = "#7cc4e8"
COLOR_CAMINO = "#4aa3df"
COLOR_FLECHA = "#8c9aa5"
COLOR_TEXTO = "#3e4a3d"


def dibujar_laberinto(Q=None, camino=None):
    lab = modelo.LABERINTO
    fig, ax = plt.subplots(figsize=(6, 6))
    fig.patch.set_facecolor("white")

    
    for f in range(8):
        for c in range(8):
            celda = lab[f][c]
            color = {"#": COLOR_PARED, "S": COLOR_INICIO, "M": COLOR_META}.get(celda, COLOR_LIBRE)
            ax.add_patch(FancyBboxPatch((c + 0.06, f + 0.06), 0.88, 0.88,
                                        boxstyle="round,pad=0,rounding_size=0.15",
                                        facecolor=color, edgecolor="none"))
            if celda in "SM":
                ax.text(c + 0.5, f + 0.5, celda, ha="center", va="center",
                        fontsize=15, weight="bold", color="white", zorder=4)

    
    if camino:
        ax.plot([c + 0.5 for _, c in camino], [f + 0.5 for f, _ in camino],
                color=COLOR_CAMINO, linewidth=6, alpha=0.55,
                solid_capstyle="round", solid_joinstyle="round")

    
    if Q is not None:
        for (f, c), accion in modelo.politica(Q).items():
            if lab[f][c] != "S":
                ax.text(c + 0.5, f + 0.5, modelo.FLECHAS[accion],
                        ha="center", va="center", fontsize=15, color=COLOR_FLECHA)

    ax.set_xlim(0, 8)
    ax.set_ylim(8, 0)  
    ax.set_aspect("equal")
    ax.axis("off")
    return fig


def grafica_exito(curvas):
    fig, ax = plt.subplots(figsize=(7, 4))
    colores = [COLOR_CAMINO, COLOR_PARED, "#e0b872", "#9a8fb8"]
    for i, (nombre, tasa) in enumerate(curvas.items()):
        ax.plot(range(1, len(tasa) + 1), tasa, label=nombre, linewidth=2.2,
                color=colores[i % len(colores)])
    ax.set_xlabel("Episodio", color=COLOR_TEXTO)
    ax.set_ylabel("% de exito (ultimos 20)", color=COLOR_TEXTO)
    ax.set_ylim(-5, 105)
    ax.grid(axis="y", alpha=0.25)
    for lado in ["top", "right"]:
        ax.spines[lado].set_visible(False)
    for lado in ["left", "bottom"]:
        ax.spines[lado].set_color("#c8cfc4")
    ax.tick_params(colors=COLOR_TEXTO)
    ax.legend(frameon=False)
    return fig


def grafica_puntos(puntos):
    fig, ax = plt.subplots(figsize=(7, 3))
    ax.plot(range(1, len(puntos) + 1), puntos, color=COLOR_PARED, linewidth=1.8)
    ax.axhline(0, color="#c8cfc4", linewidth=1)
    ax.set_xlabel("Episodio", color=COLOR_TEXTO)
    ax.set_ylabel("Puntos", color=COLOR_TEXTO)
    ax.grid(axis="y", alpha=0.25)
    for lado in ["top", "right"]:
        ax.spines[lado].set_visible(False)
    for lado in ["left", "bottom"]:
        ax.spines[lado].set_color("#c8cfc4")
    ax.tick_params(colors=COLOR_TEXTO)
    return fig

st.sidebar.header("Parámetros")
episodios = st.sidebar.slider("Episodios (intentos)", 10, 1000, 300, step=10)
alpha = st.sidebar.slider("alpha · tasa de aprendizaje", 0.01, 1.0, 0.1)
gamma = st.sidebar.slider("gamma · importancia del futuro", 0.1, 0.99, 0.9)
epsilon = st.sidebar.slider("epsilon · exploración", 0.0, 1.0, 0.1)

if st.sidebar.button("Entrenar", type="primary"):
    st.session_state["Q"], st.session_state["exitos"], st.session_state["puntos"] = \
        modelo.entrenar(episodios, alpha, gamma, epsilon)

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

    # Modificacion: puntos que junta en cada episodio
    if "puntos" in st.session_state:
        puntos = st.session_state["puntos"]
        st.subheader("🏅 Puntos por episodio")
        st.caption(f"Gana {modelo.PREMIO_ACERCARSE} punto si se acerca a la meta y pierde "
                   f"el doble ({modelo.CASTIGO_ALEJARSE}) si se aleja. "
                   f"Chocar: {modelo.CASTIGO_CHOQUE} · Llegar: +{modelo.PREMIO_META}")
        st.metric("Puntos en el último episodio", puntos[-1])
        st.pyplot(grafica_puntos(puntos))

st.divider()
st.subheader("🔬 Experimento: ¿qué pasa si cambio epsilon?")

if st.button("Correr experimento"):
    curvas = {}
    for eps in [0.0, 0.1, 0.3, 0.6]:
        Q, exitos, _ = modelo.entrenar(episodios, alpha, gamma, eps)
        curvas[f"epsilon = {eps}"] = modelo.tasa_exito(exitos)
        st.write(f"epsilon {eps}: llegó {sum(exitos)} de {len(exitos)} veces")
    st.pyplot(grafica_exito(curvas))
    st.caption("Epsilon alto = explora mucho al azar, tarda más en aprender. "
               "Epsilon bajo = aprovecha lo que sabe y sube más rápido.")

               