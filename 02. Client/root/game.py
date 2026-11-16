# GameWindow.__init__ icinde ara:
		self.targetBoard = uiTarget.TargetBoard()
		self.targetBoard.SetWhisperEvent(ui.__mem_func__(self.interface.OpenWhisperDialog))

# Altina ekle:
		if app.ENABLE_WIKI_SYSTEM:
			self.targetBoard.SetWikiEvent(ui.__mem_func__(self.interface.SearchWikiForMob))


# GameWindow.__PressHKey icinde ara:
			net.SendChatPacket("/ride")
		else:

# Altina ekle:
			if app.ENABLE_WIKI_SYSTEM:
				self.interface.OpenWikiWindow()

