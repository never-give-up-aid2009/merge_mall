"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from . import views
from django.conf import settings
from user import views as user_views
from btoken import views as btoken_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login',views.test_login),
    path('blog/',include('blog.urls')),
    path('payment/', include('payment.urls')),
    path('v1/user',user_views.UserViews.as_view()),
    path('v1/users/', include('user.urls')),
    path('v1/btoken',btoken_views.Tokenviews.as_view()),
    path('v1/product/',include('product.urls')),
    path('v1/up_clothes/', include('pet_closet.urls')),
    path('v1/weather/', include('pet_closet.urls')),
    path('v1/pet_closet/', include('pet_closet.urls')),
]
urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)