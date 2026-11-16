# WardrobeWindow.ClickCard icinde ara:
				return
			if (app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL)) and (app.IsPressed(app.DIK_LALT) or app.IsPressed(app.DIK_RALT)):

# Altina ekle:
				if app.ENABLE_WIKI_SYSTEM and self.interface:
					self.interface.SearchWikiForItem(vnum)


# WardrobeWindow.__ShowCardToolTip icinde ara:
			rows.append((("ctrl", "mouse_right"), localeInfo.TOOLTIP_SHORTCUT_SHOP_SEARCH))
		if isStored:

# Altina ekle:
			if app.ENABLE_WIKI_SYSTEM:
				rows.append((("ctrl", "alt", "mouse_left"), localeInfo.TOOLTIP_SHORTCUT_WIKI))

