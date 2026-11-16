#
# File Name : uibiologist.py
# Author    : BestStudio
# Version   : 1.0
# Date      : 2026-11-14
#

import app
import net
import player
import item
import chat
import ui
import uiToolTip
import localeInfo

BIOLOGIST_PATH = "d:/ymir work/ui/game/biology/new/%s"
PITY_PATH = "d:/ymir work/ui/game/refine2/%s"

LABEL_COLOR = 0xffcabdab
COUNT_COLOR = 0xffb1a085
TITLE_COLOR = 0xffd1b183
REWARD_COLOR = 0xffa0be8e

MISSIONS = (
	None,
	(30, 61000, 10, 0, 30220, 60050, 60051, ((item.APPLY_ATT_SPEED, 10),)),
	(40, 61001, 15, 300, 30221, 60050, 60051, ((item.APPLY_MOV_SPEED, 10), (item.APPLY_ATTBONUS_STONE, 5))),
	(50, 61002, 15, 600, 30222, 60050, 60051, ((item.APPLY_DEF_GRADE_BONUS, 60), (item.APPLY_CRITICAL_PCT, 5))),
	(60, 61003, 20, 900, 30223, 60052, 60053, ((item.APPLY_ATT_GRADE_BONUS, 50),)),
	(70, 61004, 25, 1200, 30224, 60052, 60053, ((item.APPLY_MALL_DEFBONUS, 10), (item.APPLY_ATTBONUS_STONE, 10))),
	(80, 61005, 30, 1800, 30225, 60052, 60053, ((item.APPLY_MALL_ATTBONUS, 10),)),
	(85, 61006, 40, 2700, 30226, 60052, 60053, ((item.APPLY_BLOCK, 10), (item.APPLY_ATTBONUS_STONE, 5))),
	(90, 61007, 50, 3600, 30227, 60054, 60055, ((item.APPLY_ATTBONUS_HUMAN, 8), (item.APPLY_ATTBONUS_MONSTER, 5))),
	(92, 61008, 25, 7200, 30228, 60054, 60055, ((item.APPLY_ATTBONUS_DRAGON, 20), (item.APPLY_ATTBONUS_DRAGON, 20))),
	(94, 61009, 30, 9000, 30229, 60054, 60055, ((item.APPLY_ATTBONUS_BOSS, 5), (item.APPLY_CRITICAL_PCT, 5))),
	(100, 61010, 40, 10800, 30230, 60054, 60055, ((item.APPLY_ATT_GRADE_BONUS, 100), (item.APPLY_PENETRATE_PCT, 5), (item.APPLY_ATTBONUS_MONSTER, 5))),
	(105, 61011, 40, 14400, 30231, 60056, 60057, ((item.APPLY_ATTBONUS_BOSS, 20), (item.APPLY_ITEM_DROP_BONUS, 10))),
	(108, 61012, 45, 16200, 30232, 60056, 60057, ((item.APPLY_ATTBONUS_DRAGON, 20), (item.APPLY_ATTBONUS_ELEMENTS, 5))),
	(110, 61013, 50, 18000, 30233, 60056, 60057, ((item.APPLY_NORMAL_HIT_DAMAGE_BONUS, 5), (item.APPLY_ATTBONUS_STONE, 5))),
)
MISSION_COUNT = len(MISSIONS) - 1
SUCCESS_BOOSTS = (60051, 60053, 60055, 60057)
SUCCESS_BOOST_PERCENT = 50			# biolog_renewal.cpp BIOLOG_SUCCESS_BOOST
TOOLTIP_WIDTH = 310
DESC_LIMIT_BYTES = 35


def _Utf8Len(text):
	return len(text) + sum(1 for c in text if ord(c) >= 0x80)

# BiologResult codes (biolog_renewal.cpp EBiologResult)
(RESULT_NO_MISSION, RESULT_DONE, RESULT_WAIT, RESULT_NO_ITEM, RESULT_NO_STONE, RESULT_SUCCESS, RESULT_FAIL,
	RESULT_STONE_PHASE, RESULT_COMPLETE, RESULT_BUSY, RESULT_TIME_USED) = range(11)


