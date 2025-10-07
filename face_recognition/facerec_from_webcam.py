import face_recognition_models
import face_recognition

know_image = face_recognition.load_image_file("test.png")
unknown_image = face_recognition.load_image_file("unknown.jpg")

encoding = face_recognition.face_encodings(know_image)[0]
unknown_image = face_recognition.face_encodings(unknown_image)[0]

results = face_recognition.compare_faces([encoding], unknown_image)

print(encoding)
print(unknown_image)


print(results)
print("ta funcionando")
