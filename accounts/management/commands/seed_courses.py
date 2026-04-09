import json
import os
from django.core.management.base import BaseCommand
from accounts.models import Course, Unit, Lesson, Material

class Command(BaseCommand):
    help = 'بذر قاعدة البيانات بالكورسات من ملف JSON'

    def handle(self, *args, **kwargs):
        # مسار ملف الـ JSON اللي السكريبت التاني طلعه
        file_path = 'youtube_course_data.json'
        
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'❌ لم يتم العثور على ملف {file_path}. تأكد من تشغيل سكريبت يوتيوب أولاً.'))
            return

        self.stdout.write('⏳ جاري زراعة البيانات في الداتا بيز...')

        with open(file_path, 'r', encoding='utf-8') as file:
            courses_data = json.load(file)

            for c_data in courses_data:
                # 1. إنشاء أو جلب الكورس (عشان لو شغلنا الأمر مرتين ميكررش الداتا)
                course, created = Course.objects.get_or_create(
                    name=c_data['course_name'],
                    defaults={
                        'description': c_data.get('description', ''),
                        'grade_level': c_data.get('grade_level', 'عام')
                    }
                )
                
                if created:
                    self.stdout.write(self.style.SUCCESS(f'✅ تم إنشاء كورس جديد: {course.name}'))
                else:
                    self.stdout.write(self.style.WARNING(f'⚠️ الكورس موجود بالفعل: {course.name}'))

                # 2. إنشاء الوحدات
                for u_data in c_data.get('units', []):
                    unit, u_created = Unit.objects.get_or_create(
                        course=course,
                        title=u_data['unit_title'],
                        defaults={'order': u_data.get('order', 1)}
                    )

                    # 3. إنشاء الدروس
                    for l_data in u_data.get('lessons', []):
                        lesson, l_created = Lesson.objects.get_or_create(
                            unit=unit,
                            title=l_data['lesson_title'],
                            defaults={
                                'description': l_data.get('description', ''),
                                'order': l_data.get('order', 1)
                            }
                        )

                        # 4. إنشاء المحتوى (الفيديوهات)
                        for m_data in l_data.get('materials', []):
                            Material.objects.get_or_create(
                                lesson=lesson,
                                title=m_data['title'],
                                defaults={
                                    'material_type': m_data['type'],
                                    'url': m_data['url']
                                }
                            )

        self.stdout.write(self.style.SUCCESS('\n🎉 تمت عملية الزراعة بنجاح! الداتا بيز بتاعتك مليانة دلوقتي.'))