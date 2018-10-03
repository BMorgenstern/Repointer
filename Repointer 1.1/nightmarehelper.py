class nightmaredata:
	version = 0
	desc = ''
	offset = 0
	entries = 0
	size = 0
	length = 0
	originaloffset = ''
	originalentries = ''
	def __init__(self, list1):
		i = 0
		while 1:
			try:
				self.version = int(list1[i], getBase(list1[i]))
				break
			except ValueError:
				i += 1
		while 1:
			try:
				self.desc = str(list1[i+1])
				break
			except ValueError:
				i += 1
		while 1:
			try:
				self.offset = int(list1[i+2], getBase(list1[i+2]))
				self.originaloffset = list1[i+2]
				break
			except ValueError:
				i += 1			
		while 1:
			try:
				self.entries = int(list1[i+3], getBase(list1[i+3]))
				self.originalentries = list1[i+3]
				break
			except ValueError:
				i += 1			
		while 1:
			try:
				self.size = int(list1[i+4], getBase(list1[i+4]))
				break
			except ValueError:
				i += 1			
		self.length = self.size * self.entries
		
	def getGame(self):
		c = self.desc.split()
		for i in range(0, len(c)):
			s = c[i].lower()
			if 'fe' in s:
				return str(c[i][2])
		return ''
		
	def writeOnto(self, path):
		u = open(path, 'r')
		s = u.read()
		u.close()
		s = s.replace(self.originaloffset, hex(self.offset)+'\n', 1)
		s = s.replace(self.originalentries, str(self.entries)+'\n', 1)
		u = open(path, 'w')
		u.write(s)
		u.close()
		
		

def getBase(a):
	a = str(a)
	if '0x' in a:
		return 16
	else:
		return 10

def getNighmareIndex(s):
	i = 0
	for i in range(0, len(s)):
		try:
			temp = int(s[i])
			return i
		except ValueError:
			pass

def createNightmareObject(string):
	u = open(string, 'r')
	s = u.readlines()
	u.close()
	return nightmaredata(s[getNighmareIndex(s):])
			
def main():
	try:
		g = createNightmareObject('(6).nmm')
	except IOError:
		return -1
	print("Version is " + hex(g.version))
	print('Description is ' + g.desc)
	print('offset is ' + hex(g.offset))
	print('entries is ' + hex(g.entries))
	raw_input('size is ' + hex(g.size))

if __name__ == '__main__':
	main()