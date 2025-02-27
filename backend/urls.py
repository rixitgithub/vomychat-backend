from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
     path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('', include('users.urls')),
    
]