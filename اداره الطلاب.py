import customtkinter as ctk
from tkinter import messagebox, filedialog
import json
import os
from PIL import Image, ImageTk

# إعداد الواجهة
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# دالة لتحميل البيانات من ملف JSON
def تحميل_البيانات():
    ملف_البيانات = "students.json"
    if os.path.exists(ملف_البيانات):
        with open(ملف_البيانات, "r", encoding="utf-8") as ملف:
            return json.load(ملف)
    return {}

# دالة لحفظ البيانات في ملف JSON
def حفظ_البيانات(الطلاب):
    ملف_البيانات = "students.json"
    with open(ملف_البيانات, "w", encoding="utf-8") as ملف:
        json.dump(الطلاب, ملف, ensure_ascii=False, indent=4)

# دالة لتحميل الصورة
def تحميل_صورة(مسار_الصورة, حجم=(100, 100)):
    try:
        صورة = Image.open(مسار_الصورة)
        صورة = صورة.resize(حجم, Image.ANTIALIAS)
        return ImageTk.PhotoImage(صورة)
    except Exception as خطأ:
        messagebox.showerror("خطأ", f"تعذر تحميل الصورة: {خطأ}")
        return None

# دالة لإضافة طالب جديد
def إضافة_طالب(الطلاب, رقم_الجامعي, الاسم, التخصص, سنة_البدء, مسار_الصورة=None):
    if not رقم_الجامعي or not الاسم or not التخصص or not سنة_البدء:
        messagebox.showwarning("خطأ", "يرجى ملء جميع الحقول!")
        return

    if مسار_الصورة:
        مسار_حفظ_الصورة = os.path.join("img", f"{رقم_الجامعي}.png")
        try:
            صورة = Image.open(مسار_الصورة)
            صورة.save(مسار_حفظ_الصورة)
            messagebox.showinfo("نجاح", "تم حفظ الصورة بنجاح!")
        except Exception as خطأ:
            messagebox.showerror("خطأ", f"تعذر حفظ الصورة: {خطأ}")

    الطلاب[رقم_الجامعي] = {
        "الاسم": الاسم,
        "التخصص": التخصص,
        "سنة البدء": سنة_البدء,
        "اجمالي_الحضور": 0,
        "التقدير": "G",
        "السنة": 1,
        "اخر حضور": "2025-2-8 00:54:34",
        "صورة": f"{رقم_الجامعي}.png" if مسار_الصورة else None
    }

    حفظ_البيانات(الطلاب)
    messagebox.showinfo("نجاح", "تمت إضافة الطالب بنجاح!")

# دالة لعرض قائمة الطلاب
def عرض_الطلاب(الطلاب, مربع_النص):
    مربع_النص.delete("1.0", "end")
    for رقم_الجامعي, معلومات in الطلاب.items():
        مربع_النص.insert("end", f"الرقم الجامعي: {رقم_الجامعي}\n")
        مربع_النص.insert("end", f"الاسم: {معلومات['الاسم']}\n")
        مربع_النص.insert("end", f"التخصص: {معلومات['التخصص']}\n")
        مربع_النص.insert("end", f"سنة البدء: {معلومات['سنة البدء']}\n")
        if معلومات.get("صورة"):
            مربع_النص.insert("end", f"صورة: {معلومات['صورة']}\n")
        مربع_النص.insert("end", "-" * 30 + "\n")

# دالة لإنشاء واجهة الإدخال
def إنشاء_واجهة_الإدخال(النافذة, الطلاب, مربع_النص):
    إطار = ctk.CTkFrame(النافذة)
    إطار.pack(pady=20, padx=20, fill="x")

    # حقول الإدخال
    ctk.CTkLabel(إطار, text="الرقم الجامعي:").grid(row=0, column=0, padx=10, pady=5)
    حقل_رقم_الجامعي = ctk.CTkEntry(إطار)
    حقل_رقم_الجامعي.grid(row=0, column=1, padx=10, pady=5)

    ctk.CTkLabel(إطار, text="الاسم:").grid(row=1, column=0, padx=10, pady=5)
    حقل_الاسم = ctk.CTkEntry(إطار)
    حقل_الاسم.grid(row=1, column=1, padx=10, pady=5)

    ctk.CTkLabel(إطار, text="التخصص:").grid(row=2, column=0, padx=10, pady=5)
    حقل_التخصص = ctk.CTkEntry(إطار)
    حقل_التخصص.grid(row=2, column=1, padx=10, pady=5)

    ctk.CTkLabel(إطار, text="سنة البدء:").grid(row=3, column=0, padx=10, pady=5)
    حقل_سنة_البدء = ctk.CTkEntry(إطار)
    حقل_سنة_البدء.grid(row=3, column=1, padx=10, pady=5)

    # زر تحميل الصورة
    مسار_الصورة = None
    def تحميل_الصورة():
        nonlocal مسار_الصورة
        مسار_الصورة = filedialog.askopenfilename(
            title="اختر صورة",
            filetypes=[("ملفات الصور", "*.png;*.jpg;*.jpeg")]
        )
        if مسار_الصورة:
            messagebox.showinfo("نجاح", "تم تحميل الصورة بنجاح!")

    زر_تحميل_الصورة = ctk.CTkButton(إطار, text="تحميل صورة", command=تحميل_الصورة)
    زر_تحميل_الصورة.grid(row=4, column=0, padx=10, pady=5)

    # زر الإضافة
    def إضافة():
        إضافة_طالب(
            الطلاب,
            حقل_رقم_الجامعي.get(),
            حقل_الاسم.get(),
            حقل_التخصص.get(),
            حقل_سنة_البدء.get(),
            مسار_الصورة
        )
        عرض_الطلاب(الطلاب, مربع_النص)

    زر_الإضافة = ctk.CTkButton(إطار, text="إضافة طالب", command=إضافة)
    زر_الإضافة.grid(row=4, column=1, padx=10, pady=5)

# دالة لإنشاء واجهة العرض
def إنشاء_واجهة_العرض(النافذة, الطلاب):
    إطار = ctk.CTkFrame(النافذة)
    إطار.pack(pady=20, padx=20, fill="both", expand=True)

    # قائمة عرض الطلاب
    مربع_النص = ctk.CTkTextbox(إطار, width=500, height=200)
    مربع_النص.pack(pady=10, padx=10)

    # زر تحديث القائمة
    زر_التحديث = ctk.CTkButton(إطار, text="تحديث القائمة", command=lambda: عرض_الطلاب(الطلاب, مربع_النص))
    زر_التحديث.pack(pady=10)

    return مربع_النص

# تشغيل التطبيق
if __name__ == "__main__":
    النافذة = ctk.CTk()
    النافذة.title("إدارة الطلاب")
    النافذة.geometry("600x500")

    الطلاب = تحميل_البيانات()
    مربع_النص = إنشاء_واجهة_العرض(النافذة, الطلاب)
    إنشاء_واجهة_الإدخال(النافذة, الطلاب, مربع_النص)

    النافذة.mainloop()