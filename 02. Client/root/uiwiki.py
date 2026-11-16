if __USE_DYNAMIC_MODULE__:
	import pyapi

app = __import__(pyapi.GetModuleName("app"))

import ui
import grp
import wiki
import item
import nonplayer
import renderTarget
import constInfo
import skill
import WikiUI
import localeInfo
import chat
import dbg

import uiToolTip

# if FALSE will be textline!
USE_ITEM_COUNT_NUMBER_LINE = TRUE

# if this TRUE item refine showing start index in +0 than +9 will be next item if have!
SHOW_NEXT_ITEM_REFINE = FALSE

SHOW_ITEM_LOWER_TO_BIG = FALSE

# mob_proto left out: Orman golemi, Khalyss, Am-Ani krali, Sythra, Wukong, Araf Alevi / Lanetli Agac / Kehribar /
# Capraz tas / Ay Bagli / Wukong metins, 2 relics and all 32 rare + legendary metins)
WIKI_BOSS_TIERS = (
	("WIKI_BOSS_TIER_LOW", (591, 494, 493, 492, 491, 194, 193, 192, 191)),
	("WIKI_TIER_1", (2191, 792, 691)),
	("WIKI_TIER_2", (2206, 2091, 1901, 1304)),
	("WIKI_TIER_3", (2495, 2307)),
	("WIKI_TIER_4", (3391, 3891, 3390, 3190, 3191, 3790, 3791, 3690, 3691, 3490, 3491, 3591, 3291, 3290, 3590, 3090, 3091)),
	("WIKI_TIER_5", (6407, 6393, 6391)),
	("WIKI_BOSS_TIER_MINI_DUNGEON", (4469, 4272, 6394, 6151, 4229, 2597, 1092, 7005)),
	("WIKI_BOSS_TIER_DUNGEON", (6193, 6192, 6392, 4402, 4401, 2493, 2598, 1093, 2092)),
)
WIKI_METIN_TIERS = (
	("WIKI_TIER_1", (8007, 8006, 8005)),
	("WIKI_TIER_2", (8011, 8010, 8009, 8008)),
	("WIKI_TIER_3", (8027, 8025, 8014, 8013, 8012)),
	("WIKI_TIER_4", (8055, 8054, 8052, 8051)),
	("WIKI_TIER_5", (8061, 8059)),
	("WIKI_METIN_TIER_DUNGEON", (20399, 8058, 8057, 8208, 8035, 2095, 8209)),
	("WIKI_SHRINES", (20859, 20853, 20860, 20861)),
	("WIKI_METIN_TIER_RARE", ()),
)

# category load speed
AUTOLOAD_SPEED = 0.010
AUTOLOAD_MONSTER_SPEED = 0.020

IMG_DIR = "d:/ymir work/ui/game/wiki/"
IMG_DIR_REWORK = "d:/ymir work/ui/wiki_rework/"
REWORK = "d:/ymir work/ui/game/wiki_new/"

WIKI_WIN_W = 792
WIKI_WIN_H = 516
WIKI_MAX_TABS = 6
WIKI_HOME_ARG = "System#0"
CAT_DIR = IMG_DIR + "category/"

def WikiText(text):
	try:
		import wikicontent
		return "".join(chr(wikicontent._TR_MAP.get(ord(ch), ord(ch))) for ch in text)
	except:
		return text

def WikiTr(key, default = None):
	try:
		import wikicontent
		value = wikicontent.Tr(key)
		if value and value != key:
			return value
	except:
		pass
	if key == "Guide Start":
		return key
	value = localeInfo.GetText(key, None)
	if value:
		return value
	if default != None:
		return default
	return key

WIKI_SUB_TEXT_COLOR = 0xffcabdab
WIKI_SUB_TEXT_SELECT_COLOR = 0xffc79e65

class CategoryItem(WikiUI.CategoryItem):
	# Referans: 199x39, category/btn_{norm,hover,select}.png 199x38 (chevron png icinde),
	# ikon (11,1) btn icinde dikey ortali, yazi (47,11) "  " onekli.
	def __del__(self):
		WikiUI.CategoryList.CategoryDefaultItem.__del__(self)

	def __init__(self, text, miniIconPath = None):
		WikiUI.CategoryList.CategoryDefaultItem.__init__(self)

		directionIcon = ui.ImageBox()
		directionIcon.SetParent(self)
		directionIcon.AddFlag("not_pick")
		directionIcon.SetPosition(0, 0)
		directionIcon.LoadImage(CAT_DIR + "btn_norm.png")
		directionIcon.Show()
		self.children["directionIcon"] = directionIcon

		miniIcon = ui.ImageBox()
		miniIcon.SetParent(directionIcon)
		miniIcon.AddFlag("not_pick")
		if miniIconPath:
			miniIcon.LoadImage(miniIconPath)
		else:
			miniIcon.LoadImage(IMG_DIR + "divider_small_o.tga")
		miniIcon.SetPosition(11, (directionIcon.GetHeight() - miniIcon.GetHeight()) / 2 + 1)
		miniIcon.Show()
		self.children["miniIcon"] = miniIcon

		textLine = ui.TextLine()
		textLine.SetParent(directionIcon)
		textLine.AddFlag("not_pick")
		textLine.SetPosition(47, 11)
		textLine.SetText("  " + text)
		textLine.Show()
		self.children["textLine"] = textLine

		self.SetOnExpandEvent(self.ExpandEvent)
		self.SetOnCollapseEvent(self.CollapseEvent)
		self.SetSize(199, 39)

	def __Image(self):
		if self.IsExpanded():
			return "btn_select.png"
		if self.IsIn() and (not self.parent or self.parent.IsMouseInList()):
			return "btn_hover.png"
		return "btn_norm.png"

	def RefreshImage(self):
		self.children["directionIcon"].LoadImage(CAT_DIR + self.__Image())

	def OnMouseOverIn(self):
		self.RefreshImage()

	def OnMouseOverOut(self):
		self.RefreshImage()

	def CollapseEvent(self):
		self.RefreshImage()

	def ExpandEvent(self):
		self.RefreshImage()

class CategorySubItem(WikiUI.CategorySubItem):
	# Referans: 199x24 (adim 23), category/sub_{norm,hover}.png 199x24, secili sub_select.png 201x26,
	# yazi (0,5) yatay ortali 0xffcabdab / secili 0xffc79e65, kopyala butonu (180,5) 13x13.
	def __del__(self):
		WikiUI.CategoryList.CategoryDefaultItem.__del__(self)

	def __init__(self, text):
		WikiUI.CategoryList.CategoryDefaultItem.__init__(self)

		underBoard = ui.ImageBox()
		underBoard.SetParent(self)
		underBoard.AddFlag("not_pick")
		underBoard.SetPosition(0, 0)
		underBoard.Hide()
		self.children["underBoard"] = underBoard

		directionIcon = ui.ImageBox()
		directionIcon.SetParent(self)
		directionIcon.AddFlag("not_pick")
		directionIcon.SetPosition(0, 0)
		directionIcon.LoadImage(CAT_DIR + "sub_norm.png")
		directionIcon.Show()
		self.children["directionIcon"] = directionIcon

		textLine = ui.TextLine()
		textLine.SetParent(self)
		textLine.AddFlag("not_pick")
		textLine.SetPosition(0, 5)
		textLine.SetWindowHorizontalAlignCenter()
		textLine.SetHorizontalAlignCenter()
		textLine.SetPackedFontColor(WIKI_SUB_TEXT_COLOR)
		textLine.SetText("  " + text)
		textLine.Show()
		self.children["textLine"] = textLine

		copyButton = ui.Button()
		copyButton.SetParent(self)
		copyButton.SetUpVisual(IMG_DIR + "button_copylink_norm.png")
		copyButton.SetOverVisual(IMG_DIR + "button_copylink_over.png")
		copyButton.SetDownVisual(IMG_DIR + "button_copylink_down.png")
		copyButton.SetPosition(180, 5)
		copyButton.SAFE_SetEvent(self.OnClickCopy)
		copyButton.Show()
		self.children["copyButton"] = copyButton

		self.SetOnExpandEvent(self.ExpandEvent)
		self.SetOnCollapseEvent(self.CollapseEvent)
		self.SetSize(199, 24)

	def OnClickCopy(self):
		if self.parent and not self.parent.IsMouseInList():
			return
		self.OnSelect()

	def RefreshImage(self):
		if self.IsExpanded():
			self.children["directionIcon"].LoadImage(CAT_DIR + "sub_select.png")
			self.children["textLine"].SetPackedFontColor(WIKI_SUB_TEXT_SELECT_COLOR)
		else:
			if self.IsIn() and (not self.parent or self.parent.IsMouseInList()):
				self.children["directionIcon"].LoadImage(CAT_DIR + "sub_hover.png")
			else:
				self.children["directionIcon"].LoadImage(CAT_DIR + "sub_norm.png")
			self.children["textLine"].SetPackedFontColor(WIKI_SUB_TEXT_COLOR)

	def OnMouseOverIn(self):
		self.RefreshImage()

	def OnMouseOverOut(self):
		self.RefreshImage()

	def CollapseEvent(self):
		self.RefreshImage()

	def ExpandEvent(self):
		self.RefreshImage()

class TabCloseButton(ui.Window):
	# Sekme kapatma: referansta resim degil "x" yazisi (0xffe1c29c).
	def __init__(self):
		ui.Window.__init__(self)
		self.event = None
		self.arg = None
		self.SetSize(10, 15)
		closeText = ui.TextLine()
		closeText.SetParent(self)
		closeText.AddFlag("not_pick")
		closeText.SetPosition(0, 0)
		closeText.SetPackedFontColor(0xffe1c29c)
		closeText.SetText("x")
		closeText.Show()
		self.closeText = closeText

	def __del__(self):
		ui.Window.__del__(self)

	def SetEvent(self, event, arg):
		self.event = event
		self.arg = arg

	def OnMouseLeftButtonUp(self):
		if self.event:
			self.event(self.arg)

class DropDownRow(ui.Window):
	def __init__(self, dropDown, index, label, width):
		ui.Window.__init__(self)
		self.dropDown = dropDown
		self.index = index
		self.SetParent(dropDown)
		self.SetPosition(1, 1 + index * DropDown.ROW_H)
		self.SetSize(width - 2, DropDown.ROW_H)

		hover = ui.Bar()
		hover.SetParent(self)
		hover.SetPosition(0, 0)
		hover.SetSize(width - 2, DropDown.ROW_H)
		hover.SetColor(0x55cebb98)
		hover.AddFlag("not_pick")
		hover.Hide()
		self.hover = hover

		textLine = ui.TextLine()
		textLine.SetParent(self)
		textLine.AddFlag("not_pick")
		textLine.SetPosition(5, 3)
		textLine.SetPackedFontColor(0xffcebb98)
		textLine.SetText(label)
		textLine.Show()
		self.textLine = textLine
		self.Show()

	def __del__(self):
		ui.Window.__del__(self)

	def OnMouseOverIn(self):
		self.hover.Show()

	def OnMouseOverOut(self):
		self.hover.Hide()

	def OnMouseLeftButtonDown(self):
		self.dropDown.OnSelectRow(self.index)

class DropDown(ui.Window):
	# Arama onerileri listesi (referans uiWiki.DropDown)
	ROW_H = 18

	def __init__(self):
		ui.Window.__init__(self)
		self.rows = []
		self.items = []
		self.selectEvent = None

		border = ui.Bar()
		border.SetParent(self)
		border.SetPosition(0, 0)
		border.SetColor(0xff4a3d2e)
		border.AddFlag("not_pick")
		border.Show()
		self.border = border

		board = ui.Bar()
		board.SetParent(self)
		board.SetPosition(1, 1)
		board.SetColor(0xf0120d0a)
		board.AddFlag("not_pick")
		board.Show()
		self.board = board
		self.Hide()

	def __del__(self):
		ui.Window.__del__(self)

	def SetSelectEvent(self, event):
		self.selectEvent = event

	def Clear(self):
		for row in self.rows:
			row.Hide()
		self.rows = []
		self.items = []
		self.Hide()

	def SetItems(self, items, width):
		self.Clear()
		if len(items) == 0:
			return
		self.items = items
		height = len(items) * DropDown.ROW_H + 2
		self.SetSize(width, height)
		self.border.SetSize(width, height)
		self.board.SetSize(width - 2, height - 2)
		for index in xrange(len(items)):
			self.rows.append(DropDownRow(self, index, items[index][0], width))
		self.Show()
		self.SetTop()

	def OnSelectRow(self, index):
		if index < 0 or index >= len(self.items):
			return
		if self.selectEvent:
			self.selectEvent(self.items[index][1], self.items[index][0])

