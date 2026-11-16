// bool LoadLocaleData(const char *localePath) icinde:
// Ara:
		TraceError("LoadLocaleData - LoadNPCWearItem(%s) Error", szNPCWearItem);
		return false;
	}

// Altina ekle:
#ifdef ENABLE_WIKI_SYSTEM
	CPythonWiki::Instance().ReadData(localePath);
#endif

