#bici.py
#Este módulo permite detectar y contar bicicletas en una imagen utilizando el modelo YOLOv8n


from ultralytics import YOLO

# Cargar el modelo YOLOv8 preentrenado con el dataset COCO
modelo = YOLO("yolov8n.pt")  # Asegurarse de tener este archivo en la misma carpeta o ruta válida


#Detecta bicicletas en una imagen utilizando detección de objetos
def contar_bicicletas(imagen):
    # Realiza la predicción con el modelo YOLOv8 para detectar objetos en la imagen
    # El umbral de confianza se establece en 0.3 para filtrar detecciones con baja certeza
    resultados = modelo.predict(source=imagen, conf=0.3)[0]
    
    # La clase 1 en el dataset COCO de YOLO corresponde a 'bicycle'
    # Se cuenta cuántos objetos detectados corresponden a bicicletas (clase 1)
    return sum(int(c) == 1 for c in resultados.boxes.cls)
