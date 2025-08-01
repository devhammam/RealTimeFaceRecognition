import os
import pickle
import cvzone
import cv2
import face_recognition



import numpy as np
from datetime import datetime

#للاتصال بقاعده البيانات
import json
#من هنا يبدا ترميز الصور
import os
import cv2
import pickle
import face_recognition

# المسار الأساسي للصور
folderPath = 'img'
newFolderPath = 'blob'

# إنشاء المجلد الجديد إذا لم يكن موجودًا
if not os.path.exists(newFolderPath):
    os.makedirs(newFolderPath)

imgList = []
studentIds = []
pathList = os.listdir(folderPath)

# تحميل الصور
for path in pathList:
    img = cv2.imread(os.path.join(folderPath, path))
    if img is not None:
        imgList.append(img)
        studentId = os.path.splitext(path)[0]
        studentIds.append(studentId)
        newFilePath = os.path.join(newFolderPath, path)
        cv2.imwrite(newFilePath, img)
        print(f"تم رفع الصورة: {path} إلى {newFolderPath}")
    else:
        print(f"فشل تحميل الصورة: {path}")

print("معرفات الطلاب:", studentIds)

# دالة استخراج الترميزات
def findEncodings(imgList):
    encodeList = []
    for img in imgList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        try:
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        except IndexError:
            print("لم يتم العثور على وجه في إحدى الصور.")
    return encodeList

print("الترميز يبدأ الآن...")
encoListKnown = findEncodings(imgList)
encoListKnownWithIds = [encoListKnown, studentIds]

# حفظ البيانات
file = open("EncodeFile.pickle", 'wb')
pickle.dump(encoListKnownWithIds, file)
file.close()
print("تم حفظ ملف الترميز بنجاح.")

#هنا ينتهي ترميز الصور





















# تحميل بيانات الطلاب من ملف JSON
with open("students.json", "r" ,encoding="utf-8") as file:
    student_data = json.load(file)







cap = cv2.VideoCapture(0)

cap.set(3, 640)
cap.set(4, 480)

imgBackground =cv2.imread('Resources/background.png')

#استيراد مكان الصور الئ قائمه صحيحه
folderModePath= 'Resources/Modes'
#تحديد مكان الصور في النضام
modePathlist =os.listdir(folderModePath)
imgModlist=[]



for path in modePathlist:
    #اضافه الصور الئ النضام
    imgModlist.append(cv2.imread(os.path.join(folderModePath,path)))
#print(len(imgModlist))



#استيراد ملق الترميزوتجويله الئ معرف الطالب وكتابته قي ملف

print("تحميل ملف التشفير...")
try:
    with open("EncodeFile.pickle", 'rb') as file:
        encoListKnownWithIds = pickle.load(file)
    encoListKnown, studentIds = encoListKnownWithIds
    print("تم تحميل الترميزات:", len(encoListKnown))
    print("معرفات الطلاب:", studentIds)
except FileNotFoundError:
    print("خطأ: لم يتم العثور على ملف الترميز.")
    exit()
except Exception as e:
    print(f"خطأ أثناء تحميل ملف الترميز: {e}")
    exit()
modeType = 0
counter=0
id =-1
imgStudent = []
while True:
    success, img = cap.read()
