from django.urls import path
from . import views
urlpatterns= [
    path('place_order/<int:p_id>', views.get_order),
    # 127.0.0.1:8000//payment/jump/
    path('jump/', views.JumpView.as_view()),
    # 127.0.0.1:8000//payment/result/
    path('result/', views.ResultView.as_view()),
    # path('recode/',views.recode)

]