# -*- coding: utf-8 -*-

from __future__ import absolute_import
from Components.Renderer.Renderer import Renderer
from enigma import eEPGCache, eWidget, ePoint, eSlider, eLabel, eSize, ePixmap, gFont
from Components.config import config
import json
import re
import os
import socket
import sys
from skin import parseColor


class NachtDiskInfo(Renderer):
	def __init__(self):
		Renderer.__init__(self)
		self.mode = "N/A"
		self.font = "Regular; 22"
		self.backgroundColor = "#000000"
		self.transparent = 1
		self.downloadTime = None
		self.eventNumber = 0
		self.Halign = "center"
		self.Valign = "center"

	def applySkin(self, desktop, parent):
		self.number = 0
		attribs = []
		for (attrib, value) in self.skinAttributes:
			if attrib == 'position':
				self.px = int(value.split(',')[0])
				self.py = int(value.split(',')[1])
			if attrib == 'size':
				self.szX = int(value.split(',')[0])
				self.szY = int(value.split(',')[1])
			if attrib == 'backgroundColor':
				self.backgroundColor = value
			if attrib == "mode":
				self.mode = value
			if attrib == "font":
				self.font = value
			if attrib == "option":
				self.option = value
			if attrib == "transparent":
				self.transparent = int(value)
			if attrib == "zPosition":
				self.zPosition = int(value)
			if attrib == "cornerRadius":
				self.cornerRadius = int(value)
			if attrib == "downloadTime":
				self.downloadTime = value
			if attrib == "eventNumber":
				self.eventNumber = int(value)
			if attrib == "halign":
				self.Halign = value
			if attrib == "valign":
				self.Valign = value
			attribs.append((attrib, value))
		self.skinAttributes = attribs
		return Renderer.applySkin(self, desktop, parent)
		
	GUI_WIDGET = eWidget
	def changed(self, what):
		if not self.instance:
			return
		if what[0] == self.CHANGED_CLEAR:
			return
		if what[0] != self.CHANGED_CLEAR:
			self.eventText.setText("PosterX2")
			self.eventText.resize(eSize(500,40))
			self.eventText.move(ePoint(0,0))
			self.eventText.setFont(gFont("Regular", 22))
			self.eventText.setBackgroundColor(parseColor("#90111115"))
			self.eventText.setForegroundColor(parseColor("#222225"))
			self.eventText.setHAlign(eLabel.alignCenter)
			self.eventText.setVAlign(eLabel.alignCenter)
			self.eventText.setTransparent(0)
			self.eventText.setZPosition(9)
			# self.eventText.setCornerRadius(self.cornerRadius, 15)
			self.eventText.show()


	def GUIcreate(self, parent):
		self.instance = eWidget(parent)
		self.eventText = eLabel(self.instance)
		self.eventImage = ePixmap(self.instance)

	def GUIdelete(self):
		self.eventText = None
		self.instance = None
		self.eventImage = None
