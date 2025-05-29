#auto.py
#Este módulo se encarga de detectar y contar la cantidad de automóviles ('car') en una imagen utilizando el modelo YOLOv8


from ultralytics import YOLO

# Cargamos el modelo preentrenado YOLOv8n
modelo = YOLO("yolov8n.pt")  # Asegurarse de tener este archivo en la misma carpeta o ruta válida

#Detecta objetos en la imagen y cuenta cuántos son automóviles.
def contar_autos(imagen):
    
    # Ejecuta la predicción con el modelo YOLOv8 para detectar los objetos en la imagen
    # La confianza mínima se establece en 0.3 para filtrar predicciones poco confiables
    resultados = modelo.predict(source=imagen, conf=0.3)[0]
    
    # La clase 2 en el dataset COCO de YOLO corresponde a 'car'
    # Se cuenta cuántos objetos detectados corresponden a autos (clase 2)
    return sum(int(c) == 2 for c in resultados.boxes.cls)
