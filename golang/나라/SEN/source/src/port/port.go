package port

var position uint16 = 1

type TPort struct {
	portnumber uint16
}

type TPort8bit struct {
	TPort
	jàngcount	uint16
	bindcount	uint16
}

func (self *TPort8bit) Init(portnumber uint16) {
	self.portnumber = portnumber
	self.jàngcount = 65
	self.bindcount = 65
}
func (self *TPort8bit) Bind_2(data uint8) {
	Portoutbyte(self.portnumber, data)
}
func (self *TPort8bit) Jàng() uint8 {
	var result = Portinbyte(self.portnumber)
	return result
}
func Portbindbyte(portnumber uint16, data uint8) {
	Portoutbyte(portnumber, data)
}
func Portjàngbyte(portnumber uint16) uint8 {
	result := Portinbyte(portnumber)
	return result
}

type TPort16bit struct {
	TPort
}

func (self *TPort16bit) Init(portnumber uint16) {
	self.TPort.portnumber = portnumber
}
func (self *TPort16bit) Bind_2(data uint16) {
	Portoutword(self.TPort.portnumber, data)
}
func (self *TPort16bit) Jàng() uint16 {
	var result = Portinword(self.TPort.portnumber)
	return result
}
func Portbindword(portnumber uint16, data uint16) {
	Portoutword(portnumber, data)
}
func Portjàngword(portnumber uint16) uint16 {
	var result uint16 = Portinword(portnumber)
	return result
}

type TPort32bit struct {
	TPort
}

func (self *TPort32bit) Init(portnumber uint16) {
	self.TPort.portnumber = portnumber
}
func (self *TPort32bit) Bind_2(data uint32) {
	Portoutdword(self.TPort.portnumber, data)
}
func (self *TPort32bit) Jàng() {
	Portindword(self.TPort.portnumber)
}
func Portbinddword(portnumber uint16, data uint32) {
	Portoutdword(portnumber, data)
}
func Portjàngdword(portnumber uint16) uint32 {
	var result uint32 = Portindword(portnumber)
	return result
}

var jàngcount uint16 = 65
var bindcount uint16 = 66

func Portoutbyte(portnumber uint16, data uint8)
func Portinbyte(portnumber uint16) uint8

func Portoutword(portnumber uint16, data uint16)
func Portinword(portnumber uint16) uint16

func Portoutdword(portnumber uint16, data uint32)
func Portindword(portnumber uint16) uint32
