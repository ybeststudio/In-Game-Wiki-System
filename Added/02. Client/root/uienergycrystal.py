#
# File Name : uienergycrystal.py
# Author    : BestStudio
# Version   : 1.0
# Date      : 2026-11-15
#
import app
import net
import player
import item
import chat
import ui
import uiCommon
import localeInfo
import constInfo
import mouseModule

PATH = "d:/ymir work/ui/game/energy_crystal/"
COMMON = "d:/ymir work/ui/game/common/"
GAUGE = "d:/ymir work/ui/game/67_bonus/gauge_full.png"

CRYSTAL_FIRST, CRYSTAL_LAST = 51040, 51049
UNLOCKER_VNUM = 51052
REFINE_SCROLLS = (51050, 51051)
SOURCE_ITEMS = (51031, 51032, 51033, 51034, 51035, 51036, 51037, 51038, 51039, 51050, 51051, 51053, 51054, 51055, 51058)
BONUS_ROWS = (
	(340, "ENERGY_CRYSTAL_BONUS_EREBUS", 51033),		# APPLY_ATTBONUS_EREBUS
	(342, "ENERGY_CRYSTAL_BONUS_DUNGEON", 51032),		# APPLY_ATTBONUS_DUNGEON
	(341, "ENERGY_CRYSTAL_BONUS_MELEY", 51034),		# APPLY_ATTBONUS_MELEY
	(336, "ENERGY_CRYSTAL_BONUS_AVERAGE_PVM", 51031),	# APPLY_ATTBONUS_MEDI_PVM
	(332, "ENERGY_CRYSTAL_BONUS_ELEMENT", 51035),
)

COLOR_TEXT = 0xffcabdab
COLOR_ON = 0xff9fd6a8
COLOR_OFF = 0xffe57875
CENTER_X = 124
EMBLEM_Y = 120


def _InventorySize():
	return player.INVENTORY_PAGE_SIZE * player.INVENTORY_PAGE_COUNT


def FindCrystalCell():
	for cell in xrange(_InventorySize()):
		if CRYSTAL_FIRST <= player.GetItemIndex(cell) <= CRYSTAL_LAST:
			return cell
	return -1


def FindItemCell(vnum):
	for cell in xrange(_InventorySize()):
		if player.GetItemIndex(cell) == vnum:
			return cell
	return -1


def _ItemName(vnum):
	try:
		return item.GetItemNameByVnum(vnum)
	except:
		return ""


def _TimeText(seconds):
	seconds = max(0, int(seconds))
	h, m, s = seconds / 3600, seconds % 3600 / 60, seconds % 60
	parts = []
	if h:
		parts.append(localeInfo.ENERGY_CRYSTAL_TIME_H.format(h))
	if h or m:
		parts.append(localeInfo.ENERGY_CRYSTAL_TIME_M.format(m))
	parts.append(localeInfo.ENERGY_CRYSTAL_TIME_S.format(s))
	return " ".join(parts)


def _CapacityText(seconds):
	if seconds and seconds % 86400 == 0:
		return localeInfo.ENERGY_CRYSTAL_TIME_D.format(seconds / 86400)
	return _TimeText(seconds)


def GetCrystalSummaryLines(cell, rate, cap, energy, energyMax):
	lines = [(localeInfo.ENERGY_CRYSTAL_RATE.format(rate / 10.0, cap), COLOR_ON)]
	gains = dict((applyType, gain) for (applyType, gain, unlocked) in constInfo.ENERGY_CRYSTAL_BONUS)
	owned = set(player.GetItemAttribute(cell, i)[0] for i in xrange(5))
	for (applyType, labelKey, unlockerVnum) in BONUS_ROWS:
		if applyType in owned:
			lines.append((localeInfo.ENERGY_CRYSTAL_BONUS_GAIN.format(localeInfo.GetText(labelKey, ""), gains.get(applyType, 0)), COLOR_ON))
	lines.append((localeInfo.ENERGY_CRYSTAL_TIME.format(_TimeText(energy), _CapacityText(energyMax)), COLOR_TEXT))
	return lines


