# Ara:
if app.ENABLE_IKASHOP_RENEWAL:
	import uiikashop

# Altina ekle:
if app.ENABLE_WIKI_SYSTEM:
	import uiWiki


# Interface.__init__ icinde ara:
		if app.ENABLE_DUNGEON_INFO:
			self.wndDungeonInfo = None

# Altina ekle:
		if app.ENABLE_WIKI_SYSTEM:
			self.wndWiki = None


# Interface.__MakeTaskBar icinde ara:
				self.PetInformationActivate()
				self.wndExpandedTaskBar.SetToggleButtonEvent(uiTaskBar.ExpandedTaskBar.BUTTON_PET_INFO, ui.__mem_func__(self.TogglePetInformationWindow))

# Altina ekle:
			if app.ENABLE_WIKI_SYSTEM:
				self.wndExpandedTaskBar.SetToggleButtonEvent(uiTaskBar.ExpandedTaskBar.BUTTON_WIKI, ui.__mem_func__(self.OpenWikiWindow))


# Interface.__MakeGameButtonWindow icinde ara:
		wndGameButton.SetButtonEvent("QUEST", ui.__mem_func__(self.__OnClickQuestButton))
		wndGameButton.SetButtonEvent("BUILD", ui.__mem_func__(self.__OnClickBuildButton))

# Altina ekle:
		wndGameButton.SetButtonEvent("GUIDE", ui.__mem_func__(self.__OnClickGuideButton))


# Interface icinde ara:
		advanced_option_notifications.BindButton(wndGameButton.gameButtonDict["NOTIFICATION_HISTORY"])
		self.wndGameButton = wndGameButton

# Altina ekle:
	def __OnClickGuideButton(self):
		if app.ENABLE_WIKI_SYSTEM:
			self.OpenWikiWindow()


# Interface.MakeHyperlinkTooltip icinde ara:
				self.hyperlinkItemTooltip.SetHyperlinkPetItem(tokens)
			elif "wiki" == type:

# Altina ekle:
				self.OpenWikiWindow()
				self.wndWiki.OpenRules()


# Interface.Close icinde ara:
				eachQuestWindow = None
		self.wndQuestWindow = {}

# Altina ekle:
		if app.ENABLE_WIKI_SYSTEM:
			if self.wndWiki:
				self.wndWiki.Close()
				self.wndWiki.Destroy()
				self.wndWiki=None


# Interface.ShowWhisperDialog icinde ara:
	def ShowWhisperDialog(self, btn):

# Altina ekle:
		if app.ENABLE_WIKI_SYSTEM and btn.name == "[W?K?]":
			self.__DestroyWhisperButton(btn)
			self.OpenWikiWindow()
			return


# Interface.__MakeWhisperButton icinde ara:
	def __MakeWhisperButton(self, name):
		whisperButton = uiWhisper.WhisperButton()

# Altina ekle:
		if app.ENABLE_WIKI_SYSTEM and name == "[W?K?]":
			whisperButton.SetUpVisual("d:/ymir work/ui/game/whisper/wikipedia.tga")
			whisperButton.SetOverVisual("d:/ymir work/ui/game/whisper/wikipedia_over.tga")
			whisperButton.SetDownVisual("d:/ymir work/ui/game/whisper/wikipedia.tga")
			whisperButton.SetToolTipTextWithColor(name, 0xffe7a83b)
		else:
			whisperButton.SetUpVisual("d:/ymir work/ui/game/windows/btn_mail_up.sub")
			whisperButton.SetOverVisual("d:/ymir work/ui/game/windows/btn_mail_up.sub")
			whisperButton.SetDownVisual("d:/ymir work/ui/game/windows/btn_mail_up.sub")
			if self.IsGameMasterName(name):
				whisperButton.SetToolTipTextWithColor(name, 0xffffa200)
			else:
				whisperButton.SetToolTipText(name)


# Interface icinde ara:
			self.MakeItemShopWindow()
			self.wndItemShop.GetWheelGiftData(int(itemVnum), int(itemCount))

# Altina ekle:
	if app.ENABLE_WIKI_SYSTEM:
		def SearchWikiForItem(self, itemVnum):
			if not itemVnum:
				return
			if self.wndWiki == None:
				self.__MakeWiki()
			if self.wndWiki:
				if not self.wndWiki.IsShow():
					self.wndWiki.Open()
				self.wndWiki.SearchItem(itemVnum)

		def SearchWikiForMob(self, mobVnum):
			if not mobVnum:
				return
			if self.wndWiki == None:
				self.__MakeWiki()
			if self.wndWiki:
				if not self.wndWiki.IsShow():
					self.wndWiki.Open()
				self.wndWiki.ShowItemInfo(mobVnum, 1)

		def OpenWikiWindow(self):
			if self.wndWiki == None:
				self.__MakeWiki()
			if self.wndWiki and self.wndWiki.IsShow():
				self.wndWiki.Close()
			elif self.wndWiki:
				self.wndWiki.Open()

		def __MakeWiki(self):
			if self.wndWiki == None:
				self.wndWiki = uiWiki.EncyclopediaofGame()
				self.wndInventory.BindWikiWindow(self.wndWiki)
				if self.wndInventoryNew:
					self.wndInventoryNew.BindWikiWindow(self.wndWiki)

		def RecvReadWiki(self):
			if app.ENABLE_WHISPER_MESSENGER:
				return
			name = "[W?K?]"
			if not self.whisperDialogDict.has_key(name):
				btn = self.__FindWhisperButton(name)
				if 0 == btn:
					btn = self.__MakeWhisperButton(name)
					btn.Flash()
					if app.ENABLE_BLINK_ALERT:
						app.FlashApplication()
					chat.AppendChat(chat.CHAT_TYPE_NOTICE, localeInfo.RECEIVE_MESSAGE % (name))
				else:
					btn.Flash()
					if app.ENABLE_BLINK_ALERT:
						app.FlashApplication()

