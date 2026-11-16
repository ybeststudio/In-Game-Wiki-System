// Ara:
		return Py_BuildException();
	return Py_BuildValue("s", pItemData->GetName());
}

// Altina ekle:
#ifdef ENABLE_WIKI_SYSTEM
PyObject *itemGetRefineSet(PyObject *poSelf, PyObject *poArgs)
{
	CItemData* pItemData = CItemManager::Instance().GetSelectedItemDataPointer();
	if (!pItemData)
		return Py_BuildException("Can't find select item data");
	return Py_BuildValue("i", pItemData->GetRefinedSet());
}

PyObject *itemGetRefinedVnum(PyObject *poSelf, PyObject *poArgs)
{
	CItemData* pItemData = CItemManager::Instance().GetSelectedItemDataPointer();
	if (!pItemData)
		return Py_BuildException("Can't find select item data");
	return Py_BuildValue("i", pItemData->GetRefinedVnum());
}

PyObject *itemSelectItemWiki(PyObject *poSelf, PyObject *poArgs)
{
	int iIndex;
	if (!PyTuple_GetInteger(poArgs, 0, &iIndex))
		return Py_BadArgument();
	if (!CItemManager::Instance().SelectItemData(iIndex))
		return Py_BuildValue("i", 0);
	return Py_BuildValue("i", 1);
}
#endif


// void initItem() icinde:
// Ara:
		{ "LoadItemTable",					itemLoadItemTable,						METH_VARARGS },
		{ "IsWeddingItem",					itemIsWeddingItem,						METH_VARARGS },
		{ "GetItemNameByVnum",				itemGetItemNameByVnum,					METH_VARARGS },

// Altina ekle:
#ifdef ENABLE_WIKI_SYSTEM
		{ "SelectItemWiki",					itemSelectItemWiki,						METH_VARARGS },
		{ "GetRefineSet",					itemGetRefineSet,						METH_VARARGS },
		{ "GetRefinedVnum",					itemGetRefinedVnum,						METH_VARARGS },
#endif

