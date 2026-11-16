// Ara:
		// Position
		const D3DXVECTOR3&	GetMovementVectorRef();
		const D3DXVECTOR3&	GetPositionVectorRef();

// Altina ekle:
#if defined(ENABLE_WIKI_SYSTEM) || defined(INSIDE_RENDER)
		std::vector<CGrannyLODController*>& GetLODController() { return m_LODControllerVector; }
#endif


// Ara:
		void		SetWeaponTraceTexture(const char * szTextureName);
		void		UseTextureWeaponTrace();
		void		UseAlphaWeaponTrace();

// Altina ekle:
#if defined(ENABLE_WIKI_SYSTEM) || defined(INSIDE_RENDER)
		void		RenderAllAttachingEffectWiki();
#endif

