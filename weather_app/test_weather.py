from rest_framework.test import APITestCase
from django.urls import reverse


class WeatherViewTestCases(APITestCase):

    url = reverse("weather")

    def test_weather_view_call_with_no_data(self):

        response = self.client.post(self.url)
        self.assertEqual(400, response.status_code)

    def test_weather_view_call_wrong_method(self):

        response = self.client.get(self.url)
        self.assertEqual(405, response.status_code)

    def test_weather_view_call(self):

        response = self.client.post(self.url, data={'city':'hyderabad'})
        self.assertEqual(200, response.status_code)


class ForecastViewTestCases(APITestCase):

    url = reverse("forecast")

    def test_forecast_view_call_with_no_data(self):

        response = self.client.post(self.url)
        self.assertEqual(400, response.status_code)

    def test_forecast_view_call_wrong_method(self):

        response = self.client.get(self.url)
        self.assertEqual(405, response.status_code)

    def test_forecast_view_call(self):

        response = self.client.post(self.url, {'city':'hyderabad', 'country':'india'})
        self.assertEqual(200, response.status_code)


class Forecast1ViewTestCase(APITestCase):

    url = reverse("forecast1")

    def test_forecast1_view_call_with_no_data(self):

        response = self.client.post(self.url)
        self.assertEqual(400, response.status_code)

    def test_forecast1_view_call_wrong_method(self):

        response = self.client.get(self.url)
        self.assertEqual(405, response.status_code)

    def test_forecast1_view_call(self):

        response = self.client.post(self.url, {'city':'hyderabad', 'country':'india'})
        self.assertEqual(200, response.status_code)


class Forecast2ViewTestCase(APITestCase):

    url = reverse("forecast2")

    def test_forecast2_view_call_with_no_data(self):

        response = self.client.post(self.url)
        self.assertEqual(400, response.status_code)

    def test_forecast2_view_call_wrong_method(self):

        response = self.client.get(self.url)
        self.assertEqual(405, response.status_code)

    def test_forecast2_view_call(self):

        response = self.client.post(self.url, {'city':'hyderabad', 'country':'india'})
        self.assertEqual(200, response.status_code)
