#
# File Name : uibattlepass.py
# Author    : BestStudio
# Version   : 1.0
# Date      : 2026-11-14
#

import app
import net
import item
import chat
import ui
import wndMgr
import localeInfo
import uiCommon

NEW_BP_PATH = "d:/ymir work/ui/game/new_battlepass/%s"
SIDE_PATH = "d:/ymir work/ui/game/battlepass/side_bar/buttons/%s"
CONFIG_PATH = "config_json/battlepass_config.json"

KIND_PASS = 0
KIND_EVENT = 1

TEXT_COLOR = 0xffcabdab
TITLE_COLOR = 0xfff1e6c0
VALUE_COLOR = 0xffd1b183
DONE_COLOR = 0xffa0be8e
HIGHLIGHT_COLOR = 0xfff4e6c3
BOLD_FONT = "Tahoma:12b"

REWARD_W = 100
LEVEL_X = 154			# window-relative level strip / level clip (437 wide)
LEVEL_W = 437
SCROLL_BAR_W = 90
BONUS_GAP = 20
HELP_COLOR = 0xffe6e0d3
CHECK_PATH = "d:/ymir work/ui/game/common/checkbox_new_%s.png"
REWARD_H = 130
LIST_X = 152
LIST_W = 439
FREE_Y = 114
PREMIUM_Y = 261
QUEST_X = 42
QUEST_Y = 119
QUEST_H = 52
QUEST_GAP = 2
QUEST_VIEW_H = 272
QUEST_ROWS = 5

QUEST_INFO = {
	1: ("BATTLEPASS_QUEST_KILL_MONSTERS", "kill_monsters.png", "BATTLEPASS_QUEST_DESC_LEVEL_15"),
	2: ("BATTLEPASS_QUEST_DESTROY_METIN_STONES", "destroy_metin_stones.png", "BATTLEPASS_QUEST_DESC_LEVEL_15"),
	3: ("BATTLEPASS_QUEST_KILL_BOSSES", "kill_bosses.png", "BATTLEPASS_QUEST_DESC_LEVEL_20"),
	4: ("BATTLEPASS_QUEST_FINISH_DUNGEON", "dungeons.png", "BATTLEPASS_QUEST_DESC_DUNGEON"),
	5: ("BATTLEPASS_QUEST_KILL_PLAYERS", "kill_players.png", "BATTLEPASS_QUEST_DESC_PLAYERS"),
	6: ("BATTLEPASS_QUEST_CATCH_FISH", "catch_fish.png", "BATTLEPASS_QUEST_DESC_FISH"),
	7: ("BATTLEPASS_QUEST_MINING", "mining.png", "BATTLEPASS_QUEST_DESC_MINING"),
	8: ("BATTLEPASS_QUEST_RECHARGE_DEW_DRAGON", "recharge_dew.png", "BATTLEPASS_QUEST_DESC_DEW"),
	9: ("BATTLEPASS_QUEST_GET_STONE_BAG", "stone_bag.png", "BATTLEPASS_QUEST_DESC_STONE_BAG"),
	10: ("BATTLEPASS_QUEST_SELL_ITEMS_AT_PNJ", "sell_items_at_npc.png", "BATTLEPASS_QUEST_DESC_SELL"),
	11: ("BATTLEPASS_QUEST_BUY_ITEM_TO_PNJ", "sell_items_at_npc.png", "BATTLEPASS_QUEST_DESC_BUY"),
	12: ("BATTLEPASS_QUEST_CRAFT_ITEMS", "craft_items.png", "BATTLEPASS_QUEST_DESC_CRAFT"),
	13: ("BATTLEPASS_QUEST_FINISH_QUEST_BOOK", "complete_mission_books.png", "BATTLEPASS_QUEST_DESC_QUEST_BOOK"),
	14: ("BATTLEPASS_QUEST_USE_SWITCH", "use_switch.png", "BATTLEPASS_QUEST_DESC_SWITCH"),
	15: ("BATTLEPASS_QUEST_ADD_67_BONUS", "add_67_bonus.png", "BATTLEPASS_QUEST_DESC_67"),
	16: ("BATTLEPASS_QUEST_ADD_ORE", "add_ore.png", "BATTLEPASS_QUEST_DESC_ORE"),
	17: ("BATTLEPASS_QUEST_REROLL_LUCKYBOX", "reroll_token.png", "BATTLEPASS_QUEST_DESC_LUCKYBOX"),
	18: ("BATTLEPASS_QUEST_UPGRADE_EQUIPMENT", "upgrade_equipment.png", "BATTLEPASS_QUEST_DESC_UPGRADE"),
	19: ("BATTLEPASS_QUEST_OPEN_CHESTS", "open_chests.png", "BATTLEPASS_QUEST_DESC_CHEST"),
	20: ("BATTLEPASS_QUEST_OPEN_EGGS", "open_eggs.png", "BATTLEPASS_QUEST_DESC_EGG"),
	21: ("BATTLEPASS_QUEST_BUY_ITEM_WITH_GAYA", "buy_item_with_gaya.png", "BATTLEPASS_QUEST_DESC_GAYA"),
	22: ("BATTLEPASS_QUEST_SEND_GENERAL_CHAT_MESSAGES", "send_general_chat_messages.png", "BATTLEPASS_QUEST_DESC_CHAT"),
	23: ("BATTLEPASS_QUEST_GET_SILVER_COIN", "get_silver_coins.png", "BATTLEPASS_QUEST_DESC_SILVER"),
	24: ("BATTLEPASS_QUEST_FEED_PET", "feed_pet.png", "BATTLEPASS_QUEST_DESC_PET"),
	25: ("BATTLEPASS_QUEST_BUILD_SANDCASTLE", "craft_items.png", "BATTLEPASS_QUEST_DESC_SANDCASTLE"),
	27: ("BATTLEPASS_QUEST_OPEN_MYSTICAL_CHESTS", "open_chests.png", "BATTLEPASS_QUEST_DESC_MYSTICAL"),
	28: ("BATTLEPASS_QUEST_DESTROY_TARGET_METIN", "destroy_metin_stones.png", "BATTLEPASS_QUEST_DESC_TARGET_METIN"),
	29: ("BATTLEPASS_QUEST_DESTROY_SUMMER_SHRINES", "destroy_metin_stones.png", "BATTLEPASS_QUEST_DESC_SHRINES"),
	30: ("BATTLEPASS_QUEST_FINISH_SUMMER_STONE_HUNT", "destroy_metin_stones.png", "BATTLEPASS_QUEST_DESC_STONE_HUNT"),
	31: ("BATTLEPASS_QUEST_UPGRADE_CIRCUS_SKILLS", "upgrade_equipment.png", "BATTLEPASS_QUEST_DESC_CIRCUS"),
	32: ("BATTLEPASS_QUEST_HARVEST_HALLOWEEN_FLOWERS", "open_eggs.png", "BATTLEPASS_QUEST_DESC_FLOWERS"),
	33: ("BATTLEPASS_QUEST_CATCH_HAUNTED_PEARLS", "catch_fish.png", "BATTLEPASS_QUEST_DESC_PEARLS"),
	34: ("BATTLEPASS_QUEST_FINISH_HALLOWEEN_DAILY", "complete_mission_books.png", "BATTLEPASS_QUEST_DESC_HALLOWEEN_DAILY"),
}
MISSION_NAME_TO_TYPE = {
	"KILL_MONSTER": 1, "DESTROY_METIN": 2, "KILL_BOSS": 3, "FINISH_DUNGEON": 4, "KILL_PLAYERS": 5, "CATCH_FISH": 6,
	"MINING": 7, "RECHARGE_DEW_DRAGON": 8, "GET_SPIRIT_SHARD": 9, "SELL_ITEMS_AT_PNJ": 10, "BUY_ITEM_TO_PNJ": 11,
	"CRAFT_ITEMS": 12, "FINISH_QUEST_BOOK": 13, "USE_SWITCH": 14, "ADD_67_BONUS": 15, "ADD_ORE": 16, "REROLL_LUCKYBOX": 17,
	"UPGRADE_STUFF": 18, "OPEN_CHEST": 19, "OPEN_EGG": 20, "BUY_ITEM_GAYA": 21, "SEND_MSG_GENERAL_CHAT": 22,
	"GET_SILVER_COIN": 23, "FEED_PET": 24, "BUILD_SANDCASTLE": 25, "OPEN_MYSTICAL_CHEST": 27, "DESTROY_TARGET_METIN": 28,
	"DESTROY_SUMMER_SHRINES": 29, "FINISH_SUMMER_STONE_HUNT": 30, "UPGRADE_CIRCUS_SKILLS": 31,
	"HARVEST_HALLOWEEN_FLOWERS": 32, "CATCH_HAUNTED_PEARLS": 33, "FINISH_HALLOWEEN_DAILY": 34,
}