class EncyclopediaofGame(ui.ScriptWindow):
	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Destroy(self):
		if self.children.has_key("listBoxCube"):
			self.children["listBoxCube"].ClearItem()
			self.children["listBoxCube"]=None
			del self.children["listBoxCube"]

		if self.children.has_key("resultpageListbox"):
			self.children["resultpageListbox"].RemoveAllItems()
			self.children["resultpageListbox"]=None
			del self.children["resultpageListbox"]

		self.selectArg = ""
		self.AIAppendAlgoritm = None

		if len(self.children) != 0:
			ui.ScriptWindow.Destroy(self)
			constInfo.SetMainParent(None)
			constInfo.SetListBox(None)

		self.children = {}

	def __init__(self):
		self.tierVnums = ()
		self.petSizes = (0, 0)
		ui.ScriptWindow.__init__(self)
		self.SetWindowName("EncyclopediaofGame")
		self.AddFlag("movable")
		self.AddFlag("float")

		self.wikiW = WIKI_WIN_W
		self.wikiH = WIKI_WIN_H
		self.resizing = FALSE
		self.resizeStart = (0, 0, WIKI_WIN_W, WIKI_WIN_H)
		self.previewSize = (WIKI_WIN_W, WIKI_WIN_H)
		self.tabs = []
		self.curTab = 0
		self.argTitles = {}
		self.selectArg = ""
		self.AIAppendAlgoritm = None

		self.RealBoard = ui.Board()
		self.RealBoard.SetParent(self)
		self.RealBoard.SetSize(WIKI_WIN_W, WIKI_WIN_H)
		self.RealBoard.SetPosition(0, 0)
		self.RealBoard.Show()

		self.titleBar = ui.TitleBar()
		self.titleBar.SetParent(self)
		self.titleBar.MakeTitleBar(0, "red")
		self.titleBar.SetPosition(8, 7)
		self.titleBar.SetWidth(WIKI_WIN_W - 15)
		self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))
		self.titleBar.Show()

		self.titleName = ui.TextLine()
		self.titleName.SetParent(self.titleBar)
		self.titleName.SetPosition(0, 4)
		self.titleName.SetText(WikiTr("WIKI_TITLE", localeInfo.WIKI_TITLE))
		self.titleName.SetWindowHorizontalAlignCenter()
		self.titleName.SetHorizontalAlignCenter()
		self.titleName.Show()

		self.children = {}

		self.Destroy()

		# Default variable
		self.children["characterIndex"] = 0

		bgImage = ui.ExpandedImageBox()
		bgImage.SetParent(self)
		bgImage.AddFlag("not_pick")
		bgImage.SetPosition(8, 57)
		bgImage.LoadImage(IMG_DIR + "bg.png")
		bgImage.Show()
		self.children["bgImage"] = bgImage

		self.Initialize()

	def Initialize(self):
		self.SetSize(self.wikiW, self.wikiH)
		self.SetCenterPosition()

		self.LoadSearchInfos()
		self.LoadHistoryButtons()
		self.LoadCategoryInfos()
		self.LoadBlock()
		self.LoadResultPage()
		self.LoadTabBar()
		self.LoadToolButtons()
		self.LayoutShell(self.wikiW, self.wikiH)
		self.SelectTab(0, TRUE)

	def LoadResultPage(self):
		resultPageImage = ui.Window()
		resultPageImage.SetParent(self)
		resultPageImage.SetSize(541, 369)
		resultPageImage.SetPosition(223, 131)
		resultPageImage.Show()
		self.children["resultPageImage"] = resultPageImage

		for j in xrange(4):
			characterBtn = ui.RadioButton()
			characterBtn.SetParent(resultPageImage)
			characterBtn.SetEvent(ui.__mem_func__(self.__SelectCharacters), j)
			characterBtn.SetUpVisual(IMG_DIR + "character/%d_0.tga" % j)
			characterBtn.SetOverVisual(IMG_DIR + "character/%d_1.tga" % j)
			characterBtn.SetDownVisual(IMG_DIR + "character/%d_2.tga" % j)
			characterBtn.SetPosition(18 + (132 * j), 6)
			characterBtn.Hide()
			self.children["job_%d_characterBtn" % j] = characterBtn

		resultpageListboxScrollbar = WikiUI.ScrollBarNew()
		resultpageListboxScrollbar.SetParent(self)
		self.children["resultpageListboxScrollbar"] = resultpageListboxScrollbar

		resultpageListbox = WikiUI.ListBox()
		resultpageListbox.SetParent(self)
		resultpageListbox.SetScrollBar(resultpageListboxScrollbar)
		self.children["resultpageListbox"] = resultpageListbox

		constInfo.SetMainParent(self)
		constInfo.SetListBox(resultpageListbox)

		# Referans: sabit "Wikipedia" banner'i (222,59) 559x67; tiklayinca ana sayfa.
		# ArticleGUI banner_img tokeni ayni nesneyi kullanir.
		resultpagebtn = ui.ExpandedImageBox()
		resultpagebtn.SetParent(self)
		resultpagebtn.SetPosition(222, 59)
		resultpagebtn.LoadImage(IMG_DIR + "banner.png")
		resultpagebtn.SetEvent(ui.__mem_func__(self.LoadGuidePage), "mouse_click")
		resultpagebtn.Show()
		self.children["resultpagebtn"] = resultpagebtn

	def LoadGuidePage(self, emptyArg = ""):
		self.__SelectType(WIKI_HOME_ARG, FALSE, TRUE)

	def LoadBlock(self):
		blockImage = ui.ImageBox()
		blockImage.SetParent(self)
		blockImage.LoadImage(IMG_DIR+"block.tga")
		blockImage.SetPosition(140,32)
		blockImage.Hide()
		self.children["blockImage"] = blockImage

	def LoadSearchInfos(self):
		self.children["selectedMob"] = 0
		self.children["selectedItem"] = 0

		# Referans: arama kutusu search.png (15,69) 185x23, yazi (21,74), temizle x (165,69) 10x23,
		# arama butonu (182,67) 30x27.
		searchSlot = ui.ImageBox()
		searchSlot.SetParent(self)
		searchSlot.SetPosition(15, 69)
		searchSlot.LoadImage(IMG_DIR + "search.png")
		searchSlot.Show()
		self.children["searchSlot"] = searchSlot

		searchItemName = ui.EditLine()
		searchItemName.SetParent(self)
		searchItemName.SetPosition(21, 74)
		searchItemName.SetSize(142, 16)
		searchItemName.SetInfoMessage(WikiTr("WIKI_ITEM_NAME", localeInfo.AUTO_ITEM_ADI))
		searchItemName.SetMax(30)
		searchItemName.isNeedEmpty = FALSE
		searchItemName.OnPressEscapeKey = ui.__mem_func__(self.Close)
		searchItemName.OnIMEUpdate = ui.__mem_func__(self.__OnValueUpdateItem)
		searchItemName.SetReturnEvent(ui.__mem_func__(self.StartSearchItem))
		searchItemName.Show()
		self.children["searchItemName"] = searchItemName

		searchClearBtn = ui.Button()
		searchClearBtn.SetParent(self)
		searchClearBtn.SetUpVisual(IMG_DIR + "x_btn_default.png")
		searchClearBtn.SetOverVisual(IMG_DIR + "x_btn_hover.png")
		searchClearBtn.SetDownVisual(IMG_DIR + "x_btn_down.png")
		searchClearBtn.SetPosition(165, 69)
		searchClearBtn.SAFE_SetEvent(self.ClearEditlineItem)
		searchClearBtn.Hide()
		self.children["searchClearBtn"] = searchClearBtn

		searchButton = ui.Button()
		searchButton.SetParent(self)
		searchButton.SetUpVisual(IMG_DIR + "btn_search_norm.png")
		searchButton.SetOverVisual(IMG_DIR + "btn_search_hover.png")
		searchButton.SetDownVisual(IMG_DIR + "btn_search_select.png")
		searchButton.SAFE_SetEvent(self.StartSearchItem)
		searchButton.SetPosition(182, 67)
		searchButton.Show()
		self.children["searchButton"] = searchButton

		dropDown = DropDown()
		dropDown.SetParent(self)
		dropDown.SetPosition(15, 93)
		dropDown.SetSelectEvent(self.OnSelectSearchRow)
		dropDown.Hide()
		self.children["dropDown"] = dropDown

		# Eski canavar arama kutusu: referansta yok, gizli tutuluyor (Close/ClearEditlineMob uyumu).
		mobSlot = ui.ImageBox()
		mobSlot.SetParent(self)
		mobSlot.LoadImage(IMG_DIR + "search_slot.tga")
		mobSlot.SetPosition(13, 61)
		mobSlot.Hide()
		self.children["mobSlot"] = mobSlot

		searchButtonMob = ui.Button()
		searchButtonMob.SetParent(mobSlot)
		searchButtonMob.SetUpVisual(IMG_DIR + "button_0.tga")
		searchButtonMob.SetOverVisual(IMG_DIR + "button_1.tga")
		searchButtonMob.SetDownVisual(IMG_DIR + "button_2.tga")
		searchButtonMob.SAFE_SetEvent(self.StartSearchMob)
		searchButtonMob.SetPosition(91, 2)
		searchButtonMob.Show()
		self.children["searchButtonMob"] = searchButtonMob

		searchMobName = ui.EditLine()
		searchMobName.SetParent(mobSlot)
		searchMobName.SetPosition(2, 5)
		searchMobName.SetSize(91, 26)
		searchMobName.SetInfoMessage(localeInfo.WIKI_MOB_NAME)
		searchMobName.isNeedEmpty = FALSE
		searchMobName.SetMax(30)
		searchMobName.SetOutline()
		searchMobName.OnPressEscapeKey = ui.__mem_func__(self.Close)
		searchMobName.OnIMEUpdate = ui.__mem_func__(self.__OnValueUpdateMob)
		searchMobName.SetReturnEvent(ui.__mem_func__(self.StartSearchMob))
		searchMobName.Show()
		self.children["searchMobName"] = searchMobName

		searchClearBtnMob = ui.Button()
		searchClearBtnMob.SetParent(mobSlot)
		searchClearBtnMob.SetUpVisual(IMG_DIR + "clear_button_1.tga")
		searchClearBtnMob.SetOverVisual(IMG_DIR + "clear_button_2.tga")
		searchClearBtnMob.SetDownVisual(IMG_DIR + "clear_button_1.tga")
		searchClearBtnMob.SetPosition(75, 5)
		searchClearBtnMob.SAFE_SetEvent(self.ClearEditlineMob)
		searchClearBtnMob.Hide()
		self.children["searchClearBtnMob"] = searchClearBtnMob

	def SetHistoryButtons(self):
		if not self.children.has_key("historyBack"):
			return
		historySearch = self.children["historySearch"]
		currentIndex = self.children["currentIndex"]
		canBack = currentIndex > 0
		canNext = (currentIndex + 1) < len(historySearch)
		for (key, can) in (("historyBack", canBack), ("historyNext", canNext)):
			btn = self.children[key]
			if can:
				btn.Enable()
			else:
				btn.Disable()
			try:
				if can:
					btn.SetAlpha(1.0)
				else:
					btn.SetAlpha(0.45)
			except:
				pass

	def RunHistoryArgument(self, argument, isHistory = FALSE):
		if argument.find("NEW") != -1:
			argumentList = argument.split("#")
			self.ShowItemInfo(int(argumentList[1]), int(argumentList[2]), isHistory)
		else:
			self.__SelectType(argument, FALSE, isHistory)

	def ClickBackHistory(self):
		currentIndex = self.children["currentIndex"]
		historySearch = self.children["historySearch"]

		if currentIndex - 1 < 0:
			return

		currentIndex -= 1
		self.children["currentIndex"] = currentIndex
		self.selectArg = ""
		self.RunHistoryArgument(historySearch[currentIndex])
		self.SetHistoryButtons()

	def ClickNextHistory(self):
		currentIndex = self.children["currentIndex"]
		historySearch = self.children["historySearch"]

		if currentIndex + 1 >= len(historySearch):
			return

		currentIndex += 1
		self.children["currentIndex"] = currentIndex
		self.selectArg = ""
		self.RunHistoryArgument(historySearch[currentIndex])
		self.SetHistoryButtons()

	def get_length(self, x):
		return len(x[0])

	def UpdateItemsList(self):
		input_text_real = self.children["searchItemName"].GetText()
		input_len = len(input_text_real)

		if input_len == 0:
			self.ClearEditlineItem()
			return FALSE
		if localeInfo.IsARABIC():
			input_text = input_text_real
		else:
			input_text = input_text_real.lower()
		if self.children.has_key("searchClearBtn"):
			self.children["searchClearBtn"].Show()
		items_list = item.GetItemsByName(str(input_text))
		itemList = []
		namesList = []

		for i, itemVnum in enumerate(items_list, start = 1):
			(realVnum, isRefineItem) = WikiUI.getRealVnum(itemVnum)
			if isRefineItem:
				realVnum += wiki.GetRefineMaxLevel(realVnum)
				if itemVnum != realVnum:
					continue
			item.SelectItem(itemVnum)
			if localeInfo.IsARABIC():
				itemName = item.GetItemName()
			else:
				itemName = item.GetItemName().lower()
			if itemName.find("+") != -1:
				itemName = itemName[:itemName.find("+")]
			tempName = list(itemName)
			for i in xrange(input_len):
				tempName[i] = list(input_text_real)[i]
			itemName = ""
			for x in xrange(len(tempName)):
				itemName += tempName[x]
			if itemName in namesList:
				continue
			namesList.append(itemName)
			itemList.append([itemName, realVnum])

		if len(itemList) > 0:
			if len(itemList) > 1:
				itemList = sorted(itemList, key = self.get_length, reverse = FALSE)
			self.children["selectedItem"] = itemList[0][1]
			self.children["searchItemName"].SetInfoMessage(itemList[0][0])
		else:
			self.children["selectedItem"] = 0
			self.children["searchItemName"].SetInfoMessage("")
		self.__FillDropDown(itemList, input_text_real)
		return TRUE

	def __OnValueUpdateItem(self):
		ui.EditLine.OnIMEUpdate(self.children["searchItemName"])
		if not self.UpdateItemsList():
			self.ClearEditlineItem()

		def OnKeyDown(self, key):
			if app.DIK_RETURN == key:
				if self.children["selectedItem"] > 1:
					self.StartSearchItem()
				else:
					self.StartSearchItem()
					return TRUE
			return TRUE

	def ClearEditlineItem(self):
		self.children["selectedItem"] = 0
		self.children["searchItemName"].SetText("")
		self.children["searchItemName"].SetInfoMessage(WikiTr("WIKI_ITEM_NAME", localeInfo.AUTO_ITEM_ADI))
		if self.children.has_key("searchClearBtn"):
			self.children["searchClearBtn"].Hide()
		self.__ClearDropDown()

	def StartSearchItem(self):
		self.__ClearDropDown()
		if self.children["selectedItem"] != 0:
			self.ShowItemInfo(self.children["selectedItem"], 0)

	def SearchItem(self, itemVnum):
		item.SelectItem(itemVnum)

		itemName = item.GetItemName()
		if item.GetItemType() == item.ITEM_TYPE_WEAPON or item.GetItemType() == item.ITEM_TYPE_ARMOR:
			refinePos = itemName.find('+')
			if refinePos > 0:
				itemName = itemName[:refinePos]

		self.children["searchItemName"].SetText(itemName)
		self.UpdateItemsList()

		self.ShowItemInfo(self.children["selectedItem"],0)

	def UpdateMobsList(self):
		input_text_real = self.children["searchMobName"].GetText()
		input_len = len(input_text_real)

		if input_len == 0:
			self.ClearEditlineMob()
			return FALSE
		if localeInfo.IsARABIC():
			input_text = input_text_real
		else:
			input_text = input_text_real.lower()
		self.children["searchClearBtnMob"].Show()
		mobs_list = nonplayer.GetMobsByName(str(input_text))
		mobList = []
		namesList = []
		for i, mobVnum in enumerate(mobs_list, start=1):
			if localeInfo.IsARABIC():
				mob_name = nonplayer.GetMonsterName(mobVnum)
			else:
				mob_name = nonplayer.GetMonsterName(mobVnum).lower()
			tempName = list(mob_name)
			for i in xrange(input_len):
				tempName[i]=list(input_text_real)[i]
			mob_name = ""
			for x in xrange(len(tempName)):
				mob_name+=tempName[x]
			if mob_name in namesList:
				continue
			namesList.append(mob_name)
			mobList.append([mob_name, mobVnum])
		if len(mobList) > 0:
			if len(mobList) > 1:
				mobList = sorted(mobList, key = self.get_length, reverse = FALSE)
			self.children["selectedMob"] = mobList[0][1]
			self.children["searchMobName"].SetInfoMessage(mobList[0][0])
		else:
			self.children["selectedMob"] = 0
			self.children["searchMobName"].SetInfoMessage("")
		return TRUE

	def __OnValueUpdateMob(self):
		ui.EditLine.OnIMEUpdate(self.children["searchMobName"])
		if not self.UpdateMobsList():
			self.ClearEditlineMob()

		def OnKeyDown(self, key):
			if app.DIK_RETURN == key:
				if self.children["selectedMob"] > 1:
					self.StartSearchMob()
				else:
					self.StartSearchMob()
					return TRUE
			return TRUE

	def ClearEditlineMob(self):
		self.children["selectedMob"] = 0
		self.children["searchMobName"].SetText("")
		self.children["searchMobName"].SetInfoMessage(localeInfo.WIKI_MOB_NAME)
		self.children["searchClearBtnMob"].Hide()

	def StartSearchMob(self):
		if self.children["selectedMob"] != 0:
			self.ShowItemInfo(self.children["selectedMob"], 1)

	def LoadCategoryInfos(self):
		# Referans: kategori listesi (11,132) 199x369, scrollbar (212,132) 369
		scrollBarListBoxCube = WikiUI.ScrollBarNew()
		scrollBarListBoxCube.SetParent(self)
		scrollBarListBoxCube.SetPosition(212, 132)
		scrollBarListBoxCube.Show()
		self.children["scrollBarListBoxCube"] = scrollBarListBoxCube

		listBoxCube = WikiUI.CategoryList()
		listBoxCube.SetParent(self)
		listBoxCube.SetPosition(11, 132)
		listBoxCube.SetSize(199, 369)
		listBoxCube.Show()
		listBoxCube.SetScrollBar(scrollBarListBoxCube)
		self.children["listBoxCube"] = listBoxCube
		scrollBarListBoxCube.SetScrollBarSize(369)

		self.children["listBoxCube"].AppendItemList(self.__BuildCategoryTree())

	def LoadHistoryButtons(self):
		self.children["historySearch"] = []
		self.children["currentIndex"] = 0

		# Referans: geri (15,102), ileri (50,102) 29x28
		historyBack = ui.Button()
		historyBack.SetParent(self)
		historyBack.SetUpVisual(IMG_DIR + "btn_left_norm.png")
		historyBack.SetOverVisual(IMG_DIR + "btn_left_hover.png")
		historyBack.SetDownVisual(IMG_DIR + "btn_left_select.png")
		historyBack.SetDisableVisual(IMG_DIR + "btn_left_norm.png")
		historyBack.SetPosition(15, 102)
		historyBack.SAFE_SetEvent(self.ClickBackHistory)
		historyBack.Show()
		self.children["historyBack"] = historyBack

		historyNext = ui.Button()
		historyNext.SetParent(self)
		historyNext.SetUpVisual(IMG_DIR + "btn_right_norm.png")
		historyNext.SetOverVisual(IMG_DIR + "btn_right_hover.png")
		historyNext.SetDownVisual(IMG_DIR + "btn_right_select.png")
		historyNext.SetDisableVisual(IMG_DIR + "btn_right_norm.png")
		historyNext.SetPosition(50, 102)
		historyNext.SAFE_SetEvent(self.ClickNextHistory)
		historyNext.Show()
		self.children["historyNext"] = historyNext

	def LoadToolButtons(self):
		# Yenile ikonu (236,125)
		refreshBtn = ui.Button()
		refreshBtn.SetParent(self)
		refreshBtn.SetUpVisual("d:/ymir work/ui/game/common/refresh_norm.png")
		refreshBtn.SetOverVisual("d:/ymir work/ui/game/common/refresh_hover.png")
		refreshBtn.SetDownVisual("d:/ymir work/ui/game/common/refresh_select.png")
		refreshBtn.SetPosition(236, 125)
		refreshBtn.SAFE_SetEvent(self.RefreshCurrentPage)
		refreshBtn.Hide()
		self.children["refreshBtn"] = refreshBtn

		toTopBtn = ui.Button()
		toTopBtn.SetParent(self)
		toTopBtn.SetUpVisual(IMG_DIR + "btn_to_top_norm.png")
		toTopBtn.SetOverVisual(IMG_DIR + "btn_to_top_hover.png")
		toTopBtn.SetDownVisual(IMG_DIR + "btn_to_top_select.png")
		toTopBtn.SetPosition(WIKI_WIN_W - 77, WIKI_WIN_H - 81)
		toTopBtn.SAFE_SetEvent(self.ScrollArticleToTop)
		toTopBtn.Hide()
		self.children["toTopBtn"] = toTopBtn

		# Yeniden boyutlandirma tutamagi (sag alt)
		grip = ui.Window()
		grip.SetParent(self)
		grip.SetSize(16, 16)
		grip.SetPosition(WIKI_WIN_W - 18, WIKI_WIN_H - 18)
		grip.OnMouseLeftButtonDown = ui.__mem_func__(self.__OnGripDown)
		grip.OnMouseLeftButtonUp = ui.__mem_func__(self.__OnGripUp)
		grip.Show()
		self.children["resizeGrip"] = grip

		for key in ("rpTop", "rpBottom", "rpLeft", "rpRight"):
			bar = ui.Bar()
			bar.SetColor(0xffcebb98)
			bar.AddFlag("not_pick")
			bar.Hide()
			self.children[key] = bar

	# ---- layout / resize ------------------------------------------------
	def LayoutShell(self, w, h):
		self.wikiW = w
		self.wikiH = h
		self.SetSize(w, h)
		self.RealBoard.SetSize(w, h)
		self.titleBar.SetWidth(w - 15)
		self.children["bgImage"].SetScale((w - 17) / 775.0, (h - 66) / 450.0)

		listBoxCube = self.children["listBoxCube"]
		listBoxCube.SetSize(199, h - 147)
		self.children["scrollBarListBoxCube"].SetScrollBarSize(h - 147)
		listBoxCube.RefreshList()

		self.children["resultPageImage"].SetSize(w - 251, h - 147)
		self.children["toTopBtn"].SetPosition(w - 77, h - 81)
		self.children["resizeGrip"].SetPosition(w - 18, h - 18)
		self.__ResetBanner()

	def ClampWikiSize(self, w, h):
		import wndMgr
		maxW = max(WIKI_WIN_W, wndMgr.GetScreenWidth() - 20)
		maxH = max(WIKI_WIN_H, wndMgr.GetScreenHeight() - 20)
		w = max(WIKI_WIN_W, min(int(w), maxW))
		h = max(WIKI_WIN_H, min(int(h), maxH))
		return (w, h)

	def ShowResizePreview(self, w, h):
		(x, y) = self.GetGlobalPosition()
		edges = (("rpTop", x, y, w, 2), ("rpBottom", x, y + h - 2, w, 2), ("rpLeft", x, y, 2, h), ("rpRight", x + w - 2, y, 2, h))
		for (key, ex, ey, ew, eh) in edges:
			bar = self.children[key]
			bar.SetPosition(ex, ey)
			bar.SetSize(ew, eh)
			bar.Show()
			bar.SetTop()

	def HideResizePreview(self):
		for key in ("rpTop", "rpBottom", "rpLeft", "rpRight"):
			if self.children.has_key(key):
				self.children[key].Hide()

	def __OnGripDown(self):
		import wndMgr
		(mx, my) = wndMgr.GetMousePosition()
		self.resizing = TRUE
		self.resizeStart = (mx, my, self.wikiW, self.wikiH)
		self.previewSize = (self.wikiW, self.wikiH)
		self.ShowResizePreview(self.wikiW, self.wikiH)

	def __OnGripUp(self):
		if not self.resizing:
			return
		self.resizing = FALSE
		self.HideResizePreview()
		self.OnResize(self.previewSize[0], self.previewSize[1])

	def __UpdateResizeDrag(self):
		if not self.resizing:
			return
		import wndMgr
		(mx, my) = wndMgr.GetMousePosition()
		(sx, sy, sw, sh) = self.resizeStart
		size = self.ClampWikiSize(sw + (mx - sx), sh + (my - sy))
		if size != self.previewSize:
			self.previewSize = size
			self.ShowResizePreview(size[0], size[1])

	def OnResize(self, w, h):
		(w, h) = self.ClampWikiSize(w, h)
		if w == self.wikiW and h == self.wikiH:
			return
		self.LayoutShell(w, h)
		self.RefreshCurrentPage()

	def __ResetBanner(self):
		banner = self.children["resultpagebtn"]
		banner.LoadImage(IMG_DIR + "banner.png")
		banner.SetScale((self.wikiW - 233) / 559.0, 1.0)
		banner.Show()

	# ---- tabs -------------------------------------------------------------
	def LoadTabBar(self):
		plusBtn = ui.Button()
		plusBtn.SetParent(self)
		plusBtn.SetUpVisual(IMG_DIR + "plus_btn_norm.png")
		plusBtn.SetOverVisual(IMG_DIR + "plus_btn_hover.png")
		plusBtn.SetDownVisual(IMG_DIR + "plus_btn_select.png")
		plusBtn.SetPosition(132, 30)
		plusBtn.SAFE_SetEvent(self.OpenNewTab)
		plusBtn.Show()
		self.children["tabPlus"] = plusBtn
		self.tabs = [self.__CreateTab()]
		self.curTab = 0
		self.__RelayoutTabs()

	def __CreateTab(self):
		btn = ui.RadioButton()
		btn.SetParent(self)
		btn.SetUpVisual(IMG_DIR + "tab_norm.png")
		btn.SetOverVisual(IMG_DIR + "tab_hover.png")
		btn.SetDownVisual(IMG_DIR + "tab_select.png")
		btn.Show()

		text = ui.TextLine()
		text.SetParent(btn)
		text.AddFlag("not_pick")
		text.SetPosition(8, 5)
		text.SetText(WikiTr("WIKI_HOME", localeInfo.WIKI_HOME))
		text.Show()

		close = TabCloseButton()
		close.SetParent(self)
		close.Show()

		return {"title" : WikiTr("WIKI_HOME", localeInfo.WIKI_HOME), "history" : [], "index" : 0, "btn" : btn, "text" : text, "close" : close}

	def __RelayoutTabs(self):
		for i in xrange(len(self.tabs)):
			tab = self.tabs[i]
			x = 10 + i * 122
			tab["btn"].SetPosition(x, 30)
			tab["btn"].SAFE_SetEvent(self.SelectTab, i)
			tab["close"].SetPosition(x + 107, 34)
			tab["close"].SetEvent(ui.__mem_func__(self.CloseTab), i)
			tab["close"].SetTop()
			if i == self.curTab:
				tab["btn"].Down()
				tab["text"].SetPackedFontColor(0xfff1d0a3)
			else:
				tab["btn"].SetUp()
				tab["text"].SetPackedFontColor(0xffcabdab)
		self.children["tabPlus"].SetPosition(10 + len(self.tabs) * 122, 30)
		if len(self.tabs) >= WIKI_MAX_TABS:
			self.children["tabPlus"].Hide()
		else:
			self.children["tabPlus"].Show()

	def __SetTabTitle(self, title, showLink):
		if self.curTab < len(self.tabs):
			tab = self.tabs[self.curTab]
			tab["title"] = title
			shown = title
			if len(shown) > 13:
				shown = shown[:12] + ".."
			tab["text"].SetText(shown)

	def __ArgToTitle(self, arg):
		if arg == "System#122":
			return localeInfo.AUTO_GUIDE_START
		if arg == WIKI_HOME_ARG:
			return WikiTr("WIKI_HOME", localeInfo.WIKI_HOME)
		if self.argTitles.has_key(arg):
			return self.argTitles[arg]
		return arg.split("#")[0]

	def SaveCurrentTabState(self):
		if self.curTab < len(self.tabs):
			tab = self.tabs[self.curTab]
			tab["history"] = self.children["historySearch"]
			tab["index"] = self.children["currentIndex"]

	def ApplyTabState(self):
		tab = self.tabs[self.curTab]
		self.children["historySearch"] = tab["history"]
		self.children["currentIndex"] = tab["index"]
		self.selectArg = ""
		self.__RelayoutTabs()
		if len(tab["history"]) == 0:
			self.__SelectType(WIKI_HOME_ARG, FALSE, TRUE)
		else:
			self.RunHistoryArgument(tab["history"][tab["index"]])
		self.SetHistoryButtons()

	def SelectTab(self, index, force = FALSE):
		if index < 0 or index >= len(self.tabs):
			return
		if index == self.curTab and not force:
			return
		if not force:
			self.SaveCurrentTabState()
		self.curTab = index
		self.ApplyTabState()

	def OpenNewTab(self, argument = None):
		if len(self.tabs) >= WIKI_MAX_TABS:
			return
		self.SaveCurrentTabState()
		self.tabs.append(self.__CreateTab())
		self.curTab = len(self.tabs) - 1
		tab = self.tabs[self.curTab]
		self.children["historySearch"] = tab["history"]
		self.children["currentIndex"] = 0
		self.selectArg = ""
		self.__RelayoutTabs()
		if argument == None or argument == "":
			argument = WIKI_HOME_ARG
		self.RunHistoryArgument(argument, TRUE)
		self.SetHistoryButtons()

	def CloseTab(self, index):
		if index < 0 or index >= len(self.tabs):
			return
		if len(self.tabs) <= 1:
			# son sekme: ana sayfaya sifirla
			tab = self.tabs[0]
			tab["history"] = []
			tab["index"] = 0
			self.curTab = 0
			self.ApplyTabState()
			return
		tab = self.tabs.pop(index)
		tab["btn"].Hide()
		tab["close"].Hide()
		tab["text"].Hide()
		tab["btn"] = None
		tab["close"] = None
		tab["text"] = None
		if index == self.curTab:
			self.curTab = min(index, len(self.tabs) - 1)
			self.ApplyTabState()
			return
		if index < self.curTab:
			self.curTab -= 1
		self.__RelayoutTabs()

	# ---- search dropdown ---------------------------------------------------
	def __ClearDropDown(self):
		if self.children.has_key("dropDown"):
			self.children["dropDown"].Clear()

	def __FillDropDown(self, itemList, query = ""):
		items = []
		for entry in itemList[:8]:
			vnum = entry[1]
			try:
				item.SelectItem(vnum)
				name = item.GetItemName()
			except:
				continue
			plusPos = name.find("+")
			if plusPos > 0:
				name = name[:plusPos]
			items.append((name, vnum))
		# guide / system makalelerini de oneri listesine ekle (payload = "System#<id>")
		try:
			if query:
				import wikicontent
				room = max(0, 8 - len(items))
				if room > 0:
					for (aid, title) in wikicontent.SearchArticles(query, room):
						label = title if len(title) <= 24 else title[:23] + "."
						items.append((label, "System#%d" % int(aid)))
		except:
			pass
		self.children["dropDown"].SetItems(items, 167)

	def OnSelectSearchRow(self, payload, name):
		self.__ClearDropDown()
		# makale secimi: payload "System#<id>" (str) -> ilgili wiki sayfasini ac
		if isinstance(payload, str):
			self.children["searchItemName"].SetText("")
			self.children["searchItemName"].SetInfoMessage(WikiTr("WIKI_ITEM_NAME", localeInfo.AUTO_ITEM_ADI) + "...")
			self.children["selectedItem"] = 0
			self.__SelectType(payload)
			return
		self.children["searchItemName"].SetText(name)
		self.children["selectedItem"] = payload
		self.ShowItemInfo(payload, 0)

	# ---- categories ---------------------------------------------------------
	def __BuildCategoryTree(self):
		self.argTitles = {}

		def Sub(text, arg):
			self.argTitles[arg] = text
			return {'item' : self.CreateCategorySubItem(text, lambda arg = arg: self.__SelectType(arg))}

		def Cat(text, iconName, subList):
			children = []
			for (subText, subArg) in subList:
				children.append(Sub(subText, subArg))
			return {'item' : self.CreateCategoryItem(text, lambda arg = (""): self.__EmptyFunction(arg), miniIconPath = CAT_DIR + "icons/" + iconName + ".png"), 'children' : tuple(children)}

		tree = []
		equip = [("WIKI_EQUIPMENT_WEAPONS", 0), ("WIKI_EQUIPMENT_ARMOR", 1), ("WIKI_EQUIPMENT_HELMET", 2), ("WIKI_EQUIPMENT_SHIELD", 3), ("WIKI_EQUIPMENT_EARRING", 4), ("WIKI_EQUIPMENT_BRACELET", 5), ("WIKI_EQUIPMENT_NECKLACE", 6), ("WIKI_EQUIPMENT_SHOES", 7), ("WIKI_EQUIPMENT_BELT", 8)]
		equipmentSubItems = [(WikiTr(k), "Equipment#%d" % n) for (k, n) in equip]
		equipmentSubItems.extend([
			(WikiTr("WIKI_ENIGMA_ITEMS"), "WikiSpecial#empty"),
			(WikiTr("WIKI_FISHING_MINING"), "WikiSpecial#fishing_mining"),
			(WikiTr("WIKI_ENERGY_CRYSTAL", WikiText(localeInfo.ENERGY_CRYSTAL)), "WikiSpecial#energy_crystal"),
		])
		tree.append(Cat(WikiTr("WIKI_EQUIPMENT"), "eq", equipmentSubItems))

		costume = [("WIKI_COSTUME_TAB_WEAPON", "Costume#0"), ("WIKI_COSTUME_TAB_ARMOR", "Costume#1"), ("WIKI_COSTUME_TAB_HAIR", "Costume#2"), ("WIKI_COSTUME_TAB_SASH", "Costume#3"), ("WIKI_COSTUME_TAB_SHINING", "Costume#4"), ("WIKI_COSTUME_TAB_PETS", "Pets#0"), ("WIKI_MOUNT_ITEM", "Mount#5")]
		tree.append(Cat(WikiTr("WIKI_COSTUMES"), "cost", [(WikiTr(k), a) for (k, a) in costume]))

		chests = [("WIKI_CHESTS_DUNGEON", "Chests#1"), ("WIKI_CHESTS_BOSS", "Chests#0"), ("WIKI_CHESTS_EVENT", "Chests#3"), ("WIKI_CHESTS_OTHER", "Chests#2")]
		tree.append(Cat(WikiTr("WIKI_CHESTS"), "chest", [(WikiTr(k), a) for (k, a) in chests]))

		tree.append(Cat(WikiTr("WIKI_BOSSES"), "boss", [(WikiTr(k), "MobTier#b#%d" % i) for (i, (k, vnums)) in enumerate(WIKI_BOSS_TIERS)]))
		tree.append(Cat(WikiTr("WIKI_METINSTONE"), "metin", [(WikiTr(k), "MobTier#m#%d" % i) for (i, (k, vnums)) in enumerate(WIKI_METIN_TIERS)]))

		# article kategorileri: wiki_categories.json (wikicontent) -> yoksa eski sabit liste
		extra = self.__GetArticleCategories()
		for (text, iconName, subList) in extra:
			tree.append(Cat(text, iconName, subList))

		for (text, iconName) in ((WikiTr("WIKI_CATEGORY_CRAFT", localeInfo.WIKI_CATEGORY_CRAFT), "craft"), (WikiTr("WIKI_CATEGORY_SHOP", localeInfo.WIKI_CATEGORY_SHOP), "shop")):
			tree.append({'item' : self.CreateCategoryItem(text, lambda arg = (""): self.__EmptyFunction(arg), miniIconPath = CAT_DIR + "icons/" + iconName + ".png")})
		return tree

	def __GetArticleCategories(self):
		result = []
		try:
			import wikicontent
			data = wikicontent.GetCategories()
			if isinstance(data, dict):
				data = data.get("categories", [])
			CATEGORY_ORDER = {7 : (32, 1, 3, 37, 6, 38, 41, 43, 12, 18, 25, 27, 31), 8 : (33, 34, 35, 4, 39, 40, 42, 44, 23, 36),
				9 : (128, 129, 131, 132, 134, 79, 120, 121), 10 : (122, 123, 124, 130)}
			for category in data:
				subList = []
				entries = list(category.get("items", []))
				order = CATEGORY_ORDER.get(int(category.get("id", -1)))
				if order:
					entries.sort(key = lambda e: (list(order).index(int(e.get("id"))) if int(e.get("id")) in order else 999))
				for entry in entries:
					subList.append((WikiTr(entry.get("name", "")), "System#%d" % int(entry.get("id"))))
				if len(subList) == 0:
					continue
				iconName = category.get("btn", "guide")
				result.append((WikiTr(category.get("name", "")), iconName, subList))
		except:
			result = []
		if len(result) > 0:
			return result

		fallback = [
			("WIKI_TEMNITE", "dj", [("DEVILTOWER", 9), ("SPIDERBARONESA", 10), ("BERANSETAOU", 11), ("CATACUMB", 12), ("SNOWDUNGEON", 13), ("FLAMEDUNGEON", 14), ("JOTUN_DUNGEON", 15), ("HYDRADUNGEON", 16), ("WIKI_ZODIAC", 17), ("MELEYDUNGEON", 18), ("WIKI_AKZADUR", 19)]),
			("WIKI_SYSTEM2", "syst", [("WIKI_BIOLOGO", 2), ("WIKI_ALCHEMY", 3), ("WIKI_ATTR_RARE", 4), ("WIKI_COSTUME", 5), ("WIKI_PETS", 6), ("WIKI_TALISMAN", 7), ("WIKI_BOOSTER", 8), ("ENERGY_CRYSTAL", 22)]),
			("WIKI_EVENTS", "event", [("WIKI_EVENTS", 8)]),
			("WIKI_GUIDES2", "guide", [("WIKI_FAQ2", 0), ("WIKI_THESTART2", 1), ("WIKI_GAME_RULES", 23)]),
		]
		for (textKey, iconName, subList) in fallback:
			result.append((WikiTr(textKey), iconName, [(WikiTr(k), "System#%d" % n) for (k, n) in subList]))
		return result

	# ---- navigation helpers ---------------------------------------------------
	def __PushHistory(self, entry):
		historySearch = self.children["historySearch"]
		currentIndex = self.children["currentIndex"]
		if len(historySearch) > 0 and currentIndex < len(historySearch) - 1:
			del historySearch[currentIndex + 1:]
		if len(historySearch) == 0 or historySearch[-1] != entry:
			historySearch.append(entry)
		self.children["currentIndex"] = len(historySearch) - 1
		self.SetHistoryButtons()

	def RefreshCurrentPage(self):
		historySearch = self.children["historySearch"]
		currentIndex = self.children["currentIndex"]
		self.selectArg = ""
		if len(historySearch) == 0:
			self.__SelectType(WIKI_HOME_ARG, FALSE, TRUE)
		else:
			self.RunHistoryArgument(historySearch[currentIndex])
		self.SetHistoryButtons()

	def RefreshEventDropData(self):
		self.RefreshCurrentPage()

	def OnWikiLink(self, linkType, index, pos = None):
		# ArticleGUI / markup hyperlink hedefi: item | mob | article
		if linkType == "item":
			self.ShowItemInfo(int(index), 0)
		elif linkType == "mob":
			self.ShowItemInfo(int(index), 1)
		elif linkType == "article":
			argument = "System#%d" % int(index)
			if pos != None and str(pos) not in ("", "0", "0.0"):
				argument += "#" + str(pos)
			self.__SelectType(argument)

	def OnWikiLinkString(self, linkString):
		parts = str(linkString).split("#")
		kind = parts[0].lower()
		if kind in ("system", "article", "dungeon") and len(parts) >= 2:
			pos = None
			if len(parts) >= 3:
				pos = parts[2]
			self.OnWikiLink("article", int(parts[1]), pos)

	def GetHyperlinkData(self):
		historySearch = self.children["historySearch"]
		if len(historySearch) == 0:
			return (None, 0, None)
		entry = historySearch[self.children["currentIndex"]]
		parts = entry.split("#")
		try:
			if parts[0] == "NEW":
				if int(parts[2]) == 0:
					return ("item", int(parts[1]), None)
				return ("mob", int(parts[1]), None)
			if parts[0] == "System" and len(parts) >= 2:
				pos = None
				if len(parts) >= 3:
					pos = parts[2]
				return ("article", int(parts[1]), pos)
		except:
			pass
		return (None, 0, None)

	def CopyWikiHyperlink(self):
		(kind, index, pos) = self.GetHyperlinkData()
		if kind == None:
			return
		text = "[WIKI:%s:%d]" % (kind, index)
		if pos != None:
			text = "[WIKI:%s:%d:%s]" % (kind, index, pos)
		try:
			import ime
			ime.PasteString(text)
		except:
			chat.AppendChat(chat.CHAT_TYPE_INFO, text)

	def OpenWithArgument(self, argument = None):
		self.Open()
		if argument == None or argument == "":
			return
		if isinstance(argument, int):
			self.ShowItemInfo(argument, 0)
			return
		parts = str(argument).split("#")
		kind = parts[0].lower()
		try:
			if kind == "item" and len(parts) >= 2:
				self.ShowItemInfo(int(parts[1]), 0)
			elif kind in ("mob", "monster") and len(parts) >= 2:
				self.ShowItemInfo(int(parts[1]), 1)
			elif kind == "article" and len(parts) >= 2:
				pos = None
				if len(parts) >= 3:
					pos = parts[2]
				self.OnWikiLink("article", int(parts[1]), pos)
			else:
				self.__SelectType(str(argument))
		except:
			pass

	def __ItemTitle(self, vnum, kind):
		try:
			if kind == 0:
				item.SelectItem(vnum)
				name = item.GetItemName()
				plusPos = name.find("+")
				if plusPos > 0:
					name = name[:plusPos]
				return name
			return nonplayer.GetMonsterName(vnum)
		except:
			return str(vnum)

	def OpenRules(self):
		self.__SelectType("System#23")

	def __EmptyFunction(self, arg):
		pass

	def LoadData(self, arg):
		self.__SelectType(arg)

	def __SelectCharacters(self, buttonIndex):
		for j in xrange(4):
			if self.children["characterIndex"] == buttonIndex:
				self.children["job_%d_characterBtn" % j].Down()
			else:
				self.children["job_%d_characterBtn" % j].SetUp()
		self.children["characterIndex"] = buttonIndex

		self.__SelectType(self.selectArg, TRUE)

	def __ClickRadioButton(self, buttonList, buttonIndex):
		try:
			btn = buttonList[buttonIndex]
		except IndexError:
			return
		for eachButton in buttonList:
			eachButton.SetUp()
		btn.Down()

	def SetCharacterImagesStatus(self, flag):
		for j in xrange(4):
			if not flag:
				self.children["job_%d_characterBtn" % j].Hide()
			else:
				self.children["job_%d_characterBtn" % j].Show()
				if self.children["characterIndex"] == j:
					self.children["job_%d_characterBtn" % j].Down()
				else:
					self.children["job_%d_characterBtn" % j].SetUp()

	def ClearResultListbox(self, argList, isSpecial = FALSE):
		self.AIAppendAlgoritm = None
		try:
			resultpageListbox = self.children["resultpageListbox"]
			resultpageListboxScrollbar = self.children["resultpageListboxScrollbar"]

			resultpageListbox.RemoveAllItems()
			resultpageListbox.Show()
			resultpageListboxScrollbar.Hide()

			self.__ResetBanner()

			if len(argList) == 0 or argList[0] == "":
				return

			w = self.wikiW
			listBottom = self.wikiH - 20
			if argList[0] == "Equipment" and isSpecial == FALSE:
				self.SetCharacterImagesStatus(TRUE)
				(left, top) = (228, 189)
			else:
				self.SetCharacterImagesStatus(FALSE)
				(left, top) = (228, 126)
			width = w - 251

			resultpageListbox.SetPosition(left, top)
			resultpageListbox.SetSize(width, listBottom - top)
			resultpageListboxScrollbar.SetPosition(w - 18, top + 1)
			resultpageListboxScrollbar.SetScrollBarSize(listBottom - top)
		except:
			pass

	def __SelectType(self, arg, isCharacterBtn = FALSE, isHistory = TRUE):
		if isCharacterBtn == FALSE and self.selectArg == arg:
			return

		if isHistory:
			self.__PushHistory(arg)

		self.selectArg = arg
		self.__SetTabTitle(self.__ArgToTitle(arg), arg != WIKI_HOME_ARG)
		argList = arg.split("#")
		self.ClearResultListbox(argList)

		if argList[0] == "WikiSpecial":
			if argList[1] == "empty":
				return
			itemVnums = (29110, 27480) if argList[1] == "fishing_mining" else (51002,)
			for vnum in itemVnums:
				entry = EquipmentItem(99, vnum)
				entry.LoadItemInfos()
				self.children["resultpageListbox"].AppendItem(entry, FALSE)
			self.children["resultpageListbox"].Show()
			self.children["resultpageListboxScrollbar"].Hide()
			return

		AIAppendAlgoritm = WikiUI.AutoLoad()
		AIAppendAlgoritm.SetFlag("loadTime", AUTOLOAD_SPEED)

		if argList[0] == "Equipment":
			maxSize = wiki.GetCategorySize(self.children["characterIndex"], int(argList[1]))
			if maxSize == 0:
				return

			AIAppendAlgoritm.SetFlag("maxSize", maxSize - 1)
			AIAppendAlgoritm.SetFlag("loadType", "Equipment")
			AIAppendAlgoritm.SetFlag("characterIndex", self.children["characterIndex"])
			AIAppendAlgoritm.SetFlag("itemType", int(argList[1]))

		elif argList[0] == "Pets":
			self.petSizes = (wiki.GetCostumeSize(6), wiki.GetCostumeSize(7))
			maxSize = self.petSizes[0] + self.petSizes[1]
			if maxSize == 0:
				return

			AIAppendAlgoritm.SetFlag("maxSize", maxSize - 1)
			AIAppendAlgoritm.SetFlag("loadType", "Costume")
			AIAppendAlgoritm.SetFlag("itemType", -1)

		elif argList[0] == "Costume" or argList[0] == "Mount":
			maxSize = wiki.GetCostumeSize(int(argList[1]))
			if maxSize == 0:
				return

			AIAppendAlgoritm.SetFlag("maxSize", maxSize - 1)
			AIAppendAlgoritm.SetFlag("loadType", "Costume")
			AIAppendAlgoritm.SetFlag("itemType", int(argList[1]))

		elif argList[0] == "Chests":
			maxSize = wiki.GetChestSize(int(argList[1]))
			if maxSize == 0:
				return

			AIAppendAlgoritm.SetFlag("maxSize", maxSize - 1)
			AIAppendAlgoritm.SetFlag("loadType", "Chests")
			AIAppendAlgoritm.SetFlag("itemType", int(argList[1]))

		elif argList[0] == "MobTier":
			tiers = WIKI_BOSS_TIERS if argList[1] == "b" else WIKI_METIN_TIERS
			self.tierVnums = tiers[int(argList[2])][1]
			maxSize = len(self.tierVnums)
			if maxSize == 0:
				return

			AIAppendAlgoritm.SetFlag("maxSize", maxSize - 1)
			AIAppendAlgoritm.SetFlag("loadType", "MobTier")
			AIAppendAlgoritm.SetFlag("loadTime", AUTOLOAD_MONSTER_SPEED)

		elif argList[0] == "Bosses":
			maxSize = wiki.GetBossSize(int(argList[1]))
			if maxSize == 0:
				return

			AIAppendAlgoritm.SetFlag("maxSize", maxSize - 1)
			AIAppendAlgoritm.SetFlag("loadType", "Bosses")
			AIAppendAlgoritm.SetFlag("itemType", int(argList[1]))
			AIAppendAlgoritm.SetFlag("loadTime", AUTOLOAD_MONSTER_SPEED)

		elif argList[0] == "Monster":
			maxSize = wiki.GetMonsterSize(int(argList[1]))
			if maxSize == 0:
				return

			AIAppendAlgoritm.SetFlag("maxSize", maxSize - 1)
			AIAppendAlgoritm.SetFlag("loadType", "Monster")
			AIAppendAlgoritm.SetFlag("itemType", int(argList[1]))
			AIAppendAlgoritm.SetFlag("loadTime", AUTOLOAD_MONSTER_SPEED)

		elif argList[0] == "Metinstone":
			maxSize = wiki.GetStoneSize(int(argList[1]))
			if maxSize == 0:
				return

			AIAppendAlgoritm.SetFlag("maxSize", maxSize - 1)
			AIAppendAlgoritm.SetFlag("loadType", "Metinstone")
			AIAppendAlgoritm.SetFlag("itemType", int(argList[1]))

		elif WikiUI.IsArticleCategory(argList):
			if len(argList) == 3:
				event_item = ArticleGUI(argList[1] + "#" + argList[2])
			else:
				event_item = ArticleGUI(int(argList[1]))
			self.children["resultpageListbox"].SetSize(self.wikiW - 251, self.wikiH - 146)
			self.children["resultpageListbox"].AppendItem(event_item)
			event_item.LoadItemInfos()
			self.children["resultpageListboxScrollbar"].Hide()
			return

		if AIAppendAlgoritm.GetFlag("loadTime") != 0:
			self.AIAppendAlgoritm = AIAppendAlgoritm

	def ShowItemInfo(self, vnum, arg, isHistory = TRUE):
		if arg == 3:
			self.OnWikiLinkString(vnum)
			return
		if isHistory:
			self.__PushHistory("NEW#%d#%d" % (vnum, arg))

		if arg == 3:
			self.__SelectType(vnum)

		elif arg == 0:
			self.selectArg = "Equipment#0"
			self.__SetTabTitle(self.__ItemTitle(vnum, 0), TRUE)
			self.ClearResultListbox(self.selectArg.split("#"), TRUE)
			self.children["resultpageListboxScrollbar"].Hide()
			(vnum, isRefineItem) = WikiUI.getRealVnum(vnum)
			if isRefineItem:
				vnum += wiki.GetRefineMaxLevel(vnum)
			resultpageListbox = self.children["resultpageListbox"]
			if isRefineItem:
				new_refine_table = EquipmentItem(99, vnum)
				new_refine_table.LoadItemInfos()
				resultpageListbox.AppendItem(new_refine_table)
			item.SelectItem(vnum)
			if item.GetItemType() == item.ITEM_TYPE_GIFTBOX:
				item_table = MonsterItemSpecial(vnum, 3)
				item_table.LoadItemInfos()
				resultpageListbox.AppendItem(item_table)

				monster_statics = MonsterStatics(vnum, 3)
				monster_statics.LoadItemInfos()
				resultpageListbox.AppendItem(monster_statics)
			else:
				item_table = MonsterItemSpecial(vnum, 1)
				item_table.LoadItemInfos()
				resultpageListbox.AppendItem(item_table)
			resultpageListbox.Render(0)
			self.children["resultpageListboxScrollbar"].Hide()
			self.selectArg = ""

		elif arg == 1:
			self.selectArg = "Monster#0"
			self.__SetTabTitle(self.__ItemTitle(vnum, 1), TRUE)
			self.ClearResultListbox(self.selectArg.split("#"), TRUE)
			self.children["resultpageListboxScrollbar"].Show()
			resultpageListbox = self.children["resultpageListbox"]

			monster_table = MonsterItemSpecial(vnum, 0)
			monster_table.LoadItemInfos()
			resultpageListbox.AppendItem(monster_table)

			monster_statics = MonsterStatics(vnum, 0)
			monster_statics.LoadItemInfos()
			resultpageListbox.AppendItem(monster_statics)

			resultpageListbox.Render(0)

			self.selectArg = ""

	def OnUpdate(self):
		self.CheckLoadProcess()
		self.UpdateToTopButton()
		self.__UpdateResizeDrag()
		
		# Tooltip'lerin mouse pozisyonunu takip etmesi ve tooltip alan�ndan ��k�ld���nda gizlenmesi
		try:
			import wndMgr
			(x, y) = wndMgr.GetMousePosition()
			
			# Wiki penceresinin �zerinde mi kontrol et
			onWindow = False
			if self.IsShow():
				try:
					(wx, wy) = self.GetGlobalPosition()
					ww, wh = self.GetWidth(), self.GetHeight()
					if wx <= x <= wx + ww and wy <= y <= wy + wh:
						onWindow = True
				except:
					pass
			
			# Wiki penceresi i�indeki item'lar�n �zerinde mi kontrol et
			onWikiItem = False
			if onWindow and self.children.has_key("resultpageListbox"):
				try:
					resultpageListbox = self.children["resultpageListbox"]
					if resultpageListbox:
						for item in resultpageListbox.itemList:
							try:
								(ix, iy) = item.GetGlobalPosition()
								iw, ih = item.GetWidth(), item.GetHeight()
								if ix <= x <= ix + iw and iy <= y <= iy + ih:
									onWikiItem = True
									break
							except:
								pass
				except:
					pass
			
			# T�m tooltip'leri kontrol et (merkezi sistemden)
			from uiToolTip import ToolTip
			for tooltip in ToolTip._allToolTips:
				if tooltip and tooltip.IsShow():
					try:
						(tx, ty) = tooltip.GetGlobalPosition()
						tw, th = tooltip.GetWidth(), tooltip.GetHeight()
						onTooltip = (tx <= x <= tx + tw and ty <= y <= ty + th)
						
						# Tooltip'in �zerinde de�ilse ve wiki item'�n�n da �zerinde de�ilse gizle
						if not onTooltip and not onWikiItem:
							tooltip.HideToolTip()
							tooltip.Hide()
					except:
						pass
		except:
			pass

	def GetVisibleArticle(self):
		resultBox = self.children.get("resultpageListbox")
		if not resultBox:
			return None
		for item in resultBox.itemList:
			if isinstance(item, ArticleGUI) and item.IsShow():
				return item
		return None

	def UpdateToTopButton(self):
		button = self.children.get("toTopBtn")
		if not button:
			return
		article = self.GetVisibleArticle()
		bar = article.Listbox.scrollBar if article and article.Listbox else None
		if bar and bar.IsShow() and bar.GetPos() > 0.01:
			button.Show()
		else:
			button.Hide()

	def ScrollArticleToTop(self):
		article = self.GetVisibleArticle()
		bar = article.Listbox.scrollBar if article and article.Listbox else None
		if bar:
			bar.SetPos(0.0)
		self.UpdateToTopButton()

	def SetTimeForHide(self, isOpen):
		__ai = self.AIAppendAlgoritm
		if __ai != None:
			if isOpen:
				__ai.SetFlag("nexTime", app.GetTime() + 0.15)
			else:
				__ai.SetFlag("nexTime", app.GetTime() + 999999)

	def CheckLoadProcess(self):
		__ai = self.AIAppendAlgoritm
		if __ai != None:
			if __ai.GetFlag("nexTime") > app.GetTime():
				return
			__ai.SetFlag("nexTime", app.GetTime() + __ai.GetFlag("loadTime"))
			loadType = __ai.GetFlag("loadType")
			listIndex = __ai.GetFlag("maxSize")
			if loadType == "Equipment":
				equipItemPointer = EquipmentItem(listIndex, wiki.GetCategoryData(__ai.GetFlag("characterIndex"), __ai.GetFlag("itemType"), listIndex))
				equipItemPointer.LoadItemInfos()
				equipItemPointer.sortIndex = listIndex
				self.children["resultpageListbox"].AppendItem(equipItemPointer, FALSE)

			elif loadType == "Costume":
				costumeType = __ai.GetFlag("itemType")
				costumeIndex = listIndex
				if costumeType == -1:
					(normalCount, levelCount) = self.petSizes
					(costumeType, costumeIndex) = (6, listIndex) if listIndex < normalCount else (7, listIndex - normalCount)
				createNewWindow = TRUE
				ListBoxItems = self.children["resultpageListbox"].itemList
				if len(ListBoxItems) > 0:
					lastItem = ListBoxItems[len(ListBoxItems) - 1]
					if lastItem.CanAddNewItem():
						lastItem.LoadItemInfos(wiki.GetCostumeData(costumeType, costumeIndex))
						createNewWindow = FALSE

				if createNewWindow:
					equipItemPointer = SpecialClass(listIndex, 0)
					equipItemPointer.LoadItemInfos(wiki.GetCostumeData(costumeType, costumeIndex))
					equipItemPointer.sortIndex = listIndex
					self.children["resultpageListbox"].AppendItem(equipItemPointer, FALSE)

			elif loadType == "Chests":
				(itemVnum, bossVnum) = wiki.GetChestData(__ai.GetFlag("itemType"), listIndex)
				if itemVnum == 0:
					return
				equipItemPointer = ListBoxItemSpecial(listIndex, itemVnum, bossVnum, 0)
				equipItemPointer.LoadItemInfos()
				equipItemPointer.sortIndex = listIndex
				self.children["resultpageListbox"].AppendItem(equipItemPointer, FALSE)

			elif loadType == "Monster":
				mobVnum = wiki.GetMonsterData(__ai.GetFlag("itemType"), listIndex)
				if mobVnum == 0:
					return
				equipItemPointer = ListBoxItemSpecial(listIndex, mobVnum, 0, 1)
				equipItemPointer.LoadItemInfos()
				equipItemPointer.sortIndex = listIndex
				self.children["resultpageListbox"].AppendItem(equipItemPointer, FALSE)

			elif loadType == "MobTier":
				vnums = self.tierVnums
				if listIndex >= len(vnums):
					return
				equipItemPointer = ListBoxItemSpecial(listIndex, vnums[listIndex], 0, 1)
				equipItemPointer.LoadItemInfos()
				equipItemPointer.sortIndex = listIndex if not SHOW_ITEM_LOWER_TO_BIG else len(vnums) - listIndex
				self.children["resultpageListbox"].AppendItem(equipItemPointer, FALSE)

			elif loadType == "Bosses":
				mobVnum = wiki.GetBossData(__ai.GetFlag("itemType"), listIndex)
				if mobVnum == 0:
					return
				equipItemPointer = ListBoxItemSpecial(listIndex, mobVnum, 0, 1)
				equipItemPointer.LoadItemInfos()
				equipItemPointer.sortIndex = listIndex
				self.children["resultpageListbox"].AppendItem(equipItemPointer, FALSE)

			elif loadType == "Metinstone":
				mobVnum = wiki.GetStoneData(__ai.GetFlag("itemType"), listIndex)
				if mobVnum == 0:
					return
				equipItemPointer = ListBoxItemSpecial(listIndex, mobVnum, 0, 1)
				equipItemPointer.LoadItemInfos()
				equipItemPointer.sortIndex = listIndex
				self.children["resultpageListbox"].AppendItem(equipItemPointer, FALSE)

			self.SetPositionToSort(self.children["resultpageListbox"], loadType)
			__ai.SetFlag("maxSize", listIndex-1)

			if listIndex - 1 < 0:
				self.AIAppendAlgoritm = None
				self.children["resultpageListbox"].CalculateScroll()

	def get_key(self, data):
		return data.sortIndex

	def SetPositionToSort(self, listBox, loadType):
		itemList = listBox.itemList
		if len(itemList) > 1:
			if loadType == "Costume":
				itemList = sorted(itemList, key = self.get_key, reverse = TRUE)
			else:
				itemList = sorted(itemList, key = self.get_key, reverse = SHOW_ITEM_LOWER_TO_BIG)
		y = 0
		for child in itemList:
			child.Hide()
			child.SetPosition(0, y, TRUE)
			child.OnRender()
			child.Show()
			y += child.GetHeight()

	def CreateCategoryItem(self, text, event, offset = 0, miniIconPath = None):
		listboxItem = CategoryItem(text, miniIconPath)
		listboxItem.SetVisible(TRUE)
		listboxItem.SetEvent(event)
		listboxItem.SetOffset(offset)
		return listboxItem

	def CreateCategorySubItem(self, text, event, offset = 0):
		listboxItem = CategorySubItem(text)
		listboxItem.SetEvent(event)
		listboxItem.SetOffset(offset)
		return listboxItem

	def SetRenderTargetsStatus(self, bShowStatus):
		if self.children.has_key("resultpageListbox"):
			resultpageListbox = self.children["resultpageListbox"].itemList
			for child in resultpageListbox:
				if child.renderIndex != -1:
					renderTarget.SetVisibility(child.renderIndex, bShowStatus)

	def Open(self):
		self.SetRenderTargetsStatus(TRUE)
		self.Show()
		self.SetTimeForHide(TRUE)

	def Close(self):
		self.resizing = FALSE
		self.HideResizePreview()
		self.__ClearDropDown()
		# T�m tooltip'leri kapat
		from uiToolTip import ToolTip
		for tooltip in ToolTip._allToolTips:
			if tooltip and tooltip.IsShow():
				tooltip.HideToolTip()
				tooltip.Hide()
		
		# T�m item'lar�n OverOutItem metodunu �a��r
		# T�m tooltip'leri kapat
		from uiToolTip import ToolTip
		for tooltip in ToolTip._allToolTips:
			if tooltip and tooltip.IsShow():
				tooltip.HideToolTip()
				tooltip.Hide()
		
		# DefaultWikiWindow ve DefaultWikiImage class variable tooltip'lerini de kapat
		try:
			import WikiUI
			# DefaultWikiWindow.tooltipItem class variable'�n� kapat
			tooltip = WikiUI.DefaultWikiWindow.tooltipItem
			if tooltip and tooltip.IsShow():
				tooltip.HideToolTip()
				tooltip.Hide()
			
			# DefaultWikiImage.tooltipItem class variable'�n� kapat
			tooltip = WikiUI.DefaultWikiImage.tooltipItem
			if tooltip and tooltip.IsShow():
				tooltip.HideToolTip()
				tooltip.Hide()
		except:
			pass
		
		# T�m item'lar�n OverOutItem metodunu �a��r
		if self.children.has_key("resultpageListbox"):
			try:
				resultpageListbox = self.children["resultpageListbox"]
				if resultpageListbox:
					for item in resultpageListbox.itemList:
						try:
							item.OverOutItem()
						except:
							pass
			except:
				pass
		
		self.SetRenderTargetsStatus(FALSE)
		self.SetTimeForHide(FALSE)
		self.children["searchMobName"].KillFocus()
		self.children["searchItemName"].KillFocus()
		self.Hide()

	def OnRunMouseWheel(self, nLen):
		# Mouse pozisyonunu al
		try:
			import wndMgr
			(mx, my) = wndMgr.GetMousePosition()
		except:
			mx, my = 0, 0
		
		# �nce listBoxCube'un scroll bar'�n� kontrol et (mouse listBoxCube �zerindeyse)
		if self.children.has_key("listBoxCube"):
			listBoxCube = self.children["listBoxCube"]
			if listBoxCube and listBoxCube.scrollBar:
				if listBoxCube.scrollBar.IsShow():
					try:
						(lx, ly) = listBoxCube.GetGlobalPosition()
						lw, lh = listBoxCube.GetWidth(), listBoxCube.GetHeight()
						# Mouse listBoxCube �zerindeyse onun scroll bar'�n� kullan
						if lx <= mx <= lx + lw and ly <= my <= ly + lh:
							if nLen > 0:
								listBoxCube.scrollBar.OnUp()
							else:
								listBoxCube.scrollBar.OnDown()
							return TRUE
					except:
						pass
		
		resultBox = self.children.get("resultpageListbox")
		if resultBox:
			(rx, ry) = resultBox.GetGlobalPosition()
			if rx <= mx <= rx + resultBox.GetWidth() and ry <= my <= ry + resultBox.GetHeight():
				for article in resultBox.itemList:
					bar = article.Listbox.scrollBar if article.Listbox else None
					if bar and bar.IsShow():
						if nLen > 0:
							bar.OnUp()
						else:
							bar.OnDown()
						return TRUE
		# Sonra resultpageListboxScrollbar'� kontrol et
		if self.children.has_key("resultpageListboxScrollbar"):
			self.scrollBar = self.children["resultpageListboxScrollbar"]
			if self.scrollBar.IsShow():
				if nLen > 0:
					self.scrollBar.OnUp()
				else:
					self.scrollBar.OnDown()
				return TRUE
		return FALSE

	def OnPressExitKey(self):
		self.Close()
		return TRUE

	def OnPressEscapeKey(self):
		# ESC ile kapat�ld���nda t�m tooltip'leri kapat
		from uiToolTip import ToolTip
		for tooltip in ToolTip._allToolTips:
			if tooltip and tooltip.IsShow():
				tooltip.HideToolTip()
				tooltip.Hide()
		
		self.Close()
		return TRUE

