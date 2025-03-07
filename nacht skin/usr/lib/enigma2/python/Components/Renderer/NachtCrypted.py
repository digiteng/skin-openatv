# -*- coding: utf-8 -*-
# by digiteng...10.2022
# <widget source="session.CurrentService" render="NachtCrypted" pixmaps="/usr/share/enigma2/Nacht/nicons/crypt_on.png,/usr/share/enigma2/Nacht/nicons/crypt_off.png" position="112,75" size="300,399" zPosition="9" backgroundColor="background" transparent="1" alphatest="blend" />
from __future__ import absolute_import
from Components.Renderer.Renderer import Renderer
from enigma import ePixmap, iServiceInformation

class NachtCrypted(Renderer):
	def __init__(self):
		Renderer.__init__(self)

	def applySkin(self, desktop, screen):
		attribs = self.skinAttributes[:]
		for attrib, value in self.skinAttributes:
			if attrib == 'pixmaps':
				self.pixmaps = value.split(",")			
		return Renderer.applySkin(self, desktop, screen)
		
	GUI_WIDGET = ePixmap
	def changed(self, what):
		try:
			if not self.instance:
				return
			if what[0] == self.CHANGED_CLEAR:
				return
			info = None
			service = self.source.service
			info = service and service.info()
			if not info:
				return ""
			xres = info.getInfo(iServiceInformation.sVideoWidth)
			if info.getInfo(iServiceInformation.sIsCrypted) == 1:
				self.instance.hide()
				self.instance.setPixmapFromFile("{}".format(self.pixmaps[0]))
				self.instance.show()
				if xres:
					self.instance.hide()
					self.instance.setPixmapFromFile("{}".format(self.pixmaps[1]))
					self.instance.show()
			else:
				self.instance.hide()
		except Exception as err:
			from Tools.NachtWeatherUpdate import errorlog
			errorlog(err, __file__)
