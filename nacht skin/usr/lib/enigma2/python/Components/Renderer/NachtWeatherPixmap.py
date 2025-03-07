# -*- coding: utf-8 -*-
# by digiteng...08.2022, 03.2025(added animation icon)
# <widget source="session.CurrentService" render="NachtWeatherPixmap" path="/usr/share/enigma2/Nacht/Weather_Google_Icons/" position="0,0" size="64,64" zPosition="2" transparent="1" alphatest="blend" >
	# <convert type="NachtWeatherGooglec">current;icon_name</convert>
# </widget>
from __future__ import absolute_import
from Components.Renderer.Renderer import Renderer
from enigma import ePixmap, eTimer
from Tools.NachtWeatherUpdate import errorlog
import os
import json

class NachtWeatherPixmap(Renderer):

	def __init__(self):
		Renderer.__init__(self)
		self.path = "/usr/share/enigma2/Nacht/WeatherIcons/"
		self.pathAnim = "/usr/share/enigma2/Nacht/animated_weather_icons/"
		self.x = 0
		self.mode = "n/a"
		
	def applySkin(self, desktop, parent):
		attribs = self.skinAttributes[:]
		for attrib, value in self.skinAttributes:
			if attrib == 'path':
				self.path = value
			elif attrib == 'mode':
				self.mode = value
		self.skinAttributes = attribs
		ret = Renderer.applySkin(self, desktop, parent)

	GUI_WIDGET = ePixmap
	def changed(self, what):
		if not self.instance:
			return
		if what[0] == self.CHANGED_CLEAR:
			return
		if "animation" in self.mode:
			self.anim()
		else:
			try:
				icon_name = "na"
				icon_name = self.source.text
				if icon_name == "cloudy":
					icon_name = "26"
				elif icon_name == "cloudy_s_rain":
					icon_name =	"11"
				elif icon_name == "cloudy_s_sunny":
					icon_name = "34"
				elif icon_name == "cloudy_t_rain":
					icon_name = "30"
				elif icon_name == "fog":
					icon_name = "20"
				elif icon_name == "partly_cloudy":
					icon_name = "30"
				elif icon_name == "rain":
					icon_name = "12"
				elif icon_name == "rain_heavy":
					icon_name = "12"
				elif icon_name == "rain_light":
					icon_name = "9"
				elif icon_name == "rain_s_cloudy":
					icon_name = "9"
				elif icon_name == "rain_s_sunny":
					icon_name = "39"
				elif icon_name == "rain_t_sunny":
					icon_name = "37"
				elif icon_name == "sleet":
					icon_name = "7"
				elif icon_name == "snow":
					icon_name = "14"
				elif icon_name == "snow_heavy":
					icon_name = "42"
				elif icon_name == "snow_light":
					icon_name = "41"
				elif icon_name == "snow_s_sunny":
					icon_name = "41"
				elif icon_name == "snow_t_sunny":
					icon_name = "42"
				elif icon_name == "sunny":
					icon_name = "32"
				elif icon_name == "sunny_s_cloudy":
					icon_name = "34"
				elif icon_name == "sunny_s_rain":
					icon_name = "39"
				elif icon_name == "sunny_s_snow":
					icon_name = "41"
				elif icon_name == "sunny_t_cloudy":
					icon_name = "37"
				elif icon_name == "sunny_t_snow":
					icon_name = "41"
				elif icon_name == "thunderstorms":
					icon_name = "17"

				self.instance.setPixmapFromFile("{}{}.png".format(self.path, icon_name))
				self.instance.setScale(2)
				self.instance.setAlphatest(2)
				self.instance.show()
			except Exception as err:
				from Tools.NachtWeatherUpdate import errorlog
				errorlog(err, __file__)

	def anim(self):
		try:
			icon_id = ""
			weath_json = "/tmp/Nacht_Weather_OM.json"
			if os.path.exists(weath_json):
				with open(weath_json) as f:
					read_json = json.load(f)
				try:
					icon_id = read_json["current"]["icon"]
				except: return
			if self.pathAnim:
				self.list_size = len(os.listdir("{}{}".format(self.pathAnim, icon_id)))
				self.x = self.list_size
				self.icons = []
				for n in range(self.x):
					self.icons.append("{}{}/a{}.png".format(self.pathAnim, icon_id, n))
				self.animtimer = eTimer()
				self.animtimer.callback.append(self.showanim)
				self.showanim()

		except Exception as err:
			from Tools.NachtWeatherUpdate import errorlog
			errorlog(err, __file__)

	def showanim(self):
		try:
			if self.x == 0:
				self.x = self.list_size
			self.animtimer.stop()
			self.instance.setPixmapFromFile(self.icons[self.x - 1])
			# self.instance.resize(eSize(128, 128))
			self.instance.show()
			self.x -= 1
			self.animtimer.start(100, True)
		except Exception as err:
			from Tools.NachtWeatherUpdate import errorlog
			errorlog(err, __file__)