class UnlockDialog(ui.Board):
	# "Bunun tamamlanmasi icin <Enerji Kristali Acici> gerekir." at y 135, accept (63, 145) / cancel (144, 145)
	WIDTH, HEIGHT = 260, 178

	def __init__(self):
		ui.Board.__init__(self)
		self.AddFlag("float")
		self.SetSize(self.WIDTH, self.HEIGHT)
		self.onAccept = None
		self.keep = []
		inner = ui.ThinBoardNew()
		inner.SetParent(self)
		inner.SetPosition(8, 8)
		inner.SetSize(self.WIDTH - 17, self.HEIGHT - 17)
		inner.AddFlag("not_pick")
		inner.Show()
		self.keep.append(inner)
		question = ui.TextLine()
		question.SetParent(self)
		question.SetHorizontalAlignCenter()
		question.SetVerticalAlignCenter()
		question.SetPosition(self.WIDTH / 2, 15)
		question.SetPackedFontColor(COLOR_TEXT)
		question.SetText(localeInfo.ENERGY_CRYSTAL_UNLOCK_CONFIRM)
		question.Show()
		self.keep.append(question)

		for i in xrange(3):
			frame = ui.ImageBox()
			frame.SetParent(self)
			frame.LoadImage(COMMON + "slots/slot_32x32.png")
			frame.SetPosition(114, 26 + 32 * i)
			frame.AddFlag("not_pick")
			frame.Show()
			self.keep.append(frame)
		self.slot = ui.SlotWindow()
		self.slot.SetParent(self)
		self.slot.SetPosition(114, 26)
		self.slot.SetSize(32, 96)
		for i in xrange(3):
			self.slot.AppendSlot(i, 0, 32 * i, 32, 32)
		self.slot.SetItemSlot(0, UNLOCKER_VNUM, 1)
		self.slot.Show()

		need = ui.TextLine()
		need.SetParent(self)
		need.SetHorizontalAlignCenter()
		need.SetVerticalAlignCenter()
		need.SetPosition(self.WIDTH / 2, 135)
		need.SetPackedFontColor(COLOR_TEXT)
		need.SetText(localeInfo.ENERGY_CRYSTAL_UNLOCK_REQUIRES.format(_ItemName(UNLOCKER_VNUM)))
		need.Show()
		self.keep.append(need)

		for (x, kind, event) in ((63, "accept", self.__Accept), (144, "cancel", self.Close)):
			button = ui.Button()
			button.SetParent(self)
			button.SetPosition(x, 145)
			button.SetUpVisual(COMMON + "button_%s_norm.png" % kind)
			button.SetOverVisual(COMMON + "button_%s_hover.png" % kind)
			button.SetDownVisual(COMMON + "button_%s_down.png" % kind)
			button.SetEvent(ui.__mem_func__(event))
			button.Show()
			self.keep.append(button)
		self.Hide()

	def __del__(self):
		ui.Board.__del__(self)

	def Open(self, parent, onAccept):
		self.onAccept = onAccept
		(x, y) = parent.GetGlobalPosition()
		self.SetPosition(x - 6, y + 25)
		self.Show()
		self.SetTop()

	def __Accept(self):
		onAccept = self.onAccept
		self.Close()
		if onAccept:
			onAccept()

	def Close(self):
		self.onAccept = None
		self.Hide()

	def Destroy(self):
		self.Close()
		self.keep = []

	def OnPressEscapeKey(self):
		self.Close()
		return True


