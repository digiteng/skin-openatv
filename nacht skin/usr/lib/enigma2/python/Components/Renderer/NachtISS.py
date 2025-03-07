# -*- coding: utf-8 -*-
# by digiteng...09.2022
# <widget source="session.CurrentService" render="NachtWeatherTutiempo" mode="day_1" position="112,75" size="300,399" zPosition="9" backgroundColor="black" transparent="1" />
from __future__ import absolute_import
from Components.Renderer.Renderer import Renderer
from enigma import ePixmap, ePoint, eWidget, eSize, eTimer, eLabel, gFont, addFont, loadPNG
import os
from time import time, localtime, strftime
from skin import parseColor
from Tools.NachtWeatherUpdate import checkUpdateWeather, dataRead, runISS
from threading import Thread
datajson = "/tmp/Nacht_ISS.json"
datafile = "/tmp/Nacht_isspos.png"

class NachtISS(Renderer):
	def __init__(self):
		Renderer.__init__(self)
		self.timer = eTimer()
		self.timer.callback.append(self.startDown)
		
	def applySkin(self, desktop, screen):
		attribs = self.skinAttributes[:]
		for attrib, value in self.skinAttributes:
			if attrib == 'backgroundColor':
				self.backgroundColor = value

		self.skinAttributes = attribs
		self.lbl.setBackgroundColor(parseColor(self.backgroundColor))
		self.lbl.resize(eSize(600, 460))
		self.lbl.move(ePoint(1285, 440))
		self.lbl.setFont(gFont("Regular", 20))
		self.lbl.setHAlign(eLabel.alignLeft)
		self.lbl.setTransparent(1)
		self.lbl.setZPosition(9)
		
		# self.pxmp.setPixmap(loadPNG("/usr/share/enigma2/Nacht/images/weather/wb3x.png"))
		self.pxmp.resize(eSize(750, 750))
		self.pxmp.move(ePoint(260, 115))
		self.pxmp.setTransparent(1)
		self.pxmp.setAlphatest(2)
		self.pxmp.setZPosition(9)
		self.pxmp.setScale(1)
		return Renderer.applySkin(self, desktop, screen)

	GUI_WIDGET = eWidget
	def changed(self, what):
		if not self.instance:
			return
		if what[0] == self.CHANGED_CLEAR:
			return
		
		# datajson = "/tmp/Nacht_ISS.json"
		if checkUpdateWeather(datajson) == True:
			self.timer.start(10000, True)
		Thread(target=self.getISS).start()
		
	def getISS(self):
		try:
			datajson = "/tmp/Nacht_ISS.json"
			data = dataRead(datajson)
			if data == "N/A":
				return ""		
			asi=[]
			for i in range(data["number"]):
				name = data["people"][i]["name"]
				ship = " ({})".format(data["people"][i]["craft"])
				asi.append(name + ship)
			an = "Number Of Astronauts in Space : {}\n\n".format(data["number"])
			ns = "\n".join(asi)
			self.lbl.setText("{}{}".format(an, ns))
			self.lbl.show()
			
			datafile = "/tmp/Nacht_isspos.png"
			if os.path.exists(datafile):
				# self.pxmp.setPixmapFromFile(datafile)
				self.pxmp.setPixmap(loadPNG(datafile))
				self.pxmp.show()
		except Exception as err:
			from Tools.NachtWeatherUpdate import errorlog
			errorlog(err, __file__)

	def startDown(self):
		runISS()

	def GUIcreate(self, parent):
		self.instance = eWidget(parent)
		self.lbl = eLabel(self.instance)
		self.pxmp = ePixmap(self.instance)

	def GUIdelete(self):
		self.lbl = None
		self.pxmp = None
