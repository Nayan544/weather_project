from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WeatherDataViewSet, home

app_name = 'weather'

router = DefaultRouter()
router.register(r'weather', WeatherDataViewSet, basename='weather')

urlpatterns = [
    path('', home, name='home'),
]

urlpatterns += router.urls