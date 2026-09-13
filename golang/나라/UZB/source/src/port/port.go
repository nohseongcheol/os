package port

var holati uint16 = 1

type TPort struct {
	portnumber uint16
}

type TPort8bit struct {
	TPort
	oʻqishcount	uint16
	yozishcount	uint16
}

func (self *TPort8bit) Init(portnumber uint16) {
	self.portnumber = portnumber
	self.oʻqishcount = 65
	self.yozishcount = 65
}
func (self *TPort8bit) Yozish(data uint8) {
	PortUzoqlashtirishbyte(self.portnumber, data)
}
func (self *TPort8bit) Oʻqish() uint8 {
	var result = PortYaqinlashtirishbyte(self.portnumber)
	return result
}
func PortYozishbyte(portnumber uint16, data uint8) {
	PortUzoqlashtirishbyte(portnumber, data)
}
func PortOʻqishbyte(portnumber uint16) uint8 {
	result := PortYaqinlashtirishbyte(portnumber)
	return result
}

type TPort16bit struct {
	TPort
}

func (self *TPort16bit) Init(portnumber uint16) {
	self.TPort.portnumber = portnumber
}
func (self *TPort16bit) Yozish(data uint16) {
	PortUzoqlashtirishsoz(self.TPort.portnumber, data)
}
func (self *TPort16bit) Oʻqish() uint16 {
	var result = PortYaqinlashtirishsoz(self.TPort.portnumber)
	return result
}
func PortYozishsoz(portnumber uint16, data uint16) {
	PortUzoqlashtirishsoz(portnumber, data)
}
func PortOʻqishsoz(portnumber uint16) uint16 {
	var result uint16 = PortYaqinlashtirishsoz(portnumber)
	return result
}

type TPort32bit struct {
	TPort
}

func (self *TPort32bit) Init(portnumber uint16) {
	self.TPort.portnumber = portnumber
}
func (self *TPort32bit) Yozish(data uint32) {
	PortUzoqlashtirishdword(self.TPort.portnumber, data)
}
func (self *TPort32bit) Oʻqish() {
	PortYaqinlashtirishdword(self.TPort.portnumber)
}
func PortYozishdword(portnumber uint16, data uint32) {
	PortUzoqlashtirishdword(portnumber, data)
}
func PortOʻqishdword(portnumber uint16) uint32 {
	var result uint32 = PortYaqinlashtirishdword(portnumber)
	return result
}

var oʻqishcount uint16 = 65
var yozishcount uint16 = 66

func PortUzoqlashtirishbyte(portnumber uint16, data uint8)
func PortYaqinlashtirishbyte(portnumber uint16) uint8

func PortUzoqlashtirishsoz(portnumber uint16, data uint16)
func PortYaqinlashtirishsoz(portnumber uint16) uint16

func PortUzoqlashtirishdword(portnumber uint16, data uint32)
func PortYaqinlashtirishdword(portnumber uint16) uint32
