// Dosyanin uygun bir yerine ekle:
#ifdef ENABLE_WIKI_SYSTEM
	#include "PythonWiki.h"
#endif


// Ara:
		CRenderTargetManager m_kRenderTargetManager;

// Altina ekle:
#ifdef ENABLE_WIKI_SYSTEM
		CPythonWiki m_pyWiki;
#endif

