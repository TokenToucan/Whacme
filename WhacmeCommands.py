import Tkinter as tk
import os
import subprocess

class WhacmeCommands():

	def __init__(self, owner):
		self.owner = owner
		self.setBindings()

	def setBindings(self):
		# The <<PasteSelection>> must be bound to a break in order to allow middle clicking without pasting
		# For event-orient commands, add a binding here. Most should be added to the commandClick function.
		
		self.owner.tag.text.bind('<Button>', self.commandClick)
		self.owner.tag.text.bind('<<PasteSelection>>', lambda e: 'break')
		self.owner.tag.text.bind('<<Modified>>', self.modified)
		
		self.owner.mainText.text.bind('<Button>', self.commandClick)
		self.owner.mainText.text.bind('<<PasteSelection>>', lambda e: 'break')
		self.owner.mainText.text.bind('<<Modified>>', self.modified)
		
		self.owner.sideText.text.bind('<Button>', self.commandClick)
		self.owner.sideText.text.bind('<<PasteSelection>>', lambda e: 'break')
		self.owner.sideText.text.bind('<<Modified>>', self.modified)

	def commandClick(self, event):
		cmd = self.getCommand(event)

		# exit on empty clicks or the left button
		if cmd == '':
			return
		if event.num == 1:
			return	
	
		if event.num == 2:
			self.runCommand(cmd)
		elif event.num == 3:
			self.openLocation(cmd)
	
	def getCommand(self, event):
		mouseIndex = event.widget.index('@%s,%s' % (event.x, event.y))

		# selection indices inside the tag
		select = False
		try:
			sStart = event.widget.index('sel.first')
			sEnd = event.widget.index('sel.last')
			select = True
		except Exception, e:
			pass

		# if there is a selection, use that, otherwise just the word (= block of nonwhitespace characters)
		if select:
			lIndex = sStart
			rIndex = sEnd
		else:
			line = int(mouseIndex.split('.')[0])
			left = int(mouseIndex.split('.')[1])
			right = int(mouseIndex.split('.')[1]) + 1
			lEnd = int(event.widget.index('%s lineend' % mouseIndex).split('.')[1])

			lChar = event.widget.get('%s.%s' % (line, left - 1), '%s.%s' % (line, left))
			rChar = event.widget.get('%s.%s' % (line, right), '%s.%s' % (line, right + 1))

			while (left >= 0) and (not lChar.isspace()):
				left -= 1
				lChar = event.widget.get('%s.%s' % (line, left - 1), '%s.%s' % (line, left))
			while (right <= lEnd) and (not rChar.isspace()):
				right += 1
				rChar = event.widget.get('%s.%s' % (line, right), '%s.%s' % (line, right + 1))

			lIndex = '%s.%s' % (line, left)
			rIndex = '%s.%s' % (line, right)
		
		return event.widget.get(lIndex, rIndex)
	
	def modified(self, event):
		# turn on the indicator at the upper left
		self.owner.tk.call(event.widget, 'edit', 'modified', 0)
		self.owner.tag.indicator.configure(bg=self.owner.editedColor)
		
		# clear highlighted things (done by Find etc.)
		self.owner.tag.text.tag_remove('highlightText', '1.0', 'end')
		self.owner.mainText.text.tag_remove('highlightText', '1.0', 'end')
		self.owner.sideText.text.tag_remove('highlightText', '1.0', 'end')

	def openLocation(self, loc):
		# if we currently have a file as the path, back up before working 
		if os.path.isfile(self.owner.path):
			self.owner.path = os.path.dirname(self.owner.path)

		if not loc[0] == '/':
			self.owner.path = os.path.realpath(self.owner.path + '/' + loc)
		else:
			self.owner.path = os.path.realpath(loc)
		
		if os.path.isdir(self.owner.path):
			# put the directory listing in the side area
			self.owner.sideText.text.delete('1.0', 'end')
			self.owner.sideText.text.insert('1.0', subprocess.check_output("ls -F " + self.owner.path, shell=True))
			self.owner.sideText.text.insert('1.0', '..\n')
		else:
			# load the file in main - it is fine if it doesn't exist, since it will be created later when saving it
			try:
				inFile = open(self.owner.path, 'r')
				self.owner.mainText.text.delete('1.0', 'end')
				self.owner.mainText.text.insert('1.0', inFile.read())
			except IOError as e:
				pass
			
			# display the directory on the side
			self.owner.sideText.text.delete('1.0', 'end')
			self.owner.sideText.text.insert('1.0', subprocess.check_output("ls -F " + os.path.dirname(self.owner.path), shell=True))
			self.owner.sideText.text.insert('1.0', '..\n')

		# then update the path displayed in the tag
		lEnd = int(self.owner.tag.text.index('1.0 lineend').split('.')[1])
		right = 1
		rChar = self.owner.tag.text.get('1.0', '1.1')
		while (right <= lEnd) and (not rChar.isspace()):
			right += 1
			rChar = self.owner.tag.text.get('1.%s' % right, '1.%s' % (right + 1))
		self.owner.tag.text.delete('1.0', '1.%s' % right)
		self.owner.tag.text.insert('1.0', self.owner.path)