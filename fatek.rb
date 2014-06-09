require 'serialport'

class Fatek
  def initialize(port = '/dev/ttyUSB0', station_no = '01')
    @ser = SerialPort.new(
      port,
      data_bits: 7,
      parity: SerialPort::EVEN
    )
    @station_no = station_no
  end

  def self.lrc(string)
    (string.each_byte.reduce { |sum, byte| sum + byte } & 0xff)
      .to_s(16)
      .upcase()
  end

  def send(command, data = '')
    string = "\x02" + @station_no + command + data
    @ser.write(string + Fatek.lrc(string) + "\x03")
    response = @ser.read
    {
      station: response[1..2],
      command: response[3..4],
      error: response[5],
      data: response[6..-4]
    }
  end

  def run()
    self.send('41', '1')
  end

  def stop()
    self.send('41', '0')
  end

  private :lrc
end
