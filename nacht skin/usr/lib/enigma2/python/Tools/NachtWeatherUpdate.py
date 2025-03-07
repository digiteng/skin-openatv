# -*- coding: utf-8 -*-
# by digiteng...08.2022
import os, socket, json, io, re
from enigma import eTimer
import requests
from time import time, localtime, strftime
from datetime import datetime
from PIL import Image, ImageDraw, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
from sys import version_info
header = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
py3 = version_info[0] == 3
try:
	if py3:
		from _thread import start_new_thread
		from urllib.request import urlopen, Request, quote
	else:
		from thread import start_new_thread
		from urllib2 import urlopen, Request, quote
except:
	pass
from threading import Thread
wini = "/etc/enigma2/NachtWeather.ini"

def cleanRam():
	os.system("echo 1 > /proc/sys/vm/drop_caches")
	os.system("echo 2 > /proc/sys/vm/drop_caches")
	os.system("echo 3 > /proc/sys/vm/drop_caches")

# def errorlog(err, __file__):
	# import sys
	# nt = localtime()
	# tm = '{:02d}:{:02d}:{:02d}'.format(nt.tm_hour, nt.tm_min, nt.tm_sec)
	# with open("/tmp/Nacht.log", "a+") as f:
		# f.write("NachtWeatherUpdate(Tools) ({}), {}, line:{}\n".format(tm, err, sys.exc_info()[2].tb_lineno))

def errorlog(err, filex):
	tm = strftime("%Y-%m-%d %H:%M:%S")
	with open("/tmp/Nacht.log", "a+") as f:
		f.write("File : {}, {}, \nERROR:{}, \nLine:{}\n\n".format(filex, tm, err, err.__traceback__.tb_lineno))


def mt(datajson):
	if os.path.exists(datajson):
		os.path.getmtime(datajson)
		
def getmtimedatajson(datajson):
	try:
		if os.path.exists(datajson):
			ct = strftime("%d/%m/%Y, %H:%M", localtime(mt(datajson)))
			return ct
	except Exception as err:
		errorlog(err, __file__)

def winfo():
	winid = {}
	if os.path.exists(wini):
		with open(wini) as f:
			for i in f:
				(key, value) = i.split("=")
				winid[key.strip()] = value.strip()
		return winid

lat = winfo()["lat"]
lon = winfo()["lon"]
# API_key = winfo()["OpenWeatherMap_API_KEY"]
lang = winfo()["language"]
city = winfo()["city"]

def dataRead(datajson):
	jdata = "N/A"
	try:
		if os.path.exists(datajson):
			with io.open(datajson, encoding="utf-8") as f:
				jdata = json.load(f)
		return jdata
	except:
		return jdata

def intCheck():
	try:
		socket.setdefaulttimeout(3)
		socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
		return True
	except Exception as err:
		errorlog(err, __file__)
		return False

def checkUpdateWeather(datajson):
	try:
		if os.path.exists(datajson):
			# return False
			nd = int(strftime('%d', localtime(time())))
			nc = int(strftime('%H', localtime(time())))
			fd = int(strftime('%d', localtime(os.path.getmtime(datajson))))
			fc = int(strftime('%H', localtime(os.path.getmtime(datajson))))
			if nd > fd: 
				return True
			elif nd == fd and nc - fc >= int(winfo()["refreshPeriod"]):
				return True
			else:
				return False
		else:
			return True
	except:
		return True

def runWG():
	start_new_thread(downloadWG, ())

