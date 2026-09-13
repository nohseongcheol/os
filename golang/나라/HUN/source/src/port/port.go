package port

var pozíció uint16 = 1

type TPort struct {
	portnumber uint16
}

type TPort8bit struct {
	TPort
	olvasásSzámláló	uint16
	írásSzámláló	uint16
}

func (self *TPort8bit) Init(portnumber uint16) {
	self.portnumber = portnumber
	self.olvasásSzámláló = 65
	self.írásSzámláló = 65
}
func (self *TPort8bit) Írás(data uint8) {
	PortKibyte(self.portnumber, data)
}
func (self *TPort8bit) Olvasás() uint8 {
	var result = PortBebyte(self.portnumber)
	return result
}
func PortÍrásbyte(portnumber uint16, data uint8) {
	PortKibyte(portnumber, data)
}
func PortOlvasásbyte(portnumber uint16) uint8 {
	result := PortBebyte(portnumber)
	return result
}

type TPort16bit struct {
	TPort
}

func (self *TPort16bit) Init(portnumber uint16) {
	self.TPort.portnumber = portnumber
}
func (self *TPort16bit) Írás(data uint16) {
	PortKiszó(self.TPort.portnumber, data)
}
func (self *TPort16bit) Olvasás() uint16 {
	var result = PortBeszó(self.TPort.portnumber)
	return result
}
func PortÍrásszó(portnumber uint16, data uint16) {
	PortKiszó(portnumber, data)
}
func PortOlvasásszó(portnumber uint16) uint16 {
	var result uint16 = PortBeszó(portnumber)
	return result
}

type TPort32bit struct {
	TPort
}

func (self *TPort32bit) Init(portnumber uint16) {
	self.TPort.portnumber = portnumber
}
func (self *TPort32bit) Írás(data uint32) {
	PortKidword(self.TPort.portnumber, data)
}
func (self *TPort32bit) Olvasás() {
	PortBedword(self.TPort.portnumber)
}
func PortÍrásdword(portnumber uint16, data uint32) {
	PortKidword(portnumber, data)
}
func PortOlvasásdword(portnumber uint16) uint32 {
	var result uint32 = PortBedword(portnumber)
	return result
}

var olvasásSzámláló uint16 = 65
var írásSzámláló uint16 = 66

func PortKibyte(portnumber uint16, data uint8)
func PortBebyte(portnumber uint16) uint8

func PortKiszó(portnumber uint16, data uint16)
func PortBeszó(portnumber uint16) uint16

func PortKidword(portnumber uint16, data uint32)
func PortBedword(portnumber uint16) uint32