# BPResult codes (battlepass_renewal.cpp EResult)
(RESULT_NO_SEASON, RESULT_LOCKED, RESULT_NO_PREMIUM, RESULT_CLAIMED, RESULT_REWARD, RESULT_PREMIUM_ON, RESULT_PREMIUM_HAD,
	RESULT_EXP, RESULT_LEVEL_UP, RESULT_MISSION_DONE, RESULT_INVENTORY) = range(11)


def _L(key, default = ""):
	return localeInfo.GetText(key, default)


def _Stamp(text):
	"""'2026-11-14' / '2026-11-14T00:00:00' -> 20261114000000 (comparable number)."""
	text = text.replace("T", " ")
	(date, _, time) = text.partition(" ")
	return int(date.replace("-", "") + (time or "00:00:00").replace(":", ""))


def _StampToSeconds(stamp):
	import time
	s = str(stamp)
	try:
		return int(time.mktime((int(s[0:4]), int(s[4:6]), int(s[6:8]), int(s[8:10]), int(s[10:12]), int(s[12:14]), 0, 0, -1)))
	except Exception:
		return 0


def _TimeText(seconds):
	seconds = max(0, int(seconds))
	return "%dd %02dh %02dm" % (seconds / 86400, (seconds % 86400) / 3600, (seconds % 3600) / 60)


def LoadConfig():
	try:
		import wikicontent
		return wikicontent.LoadCommonJson(CONFIG_PATH) or {}
	except Exception:
		return {}


class FilterCheckBox(ui.Window):
	def __init__(self, parent, x, y, text):
		ui.Window.__init__(self)
		self.SetParent(parent)
		self.SetPosition(x, y)
		self.checked = False
		self.event = None
		self.box = ui.ImageBox()
		self.box.SetParent(self)
		self.box.AddFlag("not_pick")
		self.box.LoadImage(CHECK_PATH % "unselected")
		self.box.Show()
		self.text = ui.TextLine()
		self.text.SetParent(self)
		self.text.SetPosition(20, 7)
		self.text.SetVerticalAlignCenter()
		self.text.SetPackedFontColor(TEXT_COLOR)
		self.text.SetOutline()
		self.text.AddFlag("not_pick")
		self.text.SetText(text)
		self.text.Show()
		self.SetSize(20 + self.text.GetTextSize()[0], 16)
		self.Show()

	def __del__(self):
		ui.Window.__del__(self)

	def SetEvent(self, event):
		self.event = event

	def GetCheckStatus(self):
		return self.checked

	def OnMouseLeftButtonUp(self):
		self.checked = not self.checked
		self.box.LoadImage(CHECK_PATH % ("selected" if self.checked else "unselected"))
		if self.event:
			self.event()
		return True


def WrapText(text, limit):
	lines = []
	line = ""
	for word in text.split(" "):
		test = (line + " " + word) if line else word
		if line and len(test) > limit:
			lines.append(line)
			line = word
		else:
			line = test
	if line:
		lines.append(line)
	return lines


