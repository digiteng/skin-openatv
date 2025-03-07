# -*- coding: utf-8 -*-
# by digiteng, 04.2022, 06.2022
# <widget render="NachtPrimeTime" source="ServiceEvent" position="1265,795" size="600,40" font="Regular; 30" noWrap="1" zPosition="2" transparent="1" />
from __future__ import absolute_import
from Components.Renderer.Renderer import Renderer
from Components.VariableText import VariableText
from enigma import eLabel, eEPGCache, eServiceReference
from time import localtime, mktime, time
from datetime import datetime
from Components.config import config

class NachtPrimeTime(Renderer, VariableText):

	def __init__(self):
		Renderer.__init__(self)
		VariableText.__init__(self)
		self.epgcache = eEPGCache.getInstance()

	GUI_WIDGET = eLabel
	def changed(self, what):
		try:
			if what[0] == self.CHANGED_CLEAR:
				self.text = ""
				return
			else:
				event = self.source.event
				if event is None:
					self.text = "N/A"
					return
					return
				try:
					service = self.source.service
				except:
					import NavigationInstance
					service = NavigationInstance.instance.getCurrentlyPlayingServiceReference()
				primetime = "N/A"
				self.text = "N/A"
				if self.epgcache is not None:
					try:
						prime_hour = config.epgselection.graph_primetimehour.value
						prime_minute = config.epgselection.graph_primetimemins.value
					except:
						prime_hour = 20
						prime_minute = 15
					bt = None
					now = localtime(time())
					dt = datetime(now.tm_year, now.tm_mon, now.tm_mday, prime_hour, prime_minute)
					pt = int(mktime(dt.timetuple()))
					self.epgcache.startTimeQuery(eServiceReference(service.toString()), pt)
					event = self.epgcache.getNextTimeEntry()
					if event and (now.tm_hour <= prime_hour):
						bt = localtime(event.getBeginTime())
						duration = round(event.getDuration() // 60)
						primetime = "\c0000??80%02d:%02d \c00??????%s (%smin)"%(bt[3], bt[4], event.getEventName(), duration)
					else:
						self.text = "N/A"

				self.text = primetime
		except Exception as err:
			from Tools.NachtWeatherUpdate import errorlog
			errorlog(err, __file__)
