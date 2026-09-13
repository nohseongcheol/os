package port

var position uint16 = 1

type TPort struct {
	portnumber uint16
}

type TPort8bit struct {
	TPort
	licount		uint16
	ekricount	uint16
}

func (self *TPort8bit) Init(portnumber uint16) {
	self.portnumber = portnumber
	self.licount = 65
	self.ekricount = 65
}
func (self *TPort8bit) Ekri(data uint8) {
	Portoutbyte(self.portnumber, data)
}
func (self *TPort8bit) Li() uint8 {
	var result = Portinbyte(self.portnumber)
	return result
}
func Portekribyte(portnumber uint16, data uint8) {
	Portoutbyte(portnumber, data)
}
func Portlibyte(portnumber uint16) uint8 {
	result := Portinbyte(portnumber)
	return result
}

type TPort16bit struct {
	TPort
}

func (self *TPort16bit) Init(portnumber uint16) {
	self.TPort.portnumber = portnumber
}
func (self *TPort16bit) Ekri(data uint16) {
	Portoutword(self.TPort.portnumber, data)
}
func (self *TPort16bit) Li() uint16 {
	var result = Portinword(self.TPort.portnumber)
	return result
}
func Portekriword(portnumber uint16, data uint16) {
	Portoutword(portnumber, data)
}
func Portliword(portnumber uint16) uint16 {
	var result uint16 = Portinword(portnumber)
	return result
}

type TPort32bit struct {
	TPort
}

func (self *TPort32bit) Init(portnumber uint16) {
	self.TPort.portnumber = portnumber
}
func (self *TPort32bit) Ekri(data uint32) {
	Portoutdword(self.TPort.portnumber, data)
}
func (self *TPort32bit) Li() {
	Portindword(self.TPort.portnumber)
}
func Portekridword(portnumber uint16, data uint32) {
	Portoutdword(portnumber, data)
}
func Portlidword(portnumber uint16) uint32 {
	var result uint32 = Portindword(portnumber)
	return result
}

var licount uint16 = 65
var ekricount uint16 = 66

func Portoutbyte(portnumber uint16, data uint8)
func Portinbyte(portnumber uint16) uint8

func Portoutword(portnumber uint16, data uint16)
func Portinword(portnumber uint16) uint16

func Portoutdword(portnumber uint16, data uint32)
func Portindword(portnumber uint16) uint32
