from django.urls import path

from blog import views

urlpatterns = [
    path('release/<int:number>',views.release),
    path('list',views.get_listall),
    path('list/<str:username>',views.get_listuser),
    path('delete/<int:b_id>',views.delete_b_id),
    path('collection/<str:username>/<int:b_id>',views.collection_username_b_id),
    path('comment/<str:username>/<int:b_id>',views.comment_username_b_id),
    path('restore/<str:username>/<int:b_id>/<int:c_id>',views.restore_username_b_id_c_id),
]

