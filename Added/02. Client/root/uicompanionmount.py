#
# File Name : uicompanionmount.py
# Author    : BestStudio
# Version   : 1.0
# Date      : 2026-11-13
#
import re
import app
import wndMgr
import net
import ui
import item
import player
import chat
import localeInfo
import uiToolTip
import uiCommon

COMPANION_PATH = "d:/ymir work/ui/game/companion/%s"
LABEL_COLOR = 0xffcabdab
VALUE_COLOR = 0xffd1b183

MOUNT_MAX_LEVEL = 30
MOUNT_MAX_EVOLUTION = 3
MOUNT_LEVEL_EXP = 10000
MOUNT_FOOD_MAX = 518400
MOUNT_FOOD_WELL_FED = 259200
MOUNT_FOOD_HUNGRY = 172800
MOUNT_FOOD_STARVING = 86400
MOUNT_FOOD_SPEED = (40, 30, 20, 10, 0)
MOUNT_FOOD_COLOR = (0xff6eeb83, 0xffffd35a, 0xffff8a3d, 0xffff4a4a, 0xffff4a4a)
MOUNT_SKILL_MAX_LEVEL = 10
MOUNT_RUNE_MAX_RANK = 10
VNUM_FOOD = 58003
VNUM_SKILL_UNLOCKER = 58014
VNUM_SKILL_BOOK = 40217

SKILL_APPLY = (item.APPLY_ATTBONUS_ELEMENTS,
	item.APPLY_ATTBONUS_STONE,
	item.APPLY_ATTBONUS_MONSTER, item.APPLY_CRITICAL_PCT)
SKILL_ICON = ("icon/item/item_mount/skill_1.png", "icon/item/item_mount/skill_3.png", "icon/item/item_mount/skill_2.png", "icon/item/item_mount/skill_4.png")
SKILL_VALUE = (0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 5)
RUNE_ITEM = (58030, 58031, 58032, 58033)
RUNE_ICON = tuple("icon/item/mount_runes/badge_%d.png" % v for v in RUNE_ITEM)
RUNE_BONUS = ("ochao", "erebus", "meley", "metin")

# MOUNT_EVOLVE_REQUIREMENTS (key = current evolution)
MOUNT_EVOLVE_REQUIREMENTS = {
	0: (10, ((50050, 5), (40912, 1)), 5000000),
	1: (20, ((50050, 10), (40912, 3), (40914, 1)), 10000000),
	2: (30, ((50050, 15), (40912, 5), (40914, 3)), 15000000),
}

BONUS_POOLS = (
	((item.APPLY_ATTBONUS_STONE, 1, 10), (item.APPLY_STUN_PCT, 1, 8), (item.APPLY_SP_REGEN, 4, 30), (item.APPLY_HP_REGEN, 4, 30), (item.APPLY_REFLECT_MELEE, 1, 10), (item.APPLY_STEAL_HP, 1, 10), (item.APPLY_STEAL_SP, 1, 10)),
	((item.APPLY_ATTBONUS_ELEMENTS, 1, 10), (item.APPLY_ENCHANT_FIRE, 1, 10), (item.APPLY_ENCHANT_DARK, 1, 10), (item.APPLY_ENCHANT_ICE, 1, 10), (item.APPLY_ENCHANT_ELECT, 1, 10), (item.APPLY_ENCHANT_WIND, 1, 10), (item.APPLY_ENCHANT_EARTH, 1, 10)),
	((item.APPLY_PENETRATE_PCT, 1, 10), (item.APPLY_MOV_SPEED, 2, 20), (item.APPLY_POISON_PCT, 1, 8), (item.APPLY_SLOW_PCT, 1, 8), (item.APPLY_DODGE, 2, 15), (item.APPLY_EXP_DOUBLE_BONUS, 2, 20), (item.APPLY_GOLD_DOUBLE_BONUS, 2, 20)),
)

# rune levels from locale/common/config_json/mount_runes.json (loaded once)
_RUNE_DATA = None
def RuneData():
	global _RUNE_DATA
	if _RUNE_DATA is None:
		_RUNE_DATA = []
		try:
			import wikicontent
			for r in wikicontent.LoadCommonJson("config_json/mount_runes.json")["runes"]:
				levels = []
				for l in r["levels"]:
					levels.append((tuple((m["vnum"], m["count"]) for m in l["materials"]), l["cost"], l["prob"], l["blessing"], l["bonuses"][0]["value"]))
				_RUNE_DATA.append(levels)
		except Exception:
			_RUNE_DATA = []
	return _RUNE_DATA


def BonusText(apply, value):
	f = uiToolTip.ItemToolTip.AFFECT_DICT.get(apply)
	if not f:
		return ""
	try:
		return f(value) if callable(f) else (f % value)
	except Exception:
		return ""


def BonusName(apply):
	text = BonusText(apply, 1)
	name = re.sub(r"(^|\s)[+\-]?%?1(\.0)?%?(?=\s|$|,)", " ", text, 1)
	return re.sub(r"\s+", " ", name).strip(" ,:") or text


def Dots(n):
	s = str(int(n))
	out = ""
	while len(s) > 3:
		out = "." + s[-3:] + out
		s = s[:-3]
	return s + out


