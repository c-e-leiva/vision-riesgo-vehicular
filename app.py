#app.py

# Aplicación para detección y análisis de riesgo en vehículos según la cantidad de ocupantes.

# Materia: Procesamiento de Imágenes - Parcial 1
# Alumno: Carlos Ezequiel Leiva
# Docente: Lucas De Rito


#Se utiliza YOLOv8 para detectar autos, motos, bicicletas y personas. Se evalúa el nivel de riesgo (bajo, medio o alto) en función del tipo de vehículo y la cantidad de personas detectadas.

import streamlit as st
import cv2
import os
import numpy as np
from PIL import Image
from logica import evaluar_riesgo
from ultralytics import YOLO

# CARGA DE MODELOS
# Carga del modelo de detección de objetos (vehículos)
# El modelo 'modelo_objetos' detecta vehículos como autos, motos, bicicletas
modelo_objetos = YOLO("yolov8n.pt")

# Carga del modelo de estimación de pose para detectar personas a través de keypoints
# El modelo 'modelo_pose' identifica la postura de las personas
modelo_pose = YOLO("yolov8n-pose.pt")

# CONFIGURACIÓN DE STREAMLIT

# Configuración de la página de Streamlit en modo 'wide'
st.set_page_config(layout="wide")

# Título principal de la app
st.title("🚗 Detección de Riesgo Vehicular - Según N° de Ocupantes")

# Lista de imágenes precargadas ubicadas en la carpeta IMG/
# Se cargan las imágenes con nombres '1.jpg', '2.jpg', ..., '8.jpg'
imagenes_precargadas = [f"{i}.jpg" for i in range(1, 9)]

# División de la pantalla en dos columnas (para mostrar el selector de imagen y el resultado de riesgo)
top_col1, top_col2 = st.columns([1, 2])

# SELECCIÓN DE IMAGEN
with top_col1:
    # Se crea un selector para que el usuario elija una imagen de las precargadas
    imagen_seleccionada = st.selectbox("Selecciona una imagen", imagenes_precargadas)

# PROCESAMIENTO DE IMAGEN
if imagen_seleccionada:
    # Obtener la ruta de la imagen seleccionada
    ruta_imagen = os.path.join("IMG", imagen_seleccionada)

    if not os.path.exists(ruta_imagen):
        # Si la imagen no se encuentra en la ruta, mostrar un error
        st.error("No se encuentra la imagen. Verifica la ruta.")
    else:
        # Leer la imagen con OpenCV y convertirla a formato RGB
        imagen = cv2.imread(ruta_imagen)
        imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)

        # DETECCIÓN DE VEHÍCULOS 

        # Modelo de detección de objetos para predecir vehículos en la imagen
        resultado_objetos = modelo_objetos.predict(source=imagen_rgb, conf=0.3)[0]
        clases = resultado_objetos.names  # Clases de objetos detectados (autos, motos, etc.)
        clases_detectadas = [clases[int(c)] for c in resultado_objetos.boxes.cls]

        # Contar la cantidad de autos, motos y bicicletas detectados
        autos = clases_detectadas.count("car")
        motos = clases_detectadas.count("motorcycle")
        bicicletas = clases_detectadas.count("bicycle")

        # Mostrar el resumen de vehículos detectados
        st.write(f"Vehículos detectados: 🚗 {autos} autos | 🏍️ {motos} motos | 🚲 {bicicletas} bicicletas")

        # DETECCIÓN DE PERSONAS (POSE ESTIMATION)
        # Modelo de pose para detectar personas y sus keypoints
        resultado_pose = modelo_pose.predict(source=imagen_rgb, conf=0.3)[0]
        personas_detectadas = 0

        # Se considera una persona válida si tiene al menos 5 keypoints visibles
        if resultado_pose.keypoints is not None and resultado_pose.keypoints.shape[0] > 0:
            for kpts in resultado_pose.keypoints.data:
                visibles = kpts[:, 2] > 0.5  # Verifica la visibilidad de los keypoints
                if visibles.sum() >= 5:
                    personas_detectadas += 1

        # DIBUJO DE RESULTADOS EN LA IMAGEN 

        # Combinamos los resultados de pose en la imagen original
        imagen_combinada = resultado_pose.plot().copy()

        # Dibujo de los cuadros de los vehículos detectados en la imagen combinada
        for box, cls in zip(resultado_objetos.boxes.xyxy, resultado_objetos.boxes.cls):
            x1, y1, x2, y2 = map(int, box)
            clase = clases[int(cls)]

            if clase in ["car", "motorcycle", "bicycle"]:
                # Colores personalizados para cada tipo de vehículo
                color = (
                    (0, 255, 255) if clase == "car" else           # Celeste para autos
                    (255, 255, 0) if clase == "motorcycle" else    # Amarillo para motos
                    (138, 43, 226)                                 # Violeta para bicis
                )
                etiqueta = "Auto" if clase == "car" else "Moto" if clase == "motorcycle" else "Bici"
                cv2.rectangle(imagen_combinada, (x1, y1), (x2, y2), color, 2)
                cv2.putText(imagen_combinada, etiqueta, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        #EVALUACIÓN DEL RIESGO
        # Evaluación del nivel de riesgo basado en el tipo de vehículos y la cantidad de personas detectadas
        mensaje_riesgo = evaluar_riesgo(autos, motos, bicicletas, personas_detectadas)

        # Color del mensaje de riesgo (rojo para alto, naranja para medio, verde para bajo)
        if "ALTO" in mensaje_riesgo.upper():
            color_riesgo = "red"
        elif "MEDIO" in mensaje_riesgo.upper():
            color_riesgo = "orange"
        else:
            color_riesgo = "green"

        #VISUALIZACIÓN DE RESULTADOS
        # mostrar la imagen original y la imagen procesada (con resultados de detección)
        col1, col2 = st.columns(2)
        with col1:
            st.image(imagen_rgb, caption="🖼️ Imagen Original", width=500)
        with col2:
            st.image(imagen_combinada, caption="✅ Imagen Procesada (Personas + Vehículos)", width=500)

        # Mostrar el mensaje de riesgo al lado del selector de imágenes
        with top_col2:
            st.markdown(
                f"<h2 style='color:{color_riesgo}; text-align:center'>{mensaje_riesgo}</h2>",
                unsafe_allow_html=True
            )