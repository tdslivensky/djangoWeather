from django.shortcuts import render

# Create your views here.
def Home(request):
	import json 
	import requests
	#https://stackoverflow.com/questions/42658285/convert-bool-values-to-string-in-json-dumps
	def convert(obj):
	    if isinstance(obj, bool) or obj == None:
	    	if obj == None:
	    		obj = 'null'
	    	return str(obj).lower()
	    if isinstance(obj, (list, tuple)):
	        return [convert(item) for item in obj]
	    if isinstance(obj, dict):
	        return {convert(key):convert(value) for key, value in obj.items()}
	    return obj

	totalWeather = requests.get("https://api.weather.gov/points/30.4036,-97.701")
	
	try:
		apiTotalWeather = json.loads(totalWeather.json())
		apiTotalWeather = convert(apiTotalWeather)
	except Exception as e:
		apiTotalWeather = 'No information returned by apiTotalWeather'
		
	forecast = requests.get(apiTotalWeather.properties.forecast)
	hourlyForecast =  requests.get(apiTotalWeather.properties.forecastHourly)
	try:
		apiForecast = json.loads(forecast.content)
		apiForecast = convert(apiForecast)
	except Exception as e:	
		apiForecast = 'No information returned by apiForecast'
		
	try:
		apiHourlyForcast = json.loads(hourlyForecast.content)
		apiHourlyForcast = convert(apiHourlyForcast)
	except Exception as e:	
		apiHourlyForcast = 'No information returned by apiHourlyForcast'	
		
	return render(request, 'Home.html', {'totalWeather': apiTotalWeather, 'forecast': apiForecast, 'hourlyForecast': apiHourlyForcast})

def about(request):
	return render(request, 'about.html', {})