class EnergyCrystalWindow(ui.BoardWithTitleBar):
	WIDTH = 248
	HEIGHT = 467
	LOCKED_HEIGHT = 229
	PAGE_SIZE = 4

	def __init__(self):
		self.unlockDialog = None
		self.lockToolTip = None
		self.interface = None
		ui.BoardWithTitleBar.__init__(self)
		self.tooltipItem = None
		self.questionDialog = None
		self.page = 0
		self.cell = -1
		self.lastRefresh = 0.0
		self.AddFlag("movable")
		self.AddFlag("float")
		self.SetSize(self.WIDTH, self.HEIGHT)
		self.SetTitleName(localeInfo.ENERGY_CRYSTAL_TITLE)
		self.SetCloseEvent(ui.__mem_func__(self.Close))
		self.__Build()
		self.Hide()

	def __del__(self):
		ui.BoardWithTitleBar.__del__(self)

	# ----------------------------------------------------------------- widgets
	def __Image(self, x, y, path):
		image = ui.ImageBox()
		image.SetParent(self)
		image.LoadImage(path)
		image.SetPosition(x, y)
		image.AddFlag("not_pick")
		image.Show()
		return image

	def __Text(self, x, y, color = COLOR_TEXT, bold = False):
		text = ui.TextLine()
		text.SetParent(self)
		if bold:
			text.SetFontName("Tahoma:12b")
		text.SetPackedFontColor(color)
		text.SetHorizontalAlignCenter()
		text.SetVerticalAlignCenter()
		text.SetPosition(x, y)
		text.AddFlag("not_pick")
		text.Show()
		return text

	def __Button(self, x, y, prefix, text = ""):
		button = ui.Button()
		button.SetParent(self)
		button.SetPosition(x, y)
		button.SetUpVisual(prefix[0])
		button.SetOverVisual(prefix[1])
		button.SetDownVisual(prefix[2])
		if text:
			button.SetText(text)
		button.Show()
		return button

	def __Build(self):
		self.bg = self.__Image(10, 29, PATH + "bg.png")

		self.circle = ui.AniImageBox()
		self.circle.SetParent(self)
		for i in xrange(60):	# circle/000-059
			self.circle.AppendImage(PATH + "circle/%03d.png" % i)
		self.circle.SetDelay(2)
		self.circle.SetPosition(CENTER_X - 59, EMBLEM_Y - 59)
		self.circle.AddFlag("not_pick")
		self.circle.Hide()

		self.slot = ui.SlotWindow()
		self.slot.SetParent(self)
		self.slot.SetPosition(CENTER_X - 16, EMBLEM_Y - 16)
		self.slot.SetSize(32, 32)
		self.slot.AppendSlot(0, 0, 0, 32, 32)
		self.slot.SetSelectEmptySlotEvent(ui.__mem_func__(self.__OnDropOnCrystal))
		self.slot.SetSelectItemSlotEvent(ui.__mem_func__(self.__OnDropOnCrystal))
		self.slot.SetOverInItemEvent(ui.__mem_func__(self.__OnOverCrystal))
		self.slot.SetOverOutItemEvent(ui.__mem_func__(self.__OnOutCrystal))
		self.slot.Show()

		self.unlockButton = self.__Button(CENTER_X - 12, EMBLEM_Y - 12, (PATH + "btn_unlock.png", PATH + "btn_unlock_hover.png", PATH + "btn_unlock_clicked.png"))
		self.unlockButton.SetEvent(ui.__mem_func__(self.__AskUnlockCrystal))
		self.unlockText = self.__Text(CENTER_X, 205, COLOR_TEXT)
		self.unlockText.SetText(localeInfo.ENERGY_CRYSTAL_UNLOCK)

		self.wikiButton = self.__Button(209, 39, (COMMON + "button_wiki_norm.png", COMMON + "button_wiki_hover.png", COMMON + "button_wiki_down.png"))
		self.wikiButton.SetEvent(ui.__mem_func__(self.__OpenWiki))

		self.nameBar = self.__Image(10, 212, PATH + "bg3.png")
		self.nameText = self.__Text(CENTER_X, 225, COLOR_TEXT, True)
		self.helpButton = self.__Button(219, 215, (COMMON + "button_info_circle_norm.png", COMMON + "button_info_circle_hover.png", COMMON + "button_info_circle_down.png"))
		self.helpButton.SetShowToolTipEvent(ui.__mem_func__(self.__ShowHelp))
		self.helpButton.SetHideToolTipEvent(ui.__mem_func__(self.__HideHelp))

		self.rateBar = self.__Image(10, 240, PATH + "bg3.png")
		self.rateText = self.__Text(CENTER_X, 253)

		self.listBg = self.__Image(10, 268, PATH + "bg2.png")
		self.rowTexts = []
		self.lockButtons = []
		for i in xrange(self.PAGE_SIZE):
			y = 268 + 28 * i
			text = ui.TextLine()
			text.SetParent(self)
			text.SetVerticalAlignCenter()
			text.SetPosition(38, y + 15)
			text.AddFlag("not_pick")
			text.Show()
			self.rowTexts.append(text)
			lock = self.__Button(214, y + 3, (PATH + "btn_unlock.png", PATH + "btn_unlock_hover.png", PATH + "btn_unlock_clicked.png"))
			lock.SetEvent(ui.__mem_func__(self.__AskBonusUnlock), i)
			self.lockButtons.append(lock)

		self.gauge = ui.ExpandedImageBox()
		self.gauge.SetParent(self)
		self.gauge.LoadImage(GAUGE)
		self.gauge.SetScale(229.0 / 210.0, 11.0 / 9.0)
		self.gauge.SetPosition(10, 385)
		self.gauge.AddFlag("not_pick")
		self.gauge.Show()
		self.energyText = self.__Text(CENTER_X, 411)

		self.activateButton = self.__Button(10, 425, (PATH + "btn_activate.png", PATH + "btn_activate_hover.png", PATH + "btn_activate_clicked.png"), localeInfo.ENERGY_CRYSTAL_ACTIVATE)
		self.activateButton.SetEvent(ui.__mem_func__(self.__Toggle))

		self.helpToolTip = None

	# ----------------------------------------------------------------- open / close
	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = tooltipItem

	def Open(self):
		self.page = 0
		self.Refresh()
		if self.cell >= 0:
			net.SendChatPacket("/energy_crystal info %d" % self.cell)
		self.Show()
		self.SetTop()

	def Toggle(self):
		if self.IsShow():
			self.Close()
		else:
			self.Open()

	def Close(self):
		self.__CloseQuestion()
		self.__HideHelp()
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()
		self.Hide()

	def Destroy(self):
		self.Close()
		self.tooltipItem = None
		if self.unlockDialog:
			self.unlockDialog.Destroy()
			self.unlockDialog = None

	def OnPressEscapeKey(self):
		self.Close()
		return True

	# ----------------------------------------------------------------- refresh
	def __SetLocked(self, locked):
		unlockedWidgets = (self.nameBar, self.nameText, self.helpButton, self.rateBar, self.rateText, self.listBg, self.gauge, self.energyText, self.activateButton)
		for widget in unlockedWidgets:
			widget.Hide() if locked else widget.Show()
		for widget in self.rowTexts + self.lockButtons:
			widget.Hide() if locked else widget.Show()
		self.unlockButton.Hide()
		self.unlockText.Hide()
		self.SetSize(self.WIDTH, self.LOCKED_HEIGHT if locked else self.HEIGHT)

	def Refresh(self):
		self.lastRefresh = app.GetTime()
		self.cell = FindCrystalCell()
		if self.cell < 0:
			self.__SetLocked(True)
			self.slot.SetItemSlot(0, UNLOCKER_VNUM, 0)
			self.circle.Hide()
			self.slot.RefreshSlot()
			return
		self.__SetLocked(False)

		vnum = player.GetItemIndex(self.cell)
		item.SelectItem(vnum)
		cap = item.GetValue(0) / 100.0
		energyMax = item.GetValue(1) or 86400
		energy = max(0, player.GetItemMetinSocket(self.cell, 0))
		rate = player.GetItemMetinSocket(self.cell, 1)
		active = player.GetItemMetinSocket(self.cell, 2) and energy > 0

		self.slot.SetItemSlot(0, vnum, 1)
		self.slot.RefreshSlot()
		self.nameText.SetText(item.GetItemName())
		self.rateText.SetText(localeInfo.ENERGY_CRYSTAL_RATE.format(rate / 10.0, cap))

		self.gauge.SetRenderingRect(0.0, 0.0, -(1.0 - min(1.0, float(energy) / energyMax)), 0.0)
		self.energyText.SetText(localeInfo.ENERGY_CRYSTAL_TIME.format(_TimeText(energy), _CapacityText(energyMax)))
		self.activateButton.SetText(localeInfo.ENERGY_CRYSTAL_TURN_OFF if active else localeInfo.ENERGY_CRYSTAL_ACTIVATE)
		if active:
			self.circle.Show()
		else:
			self.circle.Hide()
		self.__RefreshRows()

	def __Rows(self):
		bonus = dict((applyType, (gain, unlocked)) for (applyType, gain, unlocked) in constInfo.ENERGY_CRYSTAL_BONUS)
		# unlocked = the attributes of the crystal itself (the server list can belong to an older crystal)
		owned = set()
		if self.cell >= 0:
			for i in xrange(5):
				(attrType, attrValue) = player.GetItemAttribute(self.cell, i)
				if attrType:
					owned.add(attrType)
		rows = []
		for (applyType, labelKey, unlockerVnum) in BONUS_ROWS:
			gain = bonus.get(applyType, (0, 0))[0]
			unlocked = applyType in owned
			rows.append((applyType, localeInfo.GetText(labelKey, ""), unlockerVnum, gain, unlocked))
		return rows

	def __RefreshRows(self):
		rows = self.__Rows()
		pages = max(1, (len(rows) + self.PAGE_SIZE - 1) / self.PAGE_SIZE)
		self.page = max(0, min(self.page, pages - 1))
		for i in xrange(self.PAGE_SIZE):
			index = self.page * self.PAGE_SIZE + i
			text, lock = self.rowTexts[i], self.lockButtons[i]
			if index >= len(rows):
				text.SetText("")
				lock.Hide()
				continue
			(applyType, label, unlockerVnum, gain, unlocked) = rows[index]
			text.SetText(localeInfo.ENERGY_CRYSTAL_BONUS_GAIN.format(label, gain))
			text.SetPackedFontColor(COLOR_ON if unlocked else COLOR_OFF)
			if unlocked:
				lock.Hide()
			else:
				lock.Show()

	def OnUpdate(self):
		if app.GetTime() - self.lastRefresh >= 1.0:
			self.Refresh()

	def OnMouseWheel(self, delta):
		rows = len(BONUS_ROWS)
		if rows <= self.PAGE_SIZE:
			return False
		self.page += -1 if delta > 0 else 1
		self.__RefreshRows()
		return True

	# ----------------------------------------------------------------- crystal slot
	def __OnOverCrystal(self, slot):
		if self.cell < 0:
			import uiToolTip
			if not self.lockToolTip:
				self.lockToolTip = uiToolTip.ToolTip()
				self.lockToolTip.AutoAppendTextLine(localeInfo.ENERGY_CRYSTAL_UNLOCK)
				self.lockToolTip.AlignHorizonalCenter()
			self.lockToolTip.ShowToolTip()
			return
		if self.tooltipItem:
			self.tooltipItem.SetInventoryItem(self.cell)

	def __OnOutCrystal(self):
		if self.lockToolTip:
			self.lockToolTip.HideToolTip()
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def __OnDropOnCrystal(self, slot):
		if not mouseModule.mouseController.isAttached():
			if self.cell < 0:
				self.__AskUnlockCrystal()
			return
		attachedType = mouseModule.mouseController.GetAttachedType()
		sourceCell = mouseModule.mouseController.GetAttachedSlotNumber()
		mouseModule.mouseController.DeattachObject()
		if attachedType != player.SLOT_TYPE_INVENTORY or self.cell < 0:
			return
		vnum = player.GetItemIndex(sourceCell)
		if vnum not in SOURCE_ITEMS:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.ENERGY_CRYSTAL_INVALID_TARGET)
			return
		if vnum in REFINE_SCROLLS:
			self.__RegisterAutoRefine(sourceCell)
			net.SendItemUseToItemPacket(sourceCell, self.cell)
			return
		self.__Ask(localeInfo.ENERGY_CRYSTAL_CONSUME.format(_ItemName(vnum)), lambda: self.__Use(sourceCell))

	def __RegisterAutoRefine(self, sourceCell):
		if app.ENABLE_AUTO_REFINE:
			constInfo.AUTO_REFINE_TYPE = 1
			constInfo.AUTO_REFINE_DATA["ITEM"] = [sourceCell, self.cell]

	def __Use(self, sourceCell):
		if self.cell >= 0:
			net.SendChatPacket("/energy_crystal use %d %d" % (self.cell, sourceCell))

	# ----------------------------------------------------------------- actions
	def __Toggle(self):
		if self.cell >= 0:
			net.SendChatPacket("/energy_crystal toggle %d" % self.cell)

	def __AskUnlockCrystal(self):
		self.__OnOutCrystal()
		if not self.unlockDialog:
			self.unlockDialog = UnlockDialog()
		self.unlockDialog.Open(self, ui.__mem_func__(self.__UnlockCrystal))

	def __UnlockCrystal(self):
		cell = FindItemCell(UNLOCKER_VNUM)
		if cell < 0:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.ENERGY_CRYSTAL_UNLOCK_MISSING)
			return
		net.SendItemUsePacket(cell)

	def __AskBonusUnlock(self, rowIndex):
		rows = self.__Rows()
		index = self.page * self.PAGE_SIZE + rowIndex
		if index >= len(rows) or self.cell < 0:
			return
		(applyType, label, unlockerVnum, gain, unlocked) = rows[index]
		if unlocked:
			return
		cell = FindItemCell(unlockerVnum)
		if cell < 0:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.ENERGY_CRYSTAL_BONUS_ITEM_MISSING.format(_ItemName(unlockerVnum)))
			return
		self.__Ask(localeInfo.ENERGY_CRYSTAL_PERMANENT_CONFIRM.format(label), lambda: self.__Use(cell))

	def SetInterface(self, interface):
		from _weakref import proxy
		self.interface = proxy(interface)

	def __OpenWiki(self):
		interface = self.interface
		if interface and app.ENABLE_WIKI_SYSTEM:
			interface.OpenWikiWindow()

	# ----------------------------------------------------------------- question / help
	def __Ask(self, text, onAccept):
		self.__CloseQuestion()
		dialog = uiCommon.QuestionDialog()
		dialog.SetText(text)
		dialog.SetAcceptEvent(lambda: (onAccept(), self.__CloseQuestion()))
		dialog.SetCancelEvent(ui.__mem_func__(self.__CloseQuestion))
		dialog.Open()
		self.questionDialog = dialog

	def __CloseQuestion(self):
		if self.questionDialog:
			self.questionDialog.Close()
			self.questionDialog = None
		if self.unlockDialog:
			self.unlockDialog.Close()

	def __ShowHelp(self):
		import uiToolTip
		if not self.helpToolTip:
			self.helpToolTip = uiToolTip.ToolTip()
		tip = self.helpToolTip
		tip.ClearToolTip()
		import re
		for part in localeInfo.ENERGY_CRYSTAL_HELP_SHORT.split("^"):
			part = part.strip()
			m = re.match(r"^\|c([0-9a-fA-F]{8})(.*?)\|r$", part)
			if m:
				tip.AutoAppendTextLine(m.group(2), int(m.group(1), 16))
			elif part:
				tip.AutoAppendTextLine(part, COLOR_TEXT)
		tip.AlignHorizonalCenter()
		tip.ShowToolTip()

	def __HideHelp(self):
		if self.helpToolTip:
			self.helpToolTip.HideToolTip()