class MountPage(object):
	def __init__(self, board, owner):
		self.feedDialog = None
		self.owner = owner
		self.board = board
		self.keep = []
		self.info = None
		self.page = 0		# 0 skills, 1 runes
		self.questionDialog = None
		self.toolTip = uiToolTip.ToolTip()
		self.toolTip.HideToolTip()
		self.itemToolTip = uiToolTip.ItemToolTip()
		self.itemToolTip.HideToolTip()
		self.evolveWnd = None
		self.runeWnd = None
		self.__Build(board)

	def Destroy(self):
		self.__CloseQuestion()
		self.redNotice = None
		if self.feedDialog:
			self.feedDialog.Destroy()
			self.feedDialog = None
		if self.evolveWnd:
			self.evolveWnd.Destroy()
			self.evolveWnd = None
		if self.runeWnd:
			self.runeWnd.Destroy()
			self.runeWnd = None
		self.keep = []
		self.c = {}
		self.owner = None

	# ------------------------------------------------------------------ widgets
	def __Image(self, parent, name, x, y, expanded = False):
		img = ui.ExpandedImageBox() if expanded else ui.ImageBox()
		img.SetParent(parent)
		img.LoadImage(name if name.startswith("d:/") or name.startswith("icon/") else COMPANION_PATH % name)
		img.SetPosition(x, y)
		img.AddFlag("not_pick")
		img.Show()
		self.keep.append(img)
		return img

	def __Text(self, parent, text, x, y, center = True, color = LABEL_COLOR):
		line = ui.TextLine()
		line.SetParent(parent)
		line.SetPosition(x, y)
		if center:
			line.SetHorizontalAlignCenter()
		line.SetPackedFontColor(color)
		line.SetOutline()
		line.SetText(text)
		line.Show()
		self.keep.append(line)
		return line

	def __Hover(self, parent, x, y, w, h, overIn, click = None):
		area = ui.Window()
		area.SetParent(parent)
		area.SetPosition(x, y)
		area.SetSize(w, h)
		area.OnMouseOverIn = overIn
		area.OnMouseOverOut = ui.__mem_func__(self.__HideToolTip)
		if click:
			area.OnMouseLeftButtonUp = click
		area.Show()
		self.keep.append(area)
		return area

	def __Button(self, parent, name, x, y, text, event):
		btn = ui.Button()
		btn.SetParent(parent)
		btn.SetPosition(x, y)
		btn.SetUpVisual(COMPANION_PATH % (name + "_norm.png"))
		btn.SetOverVisual(COMPANION_PATH % (name + "_hover.png"))
		btn.SetDownVisual(COMPANION_PATH % (name + "_select.png"))
		btn.SetEvent(event)
		btn.Show()
		self.keep.append(btn)
		label = ui.TextLine()
		label.SetParent(btn)
		label.AddFlag("not_pick")
		label.SetPosition(41, 10)
		label.SetPackedFontColor(LABEL_COLOR)
		label.SetText(text)
		label.Show()
		self.keep.append(label)
		return btn

	def __SmallButton(self, parent, base, x, y, event):
		btn = ui.Button()
		btn.SetParent(parent)
		btn.SetPosition(x, y)
		btn.SetUpVisual(base + "_norm.png" if not base.endswith(".tga") else base)
		btn.SetOverVisual(base + "_hover.png" if not base.endswith(".tga") else base)
		btn.SetDownVisual(base + "_select.png" if not base.endswith(".tga") else base)
		btn.SetEvent(event)
		btn.Show()
		self.keep.append(btn)
		return btn

	def __HelpButton(self, parent, x, y, lines):
		btn = ui.Button()
		btn.SetParent(parent)
		btn.SetPosition(x, y)
		btn.SetUpVisual("d:/ymir work/ui/pattern/q_mark_01.tga")
		btn.SetOverVisual("d:/ymir work/ui/pattern/q_mark_02.tga")
		btn.SetDownVisual("d:/ymir work/ui/pattern/q_mark_01.tga")
		btn.SetShowToolTipEvent(lines)
		btn.SetHideToolTipEvent(ui.__mem_func__(self.__HideToolTip))
		btn.Show()
		self.keep.append(btn)
		return btn

	def __Tab(self, parent, x, y, text, index):
		tab = OrnamentTab(parent, x, y, text, lambda i = index: self.SelectPage(i))
		self.keep.append(tab)
		return tab

	def __Build(self, board):
		c = {}
		win = ui.Window()
		win.SetParent(board)
		win.SetPosition(0, 0)
		win.SetSize(280, 415)
		win.AddFlag("not_pick")
		win.Hide()
		c["mount_window"] = win

		bg = self.__Image(win, "background.png", 7, 30)
		c["backgound"] = bg

		c["slot_bg"] = self.__Image(bg, "bg_slot.png", 4, 4)
		c["slot_img"] = self.__Image(c["slot_bg"], "slot_new.png", 13, 13)
		icon = ui.ImageBox()
		icon.SetParent(c["slot_img"])
		icon.SetPosition(2, 2)
		icon.SetStringEvent("MOUSE_OVER_IN", ui.__mem_func__(self.__OverInSeal))
		icon.SetStringEvent("MOUSE_OVER_OUT", ui.__mem_func__(self.__HideItemToolTip))
		icon.Show()
		self.keep.append(icon)
		c["mount_icon"] = icon

		titles = (localeInfo.COMPANION_PET_NAME, localeInfo.COMPANION_PET_LEVEL, localeInfo.PET_EVOLUTION_TITLE)
		for i in xrange(3):
			c["bg_desc_%d" % i] = self.__Image(bg, "detail_title.png", 70, 4 + 22 * i)
			c["desc_%d" % i] = self.__Text(c["bg_desc_%d" % i], titles[i], 45, 4)
			c["bg_value_%d" % i] = self.__Image(bg, "detail_value.png", 162, 3 + 22 * i)
			c["value_%d" % i] = self.__Text(c["bg_value_%d" % i], "", 49, 4, True, VALUE_COLOR)

		c["subheader_bg_1"] = self.__Image(bg, "subheader_bg.png", 2, 68)
		self.__Text(c["subheader_bg_1"], localeInfo.COMPANION_EXP, 66, 5)
		c["subheader_bg_2"] = self.__Image(bg, "subheader_bg.png", 131, 68)
		self.__Text(c["subheader_bg_2"], localeInfo.MOUNT_FOOD, 66, 5)

		c["exp_bg"] = self.__Image(bg, "details_bg.png", 3, 92)
		expWin = ui.Window()
		expWin.SetParent(c["exp_bg"])
		expWin.SetPosition(11, 7)
		expWin.SetSize(126, 32)
		expWin.AddFlag("not_pick")
		expWin.Show()
		self.keep.append(expWin)
		for k in xrange(4):
			self.__Image(expWin, "progress_empty.png", 4 + 25 * k, 4)
			c["exp_full_%d" % (k + 1)] = self.__Image(expWin, "progress.png", 4 + 25 * k, 4)
		self.__Hover(c["exp_bg"], 0, 0, 130, 47, ui.__mem_func__(self.__OverInExp), ui.__mem_func__(self.__OnClickDonate))

		c["duration_bg"] = self.__Image(bg, "details_bg.png", 132, 92)
		c["duration_empty"] = self.__Image(c["duration_bg"], "gauge_empty.png", 6, 5)
		c["duration_full"] = self.__Image(c["duration_bg"], "gauge_full.png", 8, 7, True)
		c["duration_text"] = self.__Text(c["duration_bg"], "", 65, 28)
		self.__Hover(c["duration_bg"], 0, 0, 130, 47, ui.__mem_func__(self.__OverInFood))

		c["evolve_btn"] = self.__Button(bg, "btn_evolve", 2, 138, localeInfo.COMPANION_EVOLVE, ui.__mem_func__(self.__OnClickEvolve))
		c["feed_btn"] = self.__Button(bg, "btn_feed", 132, 138, localeInfo.MOUNT_FEED, ui.__mem_func__(self.__OnClickFeed))

		c["header_bg_2"] = self.__Image(bg, "header_title.png", 2, 169)
		self.__Text(c["header_bg_2"], localeInfo.MOUNT_BONUS_HEADER, 130, 7)
		for i in xrange(3):
			row = self.__Image(bg, "bonus_bg.png", 4, 198 + 28 * i)
			c["bg_bonus_%d" % i] = row
			c["bonus_desc_%d" % i] = self.__Text(row, "", 8, 6, False)
			c["bonus_value_%d" % i] = self.__Text(row, "", 208, 6, True, VALUE_COLOR)
			self.__HelpButton(row, 236, 5, lambda s = i: self.__ShowBonusPool(s))

		c["progress_tab_0"] = self.__Tab(bg, 4, 282, localeInfo.COMPANION_SKILLS, 0)
		c["progress_tab_1"] = self.__Tab(bg, 133, 282, localeInfo.MOUNT_RUNE_PAGE_TITLE, 1)
		self.__HelpButton(bg, 110, 288, ui.__mem_func__(self.__ShowSkillInformation))
		self.__HelpButton(bg, 239, 288, lambda: self.__ShowDescription(localeInfo.MOUNT_RUNE_INFORMATION, 398, 77))

		c["skill_bg"] = self.__Image(bg, "bg_skill_mount.png", 3, 312)
		self.skillSlot = []
		self.skillIcon = []
		self.skillLock = []
		self.skillUp = []
		self.runeIcon = []
		self.runeUp = []
		for i in xrange(4):
			x = 37 + 51 * i
			lock = self.__Image(c["skill_bg"], "slot_locked.png", x, 15)
			self.skillLock.append(lock)
			ic = ui.ImageBox()
			ic.SetParent(c["skill_bg"])
			ic.SetPosition(x, 15)
			ic.SetStringEvent("MOUSE_OVER_IN", lambda s = i: self.__OverInSlot(s))
			ic.SetStringEvent("MOUSE_OVER_OUT", ui.__mem_func__(self.__HideToolTip))
			ic.OnMouseLeftButtonUp = lambda s = i: self.__OnClickSlot(s)
			ic.Show()
			self.keep.append(ic)
			self.skillIcon.append(ic)
			up = self.__SmallButton(c["skill_bg"], "d:/ymir work/ui/game/common/add", x - 17, 37, lambda s = i: self.__OnClickUp(s))
			up.Hide()
			self.skillUp.append(up)

		notMount = ui.ThinBoardCircle()
		notMount.SetParent(win)
		notMount.SetPosition(9, 30)
		notMount.SetSize(262, 375)
		notMount.Hide()
		c["not_mount"] = notMount
		self.keep.append(notMount)
		self.__Text(notMount, localeInfo.MOUNT_NO_SPAWN, 131, 187)

		self.c = c
		self.SelectPage(0)

	# ------------------------------------------------------------------ show / data
	def Show(self):
		self.c["mount_window"].Show()
		net.SendChatPacket("/mountx info")
		self.Refresh()

	def Hide(self):
		self.c["mount_window"].Hide()
		self.__HideToolTip()
		if self.feedDialog:
			self.feedDialog.Close()

	def IsShow(self):
		return self.c["mount_window"].IsShow()

	def SetInfo(self, args):
		if not args or int(args[0]) == 0:
			self.info = None
		else:
			v = map(int, args)
			self.info = {
				"seal": v[0], "level": v[1], "exp": v[2], "evo": v[3], "food": v[4], "time": app.GetTime(),
				"bonus": [(v[5], v[6]), (v[7], v[8]), (v[9], v[10])],
				"skill": v[11:15], "unlocked": v[15], "rune": v[16:20], "bless": v[20:24],
				"medal": v[24], "medalCount": v[25],
			}
		self.Refresh()
		if self.evolveWnd and self.evolveWnd.IsShow() and self.info:
			self.evolveWnd.Open(self.info["evo"])

	def __FoodLeft(self):
		if not self.info:
			return 0
		return max(0, self.info["food"] - int(app.GetTime() - self.info["time"]))

	def Refresh(self):
		c = self.c
		info = self.info
		if not info:
			c["not_mount"].Show()
			c["backgound"].Hide()
			return
		c["not_mount"].Hide()
		c["backgound"].Show()
		if self.page == 1 and not self.__RuneReady():
			self.SelectPage(0)
		else:
			c["progress_tab_1"].SetEnabled(self.__RuneReady())

		sealVnum = player.GetItemIndex(item.EQUIPMENT_MOUNT) if app.ENABLE_MOUNT_SYSTEM else 0
		if sealVnum:
			item.SelectItem(sealVnum)
			c["mount_icon"].LoadImage(item.GetIconImageFileName())
			c["value_0"].SetText(localeInfo.MOUNT_DEFAULT_NAME_SHORT)
		c["value_1"].SetText("%d / %d" % (info["level"], MOUNT_MAX_LEVEL))
		c["value_2"].SetText("%d / %d" % (info["evo"] + 1, MOUNT_MAX_EVOLUTION + 1))

		filled = min(4, int(float(info["exp"]) / MOUNT_LEVEL_EXP * 4)) if info["level"] < MOUNT_MAX_LEVEL else 4
		for k in xrange(4):
			if k < filled:
				c["exp_full_%d" % (k + 1)].Show()
			else:
				c["exp_full_%d" % (k + 1)].Hide()

		food = self.__FoodLeft()
		c["duration_full"].SetRenderingRect(0.0, 0.0, min(1.0, float(food) / MOUNT_FOOD_MAX) - 1.0, 0.0)
		c["duration_text"].SetText(localeInfo.MOUNT_HORSE_SPEED_TEXT % MOUNT_FOOD_SPEED[self.__FoodState(food)])

		for i in xrange(3):
			(apply, value) = info["bonus"][i]
			if i <= info["evo"] and apply:
				c["bonus_desc_%d" % i].SetText(BonusName(apply))
				c["bonus_value_%d" % i].SetText(str(value))
			else:
				c["bonus_desc_%d" % i].SetText(localeInfo.MOUNT_BONUS_UNLOCK % (i + 1))
				c["bonus_value_%d" % i].SetText("")

		self.__RefreshSlots()

	def __FoodState(self, food):
		if food >= MOUNT_FOOD_WELL_FED:
			return 0
		if food >= MOUNT_FOOD_HUNGRY:
			return 1
		if food >= MOUNT_FOOD_STARVING:
			return 2
		if food > 0:
			return 3
		return 4

	def __RuneReady(self):
		info = self.info
		if not info or info["level"] < MOUNT_MAX_LEVEL or info["evo"] < MOUNT_MAX_EVOLUTION:
			return False
		return min(info["skill"]) >= MOUNT_SKILL_MAX_LEVEL

	def SelectPage(self, page):
		if page == 1 and not self.__RuneReady():
			page = 0
		self.page = page
		self.c["progress_tab_1"].SetEnabled(self.__RuneReady())
		self.c["progress_tab_0"].SetSelected(page == 0)
		self.c["progress_tab_1"].SetSelected(page == 1)
		self.__RefreshSlots()

	def __RefreshSlots(self):
		info = self.info
		for i in xrange(4):
			icon = self.skillIcon[i]
			up = self.skillUp[i]
			lock = self.skillLock[i]
			if not info:
				icon.Hide()
				up.Hide()
				lock.Show()
				continue
			if self.page == 0:
				unlocked = i < info["unlocked"]
				if unlocked:
					icon.LoadImage(SKILL_ICON[i])
					icon.Show()
					lock.Hide()
					up.Show() if info["skill"][i] < MOUNT_SKILL_MAX_LEVEL else up.Hide()
				else:
					icon.LoadImage(COMPANION_PATH % "slot_locked.png")
					icon.Show()
					lock.Show()
					up.Hide()
			else:
				icon.LoadImage(RUNE_ICON[i])
				icon.Show()
				lock.Hide()
				up.Show() if info["rune"][i] < MOUNT_RUNE_MAX_RANK else up.Hide()

	# ------------------------------------------------------------------ tooltips
	def __ShowLines(self, lines, title = None):
		t = self.toolTip
		t.ClearToolTip()
		t.toolTipWidth = 240
		if title:
			t.AppendTextLine(title, t.TITLE_COLOR)
		for line in lines:
			t.AppendTextLine(line, LABEL_COLOR)
		t.ShowToolTip()

	def __HideToolTip(self):
		self.toolTip.HideToolTip()

	def __HideItemToolTip(self):
		self.itemToolTip.HideToolTip()

	def __OverInSeal(self):
		if app.ENABLE_MOUNT_SYSTEM and player.GetItemIndex(item.EQUIPMENT_MOUNT):
			self.itemToolTip.SetInventoryItem(item.EQUIPMENT_MOUNT)

	def __OverInExp(self):
		info = self.info
		if not info:
			return
		if info["level"] >= MOUNT_MAX_LEVEL:
			self.__ShowLines([localeInfo.MOUNT_MAX_LEVEL_REACHED], localeInfo.COMPANION_EXP)
			return
		t = self.toolTip
		t.ClearToolTip()
		t.toolTipWidth = 212
		t.AppendTextLine(localeInfo.COMPANION_EXP, LABEL_COLOR)
		t.AppendTextLine("%d / %d" % (info["exp"], MOUNT_LEVEL_EXP), LABEL_COLOR)
		t.ShowToolTip()

	def __OnClickDonate(self):
		if not self.info:
			return
		net.SendChatPacket("/mountx donate %d" % (10 if app.IsPressed(app.DIK_LCONTROL) else 1))

	def __OverInFood(self):
		food = self.__FoodLeft()
		state = self.__FoodState(food)
		names = (localeInfo.MOUNT_FOOD_STATE_WELL_FED, localeInfo.MOUNT_FOOD_STATE_HUNGRY, localeInfo.MOUNT_FOOD_STATE_STARVING, localeInfo.MOUNT_FOOD_STATE_DYING, localeInfo.MOUNT_FOOD_TOOLTIP_EMPTY)
		t = self.toolTip
		t.ClearToolTip()
		t.toolTipWidth = 240
		t.AppendTextLine(names[state], MOUNT_FOOD_COLOR[state])
		t.AppendTextLine(localeInfo.MOUNT_HORSE_SPEED_TEXT % MOUNT_FOOD_SPEED[state], MOUNT_FOOD_COLOR[state])
		nextEdge = {0: (MOUNT_FOOD_WELL_FED, localeInfo.MOUNT_FOOD_TOOLTIP_TO_HUNGRY), 1: (MOUNT_FOOD_HUNGRY, localeInfo.MOUNT_FOOD_TOOLTIP_TO_STARVING), 2: (MOUNT_FOOD_STARVING, localeInfo.MOUNT_FOOD_TOOLTIP_TO_DYING), 3: (0, localeInfo.MOUNT_FOOD_TOOLTIP_TO_DYING)}
		if nextEdge.has_key(state):
			(edge, text) = nextEdge[state]
			left = max(0, food - edge)
			t.AppendSpace(5)
			t.AppendTextLine(text, LABEL_COLOR)
			t.AppendTextLine(localeInfo.MOUNT_FOOD_TIME_FMT % (left / 3600, (left % 3600) / 60, left % 60), LABEL_COLOR)
		t.ShowToolTip()

	def __Time(self, sec):
		sec = max(0, int(sec))
		return localeInfo.PET_SEAL_TIME_DHM % (sec / 86400, (sec % 86400) / 3600, (sec % 3600) / 60)

	def __ShowDescription(self, text, width, limit):
		t = self.toolTip
		t.ClearToolTip()
		t.toolTipWidth = width
		t.AppendDescription(text, limit, t.FONT_COLOR)
		t.ShowToolTip()

	def __ShowSkillInformation(self, lockedSlot = False):
		item.SelectItem(VNUM_SKILL_UNLOCKER)
		text = localeInfo.MOUNT_SKILL_INFORMATION % item.GetItemName()
		if lockedSlot:
			text += "^" + localeInfo.MOUNT_SKILL_UNLOCK_REQUIREMENTS
		self.__ShowDescription(text, 288, 60)

	def __ShowBonusPool(self, slot):
		titles = (localeInfo.MOUNT_BONUS_AVAILABLE_FIRST, localeInfo.MOUNT_BONUS_AVAILABLE_SECOND, localeInfo.MOUNT_BONUS_AVAILABLE_THIRD)
		names = []
		for (apply, lo, hi) in BONUS_POOLS[slot]:
			if apply:
				names.append(BonusName(apply))
		t = self.toolTip
		t.ClearToolTip()
		t.toolTipWidth = 244
		t.AppendTextLine(titles[slot], t.TITLE_COLOR)
		t.AppendSpace(4)
		width = 225
		left = (t.toolTipWidth - width) / 2
		top = t.toolTipHeight
		ROW = 18

		def bar(x, y, w, h, color):
			b = ui.Bar()
			b.SetParent(t)
			b.SetPosition(x, y)
			b.SetSize(w, h)
			b.SetColor(color)
			b.Show()
			t.childrenList.append(b)

		height = ROW * len(names) + 1
		bar(left, top, width, height, 0xff170f0c)
		bar(left, top, width, 1, 0xff201811)
		bar(left, top + height - 1, width, 1, 0xff201811)
		bar(left, top, 1, height, 0xff201811)
		bar(left + width - 1, top, 1, height, 0xff201811)
		for index, name in enumerate(names):
			y = top + ROW * index
			if index:
				bar(left + 1, y, width - 2, 1, 0xff756657)
			line = ui.TextLine()
			line.SetParent(t)
			line.SetPosition(t.toolTipWidth / 2, y + 3)
			line.SetHorizontalAlignCenter()
			line.SetPackedFontColor(0xffc7c7c7)
			line.SetOutline()
			line.SetText(name)
			line.Show()
			t.childrenList.append(line)
		t.toolTipHeight += height + 2
		t.ResizeToolTip()
		t.ShowToolTip()

	def __BonusPoolLines(self, slot):
		titles = (localeInfo.MOUNT_BONUS_AVAILABLE_FIRST, localeInfo.MOUNT_BONUS_AVAILABLE_SECOND, localeInfo.MOUNT_BONUS_AVAILABLE_THIRD)
		lines = [titles[slot]]
		for (apply, lo, hi) in BONUS_POOLS[slot]:
			if apply:
				lines.append("%s  %d - %d" % (BonusName(apply), lo, hi))
		return lines

	def __OverInSlot(self, i):
		info = self.info
		if not info:
			return
		if self.page == 0:
			if i >= info["unlocked"]:
				self.__ShowSkillInformation(True)
				return
			level = info["skill"][i]
			self.__ShowLines([BonusText(SKILL_APPLY[i], SKILL_VALUE[level]), localeInfo.MOUNT_SKILL_LEVEL % (level, MOUNT_SKILL_MAX_LEVEL)])
		else:
			rank = info["rune"][i]
			item.SelectItem(RUNE_ITEM[i])
			lines = [localeInfo.MOUNT_RUNE_RANK_FMT % (rank, MOUNT_RUNE_MAX_RANK)]
			data = RuneData()
			if i < len(data) and rank > 0:
				lines.append(localeInfo.MOUNT_RUNE_CURRENT + ": +%d%%" % data[i][rank - 1][4])
			if i < len(data) and rank < MOUNT_RUNE_MAX_RANK:
				lines.append(localeInfo.MOUNT_RUNE_NEXT + ": +%d%%" % data[i][rank][4])
			lines.append(localeInfo.MOUNT_RUNE_BLESSING_FMT % (info["bless"][i], data[i][rank][3] if i < len(data) and rank < MOUNT_RUNE_MAX_RANK else 0))
			self.__ShowLines(lines, item.GetItemName())

	# ------------------------------------------------------------------ actions
	def __Question(self, text, event):
		self.__CloseQuestion()
		dlg = uiCommon.QuestionDialog()
		dlg.SetText(text)
		dlg.SetAcceptEvent(lambda: (self.__CloseQuestion(), event()))
		dlg.SetCancelEvent(ui.__mem_func__(self.__CloseQuestion))
		dlg.Open()
		self.questionDialog = dlg

	def __CloseQuestion(self):
		if self.questionDialog:
			self.questionDialog.Close()
			self.questionDialog = None

	def __OnClickFeed(self):
		if not self.info:
			return
		if not self.feedDialog:
			self.feedDialog = MountFeedDialog(self.board)
		self.feedDialog.Open()

	def __OnClickEvolve(self):
		if not self.info:
			return
		import uiCompanion
		if not self.evolveWnd:
			self.evolveWnd = uiCompanion.PetUpgradeTypeWindow(self.owner, "mount")
		if self.evolveWnd.IsShow():
			self.evolveWnd.Close()
			return
		self.evolveWnd.Open(self.info["evo"])

	def __SkillUnlockError(self, i):
		info = self.info
		if info["level"] < MOUNT_MAX_LEVEL or info["evo"] < MOUNT_MAX_EVOLUTION:
			return localeInfo.MOUNT_SKILL_UNLOCK_REQUIREMENTS
		if i != info["unlocked"] or (i > 0 and info["skill"][i - 1] < MOUNT_SKILL_MAX_LEVEL):
			return localeInfo.MOUNT_SKILL_UNLOCK_ORDER
		if player.GetItemCountByVnum(VNUM_SKILL_UNLOCKER) <= 0:
			return localeInfo.COMPANION_TYPE_UP_ITEM
		return None

	def __ShowRedNotice(self, text):
		self.redNotice = ui.NoticeBoxBoard(text)

	def __OnClickSlot(self, i):
		info = self.info
		if not info or self.page != 0 or i < info["unlocked"]:
			return
		error = self.__SkillUnlockError(i)
		if error:
			self.__ShowRedNotice(error)
			return
		item.SelectItem(VNUM_SKILL_UNLOCKER)
		self.__Question(localeInfo.MOUNT_SKILL_UNLOCK_CONFIRM_FMT % item.GetItemName(), lambda: net.SendChatPacket("/mountx skill_unlock"))

	def __OnClickUp(self, i):
		if not self.info:
			return
		if self.page == 0:
			self.__Question(localeInfo.MOUNT_UPGRADE_SKILL_CONFIRMATION, lambda s = i: net.SendChatPacket("/mountx skill_up %d" % s))
			return
		import uiCompanion
		if not self.runeWnd:
			self.runeWnd = uiCompanion.PetUpgradeTypeWindow(self.owner, "rune")
		self.runeWnd.Open(i, self.info)

	def OnResult(self, code, value):
		texts = {
			0: localeInfo.MOUNT_NO_SPAWN, 1: localeInfo.MOUNT_RESULT_LEVEL_CAP, 2: localeInfo.COMPANION_TYPE_UP_ITEM, 3: localeInfo.COMPANION_TYPE_UP_GOLD,
			4: localeInfo.MOUNT_RESULT_EVOLVED, 5: localeInfo.MOUNT_RUNE_MAX, 6: localeInfo.MOUNT_RESULT_FED, 7: localeInfo.MOUNT_SKILL_UNLOCK_REQUIREMENTS,
			8: localeInfo.MOUNT_SKILL_UNLOCK_ORDER, 9: localeInfo.MOUNT_RESULT_SKILL_UNLOCKED, 10: localeInfo.MOUNT_RESULT_SKILL_UP, 11: localeInfo.MOUNT_RESULT_SKILL_FAIL,
			12: localeInfo.MOUNT_RUNE_MAX, 13: localeInfo.MOUNT_RUNE_REQUIRE_SKILLS, 14: localeInfo.MOUNT_RUNE_PREVIOUS_MAX, 15: localeInfo.MOUNT_RUNE_SUCCESS,
			16: localeInfo.MOUNT_RUNE_FAILURE, 17: localeInfo.MOUNT_RESULT_BONUS_LOCKED, 18: localeInfo.MOUNT_RESULT_BONUS_CHANGED, 20: localeInfo.MOUNT_RESULT_LEVEL_UP,
		}
		if code == 19:
			return
		text = texts.get(code)
		if text:
			try:
				text = text % value
			except TypeError:
				pass
			if code in (2, 3, 7, 8, 13, 14, 17):
				self.__ShowRedNotice(text)
			else:
				chat.AppendChat(chat.CHAT_TYPE_INFO, text)
		if self.runeWnd and self.runeWnd.IsShow() and self.info and code in (15, 16):
			self.runeWnd.Open(value, self.info)


