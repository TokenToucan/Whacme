import WhacmeCommands
import WhacmeText
import Tkinter as tk
import os

ALL = 'nsew'

class WhacmeWindow(tk.Frame):
	
	# window id
	id = 0

	def __init__(self, parent,                                                                                                 \
			path=os.path.expanduser('~'), cmdClass=WhacmeCommands.WhacmeCommands,                                              \
			mainWeight=2, mainColor='#ffffea', mainDarkColor='#99994c', mainHighlightColor='#eeee9e',                          \
			sideWeight=1, sideColor='#eaffea', sideDarkColor='#4c994c', sideHighlightColor='#9eee9e',                          \
			               tagColor='#eaffff',  tagDarkColor='#8888cc',  tagHighlightColor='#9eeeee', tagEditedColor='#000099',\
			tagText='Save Undo Redo | Find \nHaskell Python LaTeX | Apply ',                                                  \
			borderColor='#000000', scrollWidth=12,                                                                             \
			*args, **kwargs):

		tk.Frame.__init__(self, parent, *args, **kwargs)
		
		self.parent = parent
		self.path = os.path.abspath(path)

		# set and increment the id
		self.id = WhacmeWindow.id
		WhacmeWindow.id += 1

		# set the window layout
		self.columnconfigure(0, weight=mainWeight)
		self.columnconfigure(1, weight=sideWeight)
		self.rowconfigure   (0, weight=0)
		self.rowconfigure   (1, weight=1)

		# set the notification for editing
		self.editedColor = tagEditedColor
		
		# build the text areas
		self.tag      = WhacmeText.WhacmeText(window=self, color= tagColor, darkColor=tagDarkColor,  highlightColor=tagHighlightColor,  outlineColor=borderColor, isTag=True,  decorationWidth=scrollWidth, text='  ' +tagText)
		self.mainText = WhacmeText.WhacmeText(window=self, color=mainColor, darkColor=mainDarkColor, highlightColor=mainHighlightColor, outlineColor=borderColor, isTag=False, decorationWidth=scrollWidth)
		self.sideText = WhacmeText.WhacmeText(window=self, color=sideColor, darkColor=sideDarkColor, highlightColor=sideHighlightColor, outlineColor=borderColor, isTag=False, decorationWidth=scrollWidth)
		
		# grid each of the areas now
		self.tag.grid     (row=0, column=0, sticky=ALL, columnspan=2)
		self.mainText.grid(row=1, column=0, sticky=ALL)
		self.sideText.grid(row=1, column=1, sticky=ALL)

		# set up the command object for the window - this allows customization of the options available
		self.cmd = cmdClass(self)
		
		# finally, open up whatever we've been sent as a path
		self.cmd.openLocation(path)

