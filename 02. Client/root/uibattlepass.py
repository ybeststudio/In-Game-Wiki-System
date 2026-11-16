# LoadConfig icinde ara:
def LoadConfig():
	try:

# Altina ekle:
		import wikicontent
		return wikicontent.LoadCommonJson(CONFIG_PATH) or {}