def downloadWG():
	datajson = "/tmp/Nacht_WG.json"
	try:
		if intCheck():
			headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
			url = "https://www.google.com/search?q=weather%20in%20{}&newwindow=1&hl={}".format(quote(winfo()["city"].replace(",","")), winfo()["language"])
			data = urlopen(Request(url, None, headers=headers)).read().decode("utf-8")
			days={}
			cur={
			"current":{
			"city" : re.findall('class="BBwThe">(.*?)</span>', data)[0],
			"daytime" : re.findall('id="wob_dts">(.*?)</div>', data)[0],
			"desc" : re.findall('id="wob_dc">(.*?)</span>', data)[0],
			"tempC" : "%s"% (re.findall('id="wob_tm" style="display:inline">(.*?)</span>', data)[0]),
			"tempF" : "%s"% (re.findall('class="wob_t" id="wob_ttm" style="display:none">(.*?)</span></div><div', data)[0]),
			"humidity" : re.findall('<span id="wob_hm">(.*?)</span>', data)[0],
			"rainfall" : re.findall('<span id="wob_pp">(.*?)</span>', data)[0],
			"windC" : re.findall('id="wob_ws">(.*?)</span>', data)[0],
			"windF" : re.findall('id="wob_tws">(.*?)</span>', data)[0],
			# "icon" : str(data.partition('src="//ssl.gstatic.com/onebox/weather/64/')[2].partition('" id="wob_tci">')[0])[:-4]
			"icon" : re.findall('ssl.gstatic.com/onebox/weather/64/(.*?).png', data)[0],
			}}
			days.update(cur)
			n = 0
			for i in range(0,7,1):
				day = re.findall('class="Z1VzSb" aria-label="(.*?)">(.*?)</div>', data)[i] #('Friday', 'Fri')
				# desc_icon = re.findall('class="uW5pk" alt="(.*?)" src="(.*?)"></div><div', data)[i]
				# desc = desc_icon[0]
				# icon = desc_icon[1].split("/")[-1]
				temp_maxC = re.findall('class="wob_t" style="display:inline">(.*?)</span>', data)[n]
				temp_minC = re.findall('class="wob_t" style="display:inline">(.*?)</span>', data)[n+1]
				temp_maxF = re.findall('class="wob_t" style="display:none">(.*?)</span>', data)[n]
				temp_minF = re.findall('class="wob_t" style="display:none">(.*?)</span>', data)[n+1]
				n += 2
				dy = {
				"day_%s"%i : { 
							"day" : "%s"%day[0],
							"shortday" : "%s"%day[1], 
							"temp_maxC" : "%s"%temp_maxC, 
							"temp_minC"	: "%s"%temp_minC, 
							"temp_maxF" : "%s"%temp_maxF, 
							"temp_minF"	: "%s"%temp_minF, 
							}}
				days.update(dy)
			with open(datajson, "w") as f:
				f.write(json.dumps(days))
	except Exception as err:
		errorlog(err, __file__)

def runOM():
	start_new_thread(downloadOM, ())

om = {}

