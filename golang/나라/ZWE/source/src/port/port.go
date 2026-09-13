package port

var position uint16 = 1

type TPort struct {
	portnumber uint16
}

type TPort8bit struct {
	TPort
	verengacount	uint16
	nyoracount	uint16
}

func (self *TPort8bit) Init(portnumber uint16) {
	self.portnumber = portnumber
	self.verengacount = 65
	self.nyoracount = 65
}
func (self *TPort8bit) Nyora(data uint8) {
	Portoutbyte(self.portnumber, data)
}
func (self *TPort8bit) Verenga() uint8 {
	var result = Portinbyte(self.portnumber)
	return result
}
func Portnyorabyte(portnumber uint16, data uint8) {
	Portoutbyte(portnumber, data)
}
func Portverengabyte(portnumber uint16) uint8 {
	result := Portinbyte(portnumber)
	return result
}

type TPort16bit struct {
	TPort
}

func (self *TPort16bit) Init(portnumber uint16) {
	self.TPort.portnumber = portnumber
}
func (self *TPort16bit) Nyora(data uint16) {
	Portoutword(self.TPort.portnumber, data)
}
func (self *TPort16bit) Verenga() uint16 {
	var result = Portinword(self.TPort.portnumber)
	return result
}
func Portnyoraword(portnumber uint16, data uint16) {
	Portoutword(portnumber, data)
}
func Portverengaword(portnumber uint16) uint16 {
	var result uint16 = Portinword(portnumber)
	return result
}

type TPort32bit struct {
	TPort
}

func (self *TPort32bit) Init(portnumber uint16) {
	self.TPort.portnumber = portnumber
}
func (self *TPort32bit) Nyora(data uint32) {
	Portoutdword(self.TPort.portnumber, data)
}
func (self *TPort32bit) Verenga() {
	Portindword(self.TPort.portnumber)
}
func Portnyoradword(portnumber uint16, data uint32) {
	Portoutdword(portnumber, data)
}
func Portverengadword(portnumber uint16) uint32 {
	var result uint32 = Portindword(portnumber)
	return result
}

var verengacount uint16 = 65
var nyoracount uint16 = 66

func Portoutbyte(portnumber uint16, data uint8)
func Portinbyte(portnumber uint16) uint8

func Portoutword(portnumber uint16, data uint16)
func Portinword(portnumber uint16) uint16

func Portoutdword(portnumber uint16, data uint32)
func Portindword(portnumber uint16) uint32
