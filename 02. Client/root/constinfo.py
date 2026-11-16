# Ara:
		del _interface_instance
	_interface_instance = instance

# Altina ekle:
if app.ENABLE_WIKI_SYSTEM:
	_main_wiki_instance = None
	_listbox_wiki_instance = None
	def SetMainParent(instance):
		global _main_wiki_instance
		if _main_wiki_instance:
			del _main_wiki_instance
		_main_wiki_instance = instance
	def GetMainParent():
		global _main_wiki_instance
		return _main_wiki_instance
	def SetListBox(instance):
		global _listbox_wiki_instance
		if _listbox_wiki_instance:
			del _listbox_wiki_instance
		_listbox_wiki_instance = instance
	def GetListBox():
		global _listbox_wiki_instance
		return _listbox_wiki_instance
	def IS_SET(value, flag):
		return (value & flag) == flag

