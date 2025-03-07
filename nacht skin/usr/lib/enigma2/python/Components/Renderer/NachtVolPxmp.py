# -*- coding: utf-8 -*-
# by digiteng...09.2020, 10.2020
# <widget render="liveVolumePxmp" source="global.CurrentTime" path="/usr/share/enigma2/LiteHD3/volume/gVol.png" position="30,30" size="200,44" zPosition="1" alphatest="blend" transparent="1" />
from __future__ import absolute_import
# from __future__ import division
# from past.utils import old_div
from Components.Renderer.Renderer import Renderer
from enigma import ePixmap, eTimer, ePoint, eDVBVolumecontrol

class NachtVolPxmp(Renderer):

	def __init__(self):
		Renderer.__init__(self)

		self.vol_timer = eTimer()
		self.vol_timer.callback.append(self.pollme)

	def applySkin(self, desktop, parent):
		attribs = self.skinAttributes[:]
		for attrib, value in self.skinAttributes:
			if attrib == 'position':
				self.x = value.split(',')[0]
				self.y = value.split(',')[1]
			elif attrib == 'path':
				self.path = value

		self.skinAttributes = attribs
		ret = Renderer.applySkin(self, desktop, parent)

	GUI_WIDGET = ePixmap
	def changed(self, what):
		if not self.suspended:
			val = eDVBVolumecontrol.getInstance().getVolume()
			sz = self.instance.size().width()
			if val > 0:
				loc = int(sz // (100.0 / val))
			else:
				loc = 0

			self.instance.setPixmapFromFile("{}".format(self.path))
			actvLoc = ePoint(loc + int(self.x), int(self.y))
			self.instance.move(actvLoc)
			self.instance.show()

	def pollme(self):
		self.changed(None)
		return

	def onShow(self):
		self.suspended = False
		self.vol_timer.start(200)

	def onHide(self):
		self.suspended = True
		self.vol_timer.stop()
