from django.contrib import admin
from django.urls import path
from . import views  # Import your views if they are in the same directory

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload/', views.upload_bom, name='upload_bom'),
    path('', views.home, name='home'),  # Add this line
]
