// void CEffectElementBaseInstance::Render() icinde:
// Ara:
    if (IsHiddenByLod()

// Altina ekle:
#ifdef ENABLE_WIKI_SYSTEM
        && !m_wikiIgnoreFrustum
#endif


// void CEffectElementBaseInstance::Initialize() icinde:
// Ara:
	m_fLocalTime = 0.0f;
	m_dwStartTime = 0;
	m_fElapsedTime = 0.0f;

// Altina ekle:
#ifdef ENABLE_WIKI_SYSTEM
	m_wikiIgnoreFrustum = false;
#endif

