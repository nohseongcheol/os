package port

var pos uint16 = 1

type TPort struct {
	portnumber uint16
}

type TPort8Bit struct {
	TPort
	read_count	uint16
	write_count	uint16
}

func (self *TPort8Bit) Vआरंभ_करना(portnumber uint16) {
	self.portnumber = portnumber
	self.read_count = 65
	self.write_count = 65
}
func (self *TPort8Bit) Vलिखना(data uint8) {
	PortOutByte(self.portnumber, data)
}
func (self *TPort8Bit) Vपढ़ना() uint8 {
	var result = PortInByte(self.portnumber)
	return result
}
func PortWriteByte(portnumber uint16, data uint8) {
	PortOutByte(portnumber, data)
}
func PortReadByte(portnumber uint16) uint8 {
	result := PortInByte(portnumber)
	return result
}

type TPort16Bit struct {
	TPort
}

func (self *TPort16Bit) Vआरंभ_करना(portnumber uint16) {
	self.TPort.portnumber = portnumber
}
func (self *TPort16Bit) Vलिखना(data uint16) {
	PortOutWord(self.TPort.portnumber, data)
}
func (self *TPort16Bit) Vपढ़ना() uint16 {
	var result = PortInWord(self.TPort.portnumber)
	return result
}
func PortWriteWord(portnumber uint16, data uint16) {
	PortOutWord(portnumber, data)
}
func PortReadWord(portnumber uint16) uint16 {
	var result uint16 = PortInWord(portnumber)
	return result
}

type TPort32Bit struct {
	TPort
}

func (self *TPort32Bit) Vआरंभ_करना(portnumber uint16) {
	self.TPort.portnumber = portnumber
}
func (self *TPort32Bit) Vलिखना(data uint32) {
	PortOutDword(self.TPort.portnumber, data)
}
func (self *TPort32Bit) Vपढ़ना() {
	PortInDword(self.TPort.portnumber)
}
func PortWriteDword(portnumber uint16, data uint32) {
	PortOutDword(portnumber, data)
}
func PortReadDword(portnumber uint16) uint32 {
	var result uint32 = PortInDword(portnumber)
	return result
}

var read_count uint16 = 65
var write_count uint16 = 66

func PortOutByte(portnumber uint16, data uint8)
func PortInByte(portnumber uint16) uint8

func PortOutWord(portnumber uint16, data uint16)
func PortInWord(portnumber uint16) uint16

func PortOutDword(portnumber uint16, data uint32)
func PortInDword(portnumber uint16) uint32