# ---------------------------------------------------------------------------
# Wiki icerik motoru entegrasyonu (wikicontent + wikimarkup + wikipages)
#
# MIMARI NOTU
#   wikimarkup  : ui'dan bagimsiz parser + Build(parent, doc, width, ctx) -> BuildResult
#   wikipages   : item/monster/refine/obtention sayfa widget'lari (native `wiki` modulu uzerinden)
#   uiwiki      : shell (EncyclopediaofGame) + ArticleGUI (motoru Listbox'a baglar)
# Import yonu: uiwiki -> wikipages -> WikiUI (wikipages uiwiki import ETMEZ, cycle yok).
# ---------------------------------------------------------------------------
import wikipages
wikimarkupError = ""
try:
	import wikimarkup
except:
	import sys
	wikimarkupError = str(sys.exc_info()[:2])
	wikimarkup = None

# eski sinif adlari (uiWiki.EquipmentItem vb. ve WikiUI'deki isinstance(uiWiki.ListBoxItemSpecial) icin)
EquipmentItem = wikipages.EquipmentItem
MonsterItemSpecial = wikipages.MonsterItemSpecial
MonsterStatics = wikipages.MonsterStatics
ListBoxItemSpecial = wikipages.ListBoxItemSpecial
SpecialClass = wikipages.SpecialClass

