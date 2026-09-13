package port

var position uint16 = 1

type TPort struct {
	portnumber uint16
}

type TPort8bit struct {
	TPort
	kiyuncount	uint16
	liyuncount	uint16
}

func (self *TPort8bit) Init(portnumber uint16) {
	self.portnumber = portnumber
	self.kiyuncount = 65
	self.liyuncount = 65
}
func (self *TPort8bit) Liyun(data uint8) {
	Portoutbyte(self.portnumber, data)
}
func (self *TPort8bit) Kiyun() uint8 {
	var result = Portinbyte(self.portnumber)
	return result
}
func Portliyunbyte(portnumber uint16, data uint8) {
	Portoutbyte(portnumber, data)
}
func Portkiyunbyte(portnumber uint16) uint8 {
	result := Portinbyte(portnumber)
	return result
}

type TPort16bit struct {
	TPort
}

func (self *TPort16bit) Init(portnumber uint16) {
	self.TPort.portnumber = portnumber
}
func (self *TPort16bit) Liyun(data uint16) {
	Portoutword(self.TPort.portnumber, data)
}
func (self *TPort16bit) Kiyun() uint16 {
	var result = Portinword(self.TPort.portnumber)
	return result
}
func Portliyunword(portnumber uint16, data uint16) {
	Portoutword(portnumber, data)
}
func Portkiyunword(portnumber uint16) uint16 {
	var result uint16 = Portinword(portnumber)
	return result
}

type TPort32bit struct {
	TPort
}

func (self *TPort32bit) Init(portnumber uint16) {
	self.TPort.portnumber = portnumber
}
func (self *TPort32bit) Liyun(data uint32) {
	Portoutdword(self.TPort.portnumber, data)
}
func (self *TPort32bit) Kiyun() {
	Portindword(self.TPort.portnumber)
}
func Portliyundword(portnumber uint16, data uint32) {
	Portoutdword(portnumber, data)
}
func Portkiyundword(portnumber uint16) uint32 {
	var result uint32 = Portindword(portnumber)
	return result
}

var kiyuncount uint16 = 65
var liyuncount uint16 = 66

func Portoutbyte(portnumber uint16, data uint8)
func Portinbyte(portnumber uint16) uint8

func Portoutword(portnumber uint16, data uint16)
func Portinword(portnumber uint16) uint16

func Portoutdword(portnumber uint16, data uint32)
func Portindword(portnumber uint16) uint32
