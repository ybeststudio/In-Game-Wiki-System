// Ara:
		BOOL SelectItemData(DWORD dwIndex);
		CItemData *GetSelectedItemDataPointer();
		BOOL GetItemDataPointer(DWORD dwItemID, CItemData ** ppItemData);

// Altina ekle:
#if defined(ENABLE_WIKI_SYSTEM) || defined(INSIDE_RENDER) || defined(ENABLE_RENEWAL_OFFLINESHOP)
		TItemMap GetItems() const { return m_ItemMap; }
#endif

