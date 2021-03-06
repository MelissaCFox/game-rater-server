"""gamerater URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.conf.urls import include
from django.conf.urls.static import static
from django.urls import path
from rest_framework import routers
from gameraterapi.views import register_user, login_user
from gameraterapi.views import GameView, CategoryView, GameReviewView, GameRatingView
from gameraterapi.views.image import GameImageView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'games', GameView, 'game')
router.register(r'categories', CategoryView, 'category')
router.register(r'reviews', GameReviewView, 'review')
router.register(r'ratings', GameRatingView, 'rating')
router.register(r'images', GameImageView, 'image')

urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('', include('gameraterreports.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
