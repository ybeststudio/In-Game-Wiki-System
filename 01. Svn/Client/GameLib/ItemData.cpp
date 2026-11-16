// Ara:
CItemData::~CItemData()
{
}

// Altina ekle:
#if defined(ENABLE_WIKI_SYSTEM) || defined(INSIDE_RENDER)
WORD CItemData::GetRefinedSet() const
{
	return m_ItemTable.wRefineSet;
}

WORD CItemData::GetRefinedVnum() const
{
	return m_ItemTable.dwRefinedVnum;
}
#endif

