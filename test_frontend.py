import urllib.request
import json

# 1. ده اللينك بتاع الـ API اللي إنت لسه عامله
url = 'http://127.0.0.1:8000/api/chat/'

# 2. دي الرسالة اللي الطالب كتبها في الموبايل
student_message = {'message': 'أنا خايف جداً من امتحان بكرة، أعمل إيه؟'}

# 3. بنحول الرسالة للغة الـ JSON اللي بيفهمها الويب
data = json.dumps(student_message).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})

print("📱 جاري إرسال رسالة الطالب من الموبايل للـ API بتاعك... ⏳\n")

try:
    # 4. بنخبط على الـ API ونستنى الرد
    with urllib.request.urlopen(req) as response:
        # 5. بنستلم الرد ونفكه
        result = json.loads(response.read().decode('utf-8'))
        
        print("✅ الباك إند بتاعك رد بالـ JSON ده:")
        print("-----------------------------------------")
        print(f"الحالة: {result['status']}")
        print(f"رد الذكاء الاصطناعي: {result['reply']}")
        print("-----------------------------------------")
except Exception as e:
    print("⚠️ حصلت مشكلة، اتأكد إن السيرفر شغال في التيرمينال التانية:")
    print(e)