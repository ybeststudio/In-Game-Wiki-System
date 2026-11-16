// Ara:
		DWORD GetMonsterType(DWORD dwVnum);
		DWORD GetMonsterRank(DWORD dwVnum);

// Altina ekle:
#ifdef ENABLE_WIKI_SYSTEM
		DWORD GetMonsterPrice1(DWORD dwVnum);
		DWORD GetMonsterPrice2(DWORD dwVnum);
		TNonPlayerDataMap GetMonsterData() {return m_NonPlayerDataMap;}
		char GetMonsterResist(DWORD dwVnum, BYTE byResist);
		DWORD GetMonsterMaxHP(DWORD dwVnum);
		DWORD GetMonsterRaceFlag(DWORD dwVnum);
		DWORD GetMonsterLevel(DWORD dwVnum);
		DWORD GetMonsterDamage1(DWORD dwVnum);
		DWORD GetMonsterDamage2(DWORD dwVnum);
		DWORD GetMonsterExp(DWORD dwVnum);
		float GetMonsterDamageMultiply(DWORD dwVnum);
		DWORD GetMonsterST(DWORD dwVnum);
		DWORD GetMonsterDX(DWORD dwVnum);
		bool IsMonsterStone(DWORD dwVnum);
#endif

