# TargetBoard.__init__ icinde ara:
			infoBoard.Hide()
			infoButton.showWnd = infoBoard

# Altina ekle:
		if app.ENABLE_WIKI_SYSTEM:
			wikiButton = ui.Button()
			wikiButton.SetParent(self)
			wikiButton.SetUpVisual("d:/ymir work/ui/pattern/wikipediainfo_btn.png")
			wikiButton.SetOverVisual("d:/ymir work/ui/pattern/wikipediainfo_btn_hover.png")
			wikiButton.SetDownVisual("d:/ymir work/ui/pattern/wikipediainfo_btn_pressed.png")
			wikiButton.SetEvent(ui.__mem_func__(self.__OnWiki))
			wikiButton.Hide()
			self.wikiButton = wikiButton
			self.eventWiki = None


# TargetBoard.Destroy icinde ara:
				self.damageDetails.Destroy()
			self.damageDetails = None

# Altina ekle:
		if app.ENABLE_WIKI_SYSTEM:
			self.wikiButton = None
			self.eventWiki = None


# TargetBoard icinde ara:
	def SetWhisperEvent(self, event):
		self.eventWhisper = event

# Altina ekle:
	if app.ENABLE_WIKI_SYSTEM:
		def SetWikiEvent(self, event):
			self.eventWiki = event

		def __OnWiki(self):
			vnum = nonplayer.GetRaceNumByVID(self.vid)
			if self.eventWiki and vnum:
				self.eventWiki(vnum)


# TargetBoard.__ApplyHealthLayout icinde ara:
			x += self.infoButton.GetWidth()
			gap = self.INFO_BUTTON_GAP

# Altina ekle:
		if app.ENABLE_WIKI_SYSTEM and self.wikiButton.IsShow():
			x += gap
			self.wikiButton.SetPosition(x, self.WIKI_BUTTON_Y)
			x += self.wikiButton.GetWidth()


# TargetBoard.ResetTargetBoard icinde ara:
			self.infoButton.Hide()
			self.infoButton.showWnd.Close()

# Altina ekle:
		if app.ENABLE_WIKI_SYSTEM:
			self.wikiButton.Hide()


# TargetBoard.SetEnemyVID icinde ara:
			self.vnum = vnum
			self.infoButton.Show()

# Altina ekle:
		if app.ENABLE_WIKI_SYSTEM and nonplayer.GetRaceNumByVID(vid):
			self.wikiButton.Show()
		if app.ENABLE_MOB_DROP_INFO or app.ENABLE_WIKI_SYSTEM:
			if self.hpGauge.IsShow():
				self.__ApplyHealthLayout()
				self.UpdatePosition()

