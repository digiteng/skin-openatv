# -*- coding: utf-8 -*-
# by digiteng...09.2020, 02.2022
# <widget source="session.CurrentService" render="Label" position="215,940" size="520,27" font="Regular; 21" halign="left" transparent="1" zPosition="2" backgroundColor="black" valign="center">
  # <convert type="NachtServiceInfo">ServiceCompact</convert>
# </widget>
from Components.Converter.Converter import Converter
from Components.Element import cached
from enigma import iServiceInformation, iPlayableService, eServiceReference, iPlayableServicePtr
from Components.Converter.Poll import Poll
from Components.config import config

class NachtServiceInfo(Poll, Converter):
	def __init__(self, type):
		Converter.__init__(self, type)
		Poll.__init__(self)
		self.type = type
		self.poll_interval = 1000
		self.poll_enabled = True
		
	@cached
	def getText(self):
		xres=""
		yres=""
		fps=""
		info = None
		service = self.source.service
		info = service and service.info()
		if not info:
			return ""
		xres = info.getInfo(iServiceInformation.sVideoWidth)
		yres = info.getInfo(iServiceInformation.sVideoHeight)
		fps = info.getInfo(iServiceInformation.sFrameRate)
		# provider = info.getInfo(iServiceInformation.sProvider)

		if self.type == "Name":
			return info.getName()
		elif self.type == "Number":
			try:
				if config.usage.show_infobar_channel_number.value:
					ref = self.source.serviceref
					num = ref.getChannelNum() or None
					return str(num)
				else:
					return ""
			except:
				return ""
		elif self.type == "Orbital":	
			ti = info.getInfoObject(iServiceInformation.sTransponderData)
			pos = ti.get("orbital_position", 0)
			return pos > 1800 and "%d.%d°W" % ((3600 - pos) / 10, (3600 - pos) % 10) or "%d.%d°E" % (pos / 10, pos % 10) #ServiceName2
		elif self.type == "Provider":
			return info.getInfoString(iServiceInformation.sProvider)
		elif self.type == "ServiceCompact":
			gamma = ('SDR', 'HDR', 'HDR10', 'HLG', '')[info.getInfo(iServiceInformation.sGamma)]
			inf = []
			audio = service.audioTracks()
			if audio:
				n = audio.getNumberOfTracks()
				idx = 0
				while idx < n:
					i = audio.getTrackInfo(idx)
					description = i.getDescription()
					if description in ('AC3', 'AC3+', 'DTS', 'DTS-HD', 'AC-3'):
						inf.append("DOLBY")
						break
					idx += 1

			if gamma != "":
				inf.append(gamma)
			if yres < 720:
				inf.append("SD")
			elif yres >= 720 and yres < 1080 :
				inf.append("HD")
			elif yres >= 1080 and yres < 2160:
				inf.append("FHD")
			elif yres >= 2160:
				inf.append("4K")
			if info.getInfo(iServiceInformation.sIsCrypted) == 1:
				inf.append("$")
			else:
				inf.append("FTA")
			if info.getInfoString(iServiceInformation.sHBBTVUrl) != "":
				hbb = '\\c00??2200H\\c0000??00b\\c00????00b\\c0000????TV'
				inf.append(hbb)
			subservices = service.subServices()
			if subservices and subservices.getNumberOfSubservices() > 0:
				inf.append("SUB")
			subtitle = service and service.subtitle()
			subtitlelist = subtitle and subtitle.getSubtitleList()
			if subtitlelist:
				if len(subtitlelist) > 0:
					inf.append("SUBT")
			audio = service.audioTracks()
			if bool(audio and audio.getNumberOfTracks() > 1):
				inf.append("A")
			if service.streamed() is not None:
				inf.append("Stream")
			tpid = info.getInfo(iServiceInformation.sTXTPID)
			if tpid != -1:
				inf.append("TxT")
			sep_color = '\\c0000???? | '
			sep_color += '\\c00??????'
			return sep_color.join(inf)
		
		elif self.type == "Resolution":
			return "{}x{}({}fps)".format(xres, yres, (fps // 1000))
		elif self.type == "AVtype":
			try:
				atype = ""
				vtype = ""
				audio = service.audioTracks()
				if audio:
					if audio.getCurrentTrack() > -1:
						atype = str(audio.getTrackInfo(audio.getCurrentTrack()).getDescription()).replace(",","")
				vtype = ("MPEG2", "H.264", "MPEG1", "MPEG4-II", "VC1", "VC1-SM", "HEVC", "")[info.getInfo(iServiceInformation.sVideoType)]
				return "\c0000??80Audio : \c00??????{}  \c0000??80Video : \c00??????{}".format(atype, vtype)
			except:
				return ""
		elif self.type == "TunerType":
			tt = self.source.frontend_type
			return tt or  _("Unknown")
	text = property(getText)

	@cached
	def getBoolean(self):
		service = self.source.service
		info = service and service.info()
		if not info:
			return False
		xres = info.getInfo(iServiceInformation.sVideoWidth)			
		if self.type == "isStream":
			if service.streamed():
				return True
		elif self.type == "isCryptedON":
			if info.getInfo(iServiceInformation.sIsCrypted) == 1:
				return True
		elif self.type == "isCryptedOFF":
			if xres:
				if info.getInfo(iServiceInformation.sIsCrypted) == 1:
					return True
		elif self.type == "isFta":
			return info.getInfo(iServiceInformation.sIsCrypted) == 0

	boolean = property(getBoolean)			

	def changed(self, what):
		Converter.changed(self, what)
