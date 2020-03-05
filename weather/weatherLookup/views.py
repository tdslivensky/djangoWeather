from django.shortcuts import render
# pip install uszipcode
from uszipcode import Zipcode, SearchEngine, SimpleZipcode

# Create your views here.
def Home(request):
	import json 
	import requests
	
	search = SearchEngine()
	
	if request.method == "POST":
		#reference website for zip finder: https://pypi.org/project/uszipcode/
		#other reference for zip finder: https://uszipcode.readthedocs.io/01-Tutorial/index.html#basic-search
		
		formZip = request.POST['zipCode']
		
		if formZip == "":
			zipCodeRawInformation = search.by_zipcode('78758')
			zipCode =  zipCodeRawInformation.to_dict()
		else:
			zipCodeRawInformation = search.by_zipcode(request.POST['zipCode'])
			zipCode =  zipCodeRawInformation.to_dict()	
		
		latitude = zipCode["lat"]
		longitude = zipCode["lng"]
		
		try:
			totalWeather = requests.get("https://api.weather.gov/points/{0},{1}".format(latitude,longitude))
			#convert the api data which is in a request object to python dict https://stackoverflow.com/questions/48934100/how-to-convert-request-data-to-dict
			apiTotalWeather = totalWeather.json()
		except Exception as e:
			apiTotalWeather = "No information returned by apiTotalWeather"
				
		try:
			#make api request for general forecast
			forecast = requests.get(apiTotalWeather["properties"]["forecast"])
			apiForecast = forecast.json()
		except Exception as f:
			apiForecast = "No information returned by apiForecast"
			
		try:
			#make api request for hourly forecast
			hourlyForecast =  requests.get(apiTotalWeather["properties"]["forecastHourly"])
			apiHourlyForcast = hourlyForecast.json()
		except Exception as g:
			apiHourlyForcast = "No information returned by apiHourlyForcast"
		
		#dump python dict back to json data
		apiHourlyForcast = json.dumps(apiHourlyForcast)
		apiForecast = json.dumps(apiForecast)
		apiTotalWeather = json.dumps(apiTotalWeather)	
		
		return render(request, 'Home.html', {'totalWeather': apiTotalWeather, 'forecast': apiForecast, 'hourlyForecast': apiHourlyForcast})
	else:
		#Make the API request for austin default
		totalWeather = requests.get("https://api.weather.gov/points/30.4036,-97.701")
		
		try:
			#convert the api data to python dict
			apiTotalWeather = totalWeather.json()
		except Exception as e:
			apiTotalWeather = 'No information returned by apiTotalWeather'
		
		#make api request for general forecast
		forecast = requests.get(apiTotalWeather["properties"]["forecast"])
		#make api request for hourly forecast
		hourlyForecast =  requests.get(apiTotalWeather["properties"]["forecastHourly"])
		
		#dump python dict back to json data
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