class MountFeedDialog(ui.ThinBoard):
	WIDTH = 270
	HEIGHT = 185

	def __init__(self, board):
		self.keep = []
		self.host = board
		self.blocker = ui.Window()
		self.blocker.SetParent(board)
		self.blocker.SetPosition(0, 0)
		self.blocker.SetSize(board.GetWidth(), board.GetHeight())
		self.blocker.Hide()
		self.underlay = ui.Bar()
		self.underlay.SetParent(board)
		self.underlay.SetColor(0xff2e2520)
		self.underlay.AddFlag("not_pick")
		self.underlay.Hide()
		ui.ThinBoard.__init__(self)
		self.SetParent(board)
		if app.ENABLE_UI_BACKGROUND_BLUR:
			wndMgr.SetBackgroundBlur(self.hWnd, 0)
		self.toolTipItem = uiToolTip.ItemToolTip()
		self.toolTipItem.HideToolTip()
		self.SetSize(self.WIDTH, self.HEIGHT)

		self.__Text(localeInfo.MOUNT_FEED_CONFIRMATION, 20)
		x = (self.WIDTH - 32) / 2
		for i in xrange(3):
			slot = ui.ImageBox()
			slot.SetParent(self)
			slot.LoadImage("d:/ymir work/ui/public/slot_base.sub")
			slot.SetPosition(x, 34 + 33 * i)
			slot.AddFlag("not_pick")
			slot.Show()
			self.keep.append(slot)
		item.SelectItem(VNUM_FOOD)
		icon = ui.ImageBox()
		icon.SetParent(self)
		icon.LoadImage(item.GetIconImageFileName())
		icon.SetPosition(x, 34)
		icon.SetStringEvent("MOUSE_OVER_IN", ui.__mem_func__(self.__OverInItem))
		icon.SetStringEvent("MOUSE_OVER_OUT", ui.__mem_func__(self.__OverOutItem))
		icon.Show()
		self.keep.append(icon)
		count = ui.NumberLine()
		count.SetParent(icon)
		count.SetPosition(20, 20)
		count.SetNumber("1")
		count.Show()
		self.keep.append(count)
		self.__Text(localeInfo.MOUNT_FEED_NEED % item.GetItemName(), 139)

		for (name, dx, event) in (("accept", -40, self.__OnAccept), ("cancel", 40, self.Close)):
			btn = ui.Button()
			btn.SetParent(self)
			btn.SetUpVisual("d:/ymir work/ui/game/common/button_%s_norm.png" % name)
			btn.SetOverVisual("d:/ymir work/ui/game/common/button_%s_hover.png" % name)
			btn.SetDownVisual("d:/ymir work/ui/game/common/button_%s_down.png" % name)
			btn.SetPosition((self.WIDTH - 57) / 2 + dx, 152)
			btn.SetEvent(ui.__mem_func__(event))
			btn.Show()
			self.keep.append(btn)

	def __del__(self):
		ui.ThinBoard.__del__(self)

	def Destroy(self):
		self.Hide()
		if self.blocker:
			self.blocker.Hide()
			self.blocker = None
		if self.underlay:
			self.underlay.Hide()
			self.underlay = None
		self.host = None
		self.keep = []
		self.toolTipItem = None

	def __Text(self, text, y):
		line = ui.TextLine()
		line.SetParent(self)
		line.SetPosition(self.WIDTH / 2, y)
		line.SetHorizontalAlignCenter()
		line.SetVerticalAlignCenter()
		line.SetPackedFontColor(LABEL_COLOR)
		line.SetText(text)
		line.Show()
		self.keep.append(line)
		return line

	def Open(self):
		board = self.host
		self.blocker.SetSize(board.GetWidth(), board.GetHeight())
		self.blocker.Show()
		self.blocker.SetTop()
		x = int((board.GetWidth() - self.WIDTH) / 2)
		y = int((board.GetHeight() - self.HEIGHT) / 2)
		self.underlay.SetPosition(x + 1, y + 1)
		self.underlay.SetSize(self.WIDTH - 2, self.HEIGHT - 2)
		self.underlay.Show()
		self.underlay.SetTop()
		self.SetPosition(x, y)
		self.Show()
		self.SetTop()

	def Close(self):
		self.__OverOutItem()
		self.blocker.Hide()
		self.underlay.Hide()
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def __OnAccept(self):
		net.SendChatPacket("/mountx feed")
		self.Close()

	def __OverInItem(self):
		if self.toolTipItem:
			self.toolTipItem.SetItemToolTip(VNUM_FOOD, 310)
			self.toolTipItem.AppendCompanionShortcutTable()

	def __OverOutItem(self):
		if self.toolTipItem:
			self.toolTipItem.HideToolTip()


