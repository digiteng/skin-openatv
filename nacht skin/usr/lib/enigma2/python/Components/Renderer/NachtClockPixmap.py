# -*- coding: utf-8 -*-
# by digiteng...11.2020, 04.2022, 09.2022, 02.2025(added mode="Volume")
# <widget source="global.CurrentTime" render="NachtClockPixmap" path="/usr/share/enigma2/Nacht/clockneons/clockneon1/" mode="Clock" position="1520,1017" size="160,52" zPosition="5" alphatest="blend" transparent="1" backgroundColor="black" />
# <widget source="global.CurrentTime" render="NachtClockPixmap" path="/usr/share/enigma2/Nacht/clockneons/green/" mode="DayMounth" position="1410,1030" size="80,26" halign="right" zPosition="5" alphatest="blend" transparent="1" backgroundColor="black" />
# <widget source="global.CurrentTime" render="NachtClockPixmap" path="/usr/share/enigma2/Nacht/clockneons/orange/" mode="Year" position="1710,1030" size="80,26" halign="left" zPosition="5" alphatest="blend" transparent="1" backgroundColor="black" />
from __future__ import absolute_import
from Components.Renderer.Renderer import Renderer
from enigma import ePixmap, ePoint, eWidget, loadPNG, eSize, eDVBVolumecontrol
from datetime import datetime

class NachtClockPixmap(Renderer):
	def __init__(self):
		Renderer.__init__(self)
		self.mode = "Clock"

	GUI_WIDGET = eWidget
	def applySkin(self, desktop, screen):
		attribs = self.skinAttributes[:]
		for (attrib, value) in self.skinAttributes:
			if attrib == 'size':
				self.szX = int(value.split(',')[0])
				self.szY = int(value.split(',')[1])
			elif attrib == 'path':
				self.path = value
			elif attrib == 'mode':
				self.mode = value
		self.skinAttributes = attribs
		sx = self.szX // 4
		self.c0.resize(eSize(sx, self.szY))
		self.c0.move(ePoint(0, 0))
		self.c0.setScale(2)
		self.c0.setZPosition(5)
		self.c0.setTransparent(1)
		self.c0.setAlphatest(2)
		self.c1.resize(eSize(sx, self.szY))
		self.c1.move(ePoint(sx, 0))
		self.c1.setScale(2)
		self.c1.setZPosition(5)
		self.c1.setTransparent(1)
		self.c1.setAlphatest(2)
		self.dot.resize(eSize(self.szX, self.szY))
		self.dot.move(ePoint(0, 0))
		self.dot.setScale(2)
		self.dot.setZPosition(6)
		self.dot.setAlphatest(2)

		self.c3.resize(eSize(sx, self.szY))
		self.c3.move(ePoint(sx * 2, 0))
		self.c3.setScale(2)
		self.c3.setZPosition(5)
		self.c3.setTransparent(1)
		self.c3.setAlphatest(2)
		self.c4.resize(eSize(sx, self.szY))
		self.c4.move(ePoint(sx * 3, 0))
		self.c4.setScale(2)
		self.c4.setZPosition(5)
		self.c4.setTransparent(1)
		self.c4.setAlphatest(2)
		ret = Renderer.applySkin(self, desktop, screen)
		return ret

	def changed(self, what):
		if not self.instance:
			return
		now = datetime.now()
		if self.mode == 'Clock':
			clk = now.strftime("%H:%M")
			clk0 = clk[0]
			clk1 = clk[1]
			clk3 = clk[3]
			clk4 = clk[4]
			self.dot.setPixmap(loadPNG("{}blink.png".format(self.path)))
			self.dot.show()
		elif self.mode == 'DayMounth':
			clk = now.strftime("%d.%m")
			clk0 = clk[0]
			clk1 = clk[1]
			clk3 = clk[3]
			clk4 = clk[4]
			self.dot.setPixmap(loadPNG("{}blink.png".format(self.path)))
			self.dot.show()
		elif self.mode == 'Year':
			clk = now.strftime("%Y")
			clk0 = clk[0]
			clk1 = clk[1]
			clk3 = clk[2]
			clk4 = clk[3]
		elif self.mode == 'Volume':
			val = eDVBVolumecontrol.getInstance().getVolume()
			clk0 = str(val)[:1]
			clk1 = str(val)[1:2]
			clk3 = None
			if val == 100:
				clk3 = 0
			clk4 = None
			
		self.c0.setPixmap(loadPNG("{}{}.png".format(self.path, str(clk0))))
		self.c0.show()
		self.c1.setPixmap(loadPNG("{}{}.png".format(self.path, str(clk1))))
		self.c1.show()
		if clk3 is not None:
			self.c3.setPixmap(loadPNG("{}{}.png".format(self.path, str(clk3))))
			self.c3.show()
		else:
			self.c3.hide()
		if clk4 is not None:
			self.c4.setPixmap(loadPNG("{}{}.png".format(self.path, str(clk4))))
			self.c4.show()
		else:
			self.c4.hide()
	def GUIcreate(self, parent):
		self.instance = eWidget(parent)
		self.c0 = ePixmap(self.instance)
		self.c1 = ePixmap(self.instance)
		self.dot = ePixmap(self.instance)
		self.c3 = ePixmap(self.instance)
		self.c4 = ePixmap(self.instance)
		
	def GUIdelete(self):
		self.c0 = None
		self.c1 = None
		self.dot = None
		self.c3 = None
		self.c4 = None
