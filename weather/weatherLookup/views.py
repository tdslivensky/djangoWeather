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

	apiTemperature = requests.get("https://api.weather.gov/gridpoints/EWX/157,96/forecast")
	try:
		api = json.loads(apiTemperature.content)
		api = convert(api)
	except Exception as e:
		api = 'No information returned by api'
	
	temperature = api.properties.periods[0]	
	return render(request, 'Home.html', {'api': api, 'today': temperature})

def about(request):
	return render(request, 'about.html', {})