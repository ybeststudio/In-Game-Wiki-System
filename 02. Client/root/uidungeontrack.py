# DungeonTrack.__WikiBtn icinde ara:
			interface = constInfo.GetInterfaceInstance()
			if interface:

# Altina ekle:
				interface.wndWiki.Open()
				interface.wndWiki.LoadData(__wikiCommandDict[currentDungeon])
				interface.wndWiki.SetTop()

