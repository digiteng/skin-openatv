# -*- coding: utf-8 -*-
# by digiteng...03.2022
from __future__ import absolute_import
from Components.Renderer.Renderer import Renderer
from enigma import ePoint, eWidget, eSize, eSlider, eLabel, gFont, loadPNG, eGauge
from skin import parseColor
  # <widget source="session.Event_Now" render="NachtLiveTextProgress" mode="Text+Gauge" 
  # progressBar="396,982,1203,30" progressText="396,952,70,30,24" progressGauge="396,990,20,10" progressGaugeColor="#00ffff"
  # pixmap="/usr/share/enigma2/Nacht/images/progress/progress_10b.png" 
  # position="396,952" size="1203,60" backgroundColor="#23262e" zPosition="3" alphatest="blend" transparent="1">
	# <convert type="NachtSignal">Event</convert>
  # </widget>
#
# options;
# mode="Text+Progress"
# mode == "Progress"
# mode == "Gauge" 
# mode == "Text+Gauge"

class NachtLiveTextProgress(Renderer):
	def __init__(self):
		Renderer.__init__(self)
		self.prgrsPixmap = None
		self.prgrsBarColor = "#cccccc"
		self.prgrsBarBorderColor = "#cccccc"
		self.prgrsBarBorderSize = 1
		self.backgroundColor = "#000000"
		self.prgrsGaugeColor = "#cccccc"
		
	def applySkin(self, desktop, screen):
		attribs = self.skinAttributes[:]
		for attrib, value in self.skinAttributes:
			if attrib == 'size':
				self.szX = int(value.split(',')[0])
				self.szY = int(value.split(',')[1])
			if attrib == 'progressPixmap':
				self.prgrsPixmap = value
			if attrib == 'pixmap':
				self.prgrsPixmap = value
			if attrib == 'backgroundColor':
				self.backgroundColor = value
			if attrib == 'progressBar':
				sz = value.split(',')
				self.prgrs_sizeX = int(sz[2])
				self.prgrs_sizeY = int(sz[3])
				self.prgrs_posX = int(sz[0])
				self.prgrs_posY = int(sz[1])
			if attrib == 'progressText':
				st = value.split(',')
				self.prgrsText_sizeX = int(st[2])
				self.prgrsText_sizeY = int(st[3])
				self.prgrsText_posX = int(st[0])
				self.prgrsText_posY = int(st[1])
				self.prgrsText_FontSize = int(st[4])
			if attrib == 'progressBarColor':
				self.prgrsBarColor = value
			if attrib == 'progressBarBorderColor':
				self.prgrsBarBorderColor = value
			if attrib == 'progressBarBorderSize':
				self.prgrsBarBorderSize = int(value)
			if attrib == 'progressGauge':
				gz = value.split(',')
				self.prgrsGauge_sizeX = int(gz[2])
				self.prgrsGauge_sizeY = int(gz[3])
				self.prgrsGauge_posX = int(gz[0])
				self.prgrsGauge_posY = int(gz[1])
			if attrib == 'progressGaugeColor':
				self.prgrsGaugeColor = value
			if attrib == 'mode':
				self.mode = value
		self.skinAttributes = attribs
		return Renderer.applySkin(self, desktop, screen)
		
	GUI_WIDGET = eWidget
	def changed(self, what):
		if not self.instance:
			return
		if what[0] == self.CHANGED_CLEAR:
			return
		try:
			val = 0
			loc = 0
			val = self.source.text
			if val is not None:
				val = int(self.source.text)
			if val == 0 or val == None:
				val = 0
				loc = 0
			if val > 0:
				self.prgrsText.clearForegroundColor()
				loc = int(self.szX // float(100.0 / val))
			else:
				loc = 0
				self.prgrsText.setForegroundColor(parseColor("#ff2600"))
			if self.mode == "Progress" or self.mode == "Text+Progress":
				self.prgrsBar.setValue(val)
				if self.prgrsPixmap is None or self.prgrsPixmap == "":
					self.prgrsBar.setSliderForegroundColor(parseColor(self.prgrsBarColor))
					self.prgrsBar.setSliderBorderColor(parseColor(self.prgrsBarBorderColor))
					self.prgrsBar.setSliderBorderWidth(self.prgrsBarBorderSize)
				else:
					self.prgrsBar.setPixmap(loadPNG("{}".format(self.prgrsPixmap)))
				self.prgrsBar.setAlphatest(2)
				self.prgrsBar.move(ePoint(0, self.prgrs_posY - self.prgrsText_posY))
				self.prgrsBar.resize(eSize(self.prgrs_sizeX, self.prgrs_sizeY))
				self.prgrsBar.setRange(0, 100)
				self.prgrsBar.show()
			elif self.mode == "Gauge" or self.mode == "Text+Gauge":
				if self.mode == "Text+Gauge":
					posGy = self.prgrsText_sizeY
				else:
					posGy = 0
				# if self.prgrsGaugeColor == "":
				# val = int(val)
				if val <= 25:
					self.prgrsGauge.setBackgroundColor(parseColor("#F08080"))
				elif 26 <= val <= 50:
					self.prgrsGauge.setBackgroundColor(parseColor("#F4A460"))
				elif 51 <= val <= 75:
					self.prgrsGauge.setBackgroundColor(parseColor("#EEDD82"))
				elif 76 <= val <= 100:
					self.prgrsGauge.setBackgroundColor(parseColor("#98FB98"))
				# else:
				# self.prgrsGauge.setBackgroundColor(parseColor(self.prgrsGaugeColor))
				self.prgrsGauge.resize(eSize(self.prgrsGauge_sizeX, self.prgrsGauge_sizeY))
				self.prgrsGauge.move(ePoint(loc, posGy))
				self.prgrsGauge.setTransparent(0)
				self.prgrsGauge.setZPosition(9)
				self.prgrsGauge.show()
			if self.mode == "Text" or self.mode == "Text+Progress" or self.mode == "Text+Gauge":
				self.prgrsText.setText("{}%".format(val))
				self.prgrsText.setBackgroundColor(parseColor(self.backgroundColor))
				self.prgrsText.resize(eSize(self.prgrsText_sizeX, self.prgrsText_sizeY))
				if val >= 95:
					self.prgrsText.move(ePoint(loc - self.prgrsText_sizeX, 0))
				else:
					self.prgrsText.move(ePoint(loc, 0))
				self.prgrsText.setFont(gFont("Console", self.prgrsText_FontSize))
				self.prgrsText.setTransparent(1)
				self.prgrsText.setZPosition(9)
				self.prgrsText.setVAlign(eLabel.alignBottom)
				self.prgrsText.setHAlign(eLabel.alignCenter)
				self.prgrsText.show()
		except Exception as err:
			from Tools.NachtWeatherUpdate import errorlog
			errorlog(err, __file__)
			# open("/tmp/Nacht.log", "a+").write("NachtLiveTextProgress(Renderer) {}\n".format(err))

	def GUIcreate(self, parent):
		self.instance = eWidget(parent)
		self.prgrsBar = eSlider(self.instance)
		self.prgrsGauge = eLabel(self.instance)
		self.prgrsText = eLabel(self.instance)
	
	def GUIdelete(self):
		self.prgrsBar = None
		self.prgrsGauge = None
		self.prgrsText = None
	