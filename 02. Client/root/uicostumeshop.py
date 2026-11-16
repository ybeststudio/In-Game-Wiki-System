# CostumeShopWindow.__OnClickItemSlot icinde ara:
		if not entry:
			return

# Altina ekle:
		if app.ENABLE_WIKI_SYSTEM and self.interface and self.__IsCtrl() and self.__IsAlt():
			self.interface.SearchWikiForItem(entry.vnum)
			return


# CostumeShopWindow.__AppendShortcuts icinde ara:
		if app.ENABLE_IKASHOP_RENEWAL:
			rows.append((("ctrl", "mouse_right"), localeInfo.TOOLTIP_SHORTCUT_SHOP_SEARCH))

# Altina ekle:
		if app.ENABLE_WIKI_SYSTEM:
			rows.append((("ctrl", "alt", "mouse_left"), localeInfo.TOOLTIP_SHORTCUT_WIKI))

