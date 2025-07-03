from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import WeatherData
from .serializers import WeatherDataSerializer
import requests

class WeatherDataViewSet(viewsets.ModelViewSet):
    queryset = WeatherData.objects.all().order_by('-created_at')
    serializer_class = WeatherDataSerializer

    @action(detail=False, methods=['get'])
    def fetch(self, request):
        city = request.GET.get('city', 'Ahmedabad')
        api_key = 'be8827d7744cf96b45065785ed0e25a6'
        url = 'https://api.openweathermap.org/data/2.5/weather'
        params = {'q': city, 'appid': api_key, 'units': 'metric'}

        response = requests.get(url, params=params)
        data = response.json()

        if response.status_code == 200:
            temp = data['main']['temp']
            desc = data['weather'][0]['description']

            weather = WeatherData.objects.create(
                city=city,
                temperature=temp,
                description=desc
            )
            serializer = self.get_serializer(weather)
            return Response(serializer.data)
        else:
            return Response({'error': 'City not found or API error'})
        


from django.shortcuts import render
import requests

def home(request):
    city = request.GET.get('city')
    weather = None
    error = None

    if city:
        url = 'http://127.0.0.1:8000/weather/fetch/'
        params = {'city': city}
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                weather = response.json()
            else:
                error = "City not found or API error."
        except Exception as e:
            error = str(e)

    return render(request, 'weather/home.html', {'weather': weather, 'error': error})