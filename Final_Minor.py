    #! <--------------------------------------------------GUI Requirements----------------------------------------------------->
from tkinter import *
from tkinter.messagebox import showinfo


    #! <--------------------------------------------------Model Requirements----------------------------------------------------->
import face_recognition  # type: ignore
import cv2
import numpy as np
import os
import pickle
from datetime import date, datetime, timedelta



    #! <--------------------------------------------------Database Requirements----------------------------------------------------->
import sqlite3
con=sqlite3.connect("Attendance_Database.db")
cur=con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS USER_INFO (user_id VARCHAR(20), fname  varchar (20), lname  varchar (20))")
cur.execute("CREATE TABLE IF NOT EXISTS ATTENDANCE_INFO (user_id VARCHAR(20), date DATE, time TIME)")
con.commit()


# cur.execute("SELECT * FROM ATTENDANCE_INFO")
# data = cur.fetchall()
# for i in data:
#     print(i)


# cur.execute("SELECT * FROM USER_INFO")
# data = cur.fetchall()
# for i in data:
#     print(i)
#     print(i[0])
#     print(i[1])
#     print(i[2])



    #! <--------------------------------------------------Splash Window----------------------------------------------------->

class Attendance_system:
    def fun1(self):
        root=Tk()
        root.title("Minor Project Pt-I")
        root.geometry("%dx%d+0+0"%(root.winfo_screenwidth(),root.winfo_screenheight()))
        Label(root,text="Face Recognition Based Smart Attendance System",bg="grey",fg="red",font="Arial 20 bold").pack()
        Label(root,text='\n\n').pack()
        Label(root,text="NAME: VARUN PAREEK",font="Arial 14",fg="blue").pack(pady=20)
        Label(root,text="Er: 221B434",font="Arial 14",fg="blue").pack(pady=20)
        Label(root,text='\n\n').pack()


        Label(root,text="NAME: VIVEK SAINI",font="Arial 14",fg="blue").pack(pady=20)
        Label(root,text="Er: 221B453",font="Arial 14",fg="blue").pack(pady=20)
        Label(root,text='\n\n').pack()


        Label(root,text="NAME: RITU PANT",font="Arial 14",fg="blue").pack(pady=20)
        Label(root,text="Er: 221B302",font="Arial 14",fg="blue").pack(pady=20)
        Label(root,text='\n\n').pack()



        Label(root,text="Under the Mentorship of Dr. Amit Rathi",bg="grey",fg="red",font="Arial 20 bold").pack()


        Label(root,text="PRESS ANY KEY TO EXIT",font="Arial 30 bold").pack()
        def fun2(event):
            root.destroy()
            self.options()
            
        root.bind('<Key>',fun2)
        root.mainloop()


    #! <--------------------------------------------------Main Portal----------------------------------------------------->

    def options(self):
        root1 = Tk()
        root1.title("Minor Project Pt-I")
        root1.geometry("1920x1090")
        Label(root1,text="Face Recognition Based Smart Attendance System",bg="grey",fg="red",font="Arial 20 bold").pack(pady=50)
        fr=Frame(root1)
        fr.pack()

        def fun3():
            root1.destroy()
            self.option1()
        Button(fr,text="Take Attendance",bg="medium orchid",fg="black",font="Arial 15 bold",command=fun3).grid(row=0,column=0)

        def fun4():
            root1.destroy()
            self.option2()
        Button(fr,text="Your Attendance",bg="medium orchid",fg="black",font="Arial 15 bold",command=fun4).grid(row=0,column=3,padx=100)

        def fun5():
            # root1.destroy()
            self.option3()
        Button(fr,text="Add a User",bg="medium orchid",fg="black",font="Arial 15 bold",command=fun5).grid(row=0,column=6)
            
        Label(fr,text="For Admin Only",fg="red",font="Arial 13 bold").grid(row=1,column=6)
        root1.mainloop()


    #! <--------------------------------------------------Taking Attendance----------------------------------------------------->

    def option1(self):
        can_record = 0
        cap = cv2.VideoCapture(0)
        cap.set(3, 640)
        cap.set(4, 480)

        facedetect = cv2.CascadeClassifier(r'D:\VS_Code\Minor_Project_1\Main_Project_files\haarcascade_frontalface_default.xml')
        imageBackground = cv2.imread(r"D:\VS_Code\Minor_Project_1\Files\Resources\background.png")

        data_path = r'D:\VS_Code\Minor_Project_1\Main_Project_files\data\data'
        encode_file_path = os.path.join(data_path, 'EncodeFile.pkl')

        # Check if the encoding file exists
        if os.path.exists(encode_file_path):
            # Load the encodings
            with open(encode_file_path, 'rb') as f:
                all_encodings = pickle.load(f)
        else:
            showinfo("Warning", "No encoding file found.")

        # Extract stored encodings and names
        print(all_encodings)
        
        stored_encodings = []
        stored_names = []
        for encoding_data in all_encodings:
            stored_encodings.append(encoding_data[0][0])  # Extract encodings
            stored_names.append(encoding_data[1])  # Extract names

        





        while True:
            ret, frame = cap.read()

            # Detect faces in the current frame
            face_locations = face_recognition.face_locations(frame)
            face_encodings = face_recognition.face_encodings(frame, face_locations)

            for unknown_encoding in face_encodings:
                # Compare the unknown encoding with all stored encodings
                results = face_recognition.compare_faces(stored_encodings, unknown_encoding)

                # Check if a match was found
                if True in results:
                    matched_idx = results.index(True)  # Get the index of the matched encoding
                    matched_id = stored_names[matched_idx]  # Get the corresponding name
                    print(f"Match found: {matched_id}")

                    today = date.today()
                    current_time = datetime.now().time()
                    cur.execute("SELECT * FROM ATTENDANCE_INFO WHERE user_id = ?", (matched_id,))
                    data = cur.fetchall()
                    if can_record < 1:
                        today_str = today.isoformat()
                        current_time_str = current_time.strftime("%H:%M:%S")
                            
                        cur.execute("INSERT INTO ATTENDANCE_INFO (user_id, date, time) VALUES (?, ?, ?)", (matched_id, today_str, current_time_str))
                        con.commit()
                        showinfo("Success", "Attendance recorded successfully.")
                        can_record += 1




                # else:
                #     print("No match found.")

            # Display the frame
            if ret:
                imageBackground[162:162 + 480, 55:55 + 640] = frame
                cv2.imshow("Attendance", imageBackground)
                if cv2.waitKey(1) & 0xFF == ord("p"):
                    break
            else:
                break
            

        cap.release()
        cv2.destroyAllWindows()



    #! <--------------------------------------------------See Attendance Data----------------------------------------------------->

    def option2(self):

        root5 = Tk()
        root5.geometry("2000x2000")
        root5.title("My Attendance Data")
        Label(root5, text="Your Attendance Info", font="Arial 17 bold").pack(side=TOP, pady=10)
        
        fr = Frame(root5)
        fr.pack()


        def myAttendanceInfo(id):

            cur.execute("SELECT * FROM ATTENDANCE_INFO WHERE user_id = ?", (id,))
            data_ATTENDANCE_INFO = cur.fetchall()

            cur.execute("SELECT * FROM USER_INFO WHERE user_id = ?", (id,))
            data_USER_INFO = cur.fetchall()

            if not data_USER_INFO:
                Label(root5, text="No user found with the provided ID.", font="Arial 11", fg="red").pack()
                return

            Label(root5, text="\n", font="Arial 11").pack()

            fr=Frame(root5)
            fr.pack()


            def myName(id):
                if data_USER_INFO:
                    fname = data_USER_INFO[0][1] 
                    lname = data_USER_INFO[0][2]
                    Label(fr, text="            HELLO " + str(fname)+" "+str(lname), font="Arial 11").grid(row=0, column=0)
                else:
                    Label(fr, text="User information not found.", font="Arial 11", fg="red").grid(row=0, column=0)
                    root5.destroy()
                    self.option2()




            i = 1
            j = 0
            k = 1

            check = 0

            Label(fr, text="DATE", font="Arial 11").grid(row=i, column=j)
            Label(fr, text="TIME", font="Arial 11").grid(row=i, column=k)

            if not data_ATTENDANCE_INFO:
                Label(fr, text="No attendance records found.", font="Arial 11", fg="red").pack()
                root5.destroy()
                self.optionsffdf()
            else:
                for idx, record in enumerate(data_ATTENDANCE_INFO):
                    if check == 0:
                        myName(record[0])
                        check = 1
                    date = record[1]
                    time = record[2]
                    Label(fr, text=date, font="Arial 11").grid(row=idx+2, column=j)
                    Label(fr, text=time, font="Arial 11").grid(row=idx+2, column=k)




        
        Label(fr, text="Enter Your User ID", font="Arial 11").pack(side=LEFT, padx=5)
        E1 = Entry(fr, font="Arial 11")
        E1.pack(side=LEFT, padx=5)
        Button(fr, text="Check", command=lambda: myAttendanceInfo(E1.get())).pack(side=LEFT, padx=5)

        def fun7():
            root5.destroy()
            self.options()

        Button(fr, text="Home", command=fun7).pack(side=LEFT, padx=5)

        root5.mainloop()



    #! <--------------------------------------------------Adding a new user----------------------------------------------------->



    def option3(self):
        root4 = Tk()
        root4.geometry("2000x2000")
        root4.title("Attendance System")
        Label(root4, text="Add User Details", font="Arial 17 bold").pack(side=TOP, pady=10)
        fr=Frame(root4)
        fr.pack()
        Label(fr, text="User ID", font="Arial 11").grid(row=0,column=0)
        E1 = Entry(fr, font="Arial 11")
        E1.grid(row=0,column=1)

        Label(fr, text="FName", font="Arial 11").grid(row=0,column=2)
        E2 = Entry(fr, font="Arial 11")
        E2.grid(row=0,column=3)

        Label(fr, text="LName", font="Arial 11").grid(row=0,column=4)
        E3 = Entry(fr, font="Arial 11")
        E3.grid(row=0,column=5)
        

        #! Add face data
        def add_faces(id):
            cap = cv2.VideoCapture(0)
            cap.set(3, 640)
            cap.set(4, 480)

            facedetect = cv2.CascadeClassifier(r'D:\VS_Code\Minor_Project_1\Main_Project_files\haarcascade_frontalface_default.xml')
            imageBackground = cv2.imread(r"D:\VS_Code\Minor_Project_1\Files\Resources\background.png")

            faces_data = []

            def findEncodings(face):
                encodeList = []
                encode = face_recognition.face_encodings(face)
                
                if encode:  # Check if encoding is found
                    encodeList.append(encode[0])  # Append only the first encoding
                    print("Encoding for ID:", id, "is saved successfully.")
                else:
                    print("No encoding found.")
                
                encodeListKnownWithIds = [encodeList, id]
                return encodeListKnownWithIds

            face = None
            while True:
                ret, frame = cap.read()
                gray_scale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = facedetect.detectMultiScale(gray_scale, 1.3, 5)  # Detect faces 

                for (x, y, w, h) in faces:
                    crop_img = frame[y:y+h, x:x+w]
                    if len(faces_data) < 1:
                        faces_data.append(crop_img)
                        face = frame
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255,0,0), 2)

                if ret:
                    imageBackground[162:162 + 480, 55:55 + 640] = frame
                    cv2.imshow("Attendance", imageBackground)
                    if cv2.waitKey(1) & 0xFF == ord("p"):
                        break
                else:
                    break

            cap.release()
            cv2.destroyAllWindows()

            if face is not None:
                encoded_data = findEncodings(face)
                data_path = r'D:\VS_Code\Minor_Project_1\Main_Project_files\data\data'

                # Save or append encodings
                encode_file_path = os.path.join(data_path, 'EncodeFile.pkl')
                if os.path.exists(encode_file_path):
                    with open(encode_file_path, 'rb') as f:
                        existing_data = pickle.load(f)
                else:
                    existing_data = []
                
                # Append new encoding data
                existing_data.append(encoded_data)
                print("Total encodings:", len(existing_data))

                # Save updated data back to the pickle file
                with open(encode_file_path, 'wb') as f:
                    pickle.dump(existing_data, f)
                print("Encodings and ID saved to file.")
            else:
                print("No face data found.")

            showinfo("Success", "Data inserted!")

            root4.destroy()
            self.options()

        #! Add user info
        def add():
            count = 1
            cur.execute("SELECT * FROM USER_INFO")
            data = cur.fetchall()
            for i in data:
                if E1.get() == i[0]:
                    showinfo("Error", "Data already exists")
                    count = 0
            if count == 1:
                id = E1.get()
                cur.execute("INSERT INTO USER_INFO VALUES (?,?,?)", (E1.get(), E2.get(), E3.get()))
                con.commit()

                add_faces(id)


        def edit(): 
            cur.execute("UPDATE USER_INFO SET user_id=?, fname=?, lname=?", (int(E1.get()), E2.get(), E3.get()))
            con.commit()
            showinfo("Success", "Data has been edited successfully.")
            root4.destroy()
            self.options()
        
        Button(fr, text="Add", font="Arial 11 bold", bg='green', command=add).grid(row=0,column=10)    
        Button(fr, text="Edit", font="Arial 11 bold", bg='green', command=edit).grid(row=0,column=11)
        def fun13():
            root4.destroy()
            self.options()
        Button(root4, text="Home", command=fun13, font="Arial 15 bold").pack(pady=100)

m = Attendance_system()
m.fun1()