# El que aprende a intentos - Q-Learning en un laberinto

Equipo 3 · Aprendizaje por refuerzo · UT Parras de la Fuente

## ¿Qué es?
Un agente aprende solo a salir de un laberinto con Q-Learning.
Recibe premios (+100 al llegar) y castigos (-10 al chocar, -1 por paso).
Se muestra la política aprendida (flechas), la tasa de éxito por episodio
y un experimento con distintos valores de epsilon.

## Archivos
- modelo.py: backend (ambiente y Q-Learning)
- app.py: frontend en Streamlit
- capturas/: imágenes del sistema funcionando

## Cómo se corre
pip install -r requirements.txt
python -m streamlit run app.py

## Modificación propia
(Expliquen aquí qué cambiaron y por qué)

## Integrantes
- Nombre 1
- Nombre 2
- Nombre 3