if wikimarkup != None:
	_WikiProviderBase = wikimarkup.DataProvider
	_WikiContextBase = wikimarkup.WikiContext
else:
	_WikiProviderBase = object
	_WikiContextBase = object

class WikiComponentLoader:
	# wikimarkup.Parse loader'i: component sablonlari -> locale/common/wiki/composants/<rel>.txt
	def __call__(self, rel):
		import wikicontent
		return wikicontent.LoadArticleText("composants/" + rel + ".txt")

class WikiArticleProvider(_WikiProviderBase):
	# {WK:id} ve Append*/Get* data fonksiyonlari. Native wiki modulunde bonus/skill verisi yok:
	# bu fonksiyonlar bos doner (bkz. Docs/wiki_reference_20261018.md).
	def Locale(self, key):
		try:
			import wikicontent
			text = wikicontent.Tr(key, None)
			if text == None or text == str(key):
				return None
			return text
		except:
			return None

	def AppendItem(self, vnum):
		import wikicontent
		names = {40912: "WIKI_ITEM_SNAKE_TAIL", 40914: "WIKI_ITEM_SPIDER_LEGS"}
		if int(vnum) in names:
			return localeInfo.GetText(names[int(vnum)], "")
		try:
			item.SelectItem(int(vnum))
			return item.GetItemName()
		except:
			return ""

	def AppendPNJ(self, vnum):
		try:
			return nonplayer.GetMonsterName(int(vnum))
		except:
			return ""

	def AppendBonus(self, bonusId):
		return localeInfo.GetText("WIKI_BONUS_%d" % int(bonusId), "")

	def AppendSkill(self, skillId):
		try:
			return skill.GetSkillName(int(skillId))
		except:
			return ""