class BonusSlot(ui.Window):
	def __init__(self, parent, textParent, owner):
		ui.Window.__init__(self)
		self.SetParent(parent)
		self.SetSize(REWARD_W, REWARD_H)
		self.owner = owner
		self.vnum = 0
		self.keep = []
		bg = ui.ExpandedImageBox()
		bg.SetParent(self)
		bg.LoadImage(NEW_BP_PATH % "horizontalscrollpage/bg_reward_premium.png")
		bg.AddFlag("not_pick")
		bg.Show()
		self.keep.append(bg)
		icon = ui.ExpandedImageBox()
		icon.SetParent(self)
		icon.SetPosition(34, 29)
		icon.OnMouseOverIn = ui.__mem_func__(self.__ChestIn)
		icon.OnMouseOverOut = ui.__mem_func__(self.__ChestOut)
		icon.Show()
		self.icon = icon
		count = ui.TextLine()
		count.SetParent(textParent)
		count.SetHorizontalAlignRight()
		count.SetOutline()
		count.AddFlag("not_pick")
		count.Show()
		self.count = count
		title = ui.TextLine()
		title.SetParent(textParent)
		title.SetHorizontalAlignCenter()
		title.SetVerticalAlignCenter()
		title.SetFontName(BOLD_FONT)
		title.SetPackedFontColor(HIGHLIGHT_COLOR)
		title.SetOutline()
		title.SetText(localeInfo.BATTLEPASS_BONUS_CHEST)
		title.AddFlag("not_pick")
		title.Show()
		self.title = title
		helpIcon = ui.ExpandedImageBox()
		helpIcon.SetParent(self)
		helpIcon.SetPosition(78, 6)
		helpIcon.LoadImage("d:/ymir work/ui/pattern/q_mark_01.tga")
		helpIcon.OnMouseOverIn = ui.__mem_func__(self.__HelpIn)
		helpIcon.OnMouseOverOut = ui.__mem_func__(self.__HelpOut)
		helpIcon.Show()
		self.helpIcon = helpIcon
		self.helpLines = []
		self.helpText = ""
		self.helpTip = None
		self.Show()

	def __del__(self):
		ui.Window.__del__(self)

	def SetData(self, vnum, count, maxLevel, levelExp):
		self.vnum = vnum
		name = ""
		if vnum:
			item.SelectItem(vnum)
			self.icon.LoadImage(item.GetIconImageFileName())
			self.icon.Show()
			self.count.SetText(str(count))
			name = item.GetItemName()
		else:
			self.icon.Hide()
			self.count.SetText("")
		text = localeInfo.BATTLEPASS_BONUS_CHEST_HELP
		try:
			text = text % (maxLevel, levelExp, count, name)
		except TypeError:
			pass
		self.helpText = text
		self.helpLines = [localeInfo.BATTLEPASS_BONUS_CHEST] + WrapText(text, 76) + [localeInfo.BATTLEPASS_BONUS_CHEST_PREVIEW]

	def Place(self, x, y, left, top):
		self.SetPosition(x, y)
		self.count.SetPosition(left + x + 64, top + y + 52)
		self.title.SetPosition(left + x + 50, top + y + 97)

	def SetTextVisible(self, visible):
		for w in (self.count, self.title):
			w.Show() if visible else w.Hide()

	def __ChestIn(self):
		if not self.helpText:
			return
		import uiToolTip
		measure = ui.TextLine()
		measure.SetFontName(localeInfo.UI_DEF_FONT)
		measure.SetText(self.helpText)
		width = measure.GetTextSize()[0]
		if width < 100:		# measuring failed: ~6 px per character
			width = len(self.helpText) * 6
		tip = uiToolTip.ToolTip(width + 20)
		tip.AppendTextLine(self.helpText, HELP_COLOR)
		tip.ShowToolTip()
		self.helpTip = tip

	def __ChestOut(self):
		if self.helpTip:
			self.helpTip.HideToolTip()
			self.helpTip = None

	def __HelpIn(self):
		self.helpIcon.LoadImage("d:/ymir work/ui/pattern/q_mark_02.tga")
		import uiToolTip
		tip = uiToolTip.ToolTip(400)
		for line in self.helpLines:
			if line:
				tip.AppendTextLine(line, HELP_COLOR)
		tip.ShowToolTip()
		self.helpTip = tip

	def __HelpOut(self):
		self.helpIcon.LoadImage("d:/ymir work/ui/pattern/q_mark_01.tga")
		if self.helpTip:
			self.helpTip.HideToolTip()
			self.helpTip = None


class RewardSlot(ui.Window):
	def __init__(self, parent, premium, owner):
		ui.Window.__init__(self)
		self.SetParent(parent)
		self.SetSize(REWARD_W, REWARD_H)
		self.owner = owner
		self.premium = premium
		self.index = 0
		self.vnum = 0
		self.keep = []
		bg = ui.ExpandedImageBox()
		bg.SetParent(self)
		bg.LoadImage(NEW_BP_PATH % ("horizontalscrollpage/bg_reward_premium.png" if premium else "horizontalscrollpage/bg_reward_normal.png"))
		bg.AddFlag("not_pick")
		bg.Show()
		self.keep.append(bg)
		icon = ui.ExpandedImageBox()
		icon.SetParent(self)
		icon.SetPosition(34, 29)
		icon.OnMouseOverIn = ui.__mem_func__(self.__OverIn)
		icon.OnMouseOverOut = ui.__mem_func__(self.__OverOut)
		icon.Show()
		self.icon = icon
		count = ui.TextLine()
		count.SetParent(self)
		count.SetPosition(64, 52)
		count.SetHorizontalAlignRight()
		count.SetOutline()
		count.AddFlag("not_pick")
		count.Show()
		self.count = count
		self.lock = self.__Image("horizontalscrollpage/btn_locked.png")
		self.taken = self.__Image("horizontalscrollpage/artboard 5 copy.png")
		take = ui.ExpandedImageBox()
		take.SetParent(self)
		take.SetPosition(34, 87)
		take.LoadImage(NEW_BP_PATH % "horizontalscrollpage/btn_click.png")
		take.OnMouseOverIn = lambda: take.LoadImage(NEW_BP_PATH % "horizontalscrollpage/btn_click_hover.png")
		take.OnMouseOverOut = lambda: take.LoadImage(NEW_BP_PATH % "horizontalscrollpage/btn_click.png")
		take.OnMouseLeftButtonDown = lambda: take.LoadImage(NEW_BP_PATH % "horizontalscrollpage/btn_click_clicked.png")
		take.OnMouseLeftButtonUp = ui.__mem_func__(self.__OnTake)
		take.Hide()
		self.take = take
		self.keep.append(take)
		self.Show()

	def __del__(self):
		ui.Window.__del__(self)

	def __Image(self, name):
		img = ui.ExpandedImageBox()
		img.SetParent(self)
		img.SetPosition(34, 87)
		img.LoadImage(NEW_BP_PATH % name)
		img.AddFlag("not_pick")
		img.Hide()
		self.keep.append(img)
		return img

	def SetData(self, index, vnum, count):
		self.index = index
		self.vnum = vnum
		if vnum:
			item.SelectItem(vnum)
			self.icon.LoadImage(item.GetIconImageFileName())
			self.icon.Show()
			self.count.SetText(str(count) if count > 1 else "")
		else:
			self.icon.Hide()

	def SetState(self, state):
		"""0 locked, 1 claimable, 2 taken"""
		self.lock.Show() if state == 0 else self.lock.Hide()
		self.take.Show() if state == 1 else self.take.Hide()
		self.taken.Show() if state == 2 else self.taken.Hide()

	def SetTextVisible(self, flag):
		self.count.Show() if flag else self.count.Hide()

	def __OnTake(self):
		self.take.LoadImage(NEW_BP_PATH % "horizontalscrollpage/btn_click.png")
		self.owner.ClaimReward(self.premium, self.index)

	def __OverIn(self):
		self.owner.ShowItemToolTip(self.vnum)

	def __OverOut(self):
		self.owner.HideItemToolTip()


