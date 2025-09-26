import face_recognition

image = face_recognition.load_image_file("image-test.png")
face_locations = face_recognition.face_locations(image)
print(f"Encontrei {len(face_locations)} rosto(s).")
