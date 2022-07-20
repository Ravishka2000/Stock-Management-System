from django.contrib import admin
from django.urls import path, include
from stockmgmt import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('listitems/', views.list_items, name='list_items'),
    path('', views.home, name='home'),
    path('additems/', views.add_items, name='add_items'),
    path('updateitems/<str:pk>/', views.update_items, name='update_items'),
    path('deleteitems/<str:pk>/', views.delete_items, name='delete_items'),
    path('stockdetail/<str:pk>', views.stock_detail, name='stock_detail'),
    path('issueitems/<str:pk>/', views.issue_items, name='issue_items'),
    path('receiveitems/<str:pk>/', views.receive_items, name='receive_items'),
    path('reorderlevel/<str:pk>/', views.reorder_level, name='reorder_level'),
    path('accounts/', include('registration.backends.default.urls')),
    path('listhistory/', views.list_history, name='list_history'),
]
