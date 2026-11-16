# CompanionWindow.__LoadWindow icinde ara:
		board.Show()
		self.board = board

# Altina ekle:
		if app.ENABLE_WIKI_SYSTEM:
			wiki = ui.Button()
			wiki.SetParent(board.titleBar)
			wiki.SetUpVisual("d:/ymir work/ui/game/wiki/layout/button_wiki_small_norm.png")
			wiki.SetOverVisual("d:/ymir work/ui/game/wiki/layout/button_wiki_small_hover.png")
			wiki.SetDownVisual("d:/ymir work/ui/game/wiki/layout/button_wiki_small_down.png")
			(cx, cy) = board.titleBar.btnClose.GetLocalPosition()
			wiki.SetPosition(cx - 20, cy - 3)
			wiki.SetEvent(ui.__mem_func__(self.__OnClickWiki))
			wiki.Show()
			self.wikiButton = wiki


# CompanionWindow.__OnClickWiki icinde ara:
	def __OnClickWiki(self):

# Altina ekle:
		if self.interface and app.ENABLE_WIKI_SYSTEM:
			self.interface.OpenWikiWindow()