class WikiArticleContext(_WikiContextBase):
	def __init__(self, onLink):
		self.articleIndex = None
		_WikiContextBase.__init__(self, WikiArticleProvider(), None, onLink)
		self.measureLine = None

	def FontName(self, size, bold):
		name = localeInfo.UI_DEF_FONT.split(":")[0]
		if bold:
			return "%s:%db" % (name, int(size))
		return "%s:%d" % (name, int(size))

	def MeasureText(self, text, size, bold):
		try:
			if self.measureLine == None:
				self.measureLine = ui.TextLine()
			self.measureLine.SetFontName(self.FontName(size, bold))
			self.measureLine.SetText(text)
			(w, h) = self.measureLine.GetTextSize()
			return (w, size + self.line_extra)
		except:
			return _WikiContextBase.MeasureText(self, text, size, bold)

	def CreateItem(self, parent, vnum, sockets, attrs, tooltip):
		if self.articleIndex == 33 and int(vnum) in (55315, 55316, 55317):
			icon = ui.ExpandedImageBox()
			icon.SetParent(parent)
			icon.LoadImage(IMG_DIR + "exploration_icons/%d.png" % int(vnum))
			return (icon, icon.GetWidth(), icon.GetHeight())
		if self.articleIndex == 6 and int(vnum) in (58000, 58002, 58014, 40217, 40218, 40912, 40914, 58010, 58011, 58012, 58013):
			icon = ui.ExpandedImageBox()
			icon.SetParent(parent)
			icon.LoadImage(IMG_DIR + "mount_icons/%d.png" % int(vnum))
			return (icon, icon.GetWidth(), icon.GetHeight())
		slot = wikipages.WikiItemSlot()
		slot.SetParent(parent)
		slot.SetItem(int(vnum))
		return (slot, slot.GetWidth(), slot.GetHeight())

	def CreateRenderTarget(self, parent, vnum, w, h):
		if w <= 0:
			w = 47
		if h <= 0:
			h = 87
		targetIndex = renderTarget.GetFreeIndex(1000, 1000000)
		tmp = ui.RenderTarget()
		tmp.SetParent(parent)
		tmp.SetSize(w, h)
		tmp.SetRenderTarget(targetIndex)
		tmp.SetEvent(ui.__mem_func__(self.OnRenderTargetClick), "mouse_click", "mob", vnum, 0)
		renderTarget.SelectModel(targetIndex, vnum)
		renderTarget.SetVisibility(targetIndex, TRUE)
		return tmp

	def OnRenderTargetClick(self, eventType, kind, vnum, pos):
		self.OnLink(kind, vnum, pos)

	def ShowItemTooltip(self, vnum, sockets, attrs):
		wikipages.ShowItemToolTip(WikiUI.DefaultWikiImage.tooltipItem, int(vnum))

	def HideItemTooltip(self):
		WikiUI.DefaultWikiImage.tooltipItem.HideToolTip()

