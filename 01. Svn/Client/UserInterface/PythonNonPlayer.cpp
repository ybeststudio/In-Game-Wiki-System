// Dosyanin uygun bir yerine ekle:
#ifdef ENABLE_WIKI_SYSTEM
	#include "PythonWiki.h"
#endif


// bool CPythonNonPlayer::LoadNonPlayerData(const char *c_szFileName) icinde:
// Ara:
		TraceError("CPythonNonPlayer::LoadNonPlayerData: invalid size %u check data format.", zObj.GetSize());
		return false;
	}

// Altina ekle:
#ifdef ENABLE_WIKI_SYSTEM
	CPythonWiki::Instance().ClearData();
#endif


// bool CPythonNonPlayer::LoadNonPlayerData(const char *c_szFileName) icinde:
// Ara:
	{
		TMobTable * pNonPlayerData = new TMobTable;
		memcpy(pNonPlayerData, pTable, sizeof(TMobTable));

// Altina ekle:
#ifdef ENABLE_WIKI_SYSTEM
		CPythonWiki::Instance().LoadMonster(pNonPlayerData);
#endif


// bool CPythonNonPlayer::LoadNonPlayerData(const char *c_szFileName) icinde:
// Ara:
		m_NonPlayerDataMap.insert(TNonPlayerDataMap::value_type(pNonPlayerData->dwVnum, pNonPlayerData));
	}

// Altina ekle:
#ifdef ENABLE_WIKI_SYSTEM
	CPythonWiki::Instance().ListReverse();
#endif


// Ara:
	}
	return true;
}

// Altina ekle:
#ifdef ENABLE_WIKI_SYSTEM
DWORD CPythonNonPlayer::GetMonsterPrice1(DWORD dwVnum)
{
	const CPythonNonPlayer::TMobTable* c_pTable = GetTable(dwVnum);
	if (!c_pTable)
		return 0;

	return c_pTable->dwGoldMin;
}

DWORD CPythonNonPlayer::GetMonsterPrice2(DWORD dwVnum)
{
	const CPythonNonPlayer::TMobTable* c_pTable = GetTable(dwVnum);
	if (!c_pTable)
		return 0;

	return c_pTable->dwGoldMax;
}

char CPythonNonPlayer::GetMonsterResist(DWORD dwVnum, BYTE byResist)
{
	if (byResist >= MOB_RESISTS_MAX_NUM)
		return 0;

	const CPythonNonPlayer::TMobTable* c_pTable = GetTable(dwVnum);
	if (!c_pTable)
		return 0;

	return c_pTable->cResists[byResist];
}

DWORD CPythonNonPlayer::GetMonsterMaxHP(DWORD dwVnum)
{
	const CPythonNonPlayer::TMobTable* c_pTable = GetTable(dwVnum);
	if (!c_pTable)
	{
		DWORD dwMaxHP = 0;
		return dwMaxHP;
	}

	return c_pTable->dwMaxHP;
}

DWORD CPythonNonPlayer::GetMonsterRaceFlag(DWORD dwVnum)
{
	const CPythonNonPlayer::TMobTable* c_pTable = GetTable(dwVnum);
	if (!c_pTable)
	{
		DWORD dwRaceFlag = 0;
		return dwRaceFlag;
	}

	return c_pTable->dwRaceFlag;
}

DWORD CPythonNonPlayer::GetMonsterLevel(DWORD dwVnum)
{
	const CPythonNonPlayer::TMobTable* c_pTable = GetTable(dwVnum);
	if (!c_pTable)
	{
		DWORD level = 0;
		return level;
	}

	return c_pTable->bLevel;
}

DWORD CPythonNonPlayer::GetMonsterDamage1(DWORD dwVnum)
{
	const CPythonNonPlayer::TMobTable* c_pTable = GetTable(dwVnum);
	if (!c_pTable)
	{
		DWORD range = 0;
		return range;
	}

	return c_pTable->dwDamageRange[0];
}

DWORD CPythonNonPlayer::GetMonsterDamage2(DWORD dwVnum)
{
	const CPythonNonPlayer::TMobTable* c_pTable = GetTable(dwVnum);
	if (!c_pTable)
	{
		DWORD range = 0;
		return range;
	}

	return c_pTable->dwDamageRange[1];
}

DWORD CPythonNonPlayer::GetMonsterExp(DWORD dwVnum)
{
	const CPythonNonPlayer::TMobTable* c_pTable = GetTable(dwVnum);
	if (!c_pTable)
	{
		DWORD dwExp = 0;
		return dwExp;
	}

	return c_pTable->dwExp;
}

float CPythonNonPlayer::GetMonsterDamageMultiply(DWORD dwVnum)
{
	const CPythonNonPlayer::TMobTable* c_pTable = GetTable(dwVnum);
	if (!c_pTable)
	{
		DWORD fDamMultiply = 0;
		return fDamMultiply;
	}

	return c_pTable->fDamMultiply;
}

DWORD CPythonNonPlayer::GetMonsterST(DWORD dwVnum)
{
	const CPythonNonPlayer::TMobTable* c_pTable = GetTable(dwVnum);
	if (!c_pTable)
	{
		DWORD bStr = 0;
		return bStr;
	}

	return c_pTable->bStr;
}

DWORD CPythonNonPlayer::GetMonsterDX(DWORD dwVnum)
{
	const CPythonNonPlayer::TMobTable* c_pTable = GetTable(dwVnum);
	if (!c_pTable)
	{
		DWORD bDex = 0;
		return bDex;
	}

	return c_pTable->bDex;
}

bool CPythonNonPlayer::IsMonsterStone(DWORD dwVnum)
{
	const CPythonNonPlayer::TMobTable* c_pTable = GetTable(dwVnum);
	if (!c_pTable)
	{
		return 0;
	}

	return c_pTable->bType == 2;
}
#endif

