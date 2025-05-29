#moto.py
#Este módulo permite detectar y contar motocicletas en una imagen usando YOLOv8n


from ultralytics import YOLO

# Cargar el modelo YOLOv8 preentrenado con el dataset COCO
modelo = YOLO("yolov8n.pt")  # Asegurarse de tener este archivo en la misma carpeta o ruta válida


#Detecta motocicletas en la imagen proporcionada
def contar_motos(imagen):
    # Ejecuta la predicción con el modelo YOLOv8 para detectar objetos en la imagen
    # Establecemos un umbral de confianza de 0.3 para filtrar predicciones con baja certeza
    resultados = modelo.predict(source=imagen, conf=0.3)[0]
    
    # La clase 3 en el dataset COCO de YOLO corresponde a 'motorcycle'
    # Contamos cuántos objetos detectados son motocicletas (clase 3)
    return sum(int(c) == 3 for c in resultados.boxes.cls)
