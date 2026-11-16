// bool CEffectInstance::__IsOffscreenOrFar(bool* pbFar) const icinde:
// Ara:
	if (m_ignoreFrustum)
		return false;

// Altina ekle:
#ifdef ENABLE_WIKI_SYSTEM
	if (m_wikiIgnoreFrustum)
		return false;
#endif


// void CEffectInstance::__Initialize() icinde:
// Ara:
	m_isAlive = FALSE;
	m_dwFrame = 0;
	m_bOffscreen = false;

// Altina ekle:
#ifdef ENABLE_WIKI_SYSTEM
	m_wikiIgnoreFrustum = false;
#endif

