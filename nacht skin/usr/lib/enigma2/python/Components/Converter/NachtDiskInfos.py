# -*- coding: utf-8 -*-
# by digiteng...04.2022, 02.2025
		# <widget source="global.CurrentTime" render="Progress" position="100,470" size="1000,30" pixmap="Nacht/images/progress/prgrs_5a.png" alphatest="blend" backgroundColor="#222222" transparent="1" zPosition="9">
			# <convert type="NachtDiskInfos">ram_info_progress</convert>
		# </widget>
		# <widget source="session.CurrentService" render="Label" position="100,500" size="1000,40" font="Console; 30" transparent="1" foregroundColor="fc" backgroundColor="background" zPosition="1">
			# <convert type="NachtDiskInfos">ram_info</convert>
		# </widget>
		# <widget source="global.CurrentTime" render="Progress" position="100,570" size="1000,30" pixmap="Nacht/images/progress/prgrs_5a.png" alphatest="blend" backgroundColor="background" transparent="1" zPosition="1">
			# <convert type="NachtDiskInfos">swap_info_progress</convert>
		# </widget>
		# <widget source="session.CurrentService" render="Label" position="100,600" size="1000,40" font="Console; 30" transparent="1" foregroundColor="fc" backgroundColor="background" zPosition="1">
			# <convert type="NachtDiskInfos">swap_info</convert>
		# </widget>
		# <widget source="global.CurrentTime" render="Progress" position="100,670" size="1000,30" pixmap="Nacht/images/progress/prgrs_5a.png" alphatest="blend" backgroundColor="background" transparent="1" zPosition="1">
			# <convert type="NachtDiskInfos">flash_info_progress</convert>
		# </widget>
		# <widget source="session.CurrentService" render="Label" position="100,700" size="1000,40" font="Console; 30" transparent="1" foregroundColor="fc" backgroundColor="background" zPosition="1">
			# <convert type="NachtDiskInfos">flash_info</convert>
		# </widget>
		# <widget source="global.CurrentTime" render="Progress" position="100,770" size="1000,30" pixmap="Nacht/images/progress/prgrs_5a.png" alphatest="blend" transparent="1" backgroundColor="background" zPosition="1">
			# <convert type="NachtDiskInfos">disk_info_progress</convert>
		# </widget>
		# <widget source="session.CurrentService" render="Label" position="100,800" size="1000,40" font="Console; 30" transparent="1" foregroundColor="fc" backgroundColor="background" zPosition="1">
			# <convert type="NachtDiskInfos">disk_info</convert>
		# </widget>
from Components.Converter.Converter import Converter
from Components.Element import cached
import os
try:
	paths = ('/media/hdd', '/media/usb', '/media/sda1', '/media/sda2')
	for path in paths:
		if os.path.ismount(path):
			path = path
			break
		else:
			path = "/"
except:
	path = "/"

