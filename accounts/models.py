from django.db import models
from django.contrib.auth.models import User

# 1. جدول ولي الأمر
class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    def __str__(self):
        return f"Parent: {self.user.username}"

# 2. جدول الطالب
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # السحر هنا: ManyToManyField عشان الطالب يقدر يكون ليه كذا ولي أمر، وولي الأمر ليه كذا طالب
    parents = models.ManyToManyField(Parent, related_name='children', blank=True)
    
    grade_level = models.CharField(max_length=50)
    xp_points = models.IntegerField(default=0)
    student_code = models.CharField(max_length=20, unique=True, null=True, blank=True)
    
    def __str__(self):
        return f"Student: {self.user.username} - Code: {self.student_code}"

# 3. الجدول الجديد: غرفة انتظار الطلبات (نظام الموافقات)
class ConnectionRequest(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'قيد الانتظار'),
        ('Approved', 'تمت الموافقة'),
        ('Rejected', 'مرفوض'),
    )
    # مين ولي الأمر اللي باعت الطلب؟
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='requests_sent')
    # مين الطالب المبعوتله الطلب؟
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='requests_received')
    # حالة الطلب إيه دلوقتي؟
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    # الطلب اتبعت إمتى؟
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request: {self.parent.user.username} -> {self.student.user.username} ({self.status})"
    
    # ==========================================
# 4. جدول المدرس (Teacher)
# ==========================================
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    bio = models.TextField(blank=True, null=True, help_text="نبذة مختصرة عن المدرس")

    def __str__(self):
        return f"Teacher: {self.user.username}"

# ==========================================
# 5. جدول الكورس / المادة (Course) 👈 (ده اللي كان ناقص وعمل المشكلة)
# ==========================================
class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    grade_level = models.CharField(max_length=50, help_text="الصف الدراسي")
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name='courses', blank=True)
    students = models.ManyToManyField('Student', related_name='courses', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.grade_level}"

# ==========================================
# 6. جدول الوحدة (Unit)
# ==========================================
class Unit(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='units')
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.name} - {self.title}"

# ==========================================
# 7. جدول الدرس (Lesson)
# ==========================================
class Lesson(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.unit.title} - {self.title}"

# ==========================================
# 8. جدول المحتوى (Material)
# ==========================================
class Material(models.Model):
    MATERIAL_TYPES = (
        ('video', 'فيديو شرح'),
        ('pdf', 'ملف ملزمة (PDF)'),
        ('quiz', 'اختبار (Quiz)'),
    )
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='materials')
    title = models.CharField(max_length=200)
    material_type = models.CharField(max_length=20, choices=MATERIAL_TYPES)
    url = models.URLField(max_length=500)

    def __str__(self):
        return f"{self.get_material_type_display()} - {self.title}"