class downloadOM():
	
	def __init__(self):
		self.download()

	def download(self):
		try:
			url="https://api.open-meteo.com/v1/forecast?latitude={}&longitude={}&current=temperature_2m,relative_humidity_2m,apparent_temperature,is_day,precipitation,rain,showers,snowfall,weather_code,cloud_cover,pressure_msl,surface_pressure,wind_speed_10m,wind_direction_10m,wind_gusts_10m&daily=weather_code,temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,sunrise,sunset,daylight_duration,sunshine_duration,uv_index_max,uv_index_clear_sky_max,precipitation_sum,rain_sum,showers_sum,snowfall_sum,precipitation_hours,precipitation_probability_max,wind_speed_10m_max,wind_gusts_10m_max,wind_direction_10m_dominant,shortwave_radiation_sum,et0_fao_evapotranspiration&timezone=auto".format(lat, lon)
			data = json.load(urlopen(url))
			# with open(datajson, "w") as f:
				# f.write(json.dumps(data))
			# if os.path.exists(datajson):
				# with open(datajson) as f:
					# data = json.load(f)
			self.setDataCurrent(data)
		except Exception as err:
			errorlog(err, __file__)
			
	def getWind(self, data, wd, i=None, h=None):
		try:
			wind = ""
			if 0 <= wd <= 22 or 338 <= wd <= 360:
				dr = "N"
			elif 23 <= wd <= 68:
				dr = "NE"
			elif 69 <= wd <= 114:
				dr = "E"
			elif 115 <= wd <= 160:
				dr = "SE"
			elif 161 <= wd <= 206:
				dr = "S"
			elif 207 <= wd <= 255:
				dr = "SW"
			elif 256 <= wd <= 300:
				dr = "W"
			elif 301 <= wd <= 346:
				dr = "NW"
			else:
				dr = ""
			if i is not None:
				if h is not None:
					wind = "{} {} {}".format(data["hourly"]["wind_speed_10m"][i], data["hourly_units"]["wind_speed_10m_max"], dr)
				else:
					wind = "{} {} {}".format(data["daily"]["wind_speed_10m_max"][i], data["daily_units"]["wind_speed_10m_max"], dr)
			else:
				wind = "{} {} {}".format(data["current"]["wind_speed_10m"], data["current_units"]["wind_speed_10m"], dr)
			return wind
		except Exception as err:
			errorlog(err, __file__)
			
	def desc_icon(self,	 weathercode):
		try:
			desc = ""
			icon = ""
			if weathercode == 0:
				desc = "Clear sky"
				icon="32"
			elif weathercode == 1:
				desc = "Mainly clear"
				icon="34"
			elif weathercode == 2:
				desc = "partly cloudy"
				icon="30"
			elif weathercode == 3:
				desc = "overcast"
				icon="26"
			elif 45 <= weathercode <= 48:
				desc = "Fog"
				icon="20"
			elif 51 <= weathercode <= 55:
				desc = "Drizzle"
				icon="9"
			elif 56 <= weathercode <= 57:
				desc = "Freezing Drizzle"
				icon="10"
			elif  weathercode <= 61:
				desc = "Rain, Slight"
				icon="9"
			elif  weathercode <= 63:
				desc = "Rain, Moderate"
				icon="11"
			elif  weathercode <= 65:
				desc = "Rain, Heavy"
				icon="12"
			elif weathercode <= 71:
				desc = "Snow, Slight"
				icon="13"
			elif weathercode <= 73:
				desc = "Snow, Moderate"
				icon="14"
			elif weathercode <= 75:
				desc = "Snow, Heavy"
				icon="16"
			elif weathercode == 77:
				desc = "Snow grains"
				icon="15"
			elif 80 <= weathercode <= 82:
				desc = "Rain showers"
				icon="12"
			elif 85 <= weathercode <= 86:
				desc = "Snow showers"
				icon="14"
			elif weathercode == 95:
				desc = "Thunderstorm"
				icon="0"
			elif 96 <= weathercode <= 99:
				desc = "Thunderstorm with slight"
				icon="17"
			return desc, icon
		except Exception as err:
			errorlog(err, __file__)
# current ##########################################################################################


	def setDataCurrent(self, data):
		try:
			
			weathercode = data["current"]["weather_code"]
			wd = data["current"]["wind_direction_10m"]
			getDate = data["current"]["time"].replace("T", " ").split(" ")[0]
			year=getDate.split("-")[0]
			month=getDate.split("-")[1].split()[0]
			day=getDate.split("-")[2].split()[0]
			getDay = datetime(int(year), int(month), int(day))
			getDay = getDay.strftime("%a, %A").split(",")
			cur={
			"current":{
			"city" : "{}".format(winfo()["city"]),
			"elevation" : "{} m".format(data["elevation"]),
			"date" : "{}".format(getDate),
			"day" : "{}".format(getDay[1]),
			"short_day" : "{}".format(getDay[0]),
			"temp" : "{} {}".format(int(round(data["current"]["temperature_2m"])), data["daily_units"]["temperature_2m_min"]),
			"wind" : "{}".format(self.getWind(data, wd, i=None)),
			"desc" : "{}".format(self.desc_icon(weathercode)[0]),
			"icon" : "{}".format(self.desc_icon(weathercode)[1]),
			"humidity" : "{} %".format(data["current"]["relative_humidity_2m"]),
			"pressure" : "{} hPa".format(data["current"]["surface_pressure"]),
			"precipitation" : "{} mm".format(data["current"]["precipitation"]),
			"rain" : "{} mm".format(data["current"]["rain"]),
			"snowfall" : "{} cm".format(data["current"]["snowfall"]),
			"cloud" : "{} %".format(data["current"]["cloud_cover"]),
			}}
			om.update(cur)
			cur.clear()
			
			self.setDataDaily(data)
		except Exception as err:
			errorlog(err, __file__)

