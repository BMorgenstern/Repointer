__author__ = 'Brendor'
'''
Repoint.pyw by Brendan Morgenstern; V 1.1 1/9/16
This is a python file that easily reallocates data tables in a GBA ROM image and updates the pointers to said tables.
All of the repointing data is given from the input nightmare module, which species the default location of the table, length in
bytes of one object, and the number of objects in the array. Upon request, the input nightmare module can be automatically updated
with the new location of the table and the new expanded number of entries. 
If you as the user experience any bugs, or have any questions, I can be contacted at brendanmorgenstern@gmail.com. 
Enjoy.

*Python 2.7 required. 3.x is NOT supported.*
'''
import os, sys, struct
try:
	from Tkinter import *
	import tkMessageBox
	import tkFileDialog
	from ttk import *
	from nightmarehelper import *
except ImportError:
	sys.exit("An error occured. Make sure Python 2.7 is installed correctly.")		

hardware = 0x8000000

root = Tk()
rompath = StringVar()
modulepath = StringVar()
writeoffset = StringVar()
bakvar = BooleanVar(root, value = True)
updatevar = BooleanVar(root, value = True)
size = IntVar()
obo = BooleanVar(root, value = False)


def replaceData(replacew, data, night):
	global hardware, obo
	search4 = night.offset | hardware
	print(hex(replacew))
	search = (struct.pack('<I', search4))
	replacement = (struct.pack('<I', replacew))
	data = str(data)
	c = data.find(search)
	if c == -1:
		search = (struct.pack('<I', search4 - night.size))
		obo.set(True)
	data = data.replace(search, replacement)
	return data
	
def setDataSize(integer):
	global size
	if integer <= 0x100:
		size.set(2**8)
	elif integer <= 0x10000:
		size.set(2**16)
	else:
		size.set(2**32)
	
def main():
	root.title('FEGBA Table Repointer')
	root.geometry('400x200+200+200')
	root.resizable(0,0)
	label = Label(root, text = 'ROM').grid(column = 0, row = 0, sticky = 'W')
	entry = Entry(root, text = rompath, textvariable = rompath, width = 45).grid(column = 1, row = 0, columnspan = 3)
	brws = Button(root, text = 'Browse', cursor = 'hand2', command = getFile, width = 58 - 45).grid(column = 4, row = 0, sticky = 'E')
	label2 = Label(root, text = 'NMM').grid(column = 0, row = 1, sticky = 'W')
	entry2 = Entry(root, text = modulepath, textvariable = modulepath, width = 45).grid(column = 1, row = 1, columnspan = 3)
	brws2 = Button(root, text = 'Browse', cursor = 'hand2', command = getModule, width = 58 - 45).grid(column = 4, row = 1, sticky = 'E')
	label3 = Label(root, text = 'Offset').grid(column = 0, row = 2, sticky = 'W')
	entry3 = Entry(root, textvariable = writeoffset, width = 59).grid(column = 1, row = 2, columnspan = 100, sticky = 'W')
	bak = Checkbutton(root, text = 'Make a backup(.bak)?', variable = bakvar).grid(column = 0, row = 5, columnspan = 10)
	up = Checkbutton(root, text = 'Update nightmare module when done?', variable = updatevar).grid(column = 0, row = 6, columnspan = 10)
	buffer = Label(root, text = '').grid(column = 0, row = 4, sticky = 'W')
	sz = Label(root, text = 'Size').grid(column = 0, row = 3, sticky = 'W')
	for i in range(0,3):
		rads = Radiobutton(root, text = str(2**(3+i)), cursor = 'hand2', variable = size, value = (2**((i+1)*8))).grid(column = i+2, row = 3, sticky = 'W')	
	buffer = Label(root, text = '').grid(column = 0, row = 7, sticky = 'W')
	next = Button(root, text = 'Process', cursor = 'hand2', command = Process).grid(column = 0, row = 8, columnspan = 10)
	root.mainloop()
		
def getFile():
	path = tkFileDialog.askopenfilename(title = 'Choose ROM Image', filetypes=[('GBA ROMs','*.gba'), ('All files','*.*')])
	rompath.set(path)

def getModule():
	path = tkFileDialog.askopenfilename(title = 'Choose the corresponding nightmare module', filetypes=[('Nightmare modules','*.nmm')])
	modulepath.set(path)
	try:
		i = open(path)
		s = i.readlines()
		i.close()
		n = nightmaredata(s)
		setDataSize(n.entries)
		
	except:
		pass
		
		
