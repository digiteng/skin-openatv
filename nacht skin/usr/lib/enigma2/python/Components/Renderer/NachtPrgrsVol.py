# -*- coding: utf-8 -*-
# by digiteng...10.2020
# <widget render="prgrsVol" source="global.CurrentTime" position="0,0" size="100,100" backgroundColor="#000000" zPosition="3" transparent="1" />
from __future__ import absolute_import
from Components.Renderer.Renderer import Renderer
from enigma import eTimer, ePoint, eWidget, eLabel, eSize, eDVBVolumecontrol
from skin import parseColor

class NachtPrgrsVol(Renderer):
	def __init__(self):
		Renderer.__init__(self)
		self.vol_timer = eTimer()
		self.vol_timer.callback.append(self.pollme)
		
	GUI_WIDGET = eWidget
	def applySkin(self, desktop, screen):
		attribs = self.skinAttributes[:]
		for attrib, value in self.skinAttributes:
			if attrib == 'position':
				self.x = int(value.split(',')[0])
				self.y = int(value.split(',')[1])
			elif attrib == 'size':
				self.szX = int(value.split(',')[0])
				self.szY = int(value.split(',')[1])
			elif attrib == 'backgroundColor':
				self.backgroundColor = value
		self.skinAttributes = attribs
		ret = Renderer.applySkin(self, desktop, screen)
		
	def changed(self, what):
		if not self.suspended:
			val = 0
			try:
				val = eDVBVolumecontrol.getInstance().getVolume()

				x, y = 0, 0
				if val >= 0 and val <= 50:
					x = 0
					y = (float(50) / float(self.szY) ) * 100
					y = ((float(val) / float(self.szY)) * float(self.szY)) / y * 100
					y = int(-y)
					self.prgrsVal.setBackgroundColor(parseColor(self.backgroundColor))
					self.prgrsVal.resize(eSize(self.szX // 2, self.szY))
					self.prgrsVal.move(ePoint(x, y))
					self.prgrsVal.setTransparent(0)
					self.prgrsVal.setZPosition(3)
					self.prgrsVal.show()
					self.prgrsValR.setBackgroundColor(parseColor(self.backgroundColor))
					self.prgrsValR.resize(eSize(self.szX // 2, self.szY))
					self.prgrsValR.move(ePoint(self.szX // 2, 0))
					self.prgrsValR.setTransparent(0)
					self.prgrsValR.setZPosition(3)
					self.prgrsValR.show()
				elif val >= 51 and val <= 100:
					x = self.szX // 2
					y = (float(50) / float(self.szY) ) * 100
					y = (float(val) / float(self.szY) * float(self.szY)) / y * 100
					y = y - self.szY + self.szY / 10
					y = int(y)
					self.prgrsValR.clearBackgroundColor()
					self.prgrsValR.hide()
					self.prgrsVal.clearBackgroundColor()
					self.prgrsVal.setBackgroundColor(parseColor(self.backgroundColor))
					self.prgrsVal.resize(eSize(self.szX // 2, self.szY))
					self.prgrsVal.move(ePoint(x, y))
					self.prgrsVal.setTransparent(0)
					self.prgrsVal.setZPosition(3)
					self.prgrsVal.show()
				else:
					return
			except Exception as err:
				from Tools.NachtWeatherUpdate import errorlog
				errorlog(err, __file__)
				
	def GUIcreate(self, parent):
		self.instance = eWidget(parent)
		self.prgrsVal = eLabel(self.instance)
		self.prgrsValR = eLabel(self.instance)
		
	def pollme(self):
		self.changed(None)
		return
		
	def onShow(self):
		self.suspended = False
		self.vol_timer.start(200)
		
	def onHide(self):
		self.suspended = True
		self.vol_timer.stop()
		