from django.contrib import admin
from django.urls import path
from accounts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/chat/', views.chat_with_ai, name='chat_with_ai'),
    path('chat/', views.chat_ui, name='chat_ui'),
    path('login/', views.login_user, name='login'), # 👈 ده اللينك الجديد
]