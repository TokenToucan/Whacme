import Tkinter as tk

ALL = 'nsew'

class WhacmeText(tk.Frame):

	def __init__(self, window, color, darkColor, highlightColor, outlineColor, decorationWidth, isTag, text=''):

		tk.Frame.__init__(self, window)

		self.window = window
		self.isTag = isTag
		
		self.color = color
		self.darkColor = darkColor
		self.highlightColor = highlightColor
		
		# set up the columns (space for scrollbar + resizing)
		self.columnconfigure(0, minsize=decorationWidth)
		self.columnconfigure(1, weight=1)
		self.rowconfigure   (0, weight=1)
		
		self.text = tk.Text(self, background=color, relief=tk.FLAT, width=1, height=2, highlightbackground=outlineColor, undo=True, autoseparators=True, maxundo=-1, selectbackground=highlightColor, inactiveselectbackground=highlightColor, yscrollcommand=self.drawScrollbar)
		self.text.grid(row=0, column=1, sticky=ALL)
		self.text.insert('1.0', text)

		if isTag:
			self.indicator = tk.Canvas(self, background=darkColor, height=1, width=decorationWidth, highlightbackground=outlineColor)
			self.indicator.grid(row=0, column=0, sticky=ALL)
		else:
			self.scrollBar       = tk.Canvas(self, bg=darkColor, width=decorationWidth, highlightbackground=outlineColor)
			self.scrollIndicator = self.scrollBar.create_rectangle(0, 0, self.scrollBar.winfo_width(), self.scrollBar.winfo_height(), fill=color)
			self.scrollBar.grid(row=0, column=0, sticky=ALL)
		
	def drawScrollbar(self, a, b):
		if not self.isTag:
			self.scrollBar.delete(self.scrollIndicator)

			try:
				# get sizes (in pixels) to proportion the scrollbar
				fileHeight = self.tk.call(self.text, 'count', '-ypixels', '1.0', 'end')
				boxHeight  = self.text.winfo_height()
				boxLoc     = self.tk.call(self.text, 'count', '-ypixels', '1.0', self.text.index('@0,0'))

				scrollHeight = self.scrollBar.winfo_height()
				barLoc = scrollHeight * boxLoc / fileHeight
				barHeight = scrollHeight * boxHeight / fileHeight

				self.scrollIndicator = self.scrollBar.create_rectangle(0, barLoc, self.scrollBar.winfo_width(), barLoc + barHeight, fill=self.color)
			except ZeroDivisionError:
				pass