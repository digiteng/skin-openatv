# -*- coding: utf-8 -*-
# by digiteng...08.2022
# <widget source="session.CurrentService" render="NachtWeatherOMr" mode="day1" position="112,75" size="500,400" zPosition="1" backgroundColor="background" transparent="1" />
from __future__ import absolute_import
from Components.Renderer.Renderer import Renderer
from enigma import ePixmap, ePoint, eWidget, eSize, eLabel, gFont, addFont, eTimer
from Tools.NachtWeatherUpdate import checkUpdateWeather, dataRead, runOM, getmtimedatajson
from skin import parseColor
from time import localtime, strftime
from threading import Thread

addFont("/usr/share/enigma2/Nacht/fonts/meteo.ttf", "meteo", 100, 1)
datajson = "/tmp/Nacht_Weather_OM.json"

class NachtWeatherOM(Renderer):
	def __init__(self):
		Renderer.__init__(self)
		self.timer = eTimer()
		self.timer.callback.append(self.startDown)

	def applySkin(self, desktop, screen):
		attribs = self.skinAttributes[:]
		for attrib, value in self.skinAttributes:
			if attrib == 'backgroundColor':
				self.backgroundColor = value
			elif attrib == 'mode':
				self.mode = value
		self.skinAttributes = attribs

		self.day.setBackgroundColor(parseColor(self.backgroundColor))
		self.day.resize(eSize(500, 500))
		self.day.move(ePoint(10, 100))
		self.day.setFont(gFont("Regular", 24))
		self.day.setHAlign(eLabel.alignLeft)
		self.day.setTransparent(1)
		self.day.setZPosition(1)

		self.day2.setBackgroundColor(parseColor(self.backgroundColor))
		self.day2.resize(eSize(500, 500))
		self.day2.move(ePoint(10, 100))
		self.day2.setFont(gFont("Regular", 26))
		self.day2.setHAlign(eLabel.alignLeft)
		self.day2.setTransparent(1)
		self.day2.setZPosition(1)
		
		self.dayIcon.setTransparent(1)
		self.dayIcon.setAlphatest(2)
		self.dayIcon.setScale(2)
		self.dayIcon.setZPosition(2)

		return Renderer.applySkin(self, desktop, screen)

	GUI_WIDGET = eWidget
	def changed(self, what):
		if not self.instance:
			return
		if what[0] == self.CHANGED_CLEAR:
			return
		Thread(target=self.weatherinfo).start()
		if "update" in self.mode:
			if checkUpdateWeather(datajson) == True:
				self.day.setText("Updating, Wait...")
				self.timer.start(10000, True)

	def weatherinfo(self):
		try:
			data=""
			datajson = "/tmp/Nacht_Weather_OM.json"
			data = dataRead(datajson)
			if data == "N/A":
				return ""
			if "day" in self.mode:
				city = ""
				d = self.mode[3:]
				day = data["day_{}".format(d)]
				
				date = "\n\c0000??80Date : \c00??????{} {}".format(day["date"], day["short_day"])
				info = "\c0000??80Info : \c00??????{}".format(day["desc"])
				temp_min = "\c0000??80Temp Min : \c00??????{} ºC".format(day["temp_min"])
				temp_max = "\c0000??80Temp Max : \c00??????{} ºC".format(day["temp_max"])
				radiation = "\c0000??80Rad : \c00??????{}".format(day["radiation"])
				wind = "\c0000??80Wind : \c00??????{}".format(day["wind"])
				sunrise = "\c0000??80Sunrise : \c00??????{}".format(day["sunrise"])
				sunset = "\c0000??80Sunset : \c00??????{}".format(day["sunset"])
				rain = "\c0000??80Rain : \c00??????{}".format(day["rain_sum"])
				snow = "\c0000??80Snow : \c00??????{}".format(day["snowfall_sum"])
				wi = "\n".join((date, info, temp_min, temp_max, radiation, wind, sunrise, sunset, rain, snow))
				
				self.day.setText(wi)
				# self.day.setNoWrap(1)
				self.day.show()

				wicon = data["day_{}".format(d)]["icon"]
				dicon = "/usr/share/enigma2/Nacht/WeatherIcons/{}.png".format(wicon)
				self.dayIcon.setPixmapFromFile(dicon)
				self.dayIcon.resize(eSize(175, 120))
				self.dayIcon.move(ePoint(0, 0))
				self.dayIcon.show()
			
			elif "current" in self.mode:
				if "temp" in self.mode:
					tempc = int(data["current"]["temp"].split(" ")[0])
					tempColor = "\c00??????"
					if tempc <= -10: 
						tempColor = "\c0000f9??" 
					elif tempc <= 0: 
						tempColor = "\c0000????" 
					elif tempc <= 10:
						tempColor = "\c0000??00" 
					elif tempc <= 22:
						tempColor = "\c00ff??00" 
					elif tempc <= 29:
						tempColor = "\c00????00" 
					elif tempc >= 30:
						tempColor = "\c00??0000"
					self.day.setText("{}{}°".format(tempc, tempColor))
					self.day.setForegroundColor(parseColor("#00ffffff"))
					self.day.setFont(gFont("meteo", 80))
					self.day.resize(eSize(250, 80))
					self.day.move(ePoint(0, 60))
					self.day.setHAlign(eLabel.alignLeft)
					self.day.show()

					nl = localtime()
					nc = int(round(float(strftime("%H:%M", nl).replace(":","."))))
					sr = int(round(float(data["day_0"]["sunrise"].replace(":","."))))
					ss = int(round(float(data["day_0"]["sunset"].replace(":","."))))
					ci = data["current"]["icon"]
					ri = ["9", "10", "11", "12", "13"]
					if sr < nc < ss:
						curicon = "/usr/share/enigma2/Nacht/WeatherIcons/{}.png".format(ci)
					else:
						if ci == "32":
							cur_icon = "31"
						elif ci == "34":
							cur_icon = "33"
						elif ci == "30":
							cur_icon = "29"
						elif ci in ri:
							cur_icon = "45"
						else:
							cur_icon = ci
						curicon = "/usr/share/enigma2/Nacht/WeatherIcons/{}.png".format(cur_icon)
					self.dayIcon.setPixmapFromFile(curicon)
					self.dayIcon.resize(eSize(175, 120))
					self.dayIcon.move(ePoint(400, 40))
					self.dayIcon.show()


				else:
					city = "\c0000??80City : \c00??????{}".format(data["current"]["city"])
					elev = "\c0000??80Elevation : \c00??????{}".format(data["current"]["elevation"])
					date = "\c0000??80Date : \c00??????{}".format(data["current"]["date"])
					info = "\c0000??80Info : \c00??????{}".format(data["current"]["desc"])
					wind = "\c0000??80Wind : \c00??????{}".format(data["current"]["wind"])
					humi = "\c0000??80Humidity: \c00??????{}".format(data["current"]["humidity"])
					press = "\c0000??80Pressure : \c00??????{}".format(data["current"]["pressure"])
					rain = "\c0000??80Rain : \c00??????{}".format(data["current"]["rain"])
					snowfall = "\c0000??80Snow : \c00??????{}".format(data["current"]["snowfall"])
					cloud = "\c0000??80Cloud : \c00??????{}".format(data["current"]["cloud"])

					wi = "\n".join((city, elev, date, info, wind, humi, press, rain, snowfall, cloud))
					self.day2.setText(wi)
					# self.day.setNoWrap(1)
					self.day2.show()				

			if "getUpdateInfo" in self.mode:
				last_update = "https://open-meteo.com \c0000??80 \c00??????{}".format(getmtimedatajson(datajson))
				self.day.setText(str(last_update))
				self.day.setFont(gFont("meteo", 24))
				self.day.resize(eSize(1000, 40))
				self.day.move(ePoint(0, 0))
				self.day.show()
		except Exception as err:
			from Tools.NachtWeatherUpdate import errorlog
			errorlog(err, __file__)

	def startDown(self):
		runOM()

	def GUIcreate(self, parent):
		self.instance = eWidget(parent)
		self.day = eLabel(self.instance)
		self.day2 = eLabel(self.instance)
		self.dayIcon = ePixmap(self.instance)

	def GUIdelete(self):
		self.day = None
		self.day2 = None
		self.dayIcon = None
