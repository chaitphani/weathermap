from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from datetime import datetime
import requests

from .serializers import (
    WeatherInfoSerializer,
    InputWeatherSerializer,
    InputWeatherForecastSerializer,
)


class WeatherInformationView(APIView):

    '''
    API which gives current weather details of the requested city
    '''
    serializer_class = InputWeatherSerializer
    output_serializer = WeatherInfoSerializer
    app_id = "b0b2a8c6eb68cf455d2b353ed0537b55"

    def post(self, request):

        '''
        the post method takes city as request data
        reads the data in openweather API based on the city
        gives us the required weather data of the entered city.
        '''
        data = self.serializer_class(data=request.data)
        data.is_valid(raise_exception=True)

        requested_city = data.validated_data.get("city")
        request_url = "https://api.openweathermap.org/data/2.5/weather"
        params = {"q": requested_city, "appid": self.app_id, "units": "metric"}

        get_url = requests.get(request_url, params)
        response = get_url.json()

        response_data = {
            "weather_condition": response["weather"][0]["description"],
            "icon": response["weather"][0]["icon"],
            "temperature": response["main"]["temp"],
            "city": response["name"],
        }

        serializer = self.output_serializer(response_data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class WeatherForecastView2(APIView):

    '''
    API which is used to get the weather forecast data of the city
    '''
    serializer_class = InputWeatherSerializer
    app_id = "b0b2a8c6eb68cf455d2b353ed0537b55"

    def post(self, request):
        '''
        the post method takes city as request data
        reads the data in openweather API based on the city
        gives us the required weather forecast data of the entered city.
        '''
        data = self.serializer_class(data=request.data)
        data.is_valid(raise_exception=True)

        requested_city = data.validated_data.get("city")

        request_url = "http://api.openweathermap.org/data/2.5/forecast"
        params = {"q": requested_city, "appid": self.app_id, "units": "metric"}

        get_url = requests.get(request_url, params)
        response = get_url.json()

        one_date = []
        for response in response["list"]:
            only_date = response["dt_txt"].split(" ")[0]
            if only_date not in one_date:
                one_date.append(only_date)
                one_date.append(
                    (
                        response["main"]["temp"],
                        response["weather"][0]["description"],
                        response["weather"][0]["icon"],
                    )
                )

        response_dict = {}
        res_list = [ele for idx, ele in enumerate(one_date) if idx % 2 == 0]
        rem_data_list = [ele for idx, ele in enumerate(one_date) if idx % 2 != 0]
        response_dict = {"date": res_list}
        response_dict["weather"] = rem_data_list
        # response_dict = dict(zip(res_list, rem_data_list))

        return Response(response_dict, status=status.HTTP_200_OK)


class WeatherForecastView(APIView):

    '''
    API which is used to get the weather forecast data of the city
    '''
    serializer_class = InputWeatherForecastSerializer
    api_key = "	Cv7lxQHaIrQguPuYrDuLYFtQehczLXyy"

    def post(self, request):
        '''
        the post method takes city as request data
        reads the data in openweather API based on the city
        gives us the required weather forecast data of the entered city.
        '''
        data = self.serializer_class(data=request.data)
        data.is_valid(raise_exception=True)

        city_from_input = data.validated_data.get("city")
        country_from_input = data.validated_data.get("country")
        city_country = city_from_input + "_" + country_from_input

        request_url = "http://dataservice.accuweather.com/locations/v1/cities/search"
        params = {"q": city_from_input, "apikey": self.api_key}

        get_url = requests.get(request_url, params)
        response = get_url.json()

        try:
            city_key = response[0]["Key"]  # default

            for country in response:
                if country["Country"]["LocalizedName"] == country_from_input:
                    city_key = country["Key"]  # updated

            request_url_1 = (
                f"http://dataservice.accuweather.com/forecasts/v1/daily/5day/{city_key}"
            )
            params = {"apikey": self.api_key, "metric": True}

            get_url = requests.get(request_url_1, params)
            response_1 = get_url.json()

            forecast_data = []
            for response in response_1["DailyForecasts"]:
                forecast_data.append(
                    {
                        "date": response["Date"].split("T")[0],
                        "temp_min": response_1["DailyForecasts"][0]["Temperature"][
                            "Minimum"
                        ]["Value"],
                        "temp_max": response_1["DailyForecasts"][0]["Temperature"][
                            "Maximum"
                        ]["Value"],
                    }
                )

            response_data = {
                "headline_text": response_1["Headline"]["Text"],
                "effective_date": response_1["Headline"]["EffectiveDate"].split("T")[0],
                "end_date": response_1["Headline"]["EndDate"].split("T")[0],
                "place": city_country,
                "forecast": forecast_data,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as error:
            print("error as exception----", error)
            return Response(
                {"error": "apikey expired.!"}, status=status.HTTP_400_BAD_REQUEST
            )


class WeatherForecastView3(APIView):

    '''
    API which is used to get the weather forecast data of the city
    '''
    serializer_class = InputWeatherSerializer
    output_serializer = WeatherInfoSerializer
    app_id = "b0b2a8c6eb68cf455d2b353ed0537b55"

    def post(self, request):
        '''
        the post method takes city as request data
        reads the data in openweather API based on the city
        gives us the required weather forecast data of the entered city.
        '''        
        data = self.serializer_class(data=request.data)
        data.is_valid(raise_exception=True)

        requested_city = data.validated_data.get("city")

        # Current weather details based on the requested city.
        weather_request_url = "https://api.openweathermap.org/data/2.5/weather"
        params = {"q": requested_city, "appid": self.app_id, "units": "metric"}

        response_weather = requests.get(weather_request_url, params).json()
        weather_response_data = {
            "weather_condition": response_weather["weather"][0]["description"],
            "icon": response_weather["weather"][0]["icon"],
            "temperature": response_weather["main"]["temp"],
            "city": response_weather["name"],
        }
        serializer = self.output_serializer(weather_response_data)

        # 5 day forecast details based on the requested city.
        request_url = "http://api.openweathermap.org/data/2.5/forecast"
        response = requests.get(request_url, params).json()

        day = datetime.today()
        today_date = int(day.strftime("%d"))

        forcast_data_list = {}
        for cane in range(0, response["cnt"]):
            date_var1 = response["list"][cane]["dt_txt"]

            date_time_obj1 = datetime.strptime(date_var1, "%Y-%m-%d %H:%M:%S")

            if (
                int(date_time_obj1.strftime("%d")) == today_date
                or int(date_time_obj1.strftime("%d")) == today_date + 1
            ):
                if int(date_time_obj1.strftime("%d")) == today_date + 1:
                    today_date += 1
                forcast_data_list[today_date] = {}
                forcast_data_list[today_date]["day"] = date_time_obj1.strftime("%A")
                forcast_data_list[today_date]["date"] = date_time_obj1.strftime(
                    "%d-%M-%Y"
                )

                forcast_data_list[today_date]["temperature"] = response["list"][cane][
                    "main"
                ]["temp"]

                forcast_data_list[today_date]["description"] = response["list"][cane][
                    "weather"
                ][0]["description"]
                forcast_data_list[today_date]["icon"] = response["list"][cane][
                    "weather"
                ][0]["icon"]

                today_date += 1
            else:
                pass

        context = {
            "weather_response_data": serializer.data,
            "forcast_data_list": forcast_data_list,
        }

        return Response(context, status=status.HTTP_200_OK)
