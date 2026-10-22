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
En el código original, el agente perdía 1 punto por cada paso y solo sabía si iba bien cuando llegaba a la meta. Para que aprendiera más rápido, cambiamos los premios: ahora gana 1 punto cada vez que se acerca a la meta y, si se aleja, pierde el doble (2 puntos). Chocar se queda igual (−10 puntos) y llegar a la meta da 100 puntos.

Agregamos el castigo al doble para que el agente no hiciera trampa: si ganara y perdiera lo mismo, podría ir y regresar sin perder nada. Así, cada vuelta le cuesta puntos y le conviene ir directo a la meta.

Resultado: con los mismos parámetros, antes llegaba a la meta 241 de 300 veces y ahora llega 298 de 300. También agregamos una gráfica de los puntos que junta en cada episodio.

## Integrantes
- CAMILA ESTEFANIA ORTEGA LUNA
- AIDA SARAHI TORRES SALAZAR
- JOSE ALEJANDRO MARTINEZ GONZALEZ 