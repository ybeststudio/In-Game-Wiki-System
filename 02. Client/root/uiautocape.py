# BraveCapeWindow.__OnItemShortcut icinde ara:
		alt = app.IsPressed(app.DIK_LALT) or app.IsPressed(app.DIK_RALT)
		vnum = self.GetCapeVnum()

# Altina ekle:
		if ctrl and alt and app.ENABLE_WIKI_SYSTEM:
			interface.SearchWikiForItem(vnum)
		elif ctrl and not alt and app.ENABLE_IKASHOP_RENEWAL:
			interface.SearchShopForItem(vnum)


# BraveCapeWindow.__OverInItem icinde ara:
		if app.ENABLE_IKASHOP_RENEWAL:
			rows.append((("ctrl", "mouse_left"), localeInfo.TOOLTIP_SHORTCUT_SHOP_SEARCH))

# Altina ekle:
		if app.ENABLE_WIKI_SYSTEM:
			rows.append((("ctrl", "alt", "mouse_left"), localeInfo.TOOLTIP_SHORTCUT_WIKI))

