from ast import Break
from collections import Counter

from django.contrib import messages
from django.shortcuts import render ,redirect
from django.http import HttpResponse 
from django.core.files.storage import FileSystemStorage
import os

import pandas as pd 

import time



import face_recognition
import cv2
import numpy as np

def index (request):
    return render (request,"index.html")


def home (request):
    return render (request,"home.html")

def login (request):
    return render (request,"login.html")


def index2 (request):
    
    context = {}
    global attribute
    if request.method == 'POST':

        uploaded_file = request.FILES['document']
        attribute = request.POST.get('attributeid')

        print(uploaded_file)

        #check if this file ends with csv
        if uploaded_file.name.endswith('.csv'):
            savefile = FileSystemStorage()

            name = savefile.save(uploaded_file.name, uploaded_file) #gets the name of the file
            print(name)
            
            #we need to save the file somewhere in the project, MEDIA
            d = os.getcwd() # how we get the current dorectory
            file_directory = d+'\media\\'+name #saving the file in the media directory
            print(file_directory)
            readfile(file_directory)
            request.session['attribute'] = attribute
            if attribute not in data.axes[1]:
                messages.warning(request, 'Please write the column name correctly')
            else:
                print(attribute)
                return redirect(results)
        else:
            messages.warning(request, 'File was not uploaded. Please use .csv file extension!')
    return  render(request, 'index2.html', context)








    return render (request,"index2.html", context)


# Create your views here.
def readfile(filename):

    global rows,columns,data,my_file,missing_values
     #read the missing data - checking if there is a null
    missingvalue = ['?', '0', '--','unknown']

    my_file = pd.read_csv(filename, sep='[:;,|_]',na_values=missingvalue, engine='python')

    data = pd.DataFrame(data=my_file, index=None)
    print(data)

    rows = len(data.axes[0])
    columns = len(data.axes[1])


    null_data = data[data.isnull().any(axis=1)] # find where is the missing data #na null
    missing_values = len(null_data)



def results (request):

    message = 'I found ' + str(rows)+ ' rows and ' + str(columns) + ' columns. Missing data: ' + str(missing_values)
    messages.info(request, message)

    dashboard = [] # ['A11','A11',A'122',]
    for x in data[attribute]:
        dashboard.append(x)

    my_dashboard = dict(Counter(dashboard)) #{'A121': 282, 'A122': 232, 'A124': 154, 'A123': 332}

    print(data.axes[0])

    keys = my_dashboard.keys() # {'A121', 'A122', 'A124', 'A123'}
    values = my_dashboard.values()

    listkeys = []
    listvalues = []

    for x in keys:
        listkeys.append(x)

    for y in values:
        listvalues.append(y)

    print(listkeys)
    print(listvalues)

    context = {
        'listkeys': listkeys,
        'listvalues': listvalues,
    }

    return render(request, 'results.html', context)




def face_recog(request):
    

    video_capture = cv2.VideoCapture(0)
    
    login_image = face_recognition.load_image_file(r"D:\--Etudes--\4DS3\Part2\PI\Projet 1.0\bankyDjango\loginIMG\ymb.jpg")
    login_face_encoding = face_recognition.face_encodings(login_image)[0]

    known_face_encodings = []
    # Create arrays of known face encodings and their names
    known_face_encodings = [
        login_face_encoding,

    ]
    known_face_names = [
        "Youssef el mahdi bouchouicha",
    ]


    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    message= ""

    while True:

        
        # Grab a single frame of video
        ret, frame = video_capture.read()
     
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]
        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    cv2.destroyAllWindows()
                    return render(request, 'index2.html')
                else:
                    cv2.destroyAllWindows()
                    return render(request, 'home.html')      
                       
        process_this_frame = not process_this_frame

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 3)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (0, 255, 0), 1)
           
        # Display the resulting image
        cv2.imshow('Video', frame)  
      # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
    return render(request, 'login.html')
    
    


def test(request):
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        height, width,_ = frame.shape
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    return redirect('/index')