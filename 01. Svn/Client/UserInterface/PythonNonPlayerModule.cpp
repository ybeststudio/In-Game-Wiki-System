// Ara:
	CPythonNonPlayer& rkNonPlayer = CPythonNonPlayer::Instance();
	return Py_BuildValue("b", rkNonPlayer.MonsterHasRaceFlag(iVNum, szRaceFlag));
}

// Altina ekle:
#ifdef ENABLE_WIKI_SYSTEM
PyObject *nonPlayerGetMobsByName(PyObject *poSelf, PyObject *poArgs)
{
	char *szItemName;
	if (!PyTuple_GetString(poArgs, 0, &szItemName))
		return Py_BadArgument();

	CPythonNonPlayer::TNonPlayerDataMap m_vec_MonsterRange = CPythonNonPlayer::Instance().GetMonsterData();
	int n = m_vec_MonsterRange.size();
	std::string searchedFileName(szItemName);
	PyObject *poList = PyList_New(0);

	CPythonNonPlayer::TNonPlayerDataMap::iterator i;
	for (i = m_vec_MonsterRange.begin(); i != m_vec_MonsterRange.end(); ++i)
	{
		CPythonNonPlayer::TMobTable* p = i->second;
		if (p->bType == 0 || p->bType == 2)
		{
			if (p)
			{
				std::string tempFileName(p->szLocaleName);
				std::transform(tempFileName.begin(), tempFileName.end(), tempFileName.begin(), [](unsigned char c) { return std::tolower(c); });
				if (tempFileName.compare(0, searchedFileName.length(), searchedFileName) == 0)
				{
					PyObject *poItemVnum = PyInt_FromLong(p->dwVnum);
					PyList_Append(poList, poItemVnum);
				}
			}
		}
	}

	return Py_BuildValue("O", poList);
}

PyObject *nonplayerGetMonsterPrice(PyObject *poSelf, PyObject *poArgs)
{
	int race;
	if (!PyTuple_GetInteger(poArgs, 0, &race))
		return Py_BuildException();

	CPythonNonPlayer& rkNonPlayer = CPythonNonPlayer::Instance();

	DWORD price1 = rkNonPlayer.GetMonsterPrice1(race);
	DWORD price2 = rkNonPlayer.GetMonsterPrice2(race);

	return Py_BuildValue("ii", price1, price2);
}

PyObject *nonplayerGetMonsterResist(PyObject *poSelf, PyObject *poArgs)
{
	int race;
	if (!PyTuple_GetInteger(poArgs, 0, &race))
		return Py_BuildException();

	BYTE bResist;
	if (!PyTuple_GetByte(poArgs, 1, &bResist))
		return Py_BuildException();

	CPythonNonPlayer& rkNonPlayer = CPythonNonPlayer::Instance();

	return Py_BuildValue("i", rkNonPlayer.GetMonsterResist(race, bResist));
}

PyObject *nonplayerGetMonsterLevel(PyObject *poSelf, PyObject *poArgs)
{
	int race;
	if (!PyTuple_GetInteger(poArgs, 0, &race))
		return Py_BuildException();

	CPythonNonPlayer& rkNonPlayer = CPythonNonPlayer::Instance();

	return Py_BuildValue("i", rkNonPlayer.GetMonsterLevel(race));
}

PyObject *nonplayerGetMonsterDamage(PyObject *poSelf, PyObject *poArgs)
{
	int race;
	if (!PyTuple_GetInteger(poArgs, 0, &race))
		return Py_BuildException();

	CPythonNonPlayer& rkNonPlayer = CPythonNonPlayer::Instance();

	DWORD dmg1 = rkNonPlayer.GetMonsterDamage1(race);
	DWORD dmg2 = rkNonPlayer.GetMonsterDamage2(race);

	return Py_BuildValue("ii", dmg1, dmg2);
}

PyObject *nonplayerGetMonsterExp(PyObject *poSelf, PyObject *poArgs)
{
	int race;
	if (!PyTuple_GetInteger(poArgs, 0, &race))
		return Py_BuildException();

	CPythonNonPlayer& rkNonPlayer = CPythonNonPlayer::Instance();

	return Py_BuildValue("i", rkNonPlayer.GetMonsterExp(race));
}

PyObject *nonplayerGetMonsterDamageMultiply(PyObject *poSelf, PyObject *poArgs)
{
	int race;
	if (!PyTuple_GetInteger(poArgs, 0, &race))
		return Py_BuildException();

	CPythonNonPlayer& rkNonPlayer = CPythonNonPlayer::Instance();

	return Py_BuildValue("f", rkNonPlayer.GetMonsterDamageMultiply(race));
}

PyObject *nonplayerGetMonsterST(PyObject *poSelf, PyObject *poArgs)
{
	int race;
	if (!PyTuple_GetInteger(poArgs, 0, &race))
		return Py_BuildException();

	CPythonNonPlayer& rkNonPlayer = CPythonNonPlayer::Instance();

	return Py_BuildValue("i", rkNonPlayer.GetMonsterST(race));
}

