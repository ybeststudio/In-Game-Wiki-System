# BiologistWindow.__Build icinde ara:
		self.AddFlag("float")
		self.SetCenterPosition()

# Altina ekle:
		if app.ENABLE_WIKI_SYSTEM:
			wiki = ui.Button()
			wiki.SetParent(self)
			wiki.SetUpVisual("d:/ymir work/ui/game/wiki/layout/button_wiki_small_norm.png")
			wiki.SetOverVisual("d:/ymir work/ui/game/wiki/layout/button_wiki_small_hover.png")
			wiki.SetDownVisual("d:/ymir work/ui/game/wiki/layout/button_wiki_small_down.png")
			wiki.SetPosition(318, 6)
			wiki.SetEvent(ui.__mem_func__(self.__OnClickWiki))
			wiki.Show()
			self.keep.append(wiki)


# BiologistWindow.__OnClickWiki icinde ara:
	def __OnClickWiki(self):

# Altina ekle:
		if self.interface and app.ENABLE_WIKI_SYSTEM:
			self.interface.OpenWikiWindow()

