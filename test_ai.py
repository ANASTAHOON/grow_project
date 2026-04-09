import os
import django

# 1. تهيئة بيئة جانجو
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grow_backend.settings')
django.setup()

# 2. استدعاء المكتبة الجديدة بتاعة جوجل (خد بالك الاسم اتغير هنا)
from google import genai
from accounts.models import Student

# حط المفتاح "الجديد" بتاعك هنا 
api_key = "AIzaSyBJ64t9sjmMWsElp6btGBpwzbVPNyFYzR8"

# 3. تهيئة الاتصال بالطريقة الجديدة
client = genai.Client(api_key=api_key)

# 4. جلب بيانات الطالب
student = Student.objects.first()
ai_prompt = f"""
أنت مساعد ذكي تعليمي.
تتحدث مع الطالب: {student.user.username}
الصف: {student.grade_level}
النقاط: {student.xp_points}
مهمتك: شجعه في 3 أسطر لأنه يشعر بالتأخر في المذاكرة.
"""

print("\nيتم إرسال البيانات لجوجل بالإصدار الجديد... ⏳")
try:
    # 5. إرسال الطلب للموديل الجديد
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=ai_prompt
    )
    print("\nرد الذكاء الاصطناعي 🤖:")
    print("-------------------------")
    print(response.text)
except Exception as e:
    print("\n⚠️ حصلت مشكلة:")
    print(e)