# Daily ##########################################################################################

	def setDataDaily(self, data):
		try:
			for i in range(7):
				wd = data["daily"]["wind_speed_10m_max"][i]
				weathercode = data["daily"]["weather_code"][i]
				getDate = str(data["daily"]["time"][i])
				year=getDate.split("-")[0]
				month=getDate.split("-")[1].split()[0]
				day=getDate.split("-")[2].split()[0]
				getDay = datetime(int(year), int(month), int(day))
				getDay = getDay.strftime("%a, %A").split(",")
				tmin = int(round(data["daily"]["temperature_2m_min"][i]))
				tmax = int(round(data["daily"]["temperature_2m_max"][i]))
				tavg = (tmin + tmax) // 2
				days={
				"day_%s"%i : {
				"date" : "{}".format(getDate), 
				"day" : "{}".format(getDay[1]),
				"short_day" : "{}".format(getDay[0]),
				"sunrise" : "{}".format(data["daily"]["sunrise"][i].split("T")[1]),
				"sunset" : "{}".format(data["daily"]["sunset"][i].split("T")[1]),
				"temp_min" : "{}".format(tmin),
				"temp_max" : "{}".format(tmax),
				"temp":"{}º".format(tavg),
				"weathercode" : "{}".format(data["daily"]["weather_code"][i]),
				"rain_sum": "{} {}".format(data["daily"]["rain_sum"][i],	 data["daily_units"]["rain_sum"]),
				"snowfall_sum": "{} {}".format(data["daily"]["snowfall_sum"][i],	 data["daily_units"]["snowfall_sum"]),
				"radiation" : "{} {}".format(data["daily"]["shortwave_radiation_sum"][i], data["daily_units"]["shortwave_radiation_sum"]),
				"wind" : "{}".format(self.getWind(data, wd, i)),
				"desc" : "{}".format(self.desc_icon(weathercode)[0]),
				"icon" : "{}".format(self.desc_icon(weathercode)[1]),
				}}
				om.update(days)
				days.clear()
			# self.setDataHourly(data)
			with open("/tmp/Nacht_Weather_OM.json", "w") as f:
				f.write(json.dumps(om))
			del data
			om.clear()
		except Exception as err:
			errorlog(err, __file__)
# hourly ######################################################################################################

	# def setDataHourly(self, data):
		# try:
			# h = True
			# hourly_units =  data["hourly_units"]
			# for i in range(168):
				# wd=None
				# wd = data["hourly"]["windspeed_10m"][i]
				# hours={
				# "{}".format(data["hourly"]["time"][i][:-3]) : {
				# "temp" : str(round(data["hourly"]["temperature_2m"][i])) + " " + hourly_units["temperature_2m"],
				# "hum" : str(data["hourly"]["relativehumidity_2m"][i]) + " " + hourly_units["relativehumidity_2m"],
				# "pres" : str(data["hourly"]["surface_pressure"][i]) + " " + hourly_units["surface_pressure"],
				# "prec" : str(data["hourly"]["precipitation"][i]) + " " + hourly_units["precipitation"],
				# "icon" : str(data["hourly"]["weathercode"][i]),
				# "snwd" : str(data["hourly"]["snow_depth"][i]) + " " + hourly_units["snow_depth"],
				# "cloud" : str(data["hourly"]["cloudcover"][i]) + " " + hourly_units["cloudcover"],
				# "rad" : str(data["hourly"]["direct_radiation"][i]) + " " + hourly_units["direct_radiation"],
				# "wind" : "{}".format(self.getWind(data, wd, i, h)),
				# "soilt" : str(data["hourly"]["soil_temperature_0cm"][i]) + " " + hourly_units["soil_temperature_0cm"],
				# "soilm" : str(data["hourly"]["soil_moisture_0_1cm"][i]) + " " + hourly_units["soil_moisture_0_1cm"],
				# }}
				# om.update(hours)

		# except Exception as err:
			# errorlog(err, __file__)


	# def setJson(self, om):
		# datajson = "/tmp/open-meteo.json"
		# with open("/tmp/Nacht_Weather_OM.json", "w") as f:
			# f.write(json.dumps(om))

