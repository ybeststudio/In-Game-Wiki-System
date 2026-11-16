# Window.__init__ icinde ara:
		if app.ENABLE_RENEWAL_QUEST:
			self.propertyList = {}

# Altina ekle:
		if app.ENABLE_WIKI_SYSTEM:
			self.itsRendered = FALSE
			self.itsNeedDoubleRender = FALSE
			self.sortIndex = 0


# RenderTarget.__init__ icinde ara:
		def __init__(self, layer = "UI"):
			Window.__init__(self, layer)

# Altina ekle:
			if app.ENABLE_WIKI_SYSTEM:
				self.eventDict = {}
				self.eventFunc = {"mouse_click" : None, "mouse_over_in" : None, "mouse_over_out" : None}
				self.eventArgs = {"mouse_click" : None, "mouse_over_in" : None, "mouse_over_out" : None}


# RenderTarget.Destroy icinde ara:
		def Destroy(self):

# Altina ekle:
			if app.ENABLE_WIKI_SYSTEM:
				self.eventDict = {}
				self.eventFunc = 0
				self.eventArgs = 0


# RenderTarget icinde ara:
		def SetRenderTarget(self, number):
			wndMgr.SetRenderTarget(self.hWnd, number)

# Altina ekle:
		if app.ENABLE_WIKI_SYSTEM:
			def SetRenderingRect(self, left, top, right, bottom):
				wndMgr.SetRenderingRect(self.hWnd, left, top, right, bottom)

			def SetEvent(self, func, *args):
				self.eventFunc[args[0]] = func
				self.eventArgs[args[0]] = args

			def OnMouseLeftButtonUp(self) :
				if self.eventFunc["mouse_click"] :
					apply(self.eventFunc["mouse_click"], self.eventArgs["mouse_click"])

			def OnMouseOverIn(self):
				try:
					if self.eventFunc["mouse_over_in"]:
						if self.eventArgs:
							apply(self.eventFunc["mouse_over_in"], self.eventArgs["mouse_over_in"])
						else:
							self.eventFunc["mouse_over_in"]()
				except KeyError:
					pass

			def OnMouseOverOut(self):
				try:
					if self.eventFunc["mouse_over_out"]:
						if self.eventArgs:
							apply(self.eventFunc["mouse_over_out"], self.eventArgs["mouse_over_out"])
						else:
							self.eventFunc["mouse_over_out"]()
				except KeyError:
					pass


# Dosyanin uygun bir yerine ekle:
if app.ENABLE_WIKI_SYSTEM:
	class Grid:
		def __init__(self, width, height):
			self.width = width
			self.height = height
			self.reset()

		def find_blank(self, width, height):
			if width > self.width or height > self.height:
				return -1

			for row in range(self.height):
				for col in range(self.width):
					index = row * self.width + col
					if self.is_empty(index, width, height):
						return index
			return -1

		def put(self, pos, width, height):
			if not self.is_empty(pos, width, height):
				return FALSE

			for row in range(height):
				start = pos + (row * self.width)
				self.grid[start] = TRUE
				col = 1

				while col < width:
					self.grid[start + col] = TRUE
					col += 1

			return TRUE

		def clear(self, pos, width, height):
			if pos < 0 or pos >= (self.width * self.height):
				return

			for row in range(height):
				start = pos + (row * self.width)
				self.grid[start] = TRUE
				col = 1

				while col < width:
					self.grid[start + col] = FALSE
					col += 1

		def is_empty(self, pos, width, height):
			if pos < 0:
				return FALSE
			row = pos // self.width
			if (row + height) > self.height:
				return FALSE

			if (pos + width) > ((row * self.width) + self.width):
				return FALSE

			for row in range(height):
				start = pos + (row * self.width)
				if self.grid[start]:
					return FALSE
				col = 1

				while col < width:
					if self.grid[start + col]:
						return FALSE
					col += 1

			return TRUE

		def get_size(self):
			return self.width * self.height

		def reset(self):
			self.grid = [FALSE] * (self.width * self.height)

