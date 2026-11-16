// Bul:
					if (!InFrustum(*itor))

// Degistir:
#if defined(ENABLE_RENDER_TARGET) && defined(ENABLE_WIKI_SYSTEM)
					if (!InFrustum(*itor) && !m_wikiIgnoreFrustum && !m_ignoreFrustum)
#elif defined(ENABLE_RENDER_TARGET)
					if (!InFrustum(*itor) && !m_ignoreFrustum)
#elif defined(ENABLE_WIKI_SYSTEM)
					if (!InFrustum(*itor) && !m_wikiIgnoreFrustum)
#else
					if (!InFrustum(*itor))
#endif

