from django.contrib import admin
from .models import Parent, Student, ConnectionRequest

# 1. بنعمل كلاس عشان نعرض الطلبة جوه صفحة ولي الأمر
class StudentInline(admin.TabularInline):
    # السطر السحري ده بيجيب العلاقة العكسية بتاعت الـ Many-to-Many
    model = Student.parents.through  
    extra = 1  # بيظهرلك سطر فاضي لو حابب تضيف طالب جديد للأب من نفس الصفحة
    verbose_name = "Student"
    verbose_name_plural = "Students (Children)"

# 2. بنربط الكلاس ده بصفحة الأب
class ParentAdmin(admin.ModelAdmin):
    inlines = [StudentInline]

# 3. بنسجل الجداول في اللوحة
admin.site.register(Parent, ParentAdmin) # ربطنا الأب بالتعديل الجديد
admin.site.register(Student)
admin.site.register(ConnectionRequest)
# فوق خالص، اتأكد إنك مستدعي كل الجداول دي من الـ models
from .models import Student, Parent, ConnectionRequest, Teacher, Course, Unit, Lesson, Material

# (سيب أكواد تسجيل الطالب وولي الأمر القديمة زي ما هي)

# ضيف السطور دي تحت خالص عشان تظهر الجداول الجديدة
admin.site.register(Teacher)
admin.site.register(Course)
admin.site.register(Unit)
admin.site.register(Lesson)
admin.site.register(Material)