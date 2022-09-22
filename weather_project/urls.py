from django.contrib import admin
from django.urls import path, include
from weather_app import views


urlpatterns = [

    path('admin/', admin.site.urls),

    path('weather/', views.WeatherInformationView.as_view(), name='weather'),
    path('forecast/', views.WeatherForecastView.as_view(), name='forecast'),
    path('forecast/1/', views.WeatherForecastView2.as_view(), name='forecast1'),
    path('forecast/3/', views.WeatherForecastView3.as_view(), name='forecast2'),

    path('api-auth/', include('rest_framework.urls'))
]