class NachtDiskInfos(Converter, object):
	def __init__(self, type):
		Converter.__init__(self, type)
		self.type = type

	@cached
	def getText(self):
		try:
			if "flash_info" in self.type:
				st = os.statvfs("/")  # flash...
				free = self.inf(st)[0]
				total = self.inf(st)[4]
				if "short" in self.type:
					return "FLASH {:.1f} {szf} / {:.1f} {szt}".format(self.sizename(free)[1], self.sizename(total)[1], 
							szf=self.sizename(free)[0], szt=self.sizename(total)[0])
				return "FLASH Free:{:.1f} {szf} Total:{:.1f} {szt} Used:{}% ".format(
						self.sizename(free)[1], self.sizename(total)[1], self.inf(st)[1], 
						szf=self.sizename(free)[0], szt=self.sizename(total)[0])
			if "disk_info" in self.type:
				try:
					st = os.statvfs(path) # hdd or usb
				except: return
				free = self.inf(st)[0]
				total = self.inf(st)[4]
				if "short" in self.type:
					return "{} {:.1f} {szf} / {:.1f} {szt}".format(path.split('/')[-1].upper(), self.sizename(free)[1], self.sizename(total)[1], 
							szf=self.sizename(free)[0], szt=self.sizename(total)[0])
				return "DISK({}) Free:{:.1f} {szf} Total:{:.1f} {szt} Used:{}% ".format(path.split('/')[-1].upper(), 
						self.sizename(free)[1], self.sizename(total)[1], self.inf(st)[3], 
						szf=self.sizename(free)[0], szt=self.sizename(total)[0])
			if self.type == "ram_info":
				mem = self.meminfo()
				for i in mem:
					mem = i.split()
					if mem[0] == "MemFree:":
						free = int(mem[1]) // 1000
					if mem[0] == "MemTotal:":
						total = int(mem[1]) // 1000
				if total != 0:
					p = 100 - int(float(free) / float(total) * 100)
				else:
					p = 0
				return "RAM Free:{:.1f} {szf} Total:{:.1f} {szt} Used:{}% ".format(self.sizename(free)[1], self.sizename(total)[1], p, szf=self.sizename(free)[0], szt=self.sizename(total)[0])
			if self.type == "swap_info":
				mem = self.meminfo()
				for i in mem:
					mem = i.split()
					if mem[0] == "SwapFree:":
						sf = int(mem[1]) // 1000
					if mem[0] == "SwapTotal:":
						st = int(mem[1]) // 1000
				try:
					p = 100 - int(float(sf) / float(st) * 100)
				except:
					p=0
				return "SWAP Free:{} {szf} Total:{} {szt} Used:{}%".format(sf, st, p, szf=self.sizename(sf)[0], szt=self.sizename(st)[0])
		except Exception as err:
			from Tools.NachtWeatherUpdate import errorlog
			errorlog(err, __file__)
	text = property(getText)

	@cached
	def getValue(self):
		try:

			if self.type == "flash_info_progress":
				st = os.statvfs("/")
				return self.inf(st)[3]
			if self.type == "disk_info_progress":
				st = os.statvfs(path)
				return self.inf(st)[3]
			if self.type == "ram_info_progress":
				mf = 0
				mt = 0
				mem = self.meminfo()
				for i in mem:
					mem = i.split()
					if mem[0] == "MemFree:":
						mf = int(mem[1]) // 1000
					if mem[0] == "MemTotal:":
						mt = int(mem[1]) // 1000
				ramprgrs = 100 - int(float(mf) / float(mt) * 100)
				return ramprgrs
				# else:
					# return 0
			if self.type == "swap_info_progress":
				mem = self.meminfo()
				for i in mem:
					mem = i.split()
					if mem[0] == "SwapFree:":
						sf = int(mem[1]) // 1000
					if mem[0] == "SwapTotal:":
						st = int(mem[1]) // 1000
				if st != 0:
					return 100 - int(float(sf) / float(st) * 100)
				else:
					return 0
		except Exception as err:
			from Tools.NachtWeatherUpdate import errorlog
			errorlog(err, __file__)
	value = property(getValue)
	range = 100
	
	def inf(self, st):
		try:
			free = 0.0
			used = 0.0
			total = 0.0
			percent_free = 0.0
			percent_used = 0.0
			free = st.f_bavail * st.f_frsize / 1024000
			used = (st.f_blocks - st.f_bfree) * st.f_frsize / 1024000
			total = st.f_blocks * st.f_frsize / 1024000
			percent_free = (100 * st.f_bavail) // st.f_blocks
			percent_used = (100 * (st.f_blocks - st.f_bfree )) // st.f_blocks
			return free, percent_free, used, percent_used, total
		except Exception as err:
			from Tools.NachtWeatherUpdate import errorlog
			errorlog(err, __file__)
				
	def meminfo(self):
		mem = ""
		try:
			with open("/proc/meminfo", "r") as f:
				mem = f.readlines()
		except:
			with open("/proc/meminfo", "rb") as f:
				mem = f.read()		
		return mem
		
	def sizename(self, value):
		sz = ["MB", "GB"]
		if value <= 1000:
			szs = sz[0]
			value = float(value)
		else:
			szs = sz[1]
			value = value / 1000
		return szs, value
		