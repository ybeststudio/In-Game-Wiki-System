// Ara:
	protected:
		float m_fParticleScale;
		D3DXVECTOR3 m_v3MeshScale;

// Altina ekle:
#ifdef ENABLE_WIKI_SYSTEM
	public:
		void SetWikiIgnoreFrustum(bool flag) { m_wikiIgnoreFrustum = flag; }
	
	protected:
		bool m_wikiIgnoreFrustum;
#endif

