import requests
import json

# ==========================================
# 1. الإعدادات (حط المفتاح بتاعك والـ ID بتاع البلاي ليست)
# ==========================================
YOUTUBE_API_KEY = 'AIzaSyAKJtiQAUGkjwrk3s3QerkPgzXb8BnXnIs'

# الـ ID بتاع البلاي ليست (بنجيبه من لينك اليوتيوب بعد كلمة list=)
# مثال: ده ID لبلاي ليست كورس بايثون تجريبي
PLAYLIST_ID = 'PLYGJU1U6eacOn0zFwGOgl5dqFPhOlIcVc' 

def fetch_playlist_data():
    print("⏳ جاري سحب البيانات من يوتيوب...")
    
    # أول خطوة: نجيب اسم البلاي ليست عشان نخليه اسم الكورس
    url_playlist = f"https://www.googleapis.com/youtube/v3/playlists?part=snippet&id={PLAYLIST_ID}&key={YOUTUBE_API_KEY}"
    res_playlist = requests.get(url_playlist).json()
    
    if not res_playlist.get('items'):
        print("❌ لم يتم العثور على البلاي ليست! تأكد من الـ ID.")
        return

    course_name = res_playlist['items'][0]['snippet']['title']
    course_desc = res_playlist['items'][0]['snippet']['description']

    # الهيكل الأساسي للكورس زي ما صممناه في الداتا بيز
    course_data = {
        "course_name": course_name,
        "description": course_desc,
        "grade_level": "عام", # تقدر تعدلها بعدين
        "units": [
            {
                "unit_title": "الوحدة الأولى: أساسيات الكورس",
                "order": 1,
                "lessons": []
            }
        ]
    }

    # تاني خطوة: نجيب الفيديوهات اللي جوه البلاي ليست
    url_videos = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId={PLAYLIST_ID}&key={YOUTUBE_API_KEY}"
    res_videos = requests.get(url_videos).json()

    # ترتيب الدروس
    lesson_order = 1
    
    for item in res_videos.get('items', []):
        video_title = item['snippet']['title']
        video_desc = item['snippet']['description']
        video_id = item['snippet']['resourceId']['videoId']
        
        # لو الفيديو محذوف أو خاص نتجاهله
        if video_title == "Private video" or video_title == "Deleted video":
            continue

        # نبني الدرس ونحط جواه الماتيريال (الفيديو)
        lesson = {
            "lesson_title": video_title,
            "description": video_desc[:100] + "...", # ناخد أول 100 حرف بس من الوصف
            "order": lesson_order,
            "materials": [
                {
                    "title": f"فيديو شرح: {video_title}",
                    "type": "video",
                    "url": f"https://www.youtube.com/watch?v={video_id}"
                }
            ]
        }
        
        # نضيف الدرس للوحدة
        course_data['units'][0]['lessons'].append(lesson)
        lesson_order += 1

    # 3. نحفظ الداتا دي في ملف JSON عشان نستخدمه في السيستم بتاعنا
    with open('youtube_course_data.json', 'w', encoding='utf-8') as f:
        json.dump([course_data], f, ensure_ascii=False, indent=4)
        
    print(f"✅ تم سحب الكورس بنجاح! عدد الدروس: {lesson_order - 1}")
    print("📁 تم حفظ البيانات في ملف: youtube_course_data.json")

# تشغيل السكريبت
if __name__ == "__main__":
    fetch_playlist_data()