# RuneData icinde ara:
		_RUNE_DATA = []
		try:

# Altina ekle:
			import wikicontent
			for r in wikicontent.LoadCommonJson("config_json/mount_runes.json")["runes"]:
				levels = []
				for l in r["levels"]:
					levels.append((tuple((m["vnum"], m["count"]) for m in l["materials"]), l["cost"], l["prob"], l["blessing"], l["bonuses"][0]["value"]))
				_RUNE_DATA.append(levels)

