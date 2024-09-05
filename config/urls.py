"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django import urls
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.views import TokenBlacklistView
urlpatterns = [
    path('admin/', admin.site.urls),

    # django auth urls
    path('auth/api/', include('django.contrib.auth.urls')),

    # ==============================SIMPLE JWT =======================================
    # # This API endpoint will be used to obtain a JSON Web Token (JWT) for an authenticated user.
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # # This API endpoint will be used to refresh a JWT.
    # path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    # path("api/token/blacklist", TokenBlacklistView.as_view(), name="token_blacklist"),

    # ==============================DJOSER WITH SIMPLE JWT =======================================
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('api/', include('api.urls')),
]
