from django.urls import path
from . import views
urlpatterns =[
    path('list', views.list_view),
    path('add',views.add_view),
    path('del',views.del_view),
    path('update',views.update_view),
    path('update1',views.update1_view),
    path('<str:bzx>', views.weather_view),
]