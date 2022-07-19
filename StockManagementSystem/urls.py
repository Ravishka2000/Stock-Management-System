from django.contrib import admin
from django.urls import path
from stockmgmt import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('listitems/', views.list_items, name='list_items'),
    path('', views.home, name='home'),
    path('additems/', views.add_items, name='add_items'),
]
