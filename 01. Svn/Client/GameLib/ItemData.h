// Ara:
		BOOL IsFlag(DWORD dwFlag) const;
		BOOL IsWearableFlag(DWORD dwFlag) const;
		BOOL HasNextGrade() const;

// Altina ekle:
#if defined(ENABLE_WIKI_SYSTEM) || defined(INSIDE_RENDER)
		WORD GetRefinedSet() const;
		WORD GetRefinedVnum() const;
#endif

