// Ara:
	for (const auto& it : m_AttachingEffectList)
		CEffectManager::Instance().RenderOne(it.dwEffectIndex);
}

// Altina ekle:
#if defined(ENABLE_WIKI_SYSTEM) || defined(INSIDE_RENDER)
void CActorInstance::RenderAllAttachingEffectWiki()
{
	for (const auto& it : m_AttachingEffectList)
		CEffectManager::Instance().RenderOneWiki(it.dwEffectIndex);
}
#endif

