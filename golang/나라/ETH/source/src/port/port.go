package port

var አካባቢ_2 uint16 = 1

type TPort struct {
	portnumber uint16
}

type TPort8bit struct {
	TPort
	ማንበቢያcount	uint16
	መጻፊያcount	uint16
}

func (self *TPort8bit) Init(portnumber uint16) {
	self.portnumber = portnumber
	self.ማንበቢያcount = 65
	self.መጻፊያcount = 65
}
func (self *TPort8bit) Wመጻፊያ(data uint8) {
	Portውጪbyte(self.portnumber, data)
}
func (self *TPort8bit) Rማንበቢያ() uint8 {
	var result = Portውስጥbyte(self.portnumber)
	return result
}
func Portመጻፊያbyte(portnumber uint16, data uint8) {
	Portውጪbyte(portnumber, data)
}
func Portማንበቢያbyte(portnumber uint16) uint8 {
	result := Portውስጥbyte(portnumber)
	return result
}

type TPort16bit struct {
	TPort
}

func (self *TPort16bit) Init(portnumber uint16) {
	self.TPort.portnumber = portnumber
}
func (self *TPort16bit) Wመጻፊያ(data uint16) {
	Portውጪቃላት(self.TPort.portnumber, data)
}
func (self *TPort16bit) Rማንበቢያ() uint16 {
	var result = Portውስጥቃላት(self.TPort.portnumber)
	return result
}
func Portመጻፊያቃላት(portnumber uint16, data uint16) {
	Portውጪቃላት(portnumber, data)
}
func Portማንበቢያቃላት(portnumber uint16) uint16 {
	var result uint16 = Portውስጥቃላት(portnumber)
	return result
}

type TPort32bit struct {
	TPort
}

func (self *TPort32bit) Init(portnumber uint16) {
	self.TPort.portnumber = portnumber
}
func (self *TPort32bit) Wመጻፊያ(data uint32) {
	Portውጪdword(self.TPort.portnumber, data)
}
func (self *TPort32bit) Rማንበቢያ() {
	Portውስጥdword(self.TPort.portnumber)
}
func Portመጻፊያdword(portnumber uint16, data uint32) {
	Portውጪdword(portnumber, data)
}
func Portማንበቢያdword(portnumber uint16) uint32 {
	var result uint32 = Portውስጥdword(portnumber)
	return result
}

var ማንበቢያcount uint16 = 65
var መጻፊያcount uint16 = 66

func Portውጪbyte(portnumber uint16, data uint8)
func Portውስጥbyte(portnumber uint16) uint8

func Portውጪቃላት(portnumber uint16, data uint16)
func Portውስጥቃላት(portnumber uint16) uint16

func Portውጪdword(portnumber uint16, data uint32)
func Portውስጥdword(portnumber uint16) uint32
