import cv2
import numpy as np
from collections import Counter

def get_more_repetitive_hierarchy(contours,hierarchy):
    jerarquias = []
    for i, contour in enumerate(contours):
        jerarquias.append(hierarchy[0][i][3])
    report = Counter(jerarquias)
    # Encuentra el número que más se repite y cuántas veces
    number, repetitions = report.most_common(1)[0]
    return number,repetitions

def image_process(image):
    # Convertir el fotograma a escala de grises
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Aplicar un filtro Gaussiano para reducir el ruido
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # Detectar bordes con Canny
    edges = cv2.Canny(blurred, threshold1=100, threshold2=200)
    kernel = np.ones((5, 5), np.uint8)
    #Realizar una dilatación a la zona blanca (bordes)
    edges = cv2.dilate(edges, kernel, iterations=1)
    # Encontrar los contornos en la imagen con información de jerarquía
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    hierarchy_number, repetitions=get_more_repetitive_hierarchy(contours, hierarchy)
    print("jerarquia mas presente", hierarchy_number)
    # Filtrar los contornos para obtener los cuadrados internos
    inner_squares = []
    counter = 0
    for i, contour in enumerate(contours):
        if hierarchy[0][i][3] == hierarchy_number and cv2.contourArea(contour) > 1000:
            counter += 1
            inner_squares.append(contour)
            x, y, w, h = cv2.boundingRect(contour)
            square = frame[y+10:y + h-10, x+10:x + w-10]
            cv2.imwrite(f'recortes/inner_square_{counter}.jpg', square)
    print("contador ", counter)
    # Dibujar los contornos en el fotograma original (en color)
    cv2.drawContours(image, inner_squares, -1, (0, 255, 0), 3)  # Dibuja los contornos internos en verde
    return image,edges

def analize_board(cap):
    while True:
        # Capturar un fotograma de la cámara
        ret, frame = cap.read()
        frame,edges=image_process(frame)
        cv2.imshow('edges', edges)
        cv2.imshow('Image with Inner Contours', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # Liberar la captura de video y cerrar todas las ventanas
    cap.release()
    cv2.destroyAllWindows()
