#logica.py
#Módulo de lógica de evaluación de riesgo en función del tipo de vehículo detectado (auto, moto o bicicleta) y la cantidad de personas identificadas en la imagen.


# Evalúa el nivel de riesgo de segun el tipo de vehículo y la cantidad de personas detectadas.
# autos, motos, bicicletas: cantidad detectada por tipo.
# personas: total de personas en la imagen.
# Retorna un mensaje con el nivel de riesgo (bajo, moderado o alto) y una breve explicación.
def evaluar_riesgo(autos, motos, bicicletas, personas):
    if autos > 0:
        # Evaluación para autos:
        # Si hay autos, el riesgo depende de la cantidad de personas dentro.
        # Se considera seguro hasta 5 personas en el auto.
        if personas <= 4:
            return "🟢 Riesgo bajo (Vehículo automóvil con hasta 5 ocupantes)"
        else:
            # Si hay más de 5 personas, se considera alto riesgo.
            return "🔴 Riesgo alto (Vehículo automóvil con más de 5 ocupantes)"
    
    elif motos > 0:
        # Evaluación para motos:
        # Con una persona se considera bajo riesgo, con dos es moderado, y más de dos es alto riesgo.
        if personas == 1:
            return "🟢 Riesgo bajo (Moto con 1 ocupante)"
        elif personas == 2:
            return "🟠 Riesgo moderado (Moto con 2 ocupantes)"
        else:
            # Más de dos ocupantes en una moto representa un alto riesgo.
            return "🔴 Riesgo alto (Moto con 3 o más ocupantes)"
    
    elif bicicletas > 0:
        # Evaluación para bicicletas:
        # Si hay solo una persona en la bicicleta, el riesgo es bajo,
        # pero si hay más de un ocupante, el riesgo es alto.
        if personas == 1:
            return "🟢 Riesgo bajo (Bicicleta con 1 ocupante)"
        else:
            # Dos o más ocupantes en una bicicleta representa un alto riesgo.
            return "🔴 Riesgo alto (Bicicleta con 2 o más ocupantes)"
    
    else:
        # Si no hay vehículos detectados, no se evalúa riesgo.
        return "⚪ Sin vehículos detectados"