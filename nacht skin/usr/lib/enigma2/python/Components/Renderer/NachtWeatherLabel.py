# -*- coding: utf-8 -*-
# by digiteng...08.2022
from __future__ import absolute_import
from Components.VariableText import VariableText
from enigma import eLabel, eEPGCache, addFont
from Components.Renderer.Renderer import Renderer
addFont("/usr/share/enigma2/Nacht/fonts/meteo.ttf", "meteo", 100, 1)

class NachtWeatherLabel(Renderer, VariableText):
	def __init__(self):
		Renderer.__init__(self)
		VariableText.__init__(self)
		
	GUI_WIDGET = eLabel
	def changed(self, what):
		icon_font="N/A"
		txt = self.source.text
		txt = str(txt)
		if txt == "cloudy":
			icon = "26"
			icon_font = ""
		elif txt == "cloudy_s_rain":
			icon =	""
			icon_font = ""
		elif txt == "cloudy_s_sunny":
			icon = ""
			icon_font = ""
		elif txt == "cloudy_t_rain":
			icon = ""
			icon_font = ""
		elif txt == "fog":
			icon = ""
			icon_font = ""
		elif txt == "partly_cloudy":
			icon = ""
			icon_font = ""
		elif txt == "rain":
			icon = ""
			icon_font = ""
		elif txt == "rain_heavy":
			icon = ""
			icon_font = ""
		elif txt == "rain_light":
			icon = ""
			icon_font = ""
		elif txt == "rain_s_cloudy":
			icon = ""
			icon_font = ""
		elif txt == "rain_s_sunny":
			icon = ""
			icon_font = ""
		elif txt == "rain_t_sunny":
			icon = ""
			icon_font = ""
		elif txt == "sleet":
			icon = ""
			icon_font = ""
		elif txt == "snow":
			icon = ""
			icon_font = ""
		elif txt == "snow_heavy":
			icon = ""
			icon_font = ""
		elif txt == "snow_light":
			icon = ""
			icon_font = ""
		elif txt == "snow_s_sunny":
			icon = ""
			icon_font = ""
		elif txt == "snow_t_sunny":
			icon = ""
			icon_font = ""
		elif txt == "sunny":
			icon = ""
			icon_font = ""
		elif txt == "sunny_s_cloudy":
			icon = ""
			icon_font = ""
		elif txt == "sunny_s_rain":
			icon = ""
			icon_font = ""
		elif txt == "sunny_s_snow":
			icon = ""
			icon_font = ""
		elif txt == "sunny_t_cloudy":
			icon = ""
			icon_font = ""
		elif txt == "sunny_t_snow":
			icon = ""
			icon_font = ""
		elif txt == "thunderstorms":
			icon = ""
			icon_font = ""
		else:
			icon = ""
			icon_font = ""
		self.text = icon_font
