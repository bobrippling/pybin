#!/usr/bin/python2

class BufReadException(Exception):
	def __init__(self, s):
		self.s = s

	def __str__(self):
		return self.s


class BufRead:
	def __init__(self, f):
		self.file = f
		self.buf = ''
                #f.setblocking(0)

	def fileno(self):
		return self.file.fileno()


	def bufLine(self, nl):
		ret = self.buf[0:nl]
		self.buf = self.buf[nl+1:]
		return ret


	def closed(self):
		raise BufReadException("BufObj Closed")


	def readData(self):
		# assuming file is a socket
		if self.file is None:
			self.closed()
		return self.file.recv(4096)


	def readLine(self):
		nl = self.buf.find('\n')
		if nl != -1:
			return self.bufLine(nl)

		self.buf += self.readData()

		if len(self.buf) == 0:
			self.close()
			return ''

		nl = self.buf.find('\n')
		if nl == -1:
			# FIXME: wait a bit and have a few tries
			raise BufReadException("No Newline")
		return self.bufLine(nl)


	def send(self, data):
		if self.file is None:
			self.closed()
		return self.file.send(data)


	def close(self):
		ret = self.file.close()
		self.file = None
		return ret
