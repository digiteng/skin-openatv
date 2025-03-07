# -*- coding: utf-8 -*-
# by digiteng...07.2022, 09.2022
# <widget source="session.CurrentService" render="Label" position="55,170" size="400,30" zPosition="1" font="Regular; 22" halign="left" transparent="1" backgroundColor="#206C9D" foregroundColor="fc">
	# <convert type="NachtWeatherOMc">current;update, %city, %desc</convert>
# </widget>
# from __future__ import unicode_literals
from Components.Converter.Converter import Converter
from Components.Element import cached
from enigma import eTimer, addFont
from Tools.NachtWeatherUpdate import checkUpdateWeather, dataRead, runOM, errorlog, py3
from Components.Converter.Poll import Poll
from time import localtime, strftime
addFont("/usr/share/enigma2/Nacht/fonts/meteo.ttf", "meteo", 100, 1)
datajson = "/tmp/Nacht_Weather_OM.json"

class NachtWeatherOMc(Poll, Converter, object):

	def __init__(self, type):
		Converter.__init__(self, type)
		Poll.__init__(self)
		self.type = type
		self.poll_interval = 1000
		self.poll_enabled = True
		self.timer = eTimer()
		self.timer.callback.append(self.runUpdate)

	@cached
	def getText(self):
		try:
			wg = ""
			wtype = "current"
			k = ""
			sep = ""
			inf = ""
			up = self.type.split(";")[0]
			ws = self.type.split(";")[1].split(",")
			if "update" in self.type:
				self.checkUpdate()
			data = dataRead(datajson)
			if data == "N/A":
				return ""
			n = 0
			keys = self.type.split(";")[1]
			keyss = keys.split("%")[1:]
			up = self.type.split(";")[0].split(",")[0]
			ws = self.type.split(";")[1].split(",")

			if "current" in up:
				wtype = "current"
			elif "day" in up:
				wtype = "day_{}".format(up.split("_")[1])
			nl = localtime()
			nc = int(round(float(strftime("%H:%M", nl).replace(":","."))))
			sr = int(round(float(data["day_0"]["sunrise"].replace(":","."))))
			ss = int(round(float(data["day_0"]["sunset"].replace(":","."))))
			ci = data["current"]["icon"]
			ri = ["9", "10", "11", "12", "13"]
			kk = {
			"city":"city",
			"date":"date",
			"desc":"desc",
			"temp":"temp",
			"icon":"icon",
			"sunr":"sunrise",
			"suns":"sunset",
			"tmin":"temp_min",
			"tmax":"temp_max",
			"prec":"precipitation",
			"radi":"radiation",
			"wind":"wind",
			"humi":"humidity",
			"sday":"short_day",
			}
			try:
				for i in keyss:
					k = i[:4]
					kkk = kk[k]
					n += 1
					inf = data[wtype][kkk]
					sep = self.type.split("%")
					sep = sep[n][4:]
					if kkk == "icon":
						if sr < nc < ss:
							desc = ci
						else:
							if ci == "32":
								desc = "31"
							elif ci == "34":
								desc = "33"
							elif ci == "30":
								desc = "29"
							elif ci in ri:
								desc = "45"
							else:
								desc = ci
							inf = desc
					wg += inf + sep
			except:
				pass
			desc = data["current"]["desc"].lower()
			if "backpic" in self.type:
				if "cloudy" in desc or "mainly" in desc:
					backimg = "mcloudy"
				elif desc == "overcast":
					backimg = "cloudyy"
				elif "rain" in desc:
					backimg = "rainy"	
				elif "snow" in desc:
					backimg = "snowy"
				elif "sunny" in desc or "clear" in desc:
					backimg = "sunnyy"
					if int(data["current"]["temp"][:-3]) >= 30:
						backimg = "sun"
				elif "thunderstorms" in desc:
					backimg = "thunderstorms"
				elif "fog" in desc:
					backimg = "foggy"
				else:
					backimg = "weather_today_blue"
				if sr < nc < ss:
					wg = backimg
				else:
					if "clear" in desc:
						backimg = "night"
					elif "cloud" in desc or "overcast" in desc:
						backimg = "cnight"
					wg = backimg
			if py3:
				return wg
			else:
				return wg.encode('utf-8')
		except Exception as err:
			from Tools.NachtWeatherUpdate import errorlog
			errorlog(err, __file__)

	text = property(getText)

	def changed(self, what):
		if what[0] == self.CHANGED_POLL:
			Converter.changed(self, what)

	def runUpdate(self):
		runOM()

	def checkUpdate(self):
		if checkUpdateWeather(datajson) == True:
			self.timer.start(10000, True)
