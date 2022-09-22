from rest_framework import serializers

class WeatherInfoSerializer(serializers.Serializer):

    weather_condition = serializers.CharField(max_length=60)
    icon = serializers.CharField(max_length=10)
    temperature = serializers.FloatField()
    city = serializers.CharField(max_length=60)


class InputWeatherSerializer(serializers.Serializer):

    city = serializers.CharField(max_length=60, required=True)

class InputWeatherForecastSerializer(serializers.Serializer):

    city = serializers.CharField(max_length=60, required=True)
    country = serializers.CharField(max_length=60, required=True)

