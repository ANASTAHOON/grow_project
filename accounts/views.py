import json
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from google import genai
from google.genai import types # 👈 استدعينا دي عشان نظبط المعايير
from .models import Student

@csrf_exempt 
def chat_with_ai(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
           # التأكد إن اليوزر عامل لوجين الأول
            if not request.user.is_authenticated:
                return JsonResponse({'error': 'يجب تسجيل الدخول أولاً!', 'status': 'failed'}, status=401)
            
            # بنجيب بيانات الطالب المربوط باليوزر اللي فاتح دلوقتي
            try:
                student = request.user.student
            except:
                return JsonResponse({'error': 'هذا الحساب ليس حساب طالب!', 'status': 'failed'})
            # 1. المعيار الأول: (System Instruction) - الهوية المنفصلة
            system_prompt = f"""أنت مساعد تعليمي ذكي في منصة دراسية.
            - اسم الطالب الذي تتحدث معه: {student.user.username}
            - صفه الدراسي: {student.grade_level}
            - نقاطه الحالية: {student.xp_points} XP.
            
            قواعد الاستجابة الخاصة بك:
            1. كن مشجعاً وداعماً دائماً واربط كلامك بنقاط الـ XP الخاصة به.
            2. اجعل إجاباتك مختصرة (في حدود 3 إلى 4 أسطر).
            3. استخدم الرموز التعبيرية (Emojis) بشكل مناسب.
            4. ارفض بأدب الإجابة على أي أسئلة خارج نطاق التعليم والدراسة والتطوير الشخصي."""

            api_key = "AIzaSyBJ64t9sjmMWsElp6btGBpwzbVPNyFYzR8" # متنساش تغيره بعدين!
            client = genai.Client(api_key=api_key)
            
            # 2. المعيار الثاني: ضبط الإعدادات (Configuration)
            config = types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.7, # 0.7 نسبة ممتازة للتوازن بين الدقة والإبداع
            )

            # 3. إرسال "سؤال الطالب فقط" للموديل مع الإعدادات
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=user_message,
                config=config
            )

            return JsonResponse({'reply': response.text, 'status': 'success'})

        except Exception as e:
            return JsonResponse({'error': str(e), 'status': 'failed'}, status=500)
            
    return JsonResponse({'error': 'Only POST requests are allowed'}, status=400)

def chat_ui(request):
    return render(request, 'chat.html')
# ==========================================
# دالة تسجيل الدخول (Login) 🔐
# ==========================================
def login_user(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        
        # جانجو بيتأكد إن البيانات صح
        user = authenticate(request, username=u, password=p)
        
        if user is not None:
            login(request, user) # كده دخلناه السيستم
            return redirect('chat_ui') # نوديه على شاشة الشات فوراً
        else:
            # لو البيانات غلط نرجعله رسالة إيرور
            return render(request, 'login.html', {'error': 'اسم المستخدم أو كلمة المرور غير صحيحة ❌'})
            
    return render(request, 'login.html')