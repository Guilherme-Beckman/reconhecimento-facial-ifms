import face_recognition
import cv2  # serve para ver os pontos

image = face_recognition.load_image_file("image-test.png")

# vai gerar uma lista de dicionarios de marks de rostos
face_landmarks_list = face_recognition.face_landmarks(image)

# o padrao do openCV é BRG
# realiza a conversão
image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

# vai percorrer cada rosto dentro da lista
for face_landmarks_list in face_landmarks_list:
    for feature, points in face_landmarks_list.items():
        for x, y in points:
            cv2.circle(image_bgr, (x, y), 2, (0, 0, 255), -1)


cv2.imwrite("test-output/image-with-landmarks.png", image_bgr)
