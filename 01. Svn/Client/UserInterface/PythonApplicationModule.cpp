// void initapp() icinde:
// Ara:
	PyModule_AddIntConstant(poModule, "ENABLE_SKILL_COLOR_SYSTEM", 0);

// Altina ekle:
#ifdef ENABLE_WIKI_SYSTEM
	PyModule_AddIntConstant(poModule, "ENABLE_WIKI_SYSTEM", 1);
#else
	PyModule_AddIntConstant(poModule, "ENABLE_WIKI_SYSTEM", 0);
#endif

