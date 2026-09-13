package port

var position uint16 = 1

type TPort struct {
	portnumber uint16
}

type TPort8bit struct {
	TPort
	kiyavimacount	uint16
	livimacount	uint16
}

func (self *TPort8bit) Init(portnumber uint16) {
	self.portnumber = portnumber
	self.kiyavimacount = 65
	self.livimacount = 65
}
func (self *TPort8bit) Livima(data uint8) {
	Portoutbyte(self.portnumber, data)
}
func (self *TPort8bit) Kiyavima() uint8 {
	var result = Portinbyte(self.portnumber)
	return result
}
func Portlivimabyte(portnumber uint16, data uint8) {
	Portoutbyte(portnumber, data)
}
func Portkiyavimabyte(portnumber uint16) uint8 {
	result := Portinbyte(portnumber)
	return result
}

type TPort16bit struct {
	TPort
}

func (self *TPort16bit) Init(portnumber uint16) {
	self.TPort.portnumber = portnumber
}
func (self *TPort16bit) Livima(data uint16) {
	Portoutවචන(self.TPort.portnumber, data)
}
func (self *TPort16bit) Kiyavima() uint16 {
	var result = Portinවචන(self.TPort.portnumber)
	return result
}
func Portlivimaවචන(portnumber uint16, data uint16) {
	Portoutවචන(portnumber, data)
}
func Portkiyavimaවචන(portnumber uint16) uint16 {
	var result uint16 = Portinවචන(portnumber)
	return result
}

type TPort32bit struct {
	TPort
}

func (self *TPort32bit) Init(portnumber uint16) {
	self.TPort.portnumber = portnumber
}
func (self *TPort32bit) Livima(data uint32) {
	Portoutdword(self.TPort.portnumber, data)
}
func (self *TPort32bit) Kiyavima() {
	Portindword(self.TPort.portnumber)
}
func Portlivimadword(portnumber uint16, data uint32) {
	Portoutdword(portnumber, data)
}
func Portkiyavimadword(portnumber uint16) uint32 {
	var result uint32 = Portindword(portnumber)
	return result
}

var kiyavimacount uint16 = 65
var livimacount uint16 = 66

func Portoutbyte(portnumber uint16, data uint8)
func Portinbyte(portnumber uint16) uint8

func Portoutවචන(portnumber uint16, data uint16)
func Portinවචන(portnumber uint16) uint16

func Portoutdword(portnumber uint16, data uint32)
func Portindword(portnumber uint16) uint32