def Process():
	global rompath, modulepath, writeoffset, hardware, size, obo
	if rompath.get() == '' or modulepath.get() == '' or writeoffset.get() == '':
		tkMessageBox.showerror('Oi!', 'Fill out all the info first!')
	else:
		rp = rompath.get()
		mp = modulepath.get()
		try:
			rom = open(rp, 'rb')
		except IOError:
			tkMessageBox.showerror('No ROM', rp + ' not found')
			return -1
		try:
			open(mp, 'rb')
		except IOError:
			tkMessageBox.showerror('No module', modulepath.get() + ' not found')
			return -1
		try:
			address = int(writeoffset.get(), 16) 
		except ValueError:
			tkMessageBox.showerror('I am error', 'Invalid offset value. Only base 16 integers.')
			return -1
		data = rom.read()
		data = str(data)
		try:
			version = int(data[0xAE], 16)
			edited = False
		except ValueError:
			if not tkMessageBox.askyesno("Tsk tsk", "You shouldn't edit the ROM header. Are you sure the module matches the ROM?\nIf you made a mistake it could, and likely will, destroy your ROM."):
				return -1
			edited = True
		nightmare = createNightmareObject(modulepath.get())
		total = address + nightmare.length
		if total >= 0x2000000:
			tkMessageBox.showerror("It's over 9000!", 'Offset is too big, it has to be enough to accomodate a table without going over 32MB. The biggest offset you can use to fit your table is ' + hex(0x2000000 - nightmare.length))
			return -1 
		game = nightmare.getGame()
		if str(game) != str(version) and not edited:
			if game == '':
				if not tkMessageBox.askyesno("Continue?", "Couldn't validate game from the nightmare module. Are you sure this module corresponds to this game?"):
					return -1
			elif not tkMessageBox.askyesno('Uh oh', 'The ROM header and game specified in the module don\'t match.\nIf you made a mistake it could, and likely will, destroy your ROM.\nContinue anyway?\nThe module is for FE' + str(game) + '. The game is FE' + str(version)):
				return -1
		if bakvar.get():
			while True:
				try:
					backuppath = tkFileDialog.asksaveasfilename(title = 'Save your backup', filetypes=[('Backups','*.bak')])
					backup = open(backuppath, 'wb')
					rom = open(rp, 'rb')
					temp = rom.read()
					backup.write(temp)
					backup.close()
					break
				except IOError:
					if not tkMessageBox.askyesno('Oi!', 'No filepath given. Do you want to try again?'):
						break
		pointer = address | hardware
		search4 = nightmare.offset | hardware
		search = (struct.pack('<I', search4))
		replacement = (struct.pack('<I', pointer))
		data = str(data)
		c = data.find(search)
		if c == -1:
			search = (struct.pack('<I', search4 - nightmare.size))
			obo.set(True)
		data = data.replace(search, replacement)
		start = nightmare.offset
		if obo.get():
			start -= nightmare.size
		'''
		rom.seek(start)
		table = rom.read(nightmare.length)
		rom.seek(address)
		rep = rom.read(nightmare.length)
		#if len(rep) < len(table):
		'''
		data = list(data)
		if total > len(data):#os.path.getsize(rp):
			if tkMessageBox.askyesno('Expand ROM', 'Moving the table to this offset will require changing the file size\nContinue?'):
				#k = []
				tkMessageBox.showinfo('Hold', 'This\'ll take some time, so be patient.')
				for i in range(0,(total + nightmare.length - len(data))):
					data.append('\0')
				'''
				r = open(rp, 'rb')
				temprom = r.read()
				r.close()
				r = open(rp, 'wb')
				scatch = temprom + ''.join(k)
				r.write(scratch)
				r.close()
				rep = data[address:]
				'''
			else:
				tkMessageBox.showerror("No go", 'Repointing aborted')
				return -1
		#data = data.replace(rep, table)
		#l = list(data)
		rom.seek(start)
		table = rom.read(nightmare.length)
		rom.close()
		data[address:address+len(table)] = list(table)
		data = ''.join(data)
		rom = open(rp, 'wb')
		rom.write(data)
		rom.close()
		if updatevar.get():
			nightmare.offset = address
			if obo.get():
				nightmare.offset += nightmare.size
			nightmare.entries = size.get()
			nightmare.writeOnto(mp)
			tkMessageBox.showinfo("Success", "Nightmare module updated successfully.")
		tkMessageBox.showinfo("Success", "Table repointed from " + hex(start) + " to " + hex(address))
		writeoffset.set(hex(address + nightmare.size*size.get()))
		return 0
		
if __name__ == '__main__':
	main()
