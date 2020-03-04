from django.shortcuts import render

# Create your views here.
def Home(request):
	import json 
	import requests
	totalWeather = requests.get("https://api.weather.gov/points/30.4036,-97.701")
	
	try:
		apiTotalWeather = totalWeather.json()
	except Exception as e:
		apiTotalWeather = 'No information returned by apiTotalWeather'

	forecast = requests.get(apiTotalWeather["properties"]["forecast"])
	hourlyForecast =  requests.get(apiTotalWeather["properties"]["forecastHourly"])
	apiTotalWeather = json.dumps(apiTotalWeather)
	
	try:
		apiForecast = forecast.json()
		apiForecast = json.dumps(apiForecast)
	except Exception as e:
		apiForecast = 'No information returned by apiForecast'
		
	try:
		apiHourlyForcast = hourlyForecast.json()
		apiHourlyForcast = json.dumps(apiHourlyForcast)
	except Exception as e:
		apiHourlyForcast = 'No information returned by apiHourlyForcast'	
	
	return render(request, 'Home.html', {'totalWeather': apiTotalWeather, 'forecast': apiForecast, 'hourlyForecast': apiHourlyForcast})

def about(request):
	return render(request, 'about.html', {})