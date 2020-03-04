import serial

MAX_FRAME_SIZE = 200
MESSAGE_HISTORY_SIZE = 5

##################################################

class File:
	def __init__(self, max_len):
		self.array = []
		self.max_len = max_len

	def push(self, data):
		self.array.append(data)
		while(len(self.array) > self.max_len):
			self.pop()

	def pop(self):
		data = self.array[0]
		self.array = self.array[1:]
		return data

##################################################

class CDRSerial:
	def __init__(self, portname, baud):
		# standard python serial port
		self.ser = serial.Serial(portname, baud, timeout=2)

		self.xbee_id = 0

		self.buffers = [[], [], [], []]

		self.file = File(MESSAGE_HISTORY_SIZE)

		self.buffer_r = [[], [], [], []]
		self.buffer_s = [0, 0, 0, 0, 0, 0]

		self.charWaiting = []
	
	def close(self):
		self.ser.close()



	def send(self, message):
		for i in range(len(message)):
			self.__send_data(message[i])
	
	def available(self):
		return len(self.file.array) > 0

	def get_message(self):
		if(len(self.file.array) > 0):
			return self.file.pop()
		else:
			return []

	def update_serial(self):
		while(self.ser.in_waiting > 0):
			self.__on_receive()

		self.__traitement_data_received()

	def set_xbee_id(self, id):
		self.xbee_id = 0b11 & id


	def __on_receive(self):
		c = self.ser.read()

	def __data2char(self, data):
		self.buffer_s[5] = (self.xbee_id & 0b11000000) | ((data) & 0b00111111)
		self.buffer_s[4] = (self.xbee_id & 0b11000000) | ((data >> 6) & 0b00111111)
		self.buffer_s[3] = (self.xbee_id & 0b11000000) | ((data >> 12) & 0b00111111)
		self.buffer_s[2] = (self.xbee_id & 0b11000000) | ((data >> 18) & 0b00111111)
		self.buffer_s[1] = (self.xbee_id & 0b11000000) | ((data >> 24) & 0b00111111)
		self.buffer_s[0] = (self.xbee_id & 0b11000000) | ((data >> 30) & 0b00000011)

	def __char2data(self, address):
		data = 0

		for i in range(len(self.buffer_r[address])):
			data = data | (self.buffer_r[address][5-i] << (6*i))
		
		self.buffers[address].append(data)

		if(self.buffers[address][-1] == -1):
			self.file.push(self.buffers[address])
			self.buffers[address] = []

	def __send_data(self, data):
		self.__data2char(data)
		for i in range(6):
			self.ser.write(bytearray([self.buffer_s[i]]))

	def __traitement_data_received(self):
		while(len(self.charWaiting) > 0):
			address = (self.charWaiting[-1] & 0b11000000) >> 6

			if(len(self.buffer_r[address]) == 5):
				# il s'agit du dernier char de la trame
				self.__push_to_buffer_r(address, self.charWaiting[-1] & 0b00111111)
				self.__char2data(address)
				self.buffer_r[address] = 0
			else:
				self.__push_to_buffer_r(address, self.charWaiting[-1] & 0b00111111)
			
			self.charWaiting = self.charWaiting[:len(self.charWaiting)-1]

	def __push_to_buffer_r(self, address, value):
		if(0 <= address and address < 4 and len(self.buffer_r[address]) <= 5):
			self.buffer_r[address].append(value)