class WikiMarkupContainer(ui.Window):
	# Listbox'a tek item olarak eklenir; Build edilen tum pencereler bunun child'i
	def __init__(self):
		ui.Window.__init__(self)
		self.result = None

	def __del__(self):
		ui.Window.__del__(self)

	def Destroy(self):
		if self.result != None:
			self.result.Destroy()
			self.result = None
		self.Hide()

class ArticleGUI(WikiUI.DefaultWikiImage):
	def __del__(self):
		WikiUI.DefaultWikiImage.__del__(self)

	def Destroy(self):
		self.index = 0
		self.scrollPos = 0.0
		self.markupResult = None
		WikiUI.DefaultWikiImage.Destroy(self)

	def __init__(self, index):
		WikiUI.DefaultWikiImage.__init__(self)
		self.index = 0
		self.scrollPos = 0.0
		self.markupResult = None
		if isinstance(index, str):
			if index.find("#") != -1:
				indexList = index.split("#")
				if len(indexList) == 2:
					self.index = int(indexList[0])
					self.scrollPos = float(indexList[1])
			else:
				try:
					self.index = int(index)
				except:
					self.index = 0
		else:
			self.index = index
			self.scrollPos = 0.0
		self.LoadImage(IMG_DIR + "btn_pnj.png")
		self.SetSize(563, 367)
		self.children.append(self)

	def LoadItemInfos(self):
		if self.IsLoaded == FALSE:
			self.IsLoaded = TRUE
			Listbox = WikiUI.ListBoxGrid()
			Listbox.SetParent(self)
			Listbox.SetPosition(0, 0)
			Listbox.SetSize(self.GetWidth() - 15, self.GetHeight() - 15)
			Listbox.AddRenderEvent(self.OnRender)
			self.ReadArticle(Listbox, self.index)
			self.CheckScrollBarNeed(Listbox)
			Listbox.Show()
			self.Listbox = Listbox
			self.Show()
			self.OnRender()

	def GetFileName(self, index):
		file_dict = {
			0 : "wiki/guides/faq.txt",
			1 : "wiki/guides/the_start.txt",
			2 : "wiki/systems/biologist.txt",
			3 : "wiki/systems/alchemy.txt",
			4 : "wiki/systems/bonus67.txt",
			5 : "wiki/systems/costume.txt",
			6 : "wiki/systems/pets.txt",
			7 : "wiki/systems/talismane.txt",
			8 : "wiki/systems/boosters.txt",
			9 : "wiki/dungeon/devil.txt",
			10 : "wiki/dungeon/spider.txt",
			11 : "wiki/dungeon/dragon.txt",
			12 : "wiki/dungeon/catacomb.txt",
			13 : "wiki/dungeon/nemere.txt",
			14 : "wiki/dungeon/razador.txt",
			15 : "wiki/dungeon/jotun.txt",
			16 : "wiki/dungeon/hydra.txt",
			17 : "wiki/dungeon/zodiac.txt",
			18 : "wiki/dungeon/meley.txt",
			19 : "wiki/dungeon/akzadur.txt",
			20 : "wiki/systems/energy.txt",
			21 : "wiki/events.txt",
			22 : "wiki/gamerules.txt",
		}

		if file_dict.has_key(index):
			return app.GetLocalePath() + "/" + file_dict[index]
		return ""

	def ParseToken(self, data):
		data = data.replace(chr(10), "").replace(chr(13), "")
		if not (len(data) and data[0] == "["):
			return (FALSE, {}, data)

		fnd = data.find("]")
		if fnd <= 0:
			return (FALSE, {}, data)

		content = data[1:fnd]
		data = data[fnd+1:]
		content = content.split(";")
		container = {}

		for i in content:
			i = i.strip()
			splt = i.split("=")
			if len(splt) == 1:
				container[splt[0].lower().strip()] = TRUE
			else:
				container[splt[0].lower().strip()] = splt[1].lower().strip()

		return (TRUE, container, data)

	def GetColorFromString(self, strCol):
		retData = []
		dNum = 4
		hCol = long(strCol, 16)
		if hCol <= 0xFFFFFF:
			retData.append(1.0)
			dNum = 3

		for i in xrange(dNum):
			retData.append(float((hCol >> (8 * i)) & 0xFF) / 255.0)
		retData.reverse()

		return retData

	def DirectionEvent(self, emptyArg, type, index, pos):
		parent = constInfo.GetMainParent()
		if parent != None:
			if "item" == type:
				parent.ShowItemInfo(index, 0)
			elif "mob" == type:
				parent.ShowItemInfo(index, 1)
			elif "article" == type:
				parent.ShowItemInfo("system#" + str(index) + "#" + str(pos), 3)

	def ReadArticleLegacy(self, Listbox, index):
		fileName = self.GetFileName(index)
		if fileName == "":
			return
		lines = []
		try:
			lines = pack_open(fileName, "r").readlines()
		except:
			lines = []
		_y = 15
		for i in lines:
			(ret, tokenMap, i) = self.ParseToken(i)
			if ret:
				if tokenMap.has_key("banner_img"):
					mainParent = constInfo.GetMainParent()
					if mainParent != None:
						resultpagebtn = mainParent.children["resultpagebtn"]
						resultpagebtn.LoadImage(tokenMap["banner_img"])
						resultpagebtn.Show()
					tokenMap.pop("banner_img")

				if tokenMap.has_key("img"):
					cimg = ui.ExpandedImageBox()
					cimg.SetParent(Listbox)
					cimg.AddFlag("attach")
					cimg.AddFlag("not_pick")
					cimg.LoadImage(tokenMap["img"])
					cimg.Show()
					tokenMap.pop("img")
					x = 0
					if tokenMap.has_key("x"):
						x = int(tokenMap["x"])
						tokenMap.pop("x")
					y = 0
					if tokenMap.has_key("y"):
						y = int(tokenMap["y"])
						tokenMap.pop("y")
					if tokenMap.has_key("center_align"):
						cimg.SetPosition(Listbox.GetWidth() / 2 - cimg.GetWidth() / 2, y, TRUE)
						tokenMap.pop("center_align")
					elif tokenMap.has_key("right_align"):
						cimg.SetPosition(Listbox.GetWidth() - cimg.GetWidth(), y, TRUE)
						tokenMap.pop("right_align")
					else:
						cimg.SetPosition(x, y, TRUE)
					self.children.append(cimg)
					Listbox.AppendItem(cimg)

				if tokenMap.has_key("item"):
					itemVnum = int(tokenMap["item"])
					tokenMap.pop("item")
					item.SelectItem(itemVnum)
					cimg = ui.ExpandedImageBox()
					cimg.SetParent(Listbox)
					if item.GetIconImageFileName().find("gr2") == -1:
						cimg.LoadImage(item.GetIconImageFileName())
					else:
						cimg.LoadImage("icon/item/27995.tga")
					cimg.SAFE_SetStringEvent("MOUSE_OVER_IN", self.OverInItem, itemVnum)
					cimg.SAFE_SetStringEvent("MOUSE_OVER_OUT", self.OverOutItem)
					cimg.SetEvent(ui.__mem_func__(self.OnClickItem), "mouse_click", 0, itemVnum)
					cimg.Show()
					x = 0
					if tokenMap.has_key("x"):
						x = int(tokenMap["x"])
						tokenMap.pop("x")
					y = 0
					if tokenMap.has_key("y"):
						y = int(tokenMap["y"])
						tokenMap.pop("y")
					if tokenMap.has_key("center_align"):
						cimg.SetPosition(Listbox.GetWidth() / 2 - cimg.GetWidth() / 2, y, TRUE)
						tokenMap.pop("center_align")
					elif tokenMap.has_key("right_align"):
						cimg.SetPosition(Listbox.GetWidth() - cimg.GetWidth(), y, TRUE)
						tokenMap.pop("right_align")
					else:
						cimg.SetPosition(x, y, TRUE)
					self.children.append(cimg)
					Listbox.AppendItem(cimg)

				if tokenMap.has_key("link"):
					link = tokenMap["link"]
					tokenMap.pop("link")

					if tokenMap.has_key("linkindex"):
						linkindex = int(tokenMap["linkindex"])
						tokenMap.pop("linkindex")
					else:
						linkindex = 0

					if tokenMap.has_key("linkpos"):
						linkpos = float(tokenMap["linkpos"])
						tokenMap.pop("linkpos")
					else:
						linkpos = 0

					if tokenMap.has_key("linktext"):
						linkText = WikiUI.GetArgToString(tokenMap["linktext"])
						tokenMap.pop("linktext")
					else:
						linkText = ""

					tmp = WikiUI.TextlineLink()
					tmp.SetParent(Listbox)
					if tokenMap.has_key("font_size"):
						splt = localeInfo.UI_DEF_FONT.split(":")
						tmp.SetFontName(splt[0]+":"+tokenMap["font_size"])
						tokenMap.pop("font_size")
					else:
						tmp.SetFontName(localeInfo.UI_DEF_FONT)
					tmp.SetText(WikiUI.GetArgToString(linkText), 1.2)
					tmp.Show()
					tmp.SetSize(*tmp.GetTextSize())
					if tokenMap.has_key("color"):
						fontColor = self.GetColorFromString(tokenMap["color"])
						tmp.SetColor(grp.GenerateColor(fontColor[0], fontColor[1], fontColor[2], fontColor[3]), fontColor[0], fontColor[1], fontColor[2])
						tokenMap.pop("color")
					tmp.SetMouseLeftButtonDownEvent(ui.__mem_func__(self.DirectionEvent), "", link, linkindex, linkpos)
					tmp.linkIcon.SetMouseLeftButtonDownEvent(ui.__mem_func__(self.DirectionEvent),"", link, linkindex, linkpos)
					if tokenMap.has_key("y"):
						y = int(tokenMap["y"])
						tokenMap.pop("y")
					if tokenMap.has_key("center_align"):
						tmp.SetPosition(Listbox.GetWidth() / 2 - tmp.GetWidth() / 2, y, TRUE)
						tokenMap.pop("center_align")
					elif tokenMap.has_key("right_align"):
						tmp.SetPosition(Listbox.GetWidth() - tmp.GetWidth(), y, TRUE)
						tokenMap.pop("right_align")
					else:
						tmp.SetPosition(x, y, TRUE)
					self.children.append(tmp)
					Listbox.AppendItem(tmp)

				if tokenMap.has_key("rendertarget"):
					mobVnum = int(tokenMap["rendertarget"])
					tokenMap.pop("rendertarget")

					(width, height) = (47, 87)

					if tokenMap.has_key("width"):
						width = int(tokenMap["width"])
						tokenMap.pop("width")
					
					if tokenMap.has_key("height"):
						height = int(tokenMap["height"])
						tokenMap.pop("height")

					#targetIndex = app.GetRandom(100,1000)
					targetIndex = renderTarget.GetFreeIndex(1000, 1000000)
					tmp = ui.RenderTarget()
					tmp.SetParent(Listbox)
					tmp.SetSize(width, height)
					tmp.SetRenderTarget(targetIndex)
					tmp.SetEvent(ui.__mem_func__(self.DirectionEvent),"mouse_click", "mob", mobVnum, 0)
					tmp.Show()

					renderTarget.SelectModel(targetIndex, mobVnum)
					renderTarget.SetVisibility(targetIndex, TRUE)
					if tokenMap.has_key("y"):
						y = int(tokenMap["y"])
						tokenMap.pop("y")
					if tokenMap.has_key("center_align"):
						tmp.SetPosition(Listbox.GetWidth() / 2 - tmp.GetWidth() / 2, y, TRUE)
						tokenMap.pop("center_align")
					elif tokenMap.has_key("right_align"):
						tmp.SetPosition(Listbox.GetWidth() - tmp.GetWidth(), y, TRUE)
						tokenMap.pop("right_align")
					else:
						tmp.SetPosition(x, y, TRUE)
					self.children.append(tmp)
					Listbox.AppendItem(tmp)

			# Token parse edildikten sonra text render et
			# E�er token varsa (ret == TRUE) ve token'dan sonra text yoksa, sadece �zel elementler render edilir
			# E�er token yoksa (ret == FALSE), t�m sat�r text olarak render edilir
			
			# i.strip() ile bo�luk kontrol� yap, e�er bo�sa continue et
			if not i.strip():
				continue

			i = i.replace("*", "|Eemoji/e_wiki|e")
			tmp = ui.TextLine()
			tmp.SetParent(Listbox)
			if tokenMap.has_key("font_size"):
				splt = localeInfo.UI_DEF_FONT.split(":")
				tmp.SetFontName(splt[0]+":"+tokenMap["font_size"])
				tokenMap.pop("font_size")
			else:
				tmp.SetFontName(localeInfo.UI_DEF_FONT)
			tmp.SetText(WikiUI.GetArgToString(i))
			tmp.Show()
			tmp.SetSize(*tmp.GetTextSize())

			if tokenMap.has_key("color"):
				fontColor = self.GetColorFromString(tokenMap["color"])
				tmp.SetPackedFontColor(grp.GenerateColor(fontColor[0], fontColor[1], fontColor[2], fontColor[3]))
				tokenMap.pop("color")

			tmp.SetPosition(30, _y, TRUE)
			_y+=tmp.GetHeight()

			if tokenMap.has_key("center_align"):
				tmp.SetPosition(Listbox.GetWidth() / 2 - tmp.GetWidth() / 2, tmp.GetLocalPosition()[1], TRUE)
				tokenMap.pop("center_align")
			elif tokenMap.has_key("right_align"):
				tmp.SetPosition(Listbox.GetWidth() - tmp.GetWidth(), tmp.GetLocalPosition()[1], TRUE)
				tokenMap.pop("right_align")
			elif tokenMap.has_key("x_padding"):
				tmp.SetPosition(int(tokenMap["x_padding"]), tmp.GetLocalPosition()[1], TRUE)
				tokenMap.pop("x_padding")

			tmp.Show()
			self.children.append(tmp)
			Listbox.AppendItem(tmp)

	# ---- markup motoru (wikicontent + wikimarkup) ----------------------------------------
	def ReadArticle(self, Listbox, index):
		# once yeni motor, bulunamazsa eski sabit dosya listesi (ReadArticleLegacy)
		if self.ReadArticleMarkup(Listbox, index):
			return
		self.ReadArticleLegacy(Listbox, index)

	def ReadArticleMarkup(self, Listbox, index):
		if wikimarkup == None:
			return FALSE
		container = None
		try:
			import wikicontent
			rel = wikicontent.GetArticleFile(index)
			if rel == None:
				return FALSE
			text = wikicontent.LoadArticleText(rel)
			if text == None:
				return FALSE
			doc = wikimarkup.Parse(text, WikiComponentLoader())
			banner = doc.banner
			# banner node'u icerikte degil, shell'deki resultpagebtn'de cizilir (eski banner_img davranisi)
			doc.nodes = [n for n in doc.nodes if n.get("type") != "banner"]
			width = Listbox.GetWidth()
			container = WikiMarkupContainer()
			container.SetParent(Listbox)
			container.AddFlag("not_pick")
			container.SetSize(width, 10)
			container.SetPosition(0, 0, TRUE)
			container.Show()
			ctx = WikiArticleContext(ui.__mem_func__(self.OnMarkupLink))
			ctx.articleIndex = self.index
			tocOffset = 96 if self.index in (6, 33, 122) else 0
			result = wikimarkup.Build(container, doc, width, ctx, y = tocOffset)
			if tocOffset:
				self.BuildGuideContents(container, result, doc, ctx)
			if app.ENABLE_CLIP_MASKING:
				for window in result.windows:
					try:
						window.SetClippingMaskWindow(Listbox)
					except:
						pass
			container.SetSize(width, tocOffset + result.height + 20)
			container.result = result
			self.markupResult = result
			Listbox.AppendItem(container)
		except:
			try:
				import sys
				import dbg
				dbg.TraceError("wiki markup failed: article %s: %s" % (str(index), str(sys.exc_info()[:2])))
			except:
				pass
			if container != None:
				container.Destroy()
			self.markupResult = None
			return FALSE
		self.SetMarkupBanner(banner)
		return TRUE

	def BuildGuideContents(self, container, result, doc, ctx):
		sections = []
		for node in doc.nodes:
			if not node.get("anchor"):
				continue
			for child in node.get("children", []):
				if child.get("type") == "text" and child.get("text"):
					sections.append((node["anchor"], ctx.resolver.Text(child["text"])))
					break
		if len(sections) not in (3, 5, 6):
			return
		positions = [(-30, 0, 32)] if len(sections) == 3 else [(-30, 0, 32), (328, 3, 396)]
		for frameX, _, _ in positions:
			frame = ui.ExpandedImageBox()
			frame.SetParent(container)
			frame.LoadImage(IMG_DIR + "title_list_3.png")
			frame.SetPosition(frameX, 20)
			frame.Show()
			result.windows.append(frame)
		try:
			art = ui.ExpandedImageBox()
			art.SetParent(container)
			art.LoadImage(IMG_DIR + "banners/%d.png" % self.index)
			art.SetPosition(155 if len(sections) >= 5 else 245, 17)
			art.Show()
			result.windows.append(art)
		except:
			pass
		for i, (anchor, title) in enumerate(sections):
			column = 0 if i < 3 else 1
			rowIndex = i if i < 3 else i - 3
			x = positions[column][2]
			row = ui.Window()
			row.SetParent(container)
			row.SetPosition(x, 26 + rowIndex * 33)
			row.SetSize(170 if column else 155, 26)
			row.OnMouseLeftButtonDown = lambda key = anchor: self.ScrollToMarkupAnchor(key)
			row.Show()
			result.windows.append(row)
			label = ui.TextLine()
			label.SetParent(row)
			label.AddFlag("not_pick")
			label.SetPosition(0, 4)
			label.SetFontName(ctx.FontName(12, True))
			if self.index == 6 and i == 0:
				title = title[:17] + "..."
			label.SetText(title)
			label.SetPackedFontColor(0xffcebb98)
			label.Show()
			result.windows.append(label)

	def ScrollToMarkupAnchor(self, anchor):
		if not self.markupResult or not self.Listbox or not self.Listbox.scrollBar:
			return
		target = self.markupResult.anchors.get(anchor, 0)
		length = self.Listbox.scrollLen
		if length > 0:
			self.Listbox.scrollBar.SetPos(float(target) / float(length))

	def SetMarkupBanner(self, banner):
		if not banner:
			return
		mainParent = constInfo.GetMainParent()
		if mainParent == None:
			return
		try:
			resultpagebtn = mainParent.children["resultpagebtn"]
			resultpagebtn.LoadImage(banner)
			resultpagebtn.Show()
		except:
			pass

	def OnMarkupLink(self, kind, ident, pos):
		parent = constInfo.GetMainParent()
		if parent == None:
			return
		try:
			ident = int(ident)
		except:
			return
		parent.OnWikiLink(kind, ident, pos)

	def OnRender(self):
		WikiUI.DefaultWikiImage.OnRender(self)
		self.ClipMarkup()

	def ClipMarkup(self):
		# Build edilen pencereleri listbox gorunum araligina kirp (kismi gorunenler SetRenderingRect, digerleri Hide)
		result = self.markupResult
		if result == None:
			return
		listbox = constInfo.GetListBox()
		if listbox == None:
			return
		(lx, ly) = listbox.GetGlobalPosition()
		(ix, iy) = self.Listbox.GetGlobalPosition()
		top = max(ly, iy)
		bottom = min(ly + listbox.GetHeight() - 15, iy + self.Listbox.GetHeight())
		for w in result.windows:
			try:
				(wx, wy) = w.GetGlobalPosition()
				h = w.GetHeight()
			except:
				continue
			if h <= 0:
				continue
			canRect = isinstance(w, ui.ExpandedImageBox) or isinstance(w, ui.RenderTarget)
			if wy >= top and wy + h <= bottom:
				if w.itsRendered:
					if canRect:
						w.SetRenderingRect(0, 0, 0, 0)
					w.itsRendered = FALSE
				if not w.IsShow():
					w.Show()
			elif wy + h <= top or wy >= bottom:
				w.Hide()
			elif canRect:
				topCut = 0
				bottomCut = 0
				if wy < top:
					topCut = top - wy
				if wy + h > bottom:
					bottomCut = (wy + h) - bottom
				w.SetRenderingRect(0, WikiUI.calculateRect(h - topCut, h), 0, WikiUI.calculateRect(h - bottomCut, h))
				w.itsRendered = TRUE
				if not w.IsShow():
					w.Show()
			else:
				w.Hide()

	def CheckScrollBarNeed(self, Listbox):
		if Listbox.isNeedScrollBar():
			scrollBar = WikiUI.ScrollBarNew()
			scrollBar.SetParent(self)
			scrollBar.SetPosition(self.GetWidth()-15,2)
			scrollBar.SetScrollBarSize(355)
			scrollBar.Show()
			self.children.append(scrollBar)
			Listbox.SetScrollBar(scrollBar)
			scrollBar.SetPos(self.scrollPos)
			Listbox.OnScroll()
