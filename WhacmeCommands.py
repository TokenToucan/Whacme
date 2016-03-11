import Tkinter as tk
import os
import subprocess

class WhacmeCommands():

	def __init__(self, owner):
		self.owner = owner
		self.setBindings()
		
		self.buttonOneDown = False

	def setBindings(self):
		# The <<PasteSelection>> must be bound to a break in order to allow middle clicking without pasting
		# For event-orient commands, add a binding here. Most should be added to the commandClick function.
		
		
		self.owner.main.text.bind('<Button-2>', self.runCommand)
		self.owner.main.text.bind('<Button-3>', self.openLocation)
		self.owner.tag.text.bind('<<PasteSelection>>', lambda e: 'break')
		self.owner.tag.indicator.bind('<ButtonPress-1>', self.resizeDown)
		self.owner.tag.indicator.bind('<ButtonRelease-1>', self.resizeUp)
		
		self.owner.main.text.bind('<Button-2>', self.runCommand)
		self.owner.main.text.bind('<Button-3>', self.openLocation)
		self.owner.main.text.bind('<<PasteSelection>>', lambda e: 'break')
		self.owner.main.text.bind('<<Modified>>', self.modified)
		
		
		self.owner.main.text.bind('<Button-2>', self.runCommand)
		self.owner.main.text.bind('<Button-3>', self.openLocation)
		self.owner.side.text.bind('<<PasteSelection>>', lambda e: 'break')
	
	def resizeDown(self, event):
		# change the cursor to a box
		event.widget.configure(cursor='dotbox')

		# set initial position for the resize
	
	def resizeUp(self, event):
		# return cursor to normal
		event.widget.configure(cursor='X_cursor')

		# calculate weight changes needed to bring the button under/near the new position
	
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
		self.owner.main.text.tag_remove('highlightText', '1.0', 'end')
		self.owner.side.text.tag_remove('highlightText', '1.0', 'end')

	def openLocation(self, event):
		loc = getCommand(event)
		
		# if we currently have a file as the path, back up before working
		oldPath = self.owner.path
		if os.path.isfile(self.owner.path):
			self.owner.path = os.path.dirname(self.owner.path)

		if not loc[0] == '/':
			self.owner.path = os.path.realpath(self.owner.path + '/' + loc)
		else:
			self.owner.path = os.path.realpath(loc)
		
		if os.path.isdir(self.owner.path):
			# put the directory listing in the side area
			self.owner.side.text.delete('1.0', 'end')
			self.owner.side.text.insert('1.0', subprocess.check_output("ls -F " + self.owner.path, shell=True))
			self.owner.side.text.insert('1.0', '..\n')
		elif os.path.isfile(self.owner.path):
			# load the file in main - it is fine if it doesn't exist, since it will be created later when saving it
			inFile = open(self.owner.path, 'r')
			self.owner.main.text.delete('1.0', 'end')
			self.owner.main.text.insert('1.0', inFile.read())
			
			# display the directory on the side
			self.owner.side.text.delete('1.0', 'end')
			self.owner.side.text.insert('1.0', subprocess.check_output("ls -F " + os.path.dirname(self.owner.path), shell=True))
			self.owner.side.text.insert('1.0', '..\n')
		else:
			# ignore anything else, back up to normal path
			self.owner.path = oldPath

		# then update the path displayed in the tag
		lEnd = int(self.owner.tag.text.index('1.0 lineend').split('.')[1])
		right = 1
		rChar = self.owner.tag.text.get('1.0', '1.1')
		while (right <= lEnd) and (not rChar.isspace()):
			right += 1
			rChar = self.owner.tag.text.get('1.%s' % right, '1.%s' % (right + 1))
		self.owner.tag.text.delete('1.0', '1.%s' % right)
		self.owner.tag.text.insert('1.0', self.owner.path)
	
	def save(self):
		# get the path in the tag - this is if you want to change the filename before saving
		lEnd = int(self.owner.tag.text.index('1.0 lineend').split('.')[1])
		right = 1
		rChar = self.owner.tag.text.get('1.0', '1.1')
		while (right <= lEnd) and (not rChar.isspace()):
			right += 1
			rChar = self.owner.tag.text.get('1.%s' % right, '1.%s' % (right + 1))
		tagPath = os.path.realpath(self.owner.tag.text.get('1.0', '1.%s' % right))
		
		outFile = open(tagPath, 'w')
		errFile = open(tagPath + '+err', 'w')
		
		outFile.write(u'%s' % self.owner.main.text.get('1.0', 'end'))
		errFile.write(u'%s' % self.owner.side.text.get('1.0', 'end'))
		
		self.owner.tag.indicator.configure(bg=self.owner.tag.darkColor)

	def undo(self):
		self.owner.main.text.edit_undo()

	def redo(self):
		self.owner.main.text.edit_redo()
	
	def find(self, args):
		# remove the initial 'Find' keyword to get the search pattern
		pattern = reduce(lambda x,y: x + ' ' + y, args[1:], '')
		
		start = '1.0'
		cnt = tk.IntVar()
		
		# loop through the text and mark what needs to be highlighted
		# TODO: implement scrollbar marking
		while True:
			lIndex = self.owner.main.text.search(pattern, start, stopindex='end', count=cnt)
			rIndex = '%s+%sc' % (lIndex, cnt.get())

			# exit if we do not find anything
			if lIndex == '':
				break
		
			# set highlight tag on the found text
			self.owner.main.text.tag_add('highlightText', lIndex, rIndex)

			# set the new start location
			start = rIndex
		
		# set the highlighting on
		self.owner.main.text.tag_configure('highlightText', background=self.owner.main.highlightColor)

	def haskell(self):
		self.save()
		self.owner.side.text.insert('1.0', '####################\n')
		self.owner.side.text.insert('1.0', subprocess.check_output('runghc ' + self.owner.path, shell=True))
		self.owner.side.text.insert('1.0', '###HASKELL OUTPUT###\n')

	def python(self):
		self.save()
		self.owner.side.text.insert('1.0', '###################\n')
		self.owner.side.text.insert('1.0', subprocess.check_output('python ' + self.owner.path, shell=True))
		self.owner.side.text.insert('1.0', '###PYTHON OUTPUT###\n')

	def latex(self):
		# do not fiddle around if we are not currently working with a file
		if os.path.isdir(self.owner.path):
			return
		
		self.save()
		pdfName = self.owner.path.split('/')[-1].split('.')[0] + '.pdf'
		dirPath = os.path.dirname(self.owner.path)
		pdfPath = dirPath + pdfName

		subprocess.call("mkdir -p /tmp/whacme-pdf/", shell=True)

		self.owner.side.text.insert('1.0', '####################\n')
		latexProc = subprocess.Popen('pdflatex -output-directory=/tmp/whacme-pdf/ -interaction nonstopmode ' + self.owner.path, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

		self.owner.side.text.insert('1.0', latexProc.communicate()[0])
		self.owner.side.text.insert('1.0', '###LATEX OUTPUT###\n')

		try:
			subprocess.call('cp /tmp/whacme-pdf/' + pdfName + ' ' + dirPath + '/' + pdfName, shell=True)
		except subprocess.CalledProcessError, e:
			pass
		else:
			pdfWindow = subprocess.Popen('xdotool search --name ' + pdfName + ' | head -1', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
			if pdfWindow == '':
				subprocess.call('mupdf ' + dirPath + '/' + pdfName + ' &', shell=True)

			pdfWindow = subprocess.Popen('xdotool search --name ' + pdfName + ' | head -1', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
			# peel off trailing newline
			pdfWindow = pdfWindow[:-1]
			subprocess.call('xdotool key --clearmodifiers --window ' + pdfWindow + ' r', shell=True)
	
	def apply(self, args):
		# condense the arguments
		cmd = reduce(lambda x,y: x + ' ' + y, args[1:], '')
		
		# run the command in the shell with the variable
		inText = self.owner.main.text.get('1.0', 'end')
		outText = subprocess.Popen('text=\"' + inText + '\" && ' + cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
		
		self.owner.main.text.delete('1.0', 'end')
		self.owner.main.text.insert('1.0', outText)
	
	def runCommand(self, cmd):
		cmd = self.getCommand(event)

		splitCmd = cmd.split(' ')
		if cmd[0].isupper():
			if   splitCmd[0] == 'Save':
				self.save()
			elif splitCmd[0] == 'Undo':
				self.undo()
			elif splitCmd[0] == 'Redo':
				self.redo()
			elif splitCmd[0] == 'Find':
				self.find(splitCmd)
			elif splitCmd[0] == 'Haskell':
				self.haskell()
			elif splitCmd[0] == 'Python':
				self.python()
			elif splitCmd[0] == 'LaTeX':
				self.latex()
			elif splitCmd[0] == 'Apply':
				self.apply(splitCmd)
		# execute whatever it is, giving it the window id when it is not a special command
		# currently doesn't fork or anything nice, just dumps output into the out box
		else:
			self.owner.side.text.insert('1.0', '##################\n')
			self.owner.side.text.insert('1.0', subprocess.Popen('winid=' + str(self.owner.id) + ' && ' + cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0])
			self.owner.side.text.insert('1.0', '###SHELL OUTPUT###\n')


			