# InventoryWindow.SelectItemSlot icinde ara:
			return
		itemSlotIndex = self.__InventoryLocalSlotPosToGlobalSlotPos(itemSlotIndex)

# Altina ekle:
		if (app.ENABLE_WIKI_SYSTEM and self.interface and
			(app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL)) and
			(app.IsPressed(app.DIK_LALT) or app.IsPressed(app.DIK_RALT)) and
			not mouseModule.mouseController.isAttached()):


# InventoryWindow.SelectItemSlot icinde ara:
			itemVnum = player.GetItemIndex(itemSlotIndex)
			if itemVnum:

# Altina ekle:
				self.interface.SearchWikiForItem(itemVnum)


# InventoryWindow icinde ara:
				return
			net.SendItemSellPacket(itemVNum)

# Altina ekle:
	def BindWikiWindow(self, wndWiki):
		self.wndWiki = wndWiki

