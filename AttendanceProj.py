import cv2
import numpy as np
import face_recognition
import os

path= 'imagesAttendance'
images=[]
classNames= []
myList= os.listdir(path)
print(myList)
for cl in myList:
    curImg=cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)

def findEncodings(images):
    encodeList=[]
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append((encode))
    return  encodeList

encodeListKnown=findEncodings(images)
print('Encoding Complete')

cap=cv2.VideoCapture(0)

while True:
    success, img= cap.read()
    imgS=cv2.resize(img,(0,0),None,0.25,0.25)
    imgS= cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame= face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)

    for encodeFace,faceLoc in zip(encodeCurFrame,facesCurFrame):
        matches=face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDis=face_recognition.face_distance((encodeListKnown,encodeFace))

        matchIndex=np.argmin(faceDis)

        if matches[matchIndex]:
            name= classNames[matchIndex].upper()
            print(name)





#faceLoc = face_recognition.face_locations(imgElon)[0]
#encodeElon = face_recognition.face_encodings(imgElon)[0]
#cv2.rectangle(imgElon,(faceLoc[3],faceLoc[0]),(faceLoc[1],faceLoc[2]),(255,0,255),2)


#faceLocTest=face_recognition.face_locations(imgTest)[0]
#encodeTest=face_recognition.face_encodings(imgTest)[0]
#cv2.rectangle(imgTest,(faceLocTest[3],faceLocTest[0]),(faceLocTest[1],faceLocTest[2]),(255,0,255),2)

#results=face_recognition.compare_faces([encodeElon],encodeTest)
#faceDis=face_recognition.face_distance([encodeElon],encodeTest)
#cv2.putText(imgTest,f'{results}{round(faceDis[0],2)}',(50,50),cv2.FONT_HERSHEY_COMPLEX_SMALL,0.75,(0,0,255),2)