#تصغير حجم الصورة لكي تسهل المعالجه
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    # تحويل الصوره الئ RGB
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    #ياخذ الصوره من الكاميرا ويرمزها ثم يتم مقارنتها بالصور المرمزه في ملف التشفير
    faceCurFrame=face_recognition.face_locations(imgS)
    #العثور علئ الصوره ومقارنتها
    encodeCurFrame=face_recognition.face_encodings(imgS,faceCurFrame)






    #لتحديد ضهور الكاميرا في الخلفيه
    imgBackground[162:162+480, 55:55+640]= img
    #تحديد مكان الصوره في الخلفيه
    #اذا غيرت الرقم ستضهر صوره اخرئ من الصور الذي في الملف MODE
    imgBackground[44:44+633, 808:808+414]= imgModlist[modeType]

    if faceCurFrame:


        #  لووب لمقارنه صوره تلو اخرئ ياخذ الصوره في الاطار الحالي والتشفير ويقارنهما بالصور التي في الملفات
        for encodeFace, faceLoc in zip(encodeCurFrame,faceCurFrame):
            #مقارنتهما بالترميز الذي لدينا
            matches=face_recognition.compare_faces(encoListKnown,encodeFace)
            faceDis=face_recognition.face_distance(encoListKnown,encodeFace)
           # print("التطابقات", matches)
           # print("مسافه الوجه",faceDis)


           # للحصول علء اقل قيمه في موشر التطابق
            matchIndex=np.argmin(faceDis)
            print("موشر المطابقه ",matchIndex)


            if matches[matchIndex]:
                print("تم اكتشاف وجه معروف")
                print(studentIds[matchIndex])


                #لعمل مربع حول الوجة
                y1,x2,y2,x1=faceLoc
                y1, x2, y2, x1 = y1+4, x2*4, y2*4, x1*4
                bbox=55+x1,162+y1, x2-x1, y2 - y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox,20,rt=0)
                #بيانات الطالب التي ستعرض في if
                id = studentIds[matchIndex]
                print(id)
                #print(id)
                #العداد اذا كان صفرا غير الصوره في الخلفبه التي هي نشط الى
                if counter==0:
                    #cvzone.putTextRect(imgBackground,"loding",(257,400))
                    #cv2.imshow("Face Attendance",  imgBackground)
                    #cv2.waitKey(1)
                    counter =1
                    modeType=1


        if counter!= 0:
            #اذا كان الاطار الايمن يساوي الصوره 1 نعرض بيانات الطالب

            if counter==1:
                #للحصول علئ معلومات الطالب
                # جلب بيانات الطالب من studenes.json
                studentInfo = student_data.get(str(id), {})

                print("بيانات الطالب:", studentInfo)


                # جلب الصورة من الملفات المحلية
                  # المسار المحلي للصورة
                with open(f"blob/{id}.png", 'rb') as ham:
                    img_data= ham.read()


                array = np.frombuffer(img_data,np.uint8)
                imgStudent = cv2.imdecode(array,cv2.COLOR_BGR2RGB)
                imgStudent = cv2.resize(imgStudent, (216, 216))

                try:
                    datetimeObject = datetime.strptime(studentInfo.get('اخر حضور', '1900-01-01 00:00:00'),
                                                       "%Y-%m-%d %H:%M:%S")
                    secondsElapsed = (datetime.now() - datetimeObject).total_seconds()

                    if secondsElapsed >=200 :  # إذا مر وقت كاف منذ آخر حضور
                        # تحديث بيانات الطالب
                        student_data[str(id)]['اجمالي_الحضور'] += 1
                        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        student_data[str(id)]['اخر حضور'] = current_time

                        # تحديث ملف JSON
                        with open("students.json", "w",encoding="utf-8") as file:
                            json.dump(student_data, file, ensure_ascii=False, indent=4)

                        print(f"تم تسجيل الحضور للطالب {id}.")
                        modeType = 1  # تغيير الحالة بعد التحديث
                    else:

                        print(f"الوجه {id} تم تسجيل حضوره مسبقًا.")
                        modeType =3
                except Exception as e:
                    print(f"خطأ أثناء تحديث بيانات الحضور: {e}")
                    modeType = 3




            if modeType != 3:



                if 10<counter<20:
                    modeType = 2
                imgBackground[44:44 + 633, 808:808 + 414] = imgModlist[modeType]


                if counter <=10:


                    #لعرض ايام الحضور
                    cv2.putText(imgBackground,str(studentInfo['اجمالي_الحضور']),(861,125),
                                cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)



                    cv2.putText(imgBackground, str(studentInfo['التخصص']), (1006, 550),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 255, 255), 1)

                    cv2.putText(imgBackground, str(id), (1006, 493),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)

                    cv2.putText(imgBackground, str(studentInfo['التقدير']), (910, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                    cv2.putText(imgBackground, str(studentInfo['السنة']), (1052, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                    cv2.putText(imgBackground, str(studentInfo['سنة البدء']), (1125, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                    (w, h), _ = cv2.getTextSize(studentInfo['الاسم'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                    offset = (414-w)//2
                    cv2.putText(imgBackground, str(studentInfo['الاسم']), (808+offset, 445),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

                    #صوره الطالب
                    imgBackground[175:175+216,909:909+216] =imgStudent





                counter+=1

                if counter>=20:
                    counter=0
                    modeType=0
                    studentInfo=[]
                    id=-1
                    imgStudent=[]
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModlist[modeType]

    else:
        modeType = 0
        counter = 0
    # cv2.imshow("Webcam", img)
    cv2.imshow("Face Attendance",  imgBackground)

    cv2.waitKey(1)