class OrnamentTab(ui.Window):
	WIDTH = 128
	HEIGHT = 30
	BASE = "d:/ymir work/ui/game/searchshop/tab_categ_list%s.png"
	COLOR_SELECTED = 0xffd1b183
	COLOR_NORMAL = 0xffcabdab
	COLOR_DISABLED = 0xff777777

	def __init__(self, parent, x, y, text, event):
		ui.Window.__init__(self)
		self.SetParent(parent)
		self.SetPosition(x, y)
		self.SetSize(self.WIDTH, self.HEIGHT)
		self.event = event
		self.selected = False
		self.enabled = True
		self.hovered = False
		self.left = ui.ExpandedImageBox()
		self.left.SetParent(self)
		self.left.SetPosition(0, 0)
		self.left.AddFlag("not_pick")
		self.right = ui.ExpandedImageBox()
		self.right.SetParent(self)
		self.right.SetPosition(18, 0)
		self.right.AddFlag("not_pick")
		self.label = ui.TextLine()
		self.label.SetParent(self)
		self.label.SetPosition(self.WIDTH / 2, self.HEIGHT / 2)
		self.label.SetHorizontalAlignCenter()
		self.label.SetVerticalAlignCenter()
		self.label.SetOutline()
		self.label.AddFlag("not_pick")
		self.label.SetText(text)
		self.__Refresh()
		self.left.Show()
		self.right.Show()
		self.label.Show()
		self.Show()

	def __del__(self):
		ui.Window.__del__(self)

	def __Refresh(self):
		if self.selected:
			suffix = "_active_hover" if self.hovered else "_active"
			color = self.COLOR_SELECTED
		elif not self.enabled:
			suffix = ""
			color = self.COLOR_DISABLED
		else:
			suffix = "_hover" if self.hovered else ""
			color = self.COLOR_NORMAL
		image = self.BASE % suffix
		self.left.LoadImage(image)
		self.right.LoadImage(image)
		cut = float(110 - 64) / 110
		self.left.SetRenderingRect(0.0, 0.0, -cut, 0.0)
		self.right.SetRenderingRect(-cut, 0.0, 0.0, 0.0)
		self.label.SetPackedFontColor(color)

	def SetSelected(self, flag):
		self.selected = flag
		self.__Refresh()

	def SetEnabled(self, flag):
		self.enabled = flag
		self.__Refresh()

	def OnMouseOverIn(self):
		self.hovered = self.enabled
		self.__Refresh()

	def OnMouseOverOut(self):
		self.hovered = False
		self.__Refresh()

	def OnMouseLeftButtonUp(self):
		if self.enabled and not self.selected and self.event:
			self.event()