def runOWM():
	start_new_thread(downloadOWM, ())

def downloadOWM():
	try:
		if intCheck():
			url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_key}"
			data_air = json.loads(urlopen(url).read())["list"][0]["main"]["aqi"]

			if data_air == 1:
				aqi = "Good"
			elif data_air == 2:
				aqi = "Fair"
			elif data_air == 3:
				aqi = "Moderate"
			elif data_air == 4:
				aqi = "Poor"
			elif data_air == 5:
				aqi = "Very Poor"
			else:
				aqi = "N/A"

			data={}
			# https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API key}
			url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}&units=metric&lang={lang}"
			data = requests.get(url, stream=True, allow_redirects=True, headers=header).json()

			data["main"]["aqi"] = aqi
			data["main"]["loc"] = city
			datajson = "/tmp/Nacht_OWM.json"
			with open(datajson, "w") as f:
				f.write(json.dumps(data, ensure_ascii=False))

			img = "/tmp/Nacht_OWM.jpg"
			url = f'https://api.accuweather.com/maps/v1/radar/static/globalSIR/tile?apikey=de13920f574d420984d3080b1fa6132b&zoom=4&lat={lat}&lon={lon}&imgwidth=600&imgheight=337&language=en&base_data=radar'

			with open(img, 'wb') as f:
				f.write(urlopen(url, timeout=20).read())
		
	except Exception as err:
		errorlog(err, __file__)

def downloadISS():
	try:
		issimg = "/tmp/Nacht_isspos.png"
		datajson = "/tmp/Nacht_ISS.json"

		url1="http://www.heavens-above.com/orbitdisplay.aspx?icon=iss&width=750&height=750&satid=25544"
		url2="http://api.open-notify.org/astros.json"

		data1 = urlopen(url1).read()
		with open(issimg, 'wb') as f:
			f.write(data1)

		data2 = json.load(urlopen(url2))
		with open(datajson, "w") as f:
			f.write(json.dumps(data2))
	except Exception as err:
		errorlog(err, __file__)

def removeBackground():
	try:
		issimg = "/tmp/Nacht_isspos.png"
		if os.path.exists(issimg):
			image = Image.open(issimg)
			image = image.convert('RGBA')
			newImage = []
			for item in image.getdata():
				if item[:3] == (0, 0, 0):
					newImage.append((255, 255, 255, 0))
				else:
					newImage.append(item)
			image.putdata(newImage)
			image.save(issimg)
	except Exception as err:
		errorlog(err, __file__)

def runISS():
	t1 = Thread(target=downloadISS)
	t1.start()
	t1.join()

	t2 = Thread(target=removeBackground)
	t2.start()
	# t2.join()
	

def runTutiempo():
	start_new_thread(downloadTutiempo, ())

def downloadTutiempo():
	if intCheck():
		datajson = "/tmp/Nacht_Weather_Tutiempo.json"
		url = 'https://api.tutiempo.net/json/?lan={}&apid={}&ll={},{}'.format(winfo()["language"], winfo()["Tutiempo_API_KEY"], lat, lon)
		with open(datajson, 'wb') as f:
			f.write(urlopen(url).read())

	
	
	