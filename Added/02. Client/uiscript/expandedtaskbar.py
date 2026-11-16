if __USE_DYNAMIC_MODULE__:
	import pyapi

app = __import__(pyapi.GetModuleName("app"))

import uiScriptLocale


EXPANDED_BTN = "d:/ymir work/ui/game/taskbar/expanded_btn/"
BUTTON_SIZE = 37

def MakeButton(name, tooltip, default_image, over_image, down_image):
	return {
		"name" : name,
		"type" : "button",
		"style" : ("ltr", ),

		"x" : 0,
		"y" : 0,

		"width" : BUTTON_SIZE,
		"height" : BUTTON_SIZE,

		"tooltip_text" : tooltip,

		"default_image" : default_image,
		"over_image" : over_image,
		"down_image" : down_image,
	}

def MakeShortcutButton(name, tooltip, icon):
	return MakeButton(name, tooltip,
		EXPANDED_BTN + icon + "_norm.png",
		EXPANDED_BTN + icon + "_hover.png",
		EXPANDED_BTN + icon + "_select.png")

buttons = []

if app.ENABLE_RENEWAL_SWITCHBOT:
	buttons.append(MakeShortcutButton("SwitchbotButton", uiScriptLocale.TASKBAR_SWITCHBOT, "btn_sb"))

if app.ENABLE_WIKI_SYSTEM:
	buttons.append(MakeShortcutButton("WikiButton", uiScriptLocale.TASKBAR_WIKI, "btn_wiki"))

if app.ENABLE_GROWTH_PET_SYSTEM:
	buttons.append(MakeShortcutButton("PetInfoButton", uiScriptLocale.TASKBAR_PET_INFO, "btn_companion"))

if app.ENABLE_HUNTING_SYSTEM:
	buttons.append(MakeShortcutButton("HuntingButton", uiScriptLocale.TASKBAR_HUNTING_QUESTS, "btn_guide"))

if app.__AUTO_HUNT__:
	buttons.append(MakeButton("AutoButton", uiScriptLocale.TASKBAR_AUTO_HUNT,
		EXPANDED_BTN + "pvp_button_norm.png",
		EXPANDED_BTN + "pvp_button_hover.png",
		EXPANDED_BTN + "pvp_button_select.png"))

window = {
	"name" : "ExpandTaskBar",
	"style" : ("ltr", ),

	"x" : SCREEN_WIDTH/2 - (BUTTON_SIZE * len(buttons)) / 2,
	"y" : SCREEN_HEIGHT - 74,

	"width" : BUTTON_SIZE * len(buttons),
	"height" : BUTTON_SIZE,

	"children" :
	(
		{
			"name" : "ExpanedTaskBar_Board",
			"type" : "window",
			"style" : ("ltr", ),

			"x" : 0,
			"y" : 0,

			"width" : BUTTON_SIZE * len(buttons),
			"height" : BUTTON_SIZE,

			"children" : tuple(buttons),
		},
	),
}
