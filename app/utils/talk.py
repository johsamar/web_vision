import pyttsx3

def say_movement(mensaje):
    
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # Elige la primera voz disponible

    # Reproduce el mensaje
    engine.say(mensaje)
    engine.runAndWait()

    # Cierra el motor de texto a voz después de la reproducción
    engine.stop()
    
