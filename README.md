# Repointer

FEGBA Table Repointer by Brendan Morgenstern AKA Brendor V 1.1 1/9/16

A python file that repoints data tables in FEGBA ROMs given a nightmare module to reference.

Firstly, to use this software, you need Python 2.7 installed on your computer. It can be downloaded from the link below.
https://www.python.org/downloads/release/python-2711/

The main program is "Repoint.pyw", if Python 2.7 is installed correctly, all you have to do is run this file.

The user needs to input three pieces of information:
The path to the Fire Emblem ROM:
	This should be self explanatory, just select the ROM file to modify via the Browse button 
The path to the nightmare module to read off of:
	Everything is handled via the input nightmare module as far as the location of the table what type of table it is etc. 
	Just select the module that modifies the table you want to repoint eg Item Editor to repoint the item table. Pretty simple.
The offset of the new table:
	Also really simple, just the offset you want the new table to live in hexadecimal (0x)

There is also a size option which tells the repointer how big the indices for the table should be in bits. 
This is set automatically when you select a nightmare module, so don't worry about this.

There are 2 options available for the process denoted by checkboxes which are selected by default. 

Create a backup:
	Select this option if you want to create a backup of the ROM file before processing. 
	You'll be given a dialogue to save the file	wherever and with whatever name you want.
Update module when done:
	If this is selected, the input nightmare module will automatically be updated with the new offset and max index

Once all the info is put in, just click "Process" at the bottom and let the program do all the work.

If you experience any bugs or have a question, I can be contacted at brendanmorgenstern@gmail.com .

Additional notes:

Because this program reads off of nightmare modules, this program can be used to repoint tables in other ROMs as well, 
even x86 applications, as long as the nightmare module used follows the proper format as described below.

"The first line holds the module file version. For this file, that's "1". No decimal points or anything fancy.

The second line is the module description, which appears on the title bar when the module is loaded.

The third line is the root address of the data table.

The fourth line is the number of table entries.

The fifth line is the length of a single entry."