class QuestItem(ui.Window):
	def __init__(self, parent):
		ui.Window.__init__(self)
		self.listed = False
		self.SetParent(parent)
		self.SetSize(536, QUEST_H)
		self.keep = []
		self.__Img("missions page/bg_missions.png", 0, 0)
		self.icon = self.__Img("icons/kill_monsters.png", 9, 5)
		self.gauge = self.__Img("missions page/gauge_full.png", 72, 32)
		self.title = self.__Text(76, 17, TITLE_COLOR, False)
		self.desc = self.__Text(355, 17, TEXT_COLOR, False, True)
		self.reward = self.__Text(451, 17, TEXT_COLOR)
		self.reward.SetText(localeInfo.BATTLEPASS_REWARD_TITLE)
		self.exp = self.__Text(451, 37, VALUE_COLOR)
		self.progress = self.__Text(216, 38, TEXT_COLOR)
		self.done = self.__Img("missions page/done_overlay.png", 3, 3)
		self.doneText = self.__Text(268, 26, DONE_COLOR)
		self.doneText.SetText(localeInfo.BATTLEPASS_COMPLETED)
		self.locked = self.__Img("missions page/locked_mission_overlay.png", 3, 3)
		self.lockedBg = self.__Img("bg_text_overlay.png", 371, 11)
		self.lockedText = self.__Text(451, 26, HIGHLIGHT_COLOR)
		self.lockedText.SetFontName(BOLD_FONT)
		self.SetLocked(0)
		self.Show()

	def __del__(self):
		ui.Window.__del__(self)

	def __Img(self, name, x, y):
		img = ui.ExpandedImageBox()
		img.SetParent(self)
		img.LoadImage(NEW_BP_PATH % name)
		img.SetPosition(x, y)
		img.AddFlag("not_pick")
		img.Show()
		self.keep.append(img)
		return img

	def __Text(self, x, y, color, center = True, right = False):
		t = ui.TextLine()
		t.SetParent(self)
		t.SetPosition(x, y)
		if center:
			t.SetHorizontalAlignCenter()
		elif right:
			t.SetHorizontalAlignRight()
		t.SetVerticalAlignCenter()
		t.SetPackedFontColor(color)
		t.SetOutline()
		t.Show()
		self.keep.append(t)
		return t

	def SetData(self, mission, progress):
		mtype = MISSION_NAME_TO_TYPE.get(mission.get("mission", ""), 0)
		(nameKey, iconName, descKey) = QUEST_INFO.get(mtype, ("BATTLEPASS_DEFAULT_QUEST", "kill_monsters.png", "BATTLEPASS_DEFAULT_QUEST_DESC"))
		self.icon.LoadImage(NEW_BP_PATH % ("icons/" + iconName))
		name = _L(nameKey, localeInfo.BATTLEPASS_DEFAULT_QUEST)
		target = mission.get("vnum", 0)
		if target and "%s" in name:
			import nonplayer
			item.SelectItem(target)
			name = name % (item.GetItemName() or nonplayer.GetMonsterName(target))
		self.title.SetText(name)
		self.desc.SetText(_L(descKey, ""))
		count = max(1, mission.get("count", 1))
		progress = min(progress, count)
		self.exp.SetText(localeInfo.BATTLEPASS_EXP_VALUE % mission.get("exp", 0))
		self.progress.SetText("%d / %d" % (progress, count))
		self.gauge.SetPercentage(progress, count)
		finished = progress >= count
		self.done.Show() if finished else self.done.Hide()
		self.doneText.Show() if finished else self.doneText.Hide()
		return finished

	def SetLocked(self, openTime):
		"""openTime: unix time the mission week opens, 0 = open"""
		for w in (self.locked, self.lockedBg, self.lockedText):
			w.Show() if openTime else w.Hide()
		if openTime:
			import time
			self.lockedText.SetText(localeInfo.BATTLEPASS_MISSION_UNLOCK_DATE % time.strftime("%d/%m/%Y", time.localtime(openTime)))
			self.done.Hide()
			self.doneText.Hide()


