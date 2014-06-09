import serial

class Fatek:
  def __init__(self, port = '/dev/ttyUSB1', station_no = '01'):
    self.ser = serial.Serial(
      port,
      bytesize=7,
      parity=serial.PARITY_EVEN
    )
    self.station_no = station_no

  @classmethod
  def _lrc(cls, string):
    lrc = 0
    for char in string:
      lrc += ord(char)
    return hex(lrc & 0xff)[2:].upper()

  def readline(self):
    char = ''
    string = ""
    while True:
      char = self.ser.read(1).decode()
      if char != '\x03':
        string += char
      else:
        break
    return string

  def send(self, command, data = ''):
    string = '\x02' + self.station_no + command + data
    self.ser.write((string + Fatek._lrc(string) + '\x03').encode())
    response = self.readline()[1:-2]
    return dict(
      station = response[0:2],
      command = response[2:4],
      error = response[4:5],
      data = response[5:]
    )

  def run(self):
    print(self.send('41', '1'))

  def stop(self):
    print(self.send('41', '0'))
