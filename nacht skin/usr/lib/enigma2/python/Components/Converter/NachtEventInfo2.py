# -*- coding: utf-8 -*-
# by digiteng...09.2020
# <widget source='session.Event_Now' render='Label' position='135,80' size='330,40' font='Regular; 14' halign='left' transparent='1' zPosition='2' backgroundColor='background' valign='center'>
	# <convert type='EvntInfo'>SESSION_EPISODE,PARENTAL_RATING,YEAR,GENRE,DURATION</convert>
# </widget>
from Components.Converter.Converter import Converter
from Components.Element import cached
from Components.Converter.NachtEventGenre import getGenreStringSub
import re
from Components.Converter.Poll import Poll

class NachtEventInfo2(Poll, Converter, object):

	SESSION_EPISODE = 'SESSION_EPISODE'
	PARENTAL_RATING = 'PARENTAL_RATING'
	YEAR = 'YEAR'
	DURATION = 'DURATION'
	GENRE = 'GENRE'
	
	def __init__(self, type):
		Converter.__init__(self, type)
		Poll.__init__(self)
		self.types = str(type).split(',')
		self.poll_interval = 1000
		self.poll_enabled = True
	@cached
	def getText(self):
		event = self.source.event
		if event:
			fd = "{}\n{}\n{}".format(event.getEventName(), event.getShortDescription(), event.getExtendedDescription())
			if self.types:
				eventList = []
				try:
					for type in self.types:
						type.strip()

						if type == self.SESSION_EPISODE:
							prs = ['(\d+). Staffel, Folge (\d+)', 'T(\d+) Ep.(\d+)', '"Episodio (\d+)" T(\d+)']
							for i in prs:
								seg = re.search(i, fd)
								if seg:
									s = seg.group(1).zfill(2)
									e = seg.group(2).zfill(2)
									se = 'S%sE%s' % (s, e)
									eventList.append(str(se))

						elif type == self.PARENTAL_RATING:
							parentName = ''
							prs = ['[aA]b ((\d+))', '[+]((\d+))', 'Od lat: ((\d+))', '(\d+)[+]', '(TP)', '[-](\d+)']
							for i in prs:
								prr = re.search(i, fd)
								if prr:
									parentName = prr.group(1)
									parentName = parentName.replace('7', '6').replace('10', '12').replace('TP', '0')
									eventList.append('+{}'.format(parentName))
									break
							age = ''
							country = ''
							rating = event.getParentalData()
							if rating:
								country = rating.getCountryCode().upper()
								if parentName == '':
									age = rating.getRating()
									eventList.append('+{}({})'.format(str(age), str(country)))

						elif type == self.YEAR:
							year = ''
							fd = fd.replace(',', '').replace('(', '').replace(')', '')
							sd = event.getShortDescription()
							fdl = ['[A-Z]*/[A-Z]* \d{4}', '\d{4} [A-Z]+', '[A-Z]+ \d{4}', '[A-Z][a-z]+\s\d{4}', '\+\d+\s\d{4}', '\d{4}']
							for i in fdl:
								year = re.findall(i, sd)
								if year:
									year = re.sub(r'\(.*?\)|\.|\+\d+', ' ', year[0]).strip()
									eventList.append(str(year))
									break
								else:
									year = re.findall(i, fd)
									if year:
										year = re.sub(r'\(.*?\)|\.|\+\d+', ' ', year[0]).strip()
										eventList.append(str(year))
										break

						elif type == self.DURATION:
							drtn = event.getDuration() // 60
							if drtn > 0:
								eventList.append('{} min'.format(drtn))
							else:
								prs = re.findall(r' \d+ Min', fd)
								if prs:
									drtn = str(prs[0]).strip()
									eventList.append(str(drtn))

						elif type == self.GENRE:
							genres = event.getGenreDataList()
							if genres:
								genre = genres[0]
								eventList.append(getGenreStringSub(genre[0], genre[1]))

					sep_color = '\\c0000??00' + ' | '
					sep_color += '\\c00??????'
					return sep_color.join(eventList)
				except:
					return ''
		return ''
	text = property(getText)
