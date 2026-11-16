# BlessingToolTip.SetBlessing icinde ara:
		if app.ENABLE_IKASHOP_RENEWAL:
			rows.append((("ctrl", "mouse_right"), localeInfo.TOOLTIP_SHORTCUT_SHOP_SEARCH))

# Altina ekle:
		if app.ENABLE_WIKI_SYSTEM:
			rows.append((("ctrl", "alt", "mouse_left"), localeInfo.TOOLTIP_SHORTCUT_WIKI))


# SkillPage.__init__ icinde ara:
		self.donationLogButton = _Button(self, PAGE_2 + "donation_log", 68, 30)
		self.donationLogButton.SetEvent(lambda arg = wnd : arg.owner.OpenLog(LOG_DONATION))

# Altina ekle:
		if app.ENABLE_WIKI_SYSTEM:
			self.wikiButton = ui.Button()
			self.wikiButton.SetParent(self)
			self.wikiButton.SetUpVisual(WIKI_BUTTON + "norm.png")
			self.wikiButton.SetOverVisual(WIKI_BUTTON + "hover.png")
			self.wikiButton.SetDownVisual(WIKI_BUTTON + "down.png")
			self.wikiButton.SetPosition(92, 29)
			self.wikiButton.SetEvent(lambda arg = wnd : arg.OnClickWiki())
			self.wikiButton.Show()


# SkillPage.OnClickWiki icinde ara:
		interface = constInfo.GetInterfaceInstance()
		if interface:

# Altina ekle:
			interface.OpenWikiWindow()


# SkillPage.OnOverInDonation icinde ara:
		if app.ENABLE_IKASHOP_RENEWAL:
			rows.append((("ctrl", "mouse_right"), localeInfo.TOOLTIP_SHORTCUT_SHOP_SEARCH))

# Altina ekle:
		if app.ENABLE_WIKI_SYSTEM:
			rows.append((("ctrl", "alt", "mouse_left"), localeInfo.TOOLTIP_SHORTCUT_WIKI))


# ShopPage.OnOverInItem icinde ara:
			rows.append((("ctrl", "mouse_right"), localeInfo.TOOLTIP_SHORTCUT_SHOP_SEARCH))
		rows.append((("ctrl", "mouse_left"), localeInfo.TOOLTIP_SHORTCUT_MULTI_BUY))

# Altina ekle:
		if app.ENABLE_WIKI_SYSTEM:
			rows.append((("ctrl", "alt", "mouse_left"), localeInfo.TOOLTIP_SHORTCUT_WIKI))

