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
