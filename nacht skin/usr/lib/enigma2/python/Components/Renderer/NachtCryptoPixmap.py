# -*- coding: utf-8 -*-
# by digiteng...04.2022

from __future__ import absolute_import
from Components.Renderer.Renderer import Renderer
from enigma import ePixmap, iServiceInformation
from Components.Converter.Poll import Poll
from sys import version_info
pyx = version_info[0] == 2

class NachtCryptoPixmap(Poll, Renderer):
	def __init__(self):
		Renderer.__init__(self)
		Poll.__init__(self)
		self.poll_interval = 1000
		self.poll_enabled = True
		self.cv = {
			"26" : "Biss",
			"01" : "Seca",
			"06" : "Irdeto",
			"17" : "BetaCrypt",
			"05" : "Viacces",
			"18" : "Nagravision",
			"09" : "NDS-Videoguard",
			"0B" : "Conax",
			"0D" : "Cryptoworks",
			"4A" : "DRE",
			"0E" : "PowerVu",
			"22" : "Codicrypt",
			"47" : "General",
			"56" : "Verimatrix",
			"10" : "Tandberg",
			"7B" : "DRE",
			"A1" : "Rosscrypt",
			"55" : "BulCrypt",
			"" : ""
			}
			
	GUI_WIDGET = ePixmap
	
	def applySkin(self, desktop, screen):
		attribs = self.skinAttributes[:]
		for (attrib, value) in self.skinAttributes:
			if attrib == 'path':
				self.path = value
		self.skinAttributes = attribs
		ret = Renderer.applySkin(self, desktop, screen)
		return ret

	def changed(self, what):
		if not self.instance:
			return
		try:
			if what[0] == self.CHANGED_CLEAR:
				self.instance.hide()
				return
			if what[0] != self.CHANGED_CLEAR:
				service = self.source.service
				info = service and service.info()
				if not info:
					return False
				if service:
					caids = info.getInfoObject(iServiceInformation.sCAIDs)
					# for caid in caids:
						# ch = hex(caid).replace("0x", "")
						# if len(ch) == 3:
							# ch = "0{}".format(ch)
						# for cpng in self.cv:
							# open("/tmp/cpng","a+").write("%s\n"%(self.cv[cpng]))
							# if cpng == ch[:2].upper():
								# cpng = cpng
								# break
					# self.instance.setPixmapFromFile("{}{}_c.png".format(self.path, self.cv[cpng]))
					# self.instance.setScale(0)
					# self.instance.show()
					if info.getInfo(iServiceInformation.sIsCrypted) == 1:
						cp = "crypt"
					else:
						cp = "fta"
					try:
						if pyx:
							ecm = open("/tmp/ecm.info", 'rb').readlines()
						else:
							ecm = open("/tmp/ecm.info", 'r').readlines()
					except:
						ecm = ''
					if not ecm == '':
						for i in ecm:
							ecm = i.split()
							if ecm[0] == "caid:":
								ecm = ecm[1].replace("0x", "")
								break
						if len(ecm) == 3:
							ecm = "0{}".format(ecm)
						for cpng in self.cv:
							if cpng == ecm[:2]:
								cpng = cpng
								break
						cp = self.cv[cpng]
						del ecm
					self.instance.setPixmapFromFile("{}{}.png".format(self.path, cp))
					self.instance.setScale(0)
					self.instance.show()

				else:
					self.instance.hide()
					return
		except Exception as err:
			from Tools.NachtWeatherUpdate import errorlog
			errorlog(err, __file__)
			