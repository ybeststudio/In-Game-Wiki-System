# ItemToolTip.SetInventoryItem icinde ara:
				itemVnum = player.GetItemIndex(player.INVENTORY, slotIndex)
		self.ClearToolTip()

# Altina ekle:
		if window_type == player.INVENTORY and (app.ENABLE_IKASHOP_RENEWAL or app.ENABLE_WIKI_SYSTEM):
			self.toolTipWidth = max(self.toolTipWidth, 310)
			self.ResizeToolTip()


# ItemToolTip.SetShopItemMultiPrice icinde ara:
			if app.ENABLE_IKASHOP_RENEWAL:
				rows.append((("ctrl", "mouse_right"), localeInfo.TOOLTIP_SHORTCUT_SHOP_SEARCH))

# Altina ekle:
			if app.ENABLE_WIKI_SYSTEM:
				rows.append((("ctrl", "alt", "mouse_left"), localeInfo.TOOLTIP_SHORTCUT_WIKI))


# ItemToolTip icinde ara:
					metinSlot[0] = app.GetGlobalTimeStamp()+limitValue
		self.AddItemData(itemVnum, metinSlot, attrSlot)

# Altina ekle:
	if app.ENABLE_WIKI_SYSTEM:
		def SetItemToolTipWiki(self, itemVnum):
			self.itemVnum = itemVnum
			item.SelectItem(itemVnum)

			metinSlot = [0 for i in xrange(player.METIN_SOCKET_MAX_NUM)]
			attrSlot = [(0, 0) for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM)]

			for i in xrange(item.LIMIT_MAX_NUM):
				(limitType, limitValue) = item.GetLimit(i)
				if item.LIMIT_TIMER_BASED_ON_WEAR == limitType:
					metinSlot[0] = limitValue
				elif item.LIMIT_REAL_TIME == limitType or item.LIMIT_REAL_TIME_START_FIRST_USE == limitType:
					metinSlot[0] = app.GetGlobalTimeStamp()+limitValue

			self.SetTitle(item.GetItemName())
			self.AppendDescription(item.GetItemDescription(), 26)
			self.AppendDescription(item.GetItemSummary(), 26, self.CONDITION_COLOR)
			self.__AppendAffectInformation()
			self.__AppendAttributeInformation(attrSlot)
			self.AppendWearableInformation()

			for i in xrange(item.LIMIT_MAX_NUM):
				(limitType, limitValue) = item.GetLimit(i)
				if item.LIMIT_REAL_TIME == limitType:
					if metinSlot[0] > 0:
						self.AppendMallItemLastTime(metinSlot[0], limitValue)
					break

			self.ShowToolTip()


# ItemToolTip.AddItemData icinde ara:
			if app.ENABLE_IKASHOP_RENEWAL:
				shortcutRows.append((("ctrl", "mouse_right"), localeInfo.TOOLTIP_SHORTCUT_SHOP_SEARCH))

# Altina ekle:
			if app.ENABLE_WIKI_SYSTEM:
				shortcutRows.append((("ctrl", "alt", "mouse_left"), localeInfo.TOOLTIP_SHORTCUT_WIKI))


# ItemToolTip.AppendCompanionShortcutTable icinde ara:
			if app.ENABLE_IKASHOP_RENEWAL:
				rows.append((("ctrl", "mouse_right"), localeInfo.TOOLTIP_SHORTCUT_SHOP_SEARCH))

# Altina ekle:
			if app.ENABLE_WIKI_SYSTEM:
				rows.append((("ctrl", "alt", "mouse_left"), localeInfo.TOOLTIP_SHORTCUT_WIKI))