class BiologistWindow(ui.BoardWithTitleBar):
	WIDTH = 365
	HEIGHT = 316

	def __init__(self):
		ui.BoardWithTitleBar.__init__(self)
		self.interface = None
		self.keep = []
		self.info = None			# dict from BiologInfo
		self.infoTime = 0
		self.notifyPending = False
		self.lastButtonText = ""
		self.toolTipItem = None
		self.toolTip = uiToolTip.ToolTip()
		self.toolTip.HideToolTip()
		self.__Build()
		self.ticker = ui.Window()
		self.ticker.SetSize(0, 0)
		self.ticker.AddFlag("not_pick")
		self.ticker.OnUpdate = ui.__mem_func__(self.CheckTime)
		self.ticker.Show()

	def __del__(self):
		ui.BoardWithTitleBar.__del__(self)

	def Destroy(self):
		self.Hide()
		if self.ticker:
			self.ticker.Hide()
			self.ticker = None
		self.keep = []
		self.toolTipItem = None
		self.toolTip = None
		self.interface = None

	def BindInterface(self, interface):
		self.interface = interface

	def SetItemToolTip(self, toolTip):
		self.toolTipItem = toolTip

	def __Image(self, name, x, y, parent = None, path = BIOLOGIST_PATH):
		img = ui.ExpandedImageBox()
		img.SetParent(parent or self)
		img.LoadImage(path % name)
		img.SetPosition(x, y)
		img.AddFlag("not_pick")
		img.Show()
		self.keep.append(img)
		return img

	def __Text(self, x, y, color = LABEL_COLOR, center = True, vcenter = False):
		t = ui.TextLine()
		t.SetParent(self)
		t.SetPosition(x, y)
		if center:
			t.SetHorizontalAlignCenter()
		if vcenter:
			t.SetVerticalAlignCenter()
		t.SetPackedFontColor(color)
		t.Show()
		self.keep.append(t)
		return t

	def __Number(self, x, y):
		n = ui.NumberLine()
		n.SetParent(self)
		n.SetPosition(x, y)
		n.SetHorizontalAlignRight()
		n.Show()
		self.keep.append(n)
		return n

	def __Icon(self, x, y, getter):
		icon = ui.ExpandedImageBox()
		icon.SetParent(self)
		icon.SetPosition(x, y)
		icon.SetStringEvent("MOUSE_OVER_IN", lambda g = getter: self.__OverInItem(g()))
		icon.SetStringEvent("MOUSE_OVER_OUT", ui.__mem_func__(self.__OverOutItem))
		icon.Show()
		self.keep.append(icon)
		return icon

	def __Build(self):
		self.SetSize(self.WIDTH, self.HEIGHT)
		self.SetTitleName(localeInfo.BIOLOG_TITLE)
		self.SetCloseEvent(ui.__mem_func__(self.Close))
		self.AddFlag("movable")
		self.AddFlag("float")
		self.SetCenterPosition()

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

		self.__Image("background.png", 6, 28)
		self.__Image("bg_title.png", 16, 40)
		self.__Image("biolo_pnj.png", 12, 35)
		self.missionName = self.__Text(189, 48)

		self.__Image("bg_quest.png", 7, 80)
		self.__Image("biolo_slot.png", 16, 86)
		self.iconMission = self.__Icon(17, 87, self.__CurrentNeedVnum)
		self.countMission = self.__Number(47, 110)
		self.__Image("gauge_empty.png", 57, 91)
		self.gauge = self.__Image("gauge_full.png", 59, 93)
		self.missionCount = self.__Text(143, 103, COUNT_COLOR, True, True)

		self.checkTime = ui.CheckBox()
		self.checkTime.SetParent(self)
		self.checkTime.SetPosition(242, 95)
		self.checkTime.Show()
		self.iconTime = self.__Icon(259, 85, lambda: self.__Mission() and self.__Mission()[5])
		self.countTime = self.__Number(289, 108)

		self.checkSuccess = ui.CheckBox()
		self.checkSuccess.SetParent(self)
		self.checkSuccess.SetPosition(299, 95)
		self.checkSuccess.Show()
		self.iconSuccess = self.__Icon(319, 85, lambda: self.__Mission() and self.__Mission()[6])
		self.countSuccess = self.__Number(349, 108)

		give = ui.Button()
		give.SetParent(self)
		give.SetPosition(12, 140)
		give.SetUpVisual(BIOLOGIST_PATH % "btn_submit_norm.png")
		give.SetOverVisual(BIOLOGIST_PATH % "btn_submit_hover.png")
		give.SetDownVisual(BIOLOGIST_PATH % "btn_submit_select.png")
		give.SetText(localeInfo.BIOLOG_GIVE)
		give.SetTextColor(LABEL_COLOR)
		give.SetEvent(ui.__mem_func__(self.__OnClickGive))
		give.Show()
		self.keep.append(give)
		self.giveButton = give

		self.clock = self.__Image("clock.png", 41, 142)
		self.clock.Hide()
		self.checkCall = ui.CheckBox()
		self.checkCall.SetParent(self)
		self.checkCall.SetPosition(62, 144)
		self.checkCall.SetCheckStatus(True)
		self.checkCall.Hide()

		shop = ui.Button()
		shop.SetParent(self)
		shop.SetPosition(316, 134)
		shop.SetUpVisual(BIOLOGIST_PATH % "btn_shop_norm.png")
		shop.SetOverVisual(BIOLOGIST_PATH % "btn_shop_hover.png")
		shop.SetDownVisual(BIOLOGIST_PATH % "btn_shop_select.png")
		shop.SetEvent(ui.__mem_func__(self.__OnClickShop))
		shop.Show()
		self.keep.append(shop)

		self.pityName = self.__Text(268, 137)
		self.pityName.SetText(localeInfo.BIOLOG_BLESSING)
		self.pityIcons = []
		for i in xrange(3):
			x = 229 + 27 * i
			self.__Image("pitty_empty.png", x, 154, None, PITY_PATH)
			full = self.__Image("pitty_full.png", x + 2, 156, None, PITY_PATH)
			full.Hide()
			self.pityIcons.append(full)

		self.__Image("background_reward.png", 12, 175)
		self.__Image("bg_title_reward.png", 15, 178)
		self.giftTitle = self.__Text(181, 187, TITLE_COLOR)
		self.giftTitle.SetText(localeInfo.BIOLOG_REWARDS)
		self.giftTexts = []
		for i in xrange(3):
			self.__Image("bg_bonus.png", 17, 213 + 29 * i)
			self.giftTexts.append(self.__Text(181, 218 + 29 * i, REWARD_COLOR))
		self.successEffect = self.__ResultEffect("effect_success")
		self.failedEffect = self.__ResultEffect("effect_failed")
		self.effectEnd = 0.0
		self.__Refresh()

	def __ResultEffect(self, name):
		ani = ui.AniImageBox()
		ani.SetParent(self)
		for i in xrange(1, 10):
			ani.AppendImage("d:/ymir work/ui/game/common/animation/%s/%d.png" % (name, i))
		ani.SetDelay(6)
		ani.SetPosition((self.WIDTH - 132) / 2, (self.HEIGHT - 38) / 2)
		ani.AddFlag("not_pick")
		ani.Hide()
		self.keep.append(ani)
		return ani

	def __ShowResultEffect(self, success):
		self.successEffect.Hide()
		self.failedEffect.Hide()
		effect = self.successEffect if success else self.failedEffect
		effect.ResetFrame()
		effect.Show()
		effect.SetTop()
		self.effectEnd = app.GetTime() + 1.0

	# ------------------------------------------------------------------ data
	def __Mission(self):
		if not self.info:
			return None
		m = self.info["mission"]
		if m < 1 or m > MISSION_COUNT:
			return None
		return MISSIONS[m]

	def __CurrentNeedVnum(self):
		mission = self.__Mission()
		if not mission:
			return 0
		return mission[4] if self.info["stone"] else mission[1]

	def __Left(self):
		if not self.info:
			return 0
		return max(0, int(self.info["left"] - (app.GetTime() - self.infoTime)))

	def SetInfo(self, data):
		try:
			v = [int(x) for x in data.split(",")]
		except ValueError:
			return
		if len(v) < 6:
			return
		self.info = {"mission": v[0], "count": v[1], "left": v[2], "stone": v[3], "pity": v[4], "pityMax": v[5]}
		self.infoTime = app.GetTime()
		self.notifyPending = v[2] > 0
		self.__Refresh()

	def __Refresh(self):
		mission = self.__Mission()
		for t in self.giftTexts:
			t.SetText("")
		if not mission:
			done = self.info and self.info["mission"] > MISSION_COUNT
			self.missionName.SetText(localeInfo.BIOLOG_ALL_DONE if done else "")
			self.iconMission.Hide()
			self.iconTime.Hide()
			self.iconSuccess.Hide()
			self.missionCount.SetText("")
			self.gauge.SetPercentage(0, 1)
			for p in self.pityIcons:
				p.Hide()
			return

		(level, vnum, count, waitTime, stone, boostTime, boostSuccess, rewards) = mission
		need = stone if self.info["stone"] else vnum
		item.SelectItem(need)
		self.missionName.SetText(localeInfo.BIOLOG_CURRENT_MISSION % (level, item.GetItemName()))
		self.iconMission.LoadImage(item.GetIconImageFileName())
		self.iconMission.Show()
		self.countMission.SetNumber(str(player.GetItemCountByVnum(need)))

		if self.info["stone"]:
			self.missionCount.SetText("0/1")
			self.gauge.SetPercentage(0, 1)
		else:
			self.missionCount.SetText("%d/%d" % (self.info["count"], count))
			self.gauge.SetPercentage(self.info["count"], count)

		item.SelectItem(boostTime)
		self.iconTime.LoadImage(item.GetIconImageFileName())
		self.iconTime.Show()
		self.countTime.SetNumber(str(player.GetItemCountByVnum(boostTime)))
		item.SelectItem(boostSuccess)
		self.iconSuccess.LoadImage(item.GetIconImageFileName())
		self.iconSuccess.Show()
		self.countSuccess.SetNumber(str(player.GetItemCountByVnum(boostSuccess)))

		for i in xrange(3):
			self.pityIcons[i].Show() if i < self.info["pity"] else self.pityIcons[i].Hide()

		import uiToolTip as _tt
		shown = 0
		for (apply, value) in rewards:
			if not apply or shown >= len(self.giftTexts):
				continue
			try:
				text = _tt.ItemToolTip.AFFECT_DICT[apply](value)
			except Exception:
				continue
			self.giftTexts[shown].SetText(text)
			shown += 1
		self.__RefreshButton()

	def __RefreshButton(self):
		left = self.__Left() if self.info and not self.info["stone"] else 0
		if left > 0:
			text = "%02d:%02d:%02d" % (left / 3600, (left % 3600) / 60, left % 60)
			self.clock.Show()
			self.checkCall.Show()
		else:
			text = localeInfo.BIOLOG_GIVE
			self.clock.Hide()
			self.checkCall.Hide()
		if text != self.lastButtonText:
			self.giveButton.SetText(text)
			self.lastButtonText = text

	def RefreshItemCount(self):
		if self.IsShow():
			self.__Refresh()

	def OnUpdate(self):
		if self.effectEnd and app.GetTime() > self.effectEnd:
			self.effectEnd = 0.0
			self.successEffect.Hide()
			self.failedEffect.Hide()
		if not self.info:
			return
		self.__RefreshButton()

	def CheckTime(self):
		if not self.info:
			return
		if self.notifyPending and self.__Left() <= 0:
			self.notifyPending = False
			if self.checkCall.GetCheckStatus() and self.interface and app.ENABLE_WHISPER_MESSENGER:
				self.interface.RecvWhisperMessenger(localeInfo.BIOLOG_SENDER, localeInfo.BIOLOG_SENDER + " : " + localeInfo.BIOLOG_READY)

	# ------------------------------------------------------------------ actions
	def __OnClickGive(self):
		net.SendChatPacket("/biolog give %d %d" % (1 if self.checkTime.GetCheckStatus() else 0, 1 if self.checkSuccess.GetCheckStatus() else 0))

	def __OnClickShop(self):
		net.SendChatPacket("/biolog shop")

	def __OnClickWiki(self):
		if self.interface and app.ENABLE_WIKI_SYSTEM:
			self.interface.OpenWikiWindow()

	def OnResult(self, code, value):
		texts = {
			RESULT_NO_MISSION: localeInfo.BIOLOG_RESULT_LEVEL, RESULT_DONE: localeInfo.BIOLOG_ALL_DONE, RESULT_WAIT: localeInfo.BIOLOG_RESULT_WAIT,
			RESULT_NO_ITEM: localeInfo.BIOLOG_RESULT_NO_ITEM, RESULT_NO_STONE: localeInfo.BIOLOG_RESULT_NO_STONE, RESULT_SUCCESS: localeInfo.BIOLOG_RESULT_SUCCESS,
			RESULT_FAIL: localeInfo.BIOLOG_RESULT_FAIL, RESULT_STONE_PHASE: localeInfo.BIOLOG_RESULT_STONE, RESULT_COMPLETE: localeInfo.BIOLOG_RESULT_COMPLETE,
			RESULT_BUSY: localeInfo.BIOLOG_RESULT_BUSY, RESULT_TIME_USED: localeInfo.BIOLOG_RESULT_TIME_USED,
		}
		if code in (RESULT_SUCCESS, RESULT_STONE_PHASE, RESULT_COMPLETE):
			self.__ShowResultEffect(True)
		elif code == RESULT_FAIL:
			self.__ShowResultEffect(False)
		text = texts.get(code)
		if not text:
			return
		if code in (RESULT_NO_ITEM, RESULT_NO_STONE):
			item.SelectItem(value)
			text = text % item.GetItemName()
		elif code == RESULT_NO_MISSION:
			text = text % value
		elif code == RESULT_WAIT:
			text = text % (value / 3600, (value % 3600) / 60, value % 60)
		if code in (RESULT_SUCCESS, RESULT_STONE_PHASE, RESULT_COMPLETE, RESULT_TIME_USED):
			chat.AppendChat(chat.CHAT_TYPE_INFO, text)
		else:
			self.notice = ui.NoticeBoxBoard(text)

	# ------------------------------------------------------------------ tooltips
	@staticmethod
	def WrapDescription(text, limit = DESC_LIMIT_BYTES):
		lines = []
		line = ""
		for word in text.split():
			test = (line + " " + word) if line else word
			if line and _Utf8Len(test) > limit:
				lines.append(line)
				line = word
			else:
				line = test
		if line:
			lines.append(line)
		return lines

	def __OverInItem(self, vnum):
		if not vnum or not self.toolTipItem:
			return
		t = self.toolTipItem
		t.ClearToolTip()
		t.toolTipWidth = TOOLTIP_WIDTH
		item.SelectItem(vnum)
		t.AppendTextLine(item.GetItemName(), t.TITLE_COLOR)
		t.AppendSpace(5)
		for line in self.WrapDescription(item.GetItemDescription()):
			t.AppendTextLine(line, t.FONT_COLOR)
		if vnum in SUCCESS_BOOSTS:
			t.AppendSpace(5)
			t.AppendTextLine(localeInfo.BIOLOG_SUCCESS_BOOST % SUCCESS_BOOST_PERCENT, t.FONT_COLOR)
		if app.ENABLE_GROWTH_PET_SYSTEM:
			t.AppendCompanionShortcutTable()
		t.ShowToolTip()

	def __OverOutItem(self):
		if self.toolTipItem:
			self.toolTipItem.HideToolTip()

	# ------------------------------------------------------------------ open / close
	def Open(self):
		net.SendChatPacket("/biolog info")
		self.__Refresh()
		self.Show()
		self.SetTop()

	def Toggle(self):
		if self.IsShow():
			self.Close()
		else:
			self.Open()

	def Close(self):
		self.__OverOutItem()
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True
