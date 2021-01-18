from django.urls import path
from . import views

urlpatterns = [
    #http://127.0.0.1:8000/v1/product/username/upload
    path('<str:username>/upload', views.upload_product),
    path('<str:username>/uploadimg', views.upload_img),
    path('<str:username>/list', views.product_list),  #list总
    path('<str:username>/search', views.product_search),
    path('<str:username>/detail', views.product_detail)
]