PyObject *nonplayerGetMonsterDX(PyObject *poSelf, PyObject *poArgs)
{
	int race;
	if (!PyTuple_GetInteger(poArgs, 0, &race))
		return Py_BuildException();

	CPythonNonPlayer& rkNonPlayer = CPythonNonPlayer::Instance();

	return Py_BuildValue("i", rkNonPlayer.GetMonsterDX(race));
}

PyObject *nonplayerIsMonsterStone(PyObject *poSelf, PyObject *poArgs)
{
	int race;
	if (!PyTuple_GetInteger(poArgs, 0, &race))
		return Py_BuildException();

	CPythonNonPlayer& rkNonPlayer = CPythonNonPlayer::Instance();

	return Py_BuildValue("i", rkNonPlayer.IsMonsterStone(race) ? 1 : 0);
}

PyObject *nonplayerGetMonsterRaceFlag(PyObject *poSelf, PyObject *poArgs)
{
	int race;
	if (!PyTuple_GetInteger(poArgs, 0, &race))
		return Py_BuildException();

	CPythonNonPlayer& rkNonPlayer = CPythonNonPlayer::Instance();

	return Py_BuildValue("i", rkNonPlayer.GetMonsterRaceFlag(race));
}

PyObject *nonplayerGetMonsterMaxHP(PyObject *poSelf, PyObject *poArgs)
{
	int race;
	if (!PyTuple_GetInteger(poArgs, 0, &race))
		return Py_BuildException();

	CPythonNonPlayer& rkNonPlayer = CPythonNonPlayer::Instance();

	return Py_BuildValue("i", rkNonPlayer.GetMonsterMaxHP(race));
}
#endif


// void initNonPlayer() icinde:
// Ara:
		{ "MonsterHasRaceFlag",			nonplayerMonsterHasRaceFlag,		METH_VARARGS },

// Altina ekle:
#ifdef ENABLE_WIKI_SYSTEM
		{ "GetMonsterPrice",			nonplayerGetMonsterPrice,			METH_VARARGS },
		{ "GetMobsByName",				nonPlayerGetMobsByName,				METH_VARARGS },
		{ "GetMonsterLevel",			nonplayerGetMonsterLevel,			METH_VARARGS },
		{ "GetMonsterRaceFlag",			nonplayerGetMonsterRaceFlag,		METH_VARARGS },
		{ "IsMonsterStone",				nonplayerIsMonsterStone,			METH_VARARGS },
		{ "GetMonsterDamage",			nonplayerGetMonsterDamage,			METH_VARARGS },
		{ "GetMonsterExp",				nonplayerGetMonsterExp,				METH_VARARGS },
		{ "GetMonsterDamageMultiply",	nonplayerGetMonsterDamageMultiply,	METH_VARARGS },
		{ "GetMonsterST",				nonplayerGetMonsterST,				METH_VARARGS },
		{ "GetMonsterDX",				nonplayerGetMonsterDX,				METH_VARARGS },
		{ "IsMonsterStone",				nonplayerIsMonsterStone,			METH_VARARGS },
		{ "GetMonsterResist",			nonplayerGetMonsterResist,			METH_VARARGS },
		{ "GetMonsterMaxHP",			nonplayerGetMonsterMaxHP,			METH_VARARGS },
#endif


// void initNonPlayer() icinde:
// Ara:
	PyModule_AddIntConstant(poModule, "S_KNIGHT", 3);
	PyModule_AddIntConstant(poModule, "BOSS", 4);
	PyModule_AddIntConstant(poModule, "KING", 5);

// Altina ekle:
#ifdef ENABLE_WIKI_SYSTEM
	PyModule_AddIntConstant(poModule, "MOB_RESIST_SWORD", CPythonNonPlayer::MOB_RESIST_SWORD);
	PyModule_AddIntConstant(poModule, "MOB_RESIST_TWOHAND", CPythonNonPlayer::MOB_RESIST_TWOHAND);
	PyModule_AddIntConstant(poModule, "MOB_RESIST_DAGGER", CPythonNonPlayer::MOB_RESIST_DAGGER);
	PyModule_AddIntConstant(poModule, "MOB_RESIST_BELL", CPythonNonPlayer::MOB_RESIST_BELL);
	PyModule_AddIntConstant(poModule, "MOB_RESIST_FAN", CPythonNonPlayer::MOB_RESIST_FAN);
	PyModule_AddIntConstant(poModule, "MOB_RESIST_BOW", CPythonNonPlayer::MOB_RESIST_BOW);
	PyModule_AddIntConstant(poModule, "MOB_RESIST_FIRE", CPythonNonPlayer::MOB_RESIST_FIRE);
	PyModule_AddIntConstant(poModule, "MOB_RESIST_ELECT", CPythonNonPlayer::MOB_RESIST_ELECT);
	PyModule_AddIntConstant(poModule, "MOB_RESIST_MAGIC", CPythonNonPlayer::MOB_RESIST_MAGIC);
	PyModule_AddIntConstant(poModule, "MOB_RESIST_WIND", CPythonNonPlayer::MOB_RESIST_WIND);
	PyModule_AddIntConstant(poModule, "MOB_RESIST_POISON", CPythonNonPlayer::MOB_RESIST_POISON);
	PyModule_AddIntConstant(poModule, "MOB_RESIST_MAX_NUM", CPythonNonPlayer::MOB_RESISTS_MAX_NUM);
#endif