class BattlePassWindow(ui.Window):
	WIDTH = 601
	HEIGHT = 405

	def __init__(self):
		self.lastTimerUpdate = 0
		ui.Window.__init__(self)
		self.interface = None
		self.toolTipItem = None
		self.keep = []
		self.config = None
		self.info = {KIND_PASS: None, KIND_EVENT: None}
		self.progress = {KIND_PASS: {}, KIND_EVENT: {}}
		self.infoTime = 0
		self.rewardScroll = 0
		self.questScroll = 0
		self.questItems = []
		self.tab = 1
		self.questionDialog = None
		self.__Build()

	def __del__(self):
		ui.Window.__del__(self)

	def Destroy(self):
		self.Hide()
		self.__CloseQuestion()
		self.keep = []
		self.questItems = []
		self.interface = None
		self.toolTipItem = None

	def BindInterface(self, interface):
		self.interface = interface

	def SetItemToolTip(self, toolTip):
		self.toolTipItem = toolTip

	def __Image(self, parent, name, x, y, path = NEW_BP_PATH):
		img = ui.ExpandedImageBox()
		img.SetParent(parent)
		img.LoadImage(path % name)
		img.SetPosition(x, y)
		img.AddFlag("not_pick")
		img.Show()
		self.keep.append(img)
		return img

	def __Text(self, parent, x, y, color = TEXT_COLOR, align = "center", vcenter = True, bold = False):
		t = ui.TextLine()
		t.SetParent(parent)
		t.SetPosition(x, y)
		if bold:
			t.SetFontName(BOLD_FONT)
		if align == "center":
			t.SetHorizontalAlignCenter()
		elif align == "right":
			t.SetHorizontalAlignRight()
		if vcenter:
			t.SetVerticalAlignCenter()
		t.SetPackedFontColor(color)
		t.SetOutline()
		t.Show()
		self.keep.append(t)
		return t

	def __Build(self):
		self.SetSize(self.WIDTH, self.HEIGHT)
		self.AddFlag("movable")
		self.AddFlag("float")

		board = ui.BoardWithTitleBar()
		board.SetParent(self)
		board.SetPosition(30, 0)
		board.SetSize(571, 405)
		board.SetTitleName(localeInfo.BATTLEPASS_TITLE)
		board.SetCloseEvent(ui.__mem_func__(self.Close))
		board.AddFlag("attach")
		board.Show()
		self.board = board

		self.tabButtons = []
		for (i, (name, y)) in enumerate((("quest", 26), ("reward", 60), ("event", 94))):
			btn = ui.RadioButton()
			btn.SetParent(self)
			btn.SetPosition(0, y)
			btn.SetUpVisual(SIDE_PATH % ("btn_%s_norm.png" % name))
			btn.SetOverVisual(SIDE_PATH % ("btn_%s_hover.png" % name))
			btn.SetDownVisual(SIDE_PATH % ("btn_%s_select.png" % name))
			btn.SetEvent(lambda t = i: self.SelectTab(t))
			btn.Show()
			self.keep.append(btn)
			self.tabButtons.append(btn)

		# shared header (38,30)
		self.__Image(self, "header/bg.png", 38, 30)
		self.__Image(self, "header/cirlce_gauge.png", 43, 34)
		self.__Text(self, 66, 43, TEXT_COLOR, "center", False).SetText(localeInfo.BATTLEPASS_LEVEL)
		self.levelValue = self.__Text(self, 66, 57, HIGHLIGHT_COLOR, "center", False, True)
		self.__Image(self, "header/xp_icon.png", 98, 41)
		self.__Text(self, 120, 50, TITLE_COLOR, "left", True, True).SetText("EXP")
		buyExp = ui.Button()
		buyExp.SetParent(self)
		buyExp.SetPosition(292, 35)
		buyExp.SetUpVisual(NEW_BP_PATH % "header/btn_buyexp.png")
		buyExp.SetOverVisual(NEW_BP_PATH % "header/btn_buyexp_hover.png")
		buyExp.SetDownVisual(NEW_BP_PATH % "header/btn_buyexp_clicked.png")
		buyExp.SetEvent(ui.__mem_func__(self.__OnClickBuy))
		buyExp.Show()
		self.keep.append(buyExp)
		self.__Text(self, 345, 42, TEXT_COLOR, "center", False).SetText(localeInfo.BATTLEPASS_BUY_EXP)
		self.expGauge = self.__Image(self, "header/gauge.png", 96, 70)
		self.expCurrent = self.__Text(self, 240, 68, HIGHLIGHT_COLOR, "right", False)
		self.__Text(self, 248, 68, HIGHLIGHT_COLOR, "center", False).SetText("/")
		self.expTotal = self.__Text(self, 256, 68, HIGHLIGHT_COLOR, "left", False)
		premium = ui.Button()
		premium.SetParent(self)
		premium.SetPosition(402, 30)
		premium.SetUpVisual(NEW_BP_PATH % "header/btn_buy.png")
		premium.SetOverVisual(NEW_BP_PATH % "header/btn_buy_hover.png")
		premium.SetDownVisual(NEW_BP_PATH % "header/btn_buy_clicked.png")
		premium.SetEvent(ui.__mem_func__(self.__OnClickBuy))
		premium.SetToolTipText(localeInfo.BATTLEPASS_BUY_PREMIUM_TOOLTIP)
		premium.Show()
		self.keep.append(premium)
		self.premiumButton = premium
		self.premiumArt = self.__Image(self, "header/btn_buy.png", 402, 30)
		self.premiumArt.Hide()
		# "Bitise kalan: |b16d 15h 43m|B" -> beige label + bold white value, centred on 497 together
		self.timeLabel = self.__Text(self, 0, 68, TEXT_COLOR, "left", False)
		self.timeValue = self.__Text(self, 0, 68, HIGHLIGHT_COLOR, "left", False, True)

		self.__Image(self, "event page/clock_bg.png", 403, 91)
		self.filter = FilterCheckBox(self, 44, 92, localeInfo.BATTLEPASS_FILTER_UNFINISHED)
		self.filter.SetEvent(ui.__mem_func__(self.__OnFilter))
		self.questLabel = self.__Text(self, 0, 93, TEXT_COLOR, "left", False)
		self.questValue = self.__Text(self, 0, 93, HIGHLIGHT_COLOR, "left", False, True)

		self.__BuildPassPage()
		self.__BuildMissionPage()
		self.__BuildEventPage()
		self.SetCenterPosition()

	def __BuildPassPage(self):
		page = ui.Window()
		page.SetParent(self)
		page.SetPosition(0, 0)
		page.SetSize(self.WIDTH, self.HEIGHT)
		page.AddFlag("not_pick")
		page.Hide()
		self.keep.append(page)
		self.passPage = page
		self.__Image(page, "horizontalscrollpage/bg.png", 38, 114)
		self.__Image(page, "horizontalscrollpage/categ1.png", 38, 114)
		self.__Text(page, 95, 127, HIGHLIGHT_COLOR, "center", True, True).SetText(localeInfo.BATTLEPASS_FREE_TITLE)
		self.__Image(page, "horizontalscrollpage/layer 5.png", 41, 148)
		self.__Image(page, "horizontalscrollpage/categ2.png", 38, 253)
		self.__Text(page, 95, 266, HIGHLIGHT_COLOR, "center", True, True).SetText(localeInfo.BATTLEPASS_PREMIUM_TITLE)
		self.__Image(page, "horizontalscrollpage/layer 6.png", 41, 284)

		clip = ui.Window()
		clip.SetParent(page)
		clip.SetPosition(LIST_X, FREE_Y)
		clip.SetSize(LIST_W, 277)
		clip.SetInsideRender(True)
		clip.OnMouseWheel = ui.__mem_func__(self.__OnRewardWheel)
		clip.OnRunMouseWheel = ui.__mem_func__(self.__OnRewardWheel)
		clip.Show()
		self.keep.append(clip)
		self.rewardClip = clip
		self.freeSlots = []
		self.premiumSlots = []
		self.levelMarks = []
		self.levelNumbers = []
		self.rewardLevel = 0
		self.bonusSlot = None

		self.__Image(page, "horizontalscrollpage/bg_gauge.png", LEVEL_X, 245)
		self.levelGauge = self.__Image(page, "horizontalscrollpage/gauge.png", LEVEL_X, 246)
		self.levelGauge.SetPercentage(0, 1)
		levelClip = ui.Window()
		levelClip.SetParent(page)
		levelClip.SetPosition(LEVEL_X, 240)
		levelClip.SetSize(LEVEL_W, 25)
		levelClip.SetInsideRender(True)
		levelClip.AddFlag("not_pick")
		levelClip.Show()
		self.keep.append(levelClip)
		self.levelClip = levelClip
		bonusClip = ui.Window()
		bonusClip.SetParent(page)
		bonusClip.SetPosition(LIST_X, FREE_Y)
		bonusClip.SetSize(LIST_W, 277)
		bonusClip.SetInsideRender(True)
		bonusClip.AddFlag("not_pick")
		bonusClip.Show()
		self.keep.append(bonusClip)
		self.bonusClip = bonusClip

		track = ui.Bar()
		track.SetParent(page)
		track.SetPosition(LIST_X + 1, 392)
		track.SetSize(LEVEL_W, 1)
		track.SetColor(0xff3a332b)
		track.AddFlag("not_pick")
		track.Show()
		self.keep.append(track)
		area = ui.Window()
		area.SetParent(page)
		area.SetPosition(LIST_X + 1, 389)
		area.SetSize(LEVEL_W, 10)
		area.OnMouseLeftButtonDown = ui.__mem_func__(self.__OnScrollDown)
		area.OnMouseLeftButtonUp = ui.__mem_func__(self.__OnScrollUp)
		area.Show()
		self.keep.append(area)
		self.scrollArea = area
		self.scrollDrag = None
		self.scrollBar = ui.Bar()
		self.scrollBar.SetParent(page)
		self.scrollBar.SetPosition(LIST_X + 1, 393)
		self.scrollBar.SetSize(SCROLL_BAR_W, 3)
		self.scrollBar.SetColor(0xff8a7a62)
		self.scrollBar.AddFlag("not_pick")
		self.scrollBar.Show()
		self.keep.append(self.scrollBar)

	def __BuildRewardSlots(self, count):
		for w in self.freeSlots + self.premiumSlots + self.levelMarks:
			w.Hide()
		self.freeSlots = []
		self.premiumSlots = []
		self.levelMarks = []
		self.levelNumbers = []
		for i in xrange(count):
			self.freeSlots.append(RewardSlot(self.rewardClip, False, self))
			self.premiumSlots.append(RewardSlot(self.rewardClip, True, self))
		if not self.bonusSlot:
			self.bonusSlot = BonusSlot(self.bonusClip, self.passPage, self)
		for i in xrange(count):
			mark = ui.ExpandedImageBox()
			mark.SetParent(self.levelClip)
			mark.LoadImage(NEW_BP_PATH % "horizontalscrollpage/paginationbg.png")
			mark.AddFlag("not_pick")
			mark.Show()
			num = ui.TextLine()
			num.SetParent(mark)
			num.SetPosition(12, 12)
			num.SetHorizontalAlignCenter()
			num.SetVerticalAlignCenter()
			num.SetPackedFontColor(HIGHLIGHT_COLOR)
			num.SetOutline()
			num.SetText(str(i + 1))
			num.Show()
			self.keep.append(num)
			self.levelNumbers.append(num)
			self.levelMarks.append(mark)
		self.__PlaceRewards()

	def __PlaceRewards(self):
		for (i, slot) in enumerate(self.freeSlots):
			x = i * REWARD_W - self.rewardScroll
			slot.SetPosition(x, 0)
			self.premiumSlots[i].SetPosition(x, PREMIUM_Y - FREE_Y)
			inside = x >= 0 and x + 70 <= LIST_W
			slot.SetTextVisible(inside)
			self.premiumSlots[i].SetTextVisible(inside)
			mx = x + REWARD_W - 13 - (LEVEL_X - LIST_X)
			self.levelMarks[i].SetPosition(mx, 0)
			markInside = mx >= 0 and mx + 25 <= LEVEL_W
			self.levelNumbers[i].Show() if markInside else self.levelNumbers[i].Hide()
		if self.bonusSlot:
			bx = len(self.freeSlots) * REWARD_W + BONUS_GAP - self.rewardScroll
			self.bonusSlot.Place(bx, 73, LIST_X, FREE_Y)
			self.bonusSlot.SetTextVisible(bx >= 0 and bx + REWARD_W <= LIST_W)
		filled = self.rewardLevel * REWARD_W - 1 - self.rewardScroll - (LEVEL_X - LIST_X)
		self.levelGauge.SetPercentage(max(0, min(LEVEL_W, filled)), LEVEL_W)
		total = max(1, self.__RewardScrollMax())
		self.scrollBar.SetPosition(LIST_X + 1 + int((LEVEL_W - SCROLL_BAR_W) * float(self.rewardScroll) / total), 393)

	def __RewardScrollMax(self):
		return max(0, len(self.freeSlots) * REWARD_W + BONUS_GAP + REWARD_W - LIST_W)

	def __OnRewardWheel(self, delta):
		self.rewardScroll = max(0, min(self.__RewardScrollMax(), self.rewardScroll - (REWARD_W if delta > 0 else -REWARD_W)))
		self.__PlaceRewards()
		return True

	def OnRunMouseWheel(self, delta):
		if self.tab == 1:
			return self.__OnRewardWheel(delta)
		if self.tab == 0:
			return self.__OnQuestWheel(delta)
		return False

	def OnMouseWheel(self, delta):
		return self.OnRunMouseWheel(delta)

	def __OnScrollDown(self):
		(mx, _) = self.scrollArea.GetMouseLocalPosition()
		barX = self.scrollBar.GetLocalPosition()[0] - (LIST_X + 1)
		self.scrollDrag = mx - barX if barX <= mx < barX + SCROLL_BAR_W else SCROLL_BAR_W / 2
		self.__DragScroll()

	def __OnScrollUp(self):
		self.scrollDrag = None

	def __DragScroll(self):
		(mx, _) = self.scrollArea.GetMouseLocalPosition()
		pos = max(0, min(LEVEL_W - SCROLL_BAR_W, mx - self.scrollDrag))
		self.rewardScroll = int(self.__RewardScrollMax() * float(pos) / (LEVEL_W - SCROLL_BAR_W))
		self.__PlaceRewards()


	def __BuildMissionPage(self):
		page = ui.Window()
		page.SetParent(self)
		page.SetPosition(0, 0)
		page.SetSize(self.WIDTH, self.HEIGHT)
		page.AddFlag("not_pick")
		page.Hide()
		self.keep.append(page)
		self.missionPage = page
		self.__Image(page, "missions page/bg.png", 38, 114)
		clip = ui.Window()
		clip.SetParent(page)
		clip.SetPosition(QUEST_X, QUEST_Y)
		clip.SetSize(536, QUEST_VIEW_H)
		clip.SetInsideRender(True)
		clip.OnMouseWheel = ui.__mem_func__(self.__OnQuestWheel)
		clip.OnRunMouseWheel = ui.__mem_func__(self.__OnQuestWheel)
		clip.Show()
		self.keep.append(clip)
		self.questClip = clip
		self.__Image(page, "missions page/bg_scroll.png", 580, 119)
		self.questBar = ui.Bar()
		self.questBar.SetParent(page)
		self.questBar.SetPosition(582, 121)
		self.questBar.SetSize(4, 60)
		self.questBar.SetColor(0xff8a7a62)
		self.questBar.Show()
		self.keep.append(self.questBar)

	def __ListedQuests(self):
		return [q for q in self.questItems if q.listed]

	def __OnQuestWheel(self, delta):
		maxRow = max(0, len(self.__ListedQuests()) - QUEST_ROWS)
		self.questScroll = max(0, min(maxRow, self.questScroll + (-1 if delta > 0 else 1)))
		self.__PlaceQuests()
		return True

	def __PlaceQuests(self):
		listed = self.__ListedQuests()
		self.questScroll = max(0, min(self.questScroll, len(listed) - QUEST_ROWS))
		for q in self.questItems:
			if not q.listed:
				q.Hide()
		for (i, q) in enumerate(listed):
			row = i - self.questScroll
			if 0 <= row < QUEST_ROWS:
				q.SetPosition(0, row * (QUEST_H + QUEST_GAP))
				q.Show()
			else:
				q.Hide()
		if len(listed) <= QUEST_ROWS:
			self.questBar.Hide()
			return
		self.questBar.Show()
		h = max(20, int(268.0 * QUEST_ROWS / len(listed)))
		self.questBar.SetSize(4, h)
		self.questBar.SetPosition(582, 121 + int((268 - h) * float(self.questScroll) / (len(listed) - QUEST_ROWS)))

	def __BuildEventPage(self):
		page = ui.Window()
		page.SetParent(self)
		page.SetPosition(0, 0)
		page.SetSize(self.WIDTH, self.HEIGHT)
		page.AddFlag("not_pick")
		page.Hide()
		self.keep.append(page)
		self.eventPage = page
		self.__Image(page, "event page/bg.png", 38, 114)
		self.eventText = self.__Text(page, 315, 250, TEXT_COLOR)

	# ------------------------------------------------------------------ data
	def __Season(self, kind):
		info = self.info.get(kind)
		if not info or not info["season"]:
			return None
		if self.config is None:
			self.config = LoadConfig()
		key = "event_battlepasses" if kind == KIND_EVENT else "default_battlepasses"
		for s in self.config.get(key, []):
			if s.get("season_id") == info["season"]:
				return s
		return None

	def __ServerNow(self):
		info = self.info.get(KIND_PASS) or self.info.get(KIND_EVENT)
		if not info or not info["season"]:
			return 0
		return info["serverTime"] + int(app.GetTime() - self.infoTime)

	def SetInfo(self, data):
		try:
			v = [int(x) for x in data.split(",")]
		except ValueError:
			return
		kind = v[0]
		if len(v) < 11 or not v[1]:
			self.info[kind] = None
		else:
			self.info[kind] = {"season": v[1], "level": v[2], "exp": v[3], "levelExp": max(1, v[4]), "premium": v[5],
				"claimedFree": v[6], "claimedPremium": v[7], "endTime": v[8], "serverTime": v[9], "maxLevel": v[10]}
			self.infoTime = app.GetTime()
		self.Refresh()

	def SetMissions(self, data):
		(kind, chunk, rest) = (data.split(",", 2) + ["", "", ""])[:3]
		try:
			kind = int(kind)
			chunk = int(chunk)
		except ValueError:
			return
		if chunk == 0:
			self.progress[kind] = {}
		for part in rest.split(";"):
			if ":" not in part:
				continue
			(mid, value) = part.split(":", 1)
			try:
				self.progress[kind][int(mid)] = int(value)
			except ValueError:
				pass
		self.Refresh()

	def SetMission(self, data):
		try:
			(kind, mid, value) = [int(x) for x in data.split(",")]
		except ValueError:
			return
		self.progress.setdefault(kind, {})[mid] = value
		if self.IsShow():
			self.__RefreshMissions()

	def OnResult(self, data):
		try:
			(code, value) = [int(x) for x in data.split(",")]
		except ValueError:
			return
		texts = {
			RESULT_NO_SEASON: "BATTLEPASS_RESULT_NO_SEASON", RESULT_LOCKED: "BATTLEPASS_RESULT_LOCKED",
			RESULT_NO_PREMIUM: "BATTLEPASS_RESULT_NO_PREMIUM", RESULT_CLAIMED: "BATTLEPASS_RESULT_CLAIMED",
			RESULT_REWARD: "BATTLEPASS_RESULT_REWARD", RESULT_PREMIUM_ON: "BATTLEPASS_RESULT_PREMIUM_ON",
			RESULT_PREMIUM_HAD: "BATTLEPASS_RESULT_PREMIUM_HAD", RESULT_EXP: "BATTLEPASS_RESULT_EXP",
			RESULT_LEVEL_UP: "BATTLEPASS_RESULT_LEVEL_UP", RESULT_MISSION_DONE: "BATTLEPASS_RESULT_MISSION_DONE",
			RESULT_INVENTORY: "BATTLEPASS_RESULT_INVENTORY",
		}
		text = _L(texts.get(code, ""), "")
		if not text:
			return
		try:
			text = text % value
		except TypeError:
			pass
		if code in (RESULT_LOCKED, RESULT_NO_PREMIUM, RESULT_CLAIMED, RESULT_INVENTORY, RESULT_NO_SEASON, RESULT_PREMIUM_HAD):
			self.notice = ui.NoticeBoxBoard(text)
		else:
			chat.AppendChat(chat.CHAT_TYPE_INFO, text)

	# ------------------------------------------------------------------ refresh
	def Refresh(self):
		self.tabButtons[2].Show() if self.info.get(KIND_EVENT) else self.tabButtons[2].Hide()
		if not self.IsShow():
			return
		kind = KIND_EVENT if self.tab == 2 else KIND_PASS
		info = self.info.get(kind)
		if not info:
			self.levelValue.SetText("0")
			self.expCurrent.SetText("0")
			self.expTotal.SetText("0")
			self.expGauge.SetPercentage(0, 1)
			self.__SetPair(self.timeLabel, self.timeValue, "", "", 497, "center")
			self.__SetPair(self.questLabel, self.questValue, "", "", 586, "right")
			return
		self.levelValue.SetText(str(info["level"]))
		self.expCurrent.SetText(str(info["exp"]))
		self.expTotal.SetText(str(info["levelExp"]))
		self.expGauge.SetPercentage(info["exp"], info["levelExp"])
		self.premiumButton.Show() if not info["premium"] else self.premiumButton.Hide()
		self.premiumArt.Show() if info["premium"] else self.premiumArt.Hide()
		self.__RefreshTimers()
		self.__RefreshRewards()
		self.__RefreshMissions()

	def __RefreshTimers(self):
		kind = KIND_EVENT if self.tab == 2 else KIND_PASS
		info = self.info.get(kind)
		if not info:
			return
		now = self.__ServerNow()
		self.__SetPair(self.timeLabel, self.timeValue, localeInfo.BATTLEPASS_HEADER_TIME_LEFT, _TimeText(info["endTime"] - now), 497, "center")
		season = self.__Season(kind)
		nextDate = None
		if season:
			for day in sorted(season.get("quest_schedule", {}).keys()):
				if _StampToSeconds(_Stamp(day)) > now:
					nextDate = day
					break
		if nextDate:
			self.__SetPair(self.questLabel, self.questValue, localeInfo.BATTLEPASS_NEW_QUEST_TIME, _TimeText(_StampToSeconds(_Stamp(nextDate)) - now), 586, "right")
		else:
			self.__SetPair(self.questLabel, self.questValue, localeInfo.BATTLEPASS_ALL_QUESTS_AVAILABLE, "", 586, "right")

	def __SetPair(self, labelLine, valueLine, fmt, value, x, align):
		(head, _, tail) = fmt.partition("%s")
		labelLine.SetText(head)
		valueLine.SetText(value + tail)
		labelW = labelLine.GetTextSize()[0] if head else 0
		valueW = valueLine.GetTextSize()[0] if (value or tail) else 0
		left = x - (labelW + valueW) / 2 if align == "center" else x - labelW - valueW
		labelLine.SetPosition(left, labelLine.GetLocalPosition()[1])
		valueLine.SetPosition(left + labelW, valueLine.GetLocalPosition()[1])

	def __RefreshRewards(self):
		kind = KIND_EVENT if self.tab == 2 else KIND_PASS
		info = self.info.get(kind)
		season = self.__Season(kind)
		if not info or not season:
			return
		self.rewardLevel = info["level"]
		rewards = season.get("rewards", {})
		count = len(rewards)
		if len(self.freeSlots) != count:
			self.__BuildRewardSlots(count)
		for i in xrange(count):
			r = rewards.get(str(i), {})
			free = r.get("free", {})
			prem = r.get("premium", {})
			self.freeSlots[i].SetData(i, free.get("vnum", 0), free.get("count", 0))
			self.premiumSlots[i].SetData(i, prem.get("vnum", 0), prem.get("count", 0))
			unlocked = info["level"] > i
			self.freeSlots[i].SetState(2 if info["claimedFree"] & (1 << i) else (1 if unlocked else 0))
			if info["claimedPremium"] & (1 << i):
				self.premiumSlots[i].SetState(2)
			else:
				self.premiumSlots[i].SetState(1 if unlocked and info["premium"] else 0)
		if self.bonusSlot:
			bonus = season.get("max_level_bonus_reward", {})
			self.bonusSlot.SetData(bonus.get("vnum", 0), bonus.get("count", 1), count, info["levelExp"])
		self.__PlaceRewards()

	def __RefreshMissions(self):
		kind = KIND_EVENT if self.tab == 2 else KIND_PASS
		season = self.__Season(kind)
		if not season:
			for q in self.questItems:
				q.listed = False
				q.Hide()
			return
		now = self.__ServerNow()
		missions = []
		for day in sorted(season.get("quest_schedule", {}).keys()):
			openTime = _StampToSeconds(_Stamp(day))
			for m in season["quest_schedule"][day].get("missions", []):
				missions.append((m, openTime if openTime > now else 0))
		while len(self.questItems) < len(missions):
			self.questItems.append(QuestItem(self.questClip))
		onlyOpen = self.filter.GetCheckStatus()
		progress = self.progress.get(kind, {})
		for (i, q) in enumerate(self.questItems):
			if i >= len(missions):
				q.listed = False
				continue
			(m, openTime) = missions[i]
			finished = q.SetData(m, 0 if openTime else progress.get(m.get("mission_id", 0), 0))
			q.SetLocked(openTime)
			q.listed = not (onlyOpen and finished)
		self.__PlaceQuests()

	# ------------------------------------------------------------------ actions
	def SelectTab(self, tab):
		self.tab = tab
		for (i, b) in enumerate(self.tabButtons):
			b.Down() if i == tab else b.SetUp()
		self.missionPage.Show() if tab == 0 else self.missionPage.Hide()
		self.passPage.Show() if tab == 1 else self.passPage.Hide()
		self.eventPage.Show() if tab == 2 else self.eventPage.Hide()
		self.Refresh()

	def __OnFilter(self, *args):
		self.questScroll = 0
		self.__RefreshMissions()

	def ClaimReward(self, premium, index):
		kind = KIND_EVENT if self.tab == 2 else KIND_PASS
		info = self.info.get(kind)
		if not info:
			return
		earlier = False
		for i in xrange(index):
			if i < info["level"] and not (info["claimedFree"] & (1 << i)):
				earlier = True
			if i < info["level"] and info["premium"] and not (info["claimedPremium"] & (1 << i)):
				earlier = True
		if earlier:
			self.__CloseQuestion()
			dlg = uiCommon.QuestionDialog()
			dlg.SetText(localeInfo.BATTLEPASS_CLAIM_PREVIOUS_CONFIRM)
			dlg.SetAcceptEvent(lambda: (self.__CloseQuestion(), net.SendChatPacket("/bp claim_all %d" % kind)))
			dlg.SetCancelEvent(lambda: (self.__CloseQuestion(), net.SendChatPacket("/bp claim %d %d %d" % (kind, 1 if premium else 0, index))))
			dlg.Open()
			self.questionDialog = dlg
			return
		net.SendChatPacket("/bp claim %d %d %d" % (kind, 1 if premium else 0, index))

	def __CloseQuestion(self):
		if self.questionDialog:
			self.questionDialog.Close()
			self.questionDialog = None

	def __OnClickBuy(self):
		if self.interface and app.ENABLE_ITEMSHOP:
			self.interface.OpenItemShopWindow()

	def ShowItemToolTip(self, vnum):
		if vnum and self.toolTipItem:
			self.toolTipItem.descUtf8Limit = 35
			try:
				self.toolTipItem.SetItemToolTip(vnum, 220)
			finally:
				self.toolTipItem.descUtf8Limit = 0

	def HideItemToolTip(self):
		if self.toolTipItem:
			self.toolTipItem.HideToolTip()

	def OnUpdate(self):
		if self.scrollDrag is not None:
			self.__DragScroll()
		if app.GetTime() - self.lastTimerUpdate >= 1.0:
			self.lastTimerUpdate = app.GetTime()
			self.__RefreshTimers()

	# ------------------------------------------------------------------ open / close
	def Open(self):
		net.SendChatPacket("/bp info")
		self.Show()
		self.SetTop()
		self.SelectTab(self.tab)

	def Toggle(self):
		if self.IsShow():
			self.Close()
		else:
			self.Open()

	def Close(self):
		self.scrollDrag = None
		self.__CloseQuestion()
		self.HideItemToolTip()
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True
